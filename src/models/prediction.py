import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from utils.constants import GRADE_POINTS

class GradePredictor:
    def __init__(self):
        self.model = None
        self.encoder = None
        self.is_trained = False

    def train(self, courses_df):
        """Train the prediction model on course data."""
        if len(courses_df) < 5:
            return False, None, None
        
        df = courses_df.copy()
        
        # Extract features
        df['Semester_Num'] = df['Semester'].str.extract(r'(\d{4})').astype(float)
        df['Subject'] = df['Course Code'].str.extract(r'([A-Z]{2,4})')[0]
        df['Course_Level'] = df['Course Code'].str.extract(r'[A-Z]+(\d)')[0].astype(float)
        
        # Encode subjects
        self.encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        subject_encoded = self.encoder.fit_transform(df[['Subject']])
        subject_cols = [f'Subject_{cat}' for cat in self.encoder.categories_[0]]
        subject_df = pd.DataFrame(subject_encoded, columns=subject_cols)
        
        # Prepare features
        features = pd.concat([
            df[['Credits', 'Semester_Num', 'Course_Level']].reset_index(drop=True),
            subject_df.reset_index(drop=True)
        ], axis=1)
        
        # Prepare target
        df['Grade_Points'] = df['Grade'].map(GRADE_POINTS)
        target = df['Grade_Points']
        
        # Impute missing values
        imputer = SimpleImputer(strategy="mean")
        X = imputer.fit_transform(features)
        y = target.values

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        self.is_trained = True
        
        # Calculate scores
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        return True, train_score, test_score

    def predict(self, semester, course_code, credits):
        """Predict grade for a new course."""
        if not self.is_trained:
            return None

        try:
            year = semester.split()[-1]
            if not year.isdigit() or len(year) != 4:
                raise ValueError("Invalid semester format")
            semester_num = float(year)
        except (ValueError, IndexError):
            return None

        subject = course_code[:3]
        try:
            course_level = float(course_code[3])
        except (ValueError, IndexError):
            course_level = 1.0

        # Prepare input
        input_data = pd.DataFrame({
            'Credits': [credits],
            'Semester_Num': [semester_num],
            'Course_Level': [course_level],
            'Subject': [subject]
        })

        # Encode subject
        subject_encoded = self.encoder.transform(input_data[['Subject']])
        subject_cols = [f'Subject_{cat}' for cat in self.encoder.categories_[0]]
        subject_df = pd.DataFrame(subject_encoded, columns=subject_cols)

        # Combine features
        features = pd.concat([
            input_data[['Credits', 'Semester_Num', 'Course_Level']].reset_index(drop=True),
            subject_df.reset_index(drop=True)
        ], axis=1)

        # Predict
        predicted_points = self.model.predict(features)[0]

        # Convert to letter grade
        grade_mapping = {v: k for k, v in GRADE_POINTS.items()}
        closest_point = min(GRADE_POINTS.values(), key=lambda x: abs(x - predicted_points))
        predicted_grade = [k for k, v in GRADE_POINTS.items() if v == closest_point][0]

        return predicted_grade, predicted_points

    def get_feature_importance(self):
        """Get feature importance from the trained model."""
        if not self.is_trained:
            return None
        
        feature_names = ['Credits', 'Semester_Num', 'Course_Level']
        subject_cols = [f'Subject_{cat}' for cat in self.encoder.categories_[0]]
        feature_names.extend(subject_cols)
        
        importances = self.model.feature_importances_
        
        # Ensure lengths match
        if len(feature_names) != len(importances):
            feature_names = feature_names[:len(importances)]
        
        return pd.DataFrame({
            'Feature': feature_names,
            'Importance': importances
        }).sort_values('Importance', ascending=False)