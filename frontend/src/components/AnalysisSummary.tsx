import React, { useState } from 'react';
import ConfidenceBadge from './ConfidenceBadge';

interface AnalysisSummaryProps {
  results: any;
  onStartWizard: () => void;
  onSkipToRecommendations?: () => void;
}

const AnalysisSummary: React.FC<AnalysisSummaryProps> = ({ 
  results, 
  onStartWizard,
  onSkipToRecommendations 
}) => {
  const [showDetails, setShowDetails] = useState(false);

  if (!results) return null;

  const { summary, confidence, details } = results;
  const confidenceRate = parseInt(summary?.confidence_rate || '0');
  const canSkip = confidenceRate >= 80;

  const getDetectionSummary = () => {
    const items = [];

    // Compare Groups detections
    if (results.isNormal !== null) {
      items.push({
        text: results.isNormal 
          ? 'Data is normally distributed' 
          : 'Data is not normally distributed',
        confidence: confidence.isNormal,
        icon: results.isNormal ? '✅' : '❌'
      });
    }

    if (results.nGroups !== null) {
      items.push({
        text: `Detected ${results.nGroups} groups`,
        confidence: confidence.nGroups,
        icon: '✅',
        details: details.nGroups?.column ? `in '${details.nGroups.column}' column` : ''
      });
    }

    if (results.isPaired !== null) {
      items.push({
        text: results.isPaired 
          ? 'Detected paired/repeated measures structure' 
          : 'Data appears to be independent groups',
        confidence: confidence.isPaired,
        icon: results.isPaired ? '✅' : '✅'
      });
    }

    if (results.outcomeType !== null) {
      items.push({
        text: `Found ${results.outcomeType} outcome variable`,
        confidence: confidence.outcomeType,
        icon: '✅'
      });
    }

    // Find Relationships detections
    if (results.var1Type !== null && results.var2Type !== null) {
      const typeDesc = results.var1Type === 'continuous' && results.var2Type === 'continuous'
        ? 'both continuous variables'
        : results.var1Type === 'categorical' && results.var2Type === 'categorical'
        ? 'both categorical variables'
        : 'mixed variable types';
      
      items.push({
        text: `Detected ${typeDesc}`,
        confidence: confidence.varTypes,
        icon: '✅'
      });
    }

    // Predictor count
    if (results.nPredictors !== null) {
      items.push({
        text: `Found ${results.nPredictors === 1 ? 'single' : 'multiple'} predictor variable(s)`,
        confidence: confidence.nPredictors,
        icon: '✅'
      });
    }

    // Survival Analysis detections
    if (results.survival) {
      const surv = results.survival;
      if (surv.time_column) {
        items.push({
          text: `Detected time column: '${surv.time_column}'`,
          confidence: surv.confidence?.time_column || 'medium',
          icon: '⏱️'
        });
      }
      if (surv.event_column) {
        const censorPct = surv.details?.censoring_pct;
        items.push({
          text: `Detected event column: '${surv.event_column}'`,
          confidence: surv.confidence?.event_column || 'medium',
          icon: '📊',
          details: censorPct ? `${censorPct.toFixed(1)}% censored` : ''
        });
      }
      if (surv.has_groups && surv.group_column) {
        items.push({
          text: `Found groups in '${surv.group_column}' for comparison`,
          confidence: confidence.hasGroups_survival || 'medium',
          icon: '👥'
        });
      }
      if (surv.has_covariates) {
        items.push({
          text: `Found ${surv.covariate_columns?.length || 0} covariate(s) for adjustment`,
          confidence: confidence.hasCovariates || 'medium',
          icon: '📈'
        });
      }
    }

    // PCA detections
    if (results.pca && results.pca.n_numeric_vars >= 3) {
      const pca = results.pca;
      items.push({
        text: `Suggested ${pca.suggested_components} PCA components from ${pca.n_numeric_vars} variables`,
        confidence: confidence.nComponents || 'medium',
        icon: '🔍',
        details: pca.correlation_strength ? `${pca.correlation_strength} correlation` : ''
      });
      if (pca.scaling_needed) {
        items.push({
          text: 'Scaling recommended (large variance differences)',
          confidence: confidence.scaling_pca || 'high',
          icon: '⚖️'
        });
      }
    }

    // Clustering detections
    if (results.clustering && results.clustering.n_numeric_vars >= 2) {
      const clust = results.clustering;
      if (clust.suggested_k) {
        items.push({
          text: `Suggested ${clust.suggested_k} clusters using ${clust.suggested_algorithm}`,
          confidence: confidence.nClusters || 'medium',
          icon: '🎯'
        });
      }
      if (clust.has_outliers) {
        items.push({
          text: `Outliers detected (${clust.details?.outlier_pct?.toFixed(1)}%)`,
          confidence: 'high',
          icon: '⚠️'
        });
      }
    }

    return items;
  };

  const detections = getDetectionSummary();
  const highConfidenceCount = Object.values(confidence).filter(c => c === 'high').length;
  const lowConfidenceItems = detections.filter(d => d.confidence === 'low');

  return (
    <div className="mb-6 bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-lg p-6 shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="text-3xl">📊</span>
          <div>
            <h3 className="text-xl font-bold text-gray-900">
              Smart Analysis Complete!
            </h3>
            <p className="text-sm text-gray-600">
              {summary?.confidence_rate} overall confidence ({highConfidenceCount}/{Object.keys(confidence).length} high confidence)
            </p>
          </div>
        </div>
        <div className="text-right">
          {canSkip ? (
            <span className="inline-flex items-center gap-2 px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-semibold border border-green-300">
              <span>✨</span>
              <span>High Confidence</span>
            </span>
          ) : (
            <span className="inline-flex items-center gap-2 px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm font-semibold border border-yellow-300">
              <span>⚠️</span>
              <span>Review Recommended</span>
            </span>
          )}
        </div>
      </div>

      {/* Detection Summary */}
      <div className="space-y-2 mb-4">
        {detections.map((item, idx) => (
          <div key={idx} className="flex items-start gap-2 text-sm">
            <span className="text-lg">{item.icon}</span>
            <div className="flex-1">
              <span className="text-gray-800 font-medium">{item.text}</span>
              {item.details && (
                <span className="text-gray-600"> {item.details}</span>
              )}
            </div>
            <ConfidenceBadge confidence={item.confidence} size="sm" />
          </div>
        ))}
      </div>

      {/* Recommendation */}
      {lowConfidenceItems.length > 0 && (
        <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
          <div className="flex items-start gap-2">
            <span className="text-lg">💡</span>
            <div className="flex-1">
              <p className="text-sm font-semibold text-yellow-900">Recommendation:</p>
              <p className="text-sm text-yellow-800">
                {lowConfidenceItems.length} detection(s) have low confidence. 
                Please review these answers carefully in the wizard.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Technical Details (Collapsible) */}
      <div className="mb-4">
        <button
          onClick={() => setShowDetails(!showDetails)}
          className="flex items-center gap-2 text-sm text-blue-700 hover:text-blue-900 font-medium"
        >
          <span>{showDetails ? '▼' : '▶'}</span>
          <span>View Technical Details</span>
        </button>
        
        {showDetails && (
          <div className="mt-3 p-3 bg-white rounded-lg border border-gray-200 text-xs font-mono">
            <pre className="whitespace-pre-wrap text-gray-700">
              {JSON.stringify(details, null, 2)}
            </pre>
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="flex gap-3">
        {canSkip && onSkipToRecommendations && (
          <button
            onClick={onSkipToRecommendations}
            className="flex-1 px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg font-semibold hover:from-blue-700 hover:to-indigo-700 transition-all shadow-md hover:shadow-lg"
          >
            ✨ Skip to Recommendations
          </button>
        )}
        <button
          onClick={onStartWizard}
          className={`${canSkip ? 'flex-1' : 'w-full'} px-6 py-3 bg-white text-gray-700 border-2 border-gray-300 rounded-lg font-semibold hover:bg-gray-50 transition-colors`}
        >
          {canSkip ? 'Review Answers Manually' : 'Start Wizard →'}
        </button>
      </div>
    </div>
  );
};

export default AnalysisSummary;
