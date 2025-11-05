"""
Test script for LLM interpreter
Run this to verify OpenAI integration works
"""

import sys
import os

# Add worker directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'worker'))

from llm_interpreter import StatisticalInterpreter

def test_interpreter():
    """Test the LLM interpreter with sample data"""
    
    print("=" * 60)
    print("Testing LLM Statistical Interpreter")
    print("=" * 60)
    
    # Initialize interpreter
    interpreter = StatisticalInterpreter()
    
    # Check if API key is available
    if not interpreter.is_available():
        print("\n❌ ERROR: OPENAI_API_KEY not found!")
        print("\nTo fix this:")
        print("1. Get API key from: https://platform.openai.com")
        print("2. Set environment variable:")
        print("   export OPENAI_API_KEY='sk-...'  # Mac/Linux")
        print("   set OPENAI_API_KEY=sk-...       # Windows CMD")
        print("   $env:OPENAI_API_KEY='sk-...'    # Windows PowerShell")
        return False
    
    print("\n✅ OpenAI API key found!")
    print(f"✅ Using model: {interpreter.model}")
    
    # Sample analysis data (t-test results)
    sample_data = {
        'analysis_type': 'Independent Samples t-test',
        'sample_size': 45,
        'variables': ['treatment', 'score'],
        'results': {
            'p_value': 0.023,
            't_statistic': 2.45,
            'effect_size': {
                'type': "Cohen's d",
                'value': 0.68
            },
            'mean_group1': 72.3,
            'mean_group2': 87.6,
            'mean_difference': 15.3
        },
        'assumptions': {
            'normality': {'passed': True, 'p_value': 0.15},
            'equal_variances': {'passed': True, 'p_value': 0.42}
        }
    }
    
    print("\n" + "=" * 60)
    print("Test 1: Generate Interpretation")
    print("=" * 60)
    
    try:
        interpretation = interpreter.interpret_results(sample_data)
        
        print("\n📊 Interpretation:")
        print(interpretation['interpretation'])
        
        print("\n🎯 Key Findings:")
        for finding in interpretation['key_findings']:
            print(f"  ✓ {finding}")
        
        if interpretation['concerns']:
            print("\n⚠️ Concerns:")
            for concern in interpretation['concerns']:
                print(f"  ! {concern}")
        
        print("\n🚀 Next Steps:")
        for step in interpretation['next_steps']:
            print(f"  {step}")
        
        print("\n✅ Test 1 PASSED")
        
    except Exception as e:
        print(f"\n❌ Test 1 FAILED: {str(e)}")
        return False
    
    print("\n" + "=" * 60)
    print("Test 2: Answer Question")
    print("=" * 60)
    
    try:
        question = "What does Cohen's d mean?"
        print(f"\n❓ Question: {question}")
        
        answer = interpreter.answer_question(question, sample_data)
        print(f"\n💬 Answer:\n{answer}")
        
        print("\n✅ Test 2 PASSED")
        
    except Exception as e:
        print(f"\n❌ Test 2 FAILED: {str(e)}")
        return False
    
    print("\n" + "=" * 60)
    print("Test 3: What-If Scenario")
    print("=" * 60)
    
    try:
        scenario = "What if I doubled my sample size?"
        print(f"\n🔮 Scenario: {scenario}")
        
        response = interpreter.what_if_analysis(scenario, sample_data)
        print(f"\n🤖 Analysis:\n{response}")
        
        print("\n✅ Test 3 PASSED")
        
    except Exception as e:
        print(f"\n❌ Test 3 FAILED: {str(e)}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED!")
    print("=" * 60)
    print("\nLLM interpreter is working correctly!")
    print("You can now use it in GradStat.")
    
    return True


if __name__ == "__main__":
    success = test_interpreter()
    sys.exit(0 if success else 1)
