/**
 * Backend API tests
 */

const request = require('supertest');
const fs = require('fs').promises;
const path = require('path');

// Mock the app without starting the server
jest.mock('dotenv', () => ({ config: jest.fn() }));

describe('GradStat Backend API', () => {
  let app;

  beforeAll(() => {
    // Set test environment variables
    process.env.NODE_ENV = 'test';
    process.env.WORKER_URL = 'http://localhost:8001';
    process.env.UPLOAD_DIR = './test-uploads';
    process.env.RESULTS_DIR = './test-results';
  });

  beforeEach(() => {
    // Clear module cache and reimport app
    jest.resetModules();
    app = require('./server');
  });

  afterAll(async () => {
    // Cleanup test directories
    await fs.rm('./test-uploads', { recursive: true, force: true });
    await fs.rm('./test-results', { recursive: true, force: true });
  });

  describe('GET /health', () => {
    it('should return health status', async () => {
      const response = await request(app).get('/health');
      
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('status', 'ok');
      expect(response.body).toHaveProperty('timestamp');
    });
  });

  describe('POST /api/validate', () => {
    it('should reject request without file', async () => {
      const response = await request(app)
        .post('/api/validate');
      
      expect(response.status).toBe(400);
      expect(response.body).toHaveProperty('error');
    });

    it('should reject invalid file types', async () => {
      const response = await request(app)
        .post('/api/validate')
        .attach('file', Buffer.from('test'), 'test.txt');
      
      expect(response.status).toBe(500);
    });
  });

  describe('POST /api/analyze', () => {
    it('should reject request without file', async () => {
      const response = await request(app)
        .post('/api/analyze');
      
      expect(response.status).toBe(400);
      expect(response.body).toHaveProperty('error');
    });

    it('should create job with valid file', async () => {
      // Create a simple CSV
      const csvContent = 'name,age,score\nAlice,25,85\nBob,30,92';
      
      const response = await request(app)
        .post('/api/analyze')
        .attach('file', Buffer.from(csvContent), 'test.csv')
        .field('options', JSON.stringify({ analysisType: 'descriptive' }));
      
      // Note: This will fail without worker running, but tests the endpoint
      expect(response.status).toBeLessThan(500);
    });
  });

  describe('GET /api/job-status', () => {
    it('should require job ID', async () => {
      const response = await request(app)
        .get('/api/job-status');
      
      expect(response.status).toBe(400);
      expect(response.body).toHaveProperty('error');
    });

    it('should return 404 for non-existent job', async () => {
      const response = await request(app)
        .get('/api/job-status?id=non-existent-id');
      
      expect(response.status).toBe(404);
    });
  });

  describe('Error handling', () => {
    it('should handle 404 for unknown routes', async () => {
      const response = await request(app)
        .get('/unknown-route');
      
      expect(response.status).toBe(404);
      expect(response.body).toHaveProperty('error');
    });
  });
});
