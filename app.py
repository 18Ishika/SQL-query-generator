from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai
import pandas as pd
import plotly.express as px

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define functions
def get_response(question, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt[0], question])
    return response.text.strip().strip("").replace("sql", "").strip()

def read_sql(sql, db):
    conn = sqlite3.connect(db)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

def execute_sql(sql, db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

def create_visualization(df, x_col, y_col, plot_type="bar"):
    if not df.empty:
        if plot_type == "bar":
            fig = px.bar(df, x=x_col, y=y_col, title=f"{plot_type.capitalize()} Plot: {y_col} vs {x_col}")
        elif plot_type == "line":
            fig = px.line(df, x=x_col, y=y_col, title=f"{plot_type.capitalize()} Plot: {y_col} vs {x_col}")
        elif plot_type == "scatter":
            fig = px.scatter(df, x=x_col, y=y_col, title=f"{plot_type.capitalize()} Plot: {y_col} vs {x_col}")
        else:
            st.warning(f"Unsupported plot type: {plot_type}. Defaulting to bar plot.")
            fig = px.bar(df, x=x_col, y=y_col, title=f"Bar Plot: {y_col} vs {x_col}")
        return fig
    else:
        return None

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
    SELECT NAME FROM STUDENT ORDER BY MARKS DESC LIMIT 1;

    10. "Show the CLASS and average MARKS for each CLASS." should be converted to:
    SELECT CLASS, AVG(MARKS) FROM STUDENT GROUP BY CLASS;

    Ensure your output is a single, correctly formatted SQL query without any extra text or quotation marks around it. The word "SQL" should not appear in the output.

    Note: The SQL query should not include any extraneous characters like ''' at the beginning or end.
    """
]

# Streamlit configuration
st.set_page_config(page_title="SQL Query Generator", layout="centered", initial_sidebar_state="expanded")
st.markdown("<h1 style='text-align: center; color: #e74c3c;'>AI-Based SQL Query Generator with Gemini AI</h1>", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Generate SQL Query", "Insert Record", "Delete Record", "Visualize Data"])

if page == "Generate SQL Query":
    st.subheader("Generate SQL Query from Natural Language")
    question = st.text_input("Ask your question about the STUDENT database:", key="input")
    if st.button("Generate SQL Query"):
        response = get_response(question, prompt)
        st.write(f"Generated SQL Query: {response}")
        try:
            if response.lower().startswith("select"):
                df = read_sql(response, "student.db")
                st.subheader("Query Results:")
                st.dataframe(df)
                st.session_state["df"] = df
            elif response.lower().startswith(("insert", "delete", "update")):
                execute_sql(response, "student.db")
                st.success("SQL query executed successfully!")
            else:
                st.error("Generated query is not supported for execution.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

elif page == "Insert Record":
    st.subheader("Insert a New Record")
    with st.form("insert_form"):
        name = st.text_input("Name")
        class_ = st.text_input("Class")
        section = st.text_input("Section")
        marks = st.text_input("Marks")  # Changed to text input for optional value
        submitted = st.form_submit_button("Insert Record")
        if submitted:
            try:
                marks_value = int(marks) if marks else "NULL"  # Convert to integer if provided
                insert_sql = f"INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('{name}', '{class_}', '{section}', {marks_value})"
                execute_sql(insert_sql, "student.db")
                st.success("Record inserted successfully!")
            except ValueError:
                st.error("Marks must be a number.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

elif page == "Delete Record":
    st.subheader("Delete a Record")
    with st.form("delete_form"):
        delete_name = st.text_input("Name")
        delete_class = st.text_input("Class")
        delete_section = st.text_input("Section")
        delete_marks = st.text_input("Marks")  # Changed to text input for optional value
        delete_submitted = st.form_submit_button("Delete Record")
        if delete_submitted:
            delete_conditions = []
            if delete_name:
                delete_conditions.append(f"NAME = '{delete_name}'")
            if delete_class:
                delete_conditions.append(f"CLASS = '{delete_class}'")
            if delete_section:
                delete_conditions.append(f"SECTION = '{delete_section}'")
            if delete_marks:
                try:
                    delete_marks_value = int(delete_marks)
                    delete_conditions.append(f"MARKS = {delete_marks_value}")
                except ValueError:
                    st.error("Marks must be a number.")

            if delete_conditions:
                delete_sql = "DELETE FROM STUDENT WHERE " + " AND ".join(delete_conditions)
                st.write(f"Executing SQL: {delete_sql}")  # Debugging: print the query
                try:
                    execute_sql(delete_sql, "student.db")
                    st.success("Record deleted successfully!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning("Please provide at least one condition to delete a record.")

elif page == "Visualize Data":
    if "df" in st.session_state:
        st.subheader("Visualization Options")
        with st.expander("Select Visualization Options"):
            x_col = st.selectbox("Select column for x-axis:", st.session_state["df"].columns)
            y_col = st.selectbox("Select column for y-axis:", st.session_state["df"].columns)
            plot_type = st.selectbox("Select plot type:", ["bar", "line", "scatter"])

        if st.button("Visualize Data"):
            fig = create_visualization(st.session_state["df"], x_col, y_col, plot_type)
            if fig:
                st.plotly_chart(fig)
            else:
                st.write("No data available to visualize.")
    else:
        st.write("No data available. Generate a SQL query first.")
