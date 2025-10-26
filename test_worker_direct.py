"""
Test worker endpoint directly
"""
import requests

# Test file path
file_path = r"c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\test-data\normal-data.csv"

# Open and send file
with open(file_path, 'rb') as f:
    files = {'file': ('normal-data.csv', f, 'text/csv')}
    data = {'question_key': 'isNormal'}
    
    response = requests.post(
        'http://localhost:8001/test-advisor/auto-answer',
        files=files,
        data=data
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
