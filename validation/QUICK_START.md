# GradStat Validation - Quick Start Guide

## 🚀 5-Minute Validation

### Step 1: Run R Validation (2 minutes)

```bash
# Install R if needed: https://www.r-project.org/

# Navigate to project
cd gradstat

# Run R script
Rscript validation/r_validation.R
```

**You'll see:**
```
============================================================
GradStat R Validation - Spot Check
============================================================

Test 1: Independent Samples T-Test
-----------------------------------
t-statistic: -4.062
p-value: 0.0007

✅ Expected GradStat results:
   t = -4.062
   p = 0.0007
```

### Step 2: Test in GradStat (3 minutes)

1. **Start GradStat** (if not running)
   ```bash
   # Backend
   cd backend && node server.js
   
   # Worker
   cd worker && python main.py
   
   # Frontend
   cd frontend && npm start
   ```

2. **Test Each Dataset**

   | Test | File | Analysis Type | Expected Result |
   |------|------|---------------|-----------------|
   | T-Test | `r_ttest_independent.csv` | Group Comparison | t = -4.062, p = 0.0007 |
   | Paired T-Test | `r_ttest_paired.csv` | Group Comparison (paired) | t = -6.204, p = 0.0001 |
   | ANOVA | `r_anova_oneway.csv` | Group Comparison (3+ groups) | F = 49.16, p < 0.0001 |
   | Regression | `r_regression_linear.csv` | Find Relationships | slope = 0.5001, R² = 0.6665 |
   | Correlation | `r_correlation_pearson.csv` | Find Relationships | r = -0.868, p = 0.0011 |

3. **Upload & Compare**
   - Upload CSV from `validation/data/`
   - Run analysis
   - Compare to expected results
   - Tolerance: ±0.01 for statistics, ±0.001 for p-values

### Step 3: Verify ✅

**PASS if:**
- All 5 tests match R results within tolerance
- No systematic errors

**Example:**
```
✅ T-Test: t = -4.062 (expected: -4.062) ✓
✅ P-value: 0.0007 (expected: 0.0007) ✓
```

## 📊 Detailed Validation (Optional)

### Run Automated Python Suite

```bash
# Install dependencies
pip install pandas numpy scipy requests

# Run suite
python validation/validation_suite.py
```

**Output:**
```
============================================================
GradStat Validation Suite
============================================================

Running: Independent Samples T-Test...
  ✅ PASSED (accuracy: 100.0%)

...

Overall Accuracy: 100.0%
🎉 All tests PASSED!
```

## 🎯 What Gets Validated

### Statistical Accuracy
- ✅ T-statistics
- ✅ P-values
- ✅ F-statistics
- ✅ Correlation coefficients
- ✅ Regression coefficients
- ✅ R-squared values
- ✅ Degrees of freedom

### Against Gold Standards
- ✅ R (statistical computing)
- ✅ scipy (Python stats)
- ✅ Published literature

## 📝 Checklist

- [ ] R installed
- [ ] R validation script run
- [ ] 5 CSV files generated
- [ ] GradStat running
- [ ] All 5 tests uploaded
- [ ] Results compared
- [ ] All tests match ✅

## 🐛 Common Issues

**Issue:** R not found
```bash
# Install R: https://www.r-project.org/
# Or use package manager:
choco install r.project  # Windows
brew install r           # Mac
```

**Issue:** CSV files not found
```bash
# Check directory
ls validation/data/

# Should see:
# r_ttest_independent.csv
# r_ttest_paired.csv
# r_anova_oneway.csv
# r_regression_linear.csv
# r_correlation_pearson.csv
```

**Issue:** Results don't match
- Check tolerance (±0.01 for stats, ±0.001 for p-values)
- Verify correct analysis type selected
- Check for data upload errors

## 📈 Next Steps

After validation:

1. **Document Results**
   - Save screenshots
   - Note any discrepancies
   - Update README

2. **Add Badge to README**
   ```markdown
   ✅ **Statistically Validated** against R and scipy
   ```

3. **Marketing**
   - "Validated against R (gold standard)"
   - "100% accuracy on standard datasets"
   - "Trusted statistical results"

## 🎉 Success Criteria

**✅ VALIDATED if:**
- All R tests match GradStat results
- Accuracy ≥ 99.9%
- No systematic bias

**You can confidently say:**
> "GradStat has been validated against R and produces statistically accurate results with 99.9%+ accuracy on standard datasets."

---

**Time Required:** 5 minutes
**Difficulty:** Easy
**Prerequisites:** R installed, GradStat running
