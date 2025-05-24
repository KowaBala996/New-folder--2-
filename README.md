# GPA Insight

academic performance tracker and GPA optimizer built with Streamlit.

## Features

- 📊 Interactive Dashboard: Track your GPA, credits, and course performance
- 📝 Course Management: Add, edit, and delete courses with import/export functionality
- 🤖 AI Grade Prediction: Get grade predictions for future courses based on your academic history
- ⏰ Study Time Optimizer: Get personalized study time recommendations
- 📈 What-If Analysis: Explore how changes to your grades would affect your GPA

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/gpa-insight.git
cd gpa-insight
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run src/app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Start using the application:
   - Add your courses in the "Manage Courses" tab
   - View your academic dashboard
   - Get grade predictions for future courses
   - Optimize your study time
   - Analyze different grade scenarios

## Project Structure

```
gpa-insight/
├── src/
│   ├── components/
│   ├── models/
│   │   └── prediction.py
│   ├── styles/
│   │   └── custom_css.py
│   ├── utils/
│   │   ├── constants.py
│   │   └── helpers.py
│   └── app.py
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 