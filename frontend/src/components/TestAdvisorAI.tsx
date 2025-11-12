import React, { useState } from 'react';
import axios from 'axios';

// Configure API base URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';

interface TestAdvisorAIProps {
  dataSummary?: any;
  currentAnswers?: any;
  onRecommendation?: (recommendation: string) => void;
}

const TestAdvisorAI: React.FC<TestAdvisorAIProps> = ({ dataSummary, currentAnswers, onRecommendation }) => {
  const [activeTab, setActiveTab] = useState<'recommend' | 'ask' | 'compare'>('recommend');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Research Assistant state
  const [description, setDescription] = useState('');
  const [recommendation, setRecommendation] = useState<any>(null);
  
  // Ask AI state
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [chatHistory, setChatHistory] = useState<Array<{q: string, a: string}>>([]);
  
  // Compare Tests state
  const [test1, setTest1] = useState('');
  const [test2, setTest2] = useState('');
  const [comparison, setComparison] = useState<any>(null);

  const handleGetRecommendation = async () => {
    if (!description.trim()) {
      setError('Please describe your research scenario');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(`${API_BASE_URL}/api/test-advisor/recommend`, {
        description,
        data_summary: dataSummary
      });
      
      setRecommendation(response.data);
      if (onRecommendation && response.data.recommendation) {
        onRecommendation(response.data.recommendation);
      }
    } catch (err: any) {
      console.error('Recommendation error:', err);
      setError(err.response?.data?.error || 'Failed to get recommendation');
    } finally {
      setLoading(false);
    }
  };

  const handleAskQuestion = async () => {
    if (!question.trim()) {
      setError('Please enter a question');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(`${API_BASE_URL}/api/test-advisor/ask`, {
        question,
        context: {
          current_answers: currentAnswers,
          data_summary: dataSummary
        }
      });
      
      setAnswer(response.data.answer);
      setChatHistory([...chatHistory, { q: question, a: response.data.answer }]);
      setQuestion('');
    } catch (err: any) {
      console.error('Question error:', err);
      setError(err.response?.data?.error || 'Failed to answer question');
    } finally {
      setLoading(false);
    }
  };

  const handleCompareTests = async () => {
    if (!test1.trim() || !test2.trim()) {
      setError('Please enter both test names');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(`${API_BASE_URL}/api/test-advisor/compare`, {
        test1,
        test2,
        context: {
          data_summary: dataSummary
        }
      });
      
      setComparison(response.data);
    } catch (err: any) {
      console.error('Comparison error:', err);
      setError(err.response?.data?.error || 'Failed to compare tests');
    } finally {
      setLoading(false);
    }
  };

  const suggestedQuestions = [
    "What's the difference between paired and independent samples?",
    "How do I know if my data is normally distributed?",
    "What sample size do I need for a t-test?",
    "When should I use ANOVA instead of t-test?",
    "What are the assumptions of linear regression?"
  ];

  const commonTests = [
    "Independent t-test",
    "Paired t-test",
    "One-way ANOVA",
    "Chi-square test",
    "Pearson correlation",
    "Mann-Whitney U test",
    "Wilcoxon signed-rank test",
    "Linear regression"
  ];

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <span className="text-3xl">🤖</span>
          <h2 className="text-2xl font-bold text-gray-800">AI Research Assistant</h2>
        </div>
        <p className="text-gray-600">Get intelligent guidance for statistical test selection</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6 border-b border-gray-200">
        <button
          onClick={() => setActiveTab('recommend')}
          className={`px-4 py-2 font-medium transition-colors ${
            activeTab === 'recommend'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          💡 Get Recommendation
        </button>
        <button
          onClick={() => setActiveTab('ask')}
          className={`px-4 py-2 font-medium transition-colors ${
            activeTab === 'ask'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          💬 Ask Questions
        </button>
        <button
          onClick={() => setActiveTab('compare')}
          className={`px-4 py-2 font-medium transition-colors ${
            activeTab === 'compare'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          ⚖️ Compare Tests
        </button>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-800 text-sm">⚠️ {error}</p>
        </div>
      )}

      {/* Recommend Tab */}
      {activeTab === 'recommend' && (
        <div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Describe your research scenario:
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Example: I have blood pressure measurements from 50 patients before and after treatment. I want to know if the treatment was effective..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              rows={4}
            />
          </div>

          {dataSummary && (
            <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-sm text-blue-900">
                📊 <strong>Data uploaded:</strong> {dataSummary.n_rows} rows, {dataSummary.n_columns} columns
              </p>
            </div>
          )}

          <button
            onClick={handleGetRecommendation}
            disabled={loading || !description.trim()}
            className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed transition-all"
          >
            {loading ? '⏳ Analyzing...' : '🚀 Get AI Recommendation'}
          </button>

          {recommendation && recommendation.recommendation && (
            <div className="mt-6 p-6 bg-gradient-to-br from-blue-50 to-purple-50 border-2 border-blue-200 rounded-lg">
              <div className="flex items-center gap-2 mb-4">
                <span className="text-2xl">✨</span>
                <h3 className="text-lg font-bold text-gray-800">AI Recommendation</h3>
              </div>
              <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-wrap">
                {recommendation.recommendation}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Ask Tab */}
      {activeTab === 'ask' && (
        <div>
          {/* Chat History */}
          {chatHistory.length > 0 && (
            <div className="mb-4 space-y-3 max-h-96 overflow-y-auto">
              {chatHistory.map((chat, idx) => (
                <div key={idx} className="space-y-2">
                  <div className="flex justify-end">
                    <div className="bg-blue-600 text-white px-4 py-2 rounded-lg max-w-[80%]">
                      <p className="text-sm">{chat.q}</p>
                    </div>
                  </div>
                  <div className="flex justify-start">
                    <div className="bg-gray-100 text-gray-800 px-4 py-2 rounded-lg max-w-[80%]">
                      <p className="text-sm whitespace-pre-wrap">{chat.a}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Current Answer */}
          {answer && chatHistory.length === 0 && (
            <div className="mb-4 p-4 bg-gray-50 border border-gray-200 rounded-lg">
              <p className="text-sm text-gray-700 whitespace-pre-wrap">{answer}</p>
            </div>
          )}

          {/* Suggested Questions */}
          {chatHistory.length === 0 && (
            <div className="mb-4">
              <p className="text-sm font-medium text-gray-700 mb-2">💡 Suggested questions:</p>
              <div className="flex flex-wrap gap-2">
                {suggestedQuestions.map((q, idx) => (
                  <button
                    key={idx}
                    onClick={() => setQuestion(q)}
                    className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full transition-colors"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Question Input */}
          <div className="flex gap-2">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleAskQuestion()}
              placeholder="Ask a question about statistical tests..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button
              onClick={handleAskQuestion}
              disabled={loading || !question.trim()}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? '⏳' : '📤'}
            </button>
          </div>
        </div>
      )}

      {/* Compare Tab */}
      {activeTab === 'compare' && (
        <div>
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                First Test:
              </label>
              <select
                value={test1}
                onChange={(e) => setTest1(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select test...</option>
                {commonTests.map((test) => (
                  <option key={test} value={test}>{test}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Second Test:
              </label>
              <select
                value={test2}
                onChange={(e) => setTest2(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select test...</option>
                {commonTests.map((test) => (
                  <option key={test} value={test}>{test}</option>
                ))}
              </select>
            </div>
          </div>

          <button
            onClick={handleCompareTests}
            disabled={loading || !test1 || !test2}
            className="w-full px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg font-semibold hover:from-purple-700 hover:to-pink-700 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed transition-all"
          >
            {loading ? '⏳ Comparing...' : '⚖️ Compare Tests'}
          </button>

          {comparison && comparison.comparison && (
            <div className="mt-6 p-6 bg-gradient-to-br from-purple-50 to-pink-50 border-2 border-purple-200 rounded-lg">
              <div className="flex items-center gap-2 mb-4">
                <span className="text-2xl">⚖️</span>
                <h3 className="text-lg font-bold text-gray-800">Comparison</h3>
              </div>
              <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-wrap">
                {comparison.comparison}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default TestAdvisorAI;
