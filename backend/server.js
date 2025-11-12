/**
 * GradStat Backend API Server
 * Express server that orchestrates file uploads and analysis jobs
 * 
 * Copyright (c) 2024-2025 Kashif Ramay
 * All rights reserved.
 * 
 * This software is provided for educational and research purposes.
 */

const express = require('express');
const multer = require('multer');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');
const { body, validationResult } = require('express-validator');
const cron = require('node-cron');
const axios = require('axios');
const FormData = require('form-data');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs').promises;
const path = require('path');
require('dotenv').config();

const app = express();

// Trust proxy for Render.com (needed for rate limiting and X-Forwarded-For headers)
app.set('trust proxy', 1);

const PORT = process.env.PORT || 3001;
const WORKER_URL = process.env.WORKER_URL || 'http://localhost:8001';
const UPLOAD_DIR = process.env.UPLOAD_DIR || './uploads';
const RESULTS_DIR = process.env.RESULTS_DIR || './results';

// In-memory job store (use Redis in production)
const jobs = new Map();

// Ensure directories exist
async function ensureDirectories() {
  await fs.mkdir(UPLOAD_DIR, { recursive: true });
  await fs.mkdir(RESULTS_DIR, { recursive: true });
}

// Middleware
app.use(helmet());
app.use(compression());
app.use(morgan('combined'));
// CORS configuration - Allow frontend domain
const allowedOrigins = process.env.ALLOWED_ORIGINS 
  ? process.env.ALLOWED_ORIGINS.split(',')
  : [
      'http://localhost:3000',
      'https://gradstat-frontend.onrender.com'
    ];

app.use(cors({
  origin: function (origin, callback) {
    // Allow requests with no origin (like mobile apps or curl requests)
    if (!origin) return callback(null, true);
    
    if (allowedOrigins.indexOf(origin) === -1) {
      const msg = 'The CORS policy for this site does not allow access from the specified Origin.';
      return callback(new Error(msg), false);
    }
    return callback(null, true);
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'testing-password', 'x-testing-password'],
  exposedHeaders: ['Content-Type']
}));

// IMPORTANT: Do NOT add express.json() or express.urlencoded() here
// They will interfere with multer file uploads
// Instead, add them manually to specific routes that need JSON parsing

// Rate limiting - General API
const limiter = rateLimit({
  windowMs: parseInt(process.env.RATE_LIMIT_WINDOW) || 15 * 60 * 1000, // 15 minutes
  max: parseInt(process.env.RATE_LIMIT_MAX) || 20, // 20 requests per 15 min
  message: 'Too many requests from this IP, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});
app.use('/api/', limiter);

// Stricter rate limiting for analysis endpoint
const analysisLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: parseInt(process.env.ANALYSIS_LIMIT_MAX) || 5, // 5 analyses per hour
  message: 'Analysis limit reached. Please try again in an hour.',
  standardHeaders: true,
  legacyHeaders: false,
});

// Password protection for testing (optional - set TESTING_PASSWORD in .env)
const passwordProtection = (req, res, next) => {
  const testingPassword = process.env.TESTING_PASSWORD;
  
  // Skip if no password is set
  if (!testingPassword) {
    return next();
  }
  
  // Skip for health checks and ping
  if (req.path === '/health' || req.path === '/ping') {
    return next();
  }
  
  // Skip for OPTIONS requests (CORS preflight)
  if (req.method === 'OPTIONS') {
    return next();
  }
  
  const providedPassword = req.headers['x-testing-password'];
  
  if (providedPassword !== testingPassword) {
    return res.status(401).json({ 
      error: 'Unauthorized',
      message: 'Testing password required. Contact administrator for access.'
    });
  }
  
  next();
};

// Apply password protection to all API routes
app.use('/api/', passwordProtection);

// File upload configuration
const storage = multer.diskStorage({
  destination: async (req, file, cb) => {
    cb(null, UPLOAD_DIR);
  },
  filename: (req, file, cb) => {
    const uniqueName = `${uuidv4()}-${file.originalname}`;
    cb(null, uniqueName);
  },
});

