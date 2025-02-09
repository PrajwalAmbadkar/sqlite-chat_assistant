# Chat Assistant for SQLite Database

## 📌 Overview
This **Chat Assistant** is a Flask-based API that converts natural language queries into SQL queries using Google's **Gemini AI** model. It then executes these queries on an SQLite database and returns structured results in a human-readable format.

## 🚀 Features
- Converts user input into **SQL queries**.
- Retrieves **data** from an SQLite database.
- Handles **error cases** (e.g., invalid queries, missing inputs).
- Provides a **RESTful API** with a `/chat-assistant` endpoint.

## 🛠️ How It Works
1. The user sends a **natural language query** to the API.
2. The **Gemini AI model** translates the query into SQL.
3. The **Flask app** executes the SQL on the SQLite database.
4. The API **returns the results** in a structured JSON format.

## 📂 Project Structure
```
├── README.md                            # Project documentation
├── SQlite_database.db                   # SQLite database file
├── app.py                               # Main Flask application
├── chat_assistent_sql_query_output      #File to store query and response
├── requirements.txt                     # Required dependencies
```

## 🏃‍♂️ Steps to Run the Project Locally

### 1️⃣ Install Dependencies
Make sure you have Python installed (>= 3.8). Then, install the required packages:
```sh
pip install flask google-generativeai rapidfuzz
```

### 2️⃣ Set Up the SQLite Database
Ensure the database file (`SQlite_database.db`) exists in the project directory. It should have the following tables:
- **Employees** (ID, Name, Department, Salary, Hire_Date)
- **Departments** (ID, Name, Manager)

### 3️⃣ Run the Flask Application
```sh
python app.py
```
This will start a local server at `http://127.0.0.1:5000/`

### 4️⃣ Test the API
You can test the `/chat-assistant` endpoint using **Postman** or **cURL**:

#### Example Request:
```json
{
    "query": "How many employees work in HR?"
}
```

#### Example Response:
```json
{
    "user_query": "How many employees work in HR?",
    "sql_query": "SELECT COUNT(*) FROM Employees WHERE Department = 'HR';",
    "response": {
        "data": [[5]],
        "columns": ["COUNT(*)"]
    }
}
```

## ⚠️ Known Limitations & Future Improvements
### Limitations:
- Relies on **Google Gemini AI**, requiring an API key.
- May **misinterpret queries** or generate incorrect SQL.
- Currently supports **only SQLite databases**.

### Future Enhancements:
- **Improve SQL validation** to prevent incorrect queries.
- **Enhance error handling** for better user experience.
- **Expand database support** to include PostgreSQL and MySQL.
- **Add authentication** for secure API access.

---
💡 **Contributions & Suggestions are Welcome!** 🚀

