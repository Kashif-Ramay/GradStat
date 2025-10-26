/**
 * Help Content Database
 * Contextual help for statistical concepts and analysis options
 */

export interface HelpContent {
  id: string;
  title: string;
  shortDescription: string;
  fullDescription: string;
  examples?: string[];
  tips?: string[];
  learnMoreUrl?: string;
}

export const helpContent: Record<string, HelpContent> = {
  // Analysis Types
  'analysis-type': {
    id: 'analysis-type',
    title: 'Analysis Type',
    shortDescription: 'Choose the statistical test that matches your research question',
    fullDescription: `
      Select the analysis that best fits your research question and data type:
      
      • Descriptive: Summarize data with means, medians, and visualizations
      • Group Comparison: Compare means between 2+ groups (t-test, ANOVA)
      • Correlation: Measure relationship strength between variables
      • Regression: Predict outcomes from predictor variables
      • Non-parametric: Alternative tests when assumptions violated
    `,
    tips: [
      'Use Test Advisor if unsure which test to choose',
      'Check assumptions before running parametric tests',
      'Consider effect sizes, not just p-values'
    ]
  },

  // Variables
  'dependent-variable': {
    id: 'dependent-variable',
    title: 'Dependent Variable (Outcome)',
    shortDescription: 'The variable you are trying to predict or explain',
    fullDescription: `
      The dependent variable (DV) is what you measure or observe. It "depends" on 
      the independent variable(s).
      
      Examples:
      • Test scores (predicted by study hours)
      • Blood pressure (affected by medication)
      • Sales (influenced by advertising)
      
      The DV should be:
      • Continuous for regression, t-tests, ANOVA
      • Binary for logistic regression
      • Categorical for chi-square tests
    `,
    examples: [
      'Study: Does exercise improve mood? → DV: Mood score',
      'Study: Does fertilizer increase yield? → DV: Crop yield'
    ]
  },

  'independent-variable': {
    id: 'independent-variable',
    title: 'Independent Variable (Predictor)',
    shortDescription: 'The variable you manipulate or use to predict the outcome',
    fullDescription: `
      The independent variable (IV) is what you change, control, or use to predict 
      the dependent variable.
      
      Examples:
      • Study hours (predicts test scores)
      • Medication dose (affects blood pressure)
      • Advertising spend (influences sales)
      
      The IV can be:
      • Continuous (age, temperature, dose)
      • Categorical (treatment groups, gender)
      • Multiple variables (multiple regression)
    `,
    examples: [
      'Study: Does exercise improve mood? → IV: Exercise frequency',
      'Study: Does fertilizer increase yield? → IV: Fertilizer amount'
    ]
  },

  'group-variable': {
    id: 'group-variable',
    title: 'Group Variable',
    shortDescription: 'Categorical variable that defines groups to compare',
    fullDescription: `
      The group variable divides your data into categories for comparison.
      
      Examples:
      • Treatment groups (control, drug A, drug B)
      • Gender (male, female, other)
      • Education level (high school, bachelor's, master's)
      
      Requirements:
      • Must be categorical (not continuous)
      • At least 2 groups
      • Groups should be independent (unless paired design)
    `,
    tips: [
      'For 2 groups: Use t-test',
      'For 3+ groups: Use ANOVA',
      'Check group sizes are roughly equal'
    ]
  },

  // Statistical Concepts
  'alpha-level': {
    id: 'alpha-level',
    title: 'Alpha Level (Significance Threshold)',
    shortDescription: 'The probability threshold for determining statistical significance',
    fullDescription: `
      The alpha level (α) is the probability of rejecting the null hypothesis when 
      it is actually true (Type I error rate).
      
      Common values:
      • α = 0.05 (5%): Standard in most fields
      • α = 0.01 (1%): More conservative, reduces false positives
      • α = 0.10 (10%): More liberal, increases power
      
      Interpretation:
      • If p-value < α: Result is statistically significant
      • If p-value ≥ α: Result is not statistically significant
    `,
    examples: [
      'α = 0.05 means 5% chance of false positive',
      'Lower α = stricter criteria for significance'
    ],
    tips: [
      'Use 0.05 unless you have a specific reason to change',
      'Pre-specify alpha before analysis',
      'Consider adjusting for multiple comparisons'
    ]
  },

  'p-value': {
    id: 'p-value',
    title: 'P-value',
    shortDescription: 'Probability of observing results this extreme if null hypothesis is true',
    fullDescription: `
      The p-value tells you how likely your results would be if there were actually 
      no effect (null hypothesis is true).
      
      Interpretation:
      • p < 0.001: Very strong evidence against null hypothesis (***) 
      • p < 0.01: Strong evidence against null hypothesis (**)
      • p < 0.05: Moderate evidence against null hypothesis (*)
      • p ≥ 0.05: Insufficient evidence to reject null hypothesis
      
      Important:
      • P-value is NOT the probability that the null hypothesis is true
      • Small p-value doesn't mean large effect
      • Always report effect sizes along with p-values
    `,
    examples: [
      'p = 0.03: 3% chance of seeing this result if no real effect',
      'p = 0.45: 45% chance - not unusual under null hypothesis'
    ],
    tips: [
      'Don\'t rely solely on p < 0.05 threshold',
      'Consider practical significance (effect size)',
      'Report exact p-values, not just "p < 0.05"'
    ]
  },

  'effect-size': {
    id: 'effect-size',
    title: 'Effect Size',
    shortDescription: 'Magnitude of the difference or relationship',
    fullDescription: `
      Effect size measures how large or important an effect is, independent of 
      sample size.
      
      Common measures:
      • Cohen's d: Standardized mean difference
        - Small: 0.2, Medium: 0.5, Large: 0.8
      • Eta-squared (η²): Proportion of variance explained
        - Small: 0.01, Medium: 0.06, Large: 0.14
      • Correlation (r): Strength of relationship
        - Small: 0.1, Medium: 0.3, Large: 0.5
      
      Why important:
      • Statistical significance ≠ practical significance
      • Large samples can make tiny effects significant
      • Effect sizes allow comparison across studies
    `,
    examples: [
      'd = 0.8: Large effect - groups differ by 0.8 standard deviations',
      'η² = 0.14: Treatment explains 14% of outcome variance'
    ],
    tips: [
      'Always report effect sizes with p-values',
      'Consider practical importance, not just statistics',
      'Use confidence intervals for effect sizes'
    ]
  },

  // Assumptions
  'normality': {
    id: 'normality',
    title: 'Normality Assumption',
    shortDescription: 'Data should follow a normal (bell-shaped) distribution',
    fullDescription: `
      Many statistical tests assume data are normally distributed.
      
      How to check:
      • Visual: Histogram, Q-Q plot
      • Statistical: Shapiro-Wilk test
      
      What if violated:
      • Small deviations: Usually OK with n > 30 (Central Limit Theorem)
      • Large deviations: Use non-parametric tests
        - Mann-Whitney U instead of t-test
        - Kruskal-Wallis instead of ANOVA
      
      Note: With large samples (n > 100), tests are robust to violations
    `,
    tips: [
      'Check Q-Q plot: Points should follow diagonal line',
      'Shapiro-Wilk p > 0.05 suggests normality',
      'Consider transformations (log, sqrt) if skewed'
    ]
  },

  'homogeneity-variance': {
    id: 'homogeneity-variance',
    title: 'Homogeneity of Variance',
    shortDescription: 'Groups should have similar variability',
    fullDescription: `
      This assumption requires that groups have equal variances (spread).
      
      How to check:
      • Visual: Box plots should have similar heights
      • Statistical: Levene's test
      
      What if violated:
      • Use Welch's t-test instead of Student's t-test
      • Use Welch's ANOVA instead of standard ANOVA
      • Consider transformations
      
      Rule of thumb: Largest SD / Smallest SD < 2 is usually OK
    `,
    tips: [
      'Levene p > 0.05 suggests equal variances',
      'Welch corrections are robust to violations',
      'More important with unequal sample sizes'
    ]
  },

  'independence': {
    id: 'independence',
    title: 'Independence Assumption',
    shortDescription: 'Observations should be independent of each other',
    fullDescription: `
      Each observation should not influence or be related to other observations.
      
      Violations occur when:
      • Repeated measures on same subjects
      • Clustered data (students within schools)
      • Time series data (autocorrelation)
      • Matched pairs or siblings
      
      Solutions:
      • Use paired tests for repeated measures
      • Use mixed models for clustered data
      • Use time series methods for temporal data
      • Account for matching in design
    `,
    tips: [
      'Cannot be tested statistically',
      'Ensure through study design',
      'Use appropriate test for dependent data'
    ]
  },

  // Test-specific
  'correlation-method': {
    id: 'correlation-method',
    title: 'Correlation Method',
    shortDescription: 'Choose based on data type and relationship',
    fullDescription: `
      Different correlation methods for different situations:
      
      • Pearson: Linear relationships, continuous data, normal distribution
        - Most common, assumes linearity
        - Range: -1 to +1
      
      • Spearman: Monotonic relationships, ordinal data, non-normal
        - Rank-based, robust to outliers
        - Good for skewed data
      
      • Kendall: Small samples, many tied ranks
        - More conservative than Spearman
        - Better for small n
    `,
    examples: [
      'Height vs Weight: Pearson (linear, continuous)',
      'Education level vs Income: Spearman (ordinal)',
      'Ranked preferences: Kendall (small sample, ties)'
    ],
    tips: [
      'Start with Pearson if assumptions met',
      'Use Spearman if data skewed or ordinal',
      'Correlation ≠ causation!'
    ]
  },

  'post-hoc-tests': {
    id: 'post-hoc-tests',
    title: 'Post-hoc Tests',
    shortDescription: 'Pairwise comparisons after significant ANOVA',
    fullDescription: `
      After finding a significant ANOVA, post-hoc tests identify which specific 
      groups differ.
      
      Common methods:
      • Tukey HSD: Balanced design, controls family-wise error
      • Bonferroni: Conservative, good for few comparisons
      • Holm: Less conservative than Bonferroni
      • Dunnett: Compare all groups to control
      
      Why needed:
      • ANOVA only tells you groups differ somewhere
      • Post-hoc tests locate the differences
      • Corrections prevent inflated Type I error
    `,
    tips: [
      'Only run after significant ANOVA',
      'Tukey HSD is most common',
      'Report adjusted p-values'
    ]
  },

  'power-analysis': {
    id: 'power-analysis',
    title: 'Power Analysis',
    shortDescription: 'Determine required sample size or statistical power',
    fullDescription: `
      Power analysis helps plan studies and interpret results.
      
      Key concepts:
      • Power: Probability of detecting a real effect (usually 0.80)
      • Effect size: How large is the effect you want to detect?
      • Sample size: How many participants needed?
      • Alpha: Significance level (usually 0.05)
      
      Use power analysis to:
      • Plan sample size before data collection
      • Evaluate power after non-significant results
      • Justify sample size in grant proposals
    `,
    examples: [
      'Need n=64 per group to detect medium effect (d=0.5) with 80% power',
      'With n=20, you have 50% power to detect medium effect'
    ],
    tips: [
      'Aim for 80% power minimum',
      'Larger effects need smaller samples',
      'Consider practical constraints'
    ]
  }
};

// Helper function to get help content
export const getHelpContent = (id: string): HelpContent | undefined => {
  return helpContent[id];
};

// Helper function to get short description
export const getHelpDescription = (id: string): string => {
  const content = helpContent[id];
  return content ? content.shortDescription : '';
};