const upload = multer({
  storage,
  limits: {
    fileSize: parseInt(process.env.MAX_FILE_SIZE) || 10 * 1024 * 1024, // 10MB default
    files: 1, // Only 1 file at a time
  },
  fileFilter: (req, file, cb) => {
    // Allow dummy files for power analysis
    if (file.originalname === 'dummy.txt' || file.originalname === 'dummy.csv') {
      cb(null, true);
      return;
    }
    
    const allowedTypes = ['.csv', '.xlsx', '.xls'];
    const ext = path.extname(file.originalname).toLowerCase();
    
    // Check extension
    if (!allowedTypes.includes(ext)) {
      return cb(new Error('Invalid file type. Only CSV and Excel files are allowed.'));
    }
    
    // Check for suspicious filenames (path traversal)
    if (file.originalname.includes('..') || file.originalname.includes('/') || file.originalname.includes('\\')) {
      return cb(new Error('Invalid filename.'));
    }
    
    cb(null, true);
  },
});

// Root endpoint for Render health checks
app.get('/', (req, res) => {
  res.json({ 
    service: 'GradStat Backend',
    status: 'running',
    version: '1.0.0',
    endpoints: {
      health: '/health',
      analyze: '/api/analyze',
      interpret: '/api/interpret'
    }
  });
});

// Health check endpoint - minimal response for monitoring
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Ultra-minimal ping endpoint for cron jobs (even smaller response)
app.get('/ping', (req, res) => {
  res.status(200).type('text/plain').send('OK');
});

/**
 * POST /api/validate
 * Validate uploaded file and return preview
 */
app.post('/api/validate', upload.single('file'), async (req, res) => {
  try {
    // Debug logging
    console.log('Validate request received');
    console.log('Content-Type:', req.headers['content-type']);
    console.log('File:', req.file);
    console.log('Body:', req.body);
    
    if (!req.file) {
      console.error('No file in request');
      return res.status(400).json({ error: 'No file uploaded' });
    }

    // Forward to Python worker for validation
    const formData = new FormData();
    const fileBuffer = await fs.readFile(req.file.path);
    formData.append('file', fileBuffer, {
      filename: req.file.originalname,
      contentType: req.file.mimetype
    });

    const response = await axios.post(`${WORKER_URL}/validate`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      maxContentLength: Infinity,
      maxBodyLength: Infinity,
    });

    // Clean up uploaded file after validation
    await fs.unlink(req.file.path).catch(() => {});

    res.json(response.data);
  } catch (error) {
    console.error('Validation error:', error);
    
    // Clean up file on error
    if (req.file) {
      await fs.unlink(req.file.path).catch(() => {});
    }

    res.status(500).json({
      error: 'Failed to validate file',
      details: error.response?.data || error.message,
    });
  }
});

/**
 * POST /api/analyze
 * Start an analysis job
 */
app.post('/api/analyze', analysisLimiter, upload.single('file'), async (req, res) => {
  try {
    console.log('Received analyze request');
    console.log('req.body:', req.body);
    console.log('req.file:', req.file ? 'File present' : 'No file');
    
    const options = JSON.parse(req.body.options || '{}');
    const analysisType = req.body.analysisType || options.analysisType;
    
    console.log('Analysis type:', analysisType);
    console.log('Options:', options);
    
    // Power analysis doesn't need a file
    if (analysisType !== 'power' && !req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const jobId = uuidv4();

    // Create job record
    jobs.set(jobId, {
      id: jobId,
      status: 'pending',
      progress: 0,
      createdAt: new Date().toISOString(),
      filePath: req.file ? req.file.path : null,
      options,
      logs: [],
    });

    // Start analysis asynchronously
    processAnalysis(jobId, req.file ? req.file.path : null, options).catch((error) => {
      console.error(`Job ${jobId} failed:`, error);
      const job = jobs.get(jobId);
      if (job) {
        job.status = 'failed';
        job.error = error.message;
      }
    });

    res.json({ job_id: jobId });
  } catch (error) {
    console.error('Analysis start error:', error);
    console.error('Error stack:', error.stack);
    
    if (req.file) {
      await fs.unlink(req.file.path).catch(() => {});
    }

    res.status(500).json({
      error: 'Internal server error',
      details: error.message,
    });
  }
});

/**
 * GET /api/job-status
 * Get status of an analysis job
 */
app.get('/api/job-status', (req, res) => {
  const jobId = req.query.id;

  if (!jobId) {
    return res.status(400).json({ error: 'Job ID is required' });
  }

  const job = jobs.get(jobId);

  if (!job) {
    return res.status(404).json({ error: 'Job not found' });
  }

  res.json({
    status: job.status,
    progress: job.progress,
    result_url: job.resultUrl,
    result_meta: job.resultMeta,
    logs: job.logs,
    error: job.error,
  });
});

/**
 * POST /api/test-advisor/recommend
 * Get statistical test recommendations
 */
app.post('/api/test-advisor/recommend', express.json(), async (req, res) => {
  try {
    console.log('Test advisor request:', req.body);
    const response = await axios.post(`${WORKER_URL}/test-advisor/recommend`, req.body, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    console.log('Test advisor response:', response.data);
    res.json(response.data);
  } catch (error) {
    console.error('Test advisor error:', error.response?.data || error.message);
    res.status(500).json({ error: error.response?.data?.detail || error.message });
  }
});

/**
 * POST /api/test-advisor/auto-detect
 * Auto-detect data characteristics
 */
app.post('/api/test-advisor/auto-detect', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const formData = new FormData();
    formData.append('file', req.file.buffer, req.file.originalname);

    const response = await axios.post(`${WORKER_URL}/test-advisor/auto-detect`, formData, {
      headers: formData.getHeaders(),
    });

    res.json(response.data);
  } catch (error) {
    console.error('Auto-detect error:', error.message);
    res.status(500).json({ error: error.message });
  }
});

