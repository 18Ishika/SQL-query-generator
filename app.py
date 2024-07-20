from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define functions
def get_response(question, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt[0], question])
    return response.text

def read_sql(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# Prompt for the generative AI
prompt = [
    """
    You are an expert in converting English questions to SQL queries! The database contains a table named STUDENT with columns: NAME, CLASS, SECTION, and MARKS.

    For example:
    1. "How many records are there in the table?" should be converted to:
    SELECT COUNT(*) FROM STUDENT;

    2. "What is the average MARKS in each SECTION?" should be converted to:
    SELECT SECTION, AVG(MARKS) FROM STUDENT GROUP BY SECTION;

    3. "List all students in CLASS Augmented Reality." should be converted to:
    SELECT * FROM STUDENT WHERE CLASS = 'Augmented Reality';

    4. "Get the total MARKS for students in SECTION B." should be converted to:
    SELECT SUM(MARKS) FROM STUDENT WHERE SECTION = 'B';

    5. "Find the maximum MARKS in CLASS 12." should be converted to:
    SELECT MAX(MARKS) FROM STUDENT WHERE CLASS = 'DSA';

    6. "Show the NAME and MARKS of students who scored above 90." should be converted to:
    SELECT NAME, MARKS FROM STUDENT WHERE MARKS > 90;

    7. "Count the number of distinct CLASSes." should be converted to:
    SELECT COUNT(DISTINCT CLASS) FROM STUDENT;

    8. "List all students ordered by their MARKS in descending order." should be converted to:
    SELECT * FROM STUDENT ORDER BY MARKS DESC;

    9. "Get the NAME of the student with the highest MARKS." should be converted to:
    SELECT NAME FROM STUDENT ORDER BY MARKS DESC LIMIT 2;

    10. "Show the CLASS and average MARKS for each CLASS." should be converted to:
    SELECT CLASS, AVG(MARKS) FROM STUDENT GROUP BY CLASS;

    Ensure your output is a single, correctly formatted SQL query without any extra text or quotation marks around it. The word "SQL" should not appear in the output.

    Note: The SQL query should not include any extraneous characters like ''' at the beginning or end.
    """
]

# Streamlit configuration
st.set_page_config(page_title="SQL Query Generator", layout="centered")
st.header("SQL Query Generator with Gemini AI")

# User input
question = st.text_input("Ask your question about the STUDENT database:", key="input")

# Button to submit the question
if st.button("Generate SQL Query"):
    response = get_response(question, prompt)
    st.write(f"Generated SQL Query: {response}")
    try:
        data = read_sql(response, "student.db")
        st.subheader("Query Results:")
        for i in data:
            print(i)
            st.subheader(i)
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
