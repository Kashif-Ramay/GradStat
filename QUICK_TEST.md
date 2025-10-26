# ⚡ Quick Test - Phase 3 Components

> **5-minute test to verify everything works**

---

## 🚀 Start Services

### Terminal 1: Worker
```bash
cd worker
python main.py
```
✅ Wait for: `Uvicorn running on http://0.0.0.0:8001`

### Terminal 2: Backend
```bash
cd backend
node server.js
```
✅ Wait for: `Backend server running on port 3001`

### Terminal 3: Frontend
```bash
cd frontend
npm start
```
✅ Wait for: Browser opens at `http://localhost:3000`

---

## 🧪 Quick Test (5 minutes)

### Test 1: Upload & Analyze (2 min)

1. **Upload:** `test-data/small_sample.csv`
2. **Select:** Independent t-test
3. **Dependent:** outcome
4. **Group:** group
5. **Click:** Analyze

### Test 2: Check Results (3 min)

**Scroll through results and verify:**

#### ⚠️ CommonMistakes (Top of results)
```
Expected: Yellow warning box
⚠️ Small Sample Size
Your sample size (n=15) is small...
💡 How to fix: Consider collecting more data...
```
- [ ] Warning appears
- [ ] Yellow background
- [ ] Fix suggestion shows

---

#### 💡 InterpretationHelper (After warnings)
```
Expected: Purple gradient box
📊 Results Interpretation
Statistical Significance: ✓ or ✗
Effect Size: small/medium/large
What This Means: ...
📄 APA Format: ...
```
- [ ] Purple gradient background
- [ ] Statistical significance section
- [ ] Effect size interpretation
- [ ] APA format box
- [ ] Copy buttons work

---

#### ✓ AssumptionChecker (After interpretation)
```
Expected: Green/red cards
✓ Normality: Passed
✓ Equal Variances: Passed
✅ All assumptions met
```
- [ ] Overall status banner
- [ ] Individual assumption cards
- [ ] ✓ or ✗ icons
- [ ] Statistical details (p-values)
- [ ] If failed: Remediation box appears
- [ ] Educational note at bottom

---

#### 📊 Test Results (Middle)
```
Expected: Blue gradient box with statistics
t-statistic: ...
p-value: ...
Cohen's d: ...
```
- [ ] Statistics display correctly
- [ ] Values formatted properly

---

#### 📈 Visualizations (After test results)
```
Expected: Interactive Plotly charts
Box plots, scatter plots, etc.
```
- [ ] Charts render
- [ ] Interactive (zoom, pan, hover)
- [ ] Export button works

---

#### 💡 BestPractices (After visualizations)
```
Expected: Indigo/purple panel (collapsed)
💡 Best Practices & Recommendations
▶ Show
```
- [ ] Panel appears
- [ ] Click "▶ Show" to expand
- [ ] Do's section (green)
- [ ] Don'ts section (red)
- [ ] Pro Tips section (blue)
- [ ] Reporting Guidelines section (purple)

---

## ✅ Success Checklist

### Visual Check:
- [ ] No console errors (F12 → Console)
- [ ] All components render
- [ ] Colors look good
- [ ] Text is readable
- [ ] Icons display (✓, ✗, ⚠️, 💡)

### Functionality Check:
- [ ] CommonMistakes warnings appear
- [ ] InterpretationHelper shows results
- [ ] AssumptionChecker displays assumptions
- [ ] BestPractices expands/collapses
- [ ] Copy buttons work (click and see "✓ Copied!")

### Content Check:
- [ ] Warnings are appropriate
- [ ] Interpretations make sense
- [ ] Assumptions are correct
- [ ] Best practices are relevant
- [ ] Fix suggestions are helpful

---

## 🐛 If Something's Wrong

### Check Console (F12):
- Look for red error messages
- Note the component name
- Copy error message

### Common Issues:

**Components don't appear:**
- Check if `resultMeta` has data
- Verify imports in Results.tsx
- Check browser console for errors

**Styling looks wrong:**
- Clear browser cache (Ctrl+Shift+R)
- Check Tailwind classes
- Verify gradient backgrounds

**Copy buttons don't work:**
- Check browser permissions
- Try in different browser
- Check console for errors

---

## 📱 Mobile Test (Optional - 2 min)

1. Open DevTools (F12)
2. Click device toolbar icon (Ctrl+Shift+M)
3. Select "iPhone 12 Pro"
4. Scroll through results
5. Verify:
   - [ ] Components stack vertically
   - [ ] Text is readable
   - [ ] Buttons are tappable
   - [ ] No horizontal scroll

---

## 🎉 Test Complete!

### If all checks pass:
✅ **Phase 3 is working perfectly!**
✅ **Ready for production!**

### If issues found:
📝 **Document the issue**
🐛 **Report in chat**
🔧 **We'll fix immediately**

---

**Total Time:** 5-10 minutes  
**Difficulty:** Easy  
**Importance:** Critical

---

<div align="center">

**Let's make sure everything works! 🚀**

</div>
