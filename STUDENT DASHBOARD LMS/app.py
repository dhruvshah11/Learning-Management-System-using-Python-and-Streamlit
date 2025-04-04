import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from passlib.hash import pbkdf2_sha256
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'student_authenticated' not in st.session_state:
    st.session_state.student_authenticated = False
if 'student_id' not in st.session_state:
    st.session_state.student_id = None

# Configure Streamlit page with UPES branding
st.set_page_config(
    page_title="UPES Student Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Global Styles */
    .main {background-color: #1a1a1a}
    .block-container {padding-top: 2rem}
    
    /* Typography */
    h1 {color: #4a9eff; font-size: 2.5rem; font-weight: 700; margin-bottom: 2rem}
    h2 {color: #e0e0e0; font-size: 1.8rem; font-weight: 600; margin: 1.5rem 0}
    p {color: #d0d0d0}
    
    /* Metrics and Cards */
    .stMetric {background-color: #2d2d2d; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); transition: transform 0.2s}
    .stMetric:hover {transform: translateY(-2px); box-shadow: 0 6px 8px rgba(0,0,0,0.3)}
    .stMetric label {font-size: 1rem; color: #b0b0b0; font-weight: 500}
    .stMetric [data-testid="stMetricValue"] {font-size: 1.8rem; font-weight: 700; color: #4a9eff}
    
    /* Buttons and Interactive Elements */
    .stButton>button {background-color: #4a9eff; color: white; border-radius: 8px; padding: 0.5rem 1.5rem; font-weight: 500; border: none; transition: all 0.2s}
    .stButton>button:hover {background-color: #357abd; transform: translateY(-1px)}
    .stProgress .st-bo {background-color: #4a9eff; border-radius: 10px}
    
    /* Inputs and Selects */
    .stTextInput>div>div {border-radius: 8px; background-color: #2d2d2d; color: #e0e0e0}
    .stSelectbox>div>div {border-radius: 8px; background-color: #2d2d2d; color: #e0e0e0}
    
    /* Charts and Data Display */
    [data-testid="stDataFrame"] {border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); background-color: black; color: #e0e0e0}
    .js-plotly-plot {border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); background-color: black}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None

# Import student authentication
from student_auth import init_student_auth, student_login_page, student_dashboard, student_logout

# Initialize student authentication
init_student_auth()

# Sample user credentials (in production, use a secure database)
USERS = {
    'admin@upes.ac.in': pbkdf2_sha256.hash('admin123'),
    'teacher@upes.ac.in': pbkdf2_sha256.hash('teacher123')
}

def load_data():
    return pd.read_csv('data/student_data.csv')

def calculate_statistics(df):
    stats = {
        'total_students': len(df),
        'avg_attendance': df['attendance_percentage'].mean(),
        'avg_gpa': df['gpa'].mean(),
        'top_performers': len(df[df['gpa'] >= 3.7]),
        'active_clubs': df['extracurricular_activities'].nunique()
    }
    return stats

def login_page():
    st.image('assets/UPES.png', width=200)
    st.title('🎓 UPES Dashboard')
    
    # User type selection
    user_type = st.radio('Select User Type', ['Staff', 'Student'])
    
    if user_type == 'Staff':
        with st.form('staff_login_form'):
            email = st.text_input('Email')
            password = st.text_input('Password', type='password')
            submit = st.form_submit_button('Login')
            
            if submit:
                if email in USERS and pbkdf2_sha256.verify(password, USERS[email]):
                    st.session_state.authenticated = True
                    st.session_state.user_type = 'staff'
                    st.rerun()
                else:
                    st.error('Invalid credentials')
    else:
        student_login_page()

def main_dashboard():
    # Check if student is logged in
    if st.session_state.get('student_authenticated', False):
        student_dashboard()
        if st.sidebar.button('Logout'):
            student_logout()
        return
    
    # Staff dashboard
    st.sidebar.markdown("<h2 style='color: #1f4d7a; margin-bottom: 1.5rem;'>🎓 Navigation</h2>", unsafe_allow_html=True)
    page = st.sidebar.radio("", ["Overview", "Performance Analytics", "Student Details"])
    
    if st.sidebar.button('Logout'):
        st.session_state.authenticated = False
        st.session_state.user_type = None
        st.rerun()
    
    # Load and process data
    df = load_data()
    stats = calculate_statistics(df)
    
    if page == "Overview":
        st.markdown("<h1 style='text-align: center;'>📊 UPES Student Performance Analytics</h1>", unsafe_allow_html=True)
        
        # Top metrics row with enhanced styling
        st.markdown("<h2 style='color: #2c3e50; margin: 2rem 0 1rem;'>📈 Key Metrics</h2>", unsafe_allow_html=True)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric('Total Students', f"{stats['total_students']:,}")
        with col2:
            st.metric('Average Attendance', f"{stats['avg_attendance']:.1f}%", delta=f"{stats['avg_attendance']-75:.1f}%" if stats['avg_attendance'] > 75 else None)
        with col3:
            st.metric('Average GPA', f"{stats['avg_gpa']:.2f}", delta=f"{stats['avg_gpa']-3.0:.2f}" if stats['avg_gpa'] > 3.0 else None)
        with col4:
            st.metric('Top Performers', stats['top_performers'], delta=f"{(stats['top_performers']/stats['total_students']*100):.1f}%")
        with col5:
            st.metric('Active Clubs', stats['active_clubs'])
    
    elif page == "Performance Analytics":
        st.markdown("<h1 style='text-align: center;'>📈 Performance Analytics</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            # GPA Distribution with enhanced styling
            gpa_fig = go.Figure(data=[go.Histogram(x=df['gpa'], nbinsx=20, marker_color='#4a9eff')])
            gpa_fig.update_layout(
                title={'text': 'GPA Distribution', 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
                plot_bgcolor='black',
                paper_bgcolor='black',
                font={'color': '#e0e0e0'},
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#333333', title='GPA', color='#e0e0e0'),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#333333', title='Count', color='#e0e0e0')
            )
            st.plotly_chart(gpa_fig, use_container_width=True)
            
            # Specialization Distribution with enhanced styling
            spec_dist = px.pie(df, names='specialization', title='Students per Specialization',
                              color_discrete_sequence=px.colors.qualitative.Set3)
            spec_dist.update_layout(
                title={'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
                plot_bgcolor='black',
                paper_bgcolor='black',
                font={'color': '#e0e0e0'}
            )
            st.plotly_chart(spec_dist, use_container_width=True)
        
        with col2:
            # Test Scores Trend with enhanced styling
            test_scores = pd.melt(df.loc[:, ['test1_score', 'test2_score', 'test3_score']],
                                 var_name='Test', value_name='Score')
            test_box = px.box(test_scores, x='Test', y='Score', title='Test Scores Distribution',
                             color_discrete_sequence=['#4a9eff'])
            test_box.update_layout(
                title={'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
                plot_bgcolor='black',
                paper_bgcolor='black',
                font={'color': '#e0e0e0'},
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#333333', color='#e0e0e0'),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#333333', color='#e0e0e0')
            )
            st.plotly_chart(test_box, use_container_width=True)
            
            # Extracurricular Activities with enhanced styling
            club_data = df['extracurricular_activities'].value_counts().reset_index()
            club_data.columns = ['Club', 'Count']
            club_dist = px.bar(club_data, x='Club', y='Count', title='Club Participation',
                              color_discrete_sequence=['#4a9eff'])
            club_dist.update_layout(
                title={'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
                plot_bgcolor='black',
                paper_bgcolor='black',
                font={'color': '#e0e0e0'},
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#333333', color='#e0e0e0'),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#333333', color='#e0e0e0')
            )
            st.plotly_chart(club_dist, use_container_width=True)
    
    elif page == "Student Details":
        st.markdown("<h1 style='text-align: center;'>👥 Student Details</h1>", unsafe_allow_html=True)
        
        # Modern Filter Section
        st.markdown("<h2 style='color: #2c3e50; margin: 2rem 0 1rem;'>🔍 Search & Filters</h2>", unsafe_allow_html=True)
        
        # Enhanced Filter Layout
        filter_container = st.container()
        with filter_container:
            col1, col2, col3 = st.columns(3)
            with col1:
                search = st.text_input('🔎 Search by Name or ID', placeholder='Enter name or ID...')
            with col2:
                spec_filter = st.selectbox('📚 Specialization', 
                                        ['All'] + list(df['specialization'].unique()))
            with col3:
                club_filter = st.selectbox('🎯 Club Activities', 
                                        ['All'] + list(df['extracurricular_activities'].unique()))
        
        # Apply filters with modern styling
        filtered_df = df.copy()
        if search:
            filtered_df = filtered_df[filtered_df['name'].str.contains(search, case=False) | 
                                     filtered_df['student_id'].astype(str).str.contains(search)]
        if spec_filter != 'All':
            filtered_df = filtered_df[filtered_df['specialization'] == spec_filter]
        if club_filter != 'All':
            filtered_df = filtered_df[filtered_df['extracurricular_activities'] == club_filter]
        
        # Display Results Summary
        st.markdown(f"""<div style='background-color: white; padding: 1rem; border-radius: 8px; 
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin: 1rem 0;'>
            <p style='color: #2c3e50; margin: 0;'>📊 Showing {len(filtered_df)} students</p>
        </div>""", unsafe_allow_html=True)
        
        # Enhanced Student Table
        st.markdown("<h2 style='color: #2c3e50; margin: 2rem 0 1rem;'>📋 Student Records</h2>", unsafe_allow_html=True)
        
        # Modern table with improved formatting and visual hierarchy
        st.dataframe(
            filtered_df[['student_id', 'name', 'email', 'specialization', 'gpa', 
                        'attendance_percentage', 'extracurricular_activities']]
            .style.format({'gpa': '{:.2f}', 'attendance_percentage': '{:.1f}%'})
            .apply(lambda x: ['color: #e0e0e0; background-color: ' + ('#1f4d7a' if x.name in ['gpa', 'attendance_percentage'] else '#2d2d2d')
                            for i in range(len(x))], axis=0)
            .format({
                'student_id': lambda x: f'#{x}',
                'gpa': '{:.2f}',
                'attendance_percentage': '{:.1f}%'
            })
            .set_properties(**{
                'background-color': '#1a1a1a',
                'color': '#e0e0e0',
                'font-size': '14px',
                'padding': '12px',
                'border': '1px solid #333333'
            }),
            height=400,
            use_container_width=True
        )
        
        # Performance Distribution
        st.markdown("<h2 style='color: #2c3e50; margin: 2rem 0 1rem;'>📊 Performance Distribution</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            # GPA Distribution for filtered students
            gpa_hist = px.histogram(filtered_df, x='gpa', nbins=20,
                                   title='GPA Distribution',
                                   color_discrete_sequence=['#1f4d7a'])
            gpa_hist.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': '#2c3e50'},
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0'),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
            )
            st.plotly_chart(gpa_hist, use_container_width=True)
        
        with col2:
            # Attendance Distribution for filtered students
            attendance_hist = px.histogram(filtered_df, x='attendance_percentage', nbins=20,
                                          title='Attendance Distribution',
                                          color_discrete_sequence=['#1f4d7a'])
            attendance_hist.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': '#2c3e50'},
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0'),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
            )
            st.plotly_chart(attendance_hist, use_container_width=True)

# Main app logic
if not st.session_state.authenticated:
    login_page()
else:
    main_dashboard()