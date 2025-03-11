import streamlit as st

def about():
    # Introduction to the project
    st.header("Project Overview")
    st.write("""
        The **Student Performance Analysis and Prediction** project aims to analyze and predict students' academic performance
        based on various factors. By leveraging data science techniques, this project provides insights into how different
        aspects influence student success.
    """)

    # Objectives of the project
    st.header("Objectives")
    st.write("""
        - To analyze student performance data and identify key factors affecting academic success.
        - To develop a prediction model that forecasts student grades based on historical data.
        - To provide a user-friendly interface for educators and stakeholders to visualize performance metrics.
        - To assist in data-driven decision-making for improving educational strategies.
    """)

    # Description of the dataset
    st.header("Dataset")
    st.write("""
        The dataset used for this project includes various features related to student demographics, attendance,
        coursework, and examination results. The primary goal is to understand how these features correlate with
        student performance.
    """)

    st.subheader("Key Features in the Dataset")
    st.write("""
        - **Student ID** : Unique identifier for each student.
        - **Remark** : Indicates if the student passed or failed.
        - **Grade** : Grade awarded to the student (e.g., O, A+, B, F).
        - **TotalMarksObtained** : Total marks obtained by the student.
        - **TotalMarks** : Total possible marks for the examination.
        - **CreditsEarned** : Credits earned based on performance.
        - **Percentage** : Percentage of marks obtained.
        - **SGPA** : Semester Grade Point Average.
    """)

    # Methodology
    st.header("Methodology")
    st.write("""
        The project follows a structured approach:
        1. **Data Collection** : Gathering relevant data from reliable sources.
        2. **Data Preprocessing** : Cleaning and preparing data for analysis.
        3. **Exploratory Data Analysis (EDA)** : Understanding data distribution and relationships between features.
        4. **Feature Engineering** : Creating new features that enhance model performance.
        5. **Model Development** : Training machine learning models to predict student performance.
        6. **Evaluation** : Assessing model accuracy and effectiveness.
    """)

    # Tools and Technologies Used
    st.header("Tools and Technologies")
    st.write("""
        - **Python** : Programming language used for data analysis and modeling.
        - **Streamlit** : Framework for building the web application interface.
        - **Pandas** : Library for data manipulation and analysis.
        - **Scikit-Learn** : Machine learning library for model building.
        - **Plotly and Matplotlib / Seaborn** : Libraries for data visualization.
    """)

    # Conclusion
    st.header("Conclusion")
    st.write("""
        The **Student Performance Analysis and Prediction** project provides valuable insights into student performance.
        The prediction model serves as a useful tool for educators and administrators to identify at-risk students
        and implement strategies for improvement.
    """)

    # Contact Information
    st.header("Contact Information")
    st.write("""
        For further information or inquiries, please contact:
        - **Email** : [vivektusharma@gmail.com](mailto:vivektusharma@gmail.com)
        - **GitHub Repository** : [GitHub Link](https://github.com/Vivek02Sharma/Student-Performance-Analysis-and-Prediction.git)
    """)

if __name__ == "__main__":
    about()
