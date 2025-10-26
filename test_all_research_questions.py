"""
Test comprehensive analysis for ALL research questions
"""
import requests
import json

def test_analysis(name, file_path):
    """Test comprehensive analysis"""
    print(f"\n{'='*70}")
    print(f"TEST: {name}")
    print(f"{'='*70}")
    
    with open(file_path, 'rb') as f:
        files = {'file': (file_path.split('\\')[-1], f, 'text/csv')}
        
        response = requests.post(
            'http://localhost:3001/api/test-advisor/analyze-dataset',
            files=files
        )
        
        result = response.json()
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200 and result.get('ok'):
            print(f"\n✅ ANALYSIS SUCCESSFUL\n")
            
            # Compare Groups answers
            print("📊 COMPARE GROUPS Answers:")
            print(f"  - isNormal: {result.get('isNormal')} ({result.get('confidence', {}).get('isNormal', 'N/A')})")
            print(f"  - nGroups: {result.get('nGroups')} ({result.get('confidence', {}).get('nGroups', 'N/A')})")
            print(f"  - isPaired: {result.get('isPaired')} ({result.get('confidence', {}).get('isPaired', 'N/A')})")
            print(f"  - outcomeType: {result.get('outcomeType')} ({result.get('confidence', {}).get('outcomeType', 'N/A')})")
            
            # Find Relationships answers
            print(f"\n🔗 FIND RELATIONSHIPS Answers:")
            print(f"  - var1Type: {result.get('var1Type')} ({result.get('confidence', {}).get('varTypes', 'N/A')})")
            print(f"  - var2Type: {result.get('var2Type')} ({result.get('confidence', {}).get('varTypes', 'N/A')})")
            print(f"  - nPredictors: {result.get('nPredictors')} ({result.get('confidence', {}).get('nPredictors', 'N/A')})")
            
            # Predict Outcome answers
            print(f"\n🎯 PREDICT OUTCOME Answers:")
            print(f"  - outcomeType: {result.get('outcomeType')} ({result.get('confidence', {}).get('outcomeType', 'N/A')})")
            print(f"  - nPredictors: {result.get('nPredictors')} ({result.get('confidence', {}).get('nPredictors', 'N/A')})")
            
            # Summary
            if 'summary' in result:
                print(f"\n📈 SUMMARY:")
                print(f"  - Total Questions: {result['summary'].get('total_questions')}")
                print(f"  - High Confidence: {result['summary'].get('high_confidence')}")
                print(f"  - Confidence Rate: {result['summary'].get('confidence_rate')}")
                print(f"  - Recommendation: {result['summary'].get('recommendation')}")
        else:
            print(f"❌ FAILED")
            print(f"Error: {result}")
        
        return result

# Run comprehensive tests
print("🧪 COMPREHENSIVE ANALYSIS TEST - ALL RESEARCH QUESTIONS")
print("="*70)

# Test 1: Normal data (good for all types)
test_analysis(
    "Normal Data - All Research Questions",
    r"c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\test-data\normal-data.csv"
)

# Test 2: Grouped data (multiple groups)
test_analysis(
    "Grouped Data - All Research Questions",
    r"c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\test-data\grouped-data.csv"
)

# Test 3: Paired data (repeated measures)
test_analysis(
    "Paired Data - All Research Questions",
    r"c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\test-data\paired-data.csv"
)

# Test 4: Non-normal data
test_analysis(
    "Non-Normal Data - All Research Questions",
    r"c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\test-data\non-normal-data.csv"
)

print(f"\n{'='*70}")
print("🎉 TEST SUITE COMPLETE!")
print(f"{'='*70}")
print("\n📝 EXPECTED BEHAVIOR:")
print("  - Compare Groups: All 4 questions answered")
print("  - Find Relationships: Variable types + predictors detected")
print("  - Predict Outcome: Outcome type + predictors detected")
print("\n✨ All research questions should now have pre-filled answers!")
