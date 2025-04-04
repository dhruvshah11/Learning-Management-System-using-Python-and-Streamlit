import pandas as pd
import numpy as np

def calculate_gpa(test1, test2, test3):
    # Enhanced GPA calculation with weighted scores
    weights = [0.3, 0.3, 0.4]  # More weight to recent test
    weighted_avg = (test1 * weights[0] + test2 * weights[1] + test3 * weights[2])
    return (weighted_avg / 100) * 4.0

def get_performance_trend(test1, test2, test3):
    # Advanced performance trend analysis
    recent_change = test3 - test2
    overall_change = test3 - test1
    
    if recent_change > 5 and overall_change > 10:
        return '📈 Strong Improvement'
    elif recent_change > 0 and overall_change > 0:
        return '📈 Steady Improvement'
    elif recent_change < -5 and overall_change < -10:
        return '📉 Needs Attention'
    elif recent_change < 0 and overall_change < 0:
        return '📉 Slight Decline'
    else:
        return '📊 Maintaining Level'

def generate_recommendations(attendance, assignments_completed, test_scores):
    recommendations = []
    
    # Attendance recommendations
    if attendance < 85:
        recommendations.append('Try to improve your attendance to better understand the course material')
    
    # Assignment recommendations
    if assignments_completed < 8:
        recommendations.append('Complete more assignments to strengthen your practical skills')
    
    # Test performance recommendations
    avg_score = np.mean(test_scores)
    if avg_score < 70:
        recommendations.append('Consider seeking additional help with course material')
    elif avg_score < 80:
        recommendations.append('Regular practice could help improve your test scores')
    
    return recommendations

def calculate_subject_strength(test_scores):
    avg_score = np.mean(test_scores)
    if avg_score >= 90:
        return 'Excellent'
    elif avg_score >= 80:
        return 'Good'
    elif avg_score >= 70:
        return 'Average'
    return 'Needs Improvement'