"""
Test comprehensive dataset analysis (Sprint 1.2)
"""
import requests
import json

def test_comprehensive_analysis(name, file_path):
    """Test comprehensive analysis on a dataset"""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")
    
    with open(file_path, 'rb') as f:
        files = {'file': (file_path.split('\\')[-1], f, 'text/csv')}
        
        # Test through backend
        response = requests.post(
            'http://localhost:3001/api/test-advisor/analyze-dataset',
            files=files
        )
        
        result = response.json()
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200 and result.get('ok'):
            print(f"\n✅ ANALYSIS SUCCESSFUL")
            print(f"\nAnswers:")
            print(f"  - isNormal: {result.get('isNormal')} ({result.get('confidence', {}).get('isNormal', 'N/A')} confidence)")
            print(f"  - nGroups: {result.get('nGroups')} ({result.get('confidence', {}).get('nGroups', 'N/A')} confidence)")
            print(f"  - isPaired: {result.get('isPaired')} ({result.get('confidence', {}).get('isPaired', 'N/A')} confidence)")
            print(f"  - outcomeType: {result.get('outcomeType')} ({result.get('confidence', {}).get('outcomeType', 'N/A')} confidence)")
            
            if 'summary' in result:
                print(f"\nSummary:")
                print(f"  - Total Questions: {result['summary'].get('total_questions')}")
                print(f"  - High Confidence: {result['summary'].get('high_confidence')}")
                print(f"  - Confidence Rate: {result['summary'].get('confidence_rate')}")
                print(f"  - Recommendation: {result['summary'].get('recommendation')}")
        else:
            print(f"❌ FAILED")
            print(f"Error: {result}")
        
        return result

# Run tests
print("🧪 COMPREHENSIVE DATASET ANALYSIS TEST SUITE")
print("="*60)

# Test 1: Normal data
test_comprehensive_analysis(
    "Normal Data - All Questions",
    r"c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\test-data\normal-data.csv"
)

# Test 2: Non-normal data
test_comprehensive_analysis(
    "Non-Normal Data - All Questions",
    r"c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\test-data\non-normal-data.csv"
)

# Test 3: Paired data
test_comprehensive_analysis(
    "Paired Data - All Questions",
    r"c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\test-data\paired-data.csv"
)

# Test 4: Grouped data
test_comprehensive_analysis(
    "Grouped Data - All Questions",
    r"c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\test-data\grouped-data.csv"
)

print(f"\n{'='*60}")
print("🎉 TEST SUITE COMPLETE!")
print(f"{'='*60}")