/**
 * POST /api/test-advisor/auto-answer
 * Auto-answer a specific wizard question
 */
app.post('/api/test-advisor/auto-answer', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const { questionKey } = req.body;
    if (!questionKey) {
      return res.status(400).json({ error: 'questionKey is required' });
    }

    // Read file from disk (multer uses diskStorage)
    const fileBuffer = await fs.readFile(req.file.path);
    
    const formData = new FormData();
    formData.append('file', fileBuffer, {
      filename: req.file.originalname,
      contentType: req.file.mimetype || 'text/csv',
      knownLength: fileBuffer.length
    });
    formData.append('question_key', questionKey);

    const response = await axios.post(`${WORKER_URL}/test-advisor/auto-answer`, formData, {
      headers: formData.getHeaders(),
    });

    // Clean up uploaded file
    try {
      await fs.unlink(req.file.path);
    } catch (cleanupError) {
      console.warn('Failed to delete temp file:', cleanupError.message);
    }

    res.json(response.data);
  } catch (error) {
    console.error('Auto-answer error:', error.message);
    res.status(500).json({ error: error.message });
  }
});

/**
 * POST /api/test-advisor/analyze-dataset
 * Comprehensive dataset analysis - answers ALL wizard questions at once
 */
app.post('/api/test-advisor/analyze-dataset', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    // Read file from disk (multer uses diskStorage)
    const fileBuffer = await fs.readFile(req.file.path);
    
    const formData = new FormData();
    formData.append('file', fileBuffer, {
      filename: req.file.originalname,
      contentType: req.file.mimetype || 'text/csv',
      knownLength: fileBuffer.length
    });

    const response = await axios.post(`${WORKER_URL}/test-advisor/analyze-dataset`, formData, {
      headers: formData.getHeaders(),
    });

    // Clean up uploaded file
    try {
      await fs.unlink(req.file.path);
    } catch (cleanupError) {
      console.warn('Failed to delete temp file:', cleanupError.message);
    }

    res.json(response.data);
  } catch (error) {
    console.error('Dataset analysis error:', error.message);
    res.status(500).json({ error: error.message });
  }
});

/**
 * GET /api/report
 * Download analysis report
 */
app.get('/api/report', async (req, res) => {
  const jobId = req.query.id;
  console.log('Download request for job:', jobId);

  if (!jobId) {
    return res.status(400).json({ error: 'Job ID is required' });
  }

  const job = jobs.get(jobId);
  console.log('Job status:', job?.status);

  if (!job || job.status !== 'done') {
    return res.status(404).json({ error: 'Report not available' });
  }

  try {
    const reportPath = path.join(RESULTS_DIR, `${jobId}.zip`);
    console.log('Looking for file at:', reportPath);
    
    // Check if file exists
    try {
      await fs.access(reportPath);
      const stats = await fs.stat(reportPath);
      console.log('File found! Size:', stats.size, 'bytes');
    } catch (err) {
      console.error('Report file not found:', reportPath);
      console.error('Error:', err.message);
      return res.status(404).json({ error: 'Report file not found. The analysis may not have completed successfully.' });
    }
    
    // Read the file and send with proper headers
    const fileBuffer = await fs.readFile(reportPath);
    const fileName = `gradstat-report-${jobId}.zip`;
    
    console.log('Sending file:', fileName, 'Size:', fileBuffer.length);
    
    res.setHeader('Content-Type', 'application/zip');
    res.setHeader('Content-Disposition', `attachment; filename="${fileName}"`);
    res.setHeader('Content-Length', fileBuffer.length);
    res.send(fileBuffer);
    
    console.log('File sent successfully');
  } catch (error) {
    console.error('Report download error:', error);
    res.status(500).json({ error: 'Failed to download report: ' + error.message });
  }
});

