from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import sqlite3

# Load environment variables and get the API key for the AI system
load_dotenv("keys.env")
openai_key = os.getenv("openAI_api_key")

print("🚀 Running updated AI_system.py!")
print(f"🔑 OpenAI key loaded? {'Yes' if openai_key else 'No'}")

# sets up all the methods needed for the AI to access and understand the database
app = Flask(__name__)

class StudentDataAI:
    # initiates the AI system and the database
    def __init__(self, api_key: str, db_path: str = "database.db"):
        self.api_key = api_key
        self.db_path = db_path

    # gets all the data from the classes datatable within the database
    def get_all_classes(self):
        return self._query_db("SELECT name, description, tags FROM classes")

    # gets all the data from the extracurriculars datatable within the database
    def get_all_extracurriculars(self):
        return self._query_db("SELECT name, description, tags FROM extracurriculars")

    # helper function to execute a query and return rows as list of dicts
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

student_ai = StudentDataAI(api_key=openai_key, db_path="database.db")

# default route to confirm server is running
@app.route("/")
def home():
    return "✅ API is running!"

# route that the frontend calls to get recommendations
@app.route("/recommendations", methods=["POST"])
def recommendations():
    # Always fetch 3 classes & 3 activities from the database
    classes = student_ai.get_all_classes()[:3]
    activities = student_ai.get_all_extracurriculars()[:3]

    # send the data back as JSON
    return jsonify({
        "classes": classes,
        "activities": activities
    })

# runs the flask server if file is run directly
if __name__ == "__main__":
    app.run(debug=True)
