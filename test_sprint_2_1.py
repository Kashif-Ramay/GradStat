"""
Test Sprint 2.1: All Research Question Types Detection
Tests survival analysis, PCA, and clustering detection functions
"""

import pandas as pd
import sys
sys.path.append('worker')

from test_advisor import (
    detect_time_event_columns,
    detect_pca_options,
    detect_clustering_options,
    analyze_dataset_comprehensive
)

def print_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_result(label, value, confidence=None):
    conf_str = f" ({confidence})" if confidence else ""
    print(f"  {label}: {value}{conf_str}")

# Test 1: Survival Analysis Detection
print_section("TEST 1: Survival Analysis Detection")
df_survival = pd.read_csv('test-data/survival-data.csv')
print(f"Dataset shape: {df_survival.shape}")
print(f"Columns: {list(df_survival.columns)}")

survival_result = detect_time_event_columns(df_survival)
print("\n📊 Detection Results:")
print_result("Time column", survival_result['time_column'], survival_result['confidence']['time_column'])
print_result("Event column", survival_result['event_column'], survival_result['confidence']['event_column'])
print_result("Has groups", survival_result['has_groups'], survival_result['confidence']['has_groups'])
if survival_result['has_groups']:
    print_result("Group column", survival_result['group_column'])
print_result("Has covariates", survival_result['has_covariates'], survival_result['confidence']['has_covariates'])
print_result("Number of covariates", len(survival_result['covariate_columns']))

if 'censoring_pct' in survival_result['details']:
    print_result("Censoring percentage", f"{survival_result['details']['censoring_pct']:.1f}%")

# Test 2: PCA Detection
print_section("TEST 2: PCA Options Detection")
df_pca = pd.read_csv('test-data/pca-data.csv')
print(f"Dataset shape: {df_pca.shape}")
print(f"Columns: {list(df_pca.columns)}")

pca_result = detect_pca_options(df_pca)
print("\n📊 Detection Results:")
print_result("Number of numeric variables", pca_result['n_numeric_vars'])
print_result("Suggested components", pca_result['suggested_components'], pca_result['confidence']['n_components'])
print_result("Scaling needed", pca_result['scaling_needed'], pca_result['confidence']['scaling'])
print_result("Correlation strength", pca_result['correlation_strength'])

if 'variance_ratio' in pca_result['details']:
    print_result("Variance ratio", f"{pca_result['details']['variance_ratio']:.2f}")
if 'avg_correlation' in pca_result['details']:
    print_result("Average correlation", f"{pca_result['details']['avg_correlation']:.3f}")

# Test 3: Clustering Detection
print_section("TEST 3: Clustering Options Detection")
df_clustering = pd.read_csv('test-data/clustering-data.csv')
print(f"Dataset shape: {df_clustering.shape}")
print(f"Columns: {list(df_clustering.columns)}")

clustering_result = detect_clustering_options(df_clustering)
print("\n📊 Detection Results:")
print_result("Number of numeric variables", clustering_result['n_numeric_vars'])
print_result("Suggested k clusters", clustering_result['suggested_k'], clustering_result['confidence']['n_clusters'])
print_result("Suggested algorithm", clustering_result['suggested_algorithm'], clustering_result['confidence']['algorithm'])
print_result("Scaling needed", clustering_result['scaling_needed'])
print_result("Has outliers", clustering_result['has_outliers'])

if 'outlier_pct' in clustering_result['details']:
    print_result("Outlier percentage", f"{clustering_result['details']['outlier_pct']:.1f}%")

# Test 4: Comprehensive Analysis (All Research Questions)
print_section("TEST 4: Comprehensive Analysis - Survival Data")
comprehensive_result = analyze_dataset_comprehensive(df_survival)

print("\n📊 All Detections:")
print(f"\n  Compare Groups:")
print_result("  - Normal", comprehensive_result.get('isNormal'), comprehensive_result['confidence'].get('isNormal'))
print_result("  - Groups", comprehensive_result.get('nGroups'), comprehensive_result['confidence'].get('nGroups'))
print_result("  - Paired", comprehensive_result.get('isPaired'), comprehensive_result['confidence'].get('isPaired'))
print_result("  - Outcome type", comprehensive_result.get('outcomeType'), comprehensive_result['confidence'].get('outcomeType'))

print(f"\n  Find Relationships:")
print_result("  - Var1 type", comprehensive_result.get('var1Type'))
print_result("  - Var2 type", comprehensive_result.get('var2Type'))
print_result("  - Predictors", comprehensive_result.get('nPredictors'), comprehensive_result['confidence'].get('nPredictors'))

print(f"\n  Survival Analysis:")
if 'survival' in comprehensive_result:
    surv = comprehensive_result['survival']
    print_result("  - Time column", surv.get('time_column'))
    print_result("  - Event column", surv.get('event_column'))
    print_result("  - Has groups", surv.get('has_groups'), comprehensive_result['confidence'].get('hasGroups_survival'))
    print_result("  - Has covariates", surv.get('has_covariates'), comprehensive_result['confidence'].get('hasCovariates'))

print(f"\n  PCA:")
if 'pca' in comprehensive_result:
    pca = comprehensive_result['pca']
    print_result("  - Suggested components", pca.get('suggested_components'), comprehensive_result['confidence'].get('nComponents'))
    print_result("  - Scaling needed", pca.get('scaling_needed'))

print(f"\n  Clustering:")
if 'clustering' in comprehensive_result:
    clust = comprehensive_result['clustering']
    print_result("  - Suggested k", clust.get('suggested_k'), comprehensive_result['confidence'].get('nClusters'))
    print_result("  - Algorithm", clust.get('suggested_algorithm'), comprehensive_result['confidence'].get('algorithm'))

print(f"\n📈 Summary:")
print_result("  Total questions", comprehensive_result['summary']['total_questions'])
print_result("  High confidence", comprehensive_result['summary']['high_confidence'])
print_result("  Confidence rate", comprehensive_result['summary']['confidence_rate'])
print(f"  Recommendation: {comprehensive_result['summary']['recommendation']}")

print("\n" + "="*70)
print("✅ ALL TESTS COMPLETE!")
print("="*70)
print("\nNext steps:")
print("1. Restart worker: cd worker && python main.py")
print("2. Test in browser with new datasets")
print("3. Verify pre-analysis works for all research question types")
