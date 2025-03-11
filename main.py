# import os
# import streamlit as st
# from streamlit_option_menu import option_menu
# import pymongo
# from datetime import datetime

# from src.mongodb import get_data_from_mongodb
# from src.data_preprocessing import clean_data

# from web_pages import home, dataset, analysis, prediction, about, dashboard, progress
# from src.logger import logging

# # Initialize session state variables
# if 'logged_in' not in st.session_state:
#     st.session_state['logged_in'] = False

# if 'user_type' not in st.session_state:
#     st.session_state['user_type'] = ""

# if 'current_page' not in st.session_state:
#     st.session_state['current_page'] = "get_started"

# if 'app_running' not in st.session_state:
#     st.session_state.app_running = True

# if 'professor_name' not in st.session_state:
#     st.session_state['professor_name'] = None

# if 'student_name' not in st.session_state:
#     st.session_state['student_name'] = None

# if 'student_id' not in st.session_state:
#     st.session_state['student_id'] = None


# # MongoDB connection
# def get_database():
#     client = pymongo.MongoClient("mongodb://localhost:27017/")
#     return client["college_db"]

# db = get_database()
# professors_collection = db["professors"]
# students_collection = db["students"]

# # Navigation functions
# def navigate_to_login():
#     st.session_state['current_page'] = "login"
    
# def navigate_to_get_started():
#     st.session_state['current_page'] = "get_started"

# def navigate_to_dashboard():
#     st.session_state['current_page'] = "dashboard"

# # Authentication functions
# def authenticate_professor(email, password):
#     professor = professors_collection.find_one({"Email_Id": email, "Password": password})
#     if professor:
#         professor_name = professor.get("Name")
#         st.session_state['professor_name'] = professor_name
#         return professor
#     return None

# def authenticate_student(student_id, password):
#     student = students_collection.find_one({"StudentId": student_id, "Password": password})
#     if student:
#         student_name = student.get("StudentName")
#         st.session_state['student_id'] = student_id
#         st.session_state['student_name'] = student_name
#         return student
#     return None

# def set_login_type_and_navigate(user_type):
#     st.session_state['user_type'] = user_type
#     navigate_to_login()

# # Login UI Components
# def get_started_page():
#     st.markdown("## :orange[Student Performance Analysis and Prediction]")
    
#     st.markdown("Analyze and predict student performance using machine learning models.")
#     st.subheader("Log in to continue")
    
#     # Login buttons
#     col_btn1, col_btn2 = st.columns(2)
#     with col_btn1:
#         st.button("I'm a Professor", on_click=lambda: set_login_type_and_navigate("professor"), 
#                  type="primary", use_container_width=True)
#     with col_btn2:
#         st.button("I'm a Student", on_click=lambda: set_login_type_and_navigate("student"), 
#                  type="primary", use_container_width=True)
    
#     st.markdown("© 2025 Educational Institution. All rights reserved.")

# def login_page():
#     # Back button
#     st.button("← Back", on_click=navigate_to_get_started)
    
#     if st.session_state['user_type'] == "professor":
#         st.title("🔑 Professor Login")
        
#         with st.form("professor_login_form"):
#             email = st.text_input("Email Address")
#             password = st.text_input("Password", type="password")
#             submit_button = st.form_submit_button("Login", use_container_width=True)
            
#             if submit_button:
#                 if not email or not password:
#                     st.error("Please fill in all fields")
#                 else:
#                     professor = authenticate_professor(email, password)
#                     if professor:
#                         st.session_state['logged_in'] = True
#                         import time
#                         time.sleep(1)
#                         navigate_to_dashboard()
#                         st.rerun()
#                     else:
#                         st.error("Invalid email or password")
    
#     else:  # Student login
#         st.title("🔑 Student Login")
        
#         with st.form("student_login_form"):
#             student_id = st.text_input("Student ID")
#             password = st.text_input("Password", type="password")
#             submit_button = st.form_submit_button("Login", use_container_width=True)
            
