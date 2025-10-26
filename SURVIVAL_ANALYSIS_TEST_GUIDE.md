# 🧪 Survival Analysis - Complete Test Guide

## ⚠️ IMPORTANT: Cox Regression Requires Covariates!

**Cox regression and the Hazard Ratios plot ONLY appear if you select covariates!**

---

## 📊 Test Scenarios

### **Scenario 1: Basic Kaplan-Meier (Overall Survival)**

**Configuration:**
- Duration Column: `time_months`
- Event Column: `event`
- Group Column: `None (overall survival)`
- Covariates: `None`

**Expected Results:**
- ✅ Summary statistics (n_subjects, n_events, n_censored, event_rate, median_survival)
- ✅ 2 plots: Kaplan-Meier curve, Cumulative Hazard
- ❌ NO Log-Rank test (no groups)
- ❌ NO Cox regression (no covariates)
- ❌ NO Hazard Ratios plot (no covariates)

---

### **Scenario 2: Group Comparison (with Log-Rank Test)**

**Configuration:**
- Duration Column: `time_months`
- Event Column: `event`
- Group Column: `treatment` ← **SELECT THIS**
- Covariates: `None`

**Expected Results:**
- ✅ Summary statistics
- ✅ Group statistics (per-group n, events, median survival)
- ✅ **Log-Rank Test** (test statistic, p-value, significance)
- ✅ 2 plots: Kaplan-Meier curves by group, Cumulative Hazard by group
- ❌ NO Cox regression (no covariates)
- ❌ NO Hazard Ratios plot (no covariates)

---

### **Scenario 3: Cox Regression (Multivariate Analysis)** ⭐ FULL ANALYSIS

**Configuration:**
- Duration Column: `time_months`
- Event Column: `event`
- Group Column: `treatment` (optional)
- Covariates: **SELECT MULTIPLE** ← **CRITICAL!**
  - Hold `Ctrl` (Windows) or `Cmd` (Mac)
  - Click: `age`, `tumor_size`, `lymph_nodes`

**Expected Results:**
- ✅ Summary statistics
- ✅ Group statistics (if group selected)
- ✅ Log-Rank Test (if group selected)
- ✅ **Cox Regression Metrics** (C-index, Log-Likelihood, AIC)
- ✅ **Hazard Ratios Table** (HR, 95% CI, p-values, effect direction)
- ✅ **3 plots**: Kaplan-Meier, **Hazard Ratios Forest Plot**, Cumulative Hazard

---

## 🎯 Step-by-Step Test Instructions

### **Step 1: Refresh Browser**
```
Press: Ctrl + F5
```

### **Step 2: Upload Dataset**
1. Go to: http://localhost:3000
2. Upload: `gradstat/example-data/cancer_survival.csv`
3. Click: "Validate Data"

### **Step 3: Configure Analysis**
1. **Analysis Type:** "Survival Analysis (Kaplan-Meier, Cox)"
2. **Duration Column:** `time_months`
3. **Event Column:** `event`
4. **Group Column:** `treatment` (optional - for Log-Rank test)
5. **Covariates:** ⚠️ **HOLD CTRL AND SELECT MULTIPLE:**
   - `age`
   - `tumor_size`
   - `lymph_nodes`
6. Verify it shows: "Selected: 3 covariate(s)"

### **Step 4: Run Analysis**
Click: "🚀 Run Analysis"

---

## ✅ Expected Display (Full Analysis with Covariates)

### **Summary Section:**
```
Summary
Survival Analysis: 100 subjects, 51 events
```

### **Statistical Test Results:**

**Summary Statistics Cards:**
```
┌─────────────────────┬──────────────────┬─────────────────┐
│ Number of Subjects  │ Number of Events │ Number Censored │
│       100           │        51        │       49        │
├─────────────────────┼──────────────────┼─────────────────┤
│    Event Rate       │ Median Survival Time              │
│      51.0%          │       24.5                        │
└─────────────────────┴───────────────────────────────────┘
```

**Log-Rank Test** (if group selected):
```
┌──────────────────────┬─────────────────┬──────────────────┐
│ Log-Rank Statistic   │ Log-Rank P-value│ Group Comparison │
│       4.52           │     0.0335      │ ✅ Significantly │
│                      │                 │    Different     │
└──────────────────────┴─────────────────┴──────────────────┘
```

**Cox Regression Metrics:**
```
┌─────────────────────┬──────────────────┬─────────────────┐
│ Concordance Index   │ Log-Likelihood   │      AIC        │
│      0.7200         │     -145.3       │     296.6       │
└─────────────────────┴──────────────────┴─────────────────┘
```

**⚕️ Cox Regression - Hazard Ratios Table:**
```
┌────────────┬──────────┬─────────────┬─────────┬──────────────────┐
│ Covariate  │    HR    │   95% CI    │ P-value │      Effect      │
├────────────┼──────────┼─────────────┼─────────┼──────────────────┤
│    age     │  1.0500  │ (1.02-1.08) │ 0.0010* │ ⬆️ Increases Risk │
│ tumor_size │  1.2300  │ (1.10-1.38) │ 0.0002* │ ⬆️ Increases Risk │
│lymph_nodes │  1.1500  │ (1.05-1.26) │ 0.0030* │ ⬆️ Increases Risk │
└────────────┴──────────┴─────────────┴─────────┴──────────────────┘
* Significant at α = 0.05 | HR > 1: Increased hazard | HR < 1: Decreased hazard
```

### **Visualizations:**

**3 Plots:**
1. ✅ **Kaplan-Meier Survival Curve** (or by group if group selected)
2. ✅ **Hazard Ratios (Cox Regression)** ← Forest plot with confidence intervals
3. ✅ **Cumulative Hazard**

---

## 🔍 Troubleshooting

### **Problem: No Cox Regression Metrics**
**Solution:** You MUST select covariates!
- Hold Ctrl/Cmd
- Click multiple variables in the "Covariates" box
- Verify "Selected: X covariate(s)" appears

### **Problem: No Hazard Ratios Plot**
**Solution:** Same as above - select covariates!

### **Problem: No Log-Rank Test**
**Solution:** Select a group column (e.g., `treatment`, `stage`)

### **Problem: Only 2 plots instead of 3**
**Solution:** The 3rd plot (Hazard Ratios) only appears with covariates

---

## 📝 Dataset Information

**File:** `cancer_survival.csv`
**Rows:** 100 patients
**Columns:**
- `time_months` - Survival time (duration)
- `event` - Event indicator (1=death, 0=censored)
- `treatment` - Treatment group (0=control, 1=treatment)
- `stage` - Cancer stage (1-4)
- `age` - Patient age
- `tumor_size` - Tumor size (cm)
- `lymph_nodes` - Number of affected lymph nodes
- `gender` - Gender (0=female, 1=male)

---

## ✅ Success Criteria

You should see:
- ✅ 5-6 summary statistic cards
- ✅ Log-Rank test results (if group selected)
- ✅ Cox regression C-index, AIC (if covariates selected)
- ✅ Hazard ratios table with HR, CI, p-values (if covariates selected)
- ✅ 3 plots (2 without covariates, 3 with covariates)
- ✅ Interpretation text
- ✅ Recommendations

---

## 🎯 Key Takeaway

**Cox Regression = Covariates Required!**

Without covariates:
- Basic survival analysis only
- 2 plots

With covariates:
- Full multivariate analysis
- Hazard ratios
- 3 plots including forest plot

**Test with covariates to see the complete analysis!**
