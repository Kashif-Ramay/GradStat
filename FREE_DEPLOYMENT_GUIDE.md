# 🆓 GradStat - 100% FREE Deployment Guide

**Total Cost: $0/month** ✅

---

## 🎯 Best FREE Deployment Strategy

### Architecture:
```
Frontend (Vercel FREE) → Backend (Render FREE) → Worker (Render FREE)
```

**Total Cost:** $0/month  
**Limitations:** Slower performance, services sleep after 15 min inactivity  
**Perfect for:** Students, demos, portfolios, low-traffic sites

---

## 📋 Option 1: Vercel + Render (Recommended)

### Step 1: Deploy Frontend (Vercel - FREE)

**Time:** 5 minutes  
**Cost:** FREE forever

1. **Push to GitHub:**
   ```bash
   cd gradstat
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/gradstat.git
   git push -u origin main
   ```

2. **Deploy to Vercel:**
   - Go to https://vercel.com
   - Sign up with GitHub (FREE)
   - Click "New Project"
   - Import your repository
   - Configure:
     - **Root Directory:** `frontend`
     - **Framework Preset:** Create React App
     - **Build Command:** `npm run build`
     - **Output Directory:** `build`
   - Click "Deploy"

3. **Add Environment Variable:**
   - Go to Project Settings → Environment Variables
   - Add: `REACT_APP_API_URL` = `https://your-backend.onrender.com`

**Result:** Your frontend is live at `https://gradstat.vercel.app`

---

### Step 2: Deploy Backend (Render - FREE)

**Time:** 10 minutes  
**Cost:** FREE (with limitations)

1. **Create `render.yaml` in backend folder:**
   ```yaml
   services:
     - type: web
       name: gradstat-backend
       env: node
       buildCommand: npm install
       startCommand: node server.js
       envVars:
         - key: NODE_ENV
           value: production
         - key: WORKER_URL
           value: https://gradstat-worker.onrender.com
         - key: ALLOWED_ORIGINS
           value: https://gradstat.vercel.app
   ```

2. **Deploy to Render:**
   - Go to https://render.com
   - Sign up with GitHub (FREE)
   - Click "New +" → "Web Service"
   - Connect your repository
   - Configure:
     - **Name:** gradstat-backend
     - **Root Directory:** `backend`
     - **Environment:** Node
     - **Build Command:** `npm install`
     - **Start Command:** `node server.js`
     - **Plan:** FREE
   - Add environment variables (from render.yaml)
   - Click "Create Web Service"

**Result:** Backend is live at `https://gradstat-backend.onrender.com`

---

### Step 3: Deploy Worker (Render - FREE)

**Time:** 10 minutes  
**Cost:** FREE (with limitations)

1. **Create `render.yaml` in worker folder:**
   ```yaml
   services:
     - type: web
       name: gradstat-worker
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

2. **Deploy to Render:**
   - Click "New +" → "Web Service"
   - Connect your repository
   - Configure:
     - **Name:** gradstat-worker
     - **Root Directory:** `worker`
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Plan:** FREE
   - Click "Create Web Service"

**Result:** Worker is live at `https://gradstat-worker.onrender.com`

---

### Step 4: Connect Everything

Update environment variables:

**Vercel (Frontend):**
- `REACT_APP_API_URL` = `https://gradstat-backend.onrender.com`

**Render Backend:**
- `WORKER_URL` = `https://gradstat-worker.onrender.com`
- `ALLOWED_ORIGINS` = `https://gradstat.vercel.app`

**Redeploy all services** to apply changes.

---

## 📋 Option 2: Netlify + Railway (Alternative FREE)

### Frontend: Netlify (FREE)

1. Go to https://netlify.com
2. Sign up (FREE)
3. Drag & drop `frontend/build` folder
4. Or connect GitHub repo

**Free Tier:**
- 100GB bandwidth/month
- Unlimited sites
- Automatic SSL
- Custom domain

---

### Backend + Worker: Railway (FREE)

1. Go to https://railway.app
2. Sign up with GitHub (FREE)
3. Click "New Project" → "Deploy from GitHub repo"
4. Add both backend and worker services

**Free Tier:**
- $5 credit/month (enough for small apps)
- 500 hours/month
- Automatic SSL

---

## 📋 Option 3: GitHub Pages + Heroku (Classic FREE)

### Frontend: GitHub Pages (FREE)

```bash
cd frontend
npm run build
npm install -g gh-pages
gh-pages -d build
```

**Free Tier:**
- Unlimited bandwidth
- Custom domain
- Automatic SSL

---

### Backend + Worker: Heroku (FREE with limitations)

**Note:** Heroku removed free tier in Nov 2022, but you can use:
- **Fly.io** (FREE tier)
- **Cyclic** (FREE tier)
- **Glitch** (FREE tier)

---

## 🆓 Complete FREE Stack Comparison

| Service | Frontend | Backend | Worker | Total |
|---------|----------|---------|--------|-------|
| **Vercel + Render** | FREE | FREE | FREE | $0 |
| **Netlify + Railway** | FREE | $5 credit | $5 credit | $0 |
| **GitHub Pages + Fly.io** | FREE | FREE | FREE | $0 |

---

## ⚠️ FREE Tier Limitations

### Render FREE Tier:
- ✅ Unlimited apps
- ✅ Automatic SSL
- ✅ Custom domains
- ⚠️ Services sleep after 15 min inactivity
- ⚠️ 750 hours/month (enough for 1 app 24/7)
- ⚠️ Slower performance (shared resources)
- ⚠️ 500MB RAM limit

