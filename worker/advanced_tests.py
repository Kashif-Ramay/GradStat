"""
Advanced Statistical Tests
ANCOVA, Repeated Measures ANOVA, Mixed ANOVA, Post-hoc Tests, Effect Sizes
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.anova import AnovaRM
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd, MultiComparison
import logging

logger = logging.getLogger(__name__)


def plot_to_base64(fig):
    """Convert matplotlib figure to base64 string"""
    import io
    import base64
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


def calculate_cohens_d(group1, group2):
    """Calculate Cohen's d effect size"""
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std if pooled_std > 0 else 0


def calculate_eta_squared(ss_effect, ss_total):
    """Calculate eta-squared effect size"""
    return ss_effect / ss_total if ss_total > 0 else 0


def calculate_partial_eta_squared(ss_effect, ss_error):
    """Calculate partial eta-squared effect size"""
    return ss_effect / (ss_effect + ss_error) if (ss_effect + ss_error) > 0 else 0


def interpret_effect_size(value, measure='cohens_d'):
    """Interpret effect size magnitude"""
    if measure == 'cohens_d':
        if abs(value) < 0.2:
            return 'negligible'
        elif abs(value) < 0.5:
            return 'small'
        elif abs(value) < 0.8:
            return 'medium'
        else:
            return 'large'
    elif measure in ['eta_squared', 'partial_eta_squared']:
        if value < 0.01:
            return 'negligible'
        elif value < 0.06:
            return 'small'
        elif value < 0.14:
            return 'medium'
        else:
            return 'large'
    return 'unknown'


