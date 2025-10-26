# 🧪 Phase 3 Testing Guide

> **Comprehensive testing checklist for AssumptionChecker, BestPractices, and CommonMistakes**

---

## 🎯 Testing Objectives

1. Verify all Phase 3 components render correctly
2. Check that warnings appear when appropriate
3. Confirm best practices show for each analysis type
4. Test assumption checker with remediation suggestions
5. Ensure mobile responsiveness

---

## 📝 Test Scenarios

### Test 1: Small Sample Warning (CommonMistakes)

**Goal:** Trigger small sample size warning

**Steps:**
1. Create a small dataset (10-15 rows)
2. Upload to GradStat
3. Run Independent t-test
4. **Expected:** Yellow warning box at top of results

**What to look for:**
```
⚠️ Small Sample Size
Your sample size (n=15) is small. Results may be less reliable.
💡 How to fix: Consider collecting more data or using 
non-parametric tests.
```

**Test Data (save as `small_sample.csv`):**
```csv
group,outcome
control,75
control,78
control,72
control,80
control,76
treatment,85
treatment,88
treatment,82
treatment,90
treatment,87
control,74
control,79
treatment,86
treatment,84
treatment,89
```

---

### Test 2: Assumption Violations (AssumptionChecker)

**Goal:** See remediation suggestions for violated assumptions

**Steps:**
1. Upload dataset with non-normal data
2. Run Independent t-test
3. **Expected:** Red assumption card with remediation box

**What to look for:**
```
✗ Normality
Data is not normally distributed (p < .05)

💡 What to do:
• Use Mann-Whitney U test (non-parametric alternative)
• Transform your data (log, square root, Box-Cox)
• Increase sample size
• Remove outliers if they are data errors
```

**Test Data (save as `non_normal.csv`):**
```csv
group,outcome
A,10
A,12
A,11
A,13
A,15
A,95
B,20
B,22
B,21
B,23
B,25
B,98
```

---

### Test 3: Best Practices Panel (BestPractices)

**Goal:** Verify best practices show for different analyses

**Steps:**
1. Upload any dataset
2. Run different analysis types
3. Click "▶ Show" on Best Practices panel
4. **Expected:** Do's, Don'ts, Tips, and Reporting sections

**What to look for:**

**For t-test:**
```
✓ Do's:
- Check normality assumption
- Report Cohen's d for effect size
- Use Welch's t-test if variances unequal

✗ Don'ts:
- Don't rely solely on p-values
- Don't use t-test with severely non-normal data

💡 Pro Tips:
- Sample size of 30+ helps with normality
- Visualize data with box plots

📝 Reporting Guidelines:
Example: "t(28) = 3.45, p = .002, d = 0.92"
```

---

### Test 4: Interpretation Helper

**Goal:** Verify plain-language interpretations appear

**Steps:**
1. Upload dataset
2. Run any statistical test
3. **Expected:** Purple gradient box with interpretation

**What to look for:**
```
📊 Results Interpretation

Statistical Significance:
✓ The results are statistically significant (p = .023)

Effect Size:
The effect size (d = 0.65) is medium, suggesting a 
moderate practical difference.

What This Means:
Your results show a meaningful difference between groups...
```

---

### Test 5: All Components Together

**Goal:** See all Phase 3 components in one analysis

**Steps:**
1. Upload `example-data/health-study.csv` (or create one)
2. Run Independent t-test
3. Scroll through results

**Expected Order:**
1. ⚠️ **CommonMistakes** (if any issues)
2. 💡 **InterpretationHelper** (purple gradient box)
3. ✓ **AssumptionChecker** (green/red cards)
4. 📊 **Test Results** (statistics)
5. 📈 **Visualizations** (Plotly charts)
6. 💡 **BestPractices** (expandable panel)
7. **Recommendations**
8. **Download**

---

## 🎨 Visual Testing Checklist

### CommonMistakes Component:
- [ ] Red boxes for errors (🚫)
- [ ] Yellow boxes for warnings (⚠️)
- [ ] Blue boxes for info (ℹ️)
- [ ] Fix suggestions in colored sub-boxes
- [ ] Clear, readable text

