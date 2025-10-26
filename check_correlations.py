import pandas as pd
import numpy as np

df = pd.read_csv('example-data/health_exercise_study.csv')

# Check the variables you're using
vars_used = ['age', 'bmi', 'exercise_hours_per_week']

print("=" * 60)
print("CORRELATION MATRIX")
print("=" * 60)
print(df[vars_used].corr().round(3))

print("\n" + "=" * 60)
print("DESCRIPTIVE STATISTICS")
print("=" * 60)
print(df[vars_used].describe().round(2))

print("\n" + "=" * 60)
print("PAIRWISE CORRELATIONS")
print("=" * 60)
corr = df[vars_used].corr()
for i in range(len(vars_used)):
    for j in range(i+1, len(vars_used)):
        print(f"{vars_used[i]} <-> {vars_used[j]}: r = {corr.iloc[i, j]:.3f}")

# Check if cholesterol was accidentally included
print("\n" + "=" * 60)
print("CHECKING IF CHOLESTEROL IS IN THE MODEL")
print("=" * 60)
if 'cholesterol' in df.columns:
    print("Cholesterol column exists in dataset")
    print(f"Correlation with exercise_hours_per_week: {df[['cholesterol', 'exercise_hours_per_week']].corr().iloc[0,1]:.3f}")
    print(f"Correlation with age: {df[['cholesterol', 'age']].corr().iloc[0,1]:.3f}")
    print(f"Correlation with bmi: {df[['cholesterol', 'bmi']].corr().iloc[0,1]:.3f}")
