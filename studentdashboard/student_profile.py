import streamlit as st
import pandas as pd
import plotly.express as px
from analytics import calculate_gpa, get_performance_trend, generate_recommendations, calculate_subject_strength

def display_student_profile(student_data):
    # Theme toggle
    theme = st.sidebar.selectbox('🎨 Theme', ['Light', 'Dark'])
    if theme == 'Dark':
        st.markdown("""
        <style>
            .main { background-color: #1a1a1a; color: #ffffff; }
            .profile-header { text-align: center; margin-bottom: 2rem; }
            .profile-header h1 { color: #ffffff; font-size: 2.5rem; font-weight: 600; }
            .section-header { color: #ffffff; margin: 2rem 0 1rem; font-size: 1.5rem; }
            .metric-card { background-color: #2d2d2d; padding: 1.5rem; border-radius: 12px; 
                          box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: transform 0.3s; color: #ffffff; }
            .metric-card:hover { transform: translateY(-5px); }
            div[data-testid="stPlotlyChart"] { background-color: #2d2d2d !important; border-radius: 10px; padding: 1rem; }
            div[data-testid="stPlotlyChart"] .main-svg { background-color: #2d2d2d !important; }
            div[data-testid="stPlotlyChart"] .gridlayer path { stroke: #3d3d3d !important; }
            div[data-testid="stPlotlyChart"] .xy text { fill: #ffffff !important; }
            div[data-testid="stPlotlyChart"] .legendtext { fill: #ffffff !important; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .profile-header { text-align: center; margin-bottom: 2rem; }
            .profile-header h1 { color: #1f4d7a; font-size: 2.5rem; font-weight: 600; }
            .section-header { color: #2c3e50; margin: 2rem 0 1rem; font-size: 1.5rem; }
            .metric-card { background-color: white; padding: 1.5rem; border-radius: 12px; 
                          box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: transform 0.3s; }
            .metric-card:hover { transform: translateY(-5px); }
        </style>
        """, unsafe_allow_html=True)
    
    # Profile Header with Student Name and Image
    st.markdown(f"""<div class='profile-header'>
        <h1>👨‍🎓 {student_data['name']}'s Profile</h1>
        <p style='color: #666; font-size: 1.1rem;'>Student Dashboard</p>
    </div>""", unsafe_allow_html=True)
    
    # Basic Information Cards with enhanced styling
    st.markdown("<h2 class='section-header'>📋 Basic Information</h2>", unsafe_allow_html=True)
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
            <h3 style='color: #1f4d7a; margin: 0;'>Attendance</h3>
            <p style='font-size: 1.5rem; margin: 0.5rem 0;'>{student_data['attendance_percentage']:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Academic Performance Section with interactive charts
    st.markdown("<h2 class='section-header'>📈 Academic Performance</h2>", unsafe_allow_html=True)
    test_scores = [student_data['test1_score'], student_data['test2_score'], student_data['test3_score']]
    
    # GPA and Performance Trend Cards with animations
    col1, col2 = st.columns(2)
    with col1:
        gpa = calculate_gpa(test_scores[0], test_scores[1], test_scores[2])
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #1f4d7a; margin: 0;'>GPA</h3>
            <p style='font-size: 2rem; margin: 0.5rem 0;'>{gpa:.2f}<span style='font-size: 1rem;'>/4.0</span></p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        trend = get_performance_trend(test_scores[0], test_scores[1], test_scores[2])
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #1f4d7a; margin: 0;'>Performance Trend</h3>
            <p style='font-size: 1.5rem; margin: 0.5rem 0;'>{trend}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Test Scores Visualization with Enhanced Styling
    scores_df = pd.DataFrame({
        'Test': ['Test 1', 'Test 2', 'Test 3'],
        'Score': test_scores
    })
    fig = px.line(scores_df, x='Test', y='Score', markers=True)
    if theme == 'Dark':
        fig.update_layout(
            title={'text': 'Test Performance Trend', 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
            plot_bgcolor='#2d2d2d',
            paper_bgcolor='#2d2d2d',
            font={'color': '#ffffff'},
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#3d3d3d'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#3d3d3d')
        )
    else:
        fig.update_layout(
            title={'text': 'Test Performance Trend', 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': '#2c3e50'},
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        )
    fig.update_traces(line_color='#1f4d7a', marker=dict(size=10, color='#1f4d7a'))
    st.plotly_chart(fig, use_container_width=True)
    
    # Subject Strength Section with Modern Card Design
    st.markdown("<h2 style='color: #2c3e50; margin: 2rem 0 1rem;'>💪 Subject Strength</h2>", unsafe_allow_html=True)
    strength = calculate_subject_strength(test_scores)
    st.markdown(f"""<div style='background-color: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
        <h3 style='color: #1f4d7a; margin: 0;'>Overall Performance Level</h3>
        <p style='color: #2c3e50; font-size: 1.2rem; margin: 0.5rem 0;'>{strength}</p>
    </div>""", unsafe_allow_html=True)
    
    # Assignments Progress with Enhanced Visual
    st.markdown("<h2 style='color: #2c3e50; margin: 2rem 0 1rem;'>📝 Assignments Progress</h2>", unsafe_allow_html=True)
    progress = (student_data['assignments_completed'] / 10) * 100
    st.markdown(f"""<div style='background-color: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
            <span style='color: #2c3e50; font-size: 1.1rem;'>Completed {student_data['assignments_completed']} out of 10 assignments</span>
            <span style='color: #1f4d7a; font-weight: bold;'>{progress:.0f}%</span>
        </div>""", unsafe_allow_html=True)
    st.progress(progress/100)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Personalized Recommendations with Card Design
    st.markdown("<h2 style='color: #2c3e50; margin: 2rem 0 1rem;'>🎯 Personalized Recommendations</h2>", unsafe_allow_html=True)
    recommendations = generate_recommendations(
        student_data['attendance_percentage'],
        student_data['assignments_completed'],
        test_scores
    )
    for rec in recommendations:
        st.markdown(f"""<div style='background-color: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 0.5rem;'>
            <p style='color: #2c3e50; margin: 0;'>{rec}</p>
        </div>""", unsafe_allow_html=True)