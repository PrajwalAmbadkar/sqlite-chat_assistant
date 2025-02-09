from flask import Flask, request, jsonify
import sqlite3
import re
from rapidfuzz import process  
import google.generativeai as genai

# Set up Flask app
app = Flask(__name__)

# Set your Gemini API key
GEMINI_KEY = "AIzaSyAf8v93k5Be5uxRzSSIbwB3nFW5kE53XAM"
genai.configure(api_key=GEMINI_KEY)

# Path to SQLite Database
DB_PATH = "C:\SCALER\chat_assistant\SQlite_database.db"

# Log File Path
LOG_FILE = "chat_assistent_sql_query_output"

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Chat Assistant API!"})

# Function to generate SQL query from natural language prompt
def generate_sql_query_from_prompt(prompt):
    model = genai.GenerativeModel("gemini-pro")
    system_prompt = f"""
    You are an expert in SQL and SQLite databases. Convert the user's natural language query into a valid SQL query based on the given database schema:
    Employees Table:
    - ID (INTEGER, PRIMARY KEY)
    - Name (TEXT)
    - Department (TEXT)
    - Salary (REAL)
    - Hire_Date (TEXT)
    Departments Table:
    - ID (INTEGER, PRIMARY KEY)
    - Name (TEXT)
    - Manager (TEXT)
    Ensure correct SQL formatting and table names.
    User Query: "{prompt}"
    SQL:
    """
    response = model.generate_content(system_prompt)
    sql_query = response.text.strip()
    sql_query = re.sub(r"```sql|```", "", sql_query)  # Remove markdown formatting
    return sql_query

# Function to execute SQL query
def execute_sql_query(db_path, query):
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        connection.close()
        return results, column_names
    except Exception as e:
        return f"Error: {str(e)}", []

@app.route('/chat-assistant', methods=['POST'])
def chat_assistant():
    data = request.get_json()
    user_query = data.get('query')
    
    if not user_query:
        return jsonify({"error": "Query is required"}), 400
    
    sql_query = generate_sql_query_from_prompt(user_query)
    results, columns = execute_sql_query(DB_PATH, sql_query)
    
    if isinstance(results, str) and "Error" in results:
        return jsonify({"error": results}), 500
    
    response_data = [dict(zip(columns, row)) for row in results] if results else "No matching records found."
    
    return jsonify({"query": sql_query, "results": response_data})

if __name__ == '__main__':
    app.run(debug=True)
