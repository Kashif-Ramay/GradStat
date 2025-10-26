import { test, expect } from '@playwright/test';
import path from 'path';

test.describe('GradStat E2E Tests', () => {
  test('should load homepage', async ({ page }) => {
    await page.goto('/');
    
    await expect(page.locator('h1')).toContainText('GradStat');
    await expect(page.locator('text=Upload Your Data')).toBeVisible();
  });

  test('should upload and validate file', async ({ page }) => {
    await page.goto('/');
    
    // Upload file
    const fileInput = page.locator('input[type="file"]');
    const filePath = path.join(__dirname, '../../example-data/sample_dataset.csv');
    await fileInput.setInputFiles(filePath);
    
    // Click validate button
    await page.click('button:has-text("Validate")');
    
    // Wait for preview to appear
    await expect(page.locator('text=Data Preview')).toBeVisible({ timeout: 10000 });
    await expect(page.locator('text=student_id')).toBeVisible();
  });

  test('should run descriptive analysis', async ({ page }) => {
    await page.goto('/');
    
    // Upload file
    const fileInput = page.locator('input[type="file"]');
    const filePath = path.join(__dirname, '../../example-data/sample_dataset.csv');
    await fileInput.setInputFiles(filePath);
    
    // Validate
    await page.click('button:has-text("Validate")');
    await page.waitForSelector('text=Data Preview', { timeout: 10000 });
    
    // Select analysis type
    await page.selectOption('select', 'descriptive');
    
    // Run analysis
    await page.click('button:has-text("Run Analysis")');
    
    // Wait for job to complete (this may take a while)
    await expect(page.locator('text=done')).toBeVisible({ timeout: 60000 });
    
    // Check for results
    await expect(page.locator('text=Analysis Results')).toBeVisible();
  });

  test('should run group comparison analysis', async ({ page }) => {
    await page.goto('/');
    
    // Upload file
    const fileInput = page.locator('input[type="file"]');
    const filePath = path.join(__dirname, '../../example-data/sample_dataset.csv');
    await fileInput.setInputFiles(filePath);
    
    // Validate
    await page.click('button:has-text("Validate")');
    await page.waitForSelector('text=Data Preview', { timeout: 10000 });
    
    // Select analysis type
    await page.selectOption('select', 'group-comparison');
    
    // Configure variables
    await page.selectOption('select:near(:text("Group Variable"))', 'group');
    await page.selectOption('select:near(:text("Outcome Variable"))', 'exam_score');
    
    // Run analysis
    await page.click('button:has-text("Run Analysis")');
    
    // Wait for completion
    await expect(page.locator('text=done')).toBeVisible({ timeout: 60000 });
    
    // Verify results contain statistical test
    await expect(page.locator('text=p-value')).toBeVisible();
  });

  test('should download report', async ({ page }) => {
    await page.goto('/');
    
    // Upload and run analysis
    const fileInput = page.locator('input[type="file"]');
    const filePath = path.join(__dirname, '../../example-data/sample_dataset.csv');
    await fileInput.setInputFiles(filePath);
    
    await page.click('button:has-text("Validate")');
    await page.waitForSelector('text=Data Preview', { timeout: 10000 });
    
    await page.selectOption('select', 'descriptive');
    await page.click('button:has-text("Run Analysis")');
    
    // Wait for completion
    await expect(page.locator('text=done')).toBeVisible({ timeout: 60000 });
    
    // Download report
    const downloadPromise = page.waitForEvent('download');
    await page.click('a:has-text("Download Full Report")');
    const download = await downloadPromise;
    
    expect(download.suggestedFilename()).toContain('gradstat-report');
  });
});
