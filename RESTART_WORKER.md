# 🔄 Restart Worker to Apply Fix

## Issue
The auto-detection is working but showing "No numeric columns found" even though the CSV has numeric data.

## Fix Applied
Updated `worker/test_advisor.py` to:
1. Include more numeric types (int32, float32)
2. Show debugging info about column types

## How to Restart Worker

### Step 1: Find Worker Process
```powershell
netstat -ano | findstr :8001
```

Look for the PID (last number), example: **12920**

### Step 2: Kill Worker
```powershell
taskkill /F /PID 12920
```
(Replace 12920 with your actual PID)

### Step 3: Restart Worker
```powershell
cd c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\worker
python main.py
```

**Expected output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

### Step 4: Test Again
1. Refresh browser (Ctrl+Shift+R)
2. Upload normal-data.csv
3. Click "I'm not sure - Test it for me"
4. Check the result - should now show column types in the message

---

## Quick Commands (Copy-Paste)

```powershell
# Find worker PID
netstat -ano | findstr :8001

# Kill it (replace PID)
taskkill /F /PID <PID>

# Restart
cd c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\worker
python main.py
```

---

## What to Look For

After restart, the error message should show:
```
No numeric columns found in your data. 
Column types detected: {'age': 'object', 'height': 'object', ...}
```

This will tell us if pandas is reading the columns as strings instead of numbers.

---

## If Columns Are 'object' Type

The issue is that pandas is reading numbers as strings. This can happen if:
1. CSV has extra spaces
2. CSV has non-numeric characters
3. Encoding issues

We'll fix the CSV or add type conversion in the next step.
