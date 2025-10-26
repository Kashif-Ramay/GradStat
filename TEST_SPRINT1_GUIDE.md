# 🧪 Sprint 1.1 Testing Guide - "I'm Not Sure" Feature

**Date:** October 24, 2025  
**Feature:** Auto-Detection for Test Advisor Questions

---

## 📁 Test Data Files Created

Located in: `gradstat/test-data/`

1. **normal-data.csv** - Should detect as normally distributed
2. **non-normal-data.csv** - Should detect as NOT normal (has outliers)
3. **paired-data.csv** - Should detect as paired/repeated measures
4. **grouped-data.csv** - Should detect 3 groups

---

## 🚀 Step 1: Start All Services

### Terminal 1: Worker (Python)
```powershell
cd c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\worker
python main.py
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

---

### Terminal 2: Backend (Node.js)
```powershell
cd c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\backend
node server.js
```

**Expected Output:**
```
✅ Directories ready
🚀 GradStat Backend API running on port 3001
```

---

### Terminal 3: Frontend (React)
```powershell
cd c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\frontend
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view gradstat-frontend in the browser.

  Local:            http://localhost:3000
```

**Browser should auto-open to:** http://localhost:3000

---

## 🧪 Test Case 1: Normal Data Detection

### Steps:
1. **Open Test Advisor**
   - Click "🧪 Test Advisor" button in header
   - You should see: "🧭 Statistical Test Advisor"

2. **Upload File**
   - Look for blue box: "💡 Pro Tip: Upload Your Data First!"
   - Click "Choose File"
   - Select: `test-data/normal-data.csv`
   - Should see green box: "✅ Data File Uploaded!"

3. **Start Wizard**
   - Click: "Compare groups"
   - Click: "2 groups"
   - Click: "Continuous" (outcome type)

4. **Test Auto-Detection**
   - Question: "Is your data normally distributed?"
   - Look for: "✨ I'm not sure - Test it for me"
   - Click it
   - Wait for loading: "⏳ Analyzing your data..."

### Expected Result:
```
🤖 Auto-Detection Result [HIGH CONFIDENCE]

✅ 4/4 variables (100%) are normally distributed 
(Shapiro-Wilk test, p > 0.05). Your data appears normal.

[View technical details ▼]
```

### Verify:
- ✅ "Yes" option is automatically selected
- ✅ Green background on result
- ✅ "HIGH CONFIDENCE" badge is green
- ✅ Can click "View technical details" to see Shapiro-Wilk results
- ✅ Can click "✕" to dismiss

---

## 🧪 Test Case 2: Non-Normal Data Detection

### Steps:
1. Click "← Back" to return to Step 1
2. Click "Change File"
3. Upload: `test-data/non-normal-data.csv`
4. Go through wizard again to normality question
5. Click "✨ I'm not sure - Test it for me"

### Expected Result:
```
🤖 Auto-Detection Result [HIGH CONFIDENCE]

❌ Only 0/4 variables (0%) are normally distributed. 
Consider non-parametric tests.

[View technical details ▼]
```

### Verify:
- ✅ "No" option is automatically selected
- ✅ Red background on result
- ✅ "HIGH CONFIDENCE" badge is red
- ✅ Technical details show low p-values

---

## 🧪 Test Case 3: Paired Data Detection

### Steps:
1. Upload: `test-data/paired-data.csv`
2. Select "Compare groups" → "2 groups" → "Continuous"
3. On normality question, select "Yes" (manually)
4. Continue to: "Are the groups independent or paired?"
5. Click "✨ I'm not sure - Test it for me"

### Expected Result:
```
🤖 Auto-Detection Result [MEDIUM CONFIDENCE]

⚠️ Detected ID and time/repeated columns - data 
appears to be paired or repeated measures

