import React from 'react';
import axios from 'axios';
import { ResultMeta } from '../types';
import PlotlyChart from './PlotlyChart';
import AssumptionChecker from './AssumptionChecker';
import BestPractices from './BestPractices';
import InterpretationHelper from './InterpretationHelper';
import CommonMistakes from './CommonMistakes';
import AIInterpreter from './AIInterpreter';

interface ResultsProps {
  jobId: string;
  resultUrl?: string;
  resultMeta?: ResultMeta;
}

// Helper function to format numbers to 4 decimal places
const formatNumber = (num: any): string => {
  if (typeof num !== 'number') return String(num);
  if (Number.isInteger(num)) return String(num);
  
  // Use scientific notation for very small numbers (p-values < 0.0001)
  if (Math.abs(num) < 0.0001 && num !== 0) {
    return num.toExponential(4);
  }
  
  return num.toFixed(4);
};

// Helper function to render test results in a user-friendly way
const renderTestResults = (results: any) => {
  if (!results) return null;

  // Create a clean display of key statistics
  const stats: Array<{ label: string; value: any; highlight?: boolean }> = [];

  // Common statistics across all tests
  if (results.test) {
    stats.push({ label: 'Test Used', value: results.test, highlight: true });
  }

  // P-value (most important!)
  if (results.p_value !== undefined) {
    const significant = results.p_value < 0.05;
    stats.push({
      label: 'P-value',
      value: formatNumber(results.p_value),
      highlight: significant,
    });
  }

  // Significance
  if (results.significant !== undefined) {
    stats.push({
      label: 'Result',
      value: results.significant ? '✅ Statistically Significant' : '❌ Not Significant',
      highlight: true,
    });
  }

  // R-squared (regression)
  if (results.r_squared !== undefined) {
    stats.push({ label: 'R²', value: formatNumber(results.r_squared) });
  }
  if (results.adj_r_squared !== undefined) {
    stats.push({ label: 'Adjusted R²', value: formatNumber(results.adj_r_squared) });
  }

  // Correlation coefficient
  if (results.correlation !== undefined) {
    const significant = results.p_value !== undefined && results.p_value < 0.05;
    stats.push({ 
      label: 'Correlation (r)', 
      value: formatNumber(results.correlation),
      highlight: significant
    });
  }
  
  // Correlation method
  if (results.method !== undefined && results.correlation !== undefined) {
    stats.push({ label: 'Method', value: results.method });
  }
  
  // Confidence interval
  if (results.ci_lower !== undefined && results.ci_upper !== undefined) {
    stats.push({ 
      label: `${results.confidence_level || 95}% Confidence Interval`, 
      value: `[${formatNumber(results.ci_lower)}, ${formatNumber(results.ci_upper)}]`
    });
  }
  
  // Effect size (correlation)
  if (results.effect_size !== undefined && results.correlation !== undefined) {
    stats.push({ label: 'Effect Size', value: results.effect_size });
  }
  
  // Direction (correlation)
  if (results.direction !== undefined && results.correlation !== undefined) {
    stats.push({ label: 'Direction', value: results.direction.charAt(0).toUpperCase() + results.direction.slice(1) });
  }

  // F-statistic (regression, ANOVA)
  if (results.f_statistic !== undefined) {
    stats.push({ label: 'F-statistic', value: formatNumber(results.f_statistic) });
  }
  if (results.f_pvalue !== undefined) {
    stats.push({ label: 'F p-value', value: formatNumber(results.f_pvalue) });
  }

  // T-statistic (t-test)
  if (results.t_statistic !== undefined) {
    stats.push({ label: 'T-statistic', value: formatNumber(results.t_statistic) });
  }

  // Chi-square
  if (results.chi2_statistic !== undefined) {
    stats.push({ label: 'χ² statistic', value: formatNumber(results.chi2_statistic) });
  }
  if (results.cramers_v !== undefined) {
    stats.push({ label: "Cramér's V", value: formatNumber(results.cramers_v) });
  }

  // Non-parametric statistics
  if (results.u_statistic !== undefined) {
    stats.push({ label: 'U-statistic', value: formatNumber(results.u_statistic) });
  }
  if (results.h_statistic !== undefined) {
    stats.push({ label: 'H-statistic', value: formatNumber(results.h_statistic) });
  }
  if (results.w_statistic !== undefined) {
    stats.push({ label: 'W-statistic', value: formatNumber(results.w_statistic) });
  }

  // Effect sizes
  if (results.cohens_d !== undefined) {
    stats.push({ label: "Cohen's d", value: formatNumber(results.cohens_d) });
  }
  if (results.effect_size_r !== undefined) {
    stats.push({ label: 'Effect Size (r)', value: formatNumber(results.effect_size_r) });
  }
  if (results.odds_ratio !== undefined) {
    stats.push({ label: 'Odds Ratio', value: formatNumber(results.odds_ratio) });
  }

  // Degrees of freedom
  if (results.degrees_of_freedom !== undefined || results.df !== undefined) {
    stats.push({ label: 'Degrees of Freedom', value: results.degrees_of_freedom || results.df });
  }

  // Sample sizes
  if (results.n_predictors !== undefined) {
    stats.push({ label: 'Number of Predictors', value: results.n_predictors });
  }
  
  // Clustering metrics
  if (results.silhouette_score !== undefined) {
    const silScore = results.silhouette_score;
    stats.push({ 
      label: 'Silhouette Score', 
      value: formatNumber(silScore),
      highlight: silScore > 0.5
    });
  }
  if (results.method !== undefined) {
    stats.push({ label: 'Clustering Method', value: results.method === 'kmeans' ? 'K-Means' : 'Hierarchical' });
  }
  if (results.inertia !== undefined) {
    stats.push({ label: 'Inertia', value: formatNumber(results.inertia) });
  }
  if (results.n_samples !== undefined) {
    stats.push({ label: 'Number of Samples', value: results.n_samples });
  }
  if (results.n_features !== undefined) {
    stats.push({ label: 'Number of Features', value: results.n_features });
  }

  // Survival Analysis metrics
  if (results.summary_statistics) {
    const ss = results.summary_statistics;
    if (ss.n_subjects !== undefined) {
      stats.push({ label: 'Number of Subjects', value: ss.n_subjects, highlight: true });
    }
    if (ss.n_events !== undefined) {
      stats.push({ label: 'Number of Events', value: ss.n_events });
    }
    if (ss.n_censored !== undefined) {
      stats.push({ label: 'Number Censored', value: ss.n_censored });
    }
    if (ss.event_rate !== undefined) {
      stats.push({ label: 'Event Rate', value: `${(ss.event_rate * 100).toFixed(1)}%` });
    }
    if (ss.median_survival !== undefined) {
      stats.push({ label: 'Median Survival Time', value: formatNumber(ss.median_survival), highlight: true });
    }
  }

  // Log-Rank Test
  if (results.logrank_test) {
    const lr = results.logrank_test;
    stats.push({ label: 'Log-Rank Test Statistic', value: formatNumber(lr.test_statistic) });
    stats.push({ 
      label: 'Log-Rank P-value', 
      value: formatNumber(lr.p_value),
      highlight: lr.significant
    });
    stats.push({
      label: 'Group Comparison',
      value: lr.significant ? '✅ Significantly Different' : '❌ Not Significant',
      highlight: true
    });
  }

  // Cox Regression
  if (results.cox_regression) {
    const cox = results.cox_regression;
    stats.push({ 
      label: 'Concordance Index (C-index)', 
      value: formatNumber(cox.concordance_index),
      highlight: cox.concordance_index > 0.7
    });
    stats.push({ label: 'Log-Likelihood', value: formatNumber(cox.log_likelihood) });
    stats.push({ label: 'AIC', value: formatNumber(cox.aic) });
  }

  // Coefficients (regression)
  const coefficients = results.coefficients;
  const pValues = results.p_values;
  const stdErrors = results.std_errors;

  // VIF values
  const vif = results.vif;

  return (
    <div className="space-y-4">
      {/* Main Statistics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        {stats.map((stat, idx) => (
          <div
            key={idx}
            className={`p-3 rounded-lg ${
              stat.highlight
                ? 'bg-white border-2 border-blue-400 shadow-sm'
                : 'bg-white border border-gray-200'
            }`}
          >
            <div className="text-xs font-medium text-gray-600 uppercase tracking-wide">
              {stat.label}
            </div>
            <div className="text-lg font-semibold text-gray-900 mt-1">
              {stat.value}
            </div>
          </div>
        ))}
      </div>

      {/* Coefficients Table (for regression) */}
      {coefficients && Object.keys(coefficients).length > 0 && (
        <div className="mt-4">
          <h4 className="text-sm font-semibold text-gray-900 mb-2">📈 Regression Coefficients</h4>
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border border-gray-200 rounded-lg">
              <thead className="bg-gray-100">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-semibold text-gray-700">Variable</th>
                  <th className="px-4 py-2 text-right text-xs font-semibold text-gray-700">Coefficient</th>
                  {stdErrors && <th className="px-4 py-2 text-right text-xs font-semibold text-gray-700">Std Error</th>}
                  {pValues && <th className="px-4 py-2 text-right text-xs font-semibold text-gray-700">P-value</th>}
                  {vif && <th className="px-4 py-2 text-right text-xs font-semibold text-gray-700">VIF</th>}
                </tr>
              </thead>
              <tbody>
                {Object.entries(coefficients).map(([key, value]: [string, any], idx) => {
                  const pVal = pValues?.[key];
                  const isSignificant = pVal !== undefined && pVal < 0.05;
                  return (
                    <tr key={idx} className={`border-t ${isSignificant ? 'bg-green-50' : ''}`}>
                      <td className="px-4 py-2 text-sm font-medium text-gray-900">
                        {key === 'intercept' ? '(Intercept)' : key}
                      </td>
                      <td className="px-4 py-2 text-sm text-right text-gray-700 font-mono">
                        {formatNumber(value)}
                      </td>
                      {stdErrors && (
                        <td className="px-4 py-2 text-sm text-right text-gray-600 font-mono">
                          {formatNumber(stdErrors[key])}
                        </td>
                      )}
                      {pValues && (
                        <td className="px-4 py-2 text-sm text-right font-mono">
                          <span className={isSignificant ? 'text-green-700 font-semibold' : 'text-gray-600'}>
                            {formatNumber(pVal)}
                            {isSignificant && ' *'}
                          </span>
                        </td>
                      )}
                      {vif && key !== 'intercept' && (
                        <td className="px-4 py-2 text-sm text-right text-gray-700 font-mono">
                          {vif[key] !== undefined ? formatNumber(vif[key]) : '-'}
                        </td>
                      )}
                    </tr>
                  );
                })}
              </tbody>
            </table>
            {pValues && (
              <p className="text-xs text-gray-600 mt-2">* Significant at α = 0.05</p>
            )}
          </div>
        </div>
      )}

      {/* Cox Regression Hazard Ratios Table */}
      {results.cox_regression?.covariates && Object.keys(results.cox_regression.covariates).length > 0 && (
        <div className="mt-4">
          <h4 className="text-sm font-semibold text-gray-900 mb-2">⚕️ Cox Regression - Hazard Ratios</h4>
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border border-gray-200 rounded-lg">
              <thead className="bg-gray-100">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-semibold text-gray-700">Covariate</th>
                  <th className="px-4 py-2 text-right text-xs font-semibold text-gray-700">Hazard Ratio</th>
                  <th className="px-4 py-2 text-right text-xs font-semibold text-gray-700">95% CI</th>
                  <th className="px-4 py-2 text-right text-xs font-semibold text-gray-700">P-value</th>
                  <th className="px-4 py-2 text-center text-xs font-semibold text-gray-700">Effect</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(results.cox_regression.covariates).map(([key, value]: [string, any], idx) => {
                  const isSignificant = value.significant;
                  const hrValid = value.hazard_ratio !== null && value.hazard_ratio !== undefined;
                  const hrEffect = hrValid 
                    ? (value.hazard_ratio > 1 ? '⬆️ Increases Risk' : '⬇️ Decreases Risk')
                    : 'N/A (unstable)';
                  return (
                    <tr key={idx} className={`border-t ${isSignificant && hrValid ? 'bg-green-50' : ''}`}>
                      <td className="px-4 py-2 text-sm font-medium text-gray-900">{key}</td>
                      <td className="px-4 py-2 text-sm text-right text-gray-700 font-mono">
                        {hrValid ? formatNumber(value.hazard_ratio) : 'N/A'}
                      </td>
                      <td className="px-4 py-2 text-sm text-right text-gray-600 font-mono">
                        {hrValid && value.ci_lower !== null && value.ci_upper !== null
                          ? `(${formatNumber(value.ci_lower)} - ${formatNumber(value.ci_upper)})`
                          : 'N/A'}
                      </td>
                      <td className="px-4 py-2 text-sm text-right font-mono">
                        <span className={isSignificant && hrValid ? 'text-green-700 font-semibold' : 'text-gray-600'}>
                          {formatNumber(value.p_value)}
                          {isSignificant && hrValid && ' *'}
                        </span>
                      </td>
                      <td className="px-4 py-2 text-sm text-center">
                        <span className={isSignificant && hrValid ? 'font-semibold' : 'text-gray-500'}>
                          {hrEffect}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
            <p className="text-xs text-gray-600 mt-2">
              * Significant at α = 0.05 | HR &gt; 1: Increased hazard | HR &lt; 1: Decreased hazard
            </p>
          </div>
        </div>
      )}

      {/* Medians (non-parametric tests) */}
      {(results.median_group_1 !== undefined || results.medians) && (
        <div className="mt-4">
          <h4 className="text-sm font-semibold text-gray-900 mb-2">📊 Group Medians</h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {results.median_group_1 !== undefined && (
              <>
                <div className="p-3 bg-white border border-gray-200 rounded-lg">
                  <div className="text-xs text-gray-600">Group 1</div>
                  <div className="text-lg font-semibold text-gray-900">{formatNumber(results.median_group_1)}</div>
                </div>
                <div className="p-3 bg-white border border-gray-200 rounded-lg">
                  <div className="text-xs text-gray-600">Group 2</div>
                  <div className="text-lg font-semibold text-gray-900">{formatNumber(results.median_group_2)}</div>
                </div>
              </>
            )}
            {results.medians && Object.entries(results.medians).map(([group, median]: [string, any]) => (
              <div key={group} className="p-3 bg-white border border-gray-200 rounded-lg">
                <div className="text-xs text-gray-600">{group}</div>
                <div className="text-lg font-semibold text-gray-900">{formatNumber(median)}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Cluster Sizes (clustering) */}
      {results.cluster_sizes && (
        <div className="mt-4">
          <h4 className="text-sm font-semibold text-gray-900 mb-2">📦 Cluster Sizes</h4>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
            {Object.entries(results.cluster_sizes).map(([cluster, size]: [string, any]) => (
              <div key={cluster} className="p-3 bg-white border border-blue-200 rounded-lg">
                <div className="text-xs text-gray-600">Cluster {cluster}</div>
                <div className="text-lg font-semibold text-blue-900">{size} samples</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const Results: React.FC<ResultsProps> = ({ jobId, resultUrl, resultMeta }) => {
  const handleDownload = async () => {
    try {
      const response = await axios.get(`/api/report?id=${jobId}`, {
        responseType: 'blob',
      });
      
      const blob = new Blob([response.data], { type: 'application/zip' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `gradstat-report-${jobId}.zip`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Download error:', error);
      alert('Failed to download report. Please try again.');
    }
  };
  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Analysis Results</h2>

      {/* Summary */}
      {resultMeta?.summary && (
        <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h3 className="text-sm font-semibold text-blue-900 mb-2">Summary</h3>
          <p className="text-sm text-blue-800">{resultMeta.summary}</p>
        </div>
      )}

      {/* Common Mistakes Warning */}
      <CommonMistakes 
        analysisType={resultMeta?.analysis_type || ''}
        options={{}}
        dataInfo={{
          sampleSize: resultMeta?.test_results?.n,
          hasOutliers: false,
          normalityViolated: resultMeta?.assumptions?.some(a => a.name.includes('Normality') && !a.passed),
          varianceUnequal: resultMeta?.assumptions?.some(a => a.name.includes('Variance') && !a.passed)
        }}
      />

      {/* Interpretation Helper */}
      {resultMeta?.test_results && (
        <InterpretationHelper testResults={resultMeta.test_results} />
      )}

      {/* Legacy Interpretation (fallback) */}
      {resultMeta?.interpretation && !resultMeta?.test_results && (
        <div className="mb-6 p-5 bg-gradient-to-br from-blue-50 to-purple-50 border border-blue-200 rounded-lg">
          <h3 className="text-base font-semibold text-gray-900 mb-3 flex items-center gap-2">
            💡 Interpretation
          </h3>
          <div className="prose prose-sm max-w-none">
            <p className="text-gray-700">{resultMeta.interpretation}</p>
          </div>
        </div>
      )}

      {/* Assumption Checker (Phase 3) */}
      {resultMeta?.assumptions && resultMeta.assumptions.length > 0 && (
        <AssumptionChecker 
          assumptions={resultMeta.assumptions}
          analysisType={resultMeta.analysis_type}
        />
      )}

      {/* Test Results */}
      {resultMeta?.test_results && (
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-gray-900 mb-3">📊 Statistical Test Results</h3>
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-6 border border-blue-200">
            {renderTestResults(resultMeta.test_results)}
          </div>
        </div>
      )}

      {/* Plots */}
      {resultMeta?.plots && resultMeta.plots.length > 0 && (
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-gray-900 mb-3">Visualizations</h3>
          <div className="grid grid-cols-1 gap-4">
            {resultMeta.plots.map((plot, idx) => (
              <PlotlyChart
                key={idx}
                data={plot}
                title={plot.title}
                className="mb-4"
              />
            ))}
          </div>
        </div>
      )}

      {/* Best Practices (Phase 3) */}
      <BestPractices 
        analysisType={resultMeta?.analysis_type || ''}
        testResults={resultMeta?.test_results}
      />

      {/* Code Snippet - Removed per user request */}

      {/* Recommendations */}
      {resultMeta?.recommendations && resultMeta.recommendations.length > 0 && (
        <div className="mb-6 p-4 bg-purple-50 border border-purple-200 rounded-lg">
          <h3 className="text-sm font-semibold text-purple-900 mb-2">Next Steps</h3>
          <ul className="space-y-1">
            {resultMeta.recommendations.map((rec, idx) => (
              <li key={idx} className="text-sm text-purple-800 flex items-start gap-2">
                <span>•</span>
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Conclusion */}
      {resultMeta?.conclusion && (
        <div className="mb-6 p-5 bg-yellow-50 border-l-4 border-yellow-400 rounded-lg">
          <h3 className="text-base font-semibold text-gray-900 mb-3 flex items-center gap-2">
            📝 Conclusion
          </h3>
          <p className="text-sm text-gray-800 leading-relaxed">{resultMeta.conclusion}</p>
        </div>
      )}

      {/* AI Interpreter */}
      {resultMeta && (
        <AIInterpreter 
          analysisData={{
            analysis_type: resultMeta.analysis_type || 'Unknown',
            sample_size: (resultMeta.test_results as any)?.sample_size || (resultMeta.test_results as any)?.n || 0,
            variables: (resultMeta.test_results as any)?.variables || [],
            results: resultMeta.test_results || {},
            assumptions: resultMeta.assumptions || {}
          }}
        />
      )}

      {/* Download Button */}
      {resultUrl && (
        <div className="flex gap-3">
          <button
            onClick={handleDownload}
            className="flex-1 px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium text-center"
          >
            📥 Download Full Report (ZIP)
          </button>
        </div>
      )}
    </div>
  );
};

export default Results;