### InterpretationHelper Component:
- [ ] Purple gradient background
- [ ] Statistical significance section with ✓/✗
- [ ] Effect size interpretation
- [ ] "What This Means" section
- [ ] APA format box (white background)
- [ ] Copy buttons work (📋 and 📄)
- [ ] "✓ Copied!" feedback appears

### AssumptionChecker Component:
- [ ] Overall status banner (green or yellow)
- [ ] Individual assumption cards (green = pass, red = fail)
- [ ] ✓ and ✗ icons
- [ ] Statistical details (p-values, statistics)
- [ ] Remediation boxes for failed assumptions
- [ ] Educational note at bottom (blue box)

### BestPractices Component:
- [ ] Indigo/purple gradient background
- [ ] Expandable/collapsible (▶/▼)
- [ ] Do's section (green border)
- [ ] Don'ts section (red border)
- [ ] Pro Tips section (blue border)
- [ ] Reporting Guidelines section (purple border)
- [ ] Checkmarks and X marks visible

---

## 🔍 Detailed Test Cases

### Test Case 1: t-test with Good Data

**File:** `good_data.csv`
```csv
subject_id,group,outcome
1,control,75
2,control,78
3,control,72
4,control,80
5,control,76
6,control,74
7,control,79
8,control,77
9,control,73
10,control,81
11,control,75
12,control,78
13,control,76
14,control,74
15,control,77
16,treatment,85
17,treatment,88
18,treatment,82
19,treatment,90
20,treatment,87
21,treatment,86
22,treatment,84
23,treatment,89
24,treatment,83
25,treatment,91
26,treatment,85
27,treatment,88
28,treatment,86
29,treatment,84
30,treatment,87
```

**Expected Results:**
- ✅ No CommonMistakes warnings (n=30, good size)
- ✅ InterpretationHelper shows results
- ✅ AssumptionChecker: All green (normality passed)
- ✅ BestPractices: t-test specific guidance

---

### Test Case 2: ANOVA with 3 Groups

**File:** `anova_data.csv`
```csv
group,score
A,75
A,78
A,72
A,80
A,76
A,74
A,79
A,77
A,73
A,81
B,85
B,88
B,82
B,90
B,87
B,86
B,84
B,89
B,83
B,91
C,65
C,68
C,62
C,70
C,66
C,64
C,69
C,67
C,63
C,71
```

**Expected Results:**
- ✅ InterpretationHelper with ANOVA results
- ✅ AssumptionChecker for ANOVA assumptions
- ✅ BestPractices: ANOVA-specific (post-hoc tests, eta-squared)

---

### Test Case 3: Regression with Multiple Predictors

**File:** `regression_data.csv`
```csv
outcome,predictor1,predictor2,predictor3
75,10,5,2
78,12,6,3
72,8,4,1
80,14,7,4
76,11,5,2
85,15,8,5
88,17,9,6
82,13,7,4
90,19,10,7
87,16,8,5
```

**Expected Results:**
- ⚠️ CommonMistakes: "Too many predictors for sample size"
- ✅ InterpretationHelper with R² interpretation
- ✅ AssumptionChecker: Linearity, homoscedasticity
- ✅ BestPractices: Regression-specific (VIF, multicollinearity)

---

### Test Case 4: Correlation Analysis

**File:** `correlation_data.csv`
```csv
variable1,variable2
10,20
12,24
8,16
14,28
11,22
15,30
17,34
13,26
19,38
16,32
```

**Expected Results:**
- ✅ InterpretationHelper: Correlation strength interpretation
- ✅ BestPractices: Correlation-specific (causation warning)

---

## 📱 Mobile Responsiveness Test

### Desktop (1920x1080):
- [ ] All components visible
- [ ] No horizontal scrolling
- [ ] Text readable
- [ ] Buttons clickable

### Tablet (768x1024):
- [ ] Components stack properly
- [ ] Text still readable
- [ ] Buttons accessible
- [ ] No overflow

