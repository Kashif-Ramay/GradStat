# Priority 1 Features Test Plan

**Date:** October 22, 2025  
**Dataset:** health_exercise_study.csv (180 patients)

---

## Test Suite Overview

### ✅ Features to Test:
1. Simple Linear Regression (baseline)
2. Multiple Regression with VIF
3. Mann-Whitney U Test (non-parametric)
4. Kruskal-Wallis Test (non-parametric)
5. Wilcoxon Signed-Rank Test (non-parametric)
6. Chi-Square Test (categorical)

---

## Test 1: Simple Linear Regression ✅

**Purpose:** Baseline test, no multicollinearity issues

### Configuration:
```json
{
  "analysisType": "regression",
  "dependentVar": "quality_of_life_score",
  "independentVar": "exercise_hours_per_week"
}
```

### Expected Results:
- ✅ Scatter plot with regression line
- ✅ R² value (should be moderate-high, ~0.7-0.9)
- ✅ Significant p-value (< 0.05)
- ✅ Negative or positive relationship
- ✅ Residual plot
- ✅ Normality check passes

### What to Check:
- [ ] Plot renders correctly
- [ ] Coefficients displayed
- [ ] P-values shown
- [ ] Interpretation makes sense
- [ ] Download works

---

## Test 2: Multiple Regression with VIF ⚠️

**Purpose:** Test VIF calculation and multicollinearity detection

### Configuration:
```json
{
  "analysisType": "regression",
  "independentVars": ["age", "exercise_hours_per_week"],
  "dependentVar": "quality_of_life_score"
}
```

**Note:** Removed `bmi` to reduce multicollinearity

### Expected Results:
- ✅ Actual vs Predicted plot
- ✅ Correlation matrix heatmap
- ✅ VIF values displayed (should be < 10 now)
- ✅ Multiple R² and Adjusted R²
- ✅ Coefficients for both predictors
- ✅ Identification of significant predictors

### What to Check:
- [ ] VIF values reasonable (< 10)
- [ ] Correlation heatmap shows
- [ ] Both predictors have coefficients
- [ ] Adjusted R² shown
- [ ] Interpretation mentions multiple predictors
- [ ] Download includes all plots

---

## Test 3: Mann-Whitney U Test 🆕

**Purpose:** Compare 2 groups (non-parametric alternative to t-test)

### Configuration:
```json
{
  "analysisType": "nonparametric",
  "testType": "mann-whitney",
  "groupVar": "gender",
  "dependentVar": "cholesterol"
}
```

### Expected Results:
- ✅ U-statistic
- ✅ P-value
- ✅ Effect size (rank-biserial correlation)
- ✅ Median for each group (Male vs Female)
- ✅ Boxplot visualization
- ✅ No normality assumption check

### What to Check:
- [ ] U-statistic displayed
- [ ] Medians shown for both groups
- [ ] Effect size calculated
- [ ] Boxplot renders
- [ ] Interpretation mentions "non-parametric"
- [ ] Conclusion paragraph present

---

## Test 4: Kruskal-Wallis Test 🆕

**Purpose:** Compare 3+ groups (non-parametric alternative to ANOVA)

### Configuration:
```json
{
  "analysisType": "nonparametric",
  "testType": "kruskal-wallis",
  "groupVar": "exercise_type",
  "dependentVar": "resting_heart_rate"
}
```

**Groups:** None, Light, Moderate, Intense (4 groups)

### Expected Results:
- ✅ H-statistic
- ✅ P-value
- ✅ Degrees of freedom
- ✅ Medians for all 4 groups
- ✅ Boxplot with all groups
- ✅ Significant difference (heart rate should differ by exercise level)

### What to Check:
- [ ] H-statistic displayed
- [ ] All 4 group medians shown
- [ ] Boxplot shows all groups
- [ ] Interpretation mentions multiple groups
- [ ] Conclusion appropriate

---

## Test 5: Wilcoxon Signed-Rank Test 🆕

**Purpose:** Paired samples comparison (non-parametric alternative to paired t-test)

### Configuration:
```json
{
  "analysisType": "nonparametric",
  "testType": "wilcoxon",
  "variable1": "systolic_bp",
  "variable2": "diastolic_bp"
}
```

**Note:** Not truly paired in time, but demonstrates the test

### Expected Results:
- ✅ W-statistic
- ✅ P-value
- ✅ Median difference
- ✅ Number of pairs
- ✅ Histogram of differences
- ✅ Significant result (systolic > diastolic)

### What to Check:
- [ ] W-statistic displayed
- [ ] Median difference shown
- [ ] Histogram of differences renders
- [ ] Red line at zero shown
- [ ] Interpretation mentions "paired"
- [ ] Conclusion appropriate

---

## Test 6: Chi-Square Test 🆕

**Purpose:** Test association between categorical variables

### Configuration:
```json
{
  "analysisType": "categorical",
  "variable1": "gender",
  "variable2": "exercise_type"
}
```

