# 🔒 GradStat Deployment Security Guide

## ⚠️ Security Risks Summary

### Critical Risks (Must Fix Before Public Deployment)
1. **No Authentication** - Anyone can use unlimited resources
2. **No Rate Limiting** - Vulnerable to DoS attacks
3. **File Upload Attacks** - Malicious files could harm server
4. **Python Code Execution** - Potential for code injection

### Medium Risks (Fix for Production)
5. **Data Privacy** - User data not encrypted
6. **No Input Validation** - CSV content not sanitized
7. **Error Messages** - May expose system information

### Low Risks (Nice to Have)
8. **No Logging** - Can't track abuse
9. **No Monitoring** - Can't detect issues
10. **CORS Wide Open** - Any site can call API

---

## 🛡️ Security Hardening Steps

### Step 1: Add Rate Limiting (15 minutes)

**Install package:**
```bash
cd backend
npm install express-rate-limit
```

**Add to backend/server.js:**
```javascript
const rateLimit = require('express-rate-limit');

// General API rate limiter
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 20, // 20 requests per IP per 15 min
  message: 'Too many requests from this IP, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});

// Stricter limiter for analysis endpoint
const analysisLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 5, // 5 analyses per IP per hour
  message: 'Analysis limit reached. Please try again in an hour.',
});

// Apply to routes
app.use('/api/', apiLimiter);
app.post('/api/analyze', analysisLimiter, upload.single('file'), async (req, res) => {
  // existing code
});
```

---

### Step 2: Enhance File Validation (10 minutes)

**Add to backend/server.js:**
```javascript
// File size limit (10MB)
const MAX_FILE_SIZE = 10 * 1024 * 1024;

// Enhanced file filter
const fileFilter = (req, file, cb) => {
  const allowedTypes = ['.csv', '.xlsx', '.xls'];
  const ext = path.extname(file.originalname).toLowerCase();
  
  // Check extension
  if (!allowedTypes.includes(ext)) {
    return cb(new Error('Invalid file type. Only CSV and Excel files allowed.'));
  }
  
  // Check filename for suspicious patterns
  if (file.originalname.includes('..') || file.originalname.includes('/')) {
    return cb(new Error('Invalid filename.'));
  }
  
  cb(null, true);
};

// Update multer config
const upload = multer({
  storage: storage,
  fileFilter: fileFilter,
  limits: {
    fileSize: MAX_FILE_SIZE,
    files: 1
  }
});
```

---

### Step 3: Add Input Sanitization (15 minutes)

**Install packages:**
```bash
cd backend
npm install validator express-validator
```

**Add to backend/server.js:**
```javascript
const { body, validationResult } = require('express-validator');

// Validation middleware for analysis options
const validateAnalysisOptions = [
  body('analysisType').isString().trim().escape(),
  body('options').optional().isObject(),
  body('options.*.').optional().trim().escape(),
];

// Use in analyze endpoint
app.post('/api/analyze', 
  analysisLimiter,
  upload.single('file'),
  validateAnalysisOptions,
  async (req, res) => {
    // Check validation errors
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ error: 'Invalid input', details: errors.array() });
    }
    
    // existing code
  }
);
```

---

### Step 4: Add CORS Restrictions (5 minutes)

**Update backend/server.js:**
```javascript
// Instead of allowing all origins:
const cors = require('cors');

// For testing (allow localhost only)
const corsOptions = {
  origin: [
    'http://localhost:3000',
    'https://your-app-name.onrender.com' // Add your Render URL
  ],
  credentials: true,
  optionsSuccessStatus: 200
};

app.use(cors(corsOptions));
```

---

### Step 5: Add Environment Variables (10 minutes)