/**
 * Process analysis job
 * Calls Python worker and updates job status
 */
async function processAnalysis(jobId, filePath, options) {
  const job = jobs.get(jobId);
  if (!job) return;

  try {
    job.status = 'running';
    job.progress = 10;
    job.logs.push('Starting analysis...');

    const formData = new FormData();
    
    // Only read and attach file if it exists (not for power analysis)
    if (filePath) {
      const fileBuffer = await fs.readFile(filePath);
      formData.append('file', fileBuffer, {
        filename: path.basename(filePath),
        contentType: 'text/csv'
      });
    } else {
      // For power analysis, create a dummy file
      const dummyBuffer = Buffer.from('', 'utf-8');
      formData.append('file', dummyBuffer, {
        filename: 'dummy.txt',
        contentType: 'text/plain'
      });
    }
    
    formData.append('options', JSON.stringify(options));

    job.progress = 20;
    job.logs.push('Sending data to analysis worker...');

    const response = await axios.post(`${WORKER_URL}/analyze`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      maxContentLength: Infinity,
      maxBodyLength: Infinity,
      timeout: 300000, // 5 minutes
    });

    job.progress = 90;
    job.logs.push('Analysis complete, preparing results...');

    // Save results
    const resultPath = path.join(RESULTS_DIR, `${jobId}.zip`);
    
    if (response.data.report_zip) {
      // Ensure results directory exists
      await fs.mkdir(RESULTS_DIR, { recursive: true });
      
      // Save base64 zip file
      const zipBuffer = Buffer.from(response.data.report_zip, 'base64');
      await fs.writeFile(resultPath, zipBuffer);
      console.log(`Report saved to: ${resultPath} (${zipBuffer.length} bytes)`);
      job.logs.push(`Report saved: ${resultPath}`);
      
      // Verify file was written
      try {
        const stats = await fs.stat(resultPath);
        console.log(`File verified: ${stats.size} bytes`);
      } catch (err) {
        console.error('File verification failed:', err);
      }
    } else {
      console.error('No report_zip in response');
      job.logs.push('Warning: No report ZIP received from worker');
    }

    job.status = 'done';
    job.progress = 100;
    job.resultUrl = `/api/report?id=${jobId}`;
    job.resultMeta = response.data.results;
    job.logs.push('Results ready for download');

    // Clean up uploaded file (only if it exists)
    if (filePath) {
      await fs.unlink(filePath).catch(() => {});
    }
  } catch (error) {
    console.error(`Analysis processing error for job ${jobId}:`, error);
    job.status = 'failed';
    job.error = error.response?.data?.error || error.message;
    job.logs.push(`Error: ${job.error}`);
    
    // Clean up on error (only if file exists)
    if (filePath) {
      await fs.unlink(filePath).catch(() => {});
    }
  }
}

