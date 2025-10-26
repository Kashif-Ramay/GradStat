# ⚡ Quick Deploy Guide - Free Testing (30 minutes)

> **Deploy GradStat for free testing on Render.com**

---

## 🎯 What You'll Get

- ✅ Free hosting for 3 services (frontend, backend, worker)
- ✅ Auto-deploy from GitHub
- ✅ HTTPS/SSL included
- ✅ 750 hours/month per service
- ⚠️ Services sleep after 15 min (30s cold start)
- ⚠️ 512 MB RAM per service
- ⚠️ No custom domain on free tier

---

## 📋 Prerequisites

1. GitHub account
2. Render.com account (free)
3. GradStat code pushed to GitHub

---

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Code for Deployment (10 min)

#### 1.1 Add Security (CRITICAL!)

**Install packages:**
```bash
cd backend
npm install express-rate-limit helmet dotenv
```

**Create `.env` file:**
```bash
# backend/.env
NODE_ENV=production
PORT=3001
TESTING_PASSWORD=your-secret-password-123
MAX_FILE_SIZE=10485760
```

**Add to `.gitignore`:**
```
.env
.env.local
.env.production
```

#### 1.2 Update backend/server.js

**Add at the top:**
```javascript
require('dotenv').config();
const rateLimit = require('express-rate-limit');
const helmet = require('helmet');

// Security headers
app.use(helmet());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 20, // 20 requests per IP
  message: 'Too many requests, please try again later'
});

app.use('/api/', limiter);

// Simple password protection for testing
const TESTING_PASSWORD = process.env.TESTING_PASSWORD;

app.use((req, res, next) => {
  // Skip for health checks
  if (req.path === '/health') return next();
  
  const password = req.headers['x-testing-password'];
  
  if (password !== TESTING_PASSWORD) {
    return res.status(401).json({ error: 'Unauthorized - Testing password required' });
  }
  
  next();
});
```

#### 1.3 Update frontend to send password

**Add to frontend/src/App.tsx:**
```typescript
// At the top of App component
const [testingPassword, setTestingPassword] = useState('');
const [isAuthenticated, setIsAuthenticated] = useState(false);

// Set axios default header
useEffect(() => {
  if (testingPassword) {
    axios.defaults.headers.common['X-Testing-Password'] = testingPassword;
  }
}, [testingPassword]);

// Add password prompt before main UI
if (!isAuthenticated) {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
        <h2 className="text-2xl font-bold mb-4">GradStat Testing Access</h2>
        <p className="text-gray-600 mb-4">Enter testing password to continue</p>
        <input
          type="password"
          value={testingPassword}
          onChange={(e) => setTestingPassword(e.target.value)}
          className="w-full px-4 py-2 border rounded mb-4"
          placeholder="Testing password"
        />
        <button
          onClick={() => {
            if (testingPassword) {
              setIsAuthenticated(true);
            }
          }}
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          Access Testing
        </button>
      </div>
    </div>
  );
}
```

#### 1.4 Create build scripts

**Create `backend/package.json` build script:**
```json
{
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  }
}
```

**Create `worker/requirements.txt` (if not exists):**
```
fastapi==0.104.1
uvicorn==0.24.0
pandas==2.1.3
numpy==1.26.2
scipy==1.11.4
scikit-learn==1.3.2
matplotlib==3.8.2
seaborn==0.13.0
statsmodels==0.14.0
openpyxl==3.1.2
plotly==5.18.0
lifelines==0.27.8
```

#### 1.5 Push to GitHub

```bash
git add .
git commit -m "Prepare for deployment with security"
git push origin main
```

---

### Step 2: Deploy on Render.com (15 min)

#### 2.1 Create Render Account
1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repositories

#### 2.2 Deploy Worker (Python Service)

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name:** `gradstat-worker`
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Root Directory:** `worker`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** `Free`
4. **Environment Variables:**
   - `PYTHON_VERSION` = `3.11.0`
5. Click **"Create Web Service"**
6. **Copy the service URL** (e.g., `https://gradstat-worker.onrender.com`)

#### 2.3 Deploy Backend (Node Service)

1. Click **"New +"** → **"Web Service"**
2. Connect same repository
3. Configure:
   - **Name:** `gradstat-backend`
   - **Region:** Same as worker
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** `Node`
   - **Build Command:** `npm install`
   - **Start Command:** `npm start`
   - **Instance Type:** `Free`
4. **Environment Variables:**
   - `NODE_ENV` = `production`
   - `PORT` = `3001`
   - `WORKER_URL` = `https://gradstat-worker.onrender.com` (from step 2.2)
   - `TESTING_PASSWORD` = `your-secret-password-123`
5. Click **"Create Web Service"**
6. **Copy the service URL** (e.g., `https://gradstat-backend.onrender.com`)

#### 2.4 Deploy Frontend (Static Site)

1. Click **"New +"** → **"Static Site"**
2. Connect same repository
3. Configure:
   - **Name:** `gradstat-frontend`
   - **Branch:** `main`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `build`
4. **Environment Variables:**
   - `REACT_APP_BACKEND_URL` = `https://gradstat-backend.onrender.com`
5. Click **"Create Static Site"**
6. **Copy the site URL** (e.g., `https://gradstat-frontend.onrender.com`)

---

### Step 3: Configure CORS (5 min)

**Update backend/server.js:**
```javascript
const cors = require('cors');

const corsOptions = {
  origin: [
    'http://localhost:3000',
    'https://gradstat-frontend.onrender.com' // Your Render frontend URL
  ],
  credentials: true
};

app.use(cors(corsOptions));
```

**Push changes:**
```bash
git add backend/server.js
git commit -m "Update CORS for Render deployment"
git push origin main
```

