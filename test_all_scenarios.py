"""
Comprehensive test of all auto-detection scenarios
"""
import requests
import json

def test_scenario(name, file_path, question_key, expected_answer=None):
    """Test a specific scenario"""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")
    
    with open(file_path, 'rb') as f:
        files = {'file': (file_path.split('\\')[-1], f, 'text/csv')}
        data = {'questionKey': question_key}
        
        response = requests.post(
            'http://localhost:3001/api/test-advisor/auto-answer',
            files=files,
            data=data
        )
        
        result = response.json()
        
        print(f"Status: {response.status_code}")
        print(f"Answer: {result.get('answer')}")
        print(f"Confidence: {result.get('confidence')}")
        print(f"Explanation: {result.get('explanation')}")
        
        if expected_answer is not None:
            if result.get('answer') == expected_answer:
                print(f"✅ PASS - Got expected answer: {expected_answer}")
            else:
                print(f"❌ FAIL - Expected {expected_answer}, got {result.get('answer')}")
        
        # Show details if available
        if result.get('details'):
            print(f"\nDetails:")
            print(json.dumps(result['details'], indent=2))
        
        return result

# Test scenarios
print("🧪 COMPREHENSIVE AUTO-DETECTION TEST SUITE")
print("="*60)

# Test 1: Normal data - isNormal
test_scenario(
    "Normal Data - Normality Test",
    r"c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\test-data\normal-data.csv",
    "isNormal",
    expected_answer=True
)

# Test 2: Non-normal data - isNormal
test_scenario(
    "Non-Normal Data - Normality Test",
    r"c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\test-data\non-normal-data.csv",
    "isNormal",
    expected_answer=False
)

# Test 3: Paired data - isPaired
test_scenario(
    "Paired Data - Paired Test",
    r"c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\test-data\paired-data.csv",
    "isPaired",
    expected_answer=True
)

# Test 4: Grouped data - nGroups
test_scenario(
    "Grouped Data - Number of Groups",
    r"c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\test-data\grouped-data.csv",
    "nGroups",
    expected_answer=3
)

print(f"\n{'='*60}")
print("🎉 TEST SUITE COMPLETE!")
print(f"{'='*60}")
