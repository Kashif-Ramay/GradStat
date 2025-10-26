# 🚀 GradStat Deployment Guide

**Version:** 1.0  
**Date:** October 23, 2025  
**Status:** Production Ready ✅

---

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Local Testing](#local-testing)
3. [Production Build](#production-build)
4. [Deployment Options](#deployment-options)
5. [Environment Configuration](#environment-configuration)
6. [Post-Deployment Verification](#post-deployment-verification)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Troubleshooting](#troubleshooting)

---

## ✅ Pre-Deployment Checklist

### 1. Code Quality
- [x] All features tested locally
- [x] No console errors
- [x] All TypeScript types correct
- [x] Python linting passed
- [x] No hardcoded credentials

### 2. Dependencies
- [x] All npm packages up to date
- [x] All Python packages in requirements.txt
- [x] No security vulnerabilities

### 3. Configuration
- [ ] Environment variables configured
- [ ] CORS settings updated
- [ ] Rate limits adjusted for production
- [ ] File upload limits set

### 4. Documentation
- [x] README.md updated
- [x] API documentation complete
- [x] User guide available

---

## 🧪 Local Testing

### Step 1: Clean Install

```bash
# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install

# Backend
cd ../backend
rm -rf node_modules package-lock.json
npm install

# Worker
cd ../worker
pip install -r requirements.txt
```

### Step 2: Run All Services

**Terminal 1 - Worker:**
```bash
cd worker
python main.py
```
**Expected:** `Uvicorn running on http://0.0.0.0:8001`

**Terminal 2 - Backend:**
```bash
cd backend
node server.js
```
**Expected:** `GradStat backend server running on port 3001`

**Terminal 3 - Frontend:**
```bash
cd frontend
npm start
```
**Expected:** `webpack compiled successfully`

### Step 3: Test All Features

- [ ] File upload (CSV & Excel)
- [ ] All 7 analysis types
- [ ] Test Advisor (all 7 research questions)
- [ ] Power Analysis
- [ ] Report download
- [ ] All visualizations

---

## 🏗️ Production Build

### Step 1: Build Frontend

```bash
cd frontend
npm run build
```

**Output:** `build/` folder with optimized static files

**Verify:**
```bash
ls -la build/
# Should see: index.html, static/, asset-manifest.json
```

### Step 2: Optimize Backend

**Create production config:**
```bash
cd backend
cp .env.example .env.production
```

**Edit `.env.production`:**
```env
NODE_ENV=production
PORT=3001
WORKER_URL=http://localhost:8001
ALLOWED_ORIGINS=https://yourdomain.com
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100
MAX_FILE_SIZE=10485760
```

### Step 3: Prepare Worker

**Create production requirements:**
```bash
cd worker
pip freeze > requirements.txt
```

**Verify Python version:**
```bash
python --version
# Should be Python 3.8+
```

---

## 🌐 Deployment Options

### Option 1: Single Server Deployment (Recommended for Small-Medium Scale)

**Best for:** University departments, research labs, small teams

**Requirements:**
- Ubuntu 20.04+ or similar Linux server
- 4GB RAM minimum (8GB recommended)
- 20GB storage
- Python 3.8+
- Node.js 16+

**Architecture:**
```
[Nginx] → [Frontend (Static)] → [Backend (Node.js)] → [Worker (Python)]
  :80        :3000                  :3001                :8001
```

---

### Option 2: Cloud Deployment (Recommended for Production)

#### A. Frontend: Netlify/Vercel

**Netlify Deployment:**

1. **Connect Repository:**
   ```bash
   # Push to GitHub
   git add .
   git commit -m "Production ready"
   git push origin main
   ```

2. **Configure Netlify:**
   - Go to https://netlify.com
   - Click "New site from Git"
   - Select your repository
   - Build settings:
     - Base directory: `frontend`
     - Build command: `npm run build`
     - Publish directory: `frontend/build`

3. **Environment Variables:**
   ```
   REACT_APP_API_URL=https://your-backend.herokuapp.com
   ```

4. **Deploy!**

**Vercel Deployment:**

```bash
cd frontend
npm install -g vercel
vercel
```

Follow prompts and configure build settings.

---

#### B. Backend: Heroku/Railway

**Heroku Deployment:**

1. **Install Heroku CLI:**
   ```bash
   npm install -g heroku
   heroku login
   ```

2. **Create Heroku App:**
   ```bash
   cd backend
   heroku create gradstat-backend
   ```

3. **Configure Environment:**
   ```bash
   heroku config:set NODE_ENV=production
   heroku config:set WORKER_URL=https://your-worker.herokuapp.com
   heroku config:set ALLOWED_ORIGINS=https://your-frontend.netlify.app
   ```

4. **Create Procfile:**
   ```bash
   echo "web: node server.js" > Procfile
   ```

5. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy backend"
   git push heroku main
   ```

**Railway Deployment:**

```bash
cd backend
npm install -g @railway/cli
railway login
railway init
railway up
```

---

#### C. Worker: Heroku/Railway/DigitalOcean

**Heroku Deployment:**

1. **Create App:**
   ```bash
   cd worker
   heroku create gradstat-worker
   ```

2. **Add Python Buildpack:**
   ```bash
   heroku buildpacks:set heroku/python
   ```

3. **Create Procfile:**
   ```bash
   echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile
   ```

4. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy worker"
   git push heroku main
   ```

**DigitalOcean App Platform:**

1. Go to https://cloud.digitalocean.com
2. Create new App
3. Connect GitHub repository
4. Select `worker` folder
5. Configure:
   - Type: Python
   - Run command: `uvicorn main:app --host 0.0.0.0 --port 8080`
   - Environment: Python 3.11

---

### Option 3: Docker Deployment (Advanced)

**Create Docker Compose:**

```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    environment:
      - REACT_APP_API_URL=http://localhost:3001

  backend:
    build: ./backend
    ports:
      - "3001:3001"
    environment:
      - WORKER_URL=http://worker:8001
      - NODE_ENV=production
    depends_on:
      - worker

  worker:
    build: ./worker
    ports:
      - "8001:8001"
    environment:
      - PYTHONUNBUFFERED=1
```

**Deploy:**
```bash
docker-compose up -d
```

---

## ⚙️ Environment Configuration

### Frontend (.env.production)

```env
REACT_APP_API_URL=https://your-backend-url.com
REACT_APP_VERSION=1.0.0
```

### Backend (.env.production)

```env
# Server
NODE_ENV=production
PORT=3001

# Worker
WORKER_URL=https://your-worker-url.com

# Security
ALLOWED_ORIGINS=https://your-frontend-url.com
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100

# File Upload
MAX_FILE_SIZE=10485760
UPLOAD_DIR=./uploads

# Cleanup
CLEANUP_INTERVAL=3600000
MAX_FILE_AGE=86400000
```

### Worker (config.py or environment)

```python
# config.py
import os

class Config:
    ENV = os.getenv('ENV', 'production')
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8001))
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*').split(',')
```

---

## 🔍 Post-Deployment Verification

### 1. Health Checks

**Worker Health:**
```bash
curl https://your-worker-url.com/health
# Expected: {"status": "healthy"}
```

**Backend Health:**
```bash
curl https://your-backend-url.com/health
# Expected: {"status": "ok"}
```

**Frontend:**
```bash
curl https://your-frontend-url.com
# Expected: HTML content
```

### 2. Functionality Tests

**Test Upload:**
```bash
curl -X POST https://your-backend-url.com/api/upload \
  -F "file=@test.csv"
```

**Test Analysis:**
```bash
curl -X POST https://your-backend-url.com/api/analyze \
  -F "file=@test.csv" \
  -F "analysisType=descriptive"
```

### 3. Performance Tests

**Load Time:**
- Frontend load: < 3 seconds
- API response: < 2 seconds
- Analysis completion: < 30 seconds

**Use tools:**
- Google PageSpeed Insights
- GTmetrix
- WebPageTest

---

## 📊 Monitoring & Maintenance

### 1. Logging

**Backend Logging:**
```javascript
// Add to server.js
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});
```

**Worker Logging:**
```python
# Add to main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('worker.log'),
        logging.StreamHandler()
    ]
)
```

### 2. Monitoring Tools

**Recommended:**
- **Uptime:** UptimeRobot, Pingdom
- **Performance:** New Relic, DataDog
- **Errors:** Sentry
- **Analytics:** Google Analytics, Plausible

### 3. Backup Strategy

**Database (if added):**
```bash
# Daily backups
0 2 * * * pg_dump gradstat > /backups/gradstat_$(date +\%Y\%m\%d).sql
```

**Files:**
```bash
# Weekly backups
0 3 * * 0 tar -czf /backups/uploads_$(date +\%Y\%m\%d).tar.gz /app/uploads
```

### 4. Update Schedule

**Weekly:**
- Check for security updates
- Review error logs
- Monitor disk space

**Monthly:**
- Update dependencies
- Review performance metrics
- User feedback review

**Quarterly:**
- Major version updates
- Feature additions
- Security audit

---

## 🐛 Troubleshooting

### Common Issues

#### 1. CORS Errors

**Symptom:** Frontend can't connect to backend

**Fix:**
```javascript
// backend/server.js
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || '*',
  credentials: true,
}));
```

#### 2. File Upload Fails

**Symptom:** "File too large" error

**Fix:**
```javascript
// backend/server.js
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: '50mb', extended: true }));
```

#### 3. Worker Timeout

**Symptom:** Analysis takes too long

**Fix:**
```python
# worker/main.py
app = FastAPI(timeout=300)  # 5 minutes
```

#### 4. Memory Issues

**Symptom:** Server crashes under load

**Fix:**
```bash
# Increase Node.js memory
NODE_OPTIONS=--max-old-space-size=4096 node server.js

# Increase Python memory (if needed)
ulimit -v 4194304  # 4GB
```

---

## 🚀 Quick Deployment Commands

### Deploy Everything (Single Server)

```bash
#!/bin/bash
# deploy.sh

echo "🚀 Deploying GradStat..."

# Build frontend
cd frontend
npm run build
cd ..

# Restart services
pm2 restart worker
pm2 restart backend
pm2 restart frontend

echo "✅ Deployment complete!"
```

### Use PM2 for Process Management

```bash
# Install PM2
npm install -g pm2

# Start services
cd worker
pm2 start "python main.py" --name worker

cd ../backend
pm2 start server.js --name backend

cd ../frontend
pm2 serve build 3000 --name frontend --spa

# Save configuration
pm2 save
pm2 startup
```

---

## 📝 Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Secrets secured (no hardcoded keys)
- [ ] CORS configured correctly
- [ ] Rate limiting enabled
- [ ] File size limits set

### Deployment
- [ ] Frontend built successfully
- [ ] Backend deployed
- [ ] Worker deployed
- [ ] DNS configured
- [ ] SSL certificate installed
- [ ] Health checks passing

### Post-Deployment
- [ ] All features tested in production
- [ ] Performance acceptable
- [ ] Monitoring configured
- [ ] Backup strategy in place
- [ ] Documentation updated
- [ ] Team notified

---

## 🎯 Recommended Architecture

### Small Scale (< 100 users)
```
Single Server:
- Frontend: Netlify/Vercel (Free tier)
- Backend + Worker: Heroku (Hobby tier - $7/month)
Total: ~$7/month
```

### Medium Scale (100-1000 users)
```
Distributed:
- Frontend: Netlify/Vercel (Pro - $19/month)
- Backend: Heroku Standard ($25/month)
- Worker: DigitalOcean Droplet ($12/month)
Total: ~$56/month
```

### Large Scale (1000+ users)
```
Cloud Infrastructure:
- Frontend: Vercel Pro + CDN
- Backend: AWS ECS/Kubernetes
- Worker: AWS Lambda/ECS
- Database: AWS RDS
- Storage: AWS S3
Total: ~$200-500/month
```

---

## 📞 Support

**Issues:** https://github.com/yourusername/gradstat/issues  
**Email:** support@gradstat.com  
**Docs:** https://docs.gradstat.com

---

## ✅ Final Checklist

Before going live:

- [ ] All services running
- [ ] SSL certificate active
- [ ] Monitoring enabled
- [ ] Backups configured
- [ ] Documentation complete
- [ ] User guide published
- [ ] Support channels ready
- [ ] Announcement prepared

---

**Congratulations! You're ready to deploy GradStat! 🎉**

**Need help?** Follow the steps above or contact support.

---

**Last Updated:** October 23, 2025  
**Version:** 1.0  
**Status:** Production Ready ✅
