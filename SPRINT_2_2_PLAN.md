# 🎯 Sprint 2.2: Data Quality Checks

## Goal
Enhance data validation with comprehensive quality checks and actionable recommendations.

## Features to Implement

### 1. Missing Data Analysis ⏳
**Priority:** HIGH

**Detection:**
- Count missing values per column
- Calculate missing percentage
- Identify missing patterns (MCAR, MAR, MNAR)
- Detect columns with >50% missing

**Visualization:**
- Missing data heatmap
- Bar chart of missing percentages
- Pattern visualization

**Recommendations:**
- Suggest deletion if >50% missing
- Recommend imputation methods (mean, median, mode, KNN)
- Warn about listwise deletion impact

**Implementation:**
- Worker: `data_quality.py` - `analyze_missing_data(df)`
- Frontend: Display in validation results

---

### 2. Outlier Detection ⏳
**Priority:** HIGH

**Methods:**
- IQR method (1.5 * IQR)
- Z-score method (|z| > 3)
- Isolation Forest (for multivariate)

**Detection:**
- Identify outliers per numeric column
- Count outlier percentage
- Flag extreme outliers

**Visualization:**
- Box plots with outliers highlighted
- Scatter plots for multivariate

**Recommendations:**
- Suggest removal if <5% outliers
- Recommend transformation if skewed
- Warn about impact on analysis

**Implementation:**
- Worker: `data_quality.py` - `detect_outliers(df)`
- Frontend: Display in validation results

---

### 3. Data Type Validation ⏳
**Priority:** MEDIUM

**Checks:**
- Verify numeric columns are actually numeric
- Detect dates stored as strings
- Identify categorical columns with many unique values
- Find numeric columns stored as strings

**Recommendations:**
- Suggest type conversions
- Warn about mixed types
- Recommend encoding for categoricals

**Implementation:**
- Worker: `data_quality.py` - `validate_data_types(df)`
- Frontend: Display warnings

---

### 4. Sample Size Adequacy ⏳
**Priority:** MEDIUM

**Checks:**
- Minimum sample size for analysis type
- Power analysis integration
- Group size balance check

**Recommendations:**
- Warn if n < minimum for test
- Suggest power analysis
- Recommend larger sample

**Implementation:**
- Worker: `data_quality.py` - `check_sample_size(df, analysis_type)`
- Frontend: Display in Test Advisor

---

### 5. Distribution Analysis ⏳
**Priority:** MEDIUM

**Checks:**
- Normality tests (Shapiro-Wilk, Anderson-Darling)
- Skewness and kurtosis
- Identify heavy tails

**Visualization:**
- Histograms with normal overlay
- Q-Q plots

**Recommendations:**
- Suggest transformations (log, sqrt, Box-Cox)
- Recommend non-parametric alternatives
- Warn about assumption violations

**Implementation:**
- Worker: `data_quality.py` - `analyze_distributions(df)`
- Frontend: Display in validation results

---

### 6. Correlation Warnings ⏳
**Priority:** LOW

**Checks:**
- Perfect correlations (r = 1.0)
- High multicollinearity (VIF > 10)
- Redundant variables

**Recommendations:**
- Suggest removing redundant variables
- Warn about multicollinearity
- Recommend PCA if many correlated

**Implementation:**
- Worker: `data_quality.py` - `check_correlations(df)`
- Frontend: Display warnings

---

## Architecture

### Backend Structure
```
worker/
  data_quality.py          # New file - all quality check functions
  analyze.py               # Add /data-quality endpoint
  main.py                  # Import data_quality functions
```

### Frontend Structure
```
frontend/src/components/
  DataQualityReport.tsx    # New component - display all checks
  QualityWarning.tsx       # Reusable warning component
  
frontend/src/App.tsx       # Integrate quality checks in validation
```

### Data Flow
```
1. User uploads file
2. Backend validates file
3. Worker runs quality checks
4. Returns quality report with:
   - Issues (errors, warnings, info)
   - Visualizations (base64 images)
   - Recommendations
5. Frontend displays in expandable panel
```

---

## Implementation Plan

### Phase 1: Worker Functions (3-4 hours)
1. Create `worker/data_quality.py`
2. Implement all 6 check functions
3. Create quality report aggregator
4. Add endpoint to `analyze.py`
5. Test with various datasets

### Phase 2: Frontend Integration (2-3 hours)
1. Create `DataQualityReport.tsx` component
2. Create `QualityWarning.tsx` component
3. Update validation flow in `App.tsx`
4. Add expandable quality section
5. Style with Tailwind

### Phase 3: Testing (1 hour)
1. Test with clean data (no issues)
2. Test with missing data
3. Test with outliers
4. Test with type issues
5. Test with small samples

---

## Quality Report Structure

```typescript
interface QualityReport {
  overall_score: number;  // 0-100
  issues: QualityIssue[];
  visualizations: QualityVisualization[];
  recommendations: string[];
  summary: {
    total_issues: number;
    errors: number;
    warnings: number;
    info: number;
  };
}

interface QualityIssue {
  severity: 'error' | 'warning' | 'info';
  category: 'missing' | 'outliers' | 'types' | 'sample_size' | 'distribution' | 'correlation';
  column?: string;
  message: string;
  count?: number;
  percentage?: number;
  recommendation?: string;
}

interface QualityVisualization {
  title: string;
  type: 'heatmap' | 'bar' | 'box' | 'histogram' | 'qq';
  base64: string;
  description: string;
}
```

---

## UI Design

### Validation Results Section
```
┌─────────────────────────────────────────┐
│ ✅ File Validated Successfully          │
│ 📊 30 rows × 6 columns                  │
│                                         │
│ 🔍 Data Quality: 85/100 ⚠️              │
│ ├─ 2 warnings                           │
│ └─ 1 info                               │
│                                         │
│ [View Quality Report ▼]                 │
└─────────────────────────────────────────┘

When expanded:
┌─────────────────────────────────────────┐
│ 📊 Data Quality Report                  │
│                                         │
│ ⚠️ Missing Data                         │
│ • Column 'age': 10% missing (3 values)  │
│ 💡 Recommendation: Use median imputation│
│                                         │
│ ⚠️ Outliers Detected                    │
│ • Column 'income': 2 outliers (6.7%)    │
│ 💡 Recommendation: Review extreme values│
│                                         │
│ ℹ️ Sample Size                          │
│ • n=30: Adequate for t-test (min: 20)   │
│                                         │
│ [Missing Data Heatmap]                  │
│ [Outlier Box Plots]                     │
└─────────────────────────────────────────┘
```

---

## Success Metrics

### Functionality:
- ✅ All 6 quality checks implemented
- ✅ Quality report generated for every file
- ✅ Visualizations rendered correctly
- ✅ Recommendations actionable

### User Experience:
- ✅ Quality score visible immediately
- ✅ Issues categorized by severity
- ✅ Expandable details don't clutter UI
- ✅ Recommendations clear and helpful

### Performance:
- ✅ Quality checks complete in <2 seconds
- ✅ No impact on file upload speed
- ✅ Visualizations load quickly

---

## Estimated Timeline

**Total: 6-8 hours**

- Phase 1 (Worker): 3-4 hours
- Phase 2 (Frontend): 2-3 hours
- Phase 3 (Testing): 1 hour

---

## Next Steps

1. Create `worker/data_quality.py`
2. Implement missing data analysis
3. Implement outlier detection
4. Add other quality checks
5. Create frontend components
6. Integrate and test

**Ready to start implementation!** 🚀
