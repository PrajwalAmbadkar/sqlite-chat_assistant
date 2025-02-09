# Chat Assistant for SQLite Database

##  📌 **Overview**  
This Chat Assistant is a Streamlit-based application that converts natural language queries into SQL queries using Google's Gemini AI model. It then executes these queries on an SQLite database and returns the results in a clear, human-readable format for easy interpretation.

## 🚀 **Deployed Using Streamlit**  :
The app is deployed using Streamlit, providing an interactive and easy-to-use interface for users to communicate with the database in natural language.

##  🏃‍♂️**Steps of Deployment** :
1. **Prepare the Application**: Set up the necessary files including the Streamlit app, database connection, and AI model configuration.
2. **Deploy to Streamlit**: Upload the project to Streamlit Cloud using the [Streamlit for Teams](https://streamlit.io/teams) platform.
3. **Start the Application**: Once deployed, the app is accessible via a public link, allowing users to interact with the database through a conversational interface.
4. **Real-time Interaction**: Users can start querying the database in natural language, with the assistant handling everything from SQL generation to response formatting.

## 🚀 **Features**
- **Natural Language to SQL**: Effortlessly converts user input into optimized SQL queries.
- **SQLite Database Integration**: Retrieves accurate data from an SQLite database based on the generated query.
- **Error Handling**: Gracefully manages invalid queries, missing inputs, and data inconsistencies.
- **Interactive Chat Interface**: Provides a smooth, conversational experience for users to interact with the database.


## 🛠️ **How It Works**
1. **User Query**: The user submits a natural language query through the input field.
2. **Query Translation**: The Gemini AI model processes the input and generates a corresponding SQL query.
3. **Database Interaction**: The generated SQL query is executed against the SQLite database to retrieve relevant data.
4. **Human-Readable Response**: The results are then formatted into a clear, easy-to-understand response and displayed to the user.



## 📂 Project Structure
```
├── README.md                            # Project documentation
├── SQlite_database.db                   # SQLite database file
├── app.py                               # Main Flask application
├── chat_assistent_sql_query_output      #File to store query and response
├── requirements.txt                     # Required dependencies
```

## 🏃‍♂️ Steps to Run the Project Locally

- Simply click the link below to start using the chat assistant.

[Start Chat Assistant](https://app-chatassistant-hxudf2djuweh7oxrtvybun.streamlit.app/)

No additional setup is required—just type your question and get your answer instantly!


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

