"""
Utility functions and constants for the GPA Insight application
"""

import os

# Define the base directory for the application
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define paths for data files
COURSES_DATA_FILE = os.path.join(BASE_DIR, 'data', 'courses.json')
GRADES_DATA_FILE = os.path.join(BASE_DIR, 'data', 'grades.json')

# Define a constant for the minimum passing grade
MIN_PASSING_GRADE = 60

# Define a constant for the maximum number of credits
MAX_CREDITS = 21

# Define a constant for the GPA scale
GPA_SCALE = 4.0

# Define a constant for the default number of decimal places for GPA
GPA_DECIMALS = 2

# Define a constant for the application version
APP_VERSION = '1.0.0'

# Define a constant for the support email address
SUPPORT_EMAIL = 'support@gpainsightapp.com'

# Define a constant for the application name
APP_NAME = 'GPA Insight'

# Define a constant for the welcome message
WELCOME_MESSAGE = f'Welcome to {APP_NAME}, version {APP_VERSION}!'

# Print the welcome message
print(WELCOME_MESSAGE)