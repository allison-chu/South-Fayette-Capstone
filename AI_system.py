import sqlite3
import json
import pandas as pd
from openai import OpenAI
from typing import List, Dict, Any, Optional

class StudentDataAI:
    def __init__(self, api_key: str, db_path: str="database.db"):
        self.client = OpenAI(api_key = "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")
        self.db_path = db_path

    def get_all_data(self) -> List[Dict]:
        try:
            conn = sqlite3.connect(self.db_pat)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM student_data")
            rows = cursor.fetchall()

            column_names = [description[0] for description in cursor.description]

            studentData = []
            for row in rows:
                student_dict = dict(zip(column_names, row))
                studentData.append(student_dict)

            conn.close()
            return studentData
       
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
            classes= []
            for row in rows:
                class_dict = dict(zip(column_names, row))
                classes.append(class_dict)
                
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
            extracurriculars = []
            for row in rows:
                activity_dict = dict(zip(column_names, row))
                extracurriculars.append(activity_dict)
            
            conn.close()
            return extracurriculars
        
        except Exception as e:
            print(f"Database error: {e}")
            return []


    def search_classes(self, criteria: Dict) -> List[Dict]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = "SELECT * FROM classes WHERE"
            params = []
            conditions = []

            for field, value in criteria.items():
                if value is not None:
                    conditions.append(f"{field} = ?")
                    params.append(value)

            if conditions:
                query += " AND ".join(conditions)
            else:
                query = "SELECT * FROM classes"
                params = []

            cursor.execute(query, params)
            rows = cursor.fetchall()

            column_names = [description[0] for description in cursor.description]
            classes = []
            for row in rows:
                class_dict = dict(zip(column_names, row))
                classes.append(class_dict)

            conn.close()
            return classes
        
        except Exception as e:
            print(f"Database error: {e}")
            return []
        

    def search_extracurriculars(self, criteria: Dict) -> List[Dict]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = "SELECT * FROM extracurriculars WHERE"
            params = []
            conditions = []

            for field, value in criteria.items():
                if value is not None:
                    conditions.append(f"{filed} = ?")
                    params.append(value)

            if conditions:
                query += " AND ".join(conditions)
            else:
                query = "SELECT * FROM extracurriculars"
                params = []

            cursor.execute(query, params)
            rows = cursor.fetchall()

            column_names = [description[0] for description in cursor.description]
            activities = []
            for row in rows:
                activity_dict = dict(zip(column_names, row))
                activities.append(activity_dict)
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

            schema = {}
            for column_info in schema_info:
                column_name = column_info[1]
                column_type = column_info[2]
                schema[column_name] = column_type
            conn.close()
            return schema
        except Exception as e:
            print(f"Database error: {e}")
            return {}
        
    def get_recommendations(self, query: str, context: str = "") -> str:

        functions = [
            {
                "name": "get_all_data",
                "description": "Retrieve all the data about what a student has done",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
               "name": "get_all_classes",
               "description": "get all avaible classes from the classes table",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "get_all_extracurriculars",
                "description" : "get all available extracurricular activities",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "search_classes",
                "description": "ssearch for classes based on specific criteria",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "criteria": {
                            "type": "object",
                            "description": "search criteria as key-value pairs"
                        }
                    },
                    "required": ["criteria"]
                }
            },
            {
                "name": "search_extracurriculars",
                "description": "search for extracurricular activities",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "criteria": {
                            "type": "object",
                            "description": "search criteria as key-value pairs"
                        }
                    },
                    "required": ["criteria"]
                }
            },
            {
                "name": "get_database_schema",
                "description": "get the structure and column names of all database tables",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        ]

    messages = [
        {
            "role": "system",
            "content": """You are an AI educational advisor with access to a database that contains:
            -student records about what they have completed and what they like or disliked about it
            -student score of each completed item describing how much they enjoyed an item on a scale of 1-7 with 1 being strongly disliked and 7 being strongly liked
            -all possible classes that the student could take next with details like prerequisites, domain, and tags that describe what they could learn
            -all availbe extracurricular activities with details like domain and tags that describe what they could learn

            Your goal is to make intelligent recommendations by:
            1. analyzing student data to understand what they enjoy or dislike about a class or activity
            2. matching students with appropriate classes based on interests and prerequisites
            3. suggesting extracurriculars that align with their interests or help develop new skills
            4. consider the prerequisites for a class and do not suggest a class that they are unable to take

            Always explain your reasoning when possible and provide multiple options. 
            Be specific with your explaination, but keep it positive; do not say something that might offend or hurt a student.
            Consider academic and personal development based on the student's likes and dislikes.
                """
        },
        {
            "role": "user",
            "content": f"Context: {context}\n\nQuery: {query}"
        }
    ]


    response = self.client.chat.completions.create(
        model = "gpt-4",
        messages = messages,
        functions = functions,
        function_call = "auto"
    )

    while response.choices[0].finish_reason =="function_call":
        function_call = response.choices[0].message.function_call
        function_name = function_call.name
        function_args = json.loads(function_call.arguments)


        if function_name == "get_all_data":
            result = self.get_all_data()
        elif function_name == "get_all_classes":
            result = self.get_all_classes()
        elif function_name == "get_all_extracurriculars":
            result = self.get_all_extracurriculars
        elif function_name == "search_classes":
            result = self.search_classes(function_args["criteria"])
        elif function_name == "search_extracurriculars":
            result = self.search_extracurriculars(function_args["criteria"])
        elif function_name == "get_database_schema":
            result = self.get_database_schema()
        else:
            result = {"error": "Unknown function"}

        messages.append({
            "role" : "function",
            "name": function_name,
            "content": json.dumps(result, default=str)
        })

        if __name__ == "__main__":
            student_ai = StudentDataAI(
                api_key = "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",
                db_path = "../database.db"
            )

        queries = [
            "List 6 classes that the student should take next semester",
            "give 2 new extracurricular activities the student should participate in"
        ]


    for query in queries:
       response = student_ai.get_recommendations(query)
       print(response)