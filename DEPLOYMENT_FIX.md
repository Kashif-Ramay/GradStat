# 🔧 PM2 Python Command Fix

**Issue:** Worker failed to start with PM2  
**Error:** `Script not found: python main.py`  
**Status:** ✅ FIXED

---

## 🐛 The Problem

PM2 was trying to execute `"python main.py"` as a single script file instead of running Python with main.py as an argument.

**Wrong:**
```batch
pm2 start "python main.py" --name worker --interpreter none
```

**Correct:**
```batch
pm2 start main.py --name worker --interpreter python
```

---

## ✅ The Fix

Updated `deploy.bat` to use the correct PM2 syntax for Python scripts.

---

## 🚀 Try Again

Run the deployment script again:

```cmd
cd c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat
deploy.bat
```

It should now work correctly!

---

## 📝 Alternative: Manual Start

If PM2 still has issues, you can start services manually:

### Terminal 1 - Worker:
```cmd
cd worker
python main.py
```

### Terminal 2 - Backend:
```cmd
cd backend
node server.js
```

### Terminal 3 - Frontend:
```cmd
cd frontend
npm start
```

---

**The fix has been applied. Run `deploy.bat` again!** ✅
