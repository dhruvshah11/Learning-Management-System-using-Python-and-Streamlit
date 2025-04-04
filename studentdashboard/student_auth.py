import streamlit as st
import pandas as pd
from passlib.hash import pbkdf2_sha256
from analytics import calculate_subject_strength, generate_recommendations

def init_student_auth():
    if 'student_authenticated' not in st.session_state:
        st.session_state.student_authenticated = False
    if 'student_id' not in st.session_state:
        st.session_state.student_id = None

def student_login_page():
    st.image('assets/UPES.png', width=200)
    st.title('🎓 UPES Student Login')
    
    # Custom CSS for modern login form with error styling
    st.markdown("""
    <style>
        .login-form { background-color: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .form-header { color: #1f4d7a; font-size: 1.5rem; font-weight: 600; margin-bottom: 1.5rem; }
        .stButton>button { background-color: #1f4d7a; color: white; font-weight: 500; }
        .stButton>button:hover { background-color: #173d61; }
        .help-text { color: #666; font-size: 0.9rem; margin-top: 0.5rem; }
        .error-text { color: #dc3545; font-size: 0.9rem; margin-top: 0.5rem; }
        .input-error { border-color: #dc3545 !important; }
        .stButton>button:disabled { background-color: #ccc; cursor: not-allowed; }
    </style>
    """, unsafe_allow_html=True)
    
    with st.form('student_login_form', clear_on_submit=True):
        st.markdown('<p class="form-header">Welcome Back! 👋</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            student_id = st.text_input('Student ID', placeholder='Enter your 6-digit Student ID', max_chars=6)
            st.markdown('<p class="help-text">Your 6-digit student identification number</p>', unsafe_allow_html=True)
        with col2:
            password = st.text_input('Password', type='password', placeholder='Enter your Student ID as password')
            st.markdown('<p class="help-text">Use your Student ID as password</p>', unsafe_allow_html=True)
        
        col3, col4 = st.columns([3, 1])
        with col3:
            remember_me = st.checkbox('Keep me signed in')
        
        submit = st.form_submit_button('Sign In', use_container_width=True)
        
        if submit:
            if not student_id or not password:
                st.error('🚫 Please fill in both Student ID and Password')
                return
            
            if not student_id.isdigit() or len(student_id) != 6:
                st.error('🚫 Student ID must be a 6-digit number')
                return
                
            try:
                # Load student data
                df = pd.read_csv('data/student_data.csv')
                student_id_int = int(student_id)
                student = df[df['student_id'] == student_id_int]
                
                if len(student) > 0:
                    if password == student_id:
                        st.session_state.student_authenticated = True
                        st.session_state.student_id = student_id_int
                        st.session_state.student_name = student.iloc[0]['name']
                        if remember_me:
                            st.session_state.remember_student = True
                        st.success('🎉 Login successful! Welcome, ' + student.iloc[0]['name'])
                        st.rerun()
                    else:
                        st.error('🔒 Incorrect password. Please use your Student ID as password')
                else:
                    st.error('❌ Student ID not found. Please check your ID')
            except Exception as e:
                st.error('⚠️ An error occurred. Please try again later')
                
    # Help links with improved styling
    st.markdown("""
    <div style='display: flex; justify-content: space-between; margin-top: 1rem;'>
        <a href='#' style='color: #1f4d7a; text-decoration: none;'>🔑 Forgot Password?</a>
        <a href='#' style='color: #1f4d7a; text-decoration: none;'>📝 New Student? Register</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Login instructions
    with st.expander('ℹ️ Login Help'):
        st.markdown("""
        **How to Login:**
        1. Enter your 6-digit Student ID
        2. Enter your password (same as your Student ID for demo)
        3. Click 'Sign In'
        
        **Need Help?**
        - Contact IT Support: support@upes.ac.in
        - Visit Student Help Desk: Room 101, Admin Block
        """)

def get_student_data(student_id):
    df = pd.read_csv('data/student_data.csv')
    return df[df['student_id'] == student_id].iloc[0] if len(df[df['student_id'] == student_id]) > 0 else None

def student_dashboard():
    # Import plotly for interactive charts
    import plotly.express as px
    
    # Theme toggle
    theme = st.sidebar.selectbox('🎨 Theme', ['Light', 'Dark'])
    if theme == 'Dark':
        st.markdown("""
        <style>
            .main { background-color: #1a1a1a; color: #ffffff; }
            .metric-card { background-color: #2d2d2d !important; color: #ffffff !important; border: 1px solid #3d3d3d !important; }
            .section-title { color: #ffffff !important; }
            h1, h2, h3, p { color: #ffffff !important; }
            .stSelectbox { background-color: #2d2d2d; color: #ffffff; }
            div[data-testid="stPlotlyChart"] { background-color: #2d2d2d !important; border-radius: 10px; padding: 1rem; }
            div[data-testid="stPlotlyChart"] .main-svg { background-color: #2d2d2d !important; }
            div[data-testid="stPlotlyChart"] .gridlayer path { stroke: #3d3d3d !important; }
            div[data-testid="stPlotlyChart"] .xy text { fill: #ffffff !important; }
            div[data-testid="stPlotlyChart"] .legendtext { fill: #ffffff !important; }
        </style>
        """, unsafe_allow_html=True)
    
    student_data = get_student_data(st.session_state.student_id)
    if student_data is None:
        st.error('Student data not found')
        return
    
    # Display student information with personalized greeting
    greeting = 'Good morning' if pd.Timestamp.now().hour < 12 else 'Good afternoon' if pd.Timestamp.now().hour < 17 else 'Good evening'
    st.title(f'{greeting}, {student_data["name"]}! 👋')
    
    # Custom CSS for modern UI
    st.markdown("""
    <style>
        .metric-card { background-color: white; padding: 1rem; border-radius: 10px;
                      box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 1rem; }
        .section-title { color: #1f4d7a; font-size: 1.5rem; font-weight: 600; margin: 1.5rem 0; }
        .info-text { color: #666; font-size: 1rem; }
    </style>
    """, unsafe_allow_html=True)

    # Basic Information with enhanced styling
    st.markdown("<h2 class='section-title'>📋 Basic Information</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #1f4d7a; margin: 0;'>Student ID</h3>
            <p style='font-size: 1.5rem; margin: 0.5rem 0;'>{student_data['student_id']}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #1f4d7a; margin: 0;'>Course</h3>
            <p style='font-size: 1.5rem; margin: 0.5rem 0;'>{student_data['course']}</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #1f4d7a; margin: 0;'>Semester</h3>
            <p style='font-size: 1.5rem; margin: 0.5rem 0;'>Semester {student_data['semester']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Academic Performance with modern cards
    st.markdown("<h2 class='section-title'>📈 Academic Performance</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #1f4d7a; margin: 0;'>GPA</h3>
            <p style='font-size: 2rem; margin: 0.5rem 0;'>{student_data['gpa']:.2f}<span style='font-size: 1rem;'>/4.0</span></p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #1f4d7a; margin: 0;'>Attendance</h3>
            <p style='font-size: 2rem; margin: 0.5rem 0;'>{student_data['attendance_percentage']}%</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #1f4d7a; margin: 0;'>Assignments</h3>
            <p style='font-size: 2rem; margin: 0.5rem 0;'>{student_data['assignments_completed']}/15</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Test Scores with interactive chart
    st.markdown("<h2 class='section-title'>📝 Test Scores</h2>", unsafe_allow_html=True)
    scores_df = pd.DataFrame({
        'Test': ['Test 1', 'Test 2', 'Test 3'],
        'Score': [student_data['test1_score'], student_data['test2_score'], student_data['test3_score']]
    })
    fig = px.line(scores_df, x='Test', y='Score', markers=True)
    if theme == 'Dark':
        fig.update_layout(
            plot_bgcolor='#2d2d2d',
            paper_bgcolor='#2d2d2d',
            font={'color': '#ffffff'},
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#3d3d3d'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#3d3d3d')
        )
    else:
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': '#2c3e50'},
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        )
    fig.update_traces(line_color='#1f4d7a', marker=dict(size=10, color='#1f4d7a'))
    st.plotly_chart(fig, use_container_width=True)
    
    # Additional Information with modern cards
    st.markdown("<h2 class='section-title'>🎯 Additional Information</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #1f4d7a; margin: 0;'>Specialization</h3>
            <p style='font-size: 1.2rem; margin: 0.5rem 0;'>{student_data['specialization']}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #1f4d7a; margin: 0;'>Club/Activity</h3>
            <p style='font-size: 1.2rem; margin: 0.5rem 0;'>{student_data['extracurricular_activities']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance Insights and Recommendations
    st.markdown("<h2 class='section-title'>💡 Performance Insights</h2>", unsafe_allow_html=True)
    test_scores = [student_data['test1_score'], student_data['test2_score'], student_data['test3_score']]
    subject_strength = calculate_subject_strength(test_scores)
    recommendations = generate_recommendations(student_data['attendance_percentage'], student_data['assignments_completed'], test_scores)
    
    # Display subject strength
    st.markdown(f"""
    <div class='metric-card'>
        <h3 style='color: #1f4d7a; margin: 0;'>Subject Mastery Level</h3>
        <p style='font-size: 1.5rem; margin: 0.5rem 0;'>{subject_strength}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display personalized recommendations
    st.markdown("<h3 style='color: #1f4d7a; margin: 1rem 0;'>📌 Personalized Recommendations</h3>", unsafe_allow_html=True)
    for rec in recommendations:
        st.markdown(f"""
        <div style='background-color: white; padding: 1rem; border-radius: 8px; 
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 0.5rem;'>
            <p style='color: #2c3e50; margin: 0;'>{rec}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Import and add timetable
    from timetable import add_timetable_to_dashboard, display_timetable
    
    # Add today's schedule to dashboard
    add_timetable_to_dashboard()
    
    # Add tab for full timetable view
    if st.button('View Full Timetable'):
        display_timetable()

def student_logout():
    st.session_state.student_authenticated = False
    st.session_state.student_id = None
    st.rerun()