import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from io import BytesIO
import numpy as np
from src.mongodb import student_data

def get_subject_name(code):
    """Returns a readable subject name based on code"""
    subject_names = {
        'BMSBC103': 'Business Communication I',
        'BMSBL107': 'Business Law',
        'BMSBS106': 'Business Statistics',
        'BMSECO102': 'Economics',
        'BMSFA105': 'Financial Accounting',
        'BMSFC104': 'Foundation Course I',
        'BMSFHS101': 'Foundation in Human Skills',
        'BMSBC203': 'Business Communication II',
        'BMSBE201': 'Business Environment',
        'BMSBM206': 'Business Mathematics',
        'BMSFC204': 'Foundation Course II',
        'BMSIL207': 'Information Technology',
        'BMSMK205': 'Marketing',
        'BMSPM202': 'Principles of Management'
    }
    return subject_names.get(code, code)

def get_grade_color(grade):
    """Returns a color based on grade"""
    grade_colors = {
        'O': '#2E8B57',  # Green for Outstanding
        'A+': '#3366cc', # Blue for A+
        'A': '#6699cc',  # Light Blue for A
        'B+': '#9999cc', # Purplish for B+
        'B': '#cc9966',  # Bronze for B
        'C': '#cc6666',  # Reddish for C
        'D': '#cc3333',  # Red for D
        'F': '#990000'    # Dark Red for F
    }
    return grade_colors.get(grade, '#888888')  # Gray for unknown grades

def get_risk_level(percentage, trend, failed_subjects):
    # Define risk thresholds
    if percentage < 40:
        risk_level = "High Risk"
        color = "#ff0000"  # Red
        message = "Student is severely underperforming and at high risk of failing."
    elif percentage < 50:
        if trend < -5 or failed_subjects >= 2:
            risk_level = "High Risk"
            color = "#ff0000"  # Red
            message = "Student shows declining performance and multiple subject failures."
        else:
            risk_level = "Moderate Risk"
            color = "#ff9900"  # Orange
            message = "Student performance is below average but may improve with support."
    elif percentage < 60:
        if trend < -10 or failed_subjects >= 1:
            risk_level = "Moderate Risk"
            color = "#ff9900"  # Orange
            message = "Student shows declining trend or has failed subjects."
        else:
            risk_level = "Low Risk"
            color = "#ffcc00"  # Yellow
            message = "Student performance is average but needs improvement in some areas."
    else:
        if failed_subjects >= 1:
            risk_level = "Low Risk"
            color = "#ffcc00"  # Yellow
            message = "Student is performing well overall but has challenges in specific subjects."
        else:
            risk_level = "No Risk"
            color = "#00cc00"  # Green
            message = "Student is performing well with no significant risk factors."
            
    return risk_level, color, message

def analyze_subject_risk(subject_df, threshold=40):
    at_risk_subjects = subject_df[subject_df['Percentage'] < threshold]
    return at_risk_subjects


