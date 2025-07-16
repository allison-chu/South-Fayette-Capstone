from flask import Flask, jsonify, request, render_template, session, redirect, url_for
import os
import sqlite3
import logging
import random

app = Flask(__name__, template_folder='templates')
app.secret_key = 'replace-me-with-a-secret'  # needed for session

class StudentDataAI:
    def __init__(self, api_key: str, db_path: str = "database.db"):
        self.api_key = api_key
        self.db_path = db_path

    userID = None
    def get_user_id(self):
        if "currentStudent" not in session:
            return None
        
        current_student = session["currentStudent"]
        result = self._query_db("SELECT id FROM student_list WHERE name = ?", (current_student))
        if result:
            return result[0]['id']
        return None 

    def get_all_classes(self):
        return self._query_db("SELECT name, description, tags FROM classes")

    def get_all_extracurriculars(self):
        return self._query_db("SELECT name, description, tags FROM extracurriculars")
    
    def get_student_past(self, userId):
        return self._query_db("SELECT eventType, name, positiveReflection, negativeReflection, enjoymentRating, yearsCompleted FROM student_data WHERE studentId = ?", (userId))


    def generate_ai_recommendations_classes(self, student_id, num_recommendations):
        try:
            history = self.get_student_past(student_id)
            preferences = self.query_db("SELECT interests FROM student_list WHERE studentId = ?", student_id)
            classes = student_ai.get_all_classes(self)

            student_profile = self._prepare_student_profile( history, preferences)
            classes_data = self._prepare_classes_data(classes)

            if self.client:
                recommendations = self._get_openai_recommendations(
                    student_profile, classes_data, num_recommendations
                )

            return {
                "classes": recommendations
            }
        
        except Exception as e:
            return {"error": "Failed to generate recommendations"}


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
                "yearCompleted": record["yearCompleted"]
            })

        return profile

    def _prepare_class_data(self, classes):
        return [{
            "className": 
        }]  

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
def accounts():
    return render_template("accounts.html")

@app.route("/explore")
def explore():
    if "currentStudent" not in session:
        return redirect(url_for("accounts"))
    return render_template("explore.html", current_student=session["currentStudent"])


@app.route("/set_student", methods=["POST"])
def set_student():
    data = request.json
    session["currentStudent"] = data.get("student")
    return jsonify({"status": "ok"})

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("accounts"))

@app.route("/recommendations", methods=["POST"])
def recommendations():
    classes = student_ai.get_all_classes()
    activities = student_ai.get_all_extracurriculars()
    userId = student_ai.get_user_id()
    studentPast = student_ai.get_student_past(userId)

    classes = student_ai.generate_ai_recommendations_classes(userId, 3)
    activities = student_ai.generate_ai_recommendations_activities(userId, 3)

    return jsonify({
        "classes": classes,
        "activities": activities
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
