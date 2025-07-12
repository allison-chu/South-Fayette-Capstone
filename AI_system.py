import os
import sqlite3
import json
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv(dotenv_path="keys.env")

openai_key = os.getenv("openAI_api_key")

print("🚀 Running updated AI_system.py!")
print(f"🔑 OpenAI key loaded? {'Yes' if openai_key else 'No'}")

class StudentDataAI:
    def __init__(self, api_key: str, db_path: str = "database.db"):
        self.api_key = api_key
        self.db_path = db_path
        if api_key:
            self.client = OpenAI(api_key=api_key)
            print("✅ OpenAI client initialized.")
        else:
            self.client = None
            print("⚠️ No OpenAI API key provided. Will use dummy data.")

    def get_recommendations(self, query: str, context: str = "") -> str:
        if not self.client:
            print("⚠️ Using dummy recommendations because OpenAI client not initialized.")
            return self._dummy_recommendations()

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

**Extracurricular Activities**:
- Example Club: Fun activity.
- Example Workshop: Hands-on learning.
"""

# if run directly
if __name__ == "__main__":
    ai = StudentDataAI(api_key=openai_key, db_path="database.db")
    result = ai.get_recommendations("What classes or activities do you recommend?")
    print(result)