def generate_excel_report(student_name, sem1_df, sem2_df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        sem1_df.to_excel(writer, index=False, sheet_name='Semester 1')
        sem2_df.to_excel(writer, index=False, sheet_name='Semester 2')
        workbook = writer.book
        worksheet1 = writer.sheets['Semester 1']
        worksheet2 = writer.sheets['Semester 2']
        for sheet in [worksheet1, worksheet2]:
            for col_num, value in enumerate(sem1_df.columns.values):
                sheet.set_column(col_num, col_num, 18)
    output.seek(0)
    return output

def student_marks_dashboard():
    st.markdown("""
    <style>
    .main {
        padding: 1rem;
        background-color: #f8f9fa;
    }
    .header-container {
        background-color: #3366cc;
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    .grade-indicator {
        font-size: 1.2rem;
        font-weight: bold;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
    }
    .card-container {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .subject-card {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding: 1rem;
        background-color: #f0f0f0;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    student_name = st.session_state.get('student_name', 'Unknown Student')
    student_id = int(st.session_state.get('student_id', '0'))

    # MongoDB connection
    try:
        sem1_data, sem2_data = student_data(student_id=student_id)

        if not sem1_data and not sem2_data:
            st.error(f"No data found for student ID: {student_id} in either semester")
            return

    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return

    if sem1_data and sem2_data:
        # Student Information from data
        student_name = sem1_data.get('StudentName', 'Unknown Student')
        student_id = sem1_data.get('StudentId', 'Unknown ID')

        # --- MAIN CONTENT AREA ---

        # Header section with gradient
        st.markdown('<div class="header-container"><h1>📊 Student Academic Dashboard</h1></div>', unsafe_allow_html=True)

        col_info_1, col_info_2 = st.columns([1, 1])
        with col_info_1:
            st.markdown(f"**Student Name:** {student_name}")
        with col_info_2:
            st.markdown(f"**Student ID:** {student_id}")
        st.divider()

                      
        # Overview Cards
        st.subheader("Academic Overview")
        col1, col2, col3, col4 = st.columns(4)

        overall_percentage = (sem1_data.get('Percentage', 0) + sem2_data.get('Percentage', 0)) / 2
        overall_sgpa = (sem1_data.get('SGPA', 0) + sem2_data.get('SGPA', 0)) / 2
        total_credits = sem1_data.get('CreditsEarned', 0) + sem2_data.get('CreditsEarned', 0)

        with col1:
            with st.container(border=True):
                st.metric("Overall Percentage", f"{overall_percentage:.2f}%", f"{sem2_data.get('Percentage', 0) - sem1_data.get('Percentage', 0):.2f}%")

        with col2:
            with st.container(border=True):
                st.metric("Overall SGPA", f"{overall_sgpa:.2f}", f"{sem2_data.get('SGPA', 0) - sem1_data.get('SGPA', 0):.2f}")

        with col3:
            with st.container(border=True):
                st.metric("Credits Earned", total_credits)

        with col4:
            with st.container(border=True):
                st.metric("Subjects", "14") # Assuming 14 subjects in total

        # Semester Progress (horizontal bar)
        st.subheader("Program Completion")
        total_program_semesters = 6  # Typical for a bachelor's degree
        current_semester = 2  # Assuming student has data for sem 1 and 2

        progress_percentage = (current_semester / total_program_semesters) * 100
        st.progress(progress_percentage / 100)
        st.caption(f"You are in Semester {current_semester} of {total_program_semesters} ({progress_percentage:.1f}% complete)")

        # Semester Performance Summary
        st.subheader("Semester Performance")
        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.markdown(f"### Semester 1: {sem1_data.get('CourseName')}")
                st.markdown(f"<div class='grade-indicator' style='background-color: {get_grade_color(sem1_data.get('Grade'))}'>Grade: {sem1_data.get('Grade')}</div>", unsafe_allow_html=True)
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Percentage", f"{sem1_data.get('Percentage')}%")
                with col_b:
                    st.metric("SGPA", sem1_data.get('SGPA'))
                st.markdown(f"**Status:** {sem1_data.get('Remark')}")

        with col2:
            with st.container(border=True):
                st.markdown(f"### Semester 2: {sem2_data.get('CourseName')}")
                st.markdown(f"<div class='grade-indicator' style='background-color: {get_grade_color(sem2_data.get('Grade'))}'>Grade: {sem2_data.get('Grade')}</div>", unsafe_allow_html=True)
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Percentage", f"{sem2_data.get('Percentage')}%")
                with col_b:
                    st.metric("SGPA", sem2_data.get('SGPA'))
                st.markdown(f"**Status:** {sem2_data.get('Remark')}")

        # Visualization Section
        st.subheader("Performance Visualization")

        tab1, tab2 = st.tabs(["Overall Comparison", "Subject Analysis", 
                                    # "Grade Distribution"
                                    ])

        with tab1:
            fig = go.Figure()

            categories = ['Percentage', 'SGPA x 10']
            sem1_values = [sem1_data.get('Percentage'), sem1_data.get('SGPA') * 10]
            sem2_values = [sem2_data.get('Percentage'), sem2_data.get('SGPA') * 10]

            fig.add_trace(go.Bar(
                x=categories,
                y=sem1_values,
                name='Semester 1',
                marker_color='#3366cc'
            ))

            fig.add_trace(go.Bar(
                x=categories,
                y=sem2_values,
                name='Semester 2',
                marker_color='#ff9900'
            ))

            fig.update_layout(
                title='Semester Performance Comparison',
                barmode='group',
                xaxis_title='Metrics',
                yaxis_title='Value',
                legend_title='Semester',
                template='plotly_white',
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            # Extract subject data
            subjects_sem1 = []
            total_sem1 = []

            subjects_sem2 = []
            total_sem2 = []

            for key in sem1_data:
                if key.startswith('INT_'):
                    subject_code = key[4:]
                    int_marks = sem1_data.get(key, 0)
                    ext_marks = sem1_data.get(f'EXT_{subject_code}', 0)
                    total = int_marks + ext_marks
                    subjects_sem1.append(get_subject_name(subject_code))
                    total_sem1.append(total)

            for key in sem2_data:
                if key.startswith('INT_'):
                    subject_code = key[4:]
                    int_marks = sem2_data.get(key, 0)
                    ext_marks = sem2_data.get(f'EXT_{subject_code}', 0)
                    total = int_marks + ext_marks
                    subjects_sem2.append(get_subject_name(subject_code))
                    total_sem2.append(total)

            # Create subject performance chart
            col1, col2 = st.columns(2)

            with col1:
                fig = px.pie(
                    names=subjects_sem1,
                    values=total_sem1,
                    title="Semester 1 - Subject Distribution",
                    hole=0.4,
                    color_discrete_sequence=px.colors.sequential.Blues_r
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.pie(
                    names=subjects_sem2,
                    values=total_sem2,
                    title="Semester 2 - Subject Distribution",
                    hole=0.4,
                    color_discrete_sequence=px.colors.sequential.Oranges_r
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

        # with tab3:
        #     # Create a radar chart for grades
        #     # categories = ['Overall Grade', 'Communication', 'Technical Knowledge',
        #     #               'Problem Solving', 'Team Work', 'Time Management']

        #     # --- Calculate values_sem1 dynamically ---
        #     values_sem1 = [sem1_data.get('SGPA', 0)]
        #     subject_count_sem1 = 0
        #     for key in sem1_data:
        #         if key.startswith('INT_') and subject_count_sem1 < 5:
        #             subject_code = key[4:]
        #             internal = sem1_data.get(key, 0)
        #             external = sem1_data.get(f'EXT_{subject_code}', 0)
        #             total = internal + external
        #             percentage = (total / 100) * 100 if total <= 100 else 100
        #             scaled_percentage = (percentage / 100) * 10
        #             values_sem1.append(round(scaled_percentage, 1))
        #             subject_count_sem1 += 1
        #     # Pad with 0s if less than 5 subjects are found
        #     while len(values_sem1) < 6:
        #         values_sem1.append(0)

        #     values_sem2 = [sem2_data.get('SGPA', 0)]
        #     subject_count_sem2 = 0
        #     for key in sem2_data:
        #         if key.startswith('INT_') and subject_count_sem2 < 5:
        #             subject_code = key[4:]
        #             internal = sem2_data.get(key, 0)
        #             external = sem2_data.get(f'EXT_{subject_code}', 0)
        #             total = internal + external
        #             percentage = (total / 100) * 100 if total <= 100 else 100
        #             scaled_percentage = (percentage / 100) * 10
        #             values_sem2.append(round(scaled_percentage, 1))
        #             subject_count_sem2 += 1
        #     while len(values_sem2) < 6:
        #         values_sem2.append(0)

            # fig = go.Figure()

            # fig.add_trace(go.Scatterpolar(
            #     r=values_sem1,
            #     theta=categories,
            #     fill='toself',
            #     name='Semester 1',
            #     line_color='#3366cc'
            # ))

            # fig.add_trace(go.Scatterpolar(
            #     r=values_sem2,
            #     theta=categories,
            #     fill='toself',
            #     name='Semester 2',
            #     line_color='#ff9900'
            # ))

            # fig.update_layout(
            #     polar=dict(
            #         radialaxis=dict(
            #             visible=True,
            #             range=[0, 10]
            #         )),
            #     showlegend=True,
            #     title="Skill Assessment Radar",
            #     height=450
            # )

            # st.plotly_chart(fig, use_container_width=True)

        # Subject-wise Analysis
        st.subheader("Subject-wise Performance")

        subject_tab1, subject_tab2 = st.tabs(["Semester 1", "Semester 2"])

        with subject_tab1:
            subject_data = []
            for key in sem1_data:
                if key.startswith('INT_'):
                    subject_code = key[4:]
                    subject_name = get_subject_name(subject_code)
                    internal = sem1_data.get(key, 0)
                    external = sem1_data.get(f'EXT_{subject_code}', 0)
                    total = internal + external
                    percentage = (total / 100) * 100
                    subject_data.append({
                        'Subject': subject_name,
                        'Code': subject_code,
                        'Internal': internal,
                        'External': external,
                        'Total': total,
                        'Percentage': percentage
                    })

            # Create dataframe and sort
            subject_df = pd.DataFrame(subject_data)
            subject_df = subject_df.sort_values('Total', ascending=False)

            # Display bar chart
            fig = px.bar(
                subject_df,
                x='Subject',
                y=['Internal', 'External'],
                title="Subject-wise Marks Distribution (Semester 1)",
                barmode='stack',
                color_discrete_sequence=['#3366cc', '#99ccff']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

            # Display table with detailed data
            st.dataframe(
                subject_df,
                column_config={
                    'Subject': 'Subject Name',
                    'Code': 'Subject Code',
                    'Internal': st.column_config.NumberColumn('Internal (40)', format="%.0f"),
                    'External': st.column_config.NumberColumn('External (60)', format="%.0f"),
                    'Total': st.column_config.NumberColumn('Total (100)', format="%.0f"),
                    'Percentage': st.column_config.ProgressColumn('Percentage', format="%.1f%%", min_value=0, max_value=100)
                },
                hide_index=True,
                use_container_width=True
            )

        with subject_tab2:
            subject_data = []
            for key in sem2_data:
                if key.startswith('INT_'):
                    subject_code = key[4:]
                    subject_name = get_subject_name(subject_code)
                    internal = sem2_data.get(key, 0)
                    external = sem2_data.get(f'EXT_{subject_code}', 0)
                    total = internal + external
                    percentage = (total / 100) * 100
                    subject_data.append({
                        'Subject': subject_name,
                        'Code': subject_code,
                        'Internal': internal,
                        'External': external,
                        'Total': total,
                        'Percentage': percentage
                    })

            # Create dataframe and sort
            subject_df = pd.DataFrame(subject_data)
            subject_df = subject_df.sort_values('Total', ascending=False)

            # Display bar chart
            fig = px.bar(
                subject_df,
                x='Subject',
                y=['Internal', 'External'],
                title="Subject-wise Marks Distribution (Semester 2)",
                barmode='stack',
                color_discrete_sequence=['#ff9900', '#ffcc99']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

            # Display table with detailed data
            st.dataframe(
                subject_df,
                column_config={
                    'Subject': 'Subject Name',
                    'Code': 'Subject Code',
                    'Internal': st.column_config.NumberColumn('Internal (40)', format="%.0f"),
                    'External': st.column_config.NumberColumn('External (60)', format="%.0f"),
                    'Total': st.column_config.NumberColumn('Total (100)', format="%.0f"),
                    'Percentage': st.column_config.ProgressColumn('Percentage', format="%.1f%%", min_value=0, max_value=100)
                },
                hide_index=True,
                use_container_width=True
            )

        