import streamlit as st
import pandas as pd
try:
    import plotly.express as px
except ImportError:
    st.error("Error: Plotly is not installed. Please install it using: pip install plotly")
    st.stop()
from datetime import datetime
import numpy as np

from styles.custom_css import apply_custom_css
from utils.constants import GRADE_POINTS, DIFFICULTY_LEVELS, SUBJECTS, STUDY_TIPS
from utils.helpers import calculate_gpa, add_course, delete_course, recommend_study_time, simulate_gpa
from models.prediction import GradePredictor
from components.dashboard import render_dashboard
from components.course_management import render_manage_courses

def save_courses_data(courses_df):
    """Save courses data to Streamlit's session state."""
    try:
        # Convert DataFrame to CSV string
        csv_data = courses_df.to_csv(index=False)
        # Store in session state
        st.session_state.courses_data = csv_data
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

def load_courses_data():
    """Load courses data from Streamlit's session state."""
    try:
        if 'courses_data' in st.session_state:
            # Load from session state
            return pd.read_csv(pd.StringIO(st.session_state.courses_data))
        return pd.DataFrame(columns=['Semester', 'Course Code', 'Course Name', 'Credits', 'Grade', 'Timestamp'])
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(columns=['Semester', 'Course Code', 'Course Name', 'Credits', 'Grade', 'Timestamp'])

def initialize_session_state():
    """Initialize session state variables."""
    if 'courses' not in st.session_state:
        st.session_state.courses = load_courses_data()
    
    if 'predictor' not in st.session_state:
        st.session_state.predictor = GradePredictor()

