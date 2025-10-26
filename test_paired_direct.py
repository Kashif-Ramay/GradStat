"""
Test isPaired directly with worker
"""
import requests

file_path = r"c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\test-data\paired-data.csv"

print("Testing isPaired detection...")

with open(file_path, 'rb') as f:
    files = {'file': ('paired-data.csv', f, 'text/csv')}
    data = {'question_key': 'isPaired'}
    
    response = requests.post(
        'http://localhost:8001/test-advisor/auto-answer',
        files=files,
        data=data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        import json
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")