def ancova_analysis(df: pd.DataFrame, opts: Dict) -> Dict:
    """
    Analysis of Covariance (ANCOVA)
    ANOVA with continuous covariates
    """
    group_var = opts.get('groupVar')
    dep_var = opts.get('dependentVar')
    covariates = opts.get('covariates', [])
    alpha = opts.get('alpha', 0.05)
    
    if not group_var or not dep_var or not covariates:
        raise ValueError("Group variable, dependent variable, and at least one covariate required")
    
    # Clean data
    cols = [group_var, dep_var] + covariates
    data = df[cols].dropna()
    
    # Build formula
    covariate_str = ' + '.join(covariates)
    formula = f'{dep_var} ~ C({group_var}) + {covariate_str}'
    
    # Fit model
    model = ols(formula, data=data).fit()
    anova_table = anova_lm(model, typ=2)
    
    # Extract results
    group_row = f'C({group_var})'
    if group_row in anova_table.index:
        f_stat = float(anova_table.loc[group_row, 'F'])
        p_value = float(anova_table.loc[group_row, 'PR(>F)'])
        df_between = int(anova_table.loc[group_row, 'df'])
        df_within = int(anova_table.loc['Residual', 'df'])
        ss_effect = float(anova_table.loc[group_row, 'sum_sq'])
        ss_error = float(anova_table.loc['Residual', 'sum_sq'])
        
        # Calculate effect size
        partial_eta_sq = calculate_partial_eta_squared(ss_effect, ss_error)
        effect_interp = interpret_effect_size(partial_eta_sq, 'partial_eta_squared')
    else:
        raise ValueError(f"Group variable {group_var} not found in ANOVA table")
    
    # Get adjusted means
    groups = data[group_var].unique()
    adjusted_means = {}
    for group in groups:
        group_data = data[data[group_var] == group]
        adjusted_means[str(group)] = {
            'mean': float(group_data[dep_var].mean()),
            'n': int(len(group_data))
        }
    
    # Covariate effects
    covariate_effects = []
    for cov in covariates:
        if cov in anova_table.index:
            cov_f = float(anova_table.loc[cov, 'F'])
            cov_p = float(anova_table.loc[cov, 'PR(>F)'])
            covariate_effects.append({
                'covariate': cov,
                'F': cov_f,
                'p_value': cov_p,
                'significant': cov_p < alpha
            })
    
    # Create plots
    plots = []
    
    # Boxplot
    fig, ax = plt.subplots(figsize=(10, 6))
    data.boxplot(column=dep_var, by=group_var, ax=ax)
    ax.set_title(f'ANCOVA: {dep_var} by {group_var}')
    ax.set_xlabel(group_var)
    ax.set_ylabel(dep_var)
    plt.suptitle('')
    plots.append({
        'title': f'Boxplot: {dep_var} by {group_var}',
        'type': 'boxplot',
        'base64': plot_to_base64(fig)
    })
    
    # Scatter plot with covariate
    if len(covariates) > 0:
        fig, ax = plt.subplots(figsize=(10, 6))
        for group in groups:
            group_data = data[data[group_var] == group]
            ax.scatter(group_data[covariates[0]], group_data[dep_var], label=str(group), alpha=0.6)
        ax.set_xlabel(covariates[0])
        ax.set_ylabel(dep_var)
        ax.set_title(f'{dep_var} vs {covariates[0]} by {group_var}')
        ax.legend()
        ax.grid(alpha=0.3)
        plots.append({
            'title': f'Scatter: {dep_var} vs {covariates[0]}',
            'type': 'scatter',
            'base64': plot_to_base64(fig)
        })
    
    # Test results
    test_results = {
        'test': 'ANCOVA',
        'F_statistic': f_stat,
        'p_value': p_value,
        'df_between': df_between,
        'df_within': df_within,
        'significant': p_value < alpha,
        'alpha': alpha,
        'partial_eta_squared': partial_eta_sq,
        'effect_size_interpretation': effect_interp,
        'adjusted_means': adjusted_means,
        'covariate_effects': covariate_effects
    }
    
    # Summary
    summary = f"ANCOVA: F({df_between}, {df_within}) = {f_stat:.3f}, p = {p_value:.4f}"
    if p_value < alpha:
        summary += f" (significant at α={alpha})"
    summary += f"\nEffect Size: ηp² = {partial_eta_sq:.3f} ({effect_interp})"
    
    # Interpretation
    if p_value < alpha:
        interpretation = f"There is a statistically significant difference in {dep_var} between groups "
        interpretation += f"after controlling for {', '.join(covariates)} (p = {p_value:.4f}). "
        interpretation += f"The effect size is {effect_interp} (ηp² = {partial_eta_sq:.3f})."
    else:
        interpretation = f"There is no statistically significant difference in {dep_var} between groups "
        interpretation += f"after controlling for {', '.join(covariates)} (p = {p_value:.4f})."
    
    # Assumptions
    assumptions = [
        {
            'name': 'Independence of observations',
            'passed': None,
            'message': 'Observations should be independent within and between groups'
        },
        {
            'name': 'Normality of residuals',
            'passed': None,
            'message': 'Residuals should be normally distributed (check with residual plots)'
        },
        {
            'name': 'Homogeneity of variance',
            'passed': None,
            'message': 'Variance should be equal across groups (Levene test recommended)'
        },
        {
            'name': 'Homogeneity of regression slopes',
            'passed': None,
            'message': 'Relationship between covariate and DV should be similar across groups'
        },
        {
            'name': 'Linear relationship',
            'passed': None,
            'message': 'Covariate should be linearly related to dependent variable'
        }
    ]
    
    # Recommendations
    recommendations = []
    if p_value < alpha:
        recommendations.append("Conduct post-hoc tests to identify which groups differ")
        recommendations.append("Report adjusted means for each group")
    recommendations.append("Check residual plots to verify assumptions")
    recommendations.append("Consider interaction between group and covariate if appropriate")
    
    result = {
        'analysis_type': 'ancova',
        'summary': summary,
        'test_results': test_results,
        'plots': plots,
        'interpretation': interpretation,
        'assumptions': assumptions,
        'recommendations': recommendations
    }
    
    return result


