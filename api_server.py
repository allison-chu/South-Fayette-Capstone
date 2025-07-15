from flask import Flask, jsonify, request, render_template
import os
import sqlite3
import random

app = Flask(__name__, template_folder='templates')

# your StudentDataAI class
class StudentDataAI:
    def __init__(self, api_key: str, db_path: str = "database.db"):
        self.api_key = api_key
        self.db_path = db_path

    def get_all_classes(self):
        return self._query_db("SELECT name, description, tags FROM classes")

    def get_all_extracurriculars(self):
        return self._query_db("SELECT name, description, tags FROM extracurriculars")

    def _query_db(self, query):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            conn.close()
            return [dict(zip(column_names, row)) for row in rows]
        except Exception as e:
            print(f"Database error: {e}")
            return []

student_ai = StudentDataAI(api_key=os.getenv("openAI_api_key"), db_path="database.db")

@app.route("/")
def home():
    return render_template("explore.html")

@app.route("/recommendations", methods=["POST"])
def recommendations():
    classes = student_ai.get_all_classes()
    activities = student_ai.get_all_extracurriculars()

    if len(classes) >= 3:
        classes = random.sample(classes, 3)
    if len(activities) >= 3:
        activities = random.sample(activities, 3)

    return jsonify({
        "classes": classes,
        "activities": activities
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # use PORT env or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)

