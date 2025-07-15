import os
import sqlite3
import json
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

<<<<<<< Updated upstream
load_dotenv(dotenv_path="keys.env")

openai_key = os.getenv("openAI_api_key")

print("🚀 Running updated AI_system.py!")
print(f"🔑 OpenAI key loaded? {'Yes' if openai_key else 'No'}")
=======
# Load environment variables and get the api for the AI system
load_dotenv(dotenv_path='keys.env')
openai_key = os.getenv('openAI_api_key')
>>>>>>> Stashed changes


#sets up all the methods needed for the AI to access and understand the database
class StudentDataAI:

    #initiates the AI system and the database
    def __init__(self, api_key: str, db_path: str = "database.db"):
        self.api_key = api_key
        self.db_path = db_path
<<<<<<< Updated upstream
        if api_key:
            self.client = OpenAI(api_key=api_key)
            print("✅ OpenAI client initialized.")
        else:
            self.client = None
            print("⚠️ No OpenAI API key provided. Will use dummy data.")
=======

    #gets all the data from the student_data datatable within the database
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

    #gets all the data from the classes datatable within the database
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

    #gets all the data from the extracurriculars datatable within the database
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

    #allows the AI to search through the classes datatable
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

    #allows the AI to search through the extracurriculars datatable
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

    #provides the outline of the database, and how the different datatables relate to each other 
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
>>>>>>> Stashed changes

    #function that collects all the functions that the AI will have access to so that it can call them on its own
    def get_recommendations(self, query: str, context: str = "") -> str:
        if not self.client:
            print("⚠️ Using dummy recommendations because OpenAI client not initialized.")
            return self._dummy_recommendations()

        #teaches the AI about it's role within the project and how it should act
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI educational advisor with access to a database. "
                    "Your goal is to make intelligent recommendations for classes and extracurricular activities. "
                    "ALWAYS respond in the following exact format and nothing else:\n\n"
                    "**Classes**:\n"
                    "- Class Name: brief description\n"
                    "- Class Name: brief description\n\n"
                    "**Extracurricular Activities**:\n"
                    "- Activity Name: brief description\n"
                    "- Activity Name: brief description\n"
                ),
            },
            {
                "role": "user",
                "content": f"Context: {context}\n\nQuery: {query}"
            },
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

    def _dummy_recommendations(self) -> str:
        print("ℹ️ Returning dummy recommendations.")
        return """
**Classes**:
- Example Class 1: Learn something useful.
- Example Class 2: Another great course.

<<<<<<< Updated upstream
**Extracurricular Activities**:
- Example Club: Fun activity.
- Example Workshop: Hands-on learning.
"""
=======
            function_call = response.choices[0].message.function_call
            function_name = function_call.name
            function_args = json.loads(function_call.arguments)

            #checks which function was called, and provides the information for that function
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
>>>>>>> Stashed changes

# if run directly
if __name__ == "__main__":
<<<<<<< Updated upstream
    ai = StudentDataAI(api_key=openai_key, db_path="database.db")
    result = ai.get_recommendations("What classes or activities do you recommend?")
    print(result)
=======
    student_ai = StudentDataAI(api_key=openai_key, db_path="database.db")

    #specific queries given to the AI that tells it what to do within the system
    queries = [
        "List 6 classes that the student should take next semester",
        "Give 2 new extracurricular activities the student should participate in"
    ]

    #loop for each query within the list, runs the functions correctly for the system
    for query in queries:
        response = student_ai.get_recommendations(query)
        print(response)
>>>>>>> Stashed changes
