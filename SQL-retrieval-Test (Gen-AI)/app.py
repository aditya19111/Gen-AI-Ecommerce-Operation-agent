import sys
import os
import sqlite3
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Show which Python executable is being used (debugging purpose)
print("--- SCRIPT IS USING THIS PYTHON EXECUTABLE ---")
print(sys.executable)
print("---------------------------------------------")

# Load environment variables
load_dotenv()

# Configure GenAI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to query Gemini for SQL generation
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-2.5-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to execute SQL queries on SQLite DB
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

# Prompt for Gemini
prompt = [
    """
    You are an expert in converting English questions to SQL queries.
    The SQL database has the name STUDENT and has the following columns:
    NAME, CLASS, SECTION.

    Examples:
    Q: How many entries of records are present?
    A: SELECT COUNT(*) FROM STUDENT;

    Q: Tell me all the students studying in Data Science class?
    A: SELECT * FROM STUDENT WHERE CLASS="Data Science";

    Rules:
    - Do not include ``` or the word 'sql' in the response.
    - Only return the SQL query.
    """
]

# Streamlit UI
st.set_page_config(page_title="SQL Query Generator & Executor")
st.header("🔎 Gemini App to Retrieve SQL Data")

# User input
question = st.text_input("Ask your question:", key="input")
submit = st.button("Get SQL & Run")

# If user submits
if submit and question:
    sql_query = get_gemini_response(question, prompt)
    sql_query = sql_query.strip().replace("```", "").replace("sql", "")

    st.subheader("📝 Generated SQL Query")
    st.code(sql_query, language="sql")

    try:
        rows = read_sql_query(sql_query, "student.db")
        st.subheader("📊 Query Results")
        if rows:
            for row in rows:
                st.write(row)
        else:
            st.info("No results found.")
    except Exception as e:
        st.error(f"Error executing query: {e}")
