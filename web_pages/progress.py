import streamlit as st
import plotly.express as px
import pandas as pd
from src.mongodb import student_data

def student_progress_analysis():
    st.title("📈 My Progress Analysis")
    student_name = st.session_state.get('student_name', 'Unknown Student')
    student_id = st.session_state.get('student_id', 'Unknown Student ID')
    st.write(f"Welcome, {student_name}!")

    try:
        sem1_data, sem2_data = student_data(student_id=student_id)

        if not sem1_data and not sem2_data:
            st.error(f"No data found for student ID: {student_id}")
            return

        print(sem1_data)
        print(sem2_data)
    except:
        pass