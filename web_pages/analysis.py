import os
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.subplots as sp
import plotly.figure_factory as ff

process_data_path = os.path.join('data','processed',"BMS_process.csv")

def data_analysis():
    df = pd.read_csv(process_data_path)
    st.markdown("### In-Depth Analysis of Student Performance")

    # Performance Distribution Analysis
    figs = []
    dist_columns = ['TotalMarksObtained', 'Percentage', 'SGPA']
    for col in dist_columns:
        fig = ff.create_distplot([df[col]],[col])
        fig.update_layout(title = f'Distribution plot of {col}')
        figs.append(fig)
    
    st.write('#### 1. Performance Distribution Analysis')
    for fig in figs:
        st.plotly_chart(fig)

# --------------------------------------------------------------------------------------
    # Grade Analysis vs Performance
    figs = []
    for col in dist_columns:
        fig = px.box(data_frame = df,x = 'Grade',y = df[col],color = 'Grade',title = f'Grade vs {col}',points = 'all')
        figs.append(fig)

    st.write('#### 2. Grade Analysis vs Performance')
    for fig in figs:
        st.plotly_chart(fig)

# -------------------------------------------------------------------------------------------
    # Remark Based Analysis
    figs = []
    for col in dist_columns:
        fig = px.box(data_frame = df,x = 'Remark',y = df[col],color = 'Remark',title = f'{col} by Remark',points = 'all')
        figs.append(fig)

    st.write('#### 3. Remark Based Analysis')
    for fig in figs:
        st.plotly_chart(fig)

    st.markdown("- **Distribution of Marks Across Grades and Remarks**")
    fig = px.scatter(data_frame = df,x = 'Grade',y = 'TotalMarksObtained',color = 'Remark')
    st.plotly_chart(fig)

#----------------------------------------------------------------------------------------------------
    # Course Performance Analysis
    st.write('#### 4. Course Performance Analysis')
    course_columns = [col for col in df.columns if col.startswith(('INT_', 'EXT_'))]

    df_long = df.melt(id_vars = ['StudentId'], value_vars = course_columns, var_name = 'Course', value_name =  'Score')
    fig = px.box(data_frame = df_long,x = 'Course', y = 'Score',color = 'Course',title = 'Course-wise Performance',)
    fig.update_layout(xaxis_title = 'Course',yaxis_title = 'Score',xaxis_tickangle = -90)
    st.plotly_chart(fig)

    # Performance Correlation
    st.markdown("- **Performance Correlation**")
    correlation_metrics = df[course_columns].corr().round(2)

    fig = px.imshow(
    correlation_metrics,
    text_auto = True,
    color_continuous_scale = 'Viridis'
    )

    fig.update_layout(
        title = 'Correlation Heatmap',
        xaxis = dict(tickangle = -90),
        height = 800
    )

    fig.layout.autosize = True
    fig.update_traces(textfont=dict(size = 12))

    st.plotly_chart(fig)

#----------------------------------------------------------------------------------------------------
    # Credits and Marks Analysis
    st.write('#### 5. Credits and Marks Analysis')
    st.markdown("- **Credits vs Marks**")
    fig = px.scatter(data_frame = df,x = 'CreditsEarned',y = 'TotalMarksObtained',color = 'Remark',title = "Credits Earned vs Total Marks Obtained")
    st.plotly_chart(fig)

    # Credits and Percentage
    st.markdown("- **Credits vs Percentage**")
    fig = px.scatter(data_frame = df,x = 'CreditsEarned',y = 'Percentage',color = 'Remark',title = "Credits Earned vs Percentage")
    st.plotly_chart(fig)









