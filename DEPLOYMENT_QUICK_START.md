# 🚀 GradStat - Quick Deployment Guide

**Choose your deployment method:**

---

## 🖥️ Option 1: Local/Development (Easiest)

### Windows:
```cmd
deploy.bat
```

### Mac/Linux:
```bash
chmod +x deploy.sh
./deploy.sh
```

**That's it!** Access at http://localhost:3000

---

## ☁️ Option 2: Cloud (Recommended for Production)

### Step 1: Frontend (Netlify - FREE)

1. Push code to GitHub
2. Go to https://netlify.com
3. Click "New site from Git"
4. Select repository
5. Configure:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/build`
6. Deploy!

**Time:** 5 minutes  
**Cost:** FREE

---

### Step 2: Backend (Heroku - $7/month)

```bash
cd backend
heroku create gradstat-backend
heroku config:set NODE_ENV=production
heroku config:set WORKER_URL=https://your-worker.herokuapp.com
heroku config:set ALLOWED_ORIGINS=https://your-frontend.netlify.app
echo "web: node server.js" > Procfile
git add .
git commit -m "Deploy backend"
git push heroku main
```

**Time:** 10 minutes  
**Cost:** $7/month

---

### Step 3: Worker (Heroku - $7/month)

```bash
cd worker
heroku create gradstat-worker
heroku buildpacks:set heroku/python
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile
git add .
git commit -m "Deploy worker"
git push heroku main
```

**Time:** 10 minutes  
**Cost:** $7/month

---

### Step 4: Connect Everything

Update frontend environment:
```env
REACT_APP_API_URL=https://gradstat-backend.herokuapp.com
```

Update backend environment:
```bash
heroku config:set WORKER_URL=https://gradstat-worker.herokuapp.com
```

**Total Time:** 30 minutes  
**Total Cost:** $14/month  
**Result:** Production-ready app! 🎉

---

## 🐳 Option 3: Docker (Advanced)

```bash
docker-compose up -d
```

Access at http://localhost:3000

---

## 📊 Comparison

| Method | Time | Cost | Best For |
|--------|------|------|----------|
| Local | 5 min | FREE | Development, Testing |
| Cloud | 30 min | $14/mo | Production, Teams |
| Docker | 10 min | FREE | DevOps, Scaling |

---

## ✅ Post-Deployment Checklist

- [ ] All services running
- [ ] Can upload file
- [ ] Can run analysis
- [ ] Can download report
- [ ] Test Advisor works
- [ ] Power Analysis works

---

## 🆘 Quick Troubleshooting

### Issue: Services won't start
```bash
# Check if ports are in use
netstat -ano | findstr :3000
netstat -ano | findstr :3001
netstat -ano | findstr :8001

# Kill processes if needed
taskkill /F /PID <PID>
```

### Issue: CORS errors
Update `backend/server.js`:
```javascript
app.use(cors({
  origin: 'https://your-frontend-url.com',
  credentials: true
}));
```

### Issue: Build fails
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

---

## 📞 Need Help?

1. Check `DEPLOYMENT_GUIDE.md` for detailed instructions
2. Review error logs: `pm2 logs`
3. Open an issue on GitHub

---

## 🎯 Recommended: Cloud Deployment

**Why?**
- ✅ Always online
- ✅ Automatic SSL
- ✅ Easy updates
- ✅ Professional URLs
- ✅ Scalable

**Cost:** $14/month (less than a Netflix subscription!)

---

**Ready to deploy? Run `deploy.bat` (Windows) or `./deploy.sh` (Mac/Linux)!**
