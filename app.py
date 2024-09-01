import os
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

from src.mongodb import get_data_from_mongodb
from src.data_preprocessing import clean_data

from web_pages import home,dataset,analysis,prediction,about

def main():
    # Load and preprocess data
    st.markdown("## :blue[Student Performance Analysis and Prediction]")
    st.markdown("---")
    # creating a side bar 
    with st.sidebar:
        collection_name = st.selectbox(
            label="Select the semester",
            options=['sem1', 'sem2']
        )

        # sending collection_name to mongodb.py 
        get_data_from_mongodb(collection_name)

        # creating a menu option 
        bar = option_menu(
            menu_title="Menu",
            menu_icon = "list",
            options=["Home", "About Dataset", "Data Analysis", "Prediction Model", "About"]
        )

    # executing data preprocessing
    clean_data()
    
    # viewing pages
    if bar == "Home":
        home.home()

    elif bar == "About Dataset":
        dataset.dataset()

    elif bar == "Data Analysis":
        analysis.data_analysis()

    elif bar == "Prediction Model":
        prediction.model_prediction()

    elif bar == "About":
        about.about()


    # df = load_data()
    # df = clean_data(df)
    # df = create_features(df)
        
    # st.write("Data Preview:", df.head())
        
    # model = load_model('models/model.pkl')
    # predictions = model.predict(df.drop('TargetVariable', axis=1))
    # st.write("Predictions:", predictions)


if __name__=="__main__":
    main()