#             if submit_button:
#                 if not student_id or not password:
#                     st.error("Please fill in all fields")
#                 else:
#                     student = authenticate_student(student_id, password)
#                     if student:
#                         st.session_state['logged_in'] = True
#                         import time
#                         time.sleep(1)
#                         navigate_to_dashboard()
#                         st.rerun()
#                     else:
#                         st.error("Invalid Student ID or password")

# def main_application():
#     try:
#         # Display header and separator
#         st.markdown("## :blue[Student Performance Analysis and Prediction]")
#         st.markdown("---")

#         # Create a sidebar with a semester selection dropdown
#         with st.sidebar:
#             collection_name = st.selectbox(
#                 label = "Select the semester",
#                 options = ['sem1', 'sem2']
#             )
#             logging.info(f"Selected collection: {collection_name}")

#             # # Create the sidebar menu
#             # bar = option_menu(
#             #     menu_title = "Menu",
#             #     menu_icon = "list",
#             #     options = ["Home", "About Dataset", "Data Analysis", "Prediction Model", "About"]
#             # )

#              # Create different menus based on user type
#             if st.session_state['user_type'] == "professor":
#                 # Professor menu
#                 bar = option_menu(
#                     menu_title = "Menu",
#                     menu_icon = "list",
#                     options = ["Home", "About Dataset", "Data Analysis", "Prediction Model", "About"]
#                 )
#             else:
#                 # Student menu
#                 bar = option_menu(
#                     menu_title = "Menu",
#                     menu_icon = "list",
#                     options = ["Home", "My Dashboard", "My Progress", "Prediction Model", "About"]
#                 )
            
#             logging.info(f"Selected menu option: {bar}")

#             # Add logout button to sidebar
#             if st.button("Logout"):
#                 st.session_state['logged_in'] = False
#                 st.session_state['user_type'] = ""
#                 navigate_to_get_started()
#                 st.rerun()

#         # Retrieve data from MongoDB
#         logging.info("Fetching data from MongoDB...")
#         get_data_from_mongodb(collection_name)

#         # Execute data cleaning
#         logging.info("Starting data preprocessing...")
#         clean_data()

#         # Navigate between different pages based on menu selection
#         if bar == "Home":
#             logging.info("Navigating to Home page.")
#             home.home()

#         elif bar == "About Dataset":
#             logging.info("Navigating to About Dataset page.")
#             dataset.dataset()

#         elif bar == "My Dashboard":
#             logging.info("Navigating to my dashboard page.")
#             dashboard.student_marks_dashboard()

#         elif bar == "Data Analysis":
#             logging.info("Navigating to Data Analysis page.")
#             analysis.data_analysis()
        
#         elif bar == "My Progress":
#             logging.info("Navigating to My progress page.")
#             progress.student_progress_analysis()

#         elif bar == "Prediction Model":
#             logging.info("Navigating to Prediction Model page.")
#             prediction.model_prediction()

#         elif bar == "About":
#             logging.info("Navigating to About page.")
#             about.about()

#     except Exception as e:
#         logging.error(f"An error occurred: {e}")

# def main():
#     st.set_page_config(page_title="Student Performance Analysis and Prediction", page_icon="./assets/favicon.png", layout="wide")
    
#     # Check if user is logged in
#     if st.session_state['logged_in']:
#         main_application()
#     else:
#         # Show login pages
#         if st.session_state['current_page'] == "get_started":
#             get_started_page()
#         elif st.session_state['current_page'] == "login":
#             login_page()
# if __name__ == "__main__":
#     logging.info("Starting application...")
#     main()

# main.py
import os
import streamlit as st
from streamlit_option_menu import option_menu
import pymongo
from datetime import datetime

from src.mongodb import get_data_from_mongodb
from src.data_preprocessing import clean_data

from web_pages import home, dataset, analysis, prediction, about, dashboard, progress # import dashboard
from src.logger import logging

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'user_type' not in st.session_state:
    st.session_state['user_type'] = ""

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "get_started"

if 'app_running' not in st.session_state:
    st.session_state.app_running = True

if 'professor_name' not in st.session_state:
    st.session_state['professor_name'] = None

