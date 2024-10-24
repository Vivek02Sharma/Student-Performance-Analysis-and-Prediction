import os
import streamlit as st
from streamlit_option_menu import option_menu

from src.mongodb import get_data_from_mongodb
from src.data_preprocessing import clean_data

from web_pages import home, dataset, analysis, prediction, about
from src.logger import logging

st.set_page_config(
    page_title = "Student Performance Analysis and Prediction"
)

# Prevent application from re-running on every interaction
if 'app_running' not in st.session_state:
    st.session_state.app_running = True


def main():
    try:
        # Display header and separator
        st.markdown("## :blue[Student Performance Analysis and Prediction]")
        st.markdown("---")

        # Create a sidebar with a semester selection dropdown
        with st.sidebar:
            collection_name = st.selectbox(
                label = "Select the semester",
                options = ['sem1', 'sem2', 'sem3', 'sem4', 'sem5', 'sem6']
            )
            logging.info(f"Selected collection: {collection_name}")

            # Create the sidebar menu
            bar = option_menu(
                menu_title = "Menu",
                menu_icon = "list",
                options = ["Home", "About Dataset", "Data Analysis", "Prediction Model", "About"]
            )
            logging.info(f"Selected menu option: {bar}")

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

        elif bar == "Data Analysis":
            logging.info("Navigating to Data Analysis page.")
            analysis.data_analysis()

        elif bar == "Prediction Model":
            logging.info("Navigating to Prediction Model page.")
            prediction.model_prediction()

        elif bar == "About":
            logging.info("Navigating to About page.")
            about.about()

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    logging.info("Executing main application logic...")
    main()
