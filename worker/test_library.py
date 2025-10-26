"""
Statistical Test Library
Plain English explanations of statistical tests for non-statisticians
"""

TEST_LIBRARY = {
    'independent_ttest': {
        'test_name': 'Independent t-test',
        'analysis_type': 'group-comparison',
        'plain_english': 'Compare average scores between two separate groups',
        'when_to_use': [
            'You have 2 independent groups (different people)',
            'Measuring something continuous (like height, test scores)',
            'Data is roughly normally distributed'
        ],
        'example': 'Compare exam scores between students who studied vs. didn\'t study',
        'assumptions': ['Independence', 'Normality', 'Equal variance'],
        'sample_size_min': 30,
        'interpretation': 'If p < 0.05, the groups are significantly different',
        'gradstat_options': {
            'analysisType': 'group-comparison',
            'dependentVar': '<outcome>',
            'groupVar': '<group>'
        }
    },
    
    'anova': {
        'test_name': 'One-way ANOVA',
        'analysis_type': 'group-comparison',
        'plain_english': 'Compare average scores across 3 or more groups',
        'when_to_use': [
            'You have 3+ independent groups',
            'Continuous outcome variable',
            'Want to know if ANY groups differ'
        ],
        'example': 'Compare test scores across 3 teaching methods',
        'assumptions': ['Independence', 'Normality in each group', 'Equal variances'],
        'sample_size_min': 30,
        'interpretation': 'If p < 0.05, at least one group differs (use Tukey test to find which)',
        'gradstat_options': {
            'analysisType': 'group-comparison',
            'dependentVar': '<outcome>',
            'groupVar': '<group>'
        }
    },
    
    'mann_whitney': {
        'test_name': 'Mann-Whitney U test',
        'analysis_type': 'nonparametric',
        'plain_english': 'Compare rankings between two groups (when data is not normal)',
        'when_to_use': [
            'You have 2 independent groups',
            'Data is NOT normally distributed',
            'Or data is ordinal (ranks, ratings)'
        ],
        'example': 'Compare satisfaction ratings (1-5 scale) between two products',
        'assumptions': ['Independence', 'Ordinal or continuous data'],
        'sample_size_min': 20,
        'interpretation': 'If p < 0.05, the groups have different distributions',
        'gradstat_options': {
            'analysisType': 'nonparametric',
            'dependentVar': '<outcome>',
            'groupVar': '<group>',
            'testType': 'mann-whitney'
        }
    },
    
    'wilcoxon': {
        'test_name': 'Wilcoxon Signed-Rank test',
        'analysis_type': 'nonparametric',
        'plain_english': 'Compare paired measurements when data is not normal',
        'when_to_use': [
            'Paired/matched observations',
            'Data is NOT normally distributed',
            'Or ordinal data'
        ],
        'example': 'Compare pain ratings before/after treatment (1-10 scale)',
        'assumptions': ['Paired observations', 'Symmetric distribution'],
        'sample_size_min': 15,
        'interpretation': 'If p < 0.05, there is a significant change',
        'gradstat_options': {
            'analysisType': 'nonparametric',
            'dependentVar': '<outcome>',
            'groupVar': '<time>',
            'testType': 'wilcoxon'
        }
    },
    
    'kruskal_wallis': {
        'test_name': 'Kruskal-Wallis test',
        'analysis_type': 'nonparametric',
        'plain_english': 'Compare rankings across 3+ groups (when data is not normal)',
        'when_to_use': [
            'You have 3+ independent groups',
            'Data is NOT normally distributed',
            'Or ordinal data'
        ],
        'example': 'Compare customer satisfaction (1-5) across 4 stores',
        'assumptions': ['Independence', 'Ordinal or continuous data'],
        'sample_size_min': 25,
        'interpretation': 'If p < 0.05, at least one group differs',
        'gradstat_options': {
            'analysisType': 'nonparametric',
            'dependentVar': '<outcome>',
            'groupVar': '<group>',
            'testType': 'kruskal-wallis'
        }
    },
    
    'chi_square': {
        'test_name': 'Chi-Square test',
        'analysis_type': 'categorical',
        'plain_english': 'Test if two categorical variables are related',
        'when_to_use': [
            'Both variables are categorical',
            'Want to test independence/association',
            'Have frequency counts'
        ],
        'example': 'Is smoking related to lung disease? (Yes/No vs Disease/Healthy)',
        'assumptions': ['Independence', 'Expected frequency ≥ 5 in each cell'],
        'sample_size_min': 50,
        'interpretation': 'If p < 0.05, the variables are associated',
        'gradstat_options': {
            'analysisType': 'categorical',
            'var1': '<variable_1>',
            'var2': '<variable_2>'
        }
    },
    
    'simple_regression': {
        'test_name': 'Simple Linear Regression',
        'analysis_type': 'regression',
        'plain_english': 'Predict one variable from another and quantify the relationship',
        'when_to_use': [
            'Want to predict continuous outcome',
            'Have one continuous predictor',
            'Linear relationship expected'
        ],
        'example': 'Predict salary from years of experience',
        'assumptions': ['Linear relationship', 'Independence', 'Normal residuals', 'Constant variance'],
        'sample_size_min': 30,
        'interpretation': 'R² shows % variance explained. If p < 0.05, relationship is significant',
        'gradstat_options': {
            'analysisType': 'regression',
            'dependentVar': '<outcome>',
            'independentVar': '<predictor>'
        }
    },
    
    'pearson_correlation': {
        'test_name': 'Pearson Correlation',
        'analysis_type': 'correlation',
        'plain_english': 'Measure the strength and direction of linear relationship between two variables',
        'when_to_use': [
            'Want to measure association (not prediction)',
            'Both variables are continuous',
            'Linear relationship expected',
            'Data is roughly normally distributed'
        ],
        'example': 'Measure relationship between study hours and exam scores',
        'assumptions': ['Linear relationship', 'Normality', 'Independence', 'No extreme outliers'],
        'sample_size_min': 30,
        'interpretation': 'r = correlation coefficient (-1 to +1). |r| > 0.5 is strong. If p < 0.05, correlation is significant',
        'gradstat_options': {
            'analysisType': 'correlation',
            'correlationMethod': 'pearson',
            'variables': ['<variable_1>', '<variable_2>']
        }
    },
    
    'spearman_correlation': {
        'test_name': 'Spearman Correlation',
        'analysis_type': 'correlation',
        'plain_english': 'Measure monotonic relationship between variables (works with non-normal data)',
        'when_to_use': [
            'Want to measure association',
            'Data is NOT normally distributed',
            'Relationship is monotonic but not necessarily linear',
            'Or have ordinal data (rankings)'
        ],
        'example': 'Measure relationship between income rank and happiness rating',
        'assumptions': ['Monotonic relationship', 'Independence', 'Ordinal or continuous data'],
        'sample_size_min': 20,
        'interpretation': 'ρ (rho) = correlation coefficient. Robust to outliers. If p < 0.05, correlation is significant',
        'gradstat_options': {
            'analysisType': 'correlation',
            'correlationMethod': 'spearman',
            'variables': ['<variable_1>', '<variable_2>']
        }
    },
    
    'kendall_correlation': {
        'test_name': 'Kendall\'s Tau',
        'analysis_type': 'correlation',
        'plain_english': 'Conservative measure of association for ordinal data or small samples',
        'when_to_use': [
            'Small sample size (n < 30)',
            'Ordinal data (rankings)',
            'Want more conservative estimate',
            'Many tied values in data'
        ],
        'example': 'Measure agreement between two judges\' rankings',
        'assumptions': ['Monotonic relationship', 'Independence', 'Ordinal or continuous data'],
        'sample_size_min': 10,
        'interpretation': 'τ (tau) = correlation coefficient. More conservative than Spearman. If p < 0.05, correlation is significant',
        'gradstat_options': {
            'analysisType': 'correlation',
            'correlationMethod': 'kendall',
            'variables': ['<variable_1>', '<variable_2>']
        }
    },
    
    'multiple_regression': {
        'test_name': 'Multiple Linear Regression',
        'analysis_type': 'regression',
        'plain_english': 'Predict outcome from multiple predictors simultaneously',
        'when_to_use': [
            'Want to predict continuous outcome',
            'Have multiple predictors',
            'Want to control for confounders'
        ],
        'example': 'Predict house price from size, location, and age',
        'assumptions': ['Linear relationships', 'No multicollinearity', 'Normal residuals'],
        'sample_size_min': 100,
        'interpretation': 'Each coefficient shows effect while holding others constant',
        'gradstat_options': {
            'analysisType': 'regression',
            'dependentVar': '<outcome>',
            'independentVars': ['<predictor_1>', '<predictor_2>']
        }
    },
    
    'logistic_regression': {
        'test_name': 'Logistic Regression',
        'analysis_type': 'logistic-regression',
        'plain_english': 'Predict probability of yes/no outcome from predictors',
        'when_to_use': [
            'Outcome is binary (yes/no, success/fail)',
            'Want to predict probability',
            'Have continuous or categorical predictors'
        ],
        'example': 'Predict disease risk (yes/no) from age, BMI, smoking',
        'assumptions': ['Binary outcome', 'Independence', 'No extreme multicollinearity'],
        'sample_size_min': 100,
        'interpretation': 'Odds ratios show effect on odds. AUC shows prediction accuracy',
        'gradstat_options': {
            'analysisType': 'logistic-regression',
            'targetColumn': '<outcome>',
            'predictors': ['<predictor_1>', '<predictor_2>']
        }
    },
    
    'kaplan_meier': {
        'test_name': 'Kaplan-Meier Survival Analysis',
        'analysis_type': 'survival',
        'plain_english': 'Analyze time until an event occurs (survival, failure, etc.)',
        'when_to_use': [
            'Measuring time to event',
            'Have censored data (some events not observed)',
            'Want survival curves'
        ],
        'example': 'Time until patient recovery, with some still in treatment',
        'assumptions': ['Censoring is non-informative', 'Independent survival times'],
        'sample_size_min': 50,
        'interpretation': 'Survival curve shows probability over time. Median = time when 50% have event',
        'gradstat_options': {
            'analysisType': 'survival',
            'durationColumn': '<time>',
            'eventColumn': '<event>'
        }
    },
    
    'logrank_test': {
        'test_name': 'Log-Rank Test',
        'analysis_type': 'survival',
        'plain_english': 'Compare survival curves between groups',
        'when_to_use': [
            'Have survival data',
            'Want to compare 2+ groups',
            'Censored observations present'
        ],
        'example': 'Compare survival between treatment and control groups',
        'assumptions': ['Proportional hazards', 'Non-informative censoring'],
        'sample_size_min': 50,
        'interpretation': 'If p < 0.05, survival differs between groups',
        'gradstat_options': {
            'analysisType': 'survival',
            'durationColumn': '<time>',
            'eventColumn': '<event>',
            'groupColumn': '<group>'
        }
    },
    
    'cox_regression': {
        'test_name': 'Cox Proportional Hazards Regression',
        'analysis_type': 'survival',
        'plain_english': 'Model survival time with multiple predictors',
        'when_to_use': [
            'Have survival data',
            'Want to adjust for multiple factors',
            'Estimate hazard ratios'
        ],
        'example': 'Model survival from age, stage, treatment simultaneously',
        'assumptions': ['Proportional hazards', 'Linear with log-hazard', 'No multicollinearity'],
        'sample_size_min': 100,
        'interpretation': 'Hazard ratio > 1 = increased risk, < 1 = decreased risk',
        'gradstat_options': {
            'analysisType': 'survival',
            'durationColumn': '<time>',
            'eventColumn': '<event>',
            'covariates': ['<covariate_1>', '<covariate_2>']
        }
    },
    
    'paired_ttest': {
        'test_name': 'Paired t-test',
        'analysis_type': 'group-comparison',
        'plain_english': 'Compare measurements from the same people at two different times',
        'when_to_use': [
            'Same people measured twice (before/after)',
            'Matched pairs of people',
            'Continuous outcome variable'
        ],
        'example': 'Compare blood pressure before and after medication in same patients',
        'assumptions': ['Paired observations', 'Differences are normally distributed'],
        'sample_size_min': 20,
        'interpretation': 'If p < 0.05, there is a significant change',
        'gradstat_options': {
            'analysisType': 'group-comparison',
            'dependentVar': '<outcome>',
            'groupVar': '<time>'
        }
    },
    
    'descriptive': {
        'test_name': 'Descriptive Statistics',
        'analysis_type': 'descriptive',
        'plain_english': 'Summarize and describe your data',
        'when_to_use': [
            'Want to understand data characteristics',
            'First step in any analysis',
            'Presenting sample characteristics'
        ],
        'example': 'Report mean age, gender distribution, score ranges',
        'assumptions': [],
        'sample_size_min': 1,
        'interpretation': 'Mean/median show center, SD shows spread, min/max show range',
        'gradstat_options': {
            'analysisType': 'descriptive'
        }
    },
    
    'fisher_exact': {
        'test_name': 'Fisher\'s Exact Test',
        'analysis_type': 'categorical',
        'plain_english': 'Test association between two categorical variables (small samples)',
        'when_to_use': [
            'Both variables are categorical',
            'Small sample size (n < 50)',
            'Expected frequencies < 5 in any cell'
        ],
        'example': 'Is treatment effective? (10 treated, 8 control; success/failure)',
        'assumptions': ['Independence', 'Exact test - no minimum sample size'],
        'sample_size_min': 10,
        'interpretation': 'If p < 0.05, the variables are associated. More reliable than Chi-square for small samples',
        'gradstat_options': {
            'analysisType': 'categorical',
            'var1': '<variable_1>',
            'var2': '<variable_2>',
            'testType': 'fisher'
        }
    },
    
    'pca': {
        'test_name': 'Principal Component Analysis (PCA)',
        'analysis_type': 'pca',
        'plain_english': 'Reduce many variables into fewer meaningful components',
        'when_to_use': [
            'Have many correlated variables',
            'Want to reduce dimensionality',
            'Looking for underlying patterns',
            'Data visualization in 2D/3D'
        ],
        'example': 'Reduce 20 survey questions into 3-4 key themes',
        'assumptions': ['Linear relationships', 'Variables are continuous', 'Sufficient correlation between variables'],
        'sample_size_min': 100,
        'interpretation': 'Components explain variance. First few components capture most information',
        'gradstat_options': {
            'analysisType': 'pca',
            'nComponents': 3
        }
    },
    
    'clustering': {
        'test_name': 'K-Means Clustering',
        'analysis_type': 'clustering',
        'plain_english': 'Group similar observations together',
        'when_to_use': [
            'Want to find natural groups in data',
            'Customer segmentation',
            'Pattern discovery',
            'No predefined categories'
        ],
        'example': 'Group customers into segments based on purchasing behavior',
        'assumptions': ['Variables are continuous', 'Clusters are roughly spherical', 'Similar cluster sizes'],
        'sample_size_min': 50,
        'interpretation': 'Each observation assigned to a cluster. Silhouette score shows cluster quality',
        'gradstat_options': {
            'analysisType': 'clustering',
            'nClusters': 3,
            'method': 'kmeans'
        }
    }
}
