import streamlit as st

def home():
    # Introduction
    st.markdown(
        """
        ## Welcome to the **Student Performance Analysis and Prediction System**!

        This tool provides **educators, administrators, and institutions** with data-driven insights into student performance, 
        allowing them to analyze trends, predict future academic outcomes, and identify students who may need additional support. 
        By leveraging machine learning models, the system enables **early intervention** and helps in **planning academic strategies**.
        """
    )

    # Key Features Section
    st.markdown("### 🔑 Key Features")
    st.write(
        """
        - **📊 Analyze Performance Trends:**  
          Gain insights from historical data and visualize trends across multiple semesters.  
          Use dynamic graphs and charts to spot patterns in student behavior, grades, and performance.
          
        - **🤖 Predict Student Grades:**  
          Predict future student outcomes using trained machine learning models (e.g., Decision Trees, Random Forest, Naïve Bayes).  
          Forecast results early to support timely intervention strategies.

        - **🚨 Identify At-Risk Students:**  
          Highlight students who are performing poorly or are likely to underperform in the future.  
          Provide educators with actionable insights to help improve these students’ performance.

        - **📝 Generate Reports:**  
          Automatically generate **personalized reports** containing key metrics for each student.  
          Export these reports as PDFs or CSVs to share with stakeholders and students.
        """
    )

    # How to Use Section with Instructions
    st.markdown("### 📋 How to Use")
    st.write(
        """
        - **📁 About Dataset:**  
          Explore the **student data** used for analysis and prediction.  
          Understand the structure of the dataset, including student records, grades, and attendance.

        - **📈 Data Analysis:**  
          Visualize data trends with interactive graphs.  
          Use tools like **Plotly** and **Seaborn** to uncover patterns in student performance.

        - **🔮 Prediction Model:**  
          Use the trained machine learning models to **forecast grades**.  
          Input new student data and predict their performance for upcoming semesters.

        - **📢 About:**  
          Learn more about the project, including its **purpose**, **scope**, and **development team**.
        """
    )

    # Call-to-Action Button with Explanation
    st.markdown("### 🚀 Ready to Get Started?")
    st.write(
        """
        Whether you're a teacher looking for insights or an administrator planning interventions, 
        this system empowers you to **make informed decisions**.
        """
    )

    # Footer Section with a Motivational Message
    st.markdown("---")
    st.write(
        """
        🔍 *Empowering education through data-driven insights.*  
        Use this system to help students achieve **academic success** and build a **better future**.
        """
    )