**Create .env file (DON'T COMMIT!):**
```bash
# .env
NODE_ENV=production
PORT=3001
WORKER_URL=http://localhost:8001
MAX_FILE_SIZE=10485760
RATE_LIMIT_WINDOW=900000
RATE_LIMIT_MAX=20
ANALYSIS_LIMIT_MAX=5
```

**Update backend/server.js:**
```javascript
require('dotenv').config();

const PORT = process.env.PORT || 3001;
const WORKER_URL = process.env.WORKER_URL || 'http://localhost:8001';
const MAX_FILE_SIZE = parseInt(process.env.MAX_FILE_SIZE) || 10485760;

// Use in code
app.listen(PORT, () => {
  console.log(`Backend server running on port ${PORT}`);
});
```

**Add to .gitignore:**
```
.env
.env.local
.env.production
```

---

### Step 6: Add Error Handling (10 minutes)

**Add to backend/server.js:**
```javascript
// Global error handler (add at end of file)
app.use((err, req, res, next) => {
  console.error('Error:', err);
  
  // Don't expose internal errors in production
  if (process.env.NODE_ENV === 'production') {
    res.status(500).json({ 
      error: 'An error occurred processing your request.' 
    });
  } else {
    res.status(500).json({ 
      error: err.message,
      stack: err.stack 
    });
  }
});

// Handle multer errors
app.use((err, req, res, next) => {
  if (err instanceof multer.MulterError) {
    if (err.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({ error: 'File too large. Maximum size is 10MB.' });
    }
    return res.status(400).json({ error: 'File upload error: ' + err.message });
  }
  next(err);
});
```

---

### Step 7: Add File Cleanup (10 minutes)

**Add to backend/server.js:**
```javascript
const cron = require('node-cron');
const fs = require('fs').promises;

// Clean up old files every hour
cron.schedule('0 * * * *', async () => {
  console.log('Running cleanup...');
  
  try {
    // Clean uploads older than 1 hour
    const uploadsDir = path.join(__dirname, 'uploads');
    const files = await fs.readdir(uploadsDir);
    const now = Date.now();
    
    for (const file of files) {
      const filePath = path.join(uploadsDir, file);
      const stats = await fs.stat(filePath);
      const age = now - stats.mtimeMs;
      
      if (age > 60 * 60 * 1000) { // 1 hour
        await fs.unlink(filePath);
        console.log(`Deleted old file: ${file}`);
      }
    }
    
    // Clean results older than 24 hours
    const resultsDir = path.join(__dirname, 'results');
    const resultFolders = await fs.readdir(resultsDir);
    
    for (const folder of resultFolders) {
      const folderPath = path.join(resultsDir, folder);
      const stats = await fs.stat(folderPath);
      const age = now - stats.mtimeMs;
      
      if (age > 24 * 60 * 60 * 1000) { // 24 hours
        await fs.rm(folderPath, { recursive: true });
        console.log(`Deleted old results: ${folder}`);
      }
    }
  } catch (err) {
    console.error('Cleanup error:', err);
  }
});
```

**Install cron:**
```bash
npm install node-cron
```

---

### Step 8: Add Security Headers (5 minutes)

**Install helmet:**
```bash
cd backend
npm install helmet
```

**Add to backend/server.js:**
```javascript
const helmet = require('helmet');

// Add security headers
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
  },
}));
```

---

## 🚀 Deployment Checklist

### Before Deploying:
- [ ] Add rate limiting
- [ ] Enhance file validation
- [ ] Add input sanitization
- [ ] Restrict CORS
- [ ] Add environment variables
- [ ] Add error handling
- [ ] Add file cleanup
- [ ] Add security headers
- [ ] Test all security measures
- [ ] Add privacy notice to UI

### For Testing Deployment:
- [ ] Use Render free tier
- [ ] Set environment to 'production'
- [ ] Monitor usage closely
- [ ] Set up alerts for high usage
- [ ] Share URL only with trusted testers
- [ ] Add password protection (optional)

### For Production Deployment:
- [ ] All above security measures
- [ ] Add authentication (Auth0, Firebase)
- [ ] Add user accounts
- [ ] Add payment/subscription
- [ ] Add comprehensive logging
- [ ] Add monitoring (Sentry, LogRocket)
- [ ] Add backup system
- [ ] Get security audit
- [ ] Add terms of service
- [ ] Add privacy policy
- [ ] Get liability insurance

---

## 🎯 Recommended Approach for Testing

### Option 1: Password-Protected Testing (Easiest)

**Add simple password protection:**
```javascript
// Add to backend/server.js
const TESTING_PASSWORD = process.env.TESTING_PASSWORD || 'test123';

app.use((req, res, next) => {
  const password = req.headers['x-testing-password'];
  
  if (password !== TESTING_PASSWORD) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  
  next();
});
```

**Add to frontend:**
```typescript
// Add password prompt on app load
const [password, setPassword] = useState('');
const [authenticated, setAuthenticated] = useState(false);

// Include in all API calls
axios.defaults.headers.common['X-Testing-Password'] = password;
```

---

### Option 2: IP Whitelist (More Secure)

**Add to backend/server.js:**
```javascript
const ALLOWED_IPS = process.env.ALLOWED_IPS?.split(',') || ['127.0.0.1'];

app.use((req, res, next) => {
  const clientIP = req.ip || req.connection.remoteAddress;
  
  if (!ALLOWED_IPS.includes(clientIP)) {
    return res.status(403).json({ error: 'Access denied' });
  }
  
  next();
});
```

---

### Option 3: Time-Limited Access (Best for Testing)

**Add to backend/server.js:**
```javascript
const TESTING_END_DATE = new Date('2025-11-25'); // 1 month from now

app.use((req, res, next) => {
  if (new Date() > TESTING_END_DATE) {
    return res.status(503).json({ 
      error: 'Testing period has ended. Please contact administrator.' 
    });
  }
  
  next();
});
```

---

## 📊 Monitoring & Alerts

### Add Usage Tracking:
```javascript
let requestCount = 0;
let analysisCount = 0;

app.use((req, res, next) => {
  requestCount++;
  
  if (requestCount % 100 === 0) {
    console.log(`Total requests: ${requestCount}, Analyses: ${analysisCount}`);
  }
  
  next();
});

app.post('/api/analyze', async (req, res) => {
  analysisCount++;
  
  if (analysisCount > 100) {
    console.warn('⚠️ High usage detected!');
    // Send email alert
  }
  
  // existing code
});
```

---

## 🎓 Security Best Practices Summary

### For Free Testing:
1. ✅ Add rate limiting (MUST)
2. ✅ Add file size limits (MUST)
3. ✅ Add password protection (RECOMMENDED)
4. ✅ Monitor usage daily (MUST)
5. ✅ Set time limit (RECOMMENDED)
6. ✅ Share URL privately (MUST)

### For Production:
1. ✅ All testing measures
2. ✅ Add authentication
3. ✅ Add payment system
4. ✅ Professional security audit
5. ✅ Legal compliance (GDPR, etc.)
6. ✅ Insurance coverage

---

## 💰 Cost Considerations

### Free Tier Risks:
- **Render Free:** Services sleep after 15 min → slow cold starts
- **Bandwidth:** 100 GB/month → ~1000 analyses
- **Storage:** Limited → must clean up files
- **No SLA:** Can go down anytime

### When to Upgrade:
- More than 50 users
- More than 500 analyses/month
- Need 24/7 uptime
- Need faster response times
- Need more storage

---

## 🚨 Emergency Procedures

### If Abused:
1. **Immediately:** Change password or disable app
2. **Check logs:** Identify attacker
3. **Block IP:** Add to blacklist
4. **Clean up:** Delete all uploaded files
5. **Review:** Check for data breaches
6. **Report:** If serious, report to hosting provider

### If Costs Spike:
1. **Pause services:** Stop worker first
2. **Check usage:** Review logs
3. **Add limits:** Reduce rate limits
4. **Contact support:** Render support team
5. **Consider:** Move to self-hosted

---

## ✅ Quick Start Security Setup (30 minutes)

**Run these commands:**
```bash
# Install security packages
cd backend
npm install express-rate-limit helmet validator express-validator node-cron dotenv

# Create .env file
echo "NODE_ENV=production" > .env
echo "TESTING_PASSWORD=your-secure-password-here" >> .env
echo "MAX_FILE_SIZE=10485760" >> .env

# Update .gitignore
echo ".env" >> .gitignore
```

**Then apply Steps 1-8 above!**

---

<div align="center">

**🔒 Security is a journey, not a destination!**

**For testing: Implement Steps 1-5 minimum**

**For production: Implement ALL steps + professional audit**

</div>
