# 🚀 Expanded Pre-Analysis Testing Guide

## What's New in This Expansion?

Pre-analysis now supports **ALL research questions**:
- ✅ **Compare Groups** (already working)
- ✅ **Find Relationships** (NEW!)
- ✅ **Predict Outcome** (NEW!)

---

## 🔧 Setup

### IMPORTANT: Restart Worker!

The worker has new detection functions. You MUST restart it:

```powershell
# Stop current worker (Ctrl+C)

# Restart
cd c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\worker
python main.py
```

Backend and Frontend can stay running (no changes needed there).

---

## 🧪 Test 1: Backend API Test

```powershell
cd c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat
python test_all_research_questions.py
```

### Expected Output:

```
TEST: Normal Data - All Research Questions
======================================================================
Status: 200

✅ ANALYSIS SUCCESSFUL

📊 COMPARE GROUPS Answers:
  - isNormal: True (high)
  - nGroups: 2 (high)
  - isPaired: False (medium)
  - outcomeType: continuous (high)

🔗 FIND RELATIONSHIPS Answers:
  - var1Type: continuous (high)
  - var2Type: continuous (high)
  - nPredictors: 2 (high)

🎯 PREDICT OUTCOME Answers:
  - outcomeType: continuous (high)
  - nPredictors: 2 (high)

📈 SUMMARY:
  - Total Questions: 7
  - High Confidence: 6
  - Confidence Rate: 86%
  - Recommendation: Review low-confidence answers
```

---

## 🌐 Test 2: Browser UI Tests

### Test 2A: Compare Groups (Already Working)

1. Go to http://localhost:3000
2. Click "🧪 Test Advisor"
3. Upload `test-data/normal-data.csv`
4. Wait for "✅ Data File Uploaded! - 86% confidence"
5. Select "Compare groups"
6. Click Next
7. **Verify pre-filled:**
   - ✅ "2 groups" selected
   - ✅ "Continuous" selected
   - ✅ "Yes" (normal) selected
   - ✅ "Independent" selected

---

### Test 2B: Find Relationships (NEW!)

1. Upload `test-data/normal-data.csv` (if not already)
2. Select "Find relationships"
3. Click Next
4. **Verify pre-filled:**
   - ✅ "Both continuous" selected
   - ✅ "Multiple" predictors selected (if shown)

**Expected Behavior:**
- Variable types auto-selected
- Number of predictors auto-selected
- Can still override selections

---

### Test 2C: Predict Outcome (NEW!)

1. Upload `test-data/normal-data.csv` (if not already)
2. Select "Predict outcomes"
3. Click Next
4. **Verify pre-filled:**
   - ✅ "Continuous" outcome type selected
   - ✅ "Multiple" predictors selected

**Expected Behavior:**
- Outcome type auto-selected
- Number of predictors auto-selected
- Can still override selections

---

## 📊 Test Data Expectations

### normal-data.csv
```
Columns: age, height, weight, blood_pressure (all numeric)

Expected Detections:
- Compare Groups: 2 groups, continuous, normal, independent
- Find Relationships: continuous-continuous, multiple predictors
- Predict Outcome: continuous outcome, multiple predictors
```

### grouped-data.csv
```
Columns: treatment (categorical), age, score, blood_pressure (numeric)

Expected Detections:
- Compare Groups: 3 groups, continuous, normal, independent
- Find Relationships: continuous-categorical, multiple predictors
- Predict Outcome: continuous outcome, multiple predictors
```

### paired-data.csv
```
Columns: subject_id, time_point, score, blood_pressure

Expected Detections:
- Compare Groups: 2 groups, continuous, normal, PAIRED
- Find Relationships: continuous-continuous, multiple predictors
- Predict Outcome: continuous outcome, multiple predictors
```

---

## ✅ Success Criteria

### Backend Test
- [ ] All 4 datasets analyzed successfully
- [ ] Status 200 for all requests
- [ ] All 7 questions answered (4 Compare + 2 Find Rel + 2 Predict)
- [ ] Confidence levels provided for all
- [ ] Summary shows 86%+ confidence

### Frontend Test - Compare Groups
- [ ] Answers pre-filled correctly
- [ ] Can override selections
- [ ] "I'm not sure" button still works

### Frontend Test - Find Relationships
- [ ] Variable types pre-selected
- [ ] Number of predictors pre-selected
- [ ] Can change selections
- [ ] Recommendations work

### Frontend Test - Predict Outcome
- [ ] Outcome type pre-selected
- [ ] Number of predictors pre-selected
- [ ] Can change selections
- [ ] Recommendations work

---

## 🎯 What Each Research Question Gets

### Compare Groups (4 questions)
1. **isNormal** - Shapiro-Wilk test on numeric columns
2. **nGroups** - Count unique groups in categorical columns
3. **isPaired** - Detect ID + time columns
4. **outcomeType** - Detect continuous vs categorical

### Find Relationships (2-3 questions)
1. **var1Type + var2Type** - Detect variable type combinations
   - Both continuous (2+ numeric columns)
   - One continuous, one categorical (1 numeric + 1 categorical)
   - Both categorical (2+ categorical columns)
2. **nPredictors** - Count predictor variables (if continuous-continuous)

### Predict Outcome (2 questions)
1. **outcomeType** - Detect continuous vs binary outcome
2. **nPredictors** - Count predictor variables

---

## 🐛 Troubleshooting

### Issue: "No pre-filled answers for Find Relationships"
**Solution:** 
- Check browser console for errors
- Verify worker restarted with new code
- Check that var1Type and var2Type are in response

### Issue: "Wrong variable types detected"
**Solution:**
- Check dataset has expected column types
- Numeric columns should be int/float
- Categorical columns should be object/string

### Issue: "nPredictors always shows 1"
**Solution:**
- Check dataset has multiple numeric columns
- Verify ID columns are excluded (subject_id, patient_id, etc.)

---

## 📈 Performance

### Expected Timing:
- File upload: Instant
- Analysis: 2-4 seconds (slightly longer due to more detections)
- Total: < 6 seconds

### What's Being Analyzed:
1. Normality test (Shapiro-Wilk)
2. Group counting
3. Paired structure detection
4. Outcome type detection
5. **Variable type combinations** (NEW!)
6. **Predictor counting** (NEW!)

---

## 🎉 Expected Results

After successful testing, you should see:

### Backend
```
✅ 7 questions answered per dataset
✅ 86%+ confidence rate
✅ All research questions supported
```

### Frontend
```
✅ Compare Groups: 4 answers pre-filled
✅ Find Relationships: 2-3 answers pre-filled
✅ Predict Outcome: 2 answers pre-filled
✅ All answers editable
✅ Confidence rate displayed
```

---

**Restart worker and run the tests!** 🚀