def repeated_measures_anova(df: pd.DataFrame, opts: Dict) -> Dict:
    """
    Repeated Measures ANOVA
    Within-subjects ANOVA for longitudinal data
    """
    subject_var = opts.get('subjectVar')
    time_var = opts.get('timeVar')
    dep_var = opts.get('dependentVar')
    alpha = opts.get('alpha', 0.05)
    
    if not subject_var or not time_var or not dep_var:
        raise ValueError("Subject ID, time variable, and dependent variable required")
    
    # Clean data
    data = df[[subject_var, time_var, dep_var]].dropna()
    
    # Perform repeated measures ANOVA
    try:
        aovrm = AnovaRM(data, dep_var, subject_var, within=[time_var])
        res = aovrm.fit()
        
        # Extract results
        anova_table = res.anova_table
        f_stat = float(anova_table['F Value'][0])
        p_value = float(anova_table['Pr > F'][0])
        df_num = float(anova_table['Num DF'][0])
        df_den = float(anova_table['Den DF'][0])
        
        # Calculate effect size (partial eta squared)
        # For RM-ANOVA, we approximate from F-statistic
        partial_eta_sq = (f_stat * df_num) / (f_stat * df_num + df_den)
        effect_interp = interpret_effect_size(partial_eta_sq, 'partial_eta_squared')
        
    except Exception as e:
        logger.error(f"Repeated measures ANOVA error: {e}")
        raise ValueError(f"Could not perform repeated measures ANOVA: {str(e)}")
    
    # Calculate descriptive statistics
    time_points = data[time_var].unique()
    descriptives = {}
    for time in time_points:
        time_data = data[data[time_var] == time][dep_var]
        descriptives[str(time)] = {
            'mean': float(time_data.mean()),
            'std': float(time_data.std()),
            'n': int(len(time_data))
        }
    
    # Create plots
    plots = []
    
    # Line plot
    fig, ax = plt.subplots(figsize=(10, 6))
    means = [descriptives[str(t)]['mean'] for t in sorted(time_points)]
    stds = [descriptives[str(t)]['std'] for t in sorted(time_points)]
    x = range(len(time_points))
    
    ax.plot(x, means, marker='o', linewidth=2, markersize=8)
    ax.errorbar(x, means, yerr=stds, fmt='none', ecolor='gray', alpha=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels([str(t) for t in sorted(time_points)])
    ax.set_xlabel(time_var)
    ax.set_ylabel(f'{dep_var} (Mean ± SD)')
    ax.set_title(f'Repeated Measures: {dep_var} over {time_var}')
    ax.grid(alpha=0.3)
    plots.append({
        'title': f'Line Plot: {dep_var} over {time_var}',
        'type': 'line',
        'base64': plot_to_base64(fig)
    })
    
    # Test results
    test_results = {
        'test': 'Repeated Measures ANOVA',
        'F_statistic': f_stat,
        'p_value': p_value,
        'df_numerator': df_num,
        'df_denominator': df_den,
        'significant': p_value < alpha,
        'alpha': alpha,
        'partial_eta_squared': partial_eta_sq,
        'effect_size_interpretation': effect_interp,
        'descriptives': descriptives
    }
    
    # Summary
    summary = f"Repeated Measures ANOVA: F({df_num:.1f}, {df_den:.1f}) = {f_stat:.3f}, p = {p_value:.4f}"
    if p_value < alpha:
        summary += f" (significant at α={alpha})"
    summary += f"\nEffect Size: ηp² = {partial_eta_sq:.3f} ({effect_interp})"
    
    # Interpretation
    if p_value < alpha:
        interpretation = f"There is a statistically significant effect of {time_var} on {dep_var} "
        interpretation += f"(p = {p_value:.4f}). "
        interpretation += f"The effect size is {effect_interp} (ηp² = {partial_eta_sq:.3f}). "
        interpretation += f"This indicates that {dep_var} changes significantly across {time_var}."
    else:
        interpretation = f"There is no statistically significant effect of {time_var} on {dep_var} "
        interpretation += f"(p = {p_value:.4f}). "
        interpretation += f"{dep_var} does not change significantly across {time_var}."
    
    # Assumptions
    assumptions = [
        {
            'name': 'Sphericity',
            'passed': None,
            'message': 'Variances of differences between all pairs of within-subject conditions should be equal'
        },
        {
            'name': 'Normality',
            'passed': None,
            'message': 'Differences between conditions should be normally distributed'
        },
        {
            'name': 'No outliers',
            'passed': None,
            'message': 'Check for extreme outliers in the differences'
        }
    ]
    
    # Recommendations
    recommendations = []
    if p_value < alpha:
        recommendations.append("Conduct post-hoc pairwise comparisons with Bonferroni correction")
        recommendations.append("Report effect sizes for pairwise comparisons")
    recommendations.append("Check sphericity assumption with Mauchly's test")
    recommendations.append("If sphericity is violated, apply Greenhouse-Geisser or Huynh-Feldt correction")
    
    result = {
        'analysis_type': 'repeated_measures_anova',
        'summary': summary,
        'test_results': test_results,
        'plots': plots,
        'interpretation': interpretation,
        'assumptions': assumptions,
        'recommendations': recommendations
    }
    
    return result


def posthoc_tukey(df: pd.DataFrame, opts: Dict) -> Dict:
    """
    Tukey HSD Post-hoc Test
    Pairwise comparisons after ANOVA
    """
    group_var = opts.get('groupVar')
    dep_var = opts.get('dependentVar')
    alpha = opts.get('alpha', 0.05)
    
    if not group_var or not dep_var:
        raise ValueError("Group variable and dependent variable required")
    
    # Clean data
    data = df[[group_var, dep_var]].dropna()
    
    # Perform Tukey HSD
    mc = MultiComparison(data[dep_var], data[group_var])
    result_tukey = mc.tukeyhsd(alpha=alpha)
    
    # Extract pairwise comparisons
    comparisons = []
    # Get summary as DataFrame for easier access
    summary_df = result_tukey.summary()
    
    # Parse the summary table
    for i in range(1, len(summary_df.data)):  # Skip header row
        row = summary_df.data[i]
        comparisons.append({
            'group1': str(row[0]),
            'group2': str(row[1]),
            'mean_diff': float(row[2]),
            'lower_ci': float(row[3]),
            'upper_ci': float(row[4]),
            'p_adj': float(row[5]),
            'reject': bool(result_tukey.reject[i-1])
        })
    
    # Create visualization
    plots = []
    fig, ax = plt.subplots(figsize=(10, 8))
    result_tukey.plot_simultaneous(ax=ax)
    ax.set_title('Tukey HSD Confidence Intervals')
    plots.append({
        'title': 'Tukey HSD Confidence Intervals',
        'type': 'tukey',
        'base64': plot_to_base64(fig)
    })
    
    # Test results
    test_results = {
        'test': 'Tukey HSD',
        'alpha': alpha,
        'comparisons': comparisons,
        'n_comparisons': len(comparisons),
        'n_significant': sum(1 for c in comparisons if c['reject'])
    }
    
    # Summary
    n_sig = test_results['n_significant']
    n_total = test_results['n_comparisons']
    summary = f"Tukey HSD: {n_sig} of {n_total} pairwise comparisons are significant at α={alpha}"
    
    # Interpretation
    if n_sig > 0:
        sig_pairs = [f"{c['group1']} vs {c['group2']}" for c in comparisons if c['reject']]
        interpretation = f"Significant differences found between: {', '.join(sig_pairs)}. "
        interpretation += "These groups differ significantly after adjusting for multiple comparisons."
    else:
        interpretation = "No significant pairwise differences found after adjusting for multiple comparisons."
    
    result = {
        'analysis_type': 'posthoc_tukey',
        'summary': summary,
        'test_results': test_results,
        'plots': plots,
        'interpretation': interpretation
    }
    
    return result


def convert_to_python_types(obj):
    """Convert numpy/pandas types to Python native types for JSON serialization"""
    if isinstance(obj, dict):
        return {k: convert_to_python_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_python_types(item) for item in obj]
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return convert_to_python_types(obj.tolist())
    elif pd.isna(obj):
        return None
    return obj
