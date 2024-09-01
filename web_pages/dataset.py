import streamlit as st
import os
import pandas as pd

raw_data_path = os.path.join('data','raw','BMS_raw.csv')
process_data_path = os.path.join('data','processed',"BMS_process.csv")

def dataset():
    st.markdown("#### Dive Deep into Our Student Performance Dataset")
    st.markdown("<p style = 'text-align:center'> - 'Data also speak'</p>",unsafe_allow_html = True)

    st.write("**Original Data**")
    raw_df = pd.read_csv(raw_data_path)
    st.dataframe(raw_df.head())

    st.write("**Processed Data**")
    process_df = pd.read_csv(process_data_path)
    st.dataframe(process_df.head())

