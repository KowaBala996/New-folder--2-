import pandas as pd
from datetime import datetime
from .constants import GRADE_POINTS

def calculate_gpa(courses_df):
    """Calculate GPA from a DataFrame of courses."""
    if courses_df.empty:
        return 0.0
    
    # Create a copy to avoid the SettingWithCopyWarning
    df = courses_df.copy()
    
    # Map grades to points
    df['Points'] = df['Grade'].map(GRADE_POINTS)
    
    # Calculate weighted points (points * credits)
    df['Weighted Points'] = df['Points'] * df['Credits']
    
    # Calculate GPA
    total_weighted_points = df['Weighted Points'].sum()
    total_credits = df['Credits'].sum()
    
    if total_credits == 0:
        return 0.0
    else:
        return total_weighted_points / total_credits

def add_course(courses_df, semester, code, name, credits, grade):
    """Add a new course to the DataFrame."""
    new_course = pd.DataFrame({
        'Semester': [semester],
        'Course Code': [code],
        'Course Name': [name],
        'Credits': [credits],
        'Grade': [grade],
        'Timestamp': [datetime.now()]
    })
    
    return pd.concat([courses_df, new_course], ignore_index=True)

def delete_course(courses_df, index):
    """Delete a course from the DataFrame."""
    return courses_df.drop(index).reset_index(drop=True)

def recommend_study_time(difficulty, credits, target_grade):
    """Calculate recommended study time based on course parameters."""
    base_hours = 2
    
    difficulty_multiplier = {
        'Easy': 0.8,
        'Moderate': 1.0,
        'Challenging': 1.3,
        'Very Difficult': 1.6
    }
    
    grade_multiplier = {
        'A+': 1.4, 'A': 1.3, 'A-': 1.2,
        'B+': 1.1, 'B': 1.0, 'B-': 0.9,
        'C+': 0.8, 'C': 0.7, 'C-': 0.6,
        'D+': 0.5, 'D': 0.4, 'D-': 0.3
    }
    
    recommended_hours = base_hours * credits * difficulty_multiplier.get(difficulty, 1.0) * grade_multiplier.get(target_grade, 1.0)
    
    return round(recommended_hours, 1)

def simulate_gpa(courses_df, modified_courses):
    """Simulate GPA with modified grades."""
    df = courses_df.copy()
    
    for index, new_grade in modified_courses.items():
        df.at[index, 'Grade'] = new_grade
    
    return calculate_gpa(df) 