### Vercel FREE Tier:
- ✅ Unlimited projects
- ✅ 100GB bandwidth/month
- ✅ Automatic SSL
- ✅ Fast CDN
- ✅ No sleep time
- ⚠️ 100 deployments/day limit

### Railway FREE Tier:
- ✅ $5 credit/month
- ✅ 500 hours/month
- ✅ Automatic SSL
- ⚠️ Credit runs out if heavy usage

---

## 🚀 Recommended: Vercel + Render

**Why?**
1. ✅ Completely FREE
2. ✅ Easy setup (15-20 minutes)
3. ✅ Automatic deployments from GitHub
4. ✅ Professional URLs
5. ✅ Automatic SSL
6. ✅ No credit card required

**Downsides:**
- Services sleep after 15 min (first request takes 30-60 seconds)
- Slower than paid tiers
- 750 hours/month limit (still enough for 24/7 operation of 1 service)

---

## 💡 Tips for FREE Deployment

### 1. Keep Services Awake

Create a cron job to ping your services every 10 minutes:

**Use:** https://cron-job.org (FREE)
- Ping: `https://gradstat-backend.onrender.com/health`
- Ping: `https://gradstat-worker.onrender.com/health`
- Every 10 minutes

### 2. Optimize for FREE Tier

**Backend:**
```javascript
// Add health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});
```

**Worker:**
```python
# Add health check endpoint
@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### 3. Use Environment Variables

Never hardcode URLs! Always use environment variables.

---

## 📊 Performance Comparison

| Metric | FREE Tier | Paid Tier ($14/mo) |
|--------|-----------|-------------------|
| Cold Start | 30-60s | Instant |
| Response Time | 200-500ms | 50-100ms |
| Uptime | 99% | 99.9% |
| RAM | 512MB | 2GB+ |
| Bandwidth | 100GB | Unlimited |

---

## 🎯 Step-by-Step: Deploy in 30 Minutes

### Minute 0-5: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### Minute 5-10: Deploy Frontend (Vercel)
1. Sign up at vercel.com
2. Import GitHub repo
3. Set root directory: `frontend`
4. Deploy

### Minute 10-20: Deploy Backend (Render)
1. Sign up at render.com
2. New Web Service
3. Connect GitHub repo
4. Set root directory: `backend`
5. Add environment variables
6. Deploy

### Minute 20-30: Deploy Worker (Render)
1. New Web Service
2. Connect GitHub repo
3. Set root directory: `worker`
4. Deploy

### Minute 30: Connect & Test
1. Update environment variables
2. Redeploy all services
3. Test at your Vercel URL

---

## ✅ Deployment Checklist

### Before Deployment:
- [ ] Code pushed to GitHub
- [ ] All tests passing locally
- [ ] Environment variables documented
- [ ] Health check endpoints added

### Vercel (Frontend):
- [ ] Account created
- [ ] Repository connected
- [ ] Build settings configured
- [ ] Environment variables set
- [ ] Deployment successful

### Render (Backend):
- [ ] Account created
- [ ] Web service created
- [ ] Build command set
- [ ] Start command set
- [ ] Environment variables set
- [ ] Deployment successful

### Render (Worker):
- [ ] Web service created
- [ ] Python environment configured
- [ ] Requirements installed
- [ ] Deployment successful

### Final:
- [ ] All services connected
- [ ] CORS configured
- [ ] File upload working
- [ ] Analysis working
- [ ] Test Advisor working
- [ ] Power Analysis working

---

## 🆘 Troubleshooting FREE Deployment

### Issue: Service Sleeps
**Solution:** Use cron-job.org to ping every 10 minutes

### Issue: Out of Memory
**Solution:** 
- Reduce file size limits
- Optimize Python imports
- Use lazy loading

### Issue: Slow Cold Starts
**Solution:** 
- Keep services warm with pings
- Show loading message to users
- Optimize startup time

### Issue: CORS Errors
**Solution:**
```javascript
app.use(cors({
  origin: [
    'https://gradstat.vercel.app',
    'http://localhost:3000'
  ],
  credentials: true
}));
```

---

## 💰 When to Upgrade to Paid

Upgrade when:
- ❌ Cold starts annoy users (>30s wait)
- ❌ Need 24/7 instant response
- ❌ Traffic > 100 users/day
- ❌ Need more than 512MB RAM
- ❌ Need guaranteed uptime

**Cost:** ~$14/month (Hobby tier)

---

## 🎉 Summary

**Best FREE Option:** Vercel (Frontend) + Render (Backend + Worker)

**Pros:**
- ✅ $0/month
- ✅ Professional URLs
- ✅ Automatic SSL
- ✅ Easy deployment
- ✅ GitHub integration

**Cons:**
- ⚠️ Services sleep after 15 min
- ⚠️ Slower performance
- ⚠️ Limited resources

**Perfect for:**
- 👨‍🎓 Students
- 📊 Portfolios
- 🧪 Demos
- 🔬 Research projects
- 📚 Academic use

---

## 🚀 Ready to Deploy?

Follow the **Vercel + Render** guide above and you'll have GradStat live in 30 minutes for **$0/month**!

---

**Questions?** Check the troubleshooting section or open a GitHub issue.

**Last Updated:** October 23, 2025  
**Status:** 100% FREE ✅
