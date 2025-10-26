# 🔧 Test Advisor Troubleshooting Guide

## Issue: 404 Error on `/test-advisor/recommend`

### **Root Cause:**
The worker endpoint is returning 404, which means either:
1. Worker server isn't running
2. Endpoint isn't registered properly
3. Import error in worker

---

## ✅ Quick Fix Steps

### **Step 1: Restart Worker Server**
```bash
cd worker
python main.py
```

**Look for these lines in output:**
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8001
```

### **Step 2: Test Endpoint Directly**

**Open browser:**
```
http://localhost:8001/docs
```

**Look for:**
- "Test Advisor" section in Swagger UI
- `/test-advisor/recommend` endpoint
- `/test-advisor/auto-detect` endpoint

**If you see them:** ✅ Worker is working!  
**If you don't see them:** ❌ Import error - see Step 3

### **Step 3: Check for Import Errors**

**Test imports manually:**
```bash
cd worker
python
```

```python
>>> from test_advisor import recommend_test
>>> from test_library import TEST_LIBRARY
>>> print("Imports successful!")
>>> 
>>> # Test recommendation
>>> answers = {
...     'researchQuestion': 'compare_groups',
...     'nGroups': 2,
...     'outcomeType': 'continuous',
...     'isNormal': True,
...     'isPaired': False
... }
>>> result = recommend_test(answers)
>>> print(f"Got {len(result)} recommendations")
>>> print(result[0]['test_name'])
```

**Expected output:**
```
Imports successful!
Got 2 recommendations
Independent t-test
```

### **Step 4: Test via curl**

```bash
curl -X POST http://localhost:8001/test-advisor/recommend \
  -H "Content-Type: application/json" \
  -d '{"researchQuestion":"compare_groups","nGroups":2,"outcomeType":"continuous","isNormal":true,"isPaired":false}'
```

**Expected response:**
```json
{
  "ok": true,
  "recommendations": [
    {
      "test_name": "Independent t-test",
      "confidence": "high",
      ...
    }
  ]
}
```

---

## 🐛 Common Issues

### **Issue 1: Import Error**
**Symptom:** Worker starts but endpoint missing  
**Cause:** `test_advisor.py` or `test_library.py` has syntax error  
**Fix:** Check worker logs for import errors

### **Issue 2: Worker Not Running**
**Symptom:** Connection refused  
**Cause:** Worker server not started  
**Fix:** `cd worker && python main.py`

### **Issue 3: Port Conflict**
**Symptom:** Address already in use  
**Cause:** Another process on port 8001  
**Fix:** Kill process or change port

### **Issue 4: Backend Not Proxying**
**Symptom:** Backend returns 404  
**Cause:** Backend server needs restart  
**Fix:** Restart backend: `cd backend && node server.js`

---

## 🔍 Debug Checklist

- [ ] Worker server running on port 8001
- [ ] Backend server running on port 3001
- [ ] Frontend running on port 3000
- [ ] `/test-advisor/recommend` visible in Swagger UI
- [ ] Can test endpoint via curl
- [ ] No import errors in worker logs
- [ ] Backend logs show proxy request

---

## 🚀 Quick Test Script

**Save as `test_advisor_check.py` in worker folder:**

```python
#!/usr/bin/env python3
"""Quick test for Test Advisor functionality"""

import sys
sys.path.insert(0, '.')

try:
    from test_advisor import recommend_test
    from test_library import TEST_LIBRARY
    print("✅ Imports successful!")
    
    # Test recommendation
    answers = {
        'researchQuestion': 'compare_groups',
        'nGroups': 2,
        'outcomeType': 'continuous',
        'isNormal': True,
        'isPaired': False
    }
    
    result = recommend_test(answers)
    print(f"✅ Got {len(result)} recommendations")
    print(f"✅ First test: {result[0]['test_name']}")
    print(f"✅ Confidence: {result[0]['confidence']}")
    
    print("\n🎉 Test Advisor is working correctly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
```

**Run:**
```bash
cd worker
python test_advisor_check.py
```

---

## 📝 Expected Behavior

### **After clicking "Compare groups":**
1. Frontend sends POST to `/api/test-advisor/recommend`
2. Backend proxies to `http://localhost:8001/test-advisor/recommend`
3. Worker processes request
4. Returns recommendations
5. Frontend displays results

### **Console logs should show:**
```
Frontend: Sending answers: {researchQuestion: "compare_groups", ...}
Backend: Test advisor request: {researchQuestion: "compare_groups", ...}
Worker: Received test advisor request: {researchQuestion: "compare_groups", ...}
Worker: Generated 2 recommendations
Backend: Test advisor response: {ok: true, recommendations: [...]}
Frontend: Received response: {ok: true, recommendations: [...]}
```

---

## 🎯 If Still Not Working

1. **Check all three servers are running**
2. **Check browser console for exact error**
3. **Check worker logs for errors**
4. **Check backend logs for proxy errors**
5. **Test endpoint directly via Swagger UI**
6. **Restart all servers**

---

## 💡 Most Likely Fix

**99% of the time, the issue is:**
```bash
# Worker server not running or needs restart
cd worker
python main.py
```

**Then refresh browser and try again!**

---

**Last Updated:** October 23, 2025
