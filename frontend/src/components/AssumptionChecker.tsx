import React from 'react';

interface Assumption {
  name: string;
  passed: boolean;
  pValue?: number;
  statistic?: number;
  message: string;
}

interface AssumptionCheckerProps {
  assumptions: Assumption[];
  analysisType?: string;
}

const AssumptionChecker: React.FC<AssumptionCheckerProps> = ({ assumptions }) => {
  if (!assumptions || assumptions.length === 0) {
    return null;
  }

  const passedCount = assumptions.filter(a => a.passed).length;
  const totalCount = assumptions.length;
  const allPassed = passedCount === totalCount;

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900 flex items-center">
          ✓ Assumption Checks
          {allPassed && <span className="ml-2 text-green-600 text-sm">(All Passed)</span>}
        </h3>
        <div className="text-sm text-gray-600">
          {passedCount} / {totalCount} passed
        </div>
      </div>

      {/* Overall Status */}
      <div className={`mb-4 p-3 rounded-lg ${
        allPassed 
          ? 'bg-green-50 border border-green-200' 
          : 'bg-yellow-50 border border-yellow-200'
      }`}>
        <p className="text-sm font-medium">
          {allPassed ? (
            <span className="text-green-800">
              ✓ All statistical assumptions are met. Results are reliable.
            </span>
          ) : (
            <span className="text-yellow-800">
              ⚠️ Some assumptions are violated. Interpret results with caution.
            </span>
          )}
        </p>
      </div>

      {/* Individual Assumptions */}
      <div className="space-y-3">
        {assumptions.map((assumption, idx) => (
          <div
            key={idx}
            className={`p-4 rounded-lg border ${
              assumption.passed
                ? 'bg-green-50 border-green-200'
                : 'bg-red-50 border-red-200'
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center mb-1">
                  <span className={`text-lg mr-2 ${
                    assumption.passed ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {assumption.passed ? '✓' : '✗'}
                  </span>
                  <h4 className={`font-semibold ${
                    assumption.passed ? 'text-green-900' : 'text-red-900'
                  }`}>
                    {assumption.name}
                  </h4>
                </div>
                <p className={`text-sm ml-7 ${
                  assumption.passed ? 'text-green-800' : 'text-red-800'
                }`}>
                  {assumption.message}
                </p>
                
                {/* Statistical Details */}
                {(assumption.pValue !== undefined || assumption.statistic !== undefined) && (
                  <div className="mt-2 ml-7 text-xs text-gray-600">
                    {assumption.statistic !== undefined && (
                      <span className="mr-3">
                        Statistic: {assumption.statistic.toFixed(4)}
                      </span>
                    )}
                    {assumption.pValue !== undefined && (
                      <span>
                        p-value: {assumption.pValue < 0.001 ? '< 0.001' : assumption.pValue.toFixed(3)}
                      </span>
                    )}
                  </div>
                )}
              </div>
            </div>

            {/* Remediation Suggestions */}
            {!assumption.passed && (
              <div className="mt-3 ml-7 p-3 bg-white rounded border border-red-100">
                <p className="text-xs font-semibold text-red-900 mb-1">💡 What to do:</p>
                <ul className="text-xs text-red-800 space-y-1">
                  {getRemediation(assumption.name).map((remedy, i) => (
                    <li key={i} className="flex items-start">
                      <span className="mr-2">•</span>
                      <span>{remedy}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Educational Note */}
      <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-xs text-blue-800">
          <strong>📚 Why assumptions matter:</strong> Statistical tests make certain assumptions about your data. 
          When assumptions are violated, results may be unreliable. Consider using alternative tests or 
          transforming your data if assumptions are not met.
        </p>
      </div>
    </div>
  );
};

// Helper function to provide remediation suggestions
const getRemediation = (assumptionName: string): string[] => {
  const remediations: { [key: string]: string[] } = {
    'Normality': [
      'Use a non-parametric test (e.g., Mann-Whitney U, Kruskal-Wallis)',
      'Transform your data (log, square root, or Box-Cox transformation)',
      'Increase sample size (Central Limit Theorem helps with larger n)',
      'Remove outliers if they are data errors'
    ],
    'Homogeneity of Variance': [
      'Use Welch\'s t-test instead of Student\'s t-test',
      'Use Brown-Forsythe test for ANOVA',
      'Transform your data to stabilize variance',
      'Use robust statistical methods'
    ],
    'Independence': [
      'Use repeated measures or mixed-effects models',
      'Account for clustering in your analysis',
      'Check for autocorrelation in time series',
      'Ensure proper randomization in study design'
    ],
    'Linearity': [
      'Add polynomial terms (quadratic, cubic)',
      'Use non-linear regression models',
      'Transform variables (log, exponential)',
      'Consider generalized additive models (GAM)'
    ],
    'Homoscedasticity': [
      'Use weighted least squares regression',
      'Transform the dependent variable',
      'Use robust standard errors',
      'Consider heteroscedasticity-consistent estimators'
    ],
    'No Multicollinearity': [
      'Remove highly correlated predictors (VIF > 10)',
      'Use principal component analysis (PCA)',
      'Combine correlated variables into a composite',
      'Use ridge regression or LASSO'
    ]
  };

  // Try exact match first
  if (remediations[assumptionName]) {
    return remediations[assumptionName];
  }

  // Try partial match
  for (const [key, value] of Object.entries(remediations)) {
    if (assumptionName.includes(key) || key.includes(assumptionName)) {
      return value;
    }
  }

  // Default suggestions
  return [
    'Consult a statistician for guidance',
    'Consider alternative statistical methods',
    'Review your data collection process',
    'Check for data quality issues'
  ];
};

export default AssumptionChecker;
