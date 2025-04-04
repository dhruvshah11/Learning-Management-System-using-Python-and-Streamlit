import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

def generate_timetable_data():
    # Sample data for demonstration
    subjects = [
        'Data Structures', 'Algorithms', 'Database Systems', 'Computer Networks',
        'Operating Systems', 'Software Engineering', 'Web Development', 'Machine Learning'
    ]
    venues = ['Room 101', 'Room 102', 'Room 103', 'Lab 201', 'Lab 202', 'Lecture Hall 301']
    professors = [
        'Dr. Sharma', 'Dr. Patel', 'Prof. Singh', 'Dr. Kumar',
        'Prof. Gupta', 'Dr. Verma', 'Prof. Reddy', 'Dr. Malhotra'
    ]
    time_slots = [
        '09:00 AM - 10:30 AM', '10:45 AM - 12:15 PM', '01:00 PM - 02:30 PM',
        '02:45 PM - 04:15 PM', '04:30 PM - 06:00 PM'
    ]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    timetable = []
    used_slots = set()
    
    # Generate random timetable ensuring no clashes
    for day in days:
        for _ in range(4):  # 4 lectures per day
            while True:
                subject = random.choice(subjects)
                time_slot = random.choice(time_slots)
                venue = random.choice(venues)
                professor = random.choice(professors)
                
                slot_key = f"{day}-{time_slot}"
                if slot_key not in used_slots:
                    used_slots.add(slot_key)
                    timetable.append({
                        'Day': day,
                        'Time': time_slot,
                        'Subject': subject,
                        'Venue': venue,
                        'Professor': professor
                    })
                    break
    
    return pd.DataFrame(timetable)

# Global CSS styles for consistent theming
def get_theme_styles():
    return """
    <style>
        .timetable-container, .schedule-card {
            background-color: #2d2d2d;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            margin-bottom: 0.5rem;
        }
        .day-header {
            background-color: #4a9eff;
            color: white;
            padding: 0.5rem;
            border-radius: 5px;
            margin-bottom: 0.5rem;
            text-align: center;
        }
        .class-card, .schedule-card {
            background-color: #1a1a1a;
            color: #e0e0e0;
            padding: 0.5rem;
            border-radius: 5px;
            margin-bottom: 0.5rem;
            border-left: 4px solid #4a9eff;
        }
        .time-text {
            color: #4a9eff;
            font-weight: 600;
            font-size: 1.1rem;
        }
        .subject-text {
            color: #e0e0e0;
            font-size: 1rem;
            margin-top: 0.2rem;
        }
        h2.section-title {
            color: #1f4d7a;
            text-align: center;
            margin-bottom: 1.5rem;
        }
    </style>
    """

def display_timetable():
    # Apply global styles
    st.markdown(get_theme_styles(), unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>📅 Weekly Timetable</h2>", unsafe_allow_html=True)
    
    # Initialize or load timetable data
    if 'timetable_data' not in st.session_state:
        st.session_state.timetable_data = generate_timetable_data()
    
    # View options
    view_type = st.radio(
        "Select View",
        ["Weekly View", "Daily View"],
        horizontal=True
    )
    
    df = st.session_state.timetable_data
    
    if view_type == "Weekly View":
        
        for day in df['Day'].unique():
            st.markdown(f"<div class='day-header'>{day}</div>", unsafe_allow_html=True)
            day_schedule = df[df['Day'] == day].sort_values(by='Time')
            
            for _, row in day_schedule.iterrows():
                st.markdown(f"""
                <div class='class-card'>
                    <strong>{row['Time']}</strong><br>
                    📚 {row['Subject']}<br>
                    👨‍🏫 {row['Professor']}<br>
                    🏛️ {row['Venue']}
                </div>
                """, unsafe_allow_html=True)
    else:
        # Daily view
        selected_day = st.selectbox("Select Day", df['Day'].unique())
        day_schedule = df[df['Day'] == selected_day].sort_values('Time')
        
        # Create a more detailed daily view
        st.markdown(f"""<div style='text-align: center; padding: 1rem;'>
            <h3 style='color: #1f4d7a;'>{selected_day}'s Schedule</h3>
        </div>""", unsafe_allow_html=True)
        
        for _, row in day_schedule.iterrows():
            st.markdown(f"""
            <div style='background-color: #2d2d2d; padding: 1rem; border-radius: 10px; 
                        box-shadow: 0 2px 4px rgba(0,0,0,0.2); margin-bottom: 1rem;'>
                <h4 style='color: #4a9eff; margin: 0;'>{row['Time']}</h4>
                <div style='margin-top: 0.5rem;'>
                    <p style='margin: 0.2rem 0;'><strong>Subject:</strong> {row['Subject']}</p>
                    <p style='margin: 0.2rem 0;'><strong>Professor:</strong> {row['Professor']}</p>
                    <p style='margin: 0.2rem 0;'><strong>Venue:</strong> {row['Venue']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

def add_timetable_to_dashboard():
    # Apply global styles
    st.markdown(get_theme_styles(), unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>📅 Today's Schedule</h2>", unsafe_allow_html=True)
    
    try:
        # Initialize timetable data if not exists
        if 'timetable_data' not in st.session_state:
            st.session_state.timetable_data = generate_timetable_data()
        
        df = st.session_state.timetable_data
        # Get current day's schedule
        current_day = datetime.now().strftime('%A')
        today_schedule = df[df['Day'] == current_day].sort_values(by='Time')
        
        # Add error handling for empty schedule
        if today_schedule.empty:
            st.info("No classes scheduled for today!")
            return
        
        for _, row in today_schedule.iterrows():
            st.markdown(f"""
            <div class='schedule-card'>
                <div class='time-text'>{row['Time']}</div>
                <div class='subject-text'>{row['Subject']}
                    <div style='color: #6c757d; font-size: 0.9rem;'>{row['Professor']} | {row['Venue']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f'Error loading timetable data: {str(e)}')
        return
    
    # CSS styles are now managed by get_theme_styles()