Render will auto-redeploy!

---

### Step 4: Test Deployment (5 min)

1. Open `https://gradstat-frontend.onrender.com`
2. Enter testing password
3. Upload a test file
4. Run an analysis
5. Verify results appear

**Expected behavior:**
- First request may take 30s (cold start)
- Subsequent requests faster
- After 15 min idle, services sleep again

---

## 🔒 Security Measures Included

✅ **Rate Limiting:** 20 requests per 15 min per IP  
✅ **Password Protection:** Testing password required  
✅ **File Size Limits:** 10MB max  
✅ **CORS Restrictions:** Only your frontend allowed  
✅ **Security Headers:** Helmet.js protection  
✅ **HTTPS:** Automatic SSL/TLS

---

## 📊 Monitoring Your Deployment

### Check Logs:
1. Go to Render dashboard
2. Click on service name
3. Click **"Logs"** tab
4. Monitor for errors

### Check Usage:
1. Render dashboard → Service
2. **"Metrics"** tab
3. Watch:
   - Request count
   - Response times
   - Memory usage
   - Bandwidth

### Set Alerts:
1. Render dashboard → Service
2. **"Settings"** → **"Notifications"**
3. Add email for:
   - Deploy failures
   - Service crashes
   - High usage

---

## ⚠️ Important Limitations

### Free Tier Constraints:
- **Cold Starts:** 30s delay after 15 min idle
- **RAM:** 512 MB (may crash with large files)
- **Bandwidth:** 100 GB/month (~1000 analyses)
- **No Persistence:** Files deleted on restart
- **No Custom Domain:** Use Render subdomain

### What This Means:
- ✅ Good for: Testing with 5-10 users
- ✅ Good for: Demo purposes
- ✅ Good for: Development testing
- ❌ Bad for: Production use
- ❌ Bad for: High traffic
- ❌ Bad for: Large datasets (>5MB)

---

## 💰 When to Upgrade

### Upgrade to Paid ($7/month per service) if:
- More than 50 users
- Need faster response (no cold starts)
- Need more RAM (1GB+)
- Need custom domain
- Need 24/7 uptime
- Need more bandwidth

### Upgrade to Self-Hosted if:
- More than 500 users
- Need full control
- Need custom infrastructure
- Have IT team
- Need compliance (HIPAA, etc.)

---

## 🐛 Troubleshooting

### Issue: "Unauthorized" error
**Solution:** Check testing password matches in:
- Backend `.env` file
- Frontend password input
- Render environment variables

### Issue: "Worker not responding"
**Solution:** 
- Check worker logs in Render
- Verify WORKER_URL in backend env vars
- Wait 30s for cold start

### Issue: "File upload fails"
**Solution:**
- Check file size < 10MB
- Check file type (.csv, .xlsx only)
- Check backend logs for errors

### Issue: "Out of memory"
**Solution:**
- Use smaller datasets
- Upgrade to paid tier (1GB RAM)
- Optimize Python code

### Issue: "Service unavailable"
**Solution:**
- Check Render status page
- Check if free hours exhausted (750/month)
- Restart service in Render dashboard

---

## 📝 Sharing with Testers

### What to Share:
1. **URL:** `https://gradstat-frontend.onrender.com`
2. **Password:** `your-secret-password-123`
3. **Instructions:**
   - First load may take 30s
   - Use files < 5MB
   - Don't share password publicly

### What NOT to Share:
- ❌ GitHub repository (unless open source)
- ❌ Render dashboard access
- ❌ Environment variables
- ❌ Backend/Worker URLs directly

---

## 🎯 Next Steps After Testing

### If Testing Goes Well:
1. **Collect Feedback:** What works? What doesn't?
2. **Fix Bugs:** Address issues found
3. **Add Features:** Based on feedback
4. **Plan Production:** Consider paid hosting
5. **Add Analytics:** Track usage patterns

### If Moving to Production:
1. **Upgrade Render Plan:** $7/month per service
2. **Add Authentication:** Auth0, Firebase
3. **Add Payment:** Stripe integration
4. **Add Monitoring:** Sentry, LogRocket
5. **Get Security Audit:** Professional review
6. **Add Terms/Privacy:** Legal compliance
7. **Get Insurance:** Liability coverage

---

## ✅ Deployment Checklist

### Before Deploying:
- [ ] Security measures added (rate limiting, password)
- [ ] Environment variables configured
- [ ] CORS restrictions set
- [ ] Code pushed to GitHub
- [ ] Testing password chosen

### During Deployment:
- [ ] Worker service deployed
- [ ] Backend service deployed
- [ ] Frontend site deployed
- [ ] Environment variables set on all services
- [ ] CORS updated with frontend URL

### After Deployment:
- [ ] Test with sample data
- [ ] Check all features work
- [ ] Monitor logs for errors
- [ ] Set up usage alerts
- [ ] Share with testers
- [ ] Document any issues

---

## 📞 Support Resources

### Render Support:
- **Docs:** https://render.com/docs
- **Community:** https://community.render.com
- **Status:** https://status.render.com
- **Support:** support@render.com

### GradStat Issues:
- Check logs first
- Review security settings
- Test locally to isolate issue
- Check GitHub issues (if open source)

---

<div align="center">

# 🎉 You're Ready to Deploy!

**Total Time:** ~30 minutes  
**Cost:** $0 (Free tier)  
**Difficulty:** Medium

### Good luck with your testing! 🚀

</div>

---

## 📚 Additional Resources

- **Full Deployment Guide:** See `DEPLOYMENT_GUIDE.md`
- **Security Details:** See `DEPLOYMENT_SECURITY.md`
- **User Guide:** See `USER_GUIDE.md`
- **Project Documentation:** See `README.md`