if 'student_name' not in st.session_state:
    st.session_state['student_name'] = None

if 'student_id' not in st.session_state:
    st.session_state['student_id'] = None


# MongoDB connection
def get_database():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    return client["college_db"]

db = get_database()
professors_collection = db["professors"]
students_collection = db["students"]

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
        professor_name = professor.get("Name")
        st.session_state['professor_name'] = professor_name
        return professor
    return None

def authenticate_student(student_id, password):
    student = students_collection.find_one({"StudentId": student_id, "Password": password})
    if student:
        student_name = student.get("StudentName")
        st.session_state['student_id'] = student_id
        st.session_state['student_name'] = student_name
        return student
    return None

def set_login_type_and_navigate(user_type):
    st.session_state['user_type'] = user_type
    navigate_to_login()

# Login UI Components
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

    st.markdown("© 2025 Educational Institution. All rights reserved.")

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
                        import time
                        time.sleep(1)
                        navigate_to_dashboard()
                        st.rerun()
                    else:
                        st.error("Invalid Student ID or password")

def main_application():
    try:
        # Set page config here so it applies to all pages in main_application
        st.set_page_config(page_title="Student Performance Analysis and Prediction", page_icon="./assets/favicon.png", layout="wide")

        # Display header and separator
        st.markdown("## :blue[Student Performance Analysis and Prediction]")
        st.markdown("---")

        # Create a sidebar with a semester selection dropdown and menu
        with st.sidebar:
            collection_name = st.selectbox(
                label = "Select the semester",
                options = ['sem1', 'sem2']
            )
            logging.info(f"Selected collection: {collection_name}")

            # Create different menus based on user type
            if st.session_state['user_type'] == "professor":
                # Professor menu
                bar = option_menu(
                    menu_title = "Menu",
                    menu_icon = "list",
                    options = ["Home", "About Dataset", "Data Analysis", "Prediction Model", "About"]
                )
            else:
                # Student menu
                bar = option_menu(
                    menu_title = "Menu",
                    menu_icon = "list",
                    options = ["Home", "My Dashboard", "My Progress", "Prediction Model", "About"]
                )

            logging.info(f"Selected menu option: {bar}")

            # Add logout button to sidebar
            if st.button("Logout"):
                st.session_state['logged_in'] = False
                st.session_state['user_type'] = ""
                navigate_to_get_started()
                st.rerun()

        # Retrieve data from MongoDB
        logging.info("Fetching data from MongoDB...")
        get_data_from_mongodb(collection_name)

        # Execute data cleaning
        logging.info("Starting data preprocessing...")
        clean_data()

        # Navigate between different pages based on menu selection
        if bar == "Home":
            logging.info("Navigating to Home page.")
            home.home()

        elif bar == "About Dataset":
            logging.info("Navigating to About Dataset page.")
            dataset.dataset()

        elif bar == "My Dashboard":
            logging.info("Navigating to My Dashboard page.")
            dashboard.student_marks_dashboard() # Call student_marks_dashboard from dashboard.py

        elif bar == "Data Analysis":
            logging.info("Navigating to Data Analysis page.")
            analysis.data_analysis()

        elif bar == "My Progress":
            logging.info("Navigating to My progress page.")
            progress.student_progress_analysis()

        elif bar == "Prediction Model":
            logging.info("Navigating to Prediction Model page.")
            prediction.model_prediction()

        elif bar == "About":
            logging.info("Navigating to About page.")
            about.about()

    except Exception as e:
        logging.error(f"An error occurred: {e}")

def main():
    # Page config is set inside main_application to apply to all pages after login
    # st.set_page_config(page_title="Student Performance Analysis and Prediction", page_icon="./assets/favicon.png", layout="wide")

    # Check if user is logged in
    if st.session_state['logged_in']:
        main_application()
    else:
        # Show login pages
        if st.session_state['current_page'] == "get_started":
            get_started_page()
        elif st.session_state['current_page'] == "login":
            login_page()

if __name__ == "__main__":
    logging.info("Starting application...")
    main()