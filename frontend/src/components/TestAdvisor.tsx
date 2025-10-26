/**
 * Test Advisor - Interactive Wizard
 * Helps users select the appropriate statistical test
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ConfidenceBadge from './ConfidenceBadge';
import AnalysisSummary from './AnalysisSummary';

interface TestRecommendation {
  test_name: string;
  analysis_type: string;
  plain_english: string;
  when_to_use: string[];
  example: string;
  assumptions: string[];
  sample_size_min: number;
  interpretation: string;
  confidence: string;
  gradstat_options: any;
  sample_size_warning?: string;
}

interface TestAdvisorProps {
  onSelectTest: (testInfo: TestRecommendation, file: File | null, skipValidation?: boolean) => void;
}

// Auto-Detect Button Component
interface AutoDetectButtonProps {
  questionKey: string;
  onDetect: (questionKey: string) => void;
  loading: boolean;
  disabled?: boolean;
}

const AutoDetectButton: React.FC<AutoDetectButtonProps> = ({ 
  questionKey, 
  onDetect, 
  loading,
  disabled = false
}) => {
  return (
    <button
      onClick={() => onDetect(questionKey)}
      disabled={loading || disabled}
      className="mt-3 flex items-center gap-2 text-blue-600 hover:text-blue-800 
                 disabled:text-gray-400 disabled:cursor-not-allowed transition-colors
                 font-medium text-sm"
    >
      {loading ? (
        <>
          <span className="animate-spin">⏳</span>
          <span>Analyzing your data...</span>
        </>
      ) : (
        <>
          <span>✨</span>
          <span>I'm not sure - Test it for me</span>
        </>
      )}
    </button>
  );
};

// Auto-Detect Result Display Component
interface AutoDetectResultProps {
  result: any;
  onDismiss: () => void;
}

const AutoDetectResult: React.FC<AutoDetectResultProps> = ({ result, onDismiss }) => {
  const confidenceColors: Record<string, string> = {
    high: 'bg-green-50 border-green-200',
    medium: 'bg-yellow-50 border-yellow-200',
    low: 'bg-red-50 border-red-200'
  };
  const confidenceColor = confidenceColors[result.confidence] || 'bg-gray-50 border-gray-200';

  const confidenceBadges: Record<string, string> = {
    high: 'bg-green-100 text-green-800',
    medium: 'bg-yellow-100 text-yellow-800',
    low: 'bg-red-100 text-red-800'
  };
  const confidenceBadge = confidenceBadges[result.confidence] || 'bg-gray-100 text-gray-800';

  return (
    <div className={`mt-3 p-4 rounded-lg border-2 ${confidenceColor} animate-fadeIn`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-lg">🤖</span>
            <span className="font-semibold text-gray-900">Auto-Detection Result</span>
            <span className={`px-2 py-1 rounded text-xs font-medium ${confidenceBadge}`}>
              {result.confidence.toUpperCase()} CONFIDENCE
            </span>
          </div>
          
          <p className="text-sm text-gray-700 mb-2">
            {result.explanation}
          </p>

          {result.details && Object.keys(result.details).length > 0 && (
            <details className="mt-2">
              <summary className="text-xs text-gray-600 cursor-pointer hover:text-gray-800 font-medium">
                View technical details
              </summary>
              <pre className="mt-2 text-xs bg-white p-2 rounded overflow-x-auto border border-gray-200">
                {JSON.stringify(result.details, null, 2)}
              </pre>
            </details>
          )}
        </div>

        <button
          onClick={onDismiss}
          className="text-gray-400 hover:text-gray-600 ml-2 text-lg font-bold"
          title="Dismiss"
        >
          ✕
        </button>
      </div>
    </div>
  );
};

const TestAdvisor: React.FC<TestAdvisorProps> = ({ onSelectTest }) => {
  const [step, setStep] = useState(1);
  const [answers, setAnswers] = useState<any>({});
  const [recommendations, setRecommendations] = useState<TestRecommendation[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [autoDetectLoading, setAutoDetectLoading] = useState<string | null>(null);
  const [autoDetectResult, setAutoDetectResult] = useState<any>(null);
  const [preAnalysisResults, setPreAnalysisResults] = useState<any>(null);
  const [analyzingDataset, setAnalyzingDataset] = useState(false);
  const [showSummary, setShowSummary] = useState(false);

  // Auto-fetch recommendations for simple research questions
  useEffect(() => {
    const autoFetchQuestions = ['describe_data'];  // Only describe_data auto-fetches now
    if (step === 2 && autoFetchQuestions.includes(answers.researchQuestion)) {
      getRecommendations();
    }
  }, [step, answers.researchQuestion]);

  const handleAnswer = (key: string, value: any) => {
    setAnswers({ ...answers, [key]: value });
  };

  const nextStep = () => setStep(step + 1);
  const prevStep = () => setStep(step - 1);

  const getRecommendations = async () => {
    setLoading(true);
    try {
      // Include survival data in answers if available
      const answersWithData = { ...answers };
      if (preAnalysisResults?.survival && answers.researchQuestion === 'survival_analysis') {
        answersWithData._survivalData = preAnalysisResults.survival;
      }
      
      console.log('Sending answers:', answersWithData);
      const response = await axios.post('/api/test-advisor/recommend', answersWithData);
      console.log('Received response:', response.data);
      
      if (response.data.ok && response.data.recommendations) {
        setRecommendations(response.data.recommendations);
        setStep(99); // Results step
      } else {
        console.error('Invalid response format:', response.data);
        alert('Error: Invalid response from server');
      }
    } catch (error: any) {
      console.error('Error getting recommendations:', error);
      alert(`Error: ${error.response?.data?.error || error.message || 'Failed to get recommendations'}`);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setStep(1);
    setAnswers({});
    setRecommendations([]);
    setUploadedFile(null);
    setAutoDetectResult(null);
    setPreAnalysisResults(null);
    setShowSummary(false);
  };

  const reAnalyze = () => {
    if (uploadedFile) {
      setPreAnalysisResults(null);
      setShowSummary(false);
      setAnswers({});
      analyzeDataset(uploadedFile);
    }
  };

  const skipToRecommendations = () => {
    // Get recommendations directly without going through wizard
    getRecommendations();
  };

  // Helper to check if an answer was auto-detected
  const isAutoDetected = (questionKey: string, value: any): boolean => {
    if (!preAnalysisResults) return false;
    
    // Check if this specific answer matches the pre-analysis result
    const result = preAnalysisResults[questionKey];
    if (result === null || result === undefined) return false;
    
    // Handle nGroups special case (2 vs '2')
    if (questionKey === 'nGroups') {
      return (result === 2 && value === 2) || (result === 3 && value === 3) || (result > 3 && value === 3);
    }
    
    return result === value;
  };

  // Get confidence for a question
  const getConfidence = (questionKey: string): 'high' | 'medium' | 'low' | null => {
    if (!preAnalysisResults?.confidence) return null;
    return preAnalysisResults.confidence[questionKey] || null;
  };

  const analyzeDataset = async (file: File) => {
    setAnalyzingDataset(true);
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post('/api/test-advisor/analyze-dataset', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      if (response.data.ok) {
        setPreAnalysisResults(response.data);
        setShowSummary(true); // Show summary panel
        
        // Auto-fill all answers based on research question
        const newAnswers: any = {};
        
        // Compare Groups answers
        if (response.data.isNormal !== null) newAnswers.isNormal = response.data.isNormal;
        if (response.data.nGroups !== null) newAnswers.nGroups = response.data.nGroups === 2 ? '2' : '3+';
        if (response.data.isPaired !== null) newAnswers.isPaired = response.data.isPaired;
        if (response.data.outcomeType !== null) newAnswers.outcomeType = response.data.outcomeType;
        
        // Find Relationships answers
        if (response.data.var1Type !== null) newAnswers.var1Type = response.data.var1Type;
        if (response.data.var2Type !== null) newAnswers.var2Type = response.data.var2Type;
        
        // Predict Outcome & Find Relationships shared
        if (response.data.nPredictors !== null) newAnswers.nPredictors = response.data.nPredictors;
        
        // Survival Analysis answers
        if (response.data.survival) {
          if (response.data.survival.has_groups !== null) {
            newAnswers.hasGroups = response.data.survival.has_groups;
          }
          if (response.data.survival.has_covariates !== null) {
            newAnswers.hasCovariates = response.data.survival.has_covariates;
          }
        }
        
        // PCA answers
        if (response.data.pca) {
          if (response.data.pca.suggested_components !== null) {
            newAnswers.nComponents = response.data.pca.suggested_components;
          }
          if (response.data.pca.scaling_needed !== null) {
            newAnswers.scaling = response.data.pca.scaling_needed;
          }
        }
        
        // Clustering answers
        if (response.data.clustering) {
          if (response.data.clustering.suggested_k !== null) {
            newAnswers.nClusters = response.data.clustering.suggested_k;
          }
          if (response.data.clustering.suggested_algorithm !== null) {
            newAnswers.algorithm = response.data.clustering.suggested_algorithm;
          }
        }
        
        setAnswers({ ...answers, ...newAnswers });
        
        console.log('Pre-analysis complete:', response.data);
      }
    } catch (error: any) {
      console.error('Dataset analysis error:', error);
      // Don't show error to user - pre-analysis is optional
    } finally {
      setAnalyzingDataset(false);
    }
  };

  const handleAutoDetect = async (questionKey: string) => {
    if (!uploadedFile) {
      alert('Please upload your data file first to use auto-detection!');
      return;
    }

    setAutoDetectLoading(questionKey);
    setAutoDetectResult(null);

    try {
      const formData = new FormData();
      formData.append('file', uploadedFile);
      formData.append('questionKey', questionKey);

      const response = await axios.post('/api/test-advisor/auto-answer', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      if (response.data.ok) {
        // Auto-fill the answer
        setAnswers({
          ...answers,
          [questionKey]: response.data.answer,
          [`${questionKey}_autoDetected`]: true,
          [`${questionKey}_confidence`]: response.data.confidence
        });

        // Show explanation
        setAutoDetectResult({
          questionKey,
          ...response.data
        });
      }
    } catch (error: any) {
      console.error('Auto-detect error:', error);
      alert(`Error: ${error.response?.data?.error || error.message || 'Failed to auto-detect'}`);
    } finally {
      setAutoDetectLoading(null);
    }
  };

  // Step 1: Research Question
  if (step === 1) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">🧭 Statistical Test Advisor</h2>
        <p className="text-gray-600 mb-6">Let us help you find the right test for your research!</p>

        {/* File Upload Prompt */}
        {!uploadedFile && (
          <div className="mb-6 p-4 bg-blue-50 border-2 border-blue-200 rounded-lg">
            <div className="flex items-start gap-3">
              <span className="text-2xl">💡</span>
              <div className="flex-1">
                <h4 className="font-semibold text-blue-900 mb-1">
                  Pro Tip: Upload Your Data First!
                </h4>
                <p className="text-sm text-blue-800 mb-3">
                  Upload your data file now, and we can automatically answer questions 
                  for you as you go through the wizard. ✨
                </p>
                <input
                  type="file"
                  accept=".csv,.xlsx,.xls"
                  onChange={(e) => {
                    if (e.target.files?.[0]) {
                      const file = e.target.files[0];
                      setUploadedFile(file);
                      // Automatically analyze dataset
                      analyzeDataset(file);
                    }
                  }}
                  className="text-sm file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 
                           file:text-sm file:font-semibold file:bg-blue-600 file:text-white 
                           hover:file:bg-blue-700 file:cursor-pointer"
                />
              </div>
            </div>
          </div>
        )}

        {/* File Uploaded Success */}
        {uploadedFile && !showSummary && (
          <div className="mb-6 p-4 bg-green-50 border-2 border-green-200 rounded-lg">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-2xl">{analyzingDataset ? '⏳' : '✅'}</span>
                <div>
                  <h4 className="font-semibold text-green-900">
                    {analyzingDataset ? 'Analyzing Your Data...' : 'Data File Uploaded!'}
                  </h4>
                  <p className="text-sm text-green-800">
                    {uploadedFile.name}
                    {analyzingDataset && ' - Running smart pre-analysis...'}
                    {!analyzingDataset && preAnalysisResults && ` - ${preAnalysisResults.summary?.confidence_rate} confidence`}
                    {!analyzingDataset && !preAnalysisResults && ' - Auto-detection enabled'}
                  </p>
                </div>
              </div>
              <div className="flex gap-2">
                {!analyzingDataset && preAnalysisResults && (
                  <button
                    onClick={reAnalyze}
                    className="text-blue-600 hover:text-blue-800 font-medium text-sm flex items-center gap-1"
                  >
                    <span>🔄</span>
                    <span>Re-analyze</span>
                  </button>
                )}
                <button
                  onClick={() => {
                    setUploadedFile(null);
                    setPreAnalysisResults(null);
                    setShowSummary(false);
                  }}
                  className="text-green-600 hover:text-green-800 font-medium text-sm"
                  disabled={analyzingDataset}
                >
                  Change File
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Analysis Summary Panel */}
        {showSummary && preAnalysisResults && (
          <AnalysisSummary
            results={preAnalysisResults}
            onStartWizard={() => setShowSummary(false)}
            onSkipToRecommendations={skipToRecommendations}
          />
        )}

        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <span className="text-sm font-medium text-gray-700">Step 1 of 4</span>
            <div className="flex gap-2">
              <div className="w-8 h-2 bg-blue-600 rounded"></div>
              <div className="w-8 h-2 bg-gray-200 rounded"></div>
              <div className="w-8 h-2 bg-gray-200 rounded"></div>
              <div className="w-8 h-2 bg-gray-200 rounded"></div>
            </div>
          </div>
        </div>

        <h3 className="text-lg font-semibold text-gray-900 mb-4">What's your research question?</h3>

        <div className="space-y-3">
          {[
            { value: 'compare_groups', label: 'Compare groups', example: '"Is treatment A better than B?"' },
            { value: 'find_relationships', label: 'Find relationships', example: '"Does age affect blood pressure?"' },
            { value: 'predict_outcome', label: 'Predict outcomes', example: '"Predict disease risk from symptoms"' },
            { value: 'describe_data', label: 'Describe data', example: '"Summarize patient demographics"' },
            { value: 'survival_analysis', label: 'Survival/time-to-event', example: '"Time until recovery"' },
            { value: 'reduce_dimensions', label: 'Reduce many variables', example: '"Simplify 20 survey questions"' },
            { value: 'find_groups', label: 'Find natural groups', example: '"Segment customers by behavior"' },
          ].map((option) => (
            <button
              key={option.value}
              onClick={() => {
                handleAnswer('researchQuestion', option.value);
                nextStep();
              }}
              className="w-full text-left p-4 border-2 border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors"
            >
              <div className="font-semibold text-gray-900">{option.label}</div>
              <div className="text-sm text-gray-600 mt-1">Example: {option.example}</div>
            </button>
          ))}
        </div>
      </div>
    );
  }

  // Step 2: Compare Groups Questions
  if (step === 2 && answers.researchQuestion === 'compare_groups') {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Compare Groups</h2>

        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <span className="text-sm font-medium text-gray-700">Step 2 of 4</span>
            <div className="flex gap-2">
              <div className="w-8 h-2 bg-blue-600 rounded"></div>
              <div className="w-8 h-2 bg-blue-600 rounded"></div>
              <div className="w-8 h-2 bg-gray-200 rounded"></div>
              <div className="w-8 h-2 bg-gray-200 rounded"></div>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold text-gray-900">How many groups?</h3>
              {getConfidence('nGroups') && (
                <ConfidenceBadge confidence={getConfidence('nGroups')!} size="sm" />
              )}
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => handleAnswer('nGroups', 2)}
                className={`flex-1 p-4 border-2 rounded-lg ${answers.nGroups === 2 ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-semibold">2 groups</div>
                    <div className="text-sm text-gray-600">Treatment vs Control</div>
                  </div>
                  {isAutoDetected('nGroups', 2) && (
                    <span className="text-xl" title="Auto-detected">✨</span>
                  )}
                </div>
              </button>
              <button
                onClick={() => handleAnswer('nGroups', 3)}
                className={`flex-1 p-4 border-2 rounded-lg ${answers.nGroups === 3 ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-semibold">3+ groups</div>
                    <div className="text-sm text-gray-600">Multiple treatments</div>
                  </div>
                  {isAutoDetected('nGroups', 3) && (
                    <span className="text-xl" title="Auto-detected">✨</span>
                  )}
                </div>
              </button>
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold text-gray-900">What type of outcome?</h3>
              {getConfidence('outcomeType') && (
                <ConfidenceBadge confidence={getConfidence('outcomeType')!} size="sm" />
              )}
            </div>
            <div className="space-y-2">
              {[
                { value: 'continuous', label: 'Continuous', example: 'height, weight, test scores' },
                { value: 'categorical', label: 'Categorical', example: 'yes/no, disease/healthy' },
              ].map((option) => (
                <button
                  key={option.value}
                  onClick={() => handleAnswer('outcomeType', option.value)}
                  className={`w-full text-left p-3 border-2 rounded-lg ${answers.outcomeType === option.value ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="font-semibold">{option.label}</div>
                      <div className="text-sm text-gray-600">e.g., {option.example}</div>
                    </div>
                    {isAutoDetected('outcomeType', option.value) && (
                      <span className="text-xl" title="Auto-detected">✨</span>
                    )}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {answers.outcomeType === 'continuous' && (
            <>
              <div>
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-lg font-semibold text-gray-900">Is your data normally distributed?</h3>
                  {getConfidence('isNormal') && (
                    <ConfidenceBadge confidence={getConfidence('isNormal')!} size="sm" />
                  )}
                </div>
                <div className="space-y-2">
                  {[
                    { value: true, label: 'Yes', desc: 'Bell-shaped curve' },
                    { value: false, label: 'No', desc: 'Skewed or has outliers' },
                  ].map((option) => (
                    <button
                      key={String(option.value)}
                      onClick={() => handleAnswer('isNormal', option.value)}
                      className={`w-full text-left p-3 border-2 rounded-lg ${answers.isNormal === option.value ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-semibold">{option.label}</div>
                          <div className="text-sm text-gray-600">{option.desc}</div>
                        </div>
                        {isAutoDetected('isNormal', option.value) && (
                          <span className="text-xl" title="Auto-detected">✨</span>
                        )}
                      </div>
                    </button>
                  ))}
                </div>

                {/* Auto-Detect Button */}
                <AutoDetectButton
                  questionKey="isNormal"
                  onDetect={handleAutoDetect}
                  loading={autoDetectLoading === 'isNormal'}
                  disabled={!uploadedFile}
                />

                {/* Show Result if Available */}
                {autoDetectResult?.questionKey === 'isNormal' && (
                  <AutoDetectResult
                    result={autoDetectResult}
                    onDismiss={() => setAutoDetectResult(null)}
                  />
                )}
              </div>

              {answers.nGroups === 2 && (
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-lg font-semibold text-gray-900">Are the groups independent or paired?</h3>
                    {getConfidence('isPaired') && (
                      <ConfidenceBadge confidence={getConfidence('isPaired')!} size="sm" />
                    )}
                  </div>
                  <div className="space-y-2">
                    {[
                      { value: false, label: 'Independent', desc: 'Different people in each group' },
                      { value: true, label: 'Paired', desc: 'Same people measured twice' },
                    ].map((option) => (
                      <button
                        key={String(option.value)}
                        onClick={() => handleAnswer('isPaired', option.value)}
                        className={`w-full text-left p-3 border-2 rounded-lg ${answers.isPaired === option.value ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <div className="font-semibold">{option.label}</div>
                            <div className="text-sm text-gray-600">{option.desc}</div>
                          </div>
                          {isAutoDetected('isPaired', option.value) && (
                            <span className="text-xl" title="Auto-detected">✨</span>
                          )}
                        </div>
                      </button>
                    ))}
                  </div>

                  {/* Auto-Detect Button */}
                  <AutoDetectButton
                    questionKey="isPaired"
                    onDetect={handleAutoDetect}
                    loading={autoDetectLoading === 'isPaired'}
                    disabled={!uploadedFile}
                  />

                  {/* Show Result if Available */}
                  {autoDetectResult?.questionKey === 'isPaired' && (
                    <AutoDetectResult
                      result={autoDetectResult}
                      onDismiss={() => setAutoDetectResult(null)}
                    />
                  )}
                </div>
              )}
            </>
          )}
        </div>

        <div className="flex gap-3 mt-6">
          <button
            onClick={prevStep}
            className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            ← Back
          </button>
          <button
            onClick={getRecommendations}
            disabled={!answers.outcomeType || (answers.outcomeType === 'continuous' && answers.isNormal === undefined)}
            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            Get Recommendations →
          </button>
        </div>
      </div>
    );
  }

  // Step 2: Find Relationships Questions
  if (step === 2 && answers.researchQuestion === 'find_relationships') {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Find Relationships</h2>

        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-3">What types of variables?</h3>
            <div className="space-y-2">
              {[
                { var1: 'continuous', var2: 'continuous', label: 'Both continuous', example: 'height & weight' },
                { var1: 'continuous', var2: 'categorical', label: 'One continuous, one categorical', example: 'score & group' },
                { var1: 'categorical', var2: 'categorical', label: 'Both categorical', example: 'gender & disease' },
              ].map((option, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => {
                    console.log('Clicked:', option.label);
                    const newAnswers = {
                      ...answers,
                      var1Type: option.var1,
                      var2Type: option.var2
                    };
                    console.log('Setting answers to:', newAnswers);
                    setAnswers(newAnswers);
                  }}
                  className={`w-full text-left p-3 border-2 rounded-lg transition-colors ${answers.var1Type === option.var1 && answers.var2Type === option.var2 ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
                >
                  <div className="font-semibold">{option.label}</div>
                  <div className="text-sm text-gray-600">e.g., {option.example}</div>
                </button>
              ))}
            </div>
          </div>

          {answers.var1Type === 'continuous' && answers.var2Type === 'continuous' && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">How many predictor variables?</h3>
              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => {
                    console.log('Selected: One predictor');
                    handleAnswer('nPredictors', 1);
                  }}
                  className={`flex-1 p-4 border-2 rounded-lg transition-colors ${answers.nPredictors === 1 ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
                >
                  <div className="font-semibold">One</div>
                  <div className="text-sm text-gray-600">Simple relationship</div>
                </button>
                <button
                  type="button"
                  onClick={() => {
                    console.log('Selected: Multiple predictors');
                    handleAnswer('nPredictors', 2);
                  }}
                  className={`flex-1 p-4 border-2 rounded-lg transition-colors ${answers.nPredictors === 2 ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
                >
                  <div className="font-semibold">Multiple</div>
                  <div className="text-sm text-gray-600">Complex relationship</div>
                </button>
              </div>
            </div>
          )}
        </div>

        <div className="flex gap-3 mt-6">
          <button
            type="button"
            onClick={prevStep}
            className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            ← Back
          </button>
          <button
            type="button"
            onClick={() => {
              console.log('Get Recommendations clicked, answers:', answers);
              getRecommendations();
            }}
            disabled={!answers.var1Type}
            className={`flex-1 px-4 py-2 rounded-lg transition-colors ${
              answers.var1Type 
                ? 'bg-blue-600 text-white hover:bg-blue-700 cursor-pointer' 
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            Get Recommendations → {answers.var1Type ? '✓' : ''}
          </button>
        </div>
      </div>
    );
  }

  // Step 2: Predict Outcome Questions
  if (step === 2 && answers.researchQuestion === 'predict_outcome') {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Predict Outcomes</h2>

        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-3">What type of outcome?</h3>
            <div className="space-y-2">
              {[
                { value: 'continuous', label: 'Continuous', example: 'salary, blood pressure' },
                { value: 'binary', label: 'Binary', example: 'yes/no, success/fail' },
              ].map((option) => (
                <button
                  key={option.value}
                  onClick={() => handleAnswer('outcomeType', option.value)}
                  className={`w-full text-left p-3 border-2 rounded-lg ${answers.outcomeType === option.value ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
                >
                  <div className="font-semibold">{option.label}</div>
                  <div className="text-sm text-gray-600">e.g., {option.example}</div>
                </button>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-3">How many predictors?</h3>
            <div className="flex gap-3">
              <button
                onClick={() => handleAnswer('nPredictors', 1)}
                className={`flex-1 p-4 border-2 rounded-lg ${answers.nPredictors === 1 ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
              >
                <div className="font-semibold">One</div>
              </button>
              <button
                onClick={() => handleAnswer('nPredictors', 2)}
                className={`flex-1 p-4 border-2 rounded-lg ${answers.nPredictors === 2 ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
              >
                <div className="font-semibold">Multiple</div>
              </button>
            </div>
          </div>
        </div>

        <div className="flex gap-3 mt-6">
          <button
            onClick={prevStep}
            className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            ← Back
          </button>
          <button
            onClick={getRecommendations}
            disabled={!answers.outcomeType}
            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300"
          >
            Get Recommendations →
          </button>
        </div>
      </div>
    );
  }

  // PCA (Reduce Dimensions) Questions
  if (step === 2 && answers.researchQuestion === 'reduce_dimensions') {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Reduce Dimensions (PCA)</h2>

        <div className="space-y-6">
          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold text-gray-900">How many components do you want?</h3>
              {getConfidence('nComponents') && (
                <ConfidenceBadge confidence={getConfidence('nComponents')!} size="sm" />
              )}
            </div>
            <input
              type="number"
              min="2"
              value={answers.nComponents || ''}
              onChange={(e) => handleAnswer('nComponents', parseInt(e.target.value))}
              placeholder={preAnalysisResults?.pca?.suggested_components ? `Suggested: ${preAnalysisResults.pca.suggested_components}` : 'Enter number'}
              className="w-full p-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none"
            />
            {preAnalysisResults?.pca?.suggested_components && (
              <p className="mt-2 text-sm text-gray-600">
                ✨ Suggested: {preAnalysisResults.pca.suggested_components} components from {preAnalysisResults.pca.n_numeric_vars} variables
              </p>
            )}
          </div>

          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold text-gray-900">Should we scale your variables?</h3>
              {getConfidence('scaling_pca') && (
                <ConfidenceBadge confidence={getConfidence('scaling_pca')!} size="sm" />
              )}
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => handleAnswer('scaling', true)}
                className={`flex-1 p-4 border-2 rounded-lg ${answers.scaling === true ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-semibold">Yes, scale</div>
                    <div className="text-sm text-gray-600">Recommended for different units</div>
                  </div>
                  {preAnalysisResults?.pca?.scaling_needed === true && (
                    <span className="text-xl" title="Auto-detected">✨</span>
                  )}
                </div>
              </button>
              <button
                onClick={() => handleAnswer('scaling', false)}
                className={`flex-1 p-4 border-2 rounded-lg ${answers.scaling === false ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-semibold">No scaling</div>
                    <div className="text-sm text-gray-600">Same units/scale</div>
                  </div>
                  {preAnalysisResults?.pca?.scaling_needed === false && (
                    <span className="text-xl" title="Auto-detected">✨</span>
                  )}
                </div>
              </button>
            </div>
          </div>
        </div>

        <div className="flex gap-3 mt-6">
          <button
            onClick={prevStep}
            className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            ← Back
          </button>
          <button
            onClick={getRecommendations}
            disabled={!answers.nComponents}
            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300"
          >
            Get Recommendations →
          </button>
        </div>
      </div>
    );
  }

  // Clustering (Find Groups) Questions
  if (step === 2 && answers.researchQuestion === 'find_groups') {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Find Natural Groups (Clustering)</h2>

        <div className="space-y-6">
          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold text-gray-900">How many groups do you expect?</h3>
              {getConfidence('nClusters') && (
                <ConfidenceBadge confidence={getConfidence('nClusters')!} size="sm" />
              )}
            </div>
            <input
              type="number"
              min="2"
              value={answers.nClusters || ''}
              onChange={(e) => handleAnswer('nClusters', parseInt(e.target.value))}
              placeholder={preAnalysisResults?.clustering?.suggested_k ? `Suggested: ${preAnalysisResults.clustering.suggested_k}` : 'Enter number'}
              className="w-full p-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none"
            />
            {preAnalysisResults?.clustering?.suggested_k && (
              <p className="mt-2 text-sm text-gray-600">
                ✨ Suggested: {preAnalysisResults.clustering.suggested_k} clusters
              </p>
            )}
          </div>

          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold text-gray-900">Which clustering method?</h3>
              {getConfidence('algorithm') && (
                <ConfidenceBadge confidence={getConfidence('algorithm')!} size="sm" />
              )}
            </div>
            <div className="space-y-2">
              {[
                { value: 'kmeans', label: 'K-Means', desc: 'Fast, spherical clusters' },
                { value: 'hierarchical', label: 'Hierarchical', desc: 'Dendrogram, flexible shapes' },
                { value: 'dbscan', label: 'DBSCAN', desc: 'Handles outliers, arbitrary shapes' },
              ].map((option) => (
                <button
                  key={option.value}
                  onClick={() => handleAnswer('algorithm', option.value)}
                  className={`w-full text-left p-3 border-2 rounded-lg ${answers.algorithm === option.value ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="font-semibold">{option.label}</div>
                      <div className="text-sm text-gray-600">{option.desc}</div>
                    </div>
                    {preAnalysisResults?.clustering?.suggested_algorithm === option.value && (
                      <span className="text-xl" title="Auto-detected">✨</span>
                    )}
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="flex gap-3 mt-6">
          <button
            onClick={prevStep}
            className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            ← Back
          </button>
          <button
            onClick={getRecommendations}
            disabled={!answers.nClusters || !answers.algorithm}
            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300"
          >
            Get Recommendations →
          </button>
        </div>
      </div>
    );
  }

  // Auto-recommendation questions - Show loading while fetching (useEffect at top handles the call)
  const autoFetchQuestions = ['describe_data'];
  if (step === 2 && autoFetchQuestions.includes(answers.researchQuestion) && loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Analyzing your data...</p>
        </div>
      </div>
    );
  }

  // Survival Analysis Questions
  if (step === 2 && answers.researchQuestion === 'survival_analysis') {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Survival Analysis</h2>

        <div className="space-y-6">
          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold text-gray-900">Do you want to compare groups?</h3>
              {getConfidence('hasGroups_survival') && (
                <ConfidenceBadge confidence={getConfidence('hasGroups_survival')!} size="sm" />
              )}
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => handleAnswer('hasGroups', true)}
                className={`flex-1 p-4 border-2 rounded-lg ${answers.hasGroups === true ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
              >
                <div className="flex items-center justify-between">
                  <span>Yes</span>
                  {preAnalysisResults?.survival?.has_groups === true && (
                    <span className="text-xl" title="Auto-detected">✨</span>
                  )}
                </div>
              </button>
              <button
                onClick={() => handleAnswer('hasGroups', false)}
                className={`flex-1 p-4 border-2 rounded-lg ${answers.hasGroups === false ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
              >
                <div className="flex items-center justify-between">
                  <span>No</span>
                  {preAnalysisResults?.survival?.has_groups === false && (
                    <span className="text-xl" title="Auto-detected">✨</span>
                  )}
                </div>
              </button>
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold text-gray-900">Do you have covariates to adjust for?</h3>
              {getConfidence('hasCovariates') && (
                <ConfidenceBadge confidence={getConfidence('hasCovariates')!} size="sm" />
              )}
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => handleAnswer('hasCovariates', true)}
                className={`flex-1 p-4 border-2 rounded-lg ${answers.hasCovariates === true ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
              >
                <div className="flex items-center justify-between">
                  <span>Yes</span>
                  {preAnalysisResults?.survival?.has_covariates === true && (
                    <span className="text-xl" title="Auto-detected">✨</span>
                  )}
                </div>
              </button>
              <button
                onClick={() => handleAnswer('hasCovariates', false)}
                className={`flex-1 p-4 border-2 rounded-lg ${answers.hasCovariates === false ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}`}
              >
                <div className="flex items-center justify-between">
                  <span>No</span>
                  {preAnalysisResults?.survival?.has_covariates === false && (
                    <span className="text-xl" title="Auto-detected">✨</span>
                  )}
                </div>
              </button>
            </div>
          </div>
        </div>

        <div className="flex gap-3 mt-6">
          <button
            onClick={prevStep}
            className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            ← Back
          </button>
          <button
            onClick={getRecommendations}
            disabled={answers.hasGroups === undefined}
            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300"
          >
            Get Recommendations →
          </button>
        </div>
      </div>
    );
  }

  // Results Step
  if (step === 99) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">📊 Recommended Tests</h2>
        <p className="text-gray-600 mb-6">Based on your answers, here are the best tests for your research:</p>

        {loading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Finding the best tests for you...</p>
          </div>
        ) : (
          <div className="space-y-4">
            {recommendations.map((test, idx) => (
              <div
                key={idx}
                className={`border-2 rounded-lg p-5 ${
                  test.confidence === 'high' ? 'border-green-500 bg-green-50' :
                  test.confidence === 'medium' ? 'border-yellow-500 bg-yellow-50' :
                  'border-gray-300'
                }`}
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="text-xl font-bold text-gray-900">{test.test_name}</h3>
                      {test.confidence === 'high' && <span className="px-2 py-1 bg-green-600 text-white text-xs rounded-full">✓ RECOMMENDED</span>}
                      {test.confidence === 'medium' && <span className="px-2 py-1 bg-yellow-600 text-white text-xs rounded-full">⚠ ALTERNATIVE</span>}
                    </div>
                    <p className="text-gray-700 mt-1">{test.plain_english}</p>
                  </div>
                </div>

                <div className="space-y-3">
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-1">📖 When to use:</h4>
                    <ul className="list-disc list-inside text-gray-700 space-y-1">
                      {test.when_to_use.map((item, i) => (
                        <li key={i}>{item}</li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-900 mb-1">💡 Example:</h4>
                    <p className="text-gray-700">{test.example}</p>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-900 mb-1">✓ Assumptions:</h4>
                    <div className="flex flex-wrap gap-2">
                      {test.assumptions.map((assumption, i) => (
                        <span key={i} className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                          {assumption}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-900 mb-1">📊 How to interpret:</h4>
                    <p className="text-gray-700">{test.interpretation}</p>
                  </div>

                  {test.sample_size_warning && (
                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                      <p className="text-sm text-yellow-800">{test.sample_size_warning}</p>
                    </div>
                  )}

                  <div className="pt-3 border-t">
                    <button
                      onClick={() => onSelectTest(test, uploadedFile, true)}
                      className="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold"
                    >
                      Use This Test →
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        <button
          onClick={reset}
          className="mt-6 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
        >
          ← Start Over
        </button>
      </div>
    );
  }

  return <div>Loading...</div>;
};

export default TestAdvisor;
