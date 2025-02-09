# SQLite-chat_assistant

## 📌 Project Overview
This project is an **AI-powered Chat Assistant** for querying an SQLite database using natural language. It converts user questions into SQL queries, fetches the relevant data, and returns human-readable responses.

## 🚀 Features
- Converts natural language queries into SQL.
- Retrieves data from an SQLite database.
- Provides human-readable responses.
- Handles invalid queries and errors gracefully.

## 🛠️ Technologies Used
- **Programming Language:** Python 🐍
- **Database:** SQLite 🗄️
- **Libraries:** Pandas, SQLite3, Natural Language Processing (NLP) techniques
- **Interface:** Streamlit (optional for deployment)

## 📂 Project Structure
```
|-- SQLite-chat_assistant/
    |-- app17..py           # Main script for processing queries
    |-- Tecnique.db          # SQLite database file
    |-- README.md            # Project documentation
    |-- requirements.txt     # List of dependencies
```

## 🛠️ Installation & Setup
### 🔹 Prerequisites
- Install **Python 3.8+**
- Install required libraries using:
  ```bash
  pip install -r requirements.txt
  ```

### 🔹 Running the Chatbot
1. Clone the repository:
   ```bash
   git clone https://github.com/<PrajwalAmbadkar>/<sqlite-chat_assistant>.git
   cd <sqlite-chat_assistant>
   ```
2. Run the chatbot:
   ```bash
   python app17.py
   ```
3. Start chatting by entering your queries in natural language.

## 🖥️ Example Queries
| User Query | Generated SQL | Response |
|------------|--------------|----------|
| "Who is the manager of Finance?" | `SELECT Manager FROM Departments WHERE Name = 'Finance';` | "Eve is the manager of Finance." |
| "List employees with a salary less than 65,000" | `SELECT Name FROM Employees WHERE Salary < 65000;` | "The employees with a salary below 65,000 are Alice and Grace." |

## ⚠️ Error Handling
- If a query is ambiguous, the chatbot asks for clarification.
- Returns a friendly message if no data is found.
- Handles invalid department names or incorrect input formats.

## 📌 Future Improvements
- Implementing a more advanced NLP model for query understanding.
- Enhancing the UI with a web-based frontend.
- Adding more database functionalities (e.g., inserting or updating records).

## 📜 License
This project is **open-source** under the MIT License.

## 🤝 Contributing
Feel free to **fork** this repository and submit pull requests for improvements!

## 📧 Contact
For any queries, reach out via GitHub Issues or email **prajwalambadkar12345@gmail.com**.

