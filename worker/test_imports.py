#!/usr/bin/env python3
"""Test if test_advisor imports work"""

try:
    print("Testing imports...")
    from test_advisor import recommend_test, auto_detect_from_data
    print("✅ test_advisor imports successful")
    
    from test_library import TEST_LIBRARY
    print("✅ test_library imports successful")
    
    print(f"✅ Found {len(TEST_LIBRARY)} tests in library")
    
    # Test a simple recommendation
    answers = {
        'researchQuestion': 'compare_groups',
        'nGroups': 2,
        'outcomeType': 'continuous',
        'isNormal': True,
        'isPaired': False
    }
    
    result = recommend_test(answers)
    print(f"✅ Got {len(result)} recommendations")
    print(f"✅ First test: {result[0]['test_name']}")
    
    print("\n🎉 All imports working correctly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
