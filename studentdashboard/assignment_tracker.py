import pandas as pd
from datetime import datetime, timedelta

def get_assignment_status(assignments_completed):
    total_assignments = 10
    pending_assignments = total_assignments - assignments_completed
    completion_rate = (assignments_completed / total_assignments) * 100
    
    status = {
        'total': total_assignments,
        'completed': assignments_completed,
        'pending': pending_assignments,
        'completion_rate': completion_rate
    }
    
    # Generate deadline alerts
    if pending_assignments > 0:
        if completion_rate < 60:
            status['alert'] = 'High Priority: Multiple assignments pending. Please complete them soon.'
            status['alert_level'] = 'High'
        elif completion_rate < 80:
            status['alert'] = 'Medium Priority: Stay on track with your remaining assignments.'
            status['alert_level'] = 'Medium'
        else:
            status['alert'] = 'Low Priority: You\'re doing well, keep up the good work!'
            status['alert_level'] = 'Low'
    else:
        status['alert'] = 'All assignments completed! Great job!'
        status['alert_level'] = 'None'
    
    return status

def get_assignment_analytics(assignments_completed):
    status = get_assignment_status(assignments_completed)
    
    # Calculate estimated completion time
    avg_time_per_assignment = 7  # days
    remaining_time = status['pending'] * avg_time_per_assignment
    
    analytics = {
        'status': status,
        'estimated_completion_days': remaining_time,
        'recommended_pace': 'Normal' if remaining_time <= 30 else 'Accelerated',
        'success_probability': 'High' if status['completion_rate'] >= 80 else
                              'Medium' if status['completion_rate'] >= 60 else 'Low'
    }
    
    return analytics