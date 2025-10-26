# Power Analysis Test Guide 🧪

**Date:** October 22, 2025  
**Status:** Ready to Test

---

## ⚠️ IMPORTANT: Restart Worker First!

The worker is currently running the OLD code. You need to restart it:

### **Stop the worker:**
Find the terminal running the worker and press `Ctrl + C`

### **Restart the worker:**
```bash
cd C:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\worker
python main.py
```

Wait for: `INFO: Application startup complete.`

---

## 🧪 Test 1: Sample Size Calculation (EASIEST)

### **Steps:**

1. **Open:** http://localhost:3000

2. **Select Analysis Type:**
   - Click the dropdown
   - Select: **Power Analysis & Sample Size**
   - Notice: File upload section disappears! ✨

3. **Configure Parameters:**
   - Test Type: `Independent t-test (2 groups)` (default)
   - What to Calculate: `Required Sample Size` (default)
   - Effect Size: `0.5` (default - medium effect)
   - Significance Level: `0.05 (5%) - Standard` (default)
   - Desired Power: `0.80 (80%) - Standard` (default)

4. **Click "Run Analysis"**
   - No file upload needed!
   - Should take 2-3 seconds

---

### **Expected Results:**

#### **Test Results (6 cards):**
```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ TEST_TYPE       │  │ CALCULATE       │  │ RESULT_VALUE    │
│ t-test          │  │ sample_size     │  │ 64.0000         │
└─────────────────┘  └─────────────────┘  └─────────────────┘

┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ RESULT_LABEL    │  │ EFFECT_SIZE     │  │ ALPHA           │
│ Required Sample │  │ 0.5000          │  │ 0.0500          │
└─────────────────┘  └─────────────────┘  └─────────────────┘

┌─────────────────┐
│ POWER           │
│ 0.8000          │
└─────────────────┘
```

#### **2 Plots:**

1. **Power Curve**
   - Blue line showing power vs sample size
   - Red dashed line at 0.80 (power threshold)
   - Green dashed line at n=64 (required sample)
   - Green dot at intersection point
   - Title: "Power Analysis: T-TEST"

2. **Effect Size Sensitivity**
   - Red line showing sample size vs effect size
   - Green dashed line at effect size = 0.5
   - Shows how n changes with different effect sizes
   - Title: "Sample Size vs Effect Size"

#### **Interpretation:**
"Power analysis for t-test with effect size = 0.5, α = 0.05, and desired power = 0.8: You need approximately **64 participants** per group (total N = 128) to achieve 80% power."

#### **Recommendations:**
- Account for ~15-20% dropout rate: recruit 77 per group
- Consider pilot studies to better estimate effect sizes
- Higher power (0.90) recommended for critical studies
- Cohen's d: Small = 0.2, Medium = 0.5, Large = 0.8

---

## 🧪 Test 2: Power Calculation

### **Steps:**

1. **Change "What to Calculate":**
   - Select: `Statistical Power`

2. **Notice UI Changes:**
   - "Desired Power" input disappears
   - "Sample Size per Group" input appears

3. **Configure:**
   - Test Type: `Independent t-test`
   - Calculate: `Statistical Power`
   - Effect Size: `0.5`
   - Alpha: `0.05`
   - Sample Size per Group: `30`

4. **Run Analysis**

---

### **Expected Results:**

#### **Result Value:**
- Power: **~0.47** (47.1%)

#### **Interpretation:**
"Your study has **47.1% power** to detect the effect. ⚠️ This is below the conventional 80% threshold. Consider increasing sample size."

#### **Recommendations:**
- Increase sample size to ~45 per group for 80% power
- Consider reducing alpha only if you have adequate power

#### **Plot:**
- Power curve showing current position (n=30, power=0.47)
- Shows how much more n is needed to reach 0.80

---

## 🧪 Test 3: ANOVA (Multiple Groups)

### **Steps:**

1. **Change Test Type:**
   - Select: `ANOVA (3+ groups)`

2. **Notice UI Changes:**
   - "Number of Groups" input appears

3. **Configure:**
   - Test Type: `ANOVA (3+ groups)`
   - Calculate: `Required Sample Size`
   - Effect Size: `0.25` (medium for ANOVA)
   - Alpha: `0.05`
   - Power: `0.80`
   - Number of Groups: `4`

4. **Run Analysis**

---

### **Expected Results:**

#### **Result Value:**
- Sample Size per Group: **~45**
- Total N: **180** (45 × 4 groups)

#### **Interpretation:**
"You need approximately **45 participants** per group (total N = 180) to achieve 80% power."

#### **Effect Size Guide:**
- Cohen's f: Small = 0.1, Medium = 0.25, Large = 0.4

#### **Plot:**
- Power curve for ANOVA with 4 groups
- Shows steeper curve (needs more participants for multiple groups)

