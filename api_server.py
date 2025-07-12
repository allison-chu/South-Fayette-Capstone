from flask import Flask, request, jsonify, send_from_directory
from AI_system import StudentDataAI
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, static_url_path='', static_folder='.')

ai = StudentDataAI(
    api_key=os.getenv("openAI_api_key"),
    db_path="database.db"
)

@app.route("/")
def home():
    return send_from_directory(".", "explore.html")

@app.route("/script.js")
def js():
    return send_from_directory(".", "script.js")

@app.route("/styles.css")
def css():
    return send_from_directory(".", "styles.css")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

@app.route("/recommendations", methods=["POST"])
def recommendations():
    data = request.json
    query = data.get("query", "")
    context = data.get("context", "")

    print(f"Received query: {query}")
    print(f"With context: {context}")

    # call real AI now:
    result = ai.get_recommendations(query, context)

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)
