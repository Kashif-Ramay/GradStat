import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Configure API base URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';

interface AIInterpreterProps {
  analysisData: any;
}

const AIInterpreter: React.FC<AIInterpreterProps> = ({ analysisData }) => {
  const [interpretation, setInterpretation] = useState<any>(null);
  const [question, setQuestion] = useState('');
  const [conversation, setConversation] = useState<Array<{role: string, content: string}>>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'interpretation' | 'chat' | 'whatif'>('interpretation');
  const [error, setError] = useState<string | null>(null);

  // Debug: Log when component mounts
  useEffect(() => {
    console.log('AIInterpreter mounted with data:', analysisData);
  }, []);

  // Load initial interpretation
  useEffect(() => {
    if (analysisData && activeTab === 'interpretation' && !interpretation) {
      console.log('Loading interpretation...');
      loadInterpretation();
    }
  }, [analysisData, activeTab]);

  const loadInterpretation = async () => {
    console.log('loadInterpretation called');
    setLoading(true);
    setError(null);
    try {
      console.log('Sending interpretation request...');
      const response = await axios.post(`${API_BASE_URL}/api/interpret`, {
        analysis_type: analysisData.analysis_type || 'Unknown',
        sample_size: analysisData.sample_size || 0,
        variables: analysisData.variables || [],
        results: analysisData.results || {},
        assumptions: analysisData.assumptions || {}
      });
      console.log('Interpretation response:', response.data);
      setInterpretation(response.data);
    } catch (error: any) {
      console.error('Interpretation error:', error);
      console.error('Error response:', error.response);
      setError(error.response?.data?.error || error.response?.data?.detail || 'Failed to generate interpretation. AI features may not be available yet.');
    } finally {
      setLoading(false);
    }
  };

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_BASE_URL}/api/ask`, {
        question,
        analysis_data: {
          analysis_type: analysisData.analysis_type || 'Unknown',
          sample_size: analysisData.sample_size || 0,
          variables: analysisData.variables || [],
          results: analysisData.results || {},
          assumptions: analysisData.assumptions || {}
        },
        conversation_history: conversation
      });

      const newConversation = [
        ...conversation,
        { role: 'user', content: question },
        { role: 'assistant', content: response.data.answer }
      ];

      setConversation(newConversation);
      setQuestion('');
    } catch (error: any) {
      console.error('Question error:', error);
      setError(error.response?.data?.error || 'Failed to answer question');
    } finally {
      setLoading(false);
    }
  };

  const askWhatIf = async (scenario: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_BASE_URL}/api/what-if`, {
        scenario,
        analysis_data: {
          analysis_type: analysisData.analysis_type || 'Unknown',
          sample_size: analysisData.sample_size || 0,
          variables: analysisData.variables || [],
          results: analysisData.results || {},
          assumptions: analysisData.assumptions || {}
        }
      });

      const newConversation = [
        ...conversation,
        { role: 'user', content: `What if: ${scenario}` },
        { role: 'assistant', content: response.data.response }
      ];

      setConversation(newConversation);
    } catch (error: any) {
      console.error('What-if error:', error);
      setError(error.response?.data?.error || 'Failed to analyze scenario');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gradient-to-br from-purple-50 to-indigo-50 rounded-lg shadow-lg p-6 mt-6">
      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <div className="p-3 bg-purple-600 rounded-lg">
          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <div>
          <h2 className="text-2xl font-bold text-gray-900">🤖 AI Statistical Interpreter</h2>
          <p className="text-sm text-gray-600">Powered by GPT-4</p>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-start gap-2">
            <span className="text-red-600 text-xl">⚠️</span>
            <div>
              <p className="text-red-800 font-medium">Error</p>
              <p className="text-red-700 text-sm">{error}</p>
              {error.includes('API key') && (
                <p className="text-red-600 text-xs mt-2">
                  To enable AI features, add OPENAI_API_KEY to your environment variables.
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="flex gap-2 mb-6 border-b border-gray-200">
        <button
          onClick={() => setActiveTab('interpretation')}
          className={`px-4 py-2 font-medium transition-colors ${
            activeTab === 'interpretation'
              ? 'text-purple-600 border-b-2 border-purple-600'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          💡 Interpretation
        </button>
        <button
          onClick={() => setActiveTab('chat')}
          className={`px-4 py-2 font-medium transition-colors ${
            activeTab === 'chat'
              ? 'text-purple-600 border-b-2 border-purple-600'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          💬 Ask Questions
        </button>
        <button
          onClick={() => setActiveTab('whatif')}
          className={`px-4 py-2 font-medium transition-colors ${
            activeTab === 'whatif'
              ? 'text-purple-600 border-b-2 border-purple-600'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          🔮 What-If Scenarios
        </button>
      </div>

      {/* Loading Indicator */}
      {loading && (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
          <span className="ml-3 text-gray-600">AI is thinking...</span>
        </div>
      )}

      {/* Interpretation Tab */}
      {activeTab === 'interpretation' && !loading && (
        <div className="space-y-6">
          {interpretation ? (
            <>
              <div className="bg-white rounded-lg p-6 shadow">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">📊 Overall Interpretation</h3>
                <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">{interpretation.interpretation}</p>
              </div>

              {interpretation.key_findings && interpretation.key_findings.length > 0 && (
                <div className="bg-white rounded-lg p-6 shadow">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">🎯 Key Findings</h3>
                  <ul className="space-y-2">
                    {interpretation.key_findings.map((finding: string, idx: number) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-green-600 mt-1">✓</span>
                        <span className="text-gray-700">{finding}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {interpretation.concerns && interpretation.concerns.length > 0 && (
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-yellow-900 mb-3">⚠️ Concerns</h3>
                  <ul className="space-y-2">
                    {interpretation.concerns.map((concern: string, idx: number) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-yellow-600 mt-1">!</span>
                        <span className="text-yellow-800">{concern}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {interpretation.next_steps && interpretation.next_steps.length > 0 && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-blue-900 mb-3">🚀 Next Steps</h3>
                  <ul className="space-y-2">
                    {interpretation.next_steps.map((step: string, idx: number) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-blue-600 mt-1">→</span>
                        <span className="text-blue-800">{step}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </>
          ) : (
            <div className="text-center py-12 text-gray-500">
              <p>Click "Load Interpretation" to get AI insights</p>
              <button
                onClick={loadInterpretation}
                className="mt-4 px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
              >
                Load Interpretation
              </button>
            </div>
          )}
        </div>
      )}

      {/* Chat Tab */}
      {activeTab === 'chat' && !loading && (
        <div className="space-y-4">
          {/* Conversation History */}
          <div className="bg-white rounded-lg p-6 shadow max-h-96 overflow-y-auto">
            {conversation.length === 0 ? (
              <p className="text-gray-500 text-center py-8">
                Ask any question about your analysis results!
              </p>
            ) : (
              <div className="space-y-4">
                {conversation.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-lg p-4 ${
                        msg.role === 'user'
                          ? 'bg-purple-600 text-white'
                          : 'bg-gray-100 text-gray-900'
                      }`}
                    >
                      <p className="whitespace-pre-wrap">{msg.content}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Question Input */}
          <div className="flex gap-2">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && !loading && askQuestion()}
              placeholder="Ask a question about your results..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              disabled={loading}
            />
            <button
              onClick={askQuestion}
              disabled={loading || !question.trim()}
              className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Send
            </button>
          </div>

          {/* Suggested Questions */}
          <div className="flex flex-wrap gap-2">
            <span className="text-sm text-gray-600">Suggested:</span>
            {[
              "What does this p-value mean?",
              "Is my sample size adequate?",
              "How strong is this effect?",
              "What are the limitations?"
            ].map((q, idx) => (
              <button
                key={idx}
                onClick={() => setQuestion(q)}
                disabled={loading}
                className="text-sm px-3 py-1 bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors disabled:opacity-50"
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* What-If Tab */}
      {activeTab === 'whatif' && !loading && (
        <div className="space-y-4">
          <p className="text-gray-700 mb-4">
            Explore hypothetical scenarios based on your analysis:
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              "What if I doubled my sample size?",
              "What if I used a different alpha level?",
              "What if the effect was smaller?",
              "What if I had more groups?",
              "What if assumptions were violated?",
              "What if I used a non-parametric test?"
            ].map((scenario, idx) => (
              <button
                key={idx}
                onClick={() => askWhatIf(scenario)}
                disabled={loading}
                className="p-4 bg-white rounded-lg shadow hover:shadow-md transition-shadow text-left disabled:opacity-50"
              >
                <span className="text-purple-600 font-medium">🔮</span>
                <span className="ml-2 text-gray-700">{scenario}</span>
              </button>
            ))}
          </div>

          {/* Conversation for what-if */}
          {conversation.length > 0 && (
            <div className="bg-white rounded-lg p-6 shadow mt-6">
              <div className="space-y-4">
                {conversation.slice(-2).map((msg, idx) => (
                  <div key={idx}>
                    <p className="font-semibold text-gray-900 mb-2">
                      {msg.role === 'user' ? '🔮 Scenario:' : '🤖 Analysis:'}
                    </p>
                    <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AIInterpreter;