[View technical details ▼]
```

### Verify:
- ✅ "Paired" option is automatically selected
- ✅ Yellow background on result
- ✅ "MEDIUM CONFIDENCE" badge is yellow
- ✅ Technical details show detected columns

---

## 🧪 Test Case 4: Without File Upload

### Steps:
1. Refresh page (Ctrl+R)
2. Click "🧪 Test Advisor"
3. Skip file upload
4. Go to normality question
5. Try to click "✨ I'm not sure - Test it for me"

### Expected Result:
- ✅ Button should be grayed out (disabled)
- ✅ Clicking shows alert: "Please upload your data file first to use auto-detection!"

---

## 🧪 Test Case 5: Change Answer After Auto-Detection

### Steps:
1. Upload `normal-data.csv`
2. Use auto-detection on normality question
3. Result shows "Yes" is selected
4. Manually click "No" option

### Expected Result:
- ✅ Can override auto-detected answer
- ✅ "No" becomes selected
- ✅ Result box stays visible (doesn't disappear)
- ✅ Can click "✕" to dismiss result box

---

## 🧪 Test Case 6: Multiple Auto-Detections

### Steps:
1. Upload `paired-data.csv`
2. Auto-detect normality → Should say "Yes"
3. Dismiss result (click ✕)
4. Continue to paired question
5. Auto-detect paired → Should say "Paired"

### Expected Result:
- ✅ Both auto-detections work independently
- ✅ Results don't interfere with each other
- ✅ Can dismiss one without affecting the other

---

## 🧪 Test Case 7: Technical Details

### Steps:
1. Auto-detect normality with `normal-data.csv`
2. Click "View technical details"

### Expected Result:
```json
{
  "age": {
    "is_normal": true,
    "p_value": 0.234,
    "test": "Shapiro-Wilk"
  },
  "height": {
    "is_normal": true,
    "p_value": 0.456,
    "test": "Shapiro-Wilk"
  },
  ...
}
```

### Verify:
- ✅ Shows JSON with all variables
- ✅ Shows p-values
- ✅ Shows test name
- ✅ Properly formatted and readable

---

## 🐛 Common Issues & Solutions

### Issue 1: "Failed to auto-detect"
**Check:**
- Worker is running on port 8001
- Backend is running on port 3001
- No firewall blocking ports

**Solution:**
```powershell
# Check if ports are in use
netstat -ano | findstr :8001
netstat -ano | findstr :3001
```

---

### Issue 2: Button stays loading forever
**Check:**
- Browser console (F12) for errors
- Backend terminal for errors
- Worker terminal for errors

**Solution:**
- Restart worker
- Check file format is valid CSV

---

### Issue 3: Wrong detection result
**Check:**
- File has correct data
- Columns are numeric (for normality)
- File has ID/time columns (for paired)

**Solution:**
- Verify CSV format
- Check column names
- Ensure data types are correct

---

### Issue 4: File upload doesn't work
**Check:**
- File is .csv, .xlsx, or .xls
- File size is reasonable (<10MB)
- File is not corrupted

**Solution:**
- Try different file
- Check file permissions
- Verify file format

---

## 📊 Success Criteria

### Must Pass:
- ✅ File upload works
- ✅ Auto-detect button appears
- ✅ Loading state shows
- ✅ Results display correctly
- ✅ Confidence badges show right colors
- ✅ Answers auto-fill
- ✅ Can dismiss results
- ✅ Can override answers

### Should Pass:
- ✅ Normal data detected correctly
- ✅ Non-normal data detected correctly
- ✅ Paired data detected correctly
- ✅ Technical details are accurate
- ✅ No console errors
- ✅ Smooth animations
- ✅ Responsive on mobile

---

## 📸 Screenshots to Capture

1. File upload prompt (blue box)
2. File uploaded success (green box)
3. Auto-detect button
4. Loading state
5. High confidence result (green)
6. Medium confidence result (yellow)
7. Low confidence result (red)
8. Technical details expanded
9. Mobile view

---

## 🎯 Performance Benchmarks

### Target Metrics:
- **File upload:** < 1 second
- **Auto-detection:** < 3 seconds
- **UI response:** < 100ms
- **No memory leaks:** Check after 10 detections

### How to Measure:
```javascript
// In browser console
console.time('auto-detect');
// Click auto-detect button
// Wait for result
console.timeEnd('auto-detect');
```

---

## ✅ Testing Checklist

### Functionality:
- [ ] File upload works
- [ ] Auto-detect normality works
- [ ] Auto-detect paired works
- [ ] Results display correctly
- [ ] Confidence badges correct
- [ ] Technical details show
- [ ] Can dismiss results
- [ ] Can override answers
- [ ] Button disabled without file
- [ ] Error handling works

### UI/UX:
- [ ] Loading animation smooth
- [ ] Colors are correct
- [ ] Text is readable
- [ ] Buttons are clickable
- [ ] Hover effects work
- [ ] Mobile responsive
- [ ] Animations smooth
- [ ] No layout shifts

### Edge Cases:
- [ ] Empty file
- [ ] File with missing data
- [ ] File with all same values
- [ ] Very large file (1000+ rows)
- [ ] File with special characters
- [ ] Multiple rapid clicks
- [ ] Network timeout
- [ ] Server error

---

## 📝 Bug Report Template

If you find a bug, document it:

```markdown
### Bug: [Short description]

**Steps to Reproduce:**
1. 
2. 
3. 

**Expected Result:**
[What should happen]

**Actual Result:**
[What actually happened]

**Environment:**
- Browser: [Chrome/Firefox/Safari]
- OS: Windows 11
- File: [Which test file]

**Console Errors:**
[Paste any errors from F12 console]

**Screenshots:**
[Attach if relevant]

**Priority:** [High/Medium/Low]
```

---

## 🎉 When Testing is Complete

### If All Tests Pass:
1. Document any minor issues
2. Take screenshots for documentation
3. Move to Sprint 1.2 (Smart Data Pre-Analysis)

### If Issues Found:
1. Document all bugs
2. Prioritize (High/Medium/Low)
3. Fix high-priority bugs first
4. Re-test after fixes

---

## 🚀 Next Steps After Testing

### Option A: Deploy to Production
- Merge to main branch
- Deploy backend + worker
- Deploy frontend
- Monitor metrics

### Option B: Continue Development
- Move to Sprint 1.2
- Implement Smart Data Pre-Analysis
- Add more auto-detect questions

### Option C: Polish & Improve
- Add more test cases
- Improve error messages
- Add tooltips
- Create video tutorial

---

## 💡 Tips for Testing

1. **Test in order** - Follow test cases 1-7 sequentially
2. **Check console** - Keep F12 open to catch errors
3. **Take notes** - Document anything unexpected
4. **Test edge cases** - Try to break it!
5. **Test on mobile** - Responsive design matters
6. **Clear cache** - If something seems wrong, try Ctrl+Shift+R
7. **Fresh start** - Restart all services if needed

---

## 📞 Need Help?

If you encounter issues:

1. **Check logs:**
   - Worker terminal
   - Backend terminal
   - Browser console (F12)

2. **Verify setup:**
   - All services running?
   - Correct ports?
   - Files in right location?

3. **Try fresh start:**
   - Stop all services
   - Clear browser cache
   - Restart everything

---

**Ready to test! Start with Terminal 1 (Worker) and work your way through the test cases.** 🧪

**Good luck! Let me know what you find!** 🚀
