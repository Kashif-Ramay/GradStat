# 🎯 Sprint 2.3: Advanced Statistical Tests

## Goal
Expand statistical test coverage with advanced methods commonly used in graduate research.

## Features to Implement

### 1. Mixed ANOVA (Mixed Design) ⏳
**Priority:** HIGH

**Description:**
- Combines between-subjects and within-subjects factors
- Common in experimental designs with repeated measures + groups

**Use Cases:**
- Treatment groups measured over time
- Pre-test/post-test with control/experimental groups

**Implementation:**
- Worker: `analysis_functions.py` - `mixed_anova()`
- Uses: `statsmodels.stats.anova.AnovaRM` + between-subjects factor
- Returns: F-statistics, p-values, effect sizes, interaction plots

**UI:**
- Between-subjects factor (group column)
- Within-subjects factor (time/condition column)
- Subject ID column
- Dependent variable

---

### 2. ANCOVA (Analysis of Covariance) ⏳
**Priority:** HIGH

**Description:**
- ANOVA with continuous covariates
- Controls for confounding variables

**Use Cases:**
- Compare groups while controlling for baseline differences
- Adjust for age, pre-test scores, etc.

**Implementation:**
- Worker: `analysis_functions.py` - `ancova()`
- Uses: `statsmodels.formula.api.ols()` with covariates
- Returns: Adjusted means, F-statistics, p-values, covariate effects

**UI:**
- Group variable (categorical)
- Dependent variable (continuous)
- Covariates (multiple continuous variables)

---

### 3. MANOVA (Multivariate ANOVA) ⏳
**Priority:** MEDIUM

**Description:**
- ANOVA with multiple dependent variables
- Tests if groups differ on combination of outcomes

**Use Cases:**
- Multiple outcome measures (e.g., multiple test scores)
- Reduces Type I error vs. multiple ANOVAs

**Implementation:**
- Worker: `analysis_functions.py` - `manova()`
- Uses: `statsmodels.multivariate.manova.MANOVA`
- Returns: Wilks' Lambda, Pillai's trace, Roy's largest root

**UI:**
- Group variable (categorical)
- Multiple dependent variables (select multiple)

---

### 4. Repeated Measures ANOVA ⏳
**Priority:** HIGH

**Description:**
- Within-subjects ANOVA
- Same subjects measured multiple times

**Use Cases:**
- Longitudinal studies
- Before/during/after measurements

**Implementation:**
- Worker: `analysis_functions.py` - `repeated_measures_anova()`
- Uses: `statsmodels.stats.anova.AnovaRM`
- Returns: Sphericity tests, F-statistics, p-values, effect sizes

**UI:**
- Subject ID column
- Time/condition column
- Dependent variable
- Optional: Sphericity correction (Greenhouse-Geisser, Huynh-Feldt)

---

### 5. Post-hoc Tests ⏳
**Priority:** HIGH

**Description:**
- Multiple comparison tests after significant ANOVA
- Controls family-wise error rate

**Methods:**
- Tukey HSD (Honestly Significant Difference)
- Bonferroni correction
- Holm-Bonferroni
- Dunnett's test (vs. control)

**Implementation:**
- Worker: `analysis_functions.py` - `posthoc_tests()`
- Uses: `scipy.stats`, `statsmodels.stats.multicomp`
- Returns: Pairwise comparisons, adjusted p-values, confidence intervals

**UI:**
- Auto-triggered after significant ANOVA
- Method selection dropdown
- Comparison matrix display

---

### 6. Effect Sizes ⏳
**Priority:** MEDIUM

**Description:**
- Standardized measures of effect magnitude
- Essential for interpreting practical significance

**Measures:**
- Cohen's d (t-tests)
- Eta-squared (η²) - ANOVA
- Partial eta-squared (ηp²) - ANOVA with covariates
- Omega-squared (ω²) - Less biased than η²
- Hedges' g - Corrected Cohen's d for small samples

**Implementation:**
- Worker: Add to existing test functions
- Calculate automatically with each test
- Display in results

**UI:**
- Effect size badges (small/medium/large)
- Interpretation guidelines
- Visual indicators

---

## Architecture

### Backend Structure
```
worker/
  analysis_functions.py    # Add 5 new functions
  analyze.py               # Add routing for new tests
  main.py                  # Import new functions
```

### Frontend Structure
```
frontend/src/components/
  AnalysisSelector.tsx     # Add new test options
  Results.tsx              # Display new test results
  EffectSizeBadge.tsx      # New component for effect sizes
  PostHocTable.tsx         # New component for post-hoc results
```