// Automatic file cleanup - runs every hour
cron.schedule('0 * * * *', async () => {
  console.log('Running automatic file cleanup...');
  
  try {
    const now = Date.now();
    const ONE_HOUR = 60 * 60 * 1000;
    const ONE_DAY = 24 * 60 * 60 * 1000;
    
    // Clean uploads older than 1 hour
    try {
      const uploadFiles = await fs.readdir(UPLOAD_DIR);
      let uploadsCleaned = 0;
      
      for (const file of uploadFiles) {
        const filePath = path.join(UPLOAD_DIR, file);
        const stats = await fs.stat(filePath);
        const age = now - stats.mtimeMs;
        
        if (age > ONE_HOUR) {
          await fs.unlink(filePath);
          uploadsCleaned++;
        }
      }
      
      if (uploadsCleaned > 0) {
        console.log(`Cleaned ${uploadsCleaned} old upload files`);
      }
    } catch (err) {
      console.error('Error cleaning uploads:', err.message);
    }
    
    // Clean results older than 24 hours
    try {
      const resultFiles = await fs.readdir(RESULTS_DIR);
      let resultsCleaned = 0;
      
      for (const file of resultFiles) {
        const filePath = path.join(RESULTS_DIR, file);
        const stats = await fs.stat(filePath);
        const age = now - stats.mtimeMs;
        
        if (age > ONE_DAY) {
          await fs.unlink(filePath);
          resultsCleaned++;
        }
      }
      
      if (resultsCleaned > 0) {
        console.log(`Cleaned ${resultsCleaned} old result files`);
      }
    } catch (err) {
      console.error('Error cleaning results:', err.message);
    }
    
  } catch (error) {
    console.error('File cleanup error:', error);
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Server error:', err);
  
  if (err instanceof multer.MulterError) {
    if (err.code === 'LIMIT_FILE_SIZE') {
      const maxSizeMB = (parseInt(process.env.MAX_FILE_SIZE) || 10485760) / (1024 * 1024);
      return res.status(400).json({ error: `File too large. Maximum size is ${maxSizeMB}MB.` });
    }
    if (err.code === 'LIMIT_FILE_COUNT') {
      return res.status(400).json({ error: 'Too many files. Upload one file at a time.' });
    }
    return res.status(400).json({ error: err.message });
  }

  // Don't expose internal errors in production
  if (process.env.NODE_ENV === 'production') {
    res.status(500).json({
      error: 'An error occurred processing your request.',
    });
  } else {
    res.status(500).json({
      error: 'Internal server error',
      details: err.message,
      stack: err.stack,
    });
  }
});

/**
 * POST /api/interpret
 * Get AI interpretation of analysis results
 */
app.post('/api/interpret', express.json(), async (req, res) => {
  try {
    console.log('AI interpretation request');
    const response = await axios.post(`${WORKER_URL}/interpret`, req.body, {
      headers: { 'Content-Type': 'application/json' },
      timeout: 30000  // 30 second timeout for OpenAI API calls
    });
    res.json(response.data);
  } catch (error) {
    console.error('Interpretation error:', error.message);
    console.error('Worker response:', error.response?.data);
    console.error('Worker status:', error.response?.status);
    res.status(500).json({ 
      error: 'Failed to generate interpretation',
      details: error.response?.data || error.message 
    });
  }
});

/**
 * POST /api/ask
 * Ask a question about analysis results
 */
app.post('/api/ask', express.json(), async (req, res) => {
  try {
    console.log('AI question:', req.body.question);
    const response = await axios.post(`${WORKER_URL}/ask`, req.body, {
      headers: { 'Content-Type': 'application/json' },
      timeout: 30000  // 30 second timeout for OpenAI API calls
    });
    res.json(response.data);
  } catch (error) {
    console.error('Question error:', error.message);
    res.status(500).json({ 
      error: 'Failed to answer question',
      details: error.response?.data || error.message 
    });
  }
});

/**
 * POST /api/what-if
 * Explore what-if scenarios
 */
app.post('/api/what-if', express.json(), async (req, res) => {
  try {
    console.log('What-if scenario:', req.body.scenario);
    const response = await axios.post(`${WORKER_URL}/what-if`, req.body, {
      headers: { 'Content-Type': 'application/json' },
      timeout: 30000  // 30 second timeout for OpenAI API calls
    });
    res.json(response.data);
  } catch (error) {
    console.error('What-if error:', error.message);
    res.status(500).json({ 
      error: 'Failed to analyze scenario',
      details: error.response?.data || error.message 
    });
  }
});

/**
 * POST /api/test-advisor/recommend
 * Get AI test recommendations from research description
 */
app.post('/api/test-advisor/recommend', express.json(), async (req, res) => {
  try {
    console.log('AI test recommendation request');
    const response = await axios.post(`${WORKER_URL}/test-advisor/recommend`, req.body, {
      headers: { 'Content-Type': 'application/json' },
      timeout: 30000
    });
    res.json(response.data);
  } catch (error) {
    console.error('AI recommendation error:', error.message);
    res.status(500).json({ 
      error: 'Failed to get AI recommendation',
      details: error.response?.data || error.message 
    });
  }
});

/**
 * POST /api/test-advisor/ask
 * Ask AI a question about statistical tests
 */
app.post('/api/test-advisor/ask', express.json(), async (req, res) => {
  try {
    console.log('AI question:', req.body.question);
    const response = await axios.post(`${WORKER_URL}/test-advisor/ask`, req.body, {
      headers: { 'Content-Type': 'application/json' },
      timeout: 30000
    });
    res.json(response.data);
  } catch (error) {
    console.error('AI question error:', error.message);
    res.status(500).json({ 
      error: 'Failed to answer question',
      details: error.response?.data || error.message 
    });
  }
});

/**
 * POST /api/test-advisor/explain
 * Get AI explanation of statistical assumption
 */
app.post('/api/test-advisor/explain', express.json(), async (req, res) => {
  try {
    console.log('AI explanation request:', req.body.assumption);
    const response = await axios.post(`${WORKER_URL}/test-advisor/explain`, req.body, {
      headers: { 'Content-Type': 'application/json' },
      timeout: 30000
    });
    res.json(response.data);
  } catch (error) {
    console.error('AI explanation error:', error.message);
    res.status(500).json({ 
      error: 'Failed to get explanation',
      details: error.response?.data || error.message 
    });
  }
});

/**
 * POST /api/test-advisor/compare
 * Compare two statistical tests with AI
 */
app.post('/api/test-advisor/compare', express.json(), async (req, res) => {
  try {
    console.log('AI test comparison:', req.body.test1, 'vs', req.body.test2);
    const response = await axios.post(`${WORKER_URL}/test-advisor/compare`, req.body, {
      headers: { 'Content-Type': 'application/json' },
      timeout: 30000
    });
    res.json(response.data);
  } catch (error) {
    console.error('AI comparison error:', error.message);
    res.status(500).json({ 
      error: 'Failed to compare tests',
      details: error.response?.data || error.message 
    });
  }
});

/**
 * POST /api/test-advisor/enhance-detection
 * Enhance auto-detection with AI explanation
 */
app.post('/api/test-advisor/enhance-detection', express.json(), async (req, res) => {
  try {
    console.log('AI enhancement request');
    const response = await axios.post(`${WORKER_URL}/test-advisor/enhance-detection`, req.body, {
      headers: { 'Content-Type': 'application/json' },
      timeout: 30000
    });
    res.json(response.data);
  } catch (error) {
    console.error('AI enhancement error:', error.message);
    res.status(500).json({ 
      error: 'Failed to enhance detection',
      details: error.response?.data || error.message 
    });
  }
});

/**
 * POST /api/test-advisor/sample-size
 * Get AI sample size guidance
 */
app.post('/api/test-advisor/sample-size', express.json(), async (req, res) => {
  try {
    console.log('AI sample size guidance request');
    const response = await axios.post(`${WORKER_URL}/test-advisor/sample-size`, req.body, {
      headers: { 'Content-Type': 'application/json' },
      timeout: 30000
    });
    res.json(response.data);
  } catch (error) {
    console.error('AI sample size error:', error.message);
    res.status(500).json({ 
      error: 'Failed to get sample size guidance',
      details: error.response?.data || error.message 
    });
  }
});

// 404 handler - MUST be last!
app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

// Start server
async function startServer() {
  await ensureDirectories();
  
  app.listen(PORT, () => {
    console.log('='.repeat(50));
    console.log('🚀 GradStat Backend Server Started');
    console.log('='.repeat(50));
    console.log(`Port: ${PORT}`);
    console.log(`Worker URL: ${WORKER_URL}`);
    console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
    console.log(`Max File Size: ${(parseInt(process.env.MAX_FILE_SIZE) || 10485760) / (1024 * 1024)}MB`);
    console.log(`Rate Limit: ${process.env.RATE_LIMIT_MAX || 20} requests per ${(parseInt(process.env.RATE_LIMIT_WINDOW) || 900000) / 60000} minutes`);
    console.log(`Analysis Limit: ${process.env.ANALYSIS_LIMIT_MAX || 5} per hour`);
    console.log(`Password Protection: ${process.env.TESTING_PASSWORD ? 'ENABLED ✅' : 'DISABLED ⚠️'}`);
    console.log(`Auto Cleanup: ENABLED (uploads: 1h, results: 24h)`);
    console.log('='.repeat(50));
  });
}

startServer().catch((error) => {
  console.error('Failed to start server:', error);
  process.exit(1);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, shutting down gracefully...');
  process.exit(0);
});

module.exports = app; // For testing