def render_grade_prediction():
    """Render the grade prediction tab."""
    st.markdown('<h2 class="section-header">AI Grade Prediction</h2>', unsafe_allow_html=True)
    
    if len(st.session_state.courses) < 5:
        st.warning("You need at least 5 courses in your record to use the grade prediction feature.")
        return
    
    # Train the model
    if not st.session_state.predictor.is_trained:
        if st.button("Train Prediction Model", type="primary"):
            with st.spinner("Training model..."):
                success, train_score, test_score = st.session_state.predictor.train(st.session_state.courses)
                if success:
                    st.success("Model trained successfully!")
                    st.markdown(f"""
                    <div style="background-color: var(--accent-color); padding: 15px; border-radius: 8px; margin: 10px 0;">
                        <h4 style="color: var(--primary-color); margin-bottom: 10px;">Model Performance</h4>
                        <p style="margin: 5px 0;">Training accuracy: <strong>{train_score:.2f}</strong></p>
                        <p style="margin: 5px 0;">Testing accuracy: <strong>{test_score:.2f}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.success("Your prediction model is ready!")
        
        # Form for grade prediction
        with st.form("predict_grade_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                latest_semester = "Semester 1.1"  
                if not st.session_state.courses.empty:
                    semesters = st.session_state.courses['Semester'].unique().tolist()
                    latest_semester = semesters[-1]
                
                pred_semester = st.selectbox(
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
                pred_course_code = st.text_input("Course Code", placeholder="CS301", help="Enter the course code (e.g., CS301)")
            
            with col2:
                pred_credits = st.number_input("Credits", min_value=1, max_value=6, value=3, help="Select the number of credits for the course")
            
            predict_button = st.form_submit_button("Predict Grade", type="primary")
            
            if predict_button:
                if pred_semester and pred_course_code:
                    with st.spinner("Predicting grade..."):
                        result = st.session_state.predictor.predict(pred_semester, pred_course_code, pred_credits)
                        
                        if result is not None:
                            predicted_grade, predicted_points = result
                            
                            grade_color = "#4CAF50" if predicted_points >= 3.0 else "#FFC107" if predicted_points >= 2.0 else "#F44336"
                            
                            st.markdown(f"""
                            <div style="background-color: var(--accent-color); padding: 20px; border-radius: 10px; border-left: 5px solid {grade_color}; margin-top: 20px;">
                                <h3 style="color: var(--text-color); margin-bottom: 15px;">Predicted Grade</h3>
                                <p style="color: var(--text-secondary);">Based on your academic history, our AI predicts you will likely earn a grade of:</p>
                                <h2 style="color: {grade_color}; text-align: center; font-size: 36px; margin: 20px 0;">{predicted_grade}</h2>
                                <p style="text-align: center; color: var(--text-secondary);">({predicted_points:.2f} points)</p>
                                <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solidrgb(96, 91, 91);">
                                    <p style="color: var(--text-muted); font-size: 0.9em;">
                                        <strong>Note:</strong> This prediction is based on your past performance, course difficulty, and other factors.
                                    </p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error("Prediction failed. Please check your input and try again.")
                else:
                    st.error("Please fill in all required fields.")
        
        # Display feature importance
        st.markdown("---")
        st.markdown("### Grade Influencing Factors")
        
        if st.checkbox("Show what factors influence your grades the most", value=False):
            feature_importance = st.session_state.predictor.get_feature_importance()
            if feature_importance is not None:
                # Create a more visually appealing chart
                fig = px.bar(feature_importance.head(10), 
                            x='Importance', 
                            y='Feature', 
                            orientation='h',
                            title='Top Factors Influencing Your Grades',
                            color='Importance',
                            color_continuous_scale=px.colors.sequential.Blues)
                
                fig.update_layout(
                    yaxis={'categoryorder': 'total ascending'},
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=20, r=20, t=40, b=20),
                    xaxis_title="Influence Score (0-1)",
                    yaxis_title="Factors",
                    title_x=0.5,
                    title_font_size=20
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Feature Importance Section
                st.markdown("#### Understanding the Graph")
                st.markdown("""
                - Higher bars indicate stronger influence on your grades
                - Scores range from 0 (no influence) to 1 (strong influence)
                - Focus on improving factors with higher scores
                """)
            
                st.markdown("#### Key Factors")
                st.markdown("""
                - **Study Time:** Weekly study hours
                - **Previous Grades:** Academic history
                - **Attendance:** Class participation
                - **Course Difficulty:** Course complexity
                """)

def render_study_optimizer():
    """Render the study optimizer tab."""
    st.markdown('<h2 class="section-header">Study Time Optimizer</h2>', unsafe_allow_html=True)
    st.write("Plan your study time effectively to achieve your target grades")
    
    with st.form("study_optimizer_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            course_name = st.text_input("Course Name", placeholder="Data Structures", key="opt_course_name")
        
        with col2:
            difficulty = st.selectbox("Course Difficulty", list(DIFFICULTY_LEVELS.keys()), key="opt_difficulty")
            credits = st.number_input("Course Credits", min_value=1, max_value=6, value=3, key="opt_credits")
        
        with col3:
            target_grade = st.selectbox("Target Grade", list(GRADE_POINTS.keys()), key="opt_target")
        
        optimize_button = st.form_submit_button("Get Study Plan", type="primary")
        
        if optimize_button:
            if course_name:
                recommended_hours = recommend_study_time(difficulty, credits, target_grade)
                
                st.markdown(f"""
                <div style="background-color: #f0f7ff; padding: 20px; border-radius: 10px; border-left: 5px solid #1E88E5;">
                    <h3 style="color: #0D47A1;">Recommended Study Plan for {course_name}</h3>
                    <p>To achieve a target grade of <b>{target_grade}</b> in this {difficulty.lower()} {credits}-credit course, you should study:</p>
                    <h2 style="color: #1E88E5; text-align: center;">{recommended_hours} hours/week</h2>
                    <p>This recommendation is based on:</p>
                    <ul>
                        <li>Course difficulty level: {difficulty}</li>
                        <li>Number of credits: {credits}</li>
                        <li>Your target grade: {target_grade}</li>
                    </ul>
                    <p><small>Note: This is a general guideline. Adjust based on your learning style and the specific demands of the course.</small></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Weekly schedule visualization
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<b>Suggested Weekly Schedule</b>", unsafe_allow_html=True)
                
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                daily_hours = [round(recommended_hours / 5, 1) if i < 5 else 0 for i in range(7)]
                
                schedule_df = pd.DataFrame({
                    'Day': days,
                    'Study Hours': daily_hours
                })
                
                fig = px.bar(schedule_df, x='Day', y='Study Hours', 
                             title=f'Suggested Weekly Study Schedule for {course_name}',
                             color='Study Hours',
                             color_continuous_scale=px.colors.sequential.Blues)
                
                fig.update_layout(xaxis_title='Day of Week',
                                 yaxis_title='Hours of Study',
                                 plot_bgcolor='rgba(0,0,0,0)')
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Please enter a course name.")
    
    # Study tips section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<b>Study Strategy Recommendations</b>", unsafe_allow_html=True)
    
    selected_subject = st.selectbox("Select subject area for targeted study tips:", SUBJECTS)
    
    if selected_subject in STUDY_TIPS:
        st.markdown("<div style='background-color: #f5f5f5; padding: 15px; border-radius: 10px;'>", unsafe_allow_html=True)
        st.markdown(f"<h4>Top 5 Study Strategies for {selected_subject}</h4>", unsafe_allow_html=True)
        for i, tip in enumerate(STUDY_TIPS[selected_subject], 1):
            st.markdown(f"{i}. {tip}")
        st.markdown("</div>", unsafe_allow_html=True)

def render_what_if_analysis():
    """Render the what-if analysis tab."""
    st.markdown('<h2 class="section-header">What-If Scenario Analysis</h2>', unsafe_allow_html=True)
    st.write("Explore how changes to your grades would affect your overall GPA")
    
    if st.session_state.courses.empty:
        st.info("Add some courses to use the What-If Analysis feature.")
        return
    
    # Display current GPA
    current_gpa = calculate_gpa(st.session_state.courses)
    st.markdown(f"<b>Your current GPA: {current_gpa:.2f}</b>", unsafe_allow_html=True)
    
    # Create a DataFrame for scenario planning
    scenario_df = st.session_state.courses.copy()
    
    # Let the user select courses to modify
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<b>Modify Grades to See GPA Impact</b>", unsafe_allow_html=True)
    
    # Store the modified grades
    modified_grades = {}
    
    # Display courses for modification
    for index, row in scenario_df.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.write(f"{row['Course Code']}: {row['Course Name']} ({row['Semester']})")
        
        with col2:
            st.write(f"Current grade: {row['Grade']}")
        
        with col3:
            new_grade = st.selectbox(f"New grade", 
                                   list(GRADE_POINTS.keys()), 
                                   index=list(GRADE_POINTS.keys()).index(row['Grade']),
                                   key=f"what_if_{index}")
            
            if new_grade != row['Grade']:
                modified_grades[index] = new_grade
    
    # Calculate the new GPA
    if modified_grades:
        new_gpa = simulate_gpa(scenario_df, modified_grades)
        gpa_change = new_gpa - current_gpa
        
        # Display the result
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="background-color: {'#e8f5e9' if gpa_change >= 0 else '#ffebee'}; padding: 15px; border-radius: 10px; text-align: center;">
                <h3>New Projected GPA</h3>
                <h2 style="color: {'#2e7d32' if gpa_change >= 0 else '#c62828'};">{new_gpa:.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background-color: {'#e8f5e9' if gpa_change >= 0 else '#ffebee'}; padding: 15px; border-radius: 10px; text-align: center;">
                <h3>GPA Change</h3>
                <h2 style="color: {'#2e7d32' if gpa_change >= 0 else '#c62828'};">{'+' if gpa_change > 0 else ''}{gpa_change:.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Create a before/after visualization
        gpa_comparison = pd.DataFrame({
            'Scenario': ['Current GPA', 'Projected GPA'],
            'GPA': [current_gpa, new_gpa]
        })
        
        fig = px.bar(gpa_comparison, x='Scenario', y='GPA',
                     color='Scenario',
                     color_discrete_map={
                         'Current GPA': '#1E88E5',
                         'Projected GPA': '#2e7d32' if gpa_change >= 0 else '#c62828'
                     },
                     text='GPA',
                     title='GPA Comparison')
        
        fig.update_layout(yaxis_range=[0, 4.0],
                         plot_bgcolor='rgba(0,0,0,0)')
        
        fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Provide insights based on the changes
        st.markdown("<b>Analysis:</b>", unsafe_allow_html=True)
        
        if gpa_change > 0.2:
            st.markdown("✅ This scenario would **significantly improve** your GPA.")
        elif gpa_change > 0:
            st.markdown("✅ This scenario would lead to a **modest improvement** in your GPA.")
        elif gpa_change < -0.2:
            st.markdown("⚠️ This scenario would **significantly decrease** your GPA.")
        elif gpa_change < 0:
            st.markdown("⚠️ This scenario would lead to a **slight decrease** in your GPA.")
        else:
            st.markdown("ℹ️ This scenario would result in **no change** to your GPA.")
        
        # Goal-setting feature
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<b>GPA Goal Setting</b>", unsafe_allow_html=True)
        
        target_gpa = st.slider("What's your target GPA?", min_value=0.0, max_value=4.0, value=3.5, step=0.1)
        
        if target_gpa > current_gpa:
            gap = target_gpa - current_gpa
            remaining_credits = 30  # Assumption for future credits
            
            # Calculate required GPA for future courses
            current_points = current_gpa * st.session_state.courses['Credits'].sum()
            target_points = target_gpa * (st.session_state.courses['Credits'].sum() + remaining_credits)
            needed_points = target_points - current_points
            required_future_gpa = needed_points / remaining_credits
            
            if required_future_gpa <= 4.0:
                st.markdown(f"""
                <div style="background-color: #e8f5e9; padding: 15px; border-radius: 10px;">
                    <h4>To reach your target GPA of {target_gpa:.1f}:</h4>
                    <p>You'll need to maintain a <b>{required_future_gpa:.2f}</b> GPA in your next {remaining_credits} credits.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Interpret the difficulty
                if required_future_gpa > 3.7:
                    st.write("This will be challenging and will require mostly A grades.")
                elif required_future_gpa > 3.3:
                    st.write("This is achievable with a mix of A and B+ grades.")
                elif required_future_gpa > 3.0:
                    st.write("This is realistic with solid B+ performance.")
                else:
                    st.write("This is very achievable with your current performance level.")
            else:
                st.markdown(f"""
                <div style="background-color: #ffebee; padding: 15px; border-radius: 10px;">
                    <h4>Target GPA Analysis:</h4>
                    <p>Your target GPA of {target_gpa:.1f} is mathematically impossible to achieve with only {remaining_credits} remaining credits.</p>
                    <p>Consider setting a more realistic goal or planning for additional coursework.</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background-color: #e8f5e9; padding: 15px; border-radius: 10px;">
                <h4>Good news!</h4>
                <p>Your current GPA of {current_gpa:.2f} already meets or exceeds your target of {target_gpa:.1f}.</p>
                <p>Focus on maintaining your performance in future courses.</p>
            </div>
            """, unsafe_allow_html=True)

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
                if save_courses_data(st.session_state.courses):
                    st.success(f"Added {course_name} to your courses!")
                else:
                    st.error("Course added but failed to save data.")
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
                    if save_courses_data(st.session_state.courses):
                        st.success("Course deleted successfully!")
                        st.rerun()
                    else:
                        st.error("Course deleted but failed to save data.")
            
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
                        if save_courses_data(st.session_state.courses):
                            st.success("Courses imported successfully!")
                            st.rerun()
                        else:
                            st.error("Courses imported but failed to save data.")
                else:
                    st.error("The uploaded CSV does not have the required columns.")
            except Exception as e:
                st.error(f"Error importing courses: {e}")

def main():
    """Main application entry point."""
    st.set_page_config(page_title="GPA Insight", page_icon="📚", layout="wide")
    
    # Apply custom CSS
    apply_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Main header
    st.markdown('<h1 class="main-header">📚 GPA Insight</h1>', unsafe_allow_html=True)
    st.markdown("Academic performance tracker and GPA optimizer")
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Dashboard", "Manage Courses", "Grade Prediction", "Study Optimizer", "What-If Analysis"])
    
    # Render each tab
    with tab1:
        render_dashboard()
    
    with tab2:
        render_manage_courses()
    
    with tab3:
        render_grade_prediction()
    
    with tab4:
        render_study_optimizer()
    
    with tab5:
        render_what_if_analysis()

if __name__ == "__main__":
    main()