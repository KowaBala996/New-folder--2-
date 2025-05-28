import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
        /* Main theme colors */
        :root {
            --primary-color: #4A90E2;
            --primary-dark: #357ABD;
            --primary-light: #6BA4E7;
            --secondary-color: #F5F7FA;
            --text-color: #2C3E50;
            --text-secondary: #666666;
            --text-muted: #888888;
            --text-light: #FFFFFF;
            --accent-color: #E8F0FE;
            --success-color: #4CAF50;
            --warning-color: #FFC107;
            --error-color: #F44336;
            --input-bg: #2C3E50;
            --input-text: #FFFFFF;
            --button-color: #4A90E2;  
            --button-hover: #5A52D5;  
        }

        /* Global styles */
        .stApp {
            background-color: #FFFFFF;
            color: var(--text-color);
        }

        /* Text styles */
        p, li, span {
            color: var(--text-color);
        }

        .text-primary { color: var(--primary-color); }
        .text-secondary { color: var(--text-secondary); }
        .text-muted { color: var(--text-muted); }
        .text-light { color: var(--text-light); }
        .text-success { color: var(--success-color); }
        .text-warning { color: var(--warning-color); }
        .text-error { color: var(--error-color); }

        
        .main-header {
            font-size: 42px;
            color: var(--primary-color);
            text-align: center;
            margin-bottom: 20px;
            font-weight: 600;
        }

        .section-header {
            font-size: 26px;
            color: var(--text-color);
            margin-top: 30px;
            margin-bottom: 10px;
            font-weight: 500;
        }

        /* Containers */
        .dashboard-container {
            background-color: var(--secondary-color);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        .metric-container {
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            text-align: center;
            border: 1px solid #E0E0E0;
        }

        .metric-value {
            font-size: 36px;
            font-weight: bold;
            color: var(--primary-color);
        }

        .metric-label {
            font-size: 14px;
            color: var(--text-secondary);
        }

        /* Form elements */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stNumberInput > div > div > input {
            background-color: var(--input-bg);
            color: var(--input-text) !important;
            border: 1px solid #E0E0E0;
            border-radius: 4px;
            padding: 8px 12px;
        }

        /* Buttons */
        .stButton > button {
            background-color: var(--button-color) !important;
            color: #F0F0F0 !important;  /* Changed to light gray text */
            border: none !important;
            border-radius: 4px !important;
            padding: 8px 16px !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            text-transform: none !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
            transition: all 0.3s ease !important;
        }

        /* Form submit button specific styling */
        .stFormSubmitButton > button {
            background: linear-gradient(45deg, #2196F3, #00BCD4) !important;  /* Gradient blue */
            color: white !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 8px 16px !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            text-transform: none !important;
            box-shadow: 0 2px 4px rgba(33, 150, 243, 0.2) !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            position: relative !important;
            overflow: hidden !important;
        }

        .stFormSubmitButton > button:hover {
            background: linear-gradient(45deg, #1976D2, #0097A7) !important;  /* Darker gradient */
            box-shadow: 0 6px 12px rgba(33, 150, 243, 0.4) !important;
            transform: translateY(-2px) scale(1.02) !important;
        }

        .stFormSubmitButton > button:active {
            background: linear-gradient(45deg, #1565C0, #00838F) !important;  /* Even darker gradient */
            transform: translateY(1px) scale(0.98) !important;
            box-shadow: 0 2px 4px rgba(33, 150, 243, 0.3) !important;
            transition: all 0.1s ease !important;
        }

        .stFormSubmitButton > button::after {
            content: '' !important;
            position: absolute !important;
            top: 50% !important;
            left: 50% !important;
            width: 5px !important;
            height: 5px !important;
            background: rgba(255, 255, 255, 0.7) !important;  /* Brighter ripple */
            opacity: 0 !important;
            border-radius: 100% !important;
            transform: scale(1, 1) translate(-50%) !important;
            transform-origin: 50% 50% !important;
        }

        .stFormSubmitButton > button:hover::after {
            animation: ripple 1s ease-out !important;
        }

        @keyframes ripple {
            0% {
                transform: scale(0, 0) !important;
                opacity: 0.7 !important;  /* More visible ripple */
            }
            100% {
                transform: scale(20, 20) !important;
                opacity: 0 !important;
            }
        }

        .stButton > button:hover {
            background-color: var(--button-hover) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
            color: #FFFFFF !important;  /* Changed to white text on hover */
        }

        /* Success/Error messages */
        .stSuccess {
            background-color: #E8F5E9;
            border-left: 4px solid var(--success-color);
            padding: 10px;
            border-radius: 4px;
            color: var(--success-color);
        }

        .stError {
            background-color: #FFEBEE;
            border-left: 4px solid var(--error-color);
            padding: 10px;
            border-radius: 4px;
            color: var(--error-color);
        }

        .stInfo {
            background-color: var(--accent-color);
            border-left: 4px solid var(--primary-color);
            padding: 10px;
            border-radius: 4px;
            color: var(--primary-color);
        }

        /* Prediction Section Styling */
        .prediction-container {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
            border-radius: 12px !important;
            padding: 25px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
            margin: 20px 0 !important;
            border: 1px solid rgba(33, 150, 243, 0.1) !important;
        }

        .prediction-header {
            color: #1976D2 !important;
            font-size: 24px !important;
            font-weight: 600 !important;
            margin-bottom: 25px !important;
            text-align: center !important;
            text-transform: none !important;
        }

        .prediction-subheader {
            color: #424242 !important;
            font-size: 18px !important;
            font-weight: 500 !important;
            margin: 15px 0 !important;
            text-transform: none !important;
        }

        /* Prediction Form Elements */
        .prediction-container .stSelectbox > div > div > select,
        .prediction-container .stTextInput > div > div > input {
            background-color: white !important;
            border: 2px solid #E0E0E0 !important;
            border-radius: 8px !important;
            padding: 10px 15px !important;
            font-size: 16px !important;
            transition: all 0.3s ease !important;
        }

        .prediction-container .stSelectbox > div > div > select:hover,
        .prediction-container .stTextInput > div > div > input:hover {
            border-color: #2196F3 !important;
            box-shadow: 0 2px 8px rgba(33, 150, 243, 0.1) !important;
        }

        .prediction-container .stSelectbox > div > div > select:focus,
        .prediction-container .stTextInput > div > div > input:focus {
            border-color: #1976D2 !important;
            box-shadow: 0 2px 12px rgba(33, 150, 243, 0.2) !important;
        }

        /* Prediction Result Styling */
        .prediction-result {
            background: linear-gradient(45deg, #E3F2FD, #BBDEFB) !important;
            border-radius: 8px !important;
            padding: 20px !important;
            margin-top: 20px !important;
            text-align: center !important;
            border: 1px solid rgba(33, 150, 243, 0.2) !important;
        }

        .prediction-result h3 {
            color: #1976D2 !important;
            font-size: 20px !important;
            margin-bottom: 10px !important;
        }

        .prediction-result p {
            color: #424242 !important;
            font-size: 16px !important;
            margin: 5px 0 !important;
        }

        /* Model Performance Styling */
        .model-performance {
            background: linear-gradient(135deg, #ffffff 0%, #f0f7ff 100%) !important;
            border-radius: 16px !important;
            padding: 30px !important;
            margin: 25px 0 !important;
            box-shadow: 0 8px 20px rgba(33, 150, 243, 0.1) !important;
            border: 1px solid rgba(33, 150, 243, 0.2) !important;
        }

        .model-performance-header {
            color: #1565C0 !important;
            font-size: 28px !important;
            font-weight: 600 !important;
            margin-bottom: 25px !important;
            text-align: center !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
        }

        .model-metrics {
            display: flex !important;
            justify-content: space-around !important;
            flex-wrap: wrap !important;
            gap: 25px !important;
            margin: 25px 0 !important;
        }

        .metric-card {
            background: linear-gradient(145deg, #ffffff, #f8f9fa) !important;
            border-radius: 12px !important;
            padding: 20px 25px !important;
            min-width: 220px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
            border: 1px solid rgba(33, 150, 243, 0.15) !important;
            text-align: center !important;
            transition: transform 0.3s ease, box-shadow 0.3s ease !important;
        }

        .metric-card:hover {
            transform: translateY(-5px) !important;
            box-shadow: 0 8px 25px rgba(33, 150, 243, 0.15) !important;
        }

        .metric-value {
            font-size: 32px !important;
            font-weight: 700 !important;
            margin: 15px 0 !important;
            background: linear-gradient(45deg, #1976D2, #2196F3) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
        }

        .metric-value.positive {
            background: linear-gradient(45deg, #2E7D32, #4CAF50) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
        }

        .metric-value.negative {
            background: linear-gradient(45deg, #C62828, #F44336) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
        }

        .metric-label {
            color: #424242 !important;
            font-size: 16px !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            font-weight: 500 !important;
        }

        .model-warning {
            background: linear-gradient(145deg, #FFF3E0, #FFE0B2) !important;
            border-left: 4px solid #FF9800 !important;
            padding: 20px !important;
            margin: 25px 0 !important;
            border-radius: 8px !important;
            color: #E65100 !important;
            box-shadow: 0 4px 15px rgba(255, 152, 0, 0.1) !important;
        }

        .model-success {
            background: linear-gradient(145deg, #E8F5E9, #C8E6C9) !important;
            border-left: 4px solid #4CAF50 !important;
            padding: 20px !important;
            margin: 25px 0 !important;
            border-radius: 8px !important;
            color: #2E7D32 !important;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.1) !important;
        }

        /* Feature Importance Section */
        .feature-importance-section {
            background: linear-gradient(145deg, #ffffff, #f8f9fa) !important;
            border-radius: 12px !important;
            padding: 25px !important;
            margin: 20px 0 !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
        }

        .feature-explanation {
            background: linear-gradient(145deg, #E3F2FD, #BBDEFB) !important;
            border-radius: 10px !important;
            padding: 20px !important;
            margin: 15px 0 !important;
            border: 1px solid rgba(33, 150, 243, 0.2) !important;
        }

        .feature-explanation h5 {
            color: #1565C0 !important;
            font-size: 18px !important;
            font-weight: 600 !important;
            margin-bottom: 15px !important;
            display: block !important;
        }

        .feature-explanation p {
            color: #424242 !important;
            font-size: 15px !important;
            line-height: 1.6 !important;
            margin-bottom: 15px !important;
            display: block !important;
        }

        .feature-explanation ul {
            color: #424242 !important;
            font-size: 15px !important;
            line-height: 1.6 !important;
            margin-left: 20px !important;
            margin-bottom: 15px !important;
            display: block !important;
        }

        .feature-explanation li {
            color: #424242 !important;
            font-size: 15px !important;
            line-height: 1.6 !important;
            margin-bottom: 10px !important;
            display: list-item !important;
        }

        .feature-explanation strong {
            color: #1976D2 !important;
            font-weight: 600 !important;
            display: inline !important;
        }

        /* Fix for Streamlit's markdown rendering */
        .stMarkdown {
            display: block !important;
        }

        .stMarkdown p {
            display: block !important;
            margin-bottom: 1em !important;
        }

        .stMarkdown ul {
            display: block !important;
            margin-left: 2em !important;
            margin-bottom: 1em !important;
        }

        .stMarkdown li {
            display: list-item !important;
            margin-bottom: 0.5em !important;
        }

        /* Additional fixes for HTML rendering */
        .stMarkdown h5 {
            display: block !important;
            font-size: 1.17em !important;
            margin-top: 1em !important;
            margin-bottom: 1em !important;
            font-weight: bold !important;
        }

        .stMarkdown strong {
            display: inline !important;
            font-weight: bold !important;
        }

        .stMarkdown div {
            display: block !important;
        }
    </style>
    """, unsafe_allow_html=True)