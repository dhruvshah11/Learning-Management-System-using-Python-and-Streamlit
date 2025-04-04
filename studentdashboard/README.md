# Student Dashboard

A comprehensive web application for tracking and analyzing student performance metrics, including attendance, assignments, and academic progress.

## Features

- **Analytics Module**: Track GPA, performance trends, and receive personalized recommendations
- **Attendance Tracking**: Monitor attendance patterns with real-time alerts
- **Assignment Management**: Track completion status and receive deadline alerts

## Tech Stack

- Python
- Pandas for data processing
- Streamlit for web interface
- CSV for data storage

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Start the application:
```bash
streamlit run app.py
```

The dashboard will be available at `http://localhost:8501`

## Project Structure

```
├── analytics.py         # Analytics calculations and recommendations
├── app.py              # Main Streamlit application
├── assignment_tracker.py # Assignment management functions
├── attendance_tracker.py # Attendance tracking functions
├── data/               # Data storage directory
│   └── student_data.csv # Student records
├── requirements.txt    # Project dependencies
└── student_profile.py  # Student profile management
```

## Functions

### Analytics
- `calculate_gpa()`: Calculate GPA from test scores
- `get_performance_trend()`: Analyze performance trends
- `generate_recommendations()`: Get personalized recommendations

### Attendance
- `analyze_attendance_pattern()`: Track attendance patterns
- `generate_attendance_alert()`: Get attendance alerts
- `get_attendance_summary()`: Generate attendance reports

### Assignments
- `get_assignment_status()`: Track assignment completion
- `get_assignment_analytics()`: Get assignment progress analytics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License