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

        tab1, tab2, tab3 = st.tabs(["Overall Comparison", "Subject Analysis", "Grade Distribution"])

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

        with tab3:
            # Create a radar chart for grades
            categories = ['Overall Grade', 'Communication', 'Technical Knowledge',
                          'Problem Solving', 'Team Work', 'Time Management']

            # --- Calculate values_sem1 dynamically ---
            values_sem1 = [sem1_data.get('SGPA', 0)]
            subject_count_sem1 = 0
            for key in sem1_data:
                if key.startswith('INT_') and subject_count_sem1 < 5:
                    subject_code = key[4:]
                    internal = sem1_data.get(key, 0)
                    external = sem1_data.get(f'EXT_{subject_code}', 0)
                    total = internal + external
                    percentage = (total / 100) * 100 if total <= 100 else 100
                    scaled_percentage = (percentage / 100) * 10
                    values_sem1.append(round(scaled_percentage, 1))
                    subject_count_sem1 += 1
            # Pad with 0s if less than 5 subjects are found
            while len(values_sem1) < 6:
                values_sem1.append(0)

            values_sem2 = [sem2_data.get('SGPA', 0)]
            subject_count_sem2 = 0
            for key in sem2_data:
                if key.startswith('INT_') and subject_count_sem2 < 5:
                    subject_code = key[4:]
                    internal = sem2_data.get(key, 0)
                    external = sem2_data.get(f'EXT_{subject_code}', 0)
                    total = internal + external
                    percentage = (total / 100) * 100 if total <= 100 else 100
                    scaled_percentage = (percentage / 100) * 10
                    values_sem2.append(round(scaled_percentage, 1))
                    subject_count_sem2 += 1
            while len(values_sem2) < 6:
                values_sem2.append(0)

            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                r=values_sem1,
                theta=categories,
                fill='toself',
                name='Semester 1',
                line_color='#3366cc'
            ))

            fig.add_trace(go.Scatterpolar(
                r=values_sem2,
                theta=categories,
                fill='toself',
                name='Semester 2',
                line_color='#ff9900'
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10]
                    )),
                showlegend=True,
                title="Skill Assessment Radar",
                height=450
            )

            st.plotly_chart(fig, use_container_width=True)

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

    #    # Progress over time - Line chart showing improvement trends
    #     st.subheader("Academic Progress")

    #     # Create a mock dataframe with monthly performance
    #     months = ["Jan 2022", "Feb 2022", "Mar 2022", "Apr 2022", "May 2022", "Jun 2022"]

    #     # Create a simulated performance curve based on the two semester data points
    #     start_point = sem1_data.get('Percentage', 80)
    #     end_point = sem2_data.get('Percentage', 80)

    #     # Create a simple curve with some variation
    #     performance = []
    #     for i, month in enumerate(months):
    #         # Linear interpolation with some random variation
    #         progress = start_point + (end_point - start_point) * (i / (len(months) - 1))
    #         # Add some random noise (-2 to +2)
    #         noise = np.random.uniform(-2, 2)
    #         performance.append(max(0, min(100, progress + noise)))

    #     # Create attendance data (simulated)
    #     attendance = [95, 92, 88, 91, 93, 90]

    #     # Create the dataframe
    #     progress_df = pd.DataFrame({
    #         'Month': months,
    #         'Performance': performance,
    #         'Attendance': attendance
    #     })

    #     st.dataframe(progress_df)
    #     # Plot with dual Y-axis
    #     fig = go.Figure()

    #     fig.add_trace(go.Scatter(
    #         x=progress_df['Month'],
    #         y=progress_df['Performance'],
    #         name='Academic Performance',
    #         mode='lines+markers',
    #         marker=dict(size=10, color='#3366cc'),
    #         line=dict(width=3, color='#3366cc')
    #     ))

    #     fig.add_trace(go.Scatter(
    #         x=progress_df['Month'],
    #         y=progress_df['Attendance'],
    #         name='Attendance %',
    #         mode='lines+markers',
    #         marker=dict(size=10, color='#ff9900'),
    #         line=dict(width=3, color='#ff9900'),
    #         yaxis='y2'
    #     ))

    #     fig.update_layout(
    #         title='Performance & Attendance Trends',
    #         xaxis=dict(title='Month'),
    #         yaxis=dict(
    #             title='Performance (%)',
    #             range=[70, 100],
    #             titlefont=dict(color='#3366cc'),
    #             tickfont=dict(color='#3366cc')
    #         ),
    #         yaxis2=dict(
    #             title='Attendance (%)',
    #             range=[70, 100],
    #             titlefont=dict(color='#ff9900'),
    #             tickfont=dict(color='#ff9900'),
    #             anchor='x',
    #             overlaying='y',
    #             side='right'
    #         ),
    #         legend=dict(x=0.01, y=0.99),
    #         height=400
    #     )

    #     st.plotly_chart(fig, use_container_width=True)

    #     # Student Rank & Percentile (simulated)
    #     st.subheader("Class Ranking")

    #     col1, col2, col3 = st.columns(3)

    #     with col1:
    #         with st.container(border=True):
    #             # Simulated rank gauge
    #             rank = 5  # Simulated rank
    #             total_students = 60  # Simulated total

    #             fig = go.Figure(go.Indicator(
    #                 mode="gauge+number",
    #                 value=rank,
    #                 title={'text': "Class Rank"},
    #                 gauge={
    #                     'axis': {'range': [None, total_students], 'tickwidth': 1, 'tickcolor': "darkblue"},
    #                     'bar': {'color': "#3366cc"},
    #                     'bgcolor': "white",
    #                     'borderwidth': 2,
    #                     'bordercolor': "gray",
    #                     'steps': [
    #                         {'range': [0, total_students / 3], 'color': '#d4f1dd'},
    #                         {'range': [total_students / 3, 2 * total_students / 3], 'color': '#e7fcef'},
    #                         {'range': [2 * total_students / 3, total_students], 'color': '#f5f5f5'}
    #                     ],
    #                     'threshold': {
    #                         'line': {'color': "red", 'width': 4},
    #                         'thickness': 0.75,
    #                         'value': rank
    #                     }
    #                 }
    #             ))

    #             fig.update_layout(height=250)
    #             st.plotly_chart(fig, use_container_width=True)

    #     with col2:
    #         with st.container(border=True):
    #             # Percentile gauge
    #             percentile = 95  # Simulated percentile

    #             fig = go.Figure(go.Indicator(
    #                 mode="gauge+number",
    #                 value=percentile,
    #                 title={'text': "Percentile"},
    #                 gauge={
    #                     'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
    #                     'bar': {'color': "#ff9900"},
    #                     'bgcolor': "white",
    #                     'borderwidth': 2,
    #                     'bordercolor': "gray",
    #                     'steps': [
    #                         {'range': [0, 33], 'color': '#fff8e6'},
    #                         {'range': [33, 66], 'color': '#ffefbf'},
    #                         {'range': [66, 100], 'color': '#ffe599'}
    #                     ],
    #                     'threshold': {
    #                         'line': {'color': "green", 'width': 4},
    #                         'thickness': 0.75,
    #                         'value': percentile
    #                     }
    #                 }
    #             ))

    #             fig.update_layout(height=250)
    #             st.plotly_chart(fig, use_container_width=True)

    #     with col3:
    #         with st.container(border=True):
    #             # CGPA/GPA gauge
    #             cgpa = overall_sgpa  # Use calculated overall SGPA

    #             fig = go.Figure(go.Indicator(
    #                 mode="gauge+number",
    #                 value=cgpa,
    #                 title={'text': "CGPA"},
    #                 number={'suffix': "/10"},
    #                 gauge={
    #                     'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
    #                     'bar': {'color': "#4bc0c0"},
    #                     'bgcolor': "white",
    #                     'borderwidth': 2,
    #                     'bordercolor': "gray",
    #                     'steps': [
    #                         {'range': [0, 4], 'color': '#e6f5f5'},
    #                         {'range': [4, 7], 'color': '#ccebeb'},
    #                         {'range': [7, 10], 'color': '#b3e0e0'}
    #                     ],
    #                     'threshold': {
    #                         'line': {'color': "green", 'width': 4},
    #                         'thickness': 0.75,
    #                         'value': cgpa
    #                     }
    #                 }
    #             ))

    #             fig.update_layout(height=250)
    #             st.plotly_chart(fig, use_container_width=True)

    #     # Recommendations section
    #     st.subheader("Recommendations & Feedback")

    #     # Find weakest and strongest subjects from both semesters
    #     all_subjects = {}

    #     for key in sem1_data:
    #         if key.startswith('INT_'):
    #             subject_code = key[4:]
    #             internal = sem1_data.get(key, 0)
    #             external = sem1_data.get(f'EXT_{subject_code}', 0)
    #             total = internal + external
    #             all_subjects[subject_code] = {'total': total, 'name': get_subject_name(subject_code)}

    #     for key in sem2_data:
    #         if key.startswith('INT_'):
    #             subject_code = key[4:]
    #             internal = sem2_data.get(key, 0)
    #             external = sem2_data.get(f'EXT_{subject_code}', 0)
    #             total = internal + external
    #             all_subjects[subject_code] = {'total': total, 'name': get_subject_name(subject_code)}

    #     # Find min and max
    #     min_subject = min(all_subjects.items(), key=lambda x: x[1]['total'])
    #     max_subject = max(all_subjects.items(), key=lambda x: x[1]['total'])

    #     col1, col2 = st.columns(2)

    #     with col1:
    #         with st.container(border=True):
    #             st.markdown("### Areas of Strength")
    #             st.write(f"🌟 Your strongest subject is **{max_subject[1]['name']}** with a score of **{max_subject[1]['total']}**.")
    #             # Example - You might need more robust logic to determine these recommendations based on actual subject codes and names.
    #             strongest_subject_name = max_subject[1]['name']
    #             if "Business Communication" in strongest_subject_name:
    #                 st.write("💪 You demonstrate excellent understanding in Business Communication.")
    #             st.write("👍 Your time management skills are reflected in consistent performance.")  # Generic recommendation

    #     with col2:
    #         with st.container(border=True):
    #             st.markdown("### Areas for Improvement")
    #             st.write(f"📝 You may want to focus more on **{min_subject[1]['name']}** where your score is **{min_subject[1]['total']}**.")
    #             weakest_subject_name = min_subject[1]['name']
    #             if "Business Mathematics" in weakest_subject_name:
    #                 st.write("💡 Consider joining study groups for collaborative learning in Business Mathematics.")
    #             st.write("📚 Set aside additional practice time for problem-solving subjects.")  # Generic recommendation

    #     # Downloadable Report section
    #     st.subheader("Download Report")

    #     report_name = f"Student_Academic_Report_{student_id}_{datetime.now().strftime('%Y%m%d')}.xlsx"

    #     col1, col2 = st.columns([3, 1])

    #     with col1:
    #         st.write("Generate a comprehensive Excel report with all your academic details including subject-wise breakdown, semester comparisons, and performance analytics.")

    #     with col2:
    #         if st.button("Generate Report", key="report_button"):
    #             # Prepare data for Excel report
    #             excel_data = BytesIO()
    #             writer = pd.ExcelWriter(excel_data, engine='xlsxwriter')

    #             # Semester 1 Dataframe
    #             sem1_df = pd.DataFrame([sem1_data])  # Make it a list to be DataFrame
    #             sem1_df.to_excel(writer, sheet_name='Semester 1 Overview', index=False)

    #             # Semester 2 Dataframe
    #             sem2_df = pd.DataFrame([sem2_data])  # Make it a list to be DataFrame
    #             sem2_df.to_excel(writer, sheet_name='Semester 2 Overview', index=False)

    #             # Subject-wise performance for Sem 1 and 2 (using existing subject_df from tabs)
    #             subject_df_sem1_report = pd.DataFrame(columns=['Subject', 'Code', 'Internal', 'External', 'Total', 'Percentage'])
    #             for key in sem1_data:
    #                 if key.startswith('INT_'):
    #                     subject_code = key[4:]
    #                     subject_name = get_subject_name(subject_code)
    #                     internal = sem1_data.get(key, 0)
    #                     external = sem1_data.get(f'EXT_{subject_code}', 0)
    #                     total = internal + external
    #                     percentage = (total / 100) * 100
    #                     subject_df_sem1_report = pd.concat([subject_df_sem1_report, pd.DataFrame([{'Subject': subject_name, 'Code': subject_code, 'Internal': internal, 'External': external, 'Total': total, 'Percentage': percentage}])], ignore_index=True)
    #             subject_df_sem1_report.to_excel(writer, sheet_name='Sem 1 Subjects', index=False)

    #             subject_df_sem2_report = pd.DataFrame(columns=['Subject', 'Code', 'Internal', 'External', 'Total', 'Percentage'])
    #             for key in sem2_data:
    #                 if key.startswith('INT_'):
    #                     subject_code = key[4:]
    #                     subject_name = get_subject_name(subject_code)
    #                     internal = sem2_data.get(key, 0)
    #                     external = sem2_data.get(f'EXT_{subject_code}', 0)
    #                     total = internal + external
    #                     percentage = (total / 100) * 100
    #                     subject_df_sem2_report = pd.concat([subject_df_sem2_report, pd.DataFrame([{'Subject': subject_name, 'Code': subject_code, 'Internal': internal, 'External': external, 'Total': total, 'Percentage': percentage}])], ignore_index=True)
    #             subject_df_sem2_report.to_excel(writer, sheet_name='Sem 2 Subjects', index=False)

    #             writer.close()
    #             excel_data.seek(0)

    #             st.download_button(
    #                 label="Download Excel Report",
    #                 data=excel_data,
    #                 file_name=report_name,
    #                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    #             )
    #         else:
    #             st.warning("Dashboard content is not available because data for both semesters is required for full display.")

    #     # Footer
    #     st.markdown('<div class="footer">© 2025 University Management System</div>', unsafe_allow_html=True)