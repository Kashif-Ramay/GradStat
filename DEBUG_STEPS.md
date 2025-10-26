# 🔍 Debug Steps - See What's Being Read

## What I Added
Added logging to `worker/analyze.py` to show:
- Number of rows and columns
- Column names
- Data types

## Steps to Debug

### 1. Restart Worker
```powershell
# Kill current worker (Ctrl+C in worker terminal)
# Or find and kill:
netstat -ano | findstr :8001
taskkill /F /PID <PID>

# Restart
cd c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\worker
python main.py
```

### 2. Test Auto-Detection
1. Refresh browser (Ctrl+Shift+R)
2. Upload normal-data.csv
3. Click "I'm not sure - Test it for me"

### 3. Check Worker Logs
Look at the worker terminal output. You should see:
```
INFO: CSV read successfully: 15 rows, 4 columns
INFO: Columns: ['age', 'height', 'weight', 'blood_pressure']
INFO: Dtypes: {'age': 'int64', 'height': 'int64', 'weight': 'int64', 'blood_pressure': 'int64'}
```

## What to Look For

### ✅ Good Output:
```
CSV read successfully: 15 rows, 4 columns
Columns: ['age', 'height', 'weight', 'blood_pressure']
Dtypes: {'age': 'int64', ...}
```
→ File is being read correctly!

### ❌ Bad Output:
```
CSV read successfully: 0 rows, 1 columns
Columns: ['undefined']
Dtypes: {'undefined': 'object'}
```
→ File is still corrupted

### 🤔 If Still Bad:
The issue is in how the file buffer is being sent from backend to worker.

---

## Alternative: Test Worker Directly

Skip the backend and test worker directly:

```powershell
# In PowerShell
$file = "c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\test-data\normal-data.csv"

curl.exe -X POST http://localhost:8001/test-advisor/auto-answer `
  -F "file=@$file" `
  -F "question_key=isNormal"
```

**Expected response:**
```json
{
  "ok": true,
  "answer": true,
  "confidence": "high",
  "explanation": "✅ 4/4 variables (100%) are normally distributed..."
}
```

If this works, the issue is in the backend → worker communication.
If this fails, the issue is in the worker itself.

---

## Copy-Paste Commands

```powershell
# Restart worker
cd c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\worker
python main.py

# Test worker directly (in another terminal)
curl.exe -X POST http://localhost:8001/test-advisor/auto-answer -F "file=@c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\test-data\normal-data.csv" -F "question_key=isNormal"
```

---

**Restart worker, test, and share the worker logs!** 📋
