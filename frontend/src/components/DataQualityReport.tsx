import React, { useState } from 'react';

interface QualityIssue {
  severity: 'error' | 'warning' | 'info';
  category: string;
  column?: string;
  message: string;
  count?: number;
  percentage?: number;
  recommendation?: string;
}

interface QualityVisualization {
  title: string;
  type: string;
  base64: string;
  description: string;
}

interface QualityReport {
  overall_score: number;
  issues: QualityIssue[];
  visualizations: QualityVisualization[];
  recommendations: string[];
  summary: {
    total_issues: number;
    errors: number;
    warnings: number;
    info: number;
  };
}

interface DataQualityReportProps {
  report: QualityReport;
}

const DataQualityReport: React.FC<DataQualityReportProps> = ({ report }) => {
  const [expanded, setExpanded] = useState(false);

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreIcon = (score: number) => {
    if (score >= 80) return '✅';
    if (score >= 60) return '⚠️';
    return '❌';
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'error': return 'text-red-600 bg-red-50 border-red-200';
      case 'warning': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'info': return 'text-blue-600 bg-blue-50 border-blue-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'error': return '🔴';
      case 'warning': return '⚠️';
      case 'info': return 'ℹ️';
      default: return '•';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'missing': return '📊';
      case 'outliers': return '📈';
      case 'types': return '🔤';
      case 'sample_size': return '📏';
      case 'distribution': return '📉';
      case 'correlation': return '🔗';
      default: return '•';
    }
  };

  const groupIssuesByCategory = () => {
    const grouped: { [key: string]: QualityIssue[] } = {};
    report.issues.forEach(issue => {
      if (!grouped[issue.category]) {
        grouped[issue.category] = [];
      }
      grouped[issue.category].push(issue);
    });
    return grouped;
  };

  const categoryNames: { [key: string]: string } = {
    'missing': 'Missing Data',
    'outliers': 'Outliers',
    'types': 'Data Types',
    'sample_size': 'Sample Size',
    'distribution': 'Distribution',
    'correlation': 'Correlations'
  };

  return (
    <div className="mb-6 bg-white border-2 border-gray-200 rounded-lg shadow-sm">
      {/* Header - Always Visible */}
      <div 
        className="p-4 cursor-pointer hover:bg-gray-50 transition-colors"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl">{getScoreIcon(report.overall_score)}</span>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">
                Data Quality Score: <span className={getScoreColor(report.overall_score)}>{report.overall_score}/100</span>
              </h3>
              <p className="text-sm text-gray-600">
                {report.summary.total_issues === 0 ? (
                  'No issues detected'
                ) : (
                  <>
                    {report.summary.errors > 0 && <span className="text-red-600">{report.summary.errors} error{report.summary.errors !== 1 ? 's' : ''}</span>}
                    {report.summary.errors > 0 && (report.summary.warnings > 0 || report.summary.info > 0) && ', '}
                    {report.summary.warnings > 0 && <span className="text-yellow-600">{report.summary.warnings} warning{report.summary.warnings !== 1 ? 's' : ''}</span>}
                    {report.summary.warnings > 0 && report.summary.info > 0 && ', '}
                    {report.summary.info > 0 && <span className="text-blue-600">{report.summary.info} info</span>}
                  </>
                )}
              </p>
            </div>
          </div>
          <button className="text-gray-500 hover:text-gray-700">
            {expanded ? '▼' : '▶'} {expanded ? 'Hide' : 'View'} Details
          </button>
        </div>
      </div>

      {/* Expanded Content */}
      {expanded && (
        <div className="border-t border-gray-200 p-4 space-y-4">
          {/* Overall Recommendations */}
          {report.recommendations.length > 0 && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
              <h4 className="font-semibold text-blue-900 mb-2">Overall Assessment</h4>
              {report.recommendations.map((rec, idx) => (
                <p key={idx} className="text-sm text-blue-800">{rec}</p>
              ))}
            </div>
          )}

          {/* Issues by Category */}
          {Object.entries(groupIssuesByCategory()).map(([category, issues]) => (
            <div key={category} className="space-y-2">
              <h4 className="font-semibold text-gray-900 flex items-center gap-2">
                <span>{getCategoryIcon(category)}</span>
                {categoryNames[category] || category}
              </h4>
              {issues.map((issue, idx) => (
                <div 
                  key={idx}
                  className={`border rounded-lg p-3 ${getSeverityColor(issue.severity)}`}
                >
                  <div className="flex items-start gap-2">
                    <span className="text-lg">{getSeverityIcon(issue.severity)}</span>
                    <div className="flex-1">
                      <p className="font-medium">{issue.message}</p>
                      {issue.recommendation && (
                        <p className="text-sm mt-1 opacity-90">
                          💡 {issue.recommendation}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ))}

          {/* Visualizations */}
          {report.visualizations.length > 0 && (
            <div className="space-y-4">
              <h4 className="font-semibold text-gray-900">Visualizations</h4>
              {report.visualizations.map((viz, idx) => (
                <div key={idx} className="border border-gray-200 rounded-lg p-4">
                  <h5 className="font-medium text-gray-900 mb-2">{viz.title}</h5>
                  <p className="text-sm text-gray-600 mb-3">{viz.description}</p>
                  <img 
                    src={`data:image/png;base64,${viz.base64}`}
                    alt={viz.title}
                    className="w-full rounded"
                  />
                </div>
              ))}
            </div>
          )}

          {/* No Issues Message */}
          {report.issues.length === 0 && (
            <div className="text-center py-8 text-gray-600">
              <span className="text-4xl mb-2 block">✅</span>
              <p className="font-medium">Excellent Data Quality!</p>
              <p className="text-sm">No issues detected. Your data is ready for analysis.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default DataQualityReport;