---

## 🧪 Test 4: Correlation

### **Steps:**

1. **Change Test Type:**
   - Select: `Correlation`

2. **Configure:**
   - Test Type: `Correlation`
   - Calculate: `Required Sample Size`
   - Effect Size: `0.3` (medium correlation)
   - Alpha: `0.05`
   - Power: `0.80`

3. **Run Analysis**

---

### **Expected Results:**

#### **Result Value:**
- Total Sample Size: **~85**

#### **Interpretation:**
"You need approximately **85 participants** to achieve 80% power."

#### **Effect Size Guide:**
- Correlation r: Small = 0.1, Medium = 0.3, Large = 0.5

#### **Plot:**
- Power curve showing total sample size (not per group)
- X-axis goes up to 500 (correlations need larger samples)

---

## 🧪 Test 5: Detectable Effect Size

### **Steps:**

1. **Change Calculate:**
   - Select: `Detectable Effect Size`

2. **Configure:**
   - Test Type: `Independent t-test`
   - Calculate: `Detectable Effect Size`
   - Sample Size per Group: `50`
   - Alpha: `0.05`
   - Power: `0.80`

3. **Run Analysis**

---

### **Expected Results:**

#### **Result Value:**
- Detectable Effect Size: **~0.57** (Cohen's d)

#### **Interpretation:**
"You can detect an effect size of **0.57** or larger. This allows detection of medium-to-large effects."

#### **Plot:**
- Effect size sensitivity showing power vs effect size
- Blue line at power = 0.80
- Shows what effects you can/cannot detect

---

## ✅ Success Checklist

### Test 1 (Sample Size):
- [ ] No file upload section shown
- [ ] Analysis runs without file
- [ ] Result value ≈ 64
- [ ] 2 plots render correctly
- [ ] Power curve has green line at n=64
- [ ] Interpretation mentions "64 participants per group"
- [ ] Recommendations include dropout adjustment

### Test 2 (Power):
- [ ] Sample size input appears
- [ ] Power input disappears
- [ ] Result value ≈ 0.47
- [ ] Warning about low power shown
- [ ] Recommendation to increase n

### Test 3 (ANOVA):
- [ ] Number of groups input appears
- [ ] Result accounts for multiple groups
- [ ] Total N = result × groups
- [ ] Effect size guide shows Cohen's f

### Test 4 (Correlation):
- [ ] Effect size guide shows r values
- [ ] Total sample size (not per group)
- [ ] Larger sample needed than t-test

### Test 5 (Effect Size):
- [ ] Both sample size and power inputs shown
- [ ] Result is effect size value
- [ ] Interpretation mentions what you can detect

### Overall:
- [ ] All 5 tests run without errors
- [ ] Plots render for all tests
- [ ] Interpretations are clear
- [ ] Recommendations are helpful
- [ ] Download report works
- [ ] UI is responsive and intuitive

---

## 🐛 Troubleshooting

### Issue: Worker not restarted
**Symptom:** Error "Unknown analysis type: power"  
**Solution:** Stop and restart worker with Ctrl+C, then `python main.py`

### Issue: File upload still showing
**Symptom:** Upload section visible for power analysis  
**Solution:** Hard refresh browser (Ctrl+F5)

### Issue: Analysis button disabled
**Symptom:** Can't click "Run Analysis"  
**Solution:** Check that all required inputs are filled

### Issue: Plots not showing
**Symptom:** Only text results, no plots  
**Solution:** Check browser console (F12) for errors

### Issue: Wrong result values
**Symptom:** Numbers don't match expected  
**Solution:** Verify input parameters match test guide

---

## 📊 Expected Performance

| Test | Execution Time | Plots | Metrics |
|------|---------------|-------|---------|
| Sample Size | 2-3 seconds | 2 | 6 |
| Power | 2-3 seconds | 2 | 6 |
| Effect Size | 2-3 seconds | 2 | 6 |
| ANOVA | 2-3 seconds | 1 | 7 |
| Correlation | 2-3 seconds | 1 | 6 |

---

## 🎯 What to Report

After testing, note:

1. **Which tests passed?** (1-5)
2. **Any errors encountered?**
3. **Plot quality?** (clear, readable, professional?)
4. **Interpretation clarity?** (easy to understand?)
5. **UI/UX feedback?** (intuitive, confusing, suggestions?)

---

## 🚀 Next Steps

### If All Tests Pass ✅:
- Mark Power Analysis as complete
- Move to Enhanced Logistic Regression
- Update coverage metrics (87% → 90%)

### If Issues Found ❌:
- Document specific errors
- Check browser console
- Check worker logs
- Report for fixing

---

**Ready to test!** Start with Test 1 and work through the list. 🎉

**Remember:** Restart the worker first! The current one is running old code.
