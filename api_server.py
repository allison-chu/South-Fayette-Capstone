from flask import Flask, jsonify, request, render_template, session, redirect, url_for
import sqlite3
import os
import difflib

app = Flask(__name__, template_folder='templates')
app.secret_key = 'super-secret-key'


class StudentDataAI:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def get_user_id(self):
        if "currentStudent" not in session:
            print("No currentStudent in session")
            return None

        current_student = session["currentStudent"].strip()
        print(f"Looking up studentId for: [{current_student}]")

        result = self._query_db("""
            SELECT studentId FROM student_list 
            WHERE LOWER(TRIM(name)) = LOWER(TRIM(?))
        """, (current_student,))
        if result:
            print(f"Found studentId: {result[0]['studentId']}")
            return result[0]['studentId']

        # Fallback: find closest name
        all_students = self._query_db("SELECT name FROM student_list")
        names = [row["name"].strip() for row in all_students]
        closest = difflib.get_close_matches(current_student, names, n=1, cutoff=0.4)
        if closest:
            print(f"🔗 Closest match: [{closest[0]}]")
            result = self._query_db("""
                SELECT studentId FROM student_list 
                WHERE LOWER(TRIM(name)) = LOWER(TRIM(?))
            """, (closest[0],))
            if result:
                return result[0]['studentId']

        print("No suitable student found.")
        return None

    def get_all_classes(self):
        return self._query_db("SELECT name, description, tags FROM classes")

    def get_all_extracurriculars(self):
        return self._query_db("SELECT name, description, tags FROM extracurriculars")

    def generate_ai_recommendations_classes(self, student_id, num):
        preferences_row = self._query_db("SELECT interests FROM student_list WHERE studentId = ?", (student_id,))
        preferences = preferences_row[0]['interests'] if preferences_row else ""
        classes = self.get_all_classes()

        preferred = [cls for cls in classes if any(
            i.strip().lower() in cls['tags'].lower() for i in preferences.split(","))]

        if len(preferred) < num:
            preferred += [c for c in classes if c not in preferred][:num - len(preferred)]
        return preferred[:num]

    def generate_ai_recommendations_activities(self, student_id, num):
        preferences_row = self._query_db("SELECT interests FROM student_list WHERE studentId = ?", (student_id,))
        preferences = preferences_row[0]['interests'] if preferences_row else ""
        activities = self.get_all_extracurriculars()

        preferred = [act for act in activities if any(
            i.strip().lower() in act['tags'].lower() for i in preferences.split(","))]

        if len(preferred) < num:
            preferred += [a for a in activities if a not in preferred][:num - len(preferred)]
        return preferred[:num]

    def _query_db(self, query, params=()):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]


student_ai = StudentDataAI()


@app.route("/")
def accounts():
    return render_template("accounts.html")


@app.route("/get_students")
def get_students():
    rows = student_ai._query_db("SELECT name, email FROM student_list")
    students = [
        {
            "name": r["name"],
            "email": r["email"],
            "pic": f"https://api.dicebear.com/6.x/adventurer/svg?seed={r['name'].split()[0]}"
        } for r in rows
    ]
    return jsonify(students)


@app.route("/get_interests")
def get_interests():
    rows = student_ai._query_db("SELECT tags FROM classes UNION ALL SELECT tags FROM extracurriculars")
    tags = set()
    for r in rows:
        tags.update(t.strip().lower() for t in r['tags'].split(","))
    return jsonify({"interests": sorted(tags)})


@app.route("/add_profile", methods=["POST"])
def add_profile():
    d = request.get_json()
    name = f"{d['firstName'].strip().title()} {d['lastName'].strip().title()}"
    email = f"{d['firstName'].strip().lower()}.{d['lastName'].strip().lower()}@school.org"
    interests = ", ".join([i.lower() for i in d['interests']])
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO student_list (name, interests, email, gradeLevel)
        VALUES (?, ?, ?, ?)""",
        (name, interests, email, "9"))
    conn.commit()
    conn.close()
    print(f"🎉 Added profile: [{name}]")
    return jsonify({"message": f"Profile [{name}] added!"})


@app.route("/set_student", methods=["POST"])
def set_student():
    d = request.get_json()
    session["currentStudent"] = d["student"]
    print(f"Current student: [{d['student']}]")
    return jsonify({"message": "Student set."})


@app.route("/explore")
def explore():
    if "currentStudent" not in session:
        return redirect(url_for("accounts"))

    name = session["currentStudent"]
    student = student_ai._query_db(
        "SELECT name, email, interests, gradeLevel FROM student_list WHERE LOWER(TRIM(name)) = LOWER(TRIM(?))", (name,))
    if not student:
        return "Student not found", 404

    return render_template("explore.html", student=student[0])


@app.route("/recommendations", methods=["POST"])
def recommendations():
    user_id = student_ai.get_user_id()
    if not user_id:
        return jsonify({"error": "No user logged in"}), 400

    classes = student_ai.generate_ai_recommendations_classes(user_id, 3)
    activities = student_ai.generate_ai_recommendations_activities(user_id, 3)

    return jsonify({"classes": classes, "activities": activities})

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("accounts"))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)

