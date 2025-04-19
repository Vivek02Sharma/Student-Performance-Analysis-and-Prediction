import streamlit as st
import pymongo

def get_database():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    return client["college_db"]

db = get_database()
professors_collection = db["professors"]
students_collection = db["students"]

# Create session state variables
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = ""
if 'user_type' not in st.session_state:
    st.session_state['user_type'] = ""
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "get_started"


# Navigation functions
def navigate_to_login():
    st.session_state['current_page'] = "login"
    
def navigate_to_get_started():
    st.session_state['current_page'] = "get_started"

def navigate_to_dashboard():
    st.session_state['current_page'] = "dashboard"


# Authentication functions
def authenticate_professor(email, password):
    professor = professors_collection.find_one({"Email_Id": email, "Password": password})

    if professor:
        return professor
    return None

def authenticate_student(student_id, password):
    student = students_collection.find_one({"StudentId": student_id, "Password": password})
    
    if student:
        return student
    return None


# UI Components
def get_started_page():
    st.markdown("## :orange[Student Performance Analysis and Prediction]")
    
    st.markdown("Analyze and predict student performance using machine learning models.")
    st.subheader("Log in to continue")
    
    # Login buttons
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.button("I'm a Professor", on_click=lambda: set_login_type_and_navigate("professor"), 
                 type="primary", use_container_width=True)
    with col_btn2:
        st.button("I'm a Student", on_click=lambda: set_login_type_and_navigate("student"), 
                 type="primary", use_container_width=True)
    
    # Footer
    st.markdown("© 2025 Educational Institution. All rights reserved.")

def set_login_type_and_navigate(user_type):
    st.session_state['user_type'] = user_type
    navigate_to_login()

def login_page():
    # Back button
    st.button("← Back", on_click=navigate_to_get_started)
    
    if st.session_state['user_type'] == "professor":
        st.title("🔑 Professor Login")
        
        with st.form("professor_login_form"):
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login", use_container_width=True)
            
            if submit_button:
                if not email or not password:
                    st.error("Please fill in all fields")
                else:
                    professor = authenticate_professor(email, password)
                    if professor:
                        st.session_state['logged_in'] = True
                        # st.session_state['user_name'] = professor["name"]
                        # st.success(f"Welcome, Professor {professor['name']}! 🎓")
                        import time
                        time.sleep(1)
                        navigate_to_dashboard()
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
    
    else:  # Student login
        st.title("🔑 Student Login")
        
        with st.form("student_login_form"):
            student_id = st.text_input("Student ID")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login", use_container_width=True)
            
            if submit_button:
                if not student_id or not password:
                    st.error("Please fill in all fields")
                else:
                    student = authenticate_student(student_id, password)
                    if student:
                        st.session_state['logged_in'] = True
                        # st.session_state['user_name'] = student["name"]
                        # st.success(f"Welcome, {student['name']}! 📚")
                        import time
                        time.sleep(1)
                        navigate_to_dashboard()
                        st.rerun()
                    else:
                        st.error("Invalid Student ID or password")

def dashboard_page():
    st.title(f"Welcome!")
    
    user_type = "Professor" if st.session_state['user_type'] == "professor" else "Student"
    st.write(f"You are logged in as a {user_type}.")
    
    # Quick access dashboard
    st.subheader("🔍 Quick Access")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 View Student Performance")
        st.button("Performance Data", key="performance_data")
    
    with col2:
        st.markdown("### 📉 Predict Student Outcomes")
        st.button("Predict Outcomes", key="predict_outcomes")
    
    with col3:
        st.markdown("### 📜 Download Reports")
        st.button("Generate Reports", key="generate_reports")
    
    # Logout button
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        # st.session_state['user_name'] = ""
        # st.session_state['user_type'] = ""
        navigate_to_get_started()
        st.rerun()

# Main app logic
def main_login():    
    if st.session_state['logged_in']:
        dashboard_page()
    else:
        if st.session_state['current_page'] == "get_started":
            get_started_page()
        elif st.session_state['current_page'] == "login":
            login_page()

st.set_page_config(page_title="Login Page", page_icon="🔐", layout="wide")
main_login()
