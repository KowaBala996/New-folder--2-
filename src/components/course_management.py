import streamlit as st
import pandas as pd
from datetime import datetime
from utils.helpers import add_course, delete_course
from utils.constants import GRADE_POINTS

def render_manage_courses():
    """Render the manage courses tab."""
    st.markdown('<h2 class="section-header">Manage Your Courses</h2>', unsafe_allow_html=True)
    
    # Form to add new courses
    with st.form("add_course_form"):
        st.markdown("Add a New Course")
        col1, col2 = st.columns(2)
        
        with col1:
            semester = st.selectbox(
                "Semester",
                options=[
                    "Semester 1.1", "Semester 1.2",
                    "Semester 2.1", "Semester 2.2",
                    "Semester 3.1", "Semester 3.2",
                    "Semester 4.1", "Semester 4.2",
                    "Semester 5.1", "Semester 5.2",
                    "Semester 6.1", "Semester 6.2"
                ],
                help="Select the semester for this course"
            )
            course_name = st.text_input("Course Name", placeholder="Introduction to Computer Science")
            grade = st.selectbox("Grade", list(GRADE_POINTS.keys()))
        
        with col2:
            course_code = st.text_input("Course Code", placeholder="CS101")
            credits = st.number_input("Credits", min_value=1, max_value=6, value=3)
        
        submit_button = st.form_submit_button("Add Course")
        
        if submit_button:
            if semester and course_code and course_name:
                st.session_state.courses = add_course(st.session_state.courses, semester, course_code, course_name, credits, grade)
                st.success(f"Added {course_name} to your courses!")
            else:
                st.error("Please fill in all required fields.")
    
    # Display and edit existing courses
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<b>Your Courses</b>", unsafe_allow_html=True)
    
    if st.session_state.courses.empty:
        st.info("No courses added yet. Use the form above to add your first course.")
    else:
        for index, row in st.session_state.courses.iterrows():
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            
            with col1:
                st.write(f"**{row['Course Code']}**: {row['Course Name']}")
            
            with col2:
                st.write(f"Semester: {row['Semester']}")
            
            with col3:
                st.write(f"Credits: {row['Credits']}")
                st.write(f"Grade: {row['Grade']}")
            
            with col4:
                if st.button("Delete", key=f"delete_{index}"):
                    st.session_state.courses = delete_course(st.session_state.courses, index)
                    st.success("Course deleted successfully!")
                    st.rerun()
            
            st.markdown("---")
        
        # Export functionality
        st.download_button(
            label="Export Course Data (CSV)",
            data=st.session_state.courses.to_csv(index=False).encode('utf-8'),
            file_name="my_courses.csv",
            mime="text/csv",
        )
        
        # Import functionality
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<b>Import Courses</b>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload a CSV file with your courses", type="csv")
        
        if uploaded_file is not None:
            try:
                imported_courses = pd.read_csv(uploaded_file)
                required_columns = ['Semester', 'Course Code', 'Course Name', 'Credits', 'Grade']
                
                if all(col in imported_courses.columns for col in required_columns):
                    if st.button("Confirm Import"):
                        if 'Timestamp' not in imported_courses.columns:
                            imported_courses['Timestamp'] = datetime.now()
                        
                        st.session_state.courses = pd.concat([st.session_state.courses, imported_courses], ignore_index=True)
                        st.success("Courses imported successfully!")
                        st.rerun()
                else:
                    st.error("The uploaded CSV does not have the required columns.")
            except Exception as e:
                st.error(f"Error importing courses: {e}") 