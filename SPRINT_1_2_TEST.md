# 🚀 Sprint 1.2: Smart Data Pre-Analysis - Testing Guide

## What's New?

**Smart Pre-Analysis** automatically analyzes your entire dataset when you upload it and pre-fills ALL wizard answers!

### Before (Sprint 1.1):
- Upload file
- Click "I'm not sure" on EACH question
- Wait for each individual analysis
- 4 separate API calls

### After (Sprint 1.2):
- Upload file
- **ONE automatic analysis** runs in background
- **ALL answers pre-filled** instantly
- User can still override any answer
- 1 API call total

---

## 🔧 Setup

### 1. Restart Worker (REQUIRED)
```powershell
# Stop current worker (Ctrl+C in worker terminal)

# Restart with new code
cd c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\worker
python main.py
```

### 2. Restart Backend (REQUIRED)
```powershell
# Stop current backend (Ctrl+C in backend terminal)

# Restart with new code
cd c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\backend
node server.js
```

### 3. Restart Frontend (REQUIRED)
```powershell
# Stop current frontend (Ctrl+C in frontend terminal)

# Restart
cd c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\frontend
npm start
```

---

## 🧪 Test 1: Backend API Test

```powershell
cd c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat
python test_comprehensive_analysis.py
```

### Expected Output:
```
TEST: Normal Data - All Questions
============================================================
Status: 200

✅ ANALYSIS SUCCESSFUL

Answers:
  - isNormal: True (high confidence)
  - nGroups: 2 (high confidence)
  - isPaired: False (medium confidence)
  - outcomeType: continuous (high confidence)

Summary:
  - Total Questions: 4
  - High Confidence: 3
  - Confidence Rate: 75%
  - Recommendation: Review low-confidence answers
```

---

## 🌐 Test 2: Browser UI Test

### Step 1: Open Test Advisor
1. Go to http://localhost:3000
2. Click **"🧪 Test Advisor"**

### Step 2: Upload File
1. See blue "💡 Pro Tip" box
2. Click file input
3. Select `test-data/normal-data.csv`
4. **Watch the magic!** ⏳

### Expected Behavior:
```
⏳ Analyzing Your Data...
normal-data.csv - Running smart pre-analysis...
```

Then (after 1-2 seconds):
```
✅ Data File Uploaded!
normal-data.csv - 75% confidence
```

### Step 3: Check Pre-Filled Answers
1. Select research question: "Compare groups"
2. Click Next
3. **Check if answers are pre-filled:**
   - "How many groups?" → Should show "2 groups" selected
   - "What type of outcome?" → Should show "Continuous" selected
   - "Is your data normally distributed?" → Should show "Yes" selected
   - "Are the groups independent or paired?" → Should show "Independent" selected

### Step 4: Verify You Can Override
1. Click different answer (e.g., "3+ groups")
2. Should work normally
3. Pre-filled answers are just suggestions!

---

## 📊 Test 3: Different Datasets

Try with different test files:

### Normal Data (test-data/normal-data.csv)
**Expected:**
- isNormal: ✅ True
- nGroups: 2
- isPaired: ❌ False
- outcomeType: continuous

### Non-Normal Data (test-data/non-normal-data.csv)
**Expected:**
- isNormal: ❌ False
- nGroups: 2
- isPaired: ❌ False
- outcomeType: continuous

### Paired Data (test-data/paired-data.csv)
**Expected:**
- isNormal: ✅ True
- nGroups: 2
- isPaired: ✅ True
- outcomeType: continuous

### Grouped Data (test-data/grouped-data.csv)
**Expected:**
- isNormal: ✅ True
- nGroups: 3
- isPaired: ❌ False
- outcomeType: continuous

---

## 🎯 Success Criteria

### ✅ Backend Test
- [ ] All 4 datasets analyzed successfully
- [ ] Status 200 for all requests
- [ ] All 4 questions answered
- [ ] Confidence levels provided
- [ ] Summary generated

### ✅ Frontend Test
- [ ] File upload triggers analysis
- [ ] Loading state shows "⏳ Analyzing Your Data..."
- [ ] Success state shows "✅ Data File Uploaded!"
- [ ] Confidence rate displayed (e.g., "75% confidence")
- [ ] Answers pre-filled in wizard
- [ ] User can still override answers
- [ ] "I'm not sure" button still works

---

## 🐛 Troubleshooting

### Issue: "500 Internal Server Error"
**Solution:** Restart worker with new code

### Issue: Answers not pre-filled
**Solution:** 
1. Check browser console for errors
2. Check backend logs
3. Verify file uploaded successfully

### Issue: "Analyzing..." never completes
**Solution:**
1. Check worker logs for errors
2. Verify worker is running on port 8001
3. Check backend can reach worker

---

## 📈 Performance

### Expected Timing:
- File upload: Instant
- Analysis: 1-3 seconds
- Total: < 5 seconds

### What's Being Analyzed:
1. Normality test (Shapiro-Wilk on all numeric columns)
2. Group detection (categorical column analysis)
3. Paired structure detection (ID/time column patterns)
4. Outcome type detection (numeric vs categorical)

---

## 🎉 Next Steps

Once all tests pass:
1. ✅ Sprint 1.2 Complete!
2. 📝 Document the feature
3. 🎨 Polish UI/UX
4. 🚀 Consider Sprint 1.3 features

---

**Run the tests and report results!** 🧪
