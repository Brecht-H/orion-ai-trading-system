#!/usr/bin/env python3
"""
📊 API Key Monitoring System
Monitor API key usage and rotation schedule
"""

import os
import json
import requests
from datetime import datetime, timedelta

def check_api_key_status():
    """Check status of all API keys"""
    status_report = {
        'check_time': datetime.now().isoformat(),
        'api_status': {}
    }
    
    # Check Notion
    try:
        notion_token = os.getenv('NOTION_TOKEN')
        if notion_token and notion_token != 'your_key_here':
            headers = {
                'Authorization': f'Bearer {notion_token}',
                'Notion-Version': '2022-06-28'
            }
            response = requests.get('https://api.notion.com/v1/users/me', headers=headers, timeout=10)
            status_report['api_status']['notion'] = {
                'status': 'active' if response.status_code == 200 else 'failed',
                'last_check': datetime.now().isoformat(),
                'status_code': response.status_code
            }
        else:
            status_report['api_status']['notion'] = {'status': 'not_configured'}
    except Exception as e:
        status_report['api_status']['notion'] = {'status': 'error', 'error': str(e)}
    
    # Check Groq
    try:
        groq_key = os.getenv('API_Groq')
        if groq_key and groq_key != 'your_groq_key_here':
            status_report['api_status']['groq'] = {'status': 'configured'}
        else:
            status_report['api_status']['groq'] = {'status': 'missing'}
    except Exception as e:
        status_report['api_status']['groq'] = {'status': 'error', 'error': str(e)}
    
    # Check HuggingFace
    try:
        hf_token = os.getenv('HUGGINGFACE_TOKEN')
        if hf_token and len(hf_token) > 10:
            # Test HuggingFace API
            headers = {'Authorization': f'Bearer {hf_token}'}
            response = requests.get('https://huggingface.co/api/whoami', headers=headers, timeout=10)
            status_report['api_status']['huggingface'] = {
                'status': 'active' if response.status_code == 200 else 'failed',
                'last_check': datetime.now().isoformat()
            }
        else:
            status_report['api_status']['huggingface'] = {'status': 'missing'}
    except Exception as e:
        status_report['api_status']['huggingface'] = {'status': 'error', 'error': str(e)}
    
    # Check Bybit (just check if keys are configured)
    try:
        bybit_key = os.getenv('BYBIT_API_KEY')
        bybit_secret = os.getenv('BYBIT_API_SECRET')
        if bybit_key and bybit_secret and len(bybit_key) > 5:
            status_report['api_status']['bybit'] = {'status': 'configured'}
        else:
            status_report['api_status']['bybit'] = {'status': 'missing'}
    except Exception as e:
        status_report['api_status']['bybit'] = {'status': 'error', 'error': str(e)}
    
    return status_report

def check_rotation_schedule():
    """Check if rotation is due"""
    try:
        with open('config/rotation_schedule.json', 'r') as f:
            schedule = json.load(f)
        
        next_rotation = datetime.fromisoformat(schedule['next_rotation_date'])
        days_until = (next_rotation - datetime.now()).days
        
        if days_until <= 7:
            return {
                'rotation_due': True,
                'days_until': days_until,
                'message': f'⚠️ API rotation due in {days_until} days!'
            }
        else:
            return {
                'rotation_due': False,
                'days_until': days_until,
                'message': f'✅ Next rotation in {days_until} days'
            }
    except FileNotFoundError:
        return {'rotation_due': True, 'message': '⚠️ No rotation schedule found'}

def get_api_security_score():
    """Calculate overall API security score"""
    status = check_api_key_status()
    rotation = check_rotation_schedule()
    
    score = 0
    max_score = 100
    
    # API Status (60 points)
    active_apis = sum(1 for api, details in status['api_status'].items() 
                     if details['status'] in ['active', 'configured'])
    total_apis = len(status['api_status'])
    score += (active_apis / total_apis) * 60 if total_apis > 0 else 0
    
    # Rotation Schedule (40 points)
    if not rotation['rotation_due']:
        score += 40
    elif rotation.get('days_until', 0) > 0:
        score += max(0, (rotation['days_until'] / 30) * 40)  # Gradual decrease over 30 days
    
    return round(score, 1)

def main():
    """Run API monitoring"""
    print("📊 API KEY MONITORING REPORT")
    print("="*40)
    
    # Check API status
    status = check_api_key_status()
    print(f"\n🔍 API Status Check ({status['check_time'][:19]}):")
    for api, details in status['api_status'].items():
        if details['status'] == 'active':
            icon = "✅"
        elif details['status'] == 'configured':
            icon = "🔧"
        elif details['status'] == 'missing':
            icon = "❌"
        else:
            icon = "⚠️"
        print(f"  {icon} {api.upper()}: {details['status']}")
    
    # Check rotation schedule
    rotation = check_rotation_schedule()
    print(f"\n📅 Rotation Schedule:")
    print(f"  {rotation['message']}")
    
    # Security score
    security_score = get_api_security_score()
    print(f"\n🛡️ Security Score: {security_score}/100")
    
    if security_score < 70:
        print("  ⚠️ Security improvements needed!")
    elif security_score < 90:
        print("  🔶 Good security posture")
    else:
        print("  ✅ Excellent security posture")
    
    return status

if __name__ == "__main__":
    main() 