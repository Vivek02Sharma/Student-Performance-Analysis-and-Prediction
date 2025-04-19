import os
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.subplots as sp
import warnings
warnings.filterwarnings("ignore")


raw_data_path = os.path.join('data','raw','BMS_raw.csv')
process_data_path = os.path.join('data','processed',"BMS_process.csv")

def dataset():
    st.markdown("### Dive Deep into Student Performance Dataset")
    st.markdown("""
~ ' Without data, you're just another person with an opinion '
--- `W. Edwards Deming`
""")

    # reading the raw dataset
    st.write("#### Original Data")
    raw_df = pd.read_csv(raw_data_path)
    st.dataframe(raw_df.head())

# ------------------------------------------------------------------------------------
    text = f"""
#### 1. General Information

- **Number of Rows:** {raw_df.shape[0]}
- **Number of Columns:** {raw_df.shape[1]}
"""
    st.markdown(text)

    # merging columns information
    column_info = pd.DataFrame({
    'Column Name': raw_df.columns,
    'Data Type': raw_df.dtypes.astype(str)
    }).reset_index(drop=True)
    
    # showing column_info
    st.markdown("- **Column Names and Data Types**")
    st.dataframe(column_info,use_container_width = True)
    st.write("**Conclusion :** Some subject marks are recorded as object data types due to the presence of grace marks, which are denoted by an asterisk ('*').")

    # merging the column's value 
    missing_value_info = pd.DataFrame({
    'Column Name': raw_df.columns,
    'Count Of Missing Value': raw_df.isnull().sum()
    }).reset_index(drop=True)

    st.markdown("- **Missing values**")
    st.dataframe(missing_value_info,use_container_width = True)

    # creating the note 
    st.write("**Note :** The dataset below was generated after performing `Data Preprocessing`.")

    # reading the process dataset
    st.write("#### Processed Data")
    process_df = pd.read_csv(process_data_path)
    st.dataframe(process_df.head())

# # --------------------------------------------------------------------------------------------
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
    
# --------------------------------------------------------------------------------------------------------
    st.write("#### 3. Data Distribution and Visualization")

    figs = []
    for col in process_df.drop(['StudentId','Remark','Grade','TotalMarks'], axis=1).columns:
        fig = px.histogram(process_df,x = col,nbins = 30,title = f"Histogram of {col}",color = 'Remark',barmode='overlay')
        figs.append(fig)

    st.markdown("- **Distribution of numerical columns**")
    for fig in figs:
        st.plotly_chart(fig)

    # creating boxplot 
    fig_TMO = px.box(process_df, y='TotalMarksObtained', title='Boxplot of TotalMarksObtained')
    fig_PCT = px.box(process_df, y='Percentage', title='Boxplot of Percentage')
    fig = sp.make_subplots(rows = 1,cols = 2,subplot_titles=['TotalMarksObtained', 'Percentage'])

    for trace in fig_TMO.data:
        trace.update(marker_color='red')
        fig.add_trace(trace,row = 1,col = 1)
    
    for trace in fig_PCT.data:
        trace.update(marker_color='blue')
        fig.add_trace(trace,row = 1,col = 2)

    fig.update_layout(height=600, width=800)
    st.markdown("- **Boxplot of TotalMarksObtained and Percentage**")
    st.plotly_chart(fig)

    # creating clountplot
    st.markdown("- **Countplot of Remark and Grade**")

    # remark
    fig_remark_count = px.bar(process_df['Remark'].value_counts(), color = process_df['Remark'].unique(), title = "Countplot of Remark") # Removed y='Remark'
    fig_remark_count.update_layout(xaxis_title='Remark',yaxis_title='Count')
    st.plotly_chart(fig_remark_count)

    # grade
    fig_grade_count = px.bar(process_df['Grade'].value_counts(), color = process_df['Grade'].unique(), title = "Countplot of Grade") # Removed y='Grade'
    fig_grade_count.update_layout(xaxis_title='Grade',yaxis_title='Count')
    st.plotly_chart(fig_grade_count)

    # pie chart of pass and fail
    st.markdown("- **Pie chart of Pass and Fail**")
    remark = process_df['Remark'].value_counts(normalize = True)
    fig_pie = px.pie(remark,
                    values = remark.values,
                    names = remark.index,
                    title = 'Percentage of Pass and Fail',
                    hole = 0.3
                    )
    fig_pie.update_traces(
    textinfo = 'percent',
    textfont_size = 16
    )
    st.plotly_chart(fig_pie)

    # # pie chart of pass and fail
    # st.markdown("- **Pie chart of Pass and Fail**")
    # remark = process_df['Remark'].value_counts(normalize = True)
    # fig_pie = px.pie(remark,
    #                  values = remark.values,
    #                  names = remark.index,
    #                  title = 'Percentage of Pass and Fail',
    #                  hole = 0.3
    #                 )
    # fig_pie.update_traces(
    # textinfo = 'percent',  
    # textfont_size = 16
    # )
    # st.plotly_chart(fig_pie)



    










    # hist_col = process_df.drop(['StudentId','Remark','Grade','TotalMarksObtained'], axis=1).columns
    # num_cols = 2
    # num_rows = (len(hist_col) + num_cols - 1) // num_cols # number of rows needed
    # fig = sp.make_subplots(rows = num_rows,cols = num_cols,subplot_titles = [f"Histogram of {col}" for col in hist_col])
    # for i,col in enumerate(hist_col,1):
    #     row = (i - 1) // num_cols + 1
    #     col_idx = (i - 1) % num_cols + 1
    #     hist = px.histogram(process_df, x=col,title = f"Histogram of {col}")
    #     for trace in hist.data:
    #         fig.add_trace(trace,row = row,col = col_idx)
    
    # fig.update_layout(
    # height=2000, 
    # width=1000,
    # title_text = "Distribution of Columns"
    # )
    
    # st.plotly_chart(fig)


