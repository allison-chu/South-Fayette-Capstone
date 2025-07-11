import os
import json
import sqlite3
from typing import List, Dict

import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv(dotenv_path='keys.env')
openai_key = os.getenv('openAI_api_key')

class StudentDataAI:
    def __init__(self, api_key: str, db_path: str = "database.db"):
        self.client = OpenAI(api_key=api_key)
        self.db_path = db_path

    def get_all_data(self) -> List[Dict]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM student_data")
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            student_data = [dict(zip(column_names, row)) for row in rows]
            conn.close()
            return student_data
        except Exception as e:
            print(f"Database error: {e}")
            return []

    def get_all_classes(self) -> List[Dict]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM classes")
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            classes = [dict(zip(column_names, row)) for row in rows]
            conn.close()
            return classes
        except Exception as e:
            print(f"Database error: {e}")
            return []

    def get_all_extracurriculars(self) -> List[Dict]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM extracurriculars")
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            extracurriculars = [dict(zip(column_names, row)) for row in rows]
            conn.close()
            return extracurriculars
        except Exception as e:
            print(f"Database error: {e}")
            return []

    def search_classes(self, criteria: Dict) -> List[Dict]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            query = "SELECT * FROM classes"
            params = []
            if criteria:
                conditions = [f"{field} = ?" for field, value in criteria.items() if value is not None]
                params = [value for _, value in criteria.items() if value is not None]
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
            cursor.execute(query, params)
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            classes = [dict(zip(column_names, row)) for row in rows]
            conn.close()
            return classes
        except Exception as e:
            print(f"Database error: {e}")
            return []

    def search_extracurriculars(self, criteria: Dict) -> List[Dict]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            query = "SELECT * FROM extracurriculars"
            params = []
            if criteria:
                conditions = [f"{field} = ?" for field, value in criteria.items() if value is not None]
                params = [value for _, value in criteria.items() if value is not None]
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
            cursor.execute(query, params)
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            activities = [dict(zip(column_names, row)) for row in rows]
            conn.close()
            return activities
        except Exception as e:
            print(f"Database error: {e}")
            return []

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

    def get_recommendations(self, query: str, context: str = "") -> str:
        functions = [
            {"name": "get_all_data", "description": "Retrieve all the data about what a student has done", "parameters": {"type": "object", "properties": {}, "required": []}},
            {"name": "get_all_classes", "description": "Get all available classes from the classes table", "parameters": {"type": "object", "properties": {}, "required": []}},
            {"name": "get_all_extracurriculars", "description": "Get all available extracurricular activities", "parameters": {"type": "object", "properties": {}, "required": []}},
            {"name": "search_classes", "description": "Search for classes based on specific criteria", "parameters": {"type": "object", "properties": {"criteria": {"type": "object", "description": "search criteria as key-value pairs"}}, "required": ["criteria"]}},
            {"name": "search_extracurriculars", "description": "Search for extracurricular activities", "parameters": {"type": "object", "properties": {"criteria": {"type": "object", "description": "search criteria as key-value pairs"}}, "required": ["criteria"]}},
            {"name": "get_database_schema", "description": "Get the structure and column names of all database tables", "parameters": {"type": "object", "properties": {}, "required": []}}
        ]

        messages = [
            {"role": "system", "content": "You are an AI educational advisor. Recommend classes and activities based on interests and prerequisites."},
            {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
        ]

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                functions=functions,
                function_call="auto"
            )
        except openai.RateLimitError:
            print("Quota exceeded or rate limited, please check your OpenAI account and try again.")
            return "Quota exceeded."

        # Only allow a maximum of 2 function calls to avoid context overflow
        for _ in range(2):
            if response.choices[0].finish_reason != "function_call":
                break

            function_call = response.choices[0].message.function_call
            function_name = function_call.name
            function_args = json.loads(function_call.arguments)

            if function_name == "get_all_data":
                result = self.get_all_data()
            elif function_name == "get_all_classes":
                result = self.get_all_classes()
            elif function_name == "get_all_extracurriculars":
                result = self.get_all_extracurriculars()
            elif function_name == "search_classes":
                criteria = function_args.get("criteria", {})
                result = self.search_classes(criteria)
            elif function_name == "search_extracurriculars":
                criteria = function_args.get("criteria", {})
                result = self.search_extracurriculars(criteria)
            elif function_name == "get_database_schema":
                result = self.get_database_schema()
            else:
                result = {"error": "Unknown function"}

            result_str = json.dumps(result, default=str)
            if len(result_str) > 1000:
                result_str = result_str[:1000] + '... [truncated]'

            messages.append({
                "role": "function",
                "name": function_name,
                "content": result_str
            })

            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    functions=functions,
                    function_call="auto"
                )
            except openai.RateLimitError:
                print("Quota exceeded or rate limited, please check your OpenAI account and try again.")
                return "Quota exceeded."

        return response.choices[0].message.content

if __name__ == "__main__":
    student_ai = StudentDataAI(api_key=openai_key, db_path="database.db")

    queries = [
        "List 6 classes that the student should take next semester",
        "Give 2 new extracurricular activities the student should participate in"
    ]

    for query in queries:
        response = student_ai.get_recommendations(query)
        print(response)
