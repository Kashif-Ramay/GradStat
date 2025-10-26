# 🔒 GradStat Security - Quick Reference Card

## 🔑 Access Credentials

**Testing Password:** `GradStat2025!SecureTest`  
**Location:** `backend/.env` → `TESTING_PASSWORD`

---

## 📊 Current Limits

| Feature | Limit | Per |
|---------|-------|-----|
| API Requests | 20 | 15 minutes |
| Analyses | 10 | 1 hour |
| File Size | 10 MB | Upload |
| File Types | CSV, XLSX, XLS | Only |
| Files per Request | 1 | Upload |

---

## 🛡️ Security Features Active

✅ Password Protection  
✅ Rate Limiting  
✅ File Size Limits  
✅ File Type Validation  
✅ Path Traversal Protection  
✅ Auto Cleanup (1h uploads, 24h results)  
✅ Security Headers (Helmet)  
✅ CORS Protection  
✅ Enhanced Error Handling  

---

## ⚙️ Quick Configuration

### Change Password
```bash
# Edit backend/.env
TESTING_PASSWORD=YourNewPassword
```

### Adjust Rate Limits
```bash
# Edit backend/.env
RATE_LIMIT_MAX=30              # 30 requests per 15 min
ANALYSIS_LIMIT_MAX=20          # 20 analyses per hour
```

### Increase File Size
```bash
# Edit backend/.env
MAX_FILE_SIZE=20971520         # 20MB
```

---

## 🚀 Start Commands

```bash
# Terminal 1: Worker
cd worker && python main.py

# Terminal 2: Backend
cd backend && node server.js

# Terminal 3: Frontend
cd frontend && npm start
```

---

## 🔍 Check Security Status

**Backend startup shows:**
```
Password Protection: ENABLED ✅
Rate Limit: 20 requests per 15 minutes
Analysis Limit: 10 per hour
Max File Size: 10MB
Auto Cleanup: ENABLED
```

---

## ⚠️ Common Issues

| Issue | Solution |
|-------|----------|
| "Unauthorized" | Check password matches `.env` |
| "Too many requests" | Wait 15 min or increase limit |
| "File too large" | Use smaller file or increase limit |
| Password not working | Restart backend after changing `.env` |

---

## 📞 Emergency Actions

### Disable Password (Testing Only)
```bash
# Remove or comment out in backend/.env
# TESTING_PASSWORD=GradStat2025!SecureTest
```

### Reset Rate Limits
```bash
# Restart backend server
# Limits reset automatically
```

### Clear Old Files Manually
```bash
# Delete uploads
rm -rf backend/uploads/*

# Delete results  
rm -rf backend/results/*
```

---

## ✅ Pre-Deployment Checklist

- [ ] Password changed from default
- [ ] Rate limits configured
- [ ] File size appropriate
- [ ] `.env` not in git
- [ ] All 3 services start successfully
- [ ] Password screen appears
- [ ] Can access with password
- [ ] Rate limiting tested
- [ ] File upload tested
- [ ] Auto cleanup verified

---

## 📚 Full Documentation

- **Detailed Guide:** `SECURITY_IMPLEMENTED.md`
- **Deployment:** `QUICK_DEPLOY_FREE.md`
- **Security Risks:** `DEPLOYMENT_SECURITY.md`

---

<div align="center">

**Current Status: ✅ Secured for Testing**

**Password:** `GradStat2025!SecureTest`

</div>