### Expected Results:
- ✅ Chi-square statistic (or Fisher's exact if small cells)
- ✅ P-value
- ✅ Degrees of freedom
- ✅ Cramér's V effect size
- ✅ Contingency table
- ✅ Expected frequencies
- ✅ Stacked bar chart
- ✅ Heatmap of contingency table

### What to Check:
- [ ] Chi-square or Fisher's test used appropriately
- [ ] Cramér's V displayed
- [ ] Effect size interpretation (negligible/small/medium/large)
- [ ] Contingency table shown
- [ ] Both visualizations render
- [ ] Assumption check (expected frequencies ≥ 5)

---

## Test 7: Chi-Square with Small Cells (Fisher's Exact) 🆕

**Purpose:** Verify automatic Fisher's exact test selection

### Configuration:
Create a 2×2 table by filtering:
```json
{
  "analysisType": "categorical",
  "variable1": "gender",
  "variable2": "exercise_type"
}
```

**Note:** If any expected frequency < 5, should use Fisher's exact

### Expected Results:
- ✅ Automatic selection of Fisher's exact test
- ✅ Odds ratio
- ✅ P-value (exact, not approximate)
- ✅ Message: "Fisher's exact test used"

### What to Check:
- [ ] Test type correctly identified
- [ ] Odds ratio shown
- [ ] Explanation of why Fisher's was used
- [ ] 2×2 contingency table

---

## Additional Tests

### Test 8: Multiple Regression with High VIF ⚠️

**Purpose:** Verify VIF warning system works

### Configuration:
```json
{
  "analysisType": "regression",
  "independentVars": ["age", "bmi", "exercise_hours_per_week"],
  "dependentVar": "quality_of_life_score"
}
```

### Expected Results:
- ⚠️ VIF warning (max VIF > 10)
- ✅ Correlation heatmap shows high correlations
- ✅ Specific variables identified as problematic
- ✅ Model still runs and produces results

### What to Check:
- [ ] VIF values > 10 for correlated variables
- [ ] Warning message clear and actionable
- [ ] Correlation heatmap shows red/blue extremes
- [ ] Recommendation to remove variables

---

## Test 9: Error Handling

### Test Invalid Configurations:

**A. Nonparametric without group variable:**
```json
{
  "analysisType": "nonparametric",
  "testType": "mann-whitney",
  "dependentVar": "cholesterol"
}
```
Expected: Error message "Group variable required"

**B. Categorical with numeric variables:**
```json
{
  "analysisType": "categorical",
  "variable1": "age",
  "variable2": "bmi"
}
```
Expected: Should work but may give warning about continuous variables

**C. Multiple regression with 1 variable:**
```json
{
  "analysisType": "regression",
  "independentVars": ["age"],
  "dependentVar": "quality_of_life_score"
}
```
Expected: Should work, treated as simple regression

---

## Success Criteria

### For Each Test:
- ✅ Analysis completes without errors
- ✅ All expected plots render
- ✅ Statistical values are reasonable
- ✅ Interpretation text is accurate
- ✅ Conclusion paragraph present
- ✅ Download ZIP contains all files
- ✅ HTML report displays correctly
- ✅ Jupyter notebook is valid

### Overall:
- ✅ All 9 analysis types work
- ✅ VIF calculation accurate
- ✅ Non-parametric tests produce correct statistics
- ✅ Categorical analysis handles 2×2 and larger tables
- ✅ Error messages are helpful
- ✅ UI is intuitive for all new features

---

## Testing Order

1. **Start with Simple Regression** (baseline, should work perfectly)
2. **Test Multiple Regression** (2 variables, low VIF)
3. **Test Multiple Regression** (3 variables, high VIF)
4. **Test Mann-Whitney U** (2 groups)
5. **Test Kruskal-Wallis** (4 groups)
6. **Test Wilcoxon** (paired)
7. **Test Chi-Square** (gender × exercise_type)
8. **Test error handling** (invalid inputs)
9. **Download and verify reports** for each

---

## Quick Test Commands

### Using the UI:
1. Go to http://localhost:3000
2. Upload `health_exercise_study.csv`
3. Select analysis type from dropdown
4. Configure variables
5. Click "Run Analysis"
6. Verify results
7. Download report
8. Check ZIP contents

### Using API (Advanced):
```bash
curl -X POST http://localhost:3001/api/analyze \
  -F "file=@example-data/health_exercise_study.csv" \
  -F 'options={"analysisType":"nonparametric","testType":"mann-whitney","groupVar":"gender","dependentVar":"cholesterol"}'
```

---

## Known Issues to Watch For:

1. **VIF with highly correlated data** - Will show warnings (expected)
2. **Chi-square with small cells** - Should auto-switch to Fisher's exact
3. **Wilcoxon with identical values** - May give warnings
4. **Multiple regression interpretation** - Should mention specific significant predictors

---

## Report Back:

For each test, note:
- ✅ Pass / ❌ Fail
- Any error messages
- Unexpected behavior
- Missing features
- UI/UX issues

---

**Ready to start testing!** 🚀

Begin with Test 1 (Simple Regression) and work through the list.