### Mobile (375x667):
- [ ] Single column layout
- [ ] All content accessible
- [ ] Buttons large enough to tap
- [ ] No text cutoff

**How to test:**
1. Open browser DevTools (F12)
2. Click device toolbar icon
3. Select different devices
4. Scroll through results

---

## 🐛 Bug Checklist

### Things to Watch For:

- [ ] Components render without errors
- [ ] No console errors (F12 → Console)
- [ ] No TypeScript errors
- [ ] All text displays correctly
- [ ] Colors are accessible (sufficient contrast)
- [ ] Icons display properly (✓, ✗, ⚠️, 💡, etc.)
- [ ] Copy buttons work
- [ ] Expand/collapse works
- [ ] Remediation boxes appear for failed assumptions
- [ ] Best practices show for all analysis types

### Common Issues to Check:

1. **Missing Props:**
   - Check if `resultMeta.analysis_type` exists
   - Check if `resultMeta.test_results` exists
   - Check if `resultMeta.assumptions` exists

2. **Styling Issues:**
   - Gradient backgrounds render
   - Borders show correctly
   - Colors are consistent
   - Spacing looks good

3. **Functionality:**
   - Expand/collapse toggles
   - Copy to clipboard works
   - Tooltips appear on hover
   - Links open correctly

---

## ✅ Success Criteria

### Phase 3 is successful if:

1. **CommonMistakes:**
   - ✅ Warnings appear for small samples
   - ✅ Errors appear for critical issues
   - ✅ Fix suggestions are helpful
   - ✅ Severity levels are appropriate

2. **InterpretationHelper:**
   - ✅ Plain-language explanations appear
   - ✅ Statistical significance clearly indicated
   - ✅ Effect sizes interpreted correctly
   - ✅ APA format is correct
   - ✅ Copy buttons work

3. **AssumptionChecker:**
   - ✅ All assumptions displayed
   - ✅ Pass/fail clearly indicated
   - ✅ Remediation suggestions appear
   - ✅ Statistical details shown
   - ✅ Educational note helpful

4. **BestPractices:**
   - ✅ Analysis-specific guidance
   - ✅ Do's and don'ts clear
   - ✅ Pro tips valuable
   - ✅ Reporting guidelines with examples
   - ✅ Expand/collapse works

5. **Overall:**
   - ✅ No console errors
   - ✅ Components integrate smoothly
   - ✅ User experience is enhanced
   - ✅ Educational value is high
   - ✅ Mobile responsive

---

## 📊 Test Results Template

**Date:** ___________  
**Tester:** ___________

### Test 1: Small Sample Warning
- [ ] Pass
- [ ] Fail
- Notes: ___________

### Test 2: Assumption Violations
- [ ] Pass
- [ ] Fail
- Notes: ___________

### Test 3: Best Practices Panel
- [ ] Pass
- [ ] Fail
- Notes: ___________

### Test 4: Interpretation Helper
- [ ] Pass
- [ ] Fail
- Notes: ___________

### Test 5: All Components Together
- [ ] Pass
- [ ] Fail
- Notes: ___________

### Mobile Responsiveness
- [ ] Pass
- [ ] Fail
- Notes: ___________

### Overall Assessment
- [ ] Ready for production
- [ ] Needs minor fixes
- [ ] Needs major fixes

**Issues Found:**
1. ___________
2. ___________
3. ___________

**Recommendations:**
1. ___________
2. ___________
3. ___________

---

## 🚀 Quick Start Testing

**Fastest way to test everything:**

1. Start all services
2. Upload `example-data/health-study.csv`
3. Run Independent t-test
4. Scroll through results and verify:
   - ⚠️ CommonMistakes (if any)
   - 💡 InterpretationHelper
   - ✓ AssumptionChecker
   - 📊 Test Results
   - 📈 Visualizations
   - 💡 BestPractices (click to expand)
5. Check console for errors (F12)
6. Test on mobile (DevTools → Device Toolbar)

**Expected time:** 5-10 minutes

---

<div align="center">

**Happy Testing! 🧪**

Report any issues and we'll fix them immediately!

</div>