---

## Implementation Plan

### Phase 1: Worker Functions (5-6 hours)
1. Implement `mixed_anova()` - 1.5h
2. Implement `ancova()` - 1.5h
3. Implement `manova()` - 1h
4. Implement `repeated_measures_anova()` - 1h
5. Implement `posthoc_tests()` - 1h
6. Add effect sizes to all tests - 1h

### Phase 2: Frontend Integration (2-3 hours)
1. Update `AnalysisSelector.tsx` with new options
2. Create `EffectSizeBadge.tsx` component
3. Create `PostHocTable.tsx` component
4. Update `Results.tsx` for new test types
5. Add effect size displays

### Phase 3: Testing (1-2 hours)
1. Create test datasets for each method
2. Test all new analyses
3. Verify effect size calculations
4. Browser testing

---

## Test Data Requirements

### Mixed ANOVA Dataset:
```csv
subject_id,group,time,score
1,control,pre,50
1,control,post,55
2,control,pre,52
2,control,post,58
3,treatment,pre,51
3,treatment,post,70
...
```

### ANCOVA Dataset:
```csv
subject_id,group,outcome,covariate1,covariate2
1,control,75,25,100
2,control,80,30,105
3,treatment,90,28,102
...
```

### MANOVA Dataset:
```csv
subject_id,group,outcome1,outcome2,outcome3
1,control,75,80,85
2,control,78,82,88
3,treatment,85,90,92
...
```

### Repeated Measures Dataset:
```csv
subject_id,time1,time2,time3,time4
1,50,55,60,65
2,52,58,62,68
3,48,53,59,64
...
```

---

## Effect Size Guidelines

### Cohen's d:
- Small: 0.2
- Medium: 0.5
- Large: 0.8

### Eta-squared (η²):
- Small: 0.01
- Medium: 0.06
- Large: 0.14

### Omega-squared (ω²):
- Small: 0.01
- Medium: 0.06
- Large: 0.14

---

## UI Design

### Effect Size Badge:
```
┌─────────────────────────┐
│ Effect Size: 0.65       │
│ 🟢 Medium (Cohen's d)   │
└─────────────────────────┘
```

### Post-hoc Table:
```
┌─────────────────────────────────────────┐
│ Post-hoc Tests (Tukey HSD)              │
├─────────────────────────────────────────┤
│ Comparison      │ Diff  │ p-adj │ Sig   │
├─────────────────────────────────────────┤
│ A vs B          │ 5.2   │ 0.023 │ *     │
│ A vs C          │ 8.7   │ 0.001 │ ***   │
│ B vs C          │ 3.5   │ 0.156 │ ns    │
└─────────────────────────────────────────┘
```

### ANCOVA Results:
```
┌─────────────────────────────────────────┐
│ ANCOVA Results                          │
├─────────────────────────────────────────┤
│ Group Effect:                           │
│ F(2, 47) = 12.34, p < 0.001 ***        │
│ Effect Size: ηp² = 0.34 (Large)        │
│                                         │
│ Covariates:                             │
│ • Age: F = 8.23, p = 0.006 **          │
│ • Baseline: F = 15.67, p < 0.001 ***   │
│                                         │
│ Adjusted Means:                         │
│ • Control: 72.3 (SE = 2.1)             │
│ • Treatment A: 78.5 (SE = 2.0)         │
│ • Treatment B: 81.2 (SE = 2.2)         │
└─────────────────────────────────────────┘
```

---

## Success Metrics

### Functionality:
- ✅ All 5 new tests implemented
- ✅ Effect sizes calculated for all tests
- ✅ Post-hoc tests auto-triggered
- ✅ Results display correctly

### User Experience:
- ✅ Clear test selection
- ✅ Intuitive UI for complex designs
- ✅ Effect sizes easy to interpret
- ✅ Post-hoc results clear

### Statistical Validity:
- ✅ Correct test selection logic
- ✅ Assumption checks included
- ✅ Effect sizes accurate
- ✅ Multiple comparison corrections proper

---

## Estimated Timeline

**Total: 8-10 hours**

- Phase 1 (Worker): 5-6 hours
- Phase 2 (Frontend): 2-3 hours
- Phase 3 (Testing): 1-2 hours

---

## Next Steps

1. Create test datasets
2. Implement worker functions
3. Add frontend components
4. Integrate and test

**Ready to start implementation!** 🚀
