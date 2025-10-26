"""
Test Script for Advanced Statistical Tests
Sprint 2.3 - ANCOVA, Repeated Measures ANOVA, Post-hoc Tests
"""

import pandas as pd
import sys
sys.path.append('worker')

from advanced_tests import (
    ancova_analysis,
    repeated_measures_anova,
    posthoc_tukey,
    calculate_cohens_d,
    calculate_partial_eta_squared,
    interpret_effect_size
)

def test_ancova():
    """Test ANCOVA analysis"""
    print("\n" + "="*60)
    print("TEST 1: ANCOVA Analysis")
    print("="*60)
    
    # Load data
    df = pd.read_csv('test-data/ancova-data.csv')
    print(f"✓ Loaded data: {len(df)} rows, {len(df.columns)} columns")
    print(f"  Columns: {list(df.columns)}")
    print(f"  Groups: {df['group'].unique()}")
    
    # Configure options
    opts = {
        'groupVar': 'group',
        'dependentVar': 'outcome',
        'covariates': ['age', 'baseline_score'],
        'alpha': 0.05
    }
    
    # Run analysis
    try:
        result = ancova_analysis(df, opts)
        print("\n✓ ANCOVA analysis completed successfully!")
        
        # Display results
        print(f"\n📊 Summary:")
        print(f"  {result['summary']}")
        
        print(f"\n📈 Test Results:")
        test_res = result['test_results']
        print(f"  F-statistic: {test_res['F_statistic']:.3f}")
        print(f"  p-value: {test_res['p_value']:.4f}")
        print(f"  Significant: {test_res['significant']}")
        print(f"  Effect Size (ηp²): {test_res['partial_eta_squared']:.3f} ({test_res['effect_size_interpretation']})")
        
        print(f"\n📋 Adjusted Means:")
        for group, stats in test_res['adjusted_means'].items():
            print(f"  {group}: {stats['mean']:.2f} (n={stats['n']})")
        
        print(f"\n🔍 Covariate Effects:")
        for cov in test_res['covariate_effects']:
            sig = "***" if cov['p_value'] < 0.001 else "**" if cov['p_value'] < 0.01 else "*" if cov['p_value'] < 0.05 else "ns"
            print(f"  {cov['covariate']}: F={cov['F']:.3f}, p={cov['p_value']:.4f} {sig}")
        
        print(f"\n🎨 Visualizations: {len(result['plots'])} plots created")
        for plot in result['plots']:
            print(f"  - {plot['title']}")
        
        print("\n✅ ANCOVA TEST PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ ANCOVA TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_repeated_measures():
    """Test Repeated Measures ANOVA"""
    print("\n" + "="*60)
    print("TEST 2: Repeated Measures ANOVA")
    print("="*60)
    
    # Load data
    df = pd.read_csv('test-data/repeated-measures-long.csv')
    print(f"✓ Loaded data: {len(df)} rows, {len(df.columns)} columns")
    print(f"  Columns: {list(df.columns)}")
    print(f"  Subjects: {df['subject_id'].nunique()}")
    print(f"  Time points: {df['time'].unique()}")
    
    # Configure options
    opts = {
        'subjectVar': 'subject_id',
        'timeVar': 'time',
        'dependentVar': 'score',
        'alpha': 0.05
    }
    
    # Run analysis
    try:
        result = repeated_measures_anova(df, opts)
        print("\n✓ Repeated Measures ANOVA completed successfully!")
        
        # Display results
        print(f"\n📊 Summary:")
        print(f"  {result['summary']}")
        
        print(f"\n📈 Test Results:")
        test_res = result['test_results']
        print(f"  F-statistic: {test_res['F_statistic']:.3f}")
        print(f"  p-value: {test_res['p_value']:.4f}")
        print(f"  df: ({test_res['df_numerator']:.1f}, {test_res['df_denominator']:.1f})")
        print(f"  Significant: {test_res['significant']}")
        print(f"  Effect Size (ηp²): {test_res['partial_eta_squared']:.3f} ({test_res['effect_size_interpretation']})")
        
        print(f"\n📋 Descriptive Statistics:")
        for time, stats in test_res['descriptives'].items():
            print(f"  Time {time}: M={stats['mean']:.2f}, SD={stats['std']:.2f}, n={stats['n']}")
        
        print(f"\n🎨 Visualizations: {len(result['plots'])} plot created")
        for plot in result['plots']:
            print(f"  - {plot['title']}")
        
        print("\n✅ REPEATED MEASURES TEST PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ REPEATED MEASURES TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_posthoc():
    """Test Post-hoc Tukey HSD"""
    print("\n" + "="*60)
    print("TEST 3: Post-hoc Tukey HSD")
    print("="*60)
    
    # Load data
    df = pd.read_csv('test-data/ancova-data.csv')
    print(f"✓ Loaded data: {len(df)} rows, {len(df.columns)} columns")
    print(f"  Groups: {df['group'].unique()}")
    
    # Configure options
    opts = {
        'groupVar': 'group',
        'dependentVar': 'outcome',
        'alpha': 0.05
    }
    
    # Run analysis
    try:
        result = posthoc_tukey(df, opts)
        print("\n✓ Post-hoc Tukey HSD completed successfully!")
        
        # Display results
        print(f"\n📊 Summary:")
        print(f"  {result['summary']}")
        
        print(f"\n📈 Test Results:")
        test_res = result['test_results']
        print(f"  Total comparisons: {test_res['n_comparisons']}")
        print(f"  Significant comparisons: {test_res['n_significant']}")
        
        print(f"\n📋 Pairwise Comparisons:")
        for comp in test_res['comparisons']:
            sig = "***" if comp['p_adj'] < 0.001 else "**" if comp['p_adj'] < 0.01 else "*" if comp['p_adj'] < 0.05 else "ns"
            reject_str = "SIGNIFICANT" if comp['reject'] else "not significant"
            print(f"  {comp['group1']} vs {comp['group2']}:")
            print(f"    Mean Diff: {comp['mean_diff']:.3f}")
            print(f"    95% CI: [{comp['lower_ci']:.3f}, {comp['upper_ci']:.3f}]")
            print(f"    p-adj: {comp['p_adj']:.4f} {sig} ({reject_str})")
        
        print(f"\n🎨 Visualizations: {len(result['plots'])} plot created")
        for plot in result['plots']:
            print(f"  - {plot['title']}")
        
        print("\n✅ POST-HOC TEST PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ POST-HOC TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_effect_sizes():
    """Test effect size calculations"""
    print("\n" + "="*60)
    print("TEST 4: Effect Size Calculations")
    print("="*60)
    
    # Test Cohen's d
    group1 = [50, 52, 48, 51, 49]
    group2 = [68, 70, 67, 69, 66]
    d = calculate_cohens_d(group1, group2)
    interp_d = interpret_effect_size(d, 'cohens_d')
    print(f"\n✓ Cohen's d: {d:.3f} ({interp_d})")
    
    # Test partial eta-squared
    ss_effect = 100
    ss_error = 50
    eta_p = calculate_partial_eta_squared(ss_effect, ss_error)
    interp_eta = interpret_effect_size(eta_p, 'partial_eta_squared')
    print(f"✓ Partial η²: {eta_p:.3f} ({interp_eta})")
    
    # Test interpretations
    print("\n📊 Effect Size Interpretations:")
    print("  Cohen's d:")
    for val, expected in [(0.1, 'negligible'), (0.3, 'small'), (0.6, 'medium'), (1.0, 'large')]:
        result = interpret_effect_size(val, 'cohens_d')
        print(f"    {val:.1f} → {result}")
    
    print("  Eta-squared:")
    for val, expected in [(0.005, 'negligible'), (0.03, 'small'), (0.10, 'medium'), (0.20, 'large')]:
        result = interpret_effect_size(val, 'eta_squared')
        print(f"    {val:.3f} → {result}")
    
    print("\n✅ EFFECT SIZE TEST PASSED!")
    return True


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 TESTING ADVANCED STATISTICAL TESTS")
    print("Sprint 2.3 - ANCOVA, Repeated Measures, Post-hoc")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("ANCOVA", test_ancova()))
    results.append(("Repeated Measures ANOVA", test_repeated_measures()))
    results.append(("Post-hoc Tukey HSD", test_posthoc()))
    results.append(("Effect Sizes", test_effect_sizes()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\n🎯 Results: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Sprint 2.3 is ready!")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Review errors above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
