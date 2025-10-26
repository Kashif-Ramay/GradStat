"""
Test the full chain: Frontend -> Backend -> Worker
"""
import requests

# Test file path
file_path = r"c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\test-data\normal-data.csv"

print("Testing full chain: Frontend -> Backend -> Worker")
print("=" * 60)

# Test through backend (like frontend does)
with open(file_path, 'rb') as f:
    files = {'file': ('normal-data.csv', f, 'text/csv')}
    data = {'questionKey': 'isNormal'}
    
    response = requests.post(
        'http://localhost:3001/api/test-advisor/auto-answer',
        files=files,
        data=data
    )
    
    print(f"\nBackend Response:")
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON:")
    import json
    print(json.dumps(response.json(), indent=2))
