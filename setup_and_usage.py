import os
import sqlite3
from AI_system import StudentDataAI
from dotenv import load_dotenv

load_dotenv(dotenv_path='keys.env')
openai_key =os.getenv('openAI_api_key')

def setup_environment():
    print("setting up student data AI system...")

    required_packages = ['openai', 'pandas']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
            print(f"{package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"{package} is missing")

    if missing_packages:
        print(f"\nPlease install missing packages:")
        print(f"pip install{' '.join(missing_packages)}")
        return False

    return True

def check_database_tables(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlute_master WHERE type='table")
        tables = [table[0] for table in cursor.fetchall()]

        print(f"\nFound tables: {tables}")
        
        required_tables = ['student_data', 'classes', 'extracurriculars']
        missing_tables = []

        for table in required_tables:
            if table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"{table} table found ({count} records)")

                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]
                print(f" Columns: {', '.join(column_names)}")

            else:
                missing_tables.append(table)
                print(f"{table} table not found")
        conn.close

        if missing_tables:
            print(f"\nMissing required tables: {missing_tables}")
            return False
        
        return True
    
    except Exception as e: 
        print(f"Database connection error: {e}")
        return False
    
def show_sample_data(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        tables = ['student_data', 'classes', 'extracurriculars']

        for table in tables:
            print(f"\n--- Sample data from {table} ---")
            cursor.execute(f"SELECT * FROM {table} LIMIT 3")
            rows = cursor.fetchall()

            if rows:
                cursor.execute(f"PRAGMA table_info({table})")
                columns = [col[1] for col in cursor.fetchall()]

                for i, row in enumerate(rows):
                    print(f"REcord {i+1}:")
                    for col, val in zip (columns, row):
                        print(f" {col}: {val}")
                    print()

            else:
                print(" No data found")

        conn.close()

    except Exception as e:
        print(f"Error showing sample data: {e}")


def test_recommendations(student_ai):
    print("\n" + "=" * 50)
    print("Testing Recommendation System")
    print("="*50)

    test_queries = [
        "show me the database schema"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: {query}")
        print("-"*40)

        try:
            response = student_ai.get_recommendations(query)
            print(response[:500] + "..." if len(response) > 500 else response)
        except Exception as e:
            print(f"Error: {e}")

            print("-"*40)


def main():
    print("Student Recommendation AI system Setup")
    print("="*50)

    if not setup_environment():
        return
    

    print("\nConfiguration:")
    api_key = input("openai_key: ").strip()
    db_path = input("../database.db: ").strip()

    if not db_path:
        db_path = "database.db"
    
    print(f"\nChecking database structure: {db_path}")
    if not check_database_tables(db_path):
        print("\nDatabase structure check failed")
        print("Make sure your database contains these tables:")
        print("- student_data (student records)")
        print("- classes (available classes)")
        print("- extracurriculars (available activities)")
        return
    
    show_sample = input("\nShow sample data from tables? (y/n): ")
    if show_sample =='y':
        show_sample_data(db_path)

    
    print("\nInitializing AI recommendation system...")
    try:
        student_ai = StudentDataAI(api_key=api_key, dp_path=db_path)
        print("AI system initialized successfully")
    except Exception as e:
        print(f"AI initialization failed: {e}")
        return


    test_system = input("\nRun system tests? (y/n: ").lower().strip()
    if test_system =='y':
        test_recommendations(student_ai)


    print("\n" + "="*50)
    print("System ready! Try these types of queries:")
    print("• 'What extracurriculars would help with leadership skills?'")
    print("• 'What advanced math classes are available?'")
    print("• 'Suggest activities for a shy student'")
    print("• Type 'quit' to exit")
    print("="*50)

    while True:
        query = input("\nEnter your query: ").strip()

        if query.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break

        if not query:
            continue
        print("\nProcessing your query...")
        print("-"*50)

        try:
            response = student_ai.get_recommendations(query)
            print(response)
        except Exception as e:
            print(f"Error processing query: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    main()