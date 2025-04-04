# UPES Student Dashboard

A comprehensive web application for tracking and analyzing student performance metrics, including attendance, assignments, and academic progress. Developed and maintained by Dymra Tech.

## System Overview

The UPES Student Dashboard is a sophisticated platform that provides real-time monitoring of student performance through:

### Analytics Module
- Advanced GPA calculation with weighted scoring system
- Detailed performance trend analysis with indicators
- Personalized recommendations based on multiple metrics
- Subject strength evaluation system

### Authentication System
- Secure student login with session management
- Password hashing using pbkdf2_sha256
- Role-based access control (Staff/Student)
- Modern UI with error handling

### Attendance Tracking
- Real-time attendance percentage calculation
- Pattern analysis for attendance behavior
- Multi-level alert system (Good/Warning/Critical)
- Predictive calculations for attendance targets

### Assignment Management
- Comprehensive assignment status tracking
- Priority-based deadline alert system
- Progress analytics with completion time estimation
- Success probability assessment

## Technical Architecture

### Core Technologies
- **Backend**: Python with advanced data processing
- **Data Processing**: Pandas for efficient analytics
- **Frontend**: Streamlit for responsive web interface
- **Storage**: CSV-based data management system

### Key Components
- Custom authentication system
- Real-time analytics engine
- Automated alert system
- Interactive data visualizations

## Deployment Guide

### Prerequisites
- Python 3.8 or higher
- Git for version control
- Adequate storage for student data

### Installation Steps
1. Clone the repository:
```bash
git clone <repository-url>
cd studentdashboard
```

2. Create and activate virtual environment (recommended):
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix/MacOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application
1. Start the server:
```bash
streamlit run app.py
```

2. Access the dashboard at `http://localhost:8501`

### Configuration
- Adjust `config.py` for custom settings
- Ensure proper file permissions for data directory
- Configure authentication parameters as needed

## System Architecture

```
├── analytics.py         # Advanced analytics engine
├── app.py              # Main application entry point
├── assignment_tracker.py # Assignment management system
├── attendance_tracker.py # Attendance monitoring system
├── student_auth.py      # Authentication and security
├── student_profile.py   # Profile management system
├── timetable.py         # Schedule management
├── assets/             # Static resources
│   └── UPES.png        # UI assets
├── data/               # Data storage
│   └── student_data.csv # Student records
└── requirements.txt    # Project dependencies
```

### Component Details
- **Analytics Engine**: Implements weighted GPA calculation and trend analysis
- **Authentication**: Handles secure user sessions and role-based access
- **Data Management**: Efficient CSV-based storage with Pandas integration
- **UI Components**: Modern, responsive interface with dark mode support

## Core Functionality

### Analytics System
- `calculate_gpa()`: Weighted GPA calculation with recent test emphasis
- `get_performance_trend()`: Advanced trend analysis with indicators
- `generate_recommendations()`: AI-driven personalized recommendations
- `calculate_subject_strength()`: Subject-wise performance analysis

### Attendance Management
- `analyze_attendance_pattern()`: Smart pattern recognition
- `generate_attendance_alert()`: Multi-level alert system
- `get_attendance_summary()`: Comprehensive attendance reports
- `predict_attendance_target()`: Target achievement calculations

### Assignment Tracking
- `get_assignment_status()`: Real-time completion tracking
- `get_assignment_analytics()`: Progress analysis with predictions
- `calculate_success_probability()`: Assignment success metrics
- `generate_deadline_alerts()`: Priority-based alert system

## Maintenance Guide

### Regular Maintenance
1. Database backup (weekly recommended)
2. Log rotation and cleanup
3. Performance monitoring
4. Security updates

### Development Workflow
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Performance Optimization
- Regular code profiling
- Database query optimization
- Cache implementation when needed
- Resource usage monitoring

## License

MIT License - Copyright (c) 2024 Dymra Tech