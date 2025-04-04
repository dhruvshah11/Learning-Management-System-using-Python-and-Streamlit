import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def analyze_attendance_pattern(attendance_percentage, total_classes, classes_attended):
    status = 'Good' if attendance_percentage >= 85 else 'Warning' if attendance_percentage >= 75 else 'Critical'
    classes_missed = total_classes - classes_attended
    required_classes = 0
    
    if attendance_percentage < 85:
        # Calculate classes needed to reach 85% attendance
        target_attendance = 0.85
        current_total = total_classes
        while (classes_attended / current_total) < target_attendance:
            required_classes += 1
            current_total += 1
            classes_attended += 1
    
    return {
        'status': status,
        'classes_missed': classes_missed,
        'classes_needed': required_classes,
        'current_percentage': attendance_percentage
    }

def generate_attendance_alert(attendance_data):
    alerts = []
    if attendance_data['status'] == 'Critical':
        alerts.append({
            'severity': 'High',
            'message': f'Critical attendance alert! Current attendance is {attendance_data["current_percentage"]}%. '
                      f'Need to attend next {attendance_data["classes_needed"]} classes to reach minimum requirement.'
        })
    elif attendance_data['status'] == 'Warning':
        alerts.append({
            'severity': 'Medium',
            'message': f'Attendance warning! Current attendance is {attendance_data["current_percentage"]}%. '
                      f'Need to attend next {attendance_data["classes_needed"]} classes to reach good standing.'
        })
    
    return alerts

def get_attendance_summary(attendance_percentage, total_classes, classes_attended):
    pattern = analyze_attendance_pattern(attendance_percentage, total_classes, classes_attended)
    alerts = generate_attendance_alert(pattern)
    
    return {
        'pattern': pattern,
        'alerts': alerts,
        'attendance_rate': attendance_percentage,
        'total_classes': total_classes,
        'attended_classes': classes_attended
    }