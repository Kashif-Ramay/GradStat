/**
 * GradStat - Statistical Analysis Platform
 * Copyright (c) 2024-2025 Kashif Ramay
 * All rights reserved.
 * 
 * This software is provided for educational and research purposes.
 */

import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import DataUpload from './components/DataUpload';
import AnalysisSelector from './components/AnalysisSelector';
import DataPreview from './components/DataPreview';
import JobStatus from './components/JobStatus';
import Results from './components/Results';
import KeyboardShortcutsHelp from './components/KeyboardShortcutsHelp';
import TestAdvisor from './components/TestAdvisor';
import DataQualityReport from './components/DataQualityReport';
import HomePage from './components/HomePage';
import FeedbackForm from './components/FeedbackForm';
import ExampleDatasets from './components/ExampleDatasets';
import useKeyboardShortcuts from './hooks/useKeyboardShortcuts';
import { PreviewData, AnalysisOptions, JobStatusData } from './types';
import { initGA } from './utils/analytics';

// Configure API base URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';

function App() {
  const [showHomePage, setShowHomePage] = useState<boolean>(true);
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<PreviewData | null>(null);
  const [analysisType, setAnalysisType] = useState<string>('descriptive');
  const [options, setOptions] = useState<AnalysisOptions>({});
  const [showPowerAnalysis, setShowPowerAnalysis] = useState<boolean>(false);
  const [showTestAdvisor, setShowTestAdvisor] = useState<boolean>(false);
  const [jobId, setJobId] = useState<string | null>(null);
  const [jobStatus, setJobStatus] = useState<JobStatusData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showShortcutsHelp, setShowShortcutsHelp] = useState(false);
  
  // Password protection
  const [testingPassword, setTestingPassword] = useState<string>('');
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  
  // Refs for keyboard shortcuts
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Initialize Google Analytics
  useEffect(() => {
    initGA();
  }, []);

  // Configure axios with base URL and password header
  useEffect(() => {
    axios.defaults.baseURL = API_BASE_URL;
    if (testingPassword) {
      axios.defaults.headers.common['X-Testing-Password'] = testingPassword;
    }
  }, [testingPassword]);

  // Clear data
  const handleClearData = () => {
    setFile(null);
    setPreview(null);
    setJobId(null);
    setJobStatus(null);
    setError(null);
    setShowPowerAnalysis(false);
    setShowTestAdvisor(false);
    setAnalysisType('descriptive');
  };

  // Handle test selection from Test Advisor
  const handleSelectTest = async (testInfo: any, uploadedFile: File | null, skipValidation: boolean = false) => {
    // Set analysis type
    setAnalysisType(testInfo.analysis_type);
    
    // Pre-fill options if available
    if (testInfo.gradstat_options) {
      setOptions(testInfo.gradstat_options);
    }
    
    // Set the uploaded file from Test Advisor
    if (uploadedFile) {
      setFile(uploadedFile);
      
      // Exit Test Advisor mode first
      setShowTestAdvisor(false);
      
      // Skip validation if file was already validated in Test Advisor
      if (!skipValidation) {
        // Validate the file to generate preview
        setLoading(true);
        setError(null);
        
        try {
          const formData = new FormData();
          formData.append('file', uploadedFile);

          const response = await axios.post('/api/validate', formData, {
            headers: {
              'Content-Type': undefined  // Let browser set it with boundary
            }
          });

          setPreview(response.data.preview);
          
          if (response.data.issues && response.data.issues.length > 0) {
            console.warn('Data quality issues:', response.data.issues);
          }
        } catch (err: any) {
          setError(err.response?.data?.error || 'Failed to validate file');
          console.error('Validation error:', err);
        } finally {
          setLoading(false);
        }
      } else {
        // Set minimal preview to allow analysis to proceed
        // The backend will read the file directly during analysis
        setPreview({
          columns: [],
          types: {},
          rows: [],
          rowCount: 0
        });
      }
    } else {
      // Exit Test Advisor mode
      setShowTestAdvisor(false);
    }
    
    // Show success message
    setError(null);
  };

  // Download report
  const handleDownloadReport = () => {
    if (jobStatus?.status === 'done' && jobStatus.result_url) {
      window.open(jobStatus.result_url, '_blank');
    }
  };

  // Trigger file upload
  const handleTriggerUpload = () => {
    fileInputRef.current?.click();
  };

  // Handle file change and clear previous results
  const handleFileChange = (newFile: File | null) => {
    setFile(newFile);
    // Clear previous results when new file is selected
    setJobId(null);
    setJobStatus(null);
    setPreview(null);
  };

  // Validate and preview uploaded file
  const handleValidate = async (fileToValidate?: File) => {
    const targetFile = fileToValidate || file;
    
    if (!targetFile) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);
    
    // Clear previous results when validating new file
    setJobId(null);
    setJobStatus(null);

    try {
      // Debug: Check what we're actually sending
      console.log('=== FRONTEND DEBUG ===');
      console.log('targetFile:', targetFile);
      console.log('targetFile type:', typeof targetFile);
      console.log('targetFile instanceof File:', targetFile instanceof File);
      console.log('targetFile instanceof Blob:', targetFile instanceof Blob);
      console.log('targetFile.name:', targetFile?.name);
      console.log('targetFile.size:', targetFile?.size);
      console.log('targetFile.type:', targetFile?.type);
      
      const formData = new FormData();
      formData.append('file', targetFile);
      
      // Debug: Check FormData contents
      console.log('FormData entries:');
      for (let pair of formData.entries()) {
        console.log(pair[0], ':', pair[1]);
        console.log('Value type:', typeof pair[1]);
        console.log('Value instanceof File:', pair[1] instanceof File);
      }
      console.log('=== END FRONTEND DEBUG ===');

      const response = await axios.post('/api/validate', formData, {
        headers: {
          'Content-Type': undefined  // Let browser set it with boundary
        }
      });

      setPreview(response.data.preview);
      
      if (response.data.issues && response.data.issues.length > 0) {
        console.warn('Data quality issues:', response.data.issues);
      }
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to validate file');
      console.error('Validation error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Start analysis job
  const handleAnalyze = async () => {
    // Power analysis doesn't need a file
    if (!file && analysisType !== 'power') {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);
    setJobId(null);
    setJobStatus(null);

    try {
      const formData = new FormData();
      
      // Power analysis doesn't need a file, but backend expects one
      // So we create a dummy file
      if (analysisType === 'power') {
        const dummyFile = new Blob(['dummy'], { type: 'text/plain' });
        formData.append('file', dummyFile, 'dummy.txt');
      } else {
        formData.append('file', file!);
      }
      
      // Map frontend analysis types to backend types
      let backendAnalysisType = analysisType;
      if (analysisType === 'multiple-regression') {
        backendAnalysisType = 'regression';
      }
      
      // Clean options - remove empty arrays and placeholder values
      const cleanedOptions = { ...options };
      if (cleanedOptions.independentVars) {
        cleanedOptions.independentVars = cleanedOptions.independentVars.filter(
          (v: string) => v && !v.startsWith('<') && !v.endsWith('>')
        );
        if (cleanedOptions.independentVars.length === 0) {
          delete cleanedOptions.independentVars;
        }
      }
      
      formData.append('analysisType', backendAnalysisType);
      formData.append('options', JSON.stringify({ analysisType: backendAnalysisType, ...cleanedOptions }));

      const response = await axios.post('/api/analyze', formData);

      setJobId(response.data.job_id);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to start analysis');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Keyboard shortcuts
  useKeyboardShortcuts([
    {
      key: 'u',
      ctrl: true,
      action: handleTriggerUpload,
      description: 'Upload file'
    },
    {
      key: 'Enter',
      ctrl: true,
      action: handleAnalyze,
      description: 'Run analysis'
    },
    {
      key: 'd',
      ctrl: true,
      action: handleDownloadReport,
      description: 'Download report'
    },
    {
      key: 'k',
      ctrl: true,
      action: handleClearData,
      description: 'Clear data'
    },
    {
      key: '?',
      ctrl: true,
      action: () => setShowShortcutsHelp(true),
      description: 'Show keyboard shortcuts'
    },
    {
      key: 'Escape',
      action: () => setShowShortcutsHelp(false),
      description: 'Close modal'
    }
  ]);

  // Poll job status
  useEffect(() => {
    if (!jobId) return;

    const pollInterval = setInterval(async () => {
      try {
        const response = await axios.get(`/api/job-status?id=${jobId}`);
        setJobStatus(response.data);

        if (response.data.status === 'done' || response.data.status === 'failed') {
          clearInterval(pollInterval);
        }
      } catch (err) {
        console.error('Failed to fetch job status:', err);
      }
    }, 2000);

    return () => clearInterval(pollInterval);
  }, [jobId]);

  // Password authentication screen
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full">
          <div className="text-center mb-8">
            <div className="inline-block p-4 bg-blue-100 rounded-full mb-4">
              <svg className="w-12 h-12 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">GradStat</h1>
            <p className="text-gray-600">Testing Access Required</p>
          </div>
          
          <div className="space-y-4">
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                Testing Password
              </label>
              <input
                id="password"
                type="password"
                value={testingPassword}
                onChange={(e) => setTestingPassword(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && testingPassword) {
                    // Configure axios before authenticating
                    axios.defaults.baseURL = API_BASE_URL;
                    axios.defaults.headers.common['X-Testing-Password'] = testingPassword;
                    setIsAuthenticated(true);
                  }
                }}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter password"
                autoFocus
              />
            </div>
            
            <button
              onClick={() => {
                if (testingPassword) {
                  // Configure axios before authenticating
                  axios.defaults.baseURL = API_BASE_URL;
                  axios.defaults.headers.common['X-Testing-Password'] = testingPassword;
                  setIsAuthenticated(true);
                } else {
                  alert('Please enter a password');
                }
              }}
              className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors font-semibold text-lg shadow-lg hover:shadow-xl"
            >
              🔓 Access GradStat
            </button>
            
            <p className="text-xs text-gray-500 text-center mt-4">
              This is a testing environment. Contact the administrator for access credentials.
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Show home page if enabled and no data uploaded
  if (showHomePage && !file && !preview && !showTestAdvisor && !showPowerAnalysis) {
    return (
      <HomePage
        onGetStarted={() => setShowHomePage(false)}
        onTestAdvisor={() => {
          setShowHomePage(false);
          setShowTestAdvisor(true);
        }}
      />
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={() => {
                  setShowHomePage(true);
                  setFile(null);
                  setPreview(null);
                  setShowTestAdvisor(false);
                  setShowPowerAnalysis(false);
                  setJobId(null);
                  setJobStatus(null);
                }}
                className="text-gray-600 hover:text-gray-900 transition-colors"
                title="Go to Home"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
              </button>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  GradStat
                </h1>
                <p className="text-sm text-gray-600 mt-1">
                  Automated Statistical Analysis for Postgraduate Research
                </p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <button 
                onClick={() => {
                  setShowTestAdvisor(true);
                  setShowPowerAnalysis(false);
                  setFile(null);
                  setPreview(null);
                  setJobId(null);
                  setJobStatus(null);
                }}
                className="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors font-semibold text-sm"
              >
                🧭 Test Advisor
              </button>
              <button 
                onClick={() => {
                  setShowPowerAnalysis(true);
                  setShowTestAdvisor(false);
                  setAnalysisType('power');
                  setFile(null);
                  setPreview(null);
                  setJobId(null);
                  setJobStatus(null);
                  // Initialize power analysis defaults
                  setOptions({
                    powerAnalysisType: 't-test',
                    calculate: 'sample_size',
                    effectSize: 0.5,
                    alpha: 0.05,
                    power: 0.8,
                    sampleSize: 30,
                    nGroups: 2
                  });
                }}
                className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors font-semibold text-sm"
              >
                📊 Power Analysis
              </button>
              <button 
                onClick={() => {
                  setShowPowerAnalysis(false);
                  setShowTestAdvisor(false);
                  setAnalysisType('descriptive');
                  setJobId(null);
                  setJobStatus(null);
                }}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold text-sm"
              >
                📈 Data Analysis
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error Alert */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <p className="text-sm text-red-700 mt-1">{error}</p>
              </div>
              <button
                onClick={() => setError(null)}
                className="ml-auto text-red-400 hover:text-red-600"
              >
                <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        )}

        {showTestAdvisor ? (
          /* Test Advisor Mode */
          <div className="max-w-4xl mx-auto">
            <TestAdvisor onSelectTest={handleSelectTest} />
          </div>
        ) : showPowerAnalysis ? (
          /* Power Analysis Mode */
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold text-gray-900">📊 Statistical Power Analysis</h2>
                <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-semibold">No Data Upload Needed</span>
              </div>
              <p className="text-gray-600 mb-6">
                Calculate required sample sizes, statistical power, or detectable effect sizes for your research study.
              </p>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <AnalysisSelector
                analysisType="power"
                onAnalysisTypeChange={setAnalysisType}
                options={options}
                onOptionsChange={setOptions}
                columns={[]}
                columnTypes={{}}
                onAnalyze={handleAnalyze}
                loading={loading}
              />
              
              <div className="space-y-6">
                {jobId && (
                  <JobStatus
                    jobId={jobId}
                    status={jobStatus}
                  />
                )}

                {jobStatus?.status === 'done' && jobId && (
                  <Results
                    jobId={jobId}
                    resultUrl={jobStatus.result_url}
                    resultMeta={jobStatus.result_meta}
                  />
                )}
              </div>
            </div>
          </div>
        ) : (
          /* Normal Data Analysis Mode */
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left Column - Upload & Configuration */}
            <div className="lg:col-span-1 space-y-6">
              <DataUpload
                file={file}
                onFileChange={handleFileChange}
                onValidate={handleValidate}
                loading={loading}
                fileInputRef={fileInputRef}
              />

              {/* Example Datasets Button */}
              {!file && (
                <div className="flex justify-center">
                  <ExampleDatasets
                    onSelectDataset={async (exampleFile, recommendedAnalysis) => {
                      setFile(exampleFile);
                      setAnalysisType(recommendedAnalysis);
                      // Validate immediately with the file
                      handleValidate(exampleFile);
                    }}
                  />
                </div>
              )}

              {preview && (
                <AnalysisSelector
                  analysisType={analysisType}
                  onAnalysisTypeChange={setAnalysisType}
                  options={options}
                  onOptionsChange={setOptions}
                  columns={preview.columns}
                  columnTypes={preview.types}
                  onAnalyze={handleAnalyze}
                  loading={loading}
                />
              )}
            </div>

            {/* Right Column - Preview & Results */}
            <div className="lg:col-span-2 space-y-6">
              {preview && (
                <>
                  {/* Data Quality Report */}
                  {(preview as any).quality_report && (
                    <DataQualityReport report={(preview as any).quality_report} />
                  )}
                  
                  {/* Data Preview */}
                  <DataPreview preview={preview} />
                </>
              )}

              {jobId && (
                <JobStatus
                  jobId={jobId}
                  status={jobStatus}
                />
              )}

              {jobStatus?.status === 'done' && jobId && (
                <Results
                  jobId={jobId}
                  resultUrl={jobStatus.result_url}
                  resultMeta={jobStatus.result_meta}
                />
              )}
            </div>
          </div>
        )}

        {/* Info Cards */}
        {!preview && !jobId && (
          <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Upload Your Data</h3>
              <p className="text-sm text-gray-600">
                Support for CSV and Excel files. Automatic type detection and data quality checks.
              </p>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Automated Analysis</h3>
              <p className="text-sm text-gray-600">
                Choose from 7+ analysis types. Automatic assumption checking and model selection.
              </p>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Export Reports</h3>
              <p className="text-sm text-gray-600">
                Download comprehensive reports, plots, and reproducible code (Jupyter notebooks).
              </p>
            </div>
          </div>
        )}
      </main>

      {/* Keyboard Shortcuts Help Modal */}
      <KeyboardShortcutsHelp 
        isOpen={showShortcutsHelp} 
        onClose={() => setShowShortcutsHelp(false)} 
      />

      {/* Feedback Form */}
      <FeedbackForm analysisType={analysisType} />

      {/* Footer */}
      <footer className="mt-16 bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <p className="text-sm text-gray-500">
              GradStat v1.0.0 — Built for graduate researchers
            </p>
            <button
              onClick={() => setShowShortcutsHelp(true)}
              className="text-sm text-blue-600 hover:text-blue-800 flex items-center gap-1"
              title="Keyboard Shortcuts (Ctrl+?)"
            >
              ⌨️ Shortcuts
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
