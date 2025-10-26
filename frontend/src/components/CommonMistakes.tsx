import React from 'react';

interface CommonMistakesProps {
  analysisType: string;
  options?: any;
  dataInfo?: {
    sampleSize?: number;
    hasOutliers?: boolean;
    normalityViolated?: boolean;
    varianceUnequal?: boolean;
  };
}

interface Mistake {
  type: 'error' | 'warning' | 'info';
  title: string;
  message: string;
  fix?: string;
}

const CommonMistakes: React.FC<CommonMistakesProps> = ({ analysisType, options, dataInfo }) => {
  const mistakes = detectMistakes(analysisType, options, dataInfo);

  if (!mistakes || mistakes.length === 0) {
    return null;
  }

  return (
    <div className="mb-6 space-y-3">
      {mistakes.map((mistake, idx) => (
        <div
          key={idx}
          className={`rounded-lg border p-4 ${
            mistake.type === 'error'
              ? 'bg-red-50 border-red-300'
              : mistake.type === 'warning'
              ? 'bg-yellow-50 border-yellow-300'
              : 'bg-blue-50 border-blue-300'
          }`}
        >
          <div className="flex items-start">
            <span className={`text-2xl mr-3 ${
              mistake.type === 'error'
                ? 'text-red-600'
                : mistake.type === 'warning'
                ? 'text-yellow-600'
                : 'text-blue-600'
            }`}>
              {mistake.type === 'error' ? '🚫' : mistake.type === 'warning' ? '⚠️' : 'ℹ️'}
            </span>
            <div className="flex-1">
              <h4 className={`font-semibold mb-1 ${
                mistake.type === 'error'
                  ? 'text-red-900'
                  : mistake.type === 'warning'
                  ? 'text-yellow-900'
                  : 'text-blue-900'
              }`}>
                {mistake.title}
              </h4>
              <p className={`text-sm mb-2 ${
                mistake.type === 'error'
                  ? 'text-red-800'
                  : mistake.type === 'warning'
                  ? 'text-yellow-800'
                  : 'text-blue-800'
              }`}>
                {mistake.message}
              </p>
              {mistake.fix && (
                <div className={`mt-2 p-2 rounded text-xs ${
                  mistake.type === 'error'
                    ? 'bg-red-100 text-red-900'
                    : mistake.type === 'warning'
                    ? 'bg-yellow-100 text-yellow-900'
                    : 'bg-blue-100 text-blue-900'
                }`}>
                  <strong>💡 How to fix:</strong> {mistake.fix}
                </div>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

// Helper function to detect common mistakes
const detectMistakes = (
  analysisType: string,
  options?: any,
  dataInfo?: any
): Mistake[] => {
  const mistakes: Mistake[] = [];

  // Sample size checks
  if (dataInfo?.sampleSize) {
    if (dataInfo.sampleSize < 30 && ['t-test', 'anova', 'regression'].includes(analysisType)) {
      mistakes.push({
        type: 'warning',
        title: 'Small Sample Size',
        message: `Your sample size (n=${dataInfo.sampleSize}) is small. Results may be less reliable and assumptions harder to verify.`,
        fix: 'Consider collecting more data, using non-parametric tests, or interpreting results cautiously.'
      });
    }

    if (dataInfo.sampleSize < 10) {
      mistakes.push({
        type: 'error',
        title: 'Very Small Sample Size',
        message: `Your sample size (n=${dataInfo.sampleSize}) is too small for reliable statistical inference.`,
        fix: 'Collect more data before performing analysis. Consider descriptive statistics only.'
      });
    }
  }

  // Analysis-specific mistakes
  switch (analysisType.toLowerCase()) {
    case 't-test':
    case 'independent-t':
      if (dataInfo?.normalityViolated) {
        mistakes.push({
          type: 'warning',
          title: 'Normality Assumption Violated',
          message: 'Your data is not normally distributed. t-test results may be unreliable.',
          fix: 'Use Mann-Whitney U test (non-parametric alternative) or transform your data.'
        });
      }
      if (dataInfo?.varianceUnequal) {
        mistakes.push({
          type: 'info',
          title: 'Unequal Variances Detected',
          message: 'Groups have unequal variances. Standard t-test assumes equal variances.',
          fix: 'Use Welch\'s t-test (automatically applied by most software) which doesn\'t assume equal variances.'
        });
      }
      break;

    case 'anova':
    case 'one-way-anova':
      if (dataInfo?.normalityViolated) {
        mistakes.push({
          type: 'warning',
          title: 'Normality Assumption Violated',
          message: 'One or more groups are not normally distributed.',
          fix: 'Use Kruskal-Wallis H test (non-parametric alternative) or transform your data.'
        });
      }
      if (options?.nGroups && options.nGroups === 2) {
        mistakes.push({
          type: 'info',
          title: 'Only 2 Groups',
          message: 'You\'re comparing only 2 groups. A t-test would be more appropriate and powerful.',
          fix: 'Consider using an independent t-test instead of ANOVA for 2-group comparisons.'
        });
      }
      break;

    case 'regression':
    case 'linear-regression':
    case 'multiple-regression':
      if (dataInfo?.hasOutliers) {
        mistakes.push({
          type: 'warning',
          title: 'Outliers Detected',
          message: 'Outliers can heavily influence regression results and coefficients.',
          fix: 'Examine outliers (Cook\'s distance), consider removing if they\'re errors, or use robust regression.'
        });
      }
      if (options?.independentVars && options.independentVars.length > 10 && dataInfo?.sampleSize && dataInfo.sampleSize < 100) {
        mistakes.push({
          type: 'warning',
          title: 'Too Many Predictors for Sample Size',
          message: 'You have many predictors relative to sample size. Risk of overfitting.',
          fix: 'Use at least 10-15 observations per predictor. Consider variable selection or regularization.'
        });
      }
      break;

    case 'correlation':
      if (dataInfo?.hasOutliers) {
        mistakes.push({
          type: 'warning',
          title: 'Outliers May Affect Correlation',
          message: 'Outliers can artificially inflate or deflate correlation coefficients.',
          fix: 'Use Spearman correlation (less sensitive to outliers) or remove outlier data points.'
        });
      }
      break;

    case 'logistic-regression':
      if (dataInfo?.sampleSize && dataInfo.sampleSize < 100) {
        mistakes.push({
          type: 'warning',
          title: 'Small Sample for Logistic Regression',
          message: 'Logistic regression typically needs larger samples (100+ recommended).',
          fix: 'Collect more data or use simpler models with fewer predictors.'
        });
      }
      break;

    case 'chi-square':
    case 'categorical':
      if (options?.expectedFrequencies && options.expectedFrequencies.some((f: number) => f < 5)) {
        mistakes.push({
          type: 'error',
          title: 'Low Expected Frequencies',
          message: 'Some cells have expected frequencies < 5. Chi-square test is not valid.',
          fix: 'Use Fisher\'s exact test, combine categories, or collect more data.'
        });
      }
      break;
  }

  // Common mistakes across all analyses
  if (options?.alpha && options.alpha > 0.10) {
    mistakes.push({
      type: 'warning',
      title: 'Unusual Alpha Level',
      message: `Alpha level of ${options.alpha} is higher than conventional (0.05). This increases Type I error risk.`,
      fix: 'Use standard alpha = 0.05 unless you have a specific reason for a different value.'
    });
  }

  if (options?.alpha && options.alpha < 0.001) {
    mistakes.push({
      type: 'info',
      title: 'Very Conservative Alpha Level',
      message: `Alpha level of ${options.alpha} is very conservative. This increases Type II error risk.`,
      fix: 'Consider using alpha = 0.01 or 0.05 unless you need to be extremely conservative.'
    });
  }

  // Multiple testing warning
  if (options?.multipleTests && options.multipleTests > 3) {
    mistakes.push({
      type: 'warning',
      title: 'Multiple Testing Issue',
      message: 'Running multiple tests increases the chance of false positives (Type I error).',
      fix: 'Apply Bonferroni correction (divide alpha by number of tests) or use FDR correction.'
    });
  }

  return mistakes;
};

export default CommonMistakes;
