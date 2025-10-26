# 🚀 Quick Start - Test Advisor

## ✅ Fix Applied!

The endpoint issue has been fixed. The problem was with how FastAPI was parsing the request body.

---

## 🔧 To Get It Working:

### **Step 1: Restart Worker Server**
```bash
cd worker
# Stop current server (Ctrl+C if running)
python main.py
```

### **Step 2: Verify Endpoint**
Open browser: `http://localhost:8001/docs`

You should see:
- **"Test Advisor"** section
- `/test-advisor/recommend` endpoint
- `/test-advisor/auto-detect` endpoint

### **Step 3: Test It!**
1. Go to `http://localhost:3000`
2. Click **"🧭 Test Advisor"** (teal button)
3. Click **"Compare groups"**
4. Answer the questions
5. Click **"Get Recommendations"**

---

## ✅ What Was Fixed

**Problem:** FastAPI couldn't parse `Dict[str, Any]` as request body  
**Solution:** Changed to use `Request` object and manually parse JSON

**Before:**
```python
async def get_test_recommendations(request: Dict[str, Any]):
```

**After:**
```python
async def get_test_recommendations(request: Request):
    body = await request.json()
    recommendations = recommend_test(body)
```

---

## 🎯 Expected Behavior

### **After clicking "Compare groups":**

**Browser Console:**
```
Sending answers: {researchQuestion: "compare_groups", nGroups: 2, ...}
Received response: {ok: true, recommendations: [...]}
```

**Worker Console:**
```
INFO: Received test advisor request: {'researchQuestion': 'compare_groups', ...}
INFO: Generated 2 recommendations
```

### **You Should See:**
```
┌─────────────────────────────────────┐
│ ✓ RECOMMENDED                       │
│ Independent t-test                  │
│ Compare average scores between      │
│ two separate groups                 │
│                                     │
│ [Use This Test →]                  │
└─────────────────────────────────────┘
```

---

## 🐛 If Still Not Working

### **Check 1: Worker Running?**
```bash
# Should see:
INFO:     Uvicorn running on http://127.0.0.1:8001
INFO:     Application startup complete.
```

### **Check 2: Endpoint Registered?**
Visit: `http://localhost:8001/docs`  
Look for "Test Advisor" section

### **Check 3: Test Imports**
```bash
cd worker
python test_imports.py
```

Should see:
```
✅ test_advisor imports successful
✅ test_library imports successful
✅ Found 14 tests in library
✅ Got 2 recommendations
🎉 All imports working correctly!
```

### **Check 4: Backend Running?**
```bash
cd backend
node server.js
```

Should see:
```
Server running on port 3001
```

---

## 📝 All Services Must Be Running

```bash
# Terminal 1: Worker
cd worker
python main.py

# Terminal 2: Backend
cd backend
node server.js

# Terminal 3: Frontend
cd frontend
npm start
```

---

## 🎉 Success!

Once the worker is restarted, the Test Advisor should work perfectly!

**Try it now:**
1. Restart worker
2. Refresh browser
3. Click "🧭 Test Advisor"
4. Click "Compare groups"
5. Answer questions
6. Get recommendations!

---

**Last Updated:** October 23, 2025
