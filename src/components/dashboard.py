import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import calculate_gpa
from utils.constants import GRADE_POINTS
from PIL import Image
import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

def render_dashboard():
    """Render the dashboard tab."""
    # Add a welcome banner
    st.markdown("""
        <div style='text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin-bottom: 20px;'>
            <h1 style='color: #1f77b4;'>Academic Dashboard</h1>
            <p style='color: #666;'>Track your academic progress and performance</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.courses.empty:
        st.info("Add some courses to see your academic dashboard!")
        return
    
    # Calculate overall GPA
    overall_gpa = calculate_gpa(st.session_state.courses)
    
    # Display key metrics with icons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style='text-align: center; padding: 20px; background-color: #ffffff; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
                <h3 style='color: #1f77b4;'>📊 Overall GPA</h3>
                <h2 style='color: #2c3e50;'>{:.2f}</h2>
            </div>
        """.format(overall_gpa), unsafe_allow_html=True)
    
    with col2:
        total_credits = st.session_state.courses['Credits'].sum()
        st.markdown("""
            <div style='text-align: center; padding: 20px; background-color: #ffffff; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
                <h3 style='color: #1f77b4;'>📚 Total Credits</h3>
                <h2 style='color: #2c3e50;'>{}</h2>
            </div>
        """.format(total_credits), unsafe_allow_html=True)
    
    with col3:
        total_courses = len(st.session_state.courses)
        st.markdown("""
            <div style='text-align: center; padding: 20px; background-color: #ffffff; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
                <h3 style='color: #1f77b4;'>📝 Total Courses</h3>
                <h2 style='color: #2c3e50;'>{}</h2>
            </div>
        """.format(total_courses), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # GPA Trend Chart
    st.markdown('<h3 class="section-header">GPA Trend</h3>', unsafe_allow_html=True)
    
    semester_groups = st.session_state.courses.groupby('Semester')
    semester_gpas = []
    
    for sem, group in semester_groups:
        sem_gpa = calculate_gpa(group)
        semester_gpas.append({'Semester': sem, 'GPA': sem_gpa})
    
    semester_gpa_df = pd.DataFrame(semester_gpas)
    
    if not semester_gpa_df.empty:
        fig = px.line(semester_gpa_df, x='Semester', y='GPA', 
                      markers=True, line_shape='linear',
                      labels={'GPA': 'GPA', 'Semester': 'Semester'},
                      title='GPA Trend by Semester')
        
        fig.update_layout(xaxis_title='Semester',
                         yaxis_title='GPA',
                         yaxis_range=[0, 4.0],
                         plot_bgcolor='rgba(0,0,0,0)')
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Grade Distribution
    st.markdown('<h3 class="section-header">Grade Distribution</h3>', unsafe_allow_html=True)
    
    grade_counts = st.session_state.courses['Grade'].value_counts().reset_index()
    grade_counts.columns = ['Grade', 'Count']
    
    grade_order = sorted(grade_counts['Grade'], key=lambda x: GRADE_POINTS.get(x, 0), reverse=True)
    grade_counts['Grade'] = pd.Categorical(grade_counts['Grade'], categories=grade_order, ordered=True)
    grade_counts = grade_counts.sort_values('Grade')
    
    fig = px.bar(grade_counts, x='Grade', y='Count',
                 labels={'Count': 'Number of Courses', 'Grade': 'Grade'},
                 color='Grade',
                 color_discrete_sequence=px.colors.qualitative.Set1,
                 title='Distribution of Grades')
    
    fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': grade_order},
                     plot_bgcolor='rgba(0,0,0,0)')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Course Performance Table
    st.markdown('<h3 class="section-header">Course Performance</h3>', unsafe_allow_html=True)
    
    course_df = st.session_state.courses[['Semester', 'Course Code', 'Course Name', 'Credits', 'Grade']]
    course_df['GPA Impact'] = course_df['Credits'] * course_df['Grade'].map(GRADE_POINTS)
    
    st.dataframe(course_df.sort_values('GPA Impact', ascending=False), use_container_width=True,
                column_config={
                    "GPA Impact": st.column_config.NumberColumn(
                        "GPA Impact",
                        help="The weighted impact of this course on your GPA",
                        format="%.2f",
                    ),
                }) 