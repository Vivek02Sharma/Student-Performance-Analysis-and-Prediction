import streamlit as st
import os
import pandas as pd
import numpy as np
import plotly.express as px

raw_data_path = os.path.join('data','raw','BMS_raw.csv')
process_data_path = os.path.join('data','processed',"BMS_process.csv")

def dataset():
    st.markdown("### Dive Deep into Our Student Performance Dataset")
    st.markdown("""
~ ' Without data, you're just another person with an opinion '
--- `W. Edwards Deming`
""")

    # reading the raw dataset
    st.write("#### Original Data")
    raw_df = pd.read_csv(raw_data_path)
    st.dataframe(raw_df.head())

    text = f"""
#### 1. General Information

- **Number of Rows:** {raw_df.shape[0]}
- **Number of Columns:** {raw_df.shape[1]}
"""
    st.markdown(text)

    # merging columns information
    column_info = pd.DataFrame({
    'Column Name': raw_df.columns,
    'Data Type': raw_df.dtypes
    }).reset_index(drop=True)
    
    # showing column_info
    st.markdown("- **Column Names and Data Types**")
    st.dataframe(column_info,use_container_width = True)

    # merging the column's value 
    missing_value_info = pd.DataFrame({
    'Column Name': raw_df.columns,
    'Count Of Missing Value': raw_df.isnull().sum()
    }).reset_index(drop=True)

    st.markdown("- **Missing values**")
    st.dataframe(missing_value_info,use_container_width = True)

    # creating the note 
    st.write("**Note :** After performing `Data Preprocessing` below dataset is generated")

    # reading the process dataset
    st.write("#### Processed Data")
    process_df = pd.read_csv(process_data_path)
    st.dataframe(process_df.head())

    st.write("#### 2. Descriptive Statistics")

    # checking minimum of TotalMarksObtained, CreditsEarned, Percentage, SGPA
    TMO_min = process_df['TotalMarksObtained'].min()
    CreditsEarned_min = process_df['CreditsEarned'].min()
    Percentage_min = process_df['Percentage'].min()
    SGPA_min = process_df['SGPA'].min()

    st.markdown(f"""
- **Calcualating the `Minimum` values of TotalMarksObtained, CreditsEarned, Percentage, SGPA**

| Column Name                   | Minimum Value |
|-------------------------------|-----------|
| TotalMarksObtained            | {TMO_min}    |
| CreditsEarned                 | {CreditsEarned_min}    |
| Percentage                    | {Percentage_min}    |
| SGPA                          | {SGPA_min}    |
""")

    # checking average of TotalMarksObtained, CreditsEarned, Percentage, SGPA
    TMO_avg = process_df['TotalMarksObtained'].mean()
    CreditsEarned_avg = process_df['CreditsEarned'].mean()
    Percentage_avg = process_df['Percentage'].mean()
    SGPA_avg = process_df['SGPA'].mean()

    st.markdown(f"""
- **Calcualating the `Average` values of TotalMarksObtained, CreditsEarned, Percentage, SGPA**

| Column Name                   | Average Value |
|-------------------------------|-----------|
| TotalMarksObtained            | {round(TMO_avg,2)}    |
| CreditsEarned                 | {round(CreditsEarned_avg,2)}    |
| Percentage                    | {round(Percentage_avg,2)}    |
| SGPA                          | {round(SGPA_avg,2)}    |
""")
    
    # checking maximum of TotalMarksObtained, CreditsEarned, Percentage, SGPA
    TMO_max = process_df['TotalMarksObtained'].max()
    CreditsEarned_max = process_df['CreditsEarned'].max()
    Percentage_max = process_df['Percentage'].max()
    SGPA_max = process_df['SGPA'].max()

    st.markdown(f"""
- **Calcualating the `Maximum` values of TotalMarksObtained, CreditsEarned, Percentage, SGPA**

| Column Name                   | Maximum Value |
|-------------------------------|-----------|
| TotalMarksObtained            | {TMO_max}    |
| CreditsEarned                 | {CreditsEarned_max}    |
| Percentage                    | {Percentage_max}    |
| SGPA                          | {SGPA_max}    |
""")

    # value count of categorical columns
    st.write("- **Frequency count of categorical columns**")
    st.text(f"""
1. Remark
{process_df['Remark'].value_counts()}\n
2. Grade
{process_df['Grade'].value_counts()}
""")
    
    st.write("#### 3. Data Distribution and Visualization")

    # for col in process_df.select_dtypes([np.number]).columns:
    #     fig = px.histogram(process_df,x = col)
    #     fig.update_layout(title = col)
    #     st.plotly_chart(fig)