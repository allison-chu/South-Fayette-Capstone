import os
import sqlite3
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, jsonify, request

# Load environment variables and get the api for the AI system
load_dotenv(dotenv_path='keys.env')
openai_key = os.getenv('openAI_api_key')

print("🚀 Running updated AI_system.py!")
print(f"🔑 OpenAI key loaded? {'Yes' if openai_key else 'No'}")

# sets up all the methods needed for the AI to access and understand the database
class StudentDataAI:

    # initiates the AI system and the database
    def __init__(self, api_key: str, db_path: str = "database.db"):
        self.api_key = api_key
        self.db_path = db_path
        if api_key:
            self.client = OpenAI(api_key=api_key)
            print("✅ OpenAI client initialized.")
        else:
            self.client = None
            print("⚠️ No OpenAI API key provided. Will use dummy data.")

    # gets all the data from the student_data datatable within the database
    def get_all_data(self) -> List[Dict]:
        return self._query_db("SELECT * FROM student_data")

    # gets all the data from the classes datatable within the database
    def get_all_classes(self) -> List[Dict]:
        return self._query_db("SELECT * FROM classes")

    # gets all the data from the extracurriculars datatable within the database
    def get_all_extracurriculars(self) -> List[Dict]:
        return self._query_db("SELECT * FROM extracurriculars")

    # allows the AI to search through the classes datatable
    def search_classes(self, criteria: Dict) -> List[Dict]:
        return self._search_db("classes", criteria)

    # allows the AI to search through the extracurriculars datatable
    def search_extracurriculars(self, criteria: Dict) -> List[Dict]:
        return self._search_db("extracurriculars", criteria)

    # provides the outline of the database, and how the different datatables relate to each other 
    def get_database_schema(self) -> Dict:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(student_data)")
            schema_info = cursor.fetchall()
            schema = {col[1]: col[2] for col in schema_info}
            conn.close()
            return schema
        except Exception as e:
            print(f"Database error: {e}")
            return {}

    # function that collects all the functions that the AI will have access to so that it can call them on its own
    def get_recommendations(self, query: str, context: str = "") -> str:
        if not self.client:
            print("⚠️ Using dummy recommendations because OpenAI client not initialized.")
            return self._dummy_recommendations()

        # teaches the AI about its role within the project and how it should act
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI educational advisor with access to a database. "
                    "Your goal is to make intelligent recommendations for classes and extracurricular activities. "
                    "ALWAYS respond in the following exact format and nothing else:\n\n"
                    "**Classes**:\n"
                    "- Class Name: brief description\n\n"
                    "**Extracurricular Activities**:\n"
                    "- Activity Name: brief description"
                )
            },
            {
                "role": "user",
                "content": f"Context: {context}\n\nQuery: {query}"
            }
        ]

        try:
            print("📡 Sending request to OpenAI…")
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            print("✅ OpenAI response received.")
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ OpenAI error: {e}")
            return self._dummy_recommendations()

    # dummy recommendations if no OpenAI API key is loaded
    def _dummy_recommendations(self) -> str:
        print("ℹ️ Returning dummy recommendations.")
        return """
**Classes**:
- Example Class 1: Learn something useful.
- Example Class 2: Another great course.

**Extracurricular Activities**:
- Example Club: Fun activity.
- Example Workshop: Hands-on learning.
"""

    # helper function to execute queries without criteria
    def _query_db(self, query: str) -> List[Dict]:
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

    # helper function to execute queries with criteria
    def _search_db(self, table: str, criteria: Dict) -> List[Dict]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            query = f"SELECT * FROM {table}"
            params = []
            if criteria:
                conditions = [f"{field} = ?" for field, value in criteria.items() if value is not None]
                params = [value for _, value in criteria.items() if value is not None]
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
            cursor.execute(query, params)
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            conn.close()
            return [dict(zip(column_names, row)) for row in rows]
        except Exception as e:
            print(f"Database error: {e}")
            return []


# sets up the flask app to expose the AI as a web API
app = Flask(__name__)
student_ai = StudentDataAI(api_key=openai_key, db_path="database.db")

# default route to confirm server is running
@app.route("/")
def home():
    return "✅ API is running!"

# route that the frontend calls to get recommendations
@app.route("/recommendations", methods=["POST"])
def recommendations():
    # get query from frontend
    data = request.get_json()
    query = data.get("query", "What classes or activities do you recommend?")
    # get AI recommendation based on query
    result = student_ai.get_recommendations(query)
    # send it back as JSON
    return jsonify({"result": result})

# runs the flask server if file is run directly
if __name__ == "__main__":
    app.run(debug=True)
