import React, { useState } from 'react';

interface BestPracticesProps {
  analysisType: string;
  testResults?: any;
}

const BestPractices: React.FC<BestPracticesProps> = ({ analysisType, testResults }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const practices = getBestPractices(analysisType, testResults);

  if (!practices || (practices.dos.length === 0 && practices.donts.length === 0)) {
    return null;
  }

  return (
    <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-lg border border-indigo-200 p-6 mb-6">
      <div 
        className="flex items-center justify-between cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <h3 className="text-lg font-semibold text-indigo-900 flex items-center">
          💡 Best Practices & Recommendations
        </h3>
        <button className="text-indigo-600 hover:text-indigo-800 transition-colors">
          {isExpanded ? '▼ Hide' : '▶ Show'}
        </button>
      </div>

      {isExpanded && (
        <div className="mt-4 space-y-4">
          {/* Do's */}
          <div className="bg-white rounded-lg p-4 border border-green-200">
            <h4 className="font-semibold text-green-900 mb-3 flex items-center">
              ✓ Do's - Follow These Practices
            </h4>
            <ul className="space-y-2">
              {practices.dos.map((practice, idx) => (
                <li key={idx} className="flex items-start text-sm text-green-800">
                  <span className="text-green-600 mr-2 mt-0.5">✓</span>
                  <span>{practice}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Don'ts */}
          <div className="bg-white rounded-lg p-4 border border-red-200">
            <h4 className="font-semibold text-red-900 mb-3 flex items-center">
              ✗ Don'ts - Avoid These Mistakes
            </h4>
            <ul className="space-y-2">
              {practices.donts.map((practice, idx) => (
                <li key={idx} className="flex items-start text-sm text-red-800">
                  <span className="text-red-600 mr-2 mt-0.5">✗</span>
                  <span>{practice}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Tips */}
          {practices.tips && practices.tips.length > 0 && (
            <div className="bg-white rounded-lg p-4 border border-blue-200">
              <h4 className="font-semibold text-blue-900 mb-3 flex items-center">
                💡 Pro Tips
              </h4>
              <ul className="space-y-2">
                {practices.tips.map((tip, idx) => (
                  <li key={idx} className="flex items-start text-sm text-blue-800">
                    <span className="text-blue-600 mr-2 mt-0.5">💡</span>
                    <span>{tip}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Reporting Guidelines */}
          {practices.reporting && practices.reporting.length > 0 && (
            <div className="bg-white rounded-lg p-4 border border-purple-200">
              <h4 className="font-semibold text-purple-900 mb-3 flex items-center">
                📝 Reporting Guidelines
              </h4>
              <ul className="space-y-2">
                {practices.reporting.map((guideline, idx) => (
                  <li key={idx} className="flex items-start text-sm text-purple-800">
                    <span className="text-purple-600 mr-2 mt-0.5">📝</span>
                    <span>{guideline}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

// Helper function to get best practices based on analysis type
const getBestPractices = (analysisType: string, testResults?: any) => {
  const practices: {
    dos: string[];
    donts: string[];
    tips?: string[];
    reporting?: string[];
  } = {
    dos: [],
    donts: [],
    tips: [],
    reporting: []
  };

  // Common practices for all analyses
  const commonDos = [
    'Check all assumptions before interpreting results',
    'Report effect sizes along with p-values',
    'Use appropriate alpha level (typically 0.05)',
    'Describe your sample and methodology clearly'
  ];

  const commonDonts = [
    'Don\'t rely solely on p-values for decision making',
    'Don\'t ignore violated assumptions',
    'Don\'t confuse statistical significance with practical importance',
    'Don\'t p-hack by running multiple tests until you find significance'
  ];

  // Analysis-specific practices
  switch (analysisType.toLowerCase()) {
    case 't-test':
    case 'independent-t':
    case 'paired-t':
      practices.dos = [
        ...commonDos,
        'Verify normality assumption with Shapiro-Wilk test',
        'Check for equal variances (Levene\'s test)',
        'Report Cohen\'s d for effect size',
        'Use Welch\'s t-test if variances are unequal'
      ];
      practices.donts = [
        ...commonDonts,
        'Don\'t use t-test with severely non-normal data (use Mann-Whitney U)',
        'Don\'t assume equal variances without testing',
        'Don\'t use paired t-test for independent samples'
      ];
      practices.tips = [
        'Sample size of 30+ per group helps with normality assumption',
        'Visualize data with box plots before testing',
        'Consider the practical significance of the mean difference'
      ];
      practices.reporting = [
        'Report: t-statistic, degrees of freedom, p-value, Cohen\'s d',
        'Example: "t(48) = 3.45, p = .002, d = 0.92"',
        'Include means and standard deviations for each group'
      ];
      break;

    case 'anova':
    case 'one-way-anova':
      practices.dos = [
        ...commonDos,
        'Check normality for each group',
        'Test homogeneity of variance (Levene\'s test)',
        'Use post-hoc tests for pairwise comparisons',
        'Report eta-squared or partial eta-squared'
      ];
      practices.donts = [
        ...commonDonts,
        'Don\'t do multiple t-tests instead of ANOVA (inflates Type I error)',
        'Don\'t skip post-hoc tests if ANOVA is significant',
        'Don\'t use ANOVA with severely unequal group sizes without caution'
      ];
      practices.tips = [
        'Tukey HSD is good for equal sample sizes',
        'Use Bonferroni for unequal sizes or fewer comparisons',
        'Consider Kruskal-Wallis if assumptions violated'
      ];
      practices.reporting = [
        'Report: F-statistic, degrees of freedom, p-value, effect size',
        'Example: "F(2, 57) = 8.45, p < .001, η² = 0.23"',
        'Include descriptive statistics for all groups'
      ];
      break;

    case 'regression':
    case 'linear-regression':
    case 'multiple-regression':
      practices.dos = [
        ...commonDos,
        'Check for linearity with scatter plots',
        'Test for homoscedasticity (residual plots)',
        'Check for multicollinearity (VIF < 10)',
        'Examine residuals for normality',
        'Report R², adjusted R², and standardized coefficients'
      ];
      practices.donts = [
        ...commonDonts,
        'Don\'t extrapolate beyond your data range',
        'Don\'t include highly correlated predictors (VIF > 10)',
        'Don\'t ignore influential outliers (Cook\'s distance)',
        'Don\'t claim causation from correlation'
      ];
      practices.tips = [
        'Center predictors to reduce multicollinearity',
        'Use standardized coefficients to compare predictor importance',
        'Check for influential cases with leverage plots',
        'Consider interaction terms if theoretically justified'
      ];
      practices.reporting = [
        'Report: R², F-statistic, coefficients with SE and p-values',
        'Example: "R² = .45, F(3, 96) = 26.2, p < .001"',
        'Include unstandardized and standardized coefficients'
      ];
      break;

    case 'correlation':
      practices.dos = [
        ...commonDos,
        'Visualize relationship with scatter plot',
        'Check for linearity (Pearson) or monotonicity (Spearman)',
        'Report confidence intervals',
        'Consider outliers\' influence'
      ];
      practices.donts = [
        ...commonDonts,
        'Don\'t use Pearson for non-linear relationships',
        'Don\'t assume causation from correlation',
        'Don\'t ignore the influence of third variables',
        'Don\'t use correlation with categorical variables'
      ];
      practices.tips = [
        'Use Spearman for ordinal data or non-linear relationships',
        'Use Kendall\'s tau for small samples with ties',
        'Partial correlation controls for third variables'
      ];
      practices.reporting = [
        'Report: correlation coefficient, sample size, p-value',
        'Example: "r(98) = .67, p < .001"',
        'Describe strength: weak (<.3), moderate (.3-.7), strong (>.7)'
      ];
      break;

    case 'logistic-regression':
      practices.dos = [
        ...commonDos,
        'Check for multicollinearity among predictors',
        'Report odds ratios with confidence intervals',
        'Evaluate model fit with AUC-ROC',
        'Use confusion matrix to assess predictions'
      ];
      practices.donts = [
        ...commonDonts,
        'Don\'t use linear regression for binary outcomes',
        'Don\'t ignore class imbalance issues',
        'Don\'t over-interpret odds ratios for continuous predictors'
      ];
      practices.tips = [
        'AUC > 0.7 is acceptable, > 0.8 is good, > 0.9 is excellent',
        'Consider precision-recall for imbalanced data',
        'Use cross-validation to assess generalizability'
      ];
      practices.reporting = [
        'Report: odds ratios, 95% CI, p-values, AUC',
        'Example: "OR = 2.34, 95% CI [1.45, 3.78], p < .001"',
        'Include classification accuracy and confusion matrix'
      ];
      break;

    case 'chi-square':
    case 'categorical':
      practices.dos = [
        ...commonDos,
        'Check expected frequencies (all > 5)',
        'Use Fisher\'s exact test for small samples',
        'Report effect size (Cramér\'s V or phi)',
        'Include contingency table'
      ];
      practices.donts = [
        ...commonDonts,
        'Don\'t use chi-square with expected frequencies < 5',
        'Don\'t use chi-square for ordinal data (use ordinal tests)',
        'Don\'t interpret chi-square as correlation strength'
      ];
      practices.tips = [
        'Combine categories if expected frequencies are low',
        'Use residuals to identify which cells contribute most',
        'Consider logistic regression for multiple predictors'
      ];
      practices.reporting = [
        'Report: χ², degrees of freedom, p-value, effect size',
        'Example: "χ²(2) = 12.45, p = .002, V = 0.35"',
        'Include observed and expected frequencies'
      ];
      break;

    case 'ancova':
      practices.dos = [
        ...commonDos,
        'Check homogeneity of regression slopes',
        'Verify covariate is measured before treatment',
        'Report adjusted means',
        'Test covariate-treatment interaction'
      ];
      practices.donts = [
        ...commonDonts,
        'Don\'t use ANCOVA if slopes differ across groups',
        'Don\'t include covariates affected by treatment',
        'Don\'t ignore covariate-treatment interactions'
      ];
      practices.tips = [
        'ANCOVA increases power by reducing error variance',
        'Covariates should correlate with DV but not IV',
        'Report both adjusted and unadjusted means'
      ];
      break;

    default:
      practices.dos = commonDos;
      practices.donts = commonDonts;
      practices.tips = [
        'Always visualize your data before analysis',
        'Consider the practical significance of your findings',
        'Replicate findings when possible'
      ];
  }

  // Add context-specific warnings based on results
  if (testResults) {
    if (testResults.p_value !== undefined && testResults.p_value > 0.05 && testResults.p_value < 0.10) {
      practices.tips?.push('Your p-value is marginally significant (0.05 < p < 0.10). Consider collecting more data.');
    }
    
    if (testResults.effect_size !== undefined && Math.abs(testResults.effect_size) < 0.2) {
      practices.tips?.push('Your effect size is small. Consider whether the finding is practically meaningful.');
    }
  }

  return practices;
};

export default BestPractices;
