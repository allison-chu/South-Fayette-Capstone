from flask import Flask, jsonify, request, render_template, session, redirect, url_for
import os
import sqlite3
import random

app = Flask(__name__, template_folder='templates')
app.secret_key = 'my-super-secret-key'



class StudentDataAI:
    def __init__(self, api_key: str, db_path: str = "database.db"):
        self.api_key = api_key
        self.db_path = db_path
        self.client = None  # Optional: set up OpenAI if you plan to use it

    def get_user_id(self):
        if "currentStudent" not in session:
            return None
        current_student = session["currentStudent"]
        result = self._query_db("SELECT studentId FROM student_list WHERE name = ?", (current_student,))
        if result:
            return result[0]['studentId']
        return None

    def get_all_classes(self):
        return self._query_db("SELECT name, description, tags FROM classes")

    def get_all_extracurriculars(self):
        return self._query_db("SELECT name, description, tags FROM extracurriculars")

    def get_student_past(self, user_id):
        return self._query_db(
            "SELECT eventType, name, positiveReflection, negativeReflection, enjoymentRating, yearsCompleted "
            "FROM student_data WHERE studentId = ?", (user_id,)
        )

    def generate_ai_recommendations_classes(self, student_id, num_recommendations):
        try:
            history = self.get_student_past(student_id)
            preferences_row = self._query_db("SELECT interests FROM student_list WHERE studentId = ?", (student_id,))
            preferences = preferences_row[0]['interests'] if preferences_row else ""
            classes = self.get_all_classes()

            # naive matching: if student interests in tags
            preferred_classes = [
                cls for cls in classes
                if any(interest.strip().lower() in cls['tags'].lower()
                    for interest in preferences.split(","))
            ]

            if len(preferred_classes) < num_recommendations:
                # fill up with random ones (excluding already included)
                remaining = [c for c in classes if c not in preferred_classes]
                preferred_classes += random.sample(remaining, min(num_recommendations - len(preferred_classes), len(remaining)))

            return preferred_classes[:num_recommendations]

        except Exception as e:
            print(f"Error in generate_ai_recommendations_classes: {e}")
            return []


    def generate_ai_recommendations_activities(self, student_id, num_recommendations):
        try:
            preferences_row = self._query_db("SELECT interests FROM student_list WHERE studentId = ?", (student_id,))
            preferences = preferences_row[0]['interests'] if preferences_row else ""
            activities = self.get_all_extracurriculars()

            preferred_activities = [
                act for act in activities
                if any(interest.strip().lower() in act['tags'].lower()
                    for interest in preferences.split(","))
            ]

            if len(preferred_activities) < num_recommendations:
                remaining = [a for a in activities if a not in preferred_activities]
                preferred_activities += random.sample(remaining, min(num_recommendations - len(preferred_activities), len(remaining)))

            return preferred_activities[:num_recommendations]

        except Exception as e:
            print(f"Error in generate_ai_recommendations_activities: {e}")
            return []


    def _prepare_student_profile(self, history, preferences):
        profile = {
            "interests": preferences,
            "completed_things": []
        }

        for record in history:
            profile["completed_things"].append({
                "name": record["name"],
                "eventType": record["eventType"],
                "positiveReflection": record["positiveReflection"],
                "negativeReflection": record["negativeReflection"],
                "enjoymentRating": record["enjoymentRating"],
                "yearCompleted": record["yearsCompleted"]
            })

        return profile

    def _prepare_classes_data(self, classes):
        return [{
            "name": cls["name"],
            "description": cls["description"],
            "tags": cls["tags"]
        } for cls in classes]

    def _query_db(self, query, params=()):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Database error: {e}")
            return []


student_ai = StudentDataAI(api_key=os.getenv("openAI_api_key"), db_path="database.db")


@app.route("/")
def accounts():
    return render_template("accounts.html")


@app.route("/explore")
def explore():
    if "currentStudent" not in session:
        return redirect(url_for("accounts"))
    name = session["currentStudent"]

    student_record = student_ai._query_db(
        "SELECT name, email, interests, gradeLevel FROM student_list WHERE name = ?", (name,)
    )

    if not student_record:
        return "Student not found", 404

    student = student_record[0]  # first (and only) match

    return render_template("explore.html", student=student)








@app.route("/set_student", methods=["POST"])
def set_student():
    data = request.get_json()
    name = data.get("student")
    if not name:
        return jsonify({"error": "No student name provided"}), 400
    session["currentStudent"] = name
    return jsonify({"message": f"Student {name} selected."})



@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("accounts"))


@app.route("/recommendations", methods=["POST"])
def recommendations():
    user_id = student_ai.get_user_id()
    if not user_id:
        return jsonify({"error": "No user logged in"}), 400

    classes = student_ai.generate_ai_recommendations_classes(user_id, 3)
    activities = student_ai.generate_ai_recommendations_activities(user_id, 3)

    return jsonify({
        "classes": classes,
        "activities": activities
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
