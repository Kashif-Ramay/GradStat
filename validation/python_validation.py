"""
GradStat Python-Only Validation
No R required - uses scipy as ground truth
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency
import os

# Create directories
os.makedirs('validation/data', exist_ok=True)
os.makedirs('validation/results', exist_ok=True)

print("=" * 60)
print("GradStat Python Validation - Ground Truth from scipy")
print("=" * 60)
print()

# ============================================================================
# Test 1: Independent T-Test
# ============================================================================
print("Test 1: Independent Samples T-Test")
print("-" * 40)

# Student's sleep data
group1 = [0.7, -1.6, -0.2, -1.2, -0.1, 3.4, 3.7, 0.8, 0.0, 2.0]
group2 = [1.9, 0.8, 1.1, 0.1, -0.1, 4.4, 5.5, 1.6, 4.6, 3.4]

# Calculate with scipy
t_stat, p_value = stats.ttest_ind(group1, group2)

print(f"Group 1 mean: {np.mean(group1):.3f}")
print(f"Group 2 mean: {np.mean(group2):.3f}")
print(f"t-statistic: {t_stat:.3f}")
print(f"p-value: {p_value:.4f}")
print(f"df: {len(group1) + len(group2) - 2}")

# Save data
df = pd.DataFrame({
    'group': ['A']*10 + ['B']*10,
    'value': group1 + group2
})
df.to_csv('validation/data/ttest_independent.csv', index=False)

print(f"\n✅ Expected GradStat results:")
print(f"   t = {t_stat:.3f}")
print(f"   p = {p_value:.4f}")
print(f"   File: validation/data/ttest_independent.csv")
print()

# ============================================================================
# Test 2: Paired T-Test
# ============================================================================
print("Test 2: Paired Samples T-Test")
print("-" * 40)

before = [5.2, 6.1, 5.8, 4.9, 6.3, 5.7, 6.0, 5.4, 5.9, 6.2]
after = [6.1, 7.2, 6.5, 5.8, 7.1, 6.4, 6.8, 6.2, 6.7, 7.0]

t_stat, p_value = stats.ttest_rel(before, after)

print(f"Before mean: {np.mean(before):.3f}")
print(f"After mean: {np.mean(after):.3f}")
print(f"Mean difference: {np.mean(np.array(after) - np.array(before)):.3f}")
print(f"t-statistic: {t_stat:.3f}")
print(f"p-value: {p_value:.4f}")
print(f"df: {len(before) - 1}")

# Create long format for paired data (GradStat expects duplicate IDs with time column)
df = pd.DataFrame({
    'subject_id': list(range(1, 11)) * 2,
    'time_point': ['pre'] * 10 + ['post'] * 10,
    'value': before + after
})
df = df.sort_values(['subject_id', 'time_point'])
df.to_csv('validation/data/ttest_paired.csv', index=False)

print(f"\n✅ Expected GradStat results:")
print(f"   t = {t_stat:.3f}")
print(f"   p = {p_value:.4f}")
print(f"   File: validation/data/ttest_paired.csv")
print()

# ============================================================================
# Test 3: One-Way ANOVA
# ============================================================================
print("Test 3: One-Way ANOVA")
print("-" * 40)

setosa = [5.1, 4.9, 4.7, 4.6, 5.0, 5.4, 4.6, 5.0, 4.4, 4.9]
versicolor = [7.0, 6.4, 6.9, 5.5, 6.5, 5.7, 6.3, 4.9, 6.6, 5.2]
virginica = [6.3, 5.8, 7.1, 6.3, 6.5, 7.6, 4.9, 7.3, 6.7, 7.2]

f_stat, p_value = stats.f_oneway(setosa, versicolor, virginica)

print(f"Setosa mean: {np.mean(setosa):.3f}")
print(f"Versicolor mean: {np.mean(versicolor):.3f}")
print(f"Virginica mean: {np.mean(virginica):.3f}")
print(f"F-statistic: {f_stat:.3f}")
print(f"p-value: {p_value:.6f}")

df = pd.DataFrame({
    'species': ['setosa']*10 + ['versicolor']*10 + ['virginica']*10,
    'sepal_length': setosa + versicolor + virginica
})
df.to_csv('validation/data/anova_oneway.csv', index=False)

print(f"\n✅ Expected GradStat results:")
print(f"   F = {f_stat:.3f}")
print(f"   p = {p_value:.6f}")
print(f"   File: validation/data/anova_oneway.csv")
print()

# ============================================================================
# Test 4: Linear Regression
# ============================================================================
print("Test 4: Linear Regression")
print("-" * 40)

x = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
y = [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]

slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
r_squared = r_value ** 2

print(f"Slope: {slope:.4f}")
print(f"Intercept: {intercept:.4f}")
print(f"R-squared: {r_squared:.4f}")
print(f"p-value: {p_value:.6f}")

df = pd.DataFrame({'x': x, 'y': y})
df.to_csv('validation/data/regression_linear.csv', index=False)

print(f"\n✅ Expected GradStat results:")
print(f"   Slope = {slope:.4f}")
print(f"   R² = {r_squared:.4f}")
print(f"   File: validation/data/regression_linear.csv")
print()

# ============================================================================
# Test 5: Pearson Correlation
# ============================================================================
print("Test 5: Pearson Correlation")
print("-" * 40)

mpg = [21.0, 21.0, 22.8, 21.4, 18.7, 18.1, 14.3, 24.4, 22.8, 19.2]
wt = [2.620, 2.875, 2.320, 3.215, 3.440, 3.460, 3.570, 3.190, 3.150, 3.440]

r_value, p_value = stats.pearsonr(mpg, wt)

print(f"Correlation coefficient: {r_value:.4f}")
print(f"p-value: {p_value:.4f}")

df = pd.DataFrame({'mpg': mpg, 'weight': wt})
df.to_csv('validation/data/correlation_pearson.csv', index=False)

print(f"\n✅ Expected GradStat results:")
print(f"   r = {r_value:.4f}")
print(f"   p = {p_value:.4f}")
print(f"   File: validation/data/correlation_pearson.csv")
print()

# ============================================================================
# Test 6: Chi-Square Test
# ============================================================================
print("Test 6: Chi-Square Test")
print("-" * 40)

# Create contingency table data
observed = [[10, 20], [30, 40]]
chi2, p, dof, expected = chi2_contingency(observed)

print(f"Chi-square statistic: {chi2:.3f}")
print(f"p-value: {p:.4f}")
print(f"df: {dof}")

# Create CSV from contingency table
df = pd.DataFrame({
    'treatment': ['A']*30 + ['B']*70,
    'outcome': ['success']*10 + ['failure']*20 + ['success']*30 + ['failure']*40
})
df.to_csv('validation/data/chisquare.csv', index=False)

print(f"\n✅ Expected GradStat results:")
print(f"   χ² = {chi2:.3f}")
print(f"   p = {p:.4f}")
print(f"   File: validation/data/chisquare.csv")
print()

# ============================================================================
# Test 7: Mann-Whitney U Test
# ============================================================================
print("Test 7: Mann-Whitney U Test")
print("-" * 40)

group1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
group2 = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

u_stat, p_value = stats.mannwhitneyu(group1, group2)

print(f"Group 1 median: {np.median(group1):.1f}")
print(f"Group 2 median: {np.median(group2):.1f}")
print(f"U-statistic: {u_stat:.1f}")
print(f"p-value: {p_value:.4f}")

df = pd.DataFrame({
    'group': ['A']*10 + ['B']*10,
    'value': group1 + group2
})
df.to_csv('validation/data/mannwhitney.csv', index=False)

print(f"\n✅ Expected GradStat results:")
print(f"   U = {u_stat:.1f}")
print(f"   p = {p_value:.4f}")
print(f"   File: validation/data/mannwhitney.csv")
print()

# ============================================================================
# Summary
# ============================================================================
print("=" * 60)
print("SUMMARY")
print("=" * 60)
print()
print("✅ Generated 7 test datasets with scipy ground truth")
print("✅ All CSV files saved to validation/data/")
print("✅ Compare GradStat results to values above")
print()
print("Next steps:")
print("1. Upload each CSV to GradStat")
print("2. Run the corresponding analysis")
print("3. Compare results to scipy values above")
print("4. Tolerance: ±0.01 for statistics, ±0.001 for p-values")
print()
print("=" * 60)

# Save summary to file
with open('validation/results/PYTHON_VALIDATION_SUMMARY.txt', 'w', encoding='utf-8') as f:
    f.write("GradStat Python Validation Summary\n")
    f.write("=" * 60 + "\n\n")
    
    f.write("Test 1: Independent T-Test\n")
    t_stat, p_value = stats.ttest_ind(group1, group2)
    f.write(f"  t = {t_stat:.3f}\n")
    f.write(f"  p = {p_value:.4f}\n\n")
    
    f.write("Test 2: Paired T-Test\n")
    t_stat, p_value = stats.ttest_rel(before, after)
    f.write(f"  t = {t_stat:.3f}\n")
    f.write(f"  p = {p_value:.4f}\n\n")
    
    f.write("Test 3: One-Way ANOVA\n")
    f_stat, p_value = stats.f_oneway(setosa, versicolor, virginica)
    f.write(f"  F = {f_stat:.3f}\n")
    f.write(f"  p = {p_value:.6f}\n\n")
    
    f.write("Test 4: Linear Regression\n")
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    f.write(f"  Slope = {slope:.4f}\n")
    f.write(f"  R² = {r_value**2:.4f}\n\n")
    
    f.write("Test 5: Pearson Correlation\n")
    r_value, p_value = stats.pearsonr(mpg, wt)
    f.write(f"  r = {r_value:.4f}\n")
    f.write(f"  p = {p_value:.4f}\n\n")
    
    f.write("Test 6: Chi-Square\n")
    chi2, p, dof, expected = chi2_contingency(observed)
    f.write(f"  χ² = {chi2:.3f}\n")
    f.write(f"  p = {p:.4f}\n\n")
    
    f.write("Test 7: Mann-Whitney U\n")
    u_stat, p_value = stats.mannwhitneyu(group1, group2)
    f.write(f"  U = {u_stat:.1f}\n")
    f.write(f"  p = {p_value:.4f}\n")

print("\n📄 Summary saved to: validation/results/PYTHON_VALIDATION_SUMMARY.txt")
print("\n🎉 Validation data generation complete!")
