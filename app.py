import streamlit as st
import google.generativeai as genai
import sqlite3
import re
from rapidfuzz import process  # Fast fuzzy matching library
import os

# Set your Gemini API key
GEMINI_KEY = "AIzaSyAf8v93k5Be5uxRzSSIbwB3nFW5kE53XAM"
genai.configure(api_key=GEMINI_KEY)

# Path to SQLite Database
DB_PATH = "C:\SCALER\chat_assistant\SQlite_database.db"

# Log File Path
LOG_FILE = "chat_assistent_sql_query_output"

# Function to log interactions to a file
def log_interaction(query, response):
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"Query: {query}\n")
        log.write(f"Response: {response}\n")
        log.write("-" * 50 + "\n")

# Function to retrieve distinct department names
def fetch_department_names(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT Name FROM Departments;")
    departments = [row[0] for row in cursor.fetchall()]
    connection.close()
    return departments

# Function to retrieve distinct employee names
def fetch_employee_names(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT Name FROM Employees;")
    employees = [row[0] for row in cursor.fetchall()]
    connection.close()
    return employees

# Function to find closest department name
def get_closest_department_name(input_department, available_departments):
    match = process.extractOne(input_department, available_departments)
    if match:
        best_match = match[0]
        score = match[1]
        if score >= 80:  # Accept only high-confidence matches
            return best_match
    return None  # No good match found

# Function to find closest employee name
def get_closest_employee_name(input_name, available_employees):
    match = process.extractOne(input_name, available_employees)
    if match:
        best_match = match[0]
        score = match[1]
        if score >= 80:  # Accept only high-confidence matches
            return best_match
    return None  # No good match found

# Function to translate user prompt to SQL query using Gemini
def generate_sql_query_from_prompt(prompt):
    model = genai.GenerativeModel("gemini-pro")
    
    system_prompt = """You are an expert in SQL and SQLite databases. 
    Convert the user's natural language query into a valid SQL query based on the given database schema:
    
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

    Ensure:
    - Use correct table names.
    - Do not assume additional columns.
    - Wrap text values in single quotes.
    - Keep queries optimized.
    - DO NOT add markdown formatting like ```sql.

    Example:
    User: How many employees work in the Sales department?
    SQL: SELECT COUNT(*) FROM Employees WHERE Department = 'Sales';

    User: "{prompt}"
    SQL:

    """

    response = model.generate_content(system_prompt.format(prompt=prompt))
    
    # Clean extracted SQL query, removing markdown formatting if present
    sql_query = response.text.strip()
    sql_query = re.sub(r"```sql|```", "", sql_query)  # Remove triple backticks
    
    return sql_query.strip()

# Function to retrieve data from the SQLite database
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

def generate_output_prompt(query_results, columns):
    # Handle empty results case
    if not query_results:
        return "No matching records were found."

    # Constructing a detailed prompt
    output_prompt = """You are an expert in SQL and databases. Your task is to convert SQL query results into a **clear, natural, and easy-to-understand response** for a non-technical user.  

    ### **Instructions for Formatting Responses:**  
    1️ **Avoid technical jargon** like "column," "row," or "SQL result."  
    2️ **Make the response conversational** and structured like an explanation.  
    3️ **Handle singular and plural cases properly.**  
    4 **For multiple results, list them clearly** in a structured format.
    5 **carefully understand the 
    --
    ### **📌 Example Formats for Different Query Results:**  

    ✅ **1. For a Single Value (Direct Answer)**  
    **SQL Result:** `Manager: Alice`  
    **Response:** `"The manager of the Finance department is Alice."`  

    ✅ **2. For Multiple Values (Lists)**  
    **SQL Result:** `Employee Name: Bob, Frank, Eve`  
    **Response:** `"The employees working in the Engineering department are Bob, Frank, and Eve."`  

    ✅ **4. For Numerical Data (Summaries & Aggregates)**  
    **SQL Result:** `Average Salary: 75,000`  
    **Response:** `"The average salary of employees in the Finance department is 75,000."`  

    ✅ **5. For Multiple Attributes Per Entry (Detailed Lists)**  
    **SQL Result:**  
    - `Name: Bob, Salary: 60,000, Department: Sales`  
    - `Name: Frank, Salary: 72,000, Department: Engineering`  

    **Response:**  
    *"Bob, who works in Sales, earns a salary of 60,000. Frank, who is part of the Engineering team, earns 72,000."*  

    ✅ **6. For No Results Found**  
    - **SQL Result:** *(No data found for a query)*  
    - **Response:** `"No information is available for the requested query. Please check the department name or try again with a different request."`  
    ---

    ### ** Task: Generate a Human-Readable Response Based on the Given Query Results**  

    Now, based on the SQL query results below, convert them into a natural language response.  

    ### ** SQL Results:**  
    {query_results}  

    ### ** Response:**  
    """

    # Formatting results
    formatted_results = []
    for row in query_results:
        row_data = ", ".join([f"{columns[i]}: {row[i]}" for i in range(len(columns))])
        formatted_results.append(row_data)

    output_prompt += "\n".join(formatted_results) + "\n\n"
    output_prompt += "### Response:\n"

    return output_prompt


# Function to generate a human-readable response from query results
def generate_user_response(sql_query, query_results, columns):
    if isinstance(query_results, str) and "Error" in query_results:
        return f"⚠️ {query_results}"

    if not query_results:
        return "ℹ️ No matching results found."

    if "COUNT(" in sql_query.upper():
        return f"✅ The total count is **{query_results[0][0]}**."

    # Generate output prompt
    output_prompt = generate_output_prompt(query_results, columns)

    # Generate natural language response using Gemini model
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(output_prompt)
    
    return response.text.strip()

# Streamlit UI
st.title("SQLite Database Chat Assistant 🗂️")

# Input field for the user to enter a query
user_input_query = st.text_input("Enter your query in natural language:", placeholder="e.g., How many employees work in HR?")

if st.button("Generate SQL & Retrieve Data"):
    if user_input_query:
        # Translate user input into SQL query
        sql_query = generate_sql_query_from_prompt(user_input_query)
        
        st.subheader("Generated SQL Query:")
        st.code(sql_query, language="sql")

        # Retrieve department and employee names for validation
        available_departments = fetch_department_names(DB_PATH)
        available_employees = fetch_employee_names(DB_PATH)

        # Validate department names in the query
        department_match = re.search(r"WHERE\s+Department\s*=\s*'([^']+)'", sql_query, re.IGNORECASE)
        if department_match:
            input_department = department_match.group(1)
            corrected_department = get_closest_department_name(input_department, available_departments)

            if corrected_department and corrected_department != input_department:
                st.warning(f"Did you mean **'{corrected_department}'** instead of **'{input_department}'**? ")
                sql_query = sql_query.replace(f"'{input_department}'", f"'{corrected_department}'")

        # Validate employee names in the query
        employee_match = re.search(r"WHERE\s+Name\s*=\s*'([^']+)'", sql_query, re.IGNORECASE)
        if employee_match:
            input_name = employee_match.group(1)
            corrected_name = get_closest_employee_name(input_name, available_employees)

            if corrected_name and corrected_name != input_name:
                st.warning(f"Did you mean **'{corrected_name}'** instead of **'{input_name}'**?")
                sql_query = sql_query.replace(f"'{input_name}'", f"'{corrected_name}'")

        # Execute the SQL query and fetch results
        query_results, columns = execute_sql_query(DB_PATH, sql_query)

        # Generate and display a human-readable response
        user_response = generate_user_response(sql_query, query_results, columns)
        st.subheader("Response:")
        st.markdown(user_response)

        # Log the interaction to a file
        log_interaction(user_input_query, user_response)
    else:
        st.warning("Please enter a query.")
