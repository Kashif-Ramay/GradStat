"""
Statistical analysis functions for GradStat
"""

import pandas as pd
import numpy as np
from logger_config import logger, log_analysis_start, log_analysis_complete, log_analysis_error, log_inf_nan_detected
import time
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    confusion_matrix, classification_report, roc_curve, roc_auc_score,
    accuracy_score, precision_score, recall_score, f1_score
)
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from typing import Dict, List, Any

def plot_to_base64(fig) -> str:
    """Convert matplotlib figure to base64 string"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_base64

def format_pvalue(p: float) -> str:
    """Format p-value for display - use scientific notation for very small values"""
    if p < 0.0001:
        return f"{p:.4e}"
    else:
        return f"{p:.4f}"

def convert_to_python_types(obj, path="root"):
    """Convert numpy types to Python native types for JSON serialization and handle inf/nan"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        val = float(obj)
        # Replace inf and nan with None for JSON compatibility
        if np.isinf(val) or np.isnan(val):
            log_inf_nan_detected(path, "numpy_float")
            return None
        return val
    elif isinstance(obj, float):
        # Also check regular Python floats
        if np.isinf(obj) or np.isnan(obj):
            log_inf_nan_detected(path, "python_float")
            return None
        return obj
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_to_python_types(value, f"{path}.{key}") for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_python_types(item, f"{path}[{i}]") for i, item in enumerate(obj)]
    return obj

def descriptive_analysis(df: pd.DataFrame, opts: Dict) -> Dict:
    """Perform descriptive statistical analysis"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    # Summary statistics
    summary = df[numeric_cols].describe().to_dict()
    
    # Plots
    plots = []
    
    # Distribution plots
    for col in numeric_cols[:4]:  # Limit to first 4
        fig, ax = plt.subplots(figsize=(8, 5))
        df[col].hist(bins=30, ax=ax, edgecolor='black')
        ax.set_title(f'Distribution of {col}')
        ax.set_xlabel(col)
        ax.set_ylabel('Frequency')
        plots.append({
            "title": f"Distribution: {col}",
            "type": "histogram",
            "base64": plot_to_base64(fig)
        })
    
    # Correlation heatmap if multiple numeric columns
    if len(numeric_cols) > 1:
        fig, ax = plt.subplots(figsize=(10, 8))
        corr = df[numeric_cols].corr()
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
        ax.set_title('Correlation Matrix')
        plots.append({
            "title": "Correlation Heatmap",
            "type": "heatmap",
            "base64": plot_to_base64(fig)
        })
    
    result = {
        "analysis_type": "descriptive",
        "summary": f"Analyzed {len(numeric_cols)} numeric variables across {len(df)} observations",
        "test_results": summary,
        "plots": plots,
        "interpretation": generate_descriptive_interpretation(df, numeric_cols),
        "code_snippet": generate_code_snippet("descriptive", opts),
        "recommendations": ["Consider checking for outliers", "Examine variable distributions"]
    }
    result["conclusion"] = generate_conclusion(result, opts)
    return convert_to_python_types(result)

def group_comparison_analysis(df: pd.DataFrame, opts: Dict) -> Dict:
    """Perform group comparison (t-test, ANOVA, etc.)"""
    group_var = opts.get('groupVar')
    dep_var = opts.get('dependentVar')
    alpha = opts.get('alpha', 0.05)
    
    if not group_var or not dep_var:
        raise ValueError("Group variable and dependent variable required")
    
    # Clean data
    data = df[[group_var, dep_var]].dropna()
    groups = data[group_var].unique()
    n_groups = len(groups)
    
    plots = []
    assumptions = []
    
    # Boxplot
    fig, ax = plt.subplots(figsize=(10, 6))
    data.boxplot(column=dep_var, by=group_var, ax=ax)
    ax.set_title(f'{dep_var} by {group_var}')
    plots.append({
        "title": f"Boxplot: {dep_var} by {group_var}",
        "type": "boxplot",
        "base64": plot_to_base64(fig)
    })
    
    # Perform appropriate test
    if n_groups == 2:
        # Check if data is paired (duplicate IDs or explicit paired structure)
        is_paired = False
        id_col = None
        
        # Look for ID columns
        id_cols = [col for col in df.columns if 'id' in col.lower() or 'subject' in col.lower() or 'patient' in col.lower()]
        print(f"DEBUG: All columns: {df.columns.tolist()}")
        print(f"DEBUG: Found ID columns: {id_cols}")
        
        if id_cols:
            id_col = id_cols[0]
            # Check if we have duplicate IDs (indicating repeated measures)
            has_duplicates = df[id_col].duplicated().any()
            print(f"DEBUG: ID column '{id_col}' has duplicates: {has_duplicates}")
            print(f"DEBUG: Unique IDs: {df[id_col].nunique()}, Total rows: {len(df)}")
            
            if has_duplicates:
                is_paired = True
                print(f"DEBUG: PAIRED DATA DETECTED!")
        
        if is_paired and id_col:
            # PAIRED T-TEST
            # Reshape data to wide format for paired test
            try:
                # Get unique IDs and ensure we have exactly 2 measurements per ID
                pivot_data = data.pivot(index=id_col, columns=group_var, values=dep_var)
                
                if len(pivot_data.columns) == 2:
                    group1_data = pivot_data.iloc[:, 0].dropna().values
                    group2_data = pivot_data.iloc[:, 1].dropna().values
                    
                    # Ensure same length (paired)
                    min_len = min(len(group1_data), len(group2_data))
                    group1_data = group1_data[:min_len]
                    group2_data = group2_data[:min_len]
                    
                    # Check normality of differences
                    differences = group1_data - group2_data
                    if len(differences) >= 3:
                        norm_stat, norm_p = stats.shapiro(differences)
                        normality_ok = norm_p > 0.01 or len(differences) > 30
                    else:
                        norm_p = 1.0
                        normality_ok = True
                    
                    assumptions.append({
                        "name": "Normality of Differences (Shapiro-Wilk)",
                        "passed": normality_ok,
                        "pValue": float(norm_p),
                        "message": "Differences are approximately normal" if normality_ok else "Consider Wilcoxon signed-rank test"
                    })
                    
                    # Perform paired t-test
                    t_stat, p_value = stats.ttest_rel(group1_data, group2_data)
                    
                    # Effect size (Cohen's d for paired data)
                    mean_diff = np.mean(differences)
                    std_diff = np.std(differences, ddof=1)
                    cohens_d = mean_diff / std_diff if std_diff > 0 else 0
                    
                    test_results = {
                        "test": "Paired t-test",
                        "t_statistic": float(t_stat),
                        "p_value": float(p_value),
                        "df": len(differences) - 1,
                        "mean_difference": float(mean_diff),
                        "mean_group_1": float(np.mean(group1_data)),
                        "mean_group_2": float(np.mean(group2_data)),
                        "cohens_d": float(cohens_d),
                        "n_pairs": len(differences),
                        "significant": p_value < alpha
                    }
                    print(f"DEBUG: Successfully performed PAIRED t-test with {len(differences)} pairs")
                else:
                    raise ValueError("Paired data must have exactly 2 groups")
            except Exception as e:
                # Fall back to independent t-test if pairing fails
                is_paired = False
                print(f"Warning: Could not perform paired t-test ({str(e)}), using independent t-test")
        
        if not is_paired:
            # INDEPENDENT T-TEST
            group_data = [data[data[group_var] == g][dep_var].values for g in groups]
            
            # Check normality (with practical considerations)
            norm_tests = [stats.shapiro(g) for g in group_data if len(g) >= 3]
            min_p = min([p for _, p in norm_tests]) if norm_tests else 1.0
            
            # For moderate to large samples, use more lenient criteria
            total_n = sum(len(g) for g in group_data)
            
            # Normality is acceptable if:
            # 1. p > 0.01 (lenient threshold), OR
            # 2. Sample size > 30 per group (CLT applies)
            normality_ok = (min_p > 0.01) or (all(len(g) > 30 for g in group_data))
            
            if normality_ok:
                message = "Data are approximately normal (or sample size sufficient for t-test robustness)"
            elif min_p > 0.001:
                message = "Minor deviation from normality. T-test is robust with this sample size"
            else:
                message = "Consider Mann-Whitney U test as non-parametric alternative"
            
            assumptions.append({
                "name": "Normality (Shapiro-Wilk)",
                "passed": normality_ok,
                "pValue": min_p,
                "message": message
            })
            
            # Levene's test for equal variances
            levene_stat, levene_p = stats.levene(*group_data)
            var_equal = levene_p > alpha
            
            assumptions.append({
                "name": "Equal Variances (Levene)",
                "passed": var_equal,
                "pValue": levene_p,
                "message": "Variances are equal" if var_equal else "Variances are unequal"
            })
            
            # Perform t-test
            t_stat, p_value = stats.ttest_ind(*group_data, equal_var=var_equal)
            
            # Effect size (Cohen's d)
            mean_diff = np.mean(group_data[0]) - np.mean(group_data[1])
            pooled_std = np.sqrt((np.var(group_data[0]) + np.var(group_data[1])) / 2)
            cohens_d = mean_diff / pooled_std if pooled_std > 0 else 0
            
            test_results = {
                "test": "Independent t-test",
                "t_statistic": float(t_stat),
                "p_value": float(p_value),
                "df": len(data) - 2,
                "mean_group_1": float(np.mean(group_data[0])),
                "mean_group_2": float(np.mean(group_data[1])),
                "cohens_d": float(cohens_d),
                "significant": p_value < alpha
            }
            print(f"DEBUG: Performed INDEPENDENT t-test (is_paired={is_paired})")
        
    else:
        # One-way ANOVA
        group_data = [data[data[group_var] == g][dep_var].values for g in groups]
        
        f_stat, p_value = stats.f_oneway(*group_data)
        
        test_results = {
            "test": "One-way ANOVA",
            "f_statistic": float(f_stat),
            "p_value": float(p_value),
            "df_between": n_groups - 1,
            "df_within": len(data) - n_groups,
            "significant": p_value < alpha
        }
        
        # Post-hoc Tukey HSD if significant
        if p_value < alpha:
            tukey = pairwise_tukeyhsd(data[dep_var], data[group_var], alpha=alpha)
            test_results["posthoc"] = str(tukey)
    
    result = {
        "analysis_type": "group-comparison",
        "summary": f"Compared {n_groups} groups on {dep_var}",
        "test_results": test_results,
        "assumptions": assumptions,
        "plots": plots,
        "interpretation": generate_group_comparison_interpretation(test_results, alpha),
        "code_snippet": generate_code_snippet("group-comparison", opts),
        "recommendations": generate_recommendations_from_results(test_results, assumptions)
    }
    result["conclusion"] = generate_conclusion(result, opts)
    return convert_to_python_types(result)

def regression_analysis(df: pd.DataFrame, opts: Dict) -> Dict:
    """Perform linear regression analysis (simple or multiple)"""
    dep_var = opts.get('dependentVar')
    indep_vars = opts.get('independentVars', [])
    
    # Support both single and multiple predictors
    if not indep_vars:
        indep_var = opts.get('independentVar')
        if indep_var:
            indep_vars = [indep_var]
    
    alpha = opts.get('alpha', 0.05)
    
    if not dep_var or not indep_vars:
        raise ValueError("Dependent and independent variable(s) required")
    
    # Clean data
    all_vars = [dep_var] + indep_vars
    data = df[all_vars].dropna()
    X = data[indep_vars].values
    y = data[dep_var].values
    
    # Handle single vs multiple predictors
    is_simple = len(indep_vars) == 1
    if is_simple:
        X = X.reshape(-1, 1)
    
    # Fit model
    X_with_const = sm.add_constant(X)
    model = sm.OLS(y, X_with_const).fit()
    
    plots = []
    
    # Scatter plot with regression line (only for simple regression)
    if is_simple:
        # Try using Plotly for interactive plot
        try:
            from visualization import create_scatter_plot
            import plotly.graph_objects as go
            
            # Create scatter plot
            fig = go.Figure()
            
            # Add scatter points
            fig.add_trace(go.Scatter(
                x=X.flatten(),
                y=y,
                mode='markers',
                name='Data',
                marker=dict(size=8, color='#1f77b4', opacity=0.6),
                hovertemplate=f'{indep_vars[0]}: %{{x}}<br>{dep_var}: %{{y}}<extra></extra>'
            ))
            
            # Add regression line
            x_line = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
            x_line_with_const = sm.add_constant(x_line)
            y_line = model.predict(x_line_with_const)
            
            fig.add_trace(go.Scatter(
                x=x_line.flatten(),
                y=y_line,
                mode='lines',
                name='Regression Line',
                line=dict(color='red', width=2),
                hoverinfo='skip'
            ))
            
            fig.update_layout(
                title=f'Linear Regression: {dep_var} ~ {indep_vars[0]}',
                xaxis_title=indep_vars[0],
                yaxis_title=dep_var,
                template='plotly_white',
                hovermode='closest',
                font=dict(size=12),
                showlegend=True
            )
            
            import json
            plots.append({
                "title": "Regression Plot",
                "type": "plotly",
                "data": json.loads(fig.to_json()),
                "interactive": True
            })
        except ImportError:
            # Fallback to matplotlib
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(X, y, alpha=0.5)
            ax.plot(X, model.predict(X_with_const), 'r-', linewidth=2)
            ax.set_xlabel(indep_vars[0])
            ax.set_ylabel(dep_var)
            ax.set_title(f'Linear Regression: {dep_var} ~ {indep_vars[0]}')
            plots.append({
                "title": "Regression Plot",
                "type": "scatter",
                "base64": plot_to_base64(fig)
            })
    else:
        # For multiple regression, show actual vs predicted
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(y, model.fittedvalues, alpha=0.5)
        ax.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', linewidth=2)
        ax.set_xlabel(f'Actual {dep_var}')
        ax.set_ylabel(f'Predicted {dep_var}')
        ax.set_title('Actual vs Predicted Values')
        plots.append({
            "title": "Actual vs Predicted",
            "type": "scatter",
            "base64": plot_to_base64(fig)
        })
        
        # Add correlation matrix heatmap for multiple regression
        fig, ax = plt.subplots(figsize=(10, 8))
        corr_matrix = data[indep_vars].corr()
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                    center=0, vmin=-1, vmax=1, square=True, ax=ax,
                    cbar_kws={'label': 'Correlation'})
        ax.set_title('Predictor Correlation Matrix')
        plt.tight_layout()
        plots.append({
            "title": "Predictor Correlations",
            "type": "heatmap",
            "base64": plot_to_base64(fig)
        })
    
    # Residual plot
    residuals = model.resid
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(model.fittedvalues, residuals, alpha=0.5)
    ax.axhline(y=0, color='r', linestyle='--')
    ax.set_xlabel('Fitted Values')
    ax.set_ylabel('Residuals')
    ax.set_title('Residual Plot')
    plots.append({
        "title": "Residual Plot",
        "type": "scatter",
        "base64": plot_to_base64(fig)
    })
    
    # Check assumptions
    assumptions = []
    
    # Normality of residuals (using multiple criteria for robustness)
    _, norm_p = stats.shapiro(residuals)
    
    # For larger samples (n > 50), use a more lenient threshold
    # and also check skewness and kurtosis
    n = len(residuals)
    skewness = stats.skew(residuals)
    kurtosis = stats.kurtosis(residuals)
    
    # Normality is "good enough" if:
    # 1. p-value > 0.01 (more lenient than 0.05), OR
    # 2. Large sample (n > 50) AND skewness/kurtosis are reasonable
    normality_ok = (norm_p > 0.01) or (n > 50 and abs(skewness) < 2 and abs(kurtosis) < 7)
    
    if normality_ok:
        message = "Residuals are approximately normally distributed (acceptable for inference)"
    elif norm_p > 0.001:
        message = "Minor deviation from normality detected. Results are still robust with this sample size (Central Limit Theorem applies)"
    else:
        message = "Residuals show non-normality. Consider robust regression or transformation if concerned"
    
    assumptions.append({
        "name": "Normality of Residuals",
        "passed": normality_ok,
        "pValue": float(norm_p),
        "message": message
    })
    
    # Check for multicollinearity (VIF) if multiple predictors
    vif_values = {}
    if not is_simple and len(indep_vars) > 1:
        from statsmodels.stats.outliers_influence import variance_inflation_factor
        try:
            # Check for zero variance or constant columns
            variances = np.var(X, axis=0)
            zero_var_cols = [indep_vars[i] for i, v in enumerate(variances) if v < 1e-10]
            
            if zero_var_cols:
                vif_message = f"Cannot calculate VIF: Variables with zero variance detected: {', '.join(zero_var_cols)}"
                assumptions.append({
                    "name": "Multicollinearity Check (VIF)",
                    "passed": False,
                    "message": vif_message
                })
            else:
                # Calculate correlation matrix to check for perfect correlations
                corr_matrix = np.corrcoef(X.T)
                np.fill_diagonal(corr_matrix, 0)  # Ignore diagonal
                max_corr = np.max(np.abs(corr_matrix))
                
                if max_corr > 0.99:
                    # Find which variables are highly correlated
                    high_corr_pairs = []
                    for i in range(len(indep_vars)):
                        for j in range(i+1, len(indep_vars)):
                            if abs(corr_matrix[i, j]) > 0.99:
                                high_corr_pairs.append(f"{indep_vars[i]} & {indep_vars[j]} (r={corr_matrix[i, j]:.3f})")
                    
                    vif_message = f"Extremely high correlation detected (r > 0.99). Remove one variable from each pair: {'; '.join(high_corr_pairs[:3])}"
                    assumptions.append({
                        "name": "Multicollinearity Check (VIF)",
                        "passed": False,
                        "message": vif_message
                    })
                else:
                    # Calculate VIF for each predictor using X with constant
                    # VIF should be calculated on the design matrix WITH intercept
                    for i, var in enumerate(indep_vars):
                        try:
                            # VIF calculation: regress X_i on all other X variables (with constant)
                            vif = variance_inflation_factor(X_with_const, i + 1)  # +1 to skip constant column
                            # Cap VIF at 999 for display purposes
                            vif_values[var] = float(min(vif, 999.99))
                        except:
                            vif_values[var] = 999.99  # Indicates calculation issue
                    
                    max_vif = max(vif_values.values())
                    vif_ok = max_vif < 10
                    
                    # Identify problematic variables
                    high_vif_vars = [var for var, vif in vif_values.items() if vif > 10]
                    
                    if vif_ok:
                        vif_message = f"No multicollinearity detected (max VIF = {max_vif:.2f})"
                    elif max_vif < 20:
                        vif_message = f"Moderate multicollinearity (max VIF = {max_vif:.2f}). Consider removing: {', '.join(high_vif_vars)}"
                    else:
                        vif_message = f"Severe multicollinearity (max VIF = {max_vif:.2f}). Remove variables: {', '.join(high_vif_vars[:3])}"
                    
                    assumptions.append({
                        "name": "Multicollinearity Check (VIF)",
                        "passed": vif_ok,
                        "message": vif_message
                    })
        except Exception as e:
            # If VIF calculation fails, provide helpful message
            assumptions.append({
                "name": "Multicollinearity Check (VIF)",
                "passed": False,
                "message": f"VIF calculation failed. Check for: (1) constant variables, (2) perfect correlations, (3) linear dependencies. Error: {str(e)[:100]}"
            })
    
    # Build coefficients dictionary
    coefficients = {"intercept": float(model.params[0])}
    std_errors = {"intercept": float(model.bse[0])}
    p_values = {"intercept": float(model.pvalues[0])}
    
    for i, var in enumerate(indep_vars):
        coefficients[var] = float(model.params[i + 1])
        std_errors[var] = float(model.bse[i + 1])
        p_values[var] = float(model.pvalues[i + 1])
    
    test_results = {
        "r_squared": float(model.rsquared),
        "adj_r_squared": float(model.rsquared_adj),
        "f_statistic": float(model.fvalue),
        "f_pvalue": float(model.f_pvalue),
        "n_predictors": len(indep_vars),
        "coefficients": coefficients,
        "std_errors": std_errors,
        "p_values": p_values
    }
    
    if vif_values:
        test_results["vif"] = vif_values
    
    # Create summary
    if is_simple:
        summary = f"Linear regression: {dep_var} ~ {indep_vars[0]} (R² = {model.rsquared:.3f})"
        interpretation = generate_regression_interpretation(test_results, indep_vars[0], dep_var)
    else:
        predictors_str = " + ".join(indep_vars)
        summary = f"Multiple regression: {dep_var} ~ {predictors_str} (R² = {model.rsquared:.3f}, Adj R² = {model.rsquared_adj:.3f})"
        interpretation = f"Multiple regression model with {len(indep_vars)} predictors explains {model.rsquared:.1%} of variance in {dep_var}. "
        sig_predictors = [var for var in indep_vars if p_values[var] < 0.05]
        if sig_predictors:
            interpretation += f"Significant predictors: {', '.join(sig_predictors)}."
        else:
            interpretation += "No predictors reached statistical significance."
    
    result = {
        "analysis_type": "regression",
        "summary": summary,
        "test_results": test_results,
        "assumptions": assumptions,
        "plots": plots,
        "interpretation": interpretation,
        "code_snippet": generate_code_snippet("regression", opts),
        "recommendations": generate_recommendations_from_results(test_results, assumptions)
    }
    result["conclusion"] = generate_conclusion(result, opts)
    return convert_to_python_types(result)

def nonparametric_test(df: pd.DataFrame, opts: Dict) -> Dict:
    """Perform non-parametric tests (Mann-Whitney U, Kruskal-Wallis, Wilcoxon)"""
    test_type = opts.get('testType', 'mann-whitney')
    group_var = opts.get('groupVar')
    dep_var = opts.get('dependentVar')
    alpha = opts.get('alpha', 0.05)
    
    if not dep_var:
        raise ValueError("Dependent variable required")
    
    data = df[[dep_var, group_var]].dropna() if group_var else df[[dep_var]].dropna()
    
    plots = []
    assumptions = []
    
    if test_type == 'mann-whitney' or test_type == 'kruskal-wallis':
        if not group_var:
            raise ValueError("Group variable required for Mann-Whitney U or Kruskal-Wallis test")
        
        groups = data[group_var].unique()
        n_groups = len(groups)
        
        # Boxplot
        fig, ax = plt.subplots(figsize=(10, 6))
        data.boxplot(column=dep_var, by=group_var, ax=ax)
        ax.set_title(f'{dep_var} by {group_var}')
        ax.set_xlabel(group_var)
        ax.set_ylabel(dep_var)
        plt.suptitle('')  # Remove default title
        plots.append({
            "title": f"Boxplot: {dep_var} by {group_var}",
            "type": "boxplot",
            "base64": plot_to_base64(fig)
        })
        
        if n_groups == 2:
            # Mann-Whitney U test
            group_data = [data[data[group_var] == g][dep_var].values for g in groups]
            u_stat, p_value = stats.mannwhitneyu(*group_data, alternative='two-sided')
            
            # Effect size (rank-biserial correlation)
            n1, n2 = len(group_data[0]), len(group_data[1])
            r = 1 - (2*u_stat) / (n1 * n2)
            
            test_results = {
                "test": "Mann-Whitney U test",
                "u_statistic": float(u_stat),
                "p_value": float(p_value),
                "effect_size_r": float(r),
                "n_group_1": n1,
                "n_group_2": n2,
                "median_group_1": float(np.median(group_data[0])),
                "median_group_2": float(np.median(group_data[1])),
                "significant": p_value < alpha
            }
            
            p_formatted = format_pvalue(p_value)
            interpretation = f"Mann-Whitney U test {'found significant differences' if p_value < alpha else 'found no significant differences'} between groups (p = {p_formatted}). "
            interpretation += f"Median {dep_var}: {groups[0]} = {test_results['median_group_1']:.2f}, {groups[1]} = {test_results['median_group_2']:.2f}."
            
        else:
            # Kruskal-Wallis test
            group_data = [data[data[group_var] == g][dep_var].values for g in groups]
            h_stat, p_value = stats.kruskal(*group_data)
            
            medians = {str(g): float(np.median(data[data[group_var] == g][dep_var])) for g in groups}
            
            test_results = {
                "test": "Kruskal-Wallis H test",
                "h_statistic": float(h_stat),
                "p_value": float(p_value),
                "df": n_groups - 1,
                "medians": medians,
                "significant": p_value < alpha
            }
            
            p_formatted = format_pvalue(p_value)
            interpretation = f"Kruskal-Wallis test {'found significant differences' if p_value < alpha else 'found no significant differences'} among {n_groups} groups (p = {p_formatted})."
        
        assumptions.append({
            "name": "No Normality Assumption",
            "passed": True,
            "message": "Non-parametric test - does not assume normality"
        })
        
    elif test_type == 'wilcoxon':
        # Wilcoxon signed-rank test (paired samples)
        var1 = opts.get('variable1')
        var2 = opts.get('variable2')
        
        if not var1 or not var2:
            raise ValueError("Two variables required for Wilcoxon signed-rank test")
        
        data = df[[var1, var2]].dropna()
        w_stat, p_value = stats.wilcoxon(data[var1], data[var2])
        
        test_results = {
            "test": "Wilcoxon signed-rank test",
            "w_statistic": float(w_stat),
            "p_value": float(p_value),
            "n_pairs": len(data),
            "median_diff": float(np.median(data[var1] - data[var2])),
            "significant": p_value < alpha
        }
        
        p_formatted = format_pvalue(p_value)
        interpretation = f"Wilcoxon signed-rank test {'found significant differences' if p_value < alpha else 'found no significant differences'} between paired samples (p = {p_formatted})."
        
        # Histogram of differences
        fig, ax = plt.subplots(figsize=(10, 6))
        differences = data[var1] - data[var2]
        ax.hist(differences, bins=20, edgecolor='black', alpha=0.7)
        ax.axvline(x=0, color='r', linestyle='--', label='No difference')
        ax.set_xlabel(f'{var1} - {var2}')
        ax.set_ylabel('Frequency')
        ax.set_title('Distribution of Differences')
        ax.legend()
        plots.append({
            "title": "Distribution of Differences",
            "type": "histogram",
            "base64": plot_to_base64(fig)
        })
        
        assumptions.append({
            "name": "Paired Samples",
            "passed": True,
            "message": "Data are paired observations"
        })
    
    result = {
        "analysis_type": "nonparametric",
        "summary": f"{test_results['test']}: {test_results.get('p_value', 0):.4f}",
        "test_results": test_results,
        "assumptions": assumptions,
        "plots": plots,
        "interpretation": interpretation,
        "code_snippet": generate_code_snippet("nonparametric", opts),
        "recommendations": ["Non-parametric tests are robust to outliers and non-normal distributions"]
    }
    result["conclusion"] = generate_conclusion(result, opts)
    return convert_to_python_types(result)

def categorical_analysis(df: pd.DataFrame, opts: Dict) -> Dict:
    """Perform categorical data analysis (Chi-square, Fisher's exact test)"""
    var1 = opts.get('variable1')
    var2 = opts.get('variable2')
    alpha = opts.get('alpha', 0.05)
    
    if not var1 or not var2:
        raise ValueError("Two categorical variables required")
    
    data = df[[var1, var2]].dropna()
    
    # Create contingency table
    contingency_table = pd.crosstab(data[var1], data[var2])
    
    plots = []
    assumptions = []
    
    # Stacked bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    contingency_table.plot(kind='bar', stacked=True, ax=ax, colormap='viridis')
    ax.set_title(f'{var1} vs {var2}')
    ax.set_xlabel(var1)
    ax.set_ylabel('Count')
    ax.legend(title=var2)
    plt.tight_layout()
    plots.append({
        "title": f"Stacked Bar Chart: {var1} vs {var2}",
        "type": "bar",
        "base64": plot_to_base64(fig)
    })
    
    # Heatmap of contingency table
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(contingency_table, annot=True, fmt='d', cmap='YlOrRd', ax=ax)
    ax.set_title('Contingency Table Heatmap')
    plots.append({
        "title": "Contingency Table Heatmap",
        "type": "heatmap",
        "base64": plot_to_base64(fig)
    })
    
    # Determine which test to use
    expected_freq = stats.contingency.expected_freq(contingency_table)
    min_expected = expected_freq.min()
    
    # Use Fisher's exact for 2x2 tables with small expected frequencies
    use_fisher = (contingency_table.shape == (2, 2) and min_expected < 5)
    
    if use_fisher:
        # Fisher's exact test
        oddsratio, p_value = stats.fisher_exact(contingency_table)
        
        test_results = {
            "test": "Fisher's Exact Test",
            "p_value": float(p_value),
            "odds_ratio": float(oddsratio),
            "contingency_table": contingency_table.to_dict(),
            "significant": p_value < alpha
        }
        
        p_formatted = format_pvalue(p_value)
        interpretation = f"Fisher's exact test {'found a significant association' if p_value < alpha else 'found no significant association'} between {var1} and {var2} (p = {p_formatted}). "
        interpretation += f"Odds ratio = {oddsratio:.2f}."
        
        assumptions.append({
            "name": "Small Expected Frequencies",
            "passed": True,
            "message": f"Fisher's exact test used (min expected frequency = {min_expected:.1f} < 5)"
        })
        
    else:
        # Chi-square test
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        
        # Cramér's V (effect size)
        n = contingency_table.sum().sum()
        min_dim = min(contingency_table.shape[0], contingency_table.shape[1]) - 1
        cramers_v = np.sqrt(chi2 / (n * min_dim))
        
        test_results = {
            "test": "Chi-Square Test of Independence",
            "chi2_statistic": float(chi2),
            "p_value": float(p_value),
            "degrees_of_freedom": int(dof),
            "cramers_v": float(cramers_v),
            "contingency_table": contingency_table.to_dict(),
            "expected_frequencies": pd.DataFrame(expected, 
                                                 index=contingency_table.index,
                                                 columns=contingency_table.columns).to_dict(),
            "significant": p_value < alpha
        }
        
        p_formatted = format_pvalue(p_value)
        interpretation = f"Chi-square test {'found a significant association' if p_value < alpha else 'found no significant association'} between {var1} and {var2} (χ² = {chi2:.2f}, p = {p_formatted}). "
        
        if cramers_v < 0.1:
            effect = "negligible"
        elif cramers_v < 0.3:
            effect = "small"
        elif cramers_v < 0.5:
            effect = "medium"
        else:
            effect = "large"
        
        interpretation += f"Effect size (Cramér's V = {cramers_v:.3f}) is {effect}."
        
        # Check assumption
        all_expected_ok = (expected >= 5).all()
        assumptions.append({
            "name": "Expected Frequencies ≥ 5",
            "passed": all_expected_ok,
            "message": f"All expected frequencies ≥ 5: {all_expected_ok}. Min expected = {min_expected:.2f}"
        })
    
    result = {
        "analysis_type": "categorical",
        "summary": f"{test_results['test']}: {var1} × {var2} (p = {format_pvalue(p_value)})",
        "test_results": test_results,
        "assumptions": assumptions,
        "plots": plots,
        "interpretation": interpretation,
        "code_snippet": generate_code_snippet("categorical", opts),
        "recommendations": ["Examine the contingency table to understand the pattern of association"]
    }
    result["conclusion"] = generate_conclusion(result, opts)
    return convert_to_python_types(result)

def clustering_analysis(df: pd.DataFrame, opts: Dict) -> Dict:
    """Enhanced clustering analysis with elbow method, silhouette analysis, and hierarchical clustering"""
    from sklearn.metrics import silhouette_score, silhouette_samples
    from scipy.cluster.hierarchy import dendrogram, linkage
    from sklearn.cluster import AgglomerativeClustering
    
    n_clusters = opts.get('nClusters', 3)
    method = opts.get('method', 'kmeans')  # 'kmeans' or 'hierarchical'
    show_elbow = opts.get('showElbow', True)
    
    # Select numeric columns
    numeric_data = df.select_dtypes(include=[np.number]).dropna()
    
    if len(numeric_data.columns) < 2:
        raise ValueError("Need at least 2 numeric columns for clustering")
    
    # Standardize data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(numeric_data)
    
    plots = []
    
    # Elbow method and silhouette analysis
    if show_elbow:
        inertias = []
        silhouette_scores_list = []
        # Ensure we test at least k=2 to k=10, or up to n_samples-1 if dataset is small
        max_k = min(11, len(X_scaled))
        K_range = range(2, max_k) if max_k > 2 else range(2, 3)
        
        for k in K_range:
            kmeans_temp = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans_temp.fit(X_scaled)
            inertias.append(kmeans_temp.inertia_)
            silhouette_scores_list.append(silhouette_score(X_scaled, kmeans_temp.labels_))
        
        # Plot elbow curve and silhouette scores
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        ax1.plot(list(K_range), inertias, 'bo-', linewidth=2, markersize=8)
        ax1.set_xlabel('Number of Clusters (k)', fontsize=11)
        ax1.set_ylabel('Inertia (Within-cluster sum of squares)', fontsize=11)
        ax1.set_title('Elbow Method For Optimal k', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.axvline(x=n_clusters, color='r', linestyle='--', alpha=0.7, label=f'Selected k={n_clusters}')
        ax1.legend()
        
        ax2.plot(list(K_range), silhouette_scores_list, 'ro-', linewidth=2, markersize=8)
        ax2.set_xlabel('Number of Clusters (k)', fontsize=11)
        ax2.set_ylabel('Silhouette Score', fontsize=11)
        ax2.set_title('Silhouette Score vs Number of Clusters', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.axvline(x=n_clusters, color='r', linestyle='--', alpha=0.7, label=f'Selected k={n_clusters}')
        ax2.axhline(y=0.5, color='g', linestyle=':', alpha=0.5, label='Good threshold (0.5)')
        ax2.legend()
        
        plt.tight_layout()
        plots.append({
            "title": "Optimal Clusters Analysis",
            "type": "line",
            "base64": plot_to_base64(fig)
        })
    
    # Perform clustering based on method
    if method == 'kmeans':
        model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = model.fit_predict(X_scaled)
        centers = model.cluster_centers_
        inertia = model.inertia_
    else:  # hierarchical
        model = AgglomerativeClustering(n_clusters=n_clusters)
        clusters = model.fit_predict(X_scaled)
        centers = None
        inertia = None
        
        # Create dendrogram
        fig, ax = plt.subplots(figsize=(12, 6))
        linkage_matrix = linkage(X_scaled, method='ward')
        dendrogram(linkage_matrix, ax=ax, truncate_mode='lastp', p=30)
        ax.set_title('Hierarchical Clustering Dendrogram', fontsize=12, fontweight='bold')
        ax.set_xlabel('Sample Index or (Cluster Size)', fontsize=11)
        ax.set_ylabel('Distance', fontsize=11)
        ax.axhline(y=linkage_matrix[-n_clusters+1, 2], color='r', linestyle='--', 
                   label=f'Cut for {n_clusters} clusters')
        ax.legend()
        plots.append({
            "title": "Dendrogram",
            "type": "dendrogram",
            "base64": plot_to_base64(fig)
        })
    
    # Calculate silhouette score for chosen k
    silhouette_avg = silhouette_score(X_scaled, clusters)
    silhouette_vals = silhouette_samples(X_scaled, clusters)
    
    # Silhouette plot
    fig, ax = plt.subplots(figsize=(10, 7))
    y_lower = 10
    
    for i in range(n_clusters):
        cluster_silhouette_vals = silhouette_vals[clusters == i]
        cluster_silhouette_vals.sort()
        
        size_cluster_i = cluster_silhouette_vals.shape[0]
        y_upper = y_lower + size_cluster_i
        
        color = plt.cm.nipy_spectral(float(i) / n_clusters)
        ax.fill_betweenx(np.arange(y_lower, y_upper),
                         0, cluster_silhouette_vals,
                         facecolor=color, edgecolor=color, alpha=0.7)
        
        ax.text(-0.05, y_lower + 0.5 * size_cluster_i, f'Cluster {i}', fontsize=10)
        y_lower = y_upper + 10
    
    ax.set_title(f'Silhouette Plot (Average Score = {silhouette_avg:.3f})', 
                 fontsize=12, fontweight='bold')
    ax.set_xlabel('Silhouette Coefficient', fontsize=11)
    ax.set_ylabel('Cluster', fontsize=11)
    ax.axvline(x=silhouette_avg, color="red", linestyle="--", linewidth=2, label=f'Average = {silhouette_avg:.3f}')
    ax.axvline(x=0, color="black", linestyle="-", linewidth=0.5)
    ax.legend()
    ax.set_xlim([-0.1, 1])
    
    plots.append({
        "title": "Silhouette Plot",
        "type": "silhouette",
        "base64": plot_to_base64(fig)
    })
    
    # Cluster visualization (2D scatter plot)
    if X_scaled.shape[1] >= 2:
        fig, ax = plt.subplots(figsize=(10, 8))
        scatter = ax.scatter(X_scaled[:, 0], X_scaled[:, 1], c=clusters, 
                           cmap='viridis', alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
        
        if method == 'kmeans' and centers is not None:
            ax.scatter(centers[:, 0], centers[:, 1], 
                      c='red', marker='X', s=300, edgecolors='black', linewidth=2, 
                      label='Centroids', zorder=10)
        
        ax.set_xlabel(f'{numeric_data.columns[0]} (standardized)', fontsize=11)
        ax.set_ylabel(f'{numeric_data.columns[1]} (standardized)', fontsize=11)
        ax.set_title(f'{method.title()} Clustering (k={n_clusters})', fontsize=12, fontweight='bold')
        ax.legend()
        plt.colorbar(scatter, ax=ax, label='Cluster')
        
        plots.append({
            "title": "Cluster Visualization",
            "type": "scatter",
            "base64": plot_to_base64(fig)
        })
    
    # Cluster sizes
    unique, counts = np.unique(clusters, return_counts=True)
    cluster_sizes = dict(zip([int(u) for u in unique], [int(c) for c in counts]))
    
    # Build test results
    test_results = {
        "n_clusters": n_clusters,
        "method": method,
        "silhouette_score": float(silhouette_avg),
        "cluster_sizes": cluster_sizes,
        "n_samples": len(clusters),
        "n_features": X_scaled.shape[1]
    }
    
    if inertia is not None:
        test_results["inertia"] = float(inertia)
    
    # Interpretation
    interpretation = f"{method.title()} clustering identified {n_clusters} distinct groups in the data. "
    interpretation += f"The silhouette score of {silhouette_avg:.3f} indicates "
    
    if silhouette_avg > 0.7:
        quality = "strong, well-separated cluster structure"
    elif silhouette_avg > 0.5:
        quality = "reasonable cluster structure"
    elif silhouette_avg > 0.25:
        quality = "weak cluster structure"
    else:
        quality = "poor cluster structure - consider different number of clusters or method"
    
    interpretation += quality + ". "
    interpretation += f"Cluster sizes range from {min(cluster_sizes.values())} to {max(cluster_sizes.values())} members."
    
    # Recommendations
    recommendations = []
    if silhouette_avg < 0.5:
        recommendations.append("Consider trying a different number of clusters (check elbow plot)")
    if method == 'kmeans':
        recommendations.append("Try hierarchical clustering for comparison")
    else:
        recommendations.append("Try K-means clustering for comparison")
    recommendations.append("Examine cluster characteristics using descriptive statistics")
    recommendations.append("Consider domain knowledge when interpreting clusters")
    
    result = {
        "analysis_type": "clustering",
        "summary": f"{method.title()} clustering with k={n_clusters} (Silhouette = {silhouette_avg:.3f})",
        "test_results": test_results,
        "plots": plots,
        "interpretation": interpretation,
        "code_snippet": generate_code_snippet("clustering", opts),
        "recommendations": recommendations
    }
    result["conclusion"] = generate_conclusion(result, opts)
    return convert_to_python_types(result)

def pca_analysis(df: pd.DataFrame, opts: Dict) -> Dict:
    """Perform PCA analysis"""
    n_components = opts.get('nComponents', 2)
    
    # Select numeric columns
    numeric_data = df.select_dtypes(include=[np.number]).dropna()
    
    if len(numeric_data.columns) < 2:
        raise ValueError("Need at least 2 numeric columns for PCA")
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(numeric_data)
    
    # Perform PCA
    pca = PCA(n_components=min(n_components, X_scaled.shape[1]))
    X_pca = pca.fit_transform(X_scaled)
    
    plots = []
    
    # Scree plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(range(1, len(pca.explained_variance_ratio_) + 1), pca.explained_variance_ratio_)
    ax.set_xlabel('Principal Component')
    ax.set_ylabel('Explained Variance Ratio')
    ax.set_title('Scree Plot')
    plots.append({
        "title": "Scree Plot",
        "type": "bar",
        "base64": plot_to_base64(fig)
    })
    
    # Biplot (if 2+ components)
    if X_pca.shape[1] >= 2:
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.5)
        ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
        ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
        ax.set_title('PCA Biplot')
        plots.append({
            "title": "PCA Biplot",
            "type": "scatter",
            "base64": plot_to_base64(fig)
        })
    
    test_results = {
        "n_components": int(pca.n_components_),
        "explained_variance_ratio": [float(x) for x in pca.explained_variance_ratio_],
        "cumulative_variance": [float(x) for x in np.cumsum(pca.explained_variance_ratio_)],
        "components": pca.components_.tolist()
    }
    
    result = {
        "analysis_type": "pca",
        "summary": f"PCA reduced {len(numeric_data.columns)} variables to {pca.n_components_} components",
        "test_results": test_results,
        "plots": plots,
        "interpretation": f"First {pca.n_components_} components explain {np.sum(pca.explained_variance_ratio_):.1%} of variance",
        "code_snippet": generate_code_snippet("pca", opts),
        "recommendations": ["Examine component loadings", "Consider number of components to retain"]
    }
    result["conclusion"] = generate_conclusion(result, opts)
    return convert_to_python_types(result)

def time_series_analysis(df: pd.DataFrame, opts: Dict) -> Dict:
    """Perform basic time series analysis"""
    date_col = opts.get('dateColumn')
    
    if not date_col:
        raise ValueError("Date column required for time series analysis")
    
    # Convert to datetime
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)
    
    # Select numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    plots = []
    
    # Time series plot
    for col in numeric_cols[:3]:  # Limit to 3
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df[date_col], df[col])
        ax.set_xlabel('Date')
        ax.set_ylabel(col)
        ax.set_title(f'Time Series: {col}')
        plt.xticks(rotation=45)
        plots.append({
            "title": f"Time Series: {col}",
            "type": "line",
            "base64": plot_to_base64(fig)
        })
    
    result = {
        "analysis_type": "time-series",
        "summary": f"Time series analysis of {len(numeric_cols)} variables",
        "plots": plots,
        "interpretation": "Time series plotted. Consider seasonal decomposition for deeper analysis.",
        "code_snippet": generate_code_snippet("time-series", opts),
        "recommendations": ["Consider seasonal decomposition", "Check for trends and patterns"]
    }
    result["conclusion"] = generate_conclusion(result, opts)
    return convert_to_python_types(result)

# Helper functions for interpretation
def generate_descriptive_interpretation(df, numeric_cols):
    """Generate plain language interpretation of descriptive stats"""
    n = len(df)
    n_vars = len(numeric_cols)
    return f"Dataset contains {n} observations across {n_vars} numeric variables. Review the summary statistics and distributions to understand central tendency and spread."

def generate_group_comparison_interpretation(results, alpha):
    """Generate interpretation for group comparison"""
    p_val = results.get('p_value', 1)
    p_formatted = format_pvalue(p_val)
    if p_val < alpha:
        return f"Significant difference found (p = {p_formatted}). Groups differ on the outcome variable."
    else:
        return f"No significant difference found (p = {p_formatted}). Groups appear similar on the outcome variable."

def generate_regression_interpretation(results, x_var, y_var):
    """Generate interpretation for regression"""
    r2 = results['r_squared']
    coefficients = results.get('coefficients', {})
    p_values = results.get('p_values', {})
    
    # Get the coefficient and p-value for the predictor (not intercept)
    slope = coefficients.get(x_var, coefficients.get('slope', 0))
    p_val = p_values.get(x_var, p_values.get('slope', 1))
    
    if p_val < 0.05:
        direction = "positive" if slope > 0 else "negative"
        return f"Significant {direction} relationship found. {x_var} explains {r2:.1%} of variance in {y_var}."
    else:
        return f"No significant relationship found (p = {format_pvalue(p_val)})."

def generate_recommendations_from_results(results, assumptions):
    """Generate recommendations based on results"""
    recs = []
    
    if not all(a['passed'] for a in assumptions):
        recs.append("Some assumptions violated - consider non-parametric alternatives")
    
    if results.get('significant'):
        recs.append("Report effect sizes and confidence intervals")
        recs.append("Consider replication with independent sample")
    
    return recs

def generate_conclusion(results: dict, opts: dict) -> str:
    """Generate a comprehensive conclusion paragraph summarizing all findings"""
    analysis_type = results.get('analysis_type', '')
    
    if analysis_type == 'descriptive':
        summary = results.get('summary', '')
        return f"In conclusion, this descriptive analysis provided a comprehensive overview of the dataset. {summary} The visualizations and summary statistics reveal the central tendencies, variability, and distributions of the variables. These findings establish a foundation for understanding the data structure and can guide subsequent inferential analyses."
    
    elif analysis_type == 'group-comparison':
        test_results = results.get('test_results', {})
        p_val = test_results.get('p_value', 1)
        test_name = test_results.get('test', 'Statistical test')
        significant = test_results.get('significant', False)
        
        if significant:
            effect_size = test_results.get('cohens_d', test_results.get('f_statistic', 'N/A'))
            conclusion = f"In conclusion, the {test_name} revealed statistically significant differences between groups (p = {format_pvalue(p_val)}). "
            if isinstance(effect_size, (int, float)):
                conclusion += f"The effect size suggests a meaningful practical difference. "
            conclusion += "These findings indicate that the grouping variable has a substantial impact on the outcome measure. Researchers should consider these group differences when interpreting results and planning interventions."
        else:
            conclusion = f"In conclusion, the {test_name} did not reveal statistically significant differences between groups (p = {format_pvalue(p_val)}). The groups appear to be similar with respect to the outcome variable. This suggests that the grouping factor may not be a strong predictor of the outcome, or that the sample size may be insufficient to detect smaller effects."
        
        return conclusion
    
    elif analysis_type == 'regression':
        test_results = results.get('test_results', {})
        r2 = test_results.get('r_squared', 0)
        n_predictors = test_results.get('n_predictors', 1)
        coefficients = test_results.get('coefficients', {})
        p_values = test_results.get('p_values', {})
        
        # Get predictor names (exclude intercept)
        predictor_names = [k for k in coefficients.keys() if k != 'intercept']
        
        # Check if model is significant (F-test)
        f_pvalue = test_results.get('f_pvalue', 1)
        
        if f_pvalue < 0.05:
            # Model is significant
            if n_predictors == 1:
                # Simple regression
                pred_name = predictor_names[0] if predictor_names else 'predictor'
                slope = coefficients.get(pred_name, 0)
                direction = "positive" if slope > 0 else "negative"
                conclusion = f"In conclusion, this regression analysis identified a statistically significant {direction} relationship between the predictor and outcome variables (F p-value = {f_pvalue:.4f}). "
            else:
                # Multiple regression
                sig_predictors = [name for name in predictor_names if p_values.get(name, 1) < 0.05]
                conclusion = f"In conclusion, this multiple regression analysis with {n_predictors} predictors is statistically significant (F p-value = {f_pvalue:.4f}). "
                if sig_predictors:
                    conclusion += f"Significant predictors include: {', '.join(sig_predictors)}. "
            
            conclusion += f"The model explains {r2:.1%} of the variance in the outcome, indicating {'strong' if r2 > 0.5 else 'moderate' if r2 > 0.3 else 'modest'} predictive power. "
            conclusion += "These findings support the hypothesis that the independent variable(s) are meaningful predictors and can be used for forecasting or understanding the outcome variable."
        else:
            conclusion = f"In conclusion, the regression analysis did not identify a statistically significant relationship (F p-value = {f_pvalue:.4f}). "
            conclusion += f"The model explains only {r2:.1%} of the variance, suggesting that other unmeasured factors may be more important predictors of the outcome."
        
        return conclusion
    
    elif analysis_type == 'clustering':
        test_results = results.get('test_results', {})
        n_clusters = test_results.get('n_clusters', 0)
        cluster_sizes = test_results.get('cluster_sizes', {})
        
        conclusion = f"In conclusion, the clustering analysis successfully identified {n_clusters} distinct groups within the data. "
        conclusion += f"The clusters vary in size (ranging from {min(cluster_sizes.values())} to {max(cluster_sizes.values())} members), "
        conclusion += "suggesting natural subgroups with different characteristics. These clusters can be used for targeted interventions, personalized approaches, or further investigation of subgroup-specific patterns. The identified groupings provide valuable insights into the heterogeneity of the dataset."
        
        return conclusion
    
    elif analysis_type == 'pca':
        test_results = results.get('test_results', {})
        n_components = test_results.get('n_components', 0)
        explained_var = test_results.get('explained_variance_ratio', [])
        total_var = sum(explained_var) if explained_var else 0
        
        conclusion = f"In conclusion, the Principal Component Analysis successfully reduced the dimensionality of the data to {n_components} components, "
        conclusion += f"which collectively explain {total_var:.1%} of the total variance. "
        conclusion += "This dimensionality reduction simplifies the data structure while preserving most of the information, making it easier to visualize patterns and relationships. The principal components represent the main axes of variation in the dataset and can be used for further analysis or visualization."
        
        return conclusion
    
    elif analysis_type == 'time-series':
        conclusion = "In conclusion, the time series analysis revealed temporal patterns and trends in the data. "
        conclusion += "The visualizations show how variables change over time, which is essential for understanding dynamics, forecasting future values, and identifying seasonal or cyclical patterns. "
        conclusion += "These insights can inform time-sensitive decisions and help predict future outcomes based on historical trends."
        
        return conclusion
    
    elif analysis_type == 'nonparametric':
        test_results = results.get('test_results', {})
        p_val = test_results.get('p_value', 1)
        test_name = test_results.get('test', 'Non-parametric test')
        significant = test_results.get('significant', False)
        
        if significant:
            conclusion = f"In conclusion, the {test_name} revealed statistically significant differences (p = {format_pvalue(p_val)}). "
            conclusion += "As a non-parametric test, these results are robust to violations of normality and are based on ranks rather than raw values. "
            conclusion += "The findings suggest meaningful differences exist between groups/conditions that are not dependent on distributional assumptions."
        else:
            conclusion = f"In conclusion, the {test_name} did not reveal statistically significant differences (p = {format_pvalue(p_val)}). "
            conclusion += "The groups/conditions appear similar in terms of their central tendencies and distributions."
        
        return conclusion
    
    elif analysis_type == 'categorical':
        test_results = results.get('test_results', {})
        p_val = test_results.get('p_value', 1)
        test_name = test_results.get('test', 'Categorical test')
        significant = test_results.get('significant', False)
        
        if significant:
            effect_size = test_results.get('cramers_v', test_results.get('odds_ratio'))
            conclusion = f"In conclusion, the {test_name} revealed a statistically significant association between the variables (p = {format_pvalue(p_val)}). "
            if isinstance(effect_size, (int, float)):
                conclusion += f"The effect size indicates a meaningful relationship. "
            conclusion += "These findings suggest that the two categorical variables are not independent, and knowing the value of one variable provides information about the other. Researchers should examine the contingency table to understand the specific pattern of association."
        else:
            conclusion = f"In conclusion, the {test_name} did not reveal a statistically significant association (p = {format_pvalue(p_val)}). "
            conclusion += "The variables appear to be independent, suggesting no systematic relationship between them."
        
        return conclusion
    
    else:
        return "In conclusion, this analysis provided valuable insights into the data structure and relationships between variables. The findings should be interpreted in the context of the research question and study design."

def generate_code_snippet(analysis_type, opts):
    """Generate Python code snippet for reproducibility"""
    if analysis_type == "descriptive":
        return """import pandas as pd
df = pd.read_csv('data.csv')
print(df.describe())
df.hist(bins=30, figsize=(12, 8))"""
    
    elif analysis_type == "group-comparison":
        return f"""import pandas as pd
from scipy import stats

df = pd.read_csv('data.csv')
group1 = df[df['{opts.get("groupVar")}'] == 'group1']['{opts.get("dependentVar")}']
group2 = df[df['{opts.get("groupVar")}'] == 'group2']['{opts.get("dependentVar")}']
t_stat, p_value = stats.ttest_ind(group1, group2)
print(f'p-value: {{p_value:.4f}}')"""
    
    elif analysis_type == "regression":
        return f"""import pandas as pd
import statsmodels.api as sm

df = pd.read_csv('data.csv')
X = df[['{opts.get("independentVar")}']]
y = df['{opts.get("dependentVar")}']
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
print(model.summary())"""
    
    elif analysis_type == "clustering":
        return f"""import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('data.csv')
X = df.select_dtypes(include=['number'])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
kmeans = KMeans(n_clusters={opts.get('nClusters', 3)}, random_state=42)
clusters = kmeans.fit_predict(X_scaled)"""
    
    elif analysis_type == "pca":
        return f"""import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('data.csv')
X = df.select_dtypes(include=['number'])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
pca = PCA(n_components={opts.get('nComponents', 2)})
X_pca = pca.fit_transform(X_scaled)
print(f'Explained variance: {{pca.explained_variance_ratio_}}')"""
    
    elif analysis_type == "nonparametric":
        test_type = opts.get('testType', 'mann-whitney')
        if test_type == 'mann-whitney':
            return f"""import pandas as pd
from scipy import stats

df = pd.read_csv('data.csv')
group1 = df[df['{opts.get("groupVar")}'] == 'group1']['{opts.get("dependentVar")}']
group2 = df[df['{opts.get("groupVar")}'] == 'group2']['{opts.get("dependentVar")}']
u_stat, p_value = stats.mannwhitneyu(group1, group2)
print(f'Mann-Whitney U: {{u_stat}}, p-value: {{p_value:.4f}}')"""
        elif test_type == 'kruskal-wallis':
            return f"""import pandas as pd
from scipy import stats

df = pd.read_csv('data.csv')
groups = [df[df['{opts.get("groupVar")}'] == g]['{opts.get("dependentVar")}'] for g in df['{opts.get("groupVar")}'].unique()]
h_stat, p_value = stats.kruskal(*groups)
print(f'Kruskal-Wallis H: {{h_stat}}, p-value: {{p_value:.4f}}')"""
        else:
            return f"""import pandas as pd
from scipy import stats

df = pd.read_csv('data.csv')
w_stat, p_value = stats.wilcoxon(df['{opts.get("variable1")}'], df['{opts.get("variable2")}'])
print(f'Wilcoxon W: {{w_stat}}, p-value: {{p_value:.4f}}')"""
    
    elif analysis_type == "categorical":
        return f"""import pandas as pd
from scipy import stats

df = pd.read_csv('data.csv')
contingency_table = pd.crosstab(df['{opts.get("variable1")}'], df['{opts.get("variable2")}'])
chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
print(f'Chi-square: {{chi2:.2f}}, p-value: {{p_value:.4f}}')
print(contingency_table)"""
    
    elif analysis_type == "logistic_regression":
        predictor_cols = opts.get('predictorColumns', [])
        return f"""import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report

df = pd.read_csv('data.csv')
X = df[{predictor_cols}]
y = df['{opts.get('targetColumn')}']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size={opts.get('testSize', 0.3)}, random_state={opts.get('randomState', 42)}, stratify=y
)

# Train model
model = LogisticRegression(random_state={opts.get('randomState', 42)}, max_iter=1000)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Evaluate
auc = roc_auc_score(y_test, y_pred_proba)
cm = confusion_matrix(y_test, y_pred)
print(f'AUC-ROC: {{auc:.3f}}')
print('\\nConfusion Matrix:')
print(cm)
print('\\nClassification Report:')
print(classification_report(y_test, y_pred))"""
    
    elif analysis_type == "survival":
        duration_col = opts.get('durationColumn', 'time')
        event_col = opts.get('eventColumn', 'event')
        group_col = opts.get('groupColumn')
        covariates = opts.get('covariates', [])
        
        code = f"""import pandas as pd
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test

df = pd.read_csv('data.csv')

# Kaplan-Meier Analysis
kmf = KaplanMeierFitter()
kmf.fit(durations=df['{duration_col}'], event_observed=df['{event_col}'])
kmf.plot_survival_function()
print(f'Median survival: {{kmf.median_survival_time_}}')"""
        
        if group_col:
            code += f"""

# Compare groups with Log-Rank test
groups = df['{group_col}'].unique()
for group in groups:
    mask = df['{group_col}'] == group
    kmf.fit(durations=df[mask]['{duration_col}'], event_observed=df[mask]['{event_col}'], label=str(group))
    kmf.plot_survival_function()

# Log-Rank test
logrank_result = logrank_test(
    durations_A=df[df['{group_col}']==groups[0]]['{duration_col}'],
    durations_B=df[df['{group_col}']==groups[1]]['{duration_col}'],
    event_observed_A=df[df['{group_col}']==groups[0]]['{event_col}'],
    event_observed_B=df[df['{group_col}']==groups[1]]['{event_col}']
)
print(f'Log-Rank p-value: {{logrank_result.p_value}}')"""
        
        if covariates:
            code += f"""

# Cox Proportional Hazards Regression
cph = CoxPHFitter()
cox_data = df[['{duration_col}', '{event_col}'] + {covariates}]
cph.fit(cox_data, duration_col='{duration_col}', event_col='{event_col}')
print(cph.summary)
print(f'Concordance Index: {{cph.concordance_index_}}')"""
        
        return code
    
    elif analysis_type == "power":
        test_type = opts.get('powerAnalysisType', 't-test')
        calculate = opts.get('calculate', 'sample_size')
        return f"""from statsmodels.stats.power import TTestIndPower

# Power analysis for {test_type}
power_analysis = TTestIndPower()
result = power_analysis.solve_power(
    effect_size={opts.get('effectSize', 0.5)},
    alpha={opts.get('alpha', 0.05)},
    power={opts.get('power', 0.8)}
)
print(f'Required sample size per group: {{result:.0f}}')"""
    
    else:
        return "# Code snippet not available"

def power_analysis(opts: Dict) -> Dict:
    """Perform statistical power analysis for sample size or power calculation"""
    from statsmodels.stats.power import TTestIndPower, FTestAnovaPower, FTestPower
    
    test_type = opts.get('powerAnalysisType', 't-test')  # 't-test', 'anova', 'regression', 'correlation'
    calculate = opts.get('calculate', 'sample_size')  # 'sample_size', 'power', 'effect_size'
    
    effect_size = float(opts.get('effectSize', 0.5))
    alpha = float(opts.get('alpha', 0.05))
    power = float(opts.get('power', 0.8))
    sample_size = int(opts.get('sampleSize', 30))
    n_groups = int(opts.get('nGroups', 2))  # For ANOVA
    
    plots = []
    
    if test_type == 't-test':
        power_analyzer = TTestIndPower()
        
        if calculate == 'sample_size':
            result_value = power_analyzer.solve_power(
                effect_size=effect_size,
                alpha=alpha,
                power=power,
                ratio=1.0,
                alternative='two-sided'
            )
            result_label = "Required Sample Size per Group"
            result_unit = "participants"
        elif calculate == 'power':
            result_value = power_analyzer.solve_power(
                effect_size=effect_size,
                nobs1=sample_size,
                alpha=alpha,
                ratio=1.0,
                alternative='two-sided'
            )
            result_label = "Statistical Power"
            result_unit = ""
        else:  # effect_size
            result_value = power_analyzer.solve_power(
                nobs1=sample_size,
                alpha=alpha,
                power=power,
                ratio=1.0,
                alternative='two-sided'
            )
            result_label = "Detectable Effect Size (Cohen's d)"
            result_unit = ""
        
        # Power curve
        fig, ax = plt.subplots(figsize=(10, 6))
        sample_sizes = np.arange(10, 200, 5)
        powers = [power_analyzer.solve_power(effect_size=effect_size, nobs1=n, alpha=alpha) 
                  for n in sample_sizes]
        
        ax.plot(sample_sizes, powers, 'b-', linewidth=2.5, label='Power Curve')
        ax.axhline(y=0.8, color='r', linestyle='--', linewidth=2, label='Conventional Power = 0.80')
        if calculate == 'sample_size':
            ax.axvline(x=result_value, color='g', linestyle='--', linewidth=2, 
                      label=f'Required n = {result_value:.0f}')
            ax.plot(result_value, power, 'go', markersize=12, zorder=5)
        ax.set_xlabel('Sample Size per Group', fontsize=12, fontweight='bold')
        ax.set_ylabel('Statistical Power (1 - β)', fontsize=12, fontweight='bold')
        ax.set_title(f'Power Analysis: {test_type.upper()}\n(Effect Size = {effect_size}, α = {alpha})', 
                    fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)
        ax.set_ylim([0, 1])
        
        plots.append({
            "title": "Power Curve",
            "type": "line",
            "base64": plot_to_base64(fig)
        })
        
        # Effect size sensitivity plot
        fig, ax = plt.subplots(figsize=(10, 6))
        effect_sizes = np.arange(0.1, 1.5, 0.05)
        if calculate == 'sample_size':
            n_per_effect = [power_analyzer.solve_power(effect_size=es, alpha=alpha, power=power) 
                           for es in effect_sizes]
            ax.plot(effect_sizes, n_per_effect, 'r-', linewidth=2.5)
            ax.axvline(x=effect_size, color='g', linestyle='--', linewidth=2, 
                      label=f'Selected Effect Size = {effect_size}')
            ax.set_ylabel('Required Sample Size per Group', fontsize=12, fontweight='bold')
            ax.set_title(f'Sample Size vs Effect Size\n(Power = {power}, α = {alpha})', 
                        fontsize=13, fontweight='bold')
        else:
            powers_per_effect = [power_analyzer.solve_power(effect_size=es, nobs1=sample_size, alpha=alpha) 
                                for es in effect_sizes]
            ax.plot(effect_sizes, powers_per_effect, 'r-', linewidth=2.5)
            ax.axhline(y=0.8, color='b', linestyle='--', linewidth=2, label='Power = 0.80')
            ax.set_ylabel('Statistical Power', fontsize=12, fontweight='bold')
            ax.set_title(f'Power vs Effect Size\n(n = {sample_size} per group, α = {alpha})', 
                        fontsize=13, fontweight='bold')
        
        ax.set_xlabel("Effect Size (Cohen's d)", fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)
        
        plots.append({
            "title": "Effect Size Sensitivity",
            "type": "line",
            "base64": plot_to_base64(fig)
        })
    
    elif test_type == 'anova':
        power_analyzer = FTestAnovaPower()
        
        if calculate == 'sample_size':
            result_value = power_analyzer.solve_power(
                effect_size=effect_size,
                alpha=alpha,
                power=power,
                k_groups=n_groups
            )
            result_label = "Required Sample Size per Group"
            result_unit = "participants"
        elif calculate == 'power':
            result_value = power_analyzer.solve_power(
                effect_size=effect_size,
                nobs=sample_size * n_groups,
                alpha=alpha,
                k_groups=n_groups
            )
            result_label = "Statistical Power"
            result_unit = ""
        else:  # effect_size
            result_value = power_analyzer.solve_power(
                nobs=sample_size * n_groups,
                alpha=alpha,
                power=power,
                k_groups=n_groups
            )
            result_label = "Detectable Effect Size (Cohen's f)"
            result_unit = ""
        
        # Power curve for ANOVA
        fig, ax = plt.subplots(figsize=(10, 6))
        sample_sizes = np.arange(10, 200, 5)
        powers = [power_analyzer.solve_power(effect_size=effect_size, nobs=n*n_groups, alpha=alpha, k_groups=n_groups) 
                  for n in sample_sizes]
        
        ax.plot(sample_sizes, powers, 'b-', linewidth=2.5, label='Power Curve')
        ax.axhline(y=0.8, color='r', linestyle='--', linewidth=2, label='Power = 0.80')
        if calculate == 'sample_size':
            ax.axvline(x=result_value, color='g', linestyle='--', linewidth=2, 
                      label=f'Required n = {result_value:.0f}')
        ax.set_xlabel('Sample Size per Group', fontsize=12, fontweight='bold')
        ax.set_ylabel('Statistical Power', fontsize=12, fontweight='bold')
        ax.set_title(f'Power Analysis: ANOVA ({n_groups} groups)\n(Effect Size = {effect_size}, α = {alpha})', 
                    fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)
        ax.set_ylim([0, 1])
        
        plots.append({
            "title": "Power Curve (ANOVA)",
            "type": "line",
            "base64": plot_to_base64(fig)
        })
    
    elif test_type == 'correlation':
        # For correlation, use r to Fisher's z transformation
        if calculate == 'sample_size':
            # Approximate formula for correlation
            z_alpha = stats.norm.ppf(1 - alpha/2)
            z_beta = stats.norm.ppf(power)
            z_r = 0.5 * np.log((1 + effect_size) / (1 - effect_size))  # Fisher's z
            result_value = ((z_alpha + z_beta) / z_r) ** 2 + 3
            result_label = "Required Total Sample Size"
            result_unit = "participants"
        elif calculate == 'power':
            z_r = 0.5 * np.log((1 + effect_size) / (1 - effect_size))
            z_alpha = stats.norm.ppf(1 - alpha/2)
            z_beta = z_r * np.sqrt(sample_size - 3) - z_alpha
            result_value = stats.norm.cdf(z_beta)
            result_label = "Statistical Power"
            result_unit = ""
        else:  # effect_size
            z_alpha = stats.norm.ppf(1 - alpha/2)
            z_beta = stats.norm.ppf(power)
            z_r = (z_alpha + z_beta) / np.sqrt(sample_size - 3)
            result_value = (np.exp(2 * z_r) - 1) / (np.exp(2 * z_r) + 1)
            result_label = "Detectable Correlation (r)"
            result_unit = ""
        
        # Power curve for correlation
        fig, ax = plt.subplots(figsize=(10, 6))
        sample_sizes = np.arange(10, 500, 10)
        powers = []
        for n in sample_sizes:
            z_r = 0.5 * np.log((1 + effect_size) / (1 - effect_size))
            z_alpha = stats.norm.ppf(1 - alpha/2)
            z_beta = z_r * np.sqrt(n - 3) - z_alpha
            powers.append(stats.norm.cdf(z_beta))
        
        ax.plot(sample_sizes, powers, 'b-', linewidth=2.5, label='Power Curve')
        ax.axhline(y=0.8, color='r', linestyle='--', linewidth=2, label='Power = 0.80')
        if calculate == 'sample_size':
            ax.axvline(x=result_value, color='g', linestyle='--', linewidth=2, 
                      label=f'Required n = {result_value:.0f}')
        ax.set_xlabel('Total Sample Size', fontsize=12, fontweight='bold')
        ax.set_ylabel('Statistical Power', fontsize=12, fontweight='bold')
        ax.set_title(f'Power Analysis: Correlation\n(r = {effect_size}, α = {alpha})', 
                    fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)
        ax.set_ylim([0, 1])
        
        plots.append({
            "title": "Power Curve (Correlation)",
            "type": "line",
            "base64": plot_to_base64(fig)
        })
    
    # Build test results
    test_results = {
        "test_type": test_type,
        "calculate": calculate,
        "result_value": float(result_value),
        "result_label": result_label,
        "result_unit": result_unit,
        "effect_size": effect_size,
        "alpha": alpha,
        "power": power if calculate != 'power' else float(result_value),
        "sample_size": sample_size if calculate != 'sample_size' else float(result_value)
    }
    
    if test_type == 'anova':
        test_results["n_groups"] = n_groups
        test_results["total_sample_size"] = float(result_value * n_groups) if calculate == 'sample_size' else sample_size * n_groups
    
    # Interpretation
    interpretation = f"Power analysis for {test_type} with "
    
    if calculate == 'sample_size':
        interpretation += f"effect size = {effect_size}, α = {alpha}, and desired power = {power}: "
        interpretation += f"You need approximately **{int(np.ceil(result_value))} {result_unit}** "
        if test_type == 'anova':
            interpretation += f"per group (total N = {int(np.ceil(result_value * n_groups))}) "
        elif test_type == 't-test':
            interpretation += f"per group (total N = {int(np.ceil(result_value * 2))}) "
        interpretation += f"to achieve {power*100:.0f}% power."
    elif calculate == 'power':
        interpretation += f"effect size = {effect_size}, α = {alpha}, and n = {sample_size}: "
        interpretation += f"Your study has **{result_value*100:.1f}% power** to detect the effect. "
        if result_value < 0.8:
            interpretation += "⚠️ This is below the conventional 80% threshold. Consider increasing sample size."
        else:
            interpretation += "✅ This meets the conventional 80% power threshold."
    else:  # effect_size
        interpretation += f"n = {sample_size}, α = {alpha}, and desired power = {power}: "
        interpretation += f"You can detect an effect size of **{result_value:.3f}** or larger. "
        if test_type == 't-test' and result_value < 0.5:
            interpretation += "This allows detection of medium effects (Cohen's d ≥ 0.5)."
        elif test_type == 't-test' and result_value < 0.8:
            interpretation += "This allows detection of medium-to-large effects."
        elif test_type == 'correlation' and result_value < 0.3:
            interpretation += "This allows detection of medium-to-large correlations."
    
    # Effect size interpretation
    effect_size_guide = ""
    if test_type == 't-test':
        effect_size_guide = "Cohen's d: Small = 0.2, Medium = 0.5, Large = 0.8"
    elif test_type == 'anova':
        effect_size_guide = "Cohen's f: Small = 0.1, Medium = 0.25, Large = 0.4"
    elif test_type == 'correlation':
        effect_size_guide = "Correlation r: Small = 0.1, Medium = 0.3, Large = 0.5"
    
    # Recommendations
    recommendations = []
    if calculate == 'sample_size':
        recommendations.append(f"Account for ~15-20% dropout rate: recruit {int(np.ceil(result_value * 1.2))} per group")
        recommendations.append("Consider pilot studies to better estimate effect sizes")
        recommendations.append("Higher power (0.90) recommended for critical studies")
    elif calculate == 'power' and result_value < 0.8:
        recommendations.append(f"Increase sample size to ~{int(np.ceil(sample_size * 1.5))} per group for 80% power")
        recommendations.append("Consider reducing alpha (e.g., 0.01) only if you have adequate power")
    else:
        recommendations.append("Ensure effect size estimates are based on prior research or pilot data")
        recommendations.append("Consider sensitivity analyses with different effect sizes")
    
    recommendations.append(effect_size_guide)
    
    result = {
        "analysis_type": "power",
        "summary": f"Power Analysis: {result_label} = {result_value:.2f} {result_unit}",
        "test_results": test_results,
        "plots": plots,
        "interpretation": interpretation,
        "code_snippet": generate_code_snippet("power", opts),
        "recommendations": recommendations
    }
        
    conclusion = f"Based on power analysis for {test_type}, {interpretation}"
    result["conclusion"] = conclusion
    
    return convert_to_python_types(result)


def logistic_regression_analysis(df: pd.DataFrame, opts: Dict) -> Dict:
    """
    Perform enhanced logistic regression with ROC curve, confusion matrix, and classification metrics
    """
    from sklearn.model_selection import train_test_split
    
    target_col = opts.get('targetColumn')
    predictor_cols = opts.get('predictorColumns', [])
    test_size = float(opts.get('testSize', 0.3))
    random_state = int(opts.get('randomState', 42))
    
    if not target_col or not predictor_cols:
        raise ValueError("Target column and at least one predictor column are required")
    
    # Prepare data
    X = df[predictor_cols].copy()
    y = df[target_col].copy()
    
    # Handle missing values
    X = X.dropna()
    y = y[X.index]
    
    # Convert target to binary if categorical
    if y.dtype == 'object' or y.dtype.name == 'category':
        unique_vals = y.unique()
        if len(unique_vals) != 2:
            raise ValueError(f"Target must be binary. Found {len(unique_vals)} unique values")
        y = (y == unique_vals[1]).astype(int)
        class_names = [str(unique_vals[0]), str(unique_vals[1])]
    else:
        unique_vals = y.unique()
        if len(unique_vals) != 2:
            raise ValueError(f"Target must be binary. Found {len(unique_vals)} unique values")
        class_names = [str(int(v)) for v in sorted(unique_vals)]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Train logistic regression model
    model = LogisticRegression(random_state=random_state, max_iter=1000)
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    
    # ROC curve and AUC
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    auc_score = roc_auc_score(y_test, y_pred_proba)
    
    # Find optimal threshold (Youden's J statistic)
    j_scores = tpr - fpr
    optimal_idx = np.argmax(j_scores)
    optimal_threshold = thresholds[optimal_idx]
    
    # Plots
    plots = []
    
    # 1. ROC Curve
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {auc_score:.3f})')
    ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
    ax.scatter(fpr[optimal_idx], tpr[optimal_idx], marker='o', color='red', s=100, 
               label=f'Optimal Threshold = {optimal_threshold:.3f}', zorder=3)
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate (1 - Specificity)', fontsize=12)
    ax.set_ylabel('True Positive Rate (Sensitivity)', fontsize=12)
    ax.set_title('Receiver Operating Characteristic (ROC) Curve', fontsize=14, fontweight='bold')
    ax.legend(loc="lower right", fontsize=10)
    ax.grid(True, alpha=0.3)
    plots.append({
        "title": "ROC Curve",
        "type": "line",
        "base64": plot_to_base64(fig)
    })
    
    # 2. Confusion Matrix Heatmap
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True, 
                xticklabels=class_names, yticklabels=class_names, ax=ax,
                annot_kws={'size': 14, 'weight': 'bold'})
    ax.set_xlabel('Predicted Label', fontsize=12, fontweight='bold')
    ax.set_ylabel('True Label', fontsize=12, fontweight='bold')
    ax.set_title('Confusion Matrix', fontsize=14, fontweight='bold')
    
    # Add text annotations
    ax.text(0.5, -0.15, f'TN={tn}  FP={fp}  FN={fn}  TP={tp}', 
            ha='center', transform=ax.transAxes, fontsize=10, style='italic')
    
    plots.append({
        "title": "Confusion Matrix",
        "type": "heatmap",
        "base64": plot_to_base64(fig)
    })
    
    # 3. Feature Importance
    coefficients = pd.DataFrame({
        'Feature': predictor_cols,
        'Coefficient': model.coef_[0],
        'Abs_Coefficient': np.abs(model.coef_[0])
    }).sort_values('Abs_Coefficient', ascending=False)
    
    fig, ax = plt.subplots(figsize=(8, max(6, len(predictor_cols) * 0.4)))
    colors = ['green' if c > 0 else 'red' for c in coefficients['Coefficient']]
    ax.barh(coefficients['Feature'], coefficients['Coefficient'], color=colors, alpha=0.7)
    ax.set_xlabel('Coefficient Value', fontsize=12, fontweight='bold')
    ax.set_ylabel('Features', fontsize=12, fontweight='bold')
    ax.set_title('Feature Importance (Coefficients)', fontsize=14, fontweight='bold')
    ax.axvline(x=0, color='black', linestyle='--', linewidth=1)
    ax.grid(True, alpha=0.3, axis='x')
    plots.append({
        "title": "Feature Importance",
        "type": "bar",
        "base64": plot_to_base64(fig)
    })
    
    # 4. Probability Distribution
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(y_pred_proba[y_test == 0], bins=30, alpha=0.6, label=f'Class {class_names[0]}', color='blue')
    ax.hist(y_pred_proba[y_test == 1], bins=30, alpha=0.6, label=f'Class {class_names[1]}', color='orange')
    ax.axvline(x=0.5, color='red', linestyle='--', linewidth=2, label='Default Threshold (0.5)')
    ax.axvline(x=optimal_threshold, color='green', linestyle='--', linewidth=2, 
               label=f'Optimal Threshold ({optimal_threshold:.3f})')
    ax.set_xlabel('Predicted Probability', fontsize=12, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax.set_title('Distribution of Predicted Probabilities', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plots.append({
        "title": "Probability Distribution",
        "type": "histogram",
        "base64": plot_to_base64(fig)
    })
    
    # Test results
    test_results = {
        "model_type": "Logistic Regression",
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "n_predictors": len(predictor_cols),
        "target_variable": target_col,
        "predictor_variables": predictor_cols,
        "class_names": class_names,
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "specificity": float(specificity),
        "auc_score": float(auc_score),
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
        "default_threshold": 0.5,
        "optimal_threshold": float(optimal_threshold),
        "intercept": float(model.intercept_[0]),
        "coefficients": {col: float(coef) for col, coef in zip(predictor_cols, model.coef_[0])}
    }
    
    # Interpretation
    interpretation = f"The logistic regression model achieved an accuracy of {accuracy*100:.1f}% with an AUC-ROC of {auc_score:.3f}. "
    interpretation += f"Precision: {precision*100:.1f}%, Recall: {recall*100:.1f}%, F1-Score: {f1:.3f}. "
    interpretation += f"The optimal classification threshold is {optimal_threshold:.3f}."
    
    # Recommendations
    recommendations = []
    if auc_score < 0.7:
        recommendations.append("⚠️ Low AUC - consider adding more features or trying different algorithms")
    elif auc_score >= 0.9:
        recommendations.append("✅ Excellent model performance")
    
    if precision < 0.7:
        recommendations.append("⚠️ Low precision - many false positives")
    if recall < 0.7:
        recommendations.append("⚠️ Low recall - missing many positive cases")
    
    recommendations.append(f"Use optimal threshold ({optimal_threshold:.3f}) for balanced predictions")
    
    result = {
        "analysis_type": "logistic_regression",
        "summary": f"Logistic Regression: Accuracy = {accuracy*100:.1f}%, AUC = {auc_score:.3f}",
        "test_results": test_results,
        "plots": plots,
        "interpretation": interpretation,
        "code_snippet": generate_code_snippet("logistic_regression", opts),
        "recommendations": recommendations,
        "conclusion": f"Model achieved {accuracy*100:.1f}% accuracy with AUC of {auc_score:.3f}"
    }
    
    return convert_to_python_types(result)


def survival_analysis(df: pd.DataFrame, opts: Dict) -> Dict:
    """
    Perform survival analysis with Kaplan-Meier curves, Log-Rank test, and Cox regression
    
    Parameters:
    - duration_column: Time to event or censoring
    - event_column: Event indicator (1=event occurred, 0=censored)
    - group_column: Optional grouping variable for comparison
    - covariates: Optional list of covariates for Cox regression
    """
    
    start_time = time.time()
    log_analysis_start('survival', opts)
    
    duration_col = opts.get('durationColumn')
    event_col = opts.get('eventColumn')
    group_col = opts.get('groupColumn')
    covariates = opts.get('covariates', [])
    
    logger.info(f"Duration: {duration_col}, Event: {event_col}, Group: {group_col}, Covariates: {covariates}")
    
    if not duration_col or not event_col:
        raise ValueError("Duration and event columns are required")
    
    # Prepare data
    df_clean = df[[duration_col, event_col]].copy()
    if group_col:
        df_clean[group_col] = df[group_col]
    if covariates:
        for cov in covariates:
            df_clean[cov] = df[cov]
    
    # Remove missing values
    df_clean = df_clean.dropna()
    
    # Ensure proper data types
    try:
        df_clean[duration_col] = pd.to_numeric(df_clean[duration_col])
    except (ValueError, TypeError) as e:
        raise ValueError(f"Duration column '{duration_col}' must contain numeric values. Error: {str(e)}")
    
    try:
        df_clean[event_col] = pd.to_numeric(df_clean[event_col]).astype(int)
    except (ValueError, TypeError) as e:
        unique_vals = df_clean[event_col].unique()[:5]  # Show first 5 unique values
        raise ValueError(
            f"Event column '{event_col}' must contain numeric values (0 or 1). "
            f"Found values: {unique_vals}. "
            f"Please select a column with binary event indicators (1=event occurred, 0=censored)."
        )
    
    plots = []
    test_results = {}
    
    # 1. Kaplan-Meier Analysis
    kmf = KaplanMeierFitter()
    
    if group_col:
        # Kaplan-Meier by groups
        groups = df_clean[group_col].unique()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        group_results = {}
        for group in groups:
            mask = df_clean[group_col] == group
            kmf.fit(
                durations=df_clean[mask][duration_col],
                event_observed=df_clean[mask][event_col],
                label=str(group)
            )
            kmf.plot_survival_function(ax=ax, ci_show=True)
            
            # Store group statistics
            group_results[str(group)] = {
                'n': int(mask.sum()),
                'events': int(df_clean[mask][event_col].sum()),
                'median_survival': float(kmf.median_survival_time_) if not np.isnan(kmf.median_survival_time_) else None,
                'survival_at_times': {
                    f't_{int(t)}': float(kmf.survival_function_at_times(t).values[0])
                    for t in [df_clean[duration_col].quantile(q) for q in [0.25, 0.5, 0.75]]
                    if t <= df_clean[duration_col].max()
                }
            }
        
        ax.set_xlabel('Time', fontsize=12, fontweight='bold')
        ax.set_ylabel('Survival Probability', fontsize=12, fontweight='bold')
        ax.set_title('Kaplan-Meier Survival Curves by Group', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim([0, 1.05])
        
        plots.append({
            "title": "Kaplan-Meier Curves by Group",
            "type": "line",
            "base64": plot_to_base64(fig)
        })
        plt.close(fig)
        
        test_results['group_statistics'] = group_results
        
        # Log-Rank Test
        if len(groups) == 2:
            group1_mask = df_clean[group_col] == groups[0]
            group2_mask = df_clean[group_col] == groups[1]
            
            logrank_result = logrank_test(
                durations_A=df_clean[group1_mask][duration_col],
                durations_B=df_clean[group2_mask][duration_col],
                event_observed_A=df_clean[group1_mask][event_col],
                event_observed_B=df_clean[group2_mask][event_col]
            )
            
            test_results['logrank_test'] = {
                'test_statistic': float(logrank_result.test_statistic),
                'p_value': float(logrank_result.p_value),
                'significant': logrank_result.p_value < 0.05,
                'group1': str(groups[0]),
                'group2': str(groups[1])
            }
    
    else:
        # Overall Kaplan-Meier
        kmf.fit(
            durations=df_clean[duration_col],
            event_observed=df_clean[event_col],
            label='Overall'
        )
        
        fig, ax = plt.subplots(figsize=(10, 6))
        kmf.plot_survival_function(ax=ax, ci_show=True)
        ax.set_xlabel('Time', fontsize=12, fontweight='bold')
        ax.set_ylabel('Survival Probability', fontsize=12, fontweight='bold')
        ax.set_title('Kaplan-Meier Survival Curve', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_ylim([0, 1.05])
        
        plots.append({
            "title": "Kaplan-Meier Survival Curve",
            "type": "line",
            "base64": plot_to_base64(fig)
        })
        plt.close(fig)
        
        test_results['overall_statistics'] = {
            'n': int(len(df_clean)),
            'events': int(df_clean[event_col].sum()),
            'median_survival': float(kmf.median_survival_time_) if not np.isnan(kmf.median_survival_time_) else None
        }
    
    # 2. Cox Proportional Hazards Regression
    if covariates:
        print(f"Cox regression requested with covariates: {covariates}")
        cph = CoxPHFitter()
        
        # Prepare data for Cox model
        cox_data = df_clean[[duration_col, event_col] + covariates].copy()
        cox_data.columns = ['duration', 'event'] + covariates
        print(f"Cox data shape: {cox_data.shape}")
        print(f"Cox data columns: {cox_data.columns.tolist()}")
        
        try:
            cph.fit(cox_data, duration_col='duration', event_col='event')
            
            # Extract results
            c_index = float(cph.concordance_index_)
            log_lik = float(cph.log_likelihood_)
            
            # Use AIC_partial_ for semi-parametric models
            try:
                aic = float(cph.AIC_partial_)
            except AttributeError:
                try:
                    aic = float(cph.AIC_)
                except:
                    aic = None
            
            # Handle inf/nan in main metrics
            if np.isinf(c_index) or np.isnan(c_index):
                c_index = None
            if np.isinf(log_lik) or np.isnan(log_lik):
                log_lik = None
            if aic is not None and (np.isinf(aic) or np.isnan(aic)):
                aic = None
            
            cox_results = {
                'concordance_index': c_index,
                'log_likelihood': log_lik,
                'aic': aic,
                'covariates': {}
            }
            
            for covariate in covariates:
                hr = float(np.exp(cph.params_[covariate]))
                ci_lower = float(np.exp(cph.confidence_intervals_.loc[covariate, '95% lower-bound']))
                ci_upper = float(np.exp(cph.confidence_intervals_.loc[covariate, '95% upper-bound']))
                coef = float(cph.params_[covariate])
                se = float(cph.standard_errors_[covariate])
                p_val = float(cph.summary.loc[covariate, 'p'])
                
                # Handle inf/nan values
                if np.isinf(hr) or np.isnan(hr):
                    hr = None
                if np.isinf(ci_lower) or np.isnan(ci_lower):
                    ci_lower = None
                if np.isinf(ci_upper) or np.isnan(ci_upper):
                    ci_upper = None
                if np.isinf(coef) or np.isnan(coef):
                    coef = None
                if np.isinf(se) or np.isnan(se):
                    se = None
                if np.isinf(p_val) or np.isnan(p_val):
                    p_val = None
                
                cox_results['covariates'][covariate] = {
                    'hazard_ratio': hr,
                    'coef': coef,
                    'se': se,
                    'p_value': p_val,
                    'ci_lower': ci_lower,
                    'ci_upper': ci_upper,
                    'significant': p_val is not None and p_val < 0.05
                }
            
            test_results['cox_regression'] = cox_results
            
            # Forest plot for hazard ratios (only if we have valid values)
            hrs = [cox_results['covariates'][cov]['hazard_ratio'] for cov in covariates]
            ci_lowers = [cox_results['covariates'][cov]['ci_lower'] for cov in covariates]
            ci_uppers = [cox_results['covariates'][cov]['ci_upper'] for cov in covariates]
            
            # Check if we have any valid values
            valid_hrs = [hr for hr in hrs if hr is not None]
            
            if valid_hrs:
                fig, ax = plt.subplots(figsize=(10, max(6, len(covariates) * 0.6)))
                
                y_pos = np.arange(len(covariates))
                
                # Plot points and error bars (skip None values)
                for i, (hr, ci_l, ci_u) in enumerate(zip(hrs, ci_lowers, ci_uppers)):
                    if hr is not None and ci_l is not None and ci_u is not None:
                        color = 'red' if hr < 1 else 'green'
                        ax.scatter(hr, i, s=100, c=color, zorder=3, alpha=0.7)
                        ax.plot([ci_l, ci_u], [i, i], 'k-', linewidth=2, alpha=0.5)
                
                ax.axvline(x=1, color='black', linestyle='--', linewidth=2, label='No Effect (HR=1)')
                ax.set_yticks(y_pos)
                ax.set_yticklabels(covariates)
                ax.set_xlabel('Hazard Ratio (95% CI)', fontsize=12, fontweight='bold')
                ax.set_title('Cox Regression - Hazard Ratios', fontsize=14, fontweight='bold')
                ax.grid(True, alpha=0.3, axis='x')
                ax.legend(fontsize=10)
                
                # Add HR values as text
                max_hr = max([hr for hr in hrs if hr is not None])
                for i, (cov, hr, ci_l, ci_u) in enumerate(zip(covariates, hrs, ci_lowers, ci_uppers)):
                    if hr is not None and ci_l is not None and ci_u is not None:
                        ax.text(max_hr * 1.1, i, f'{hr:.2f} ({ci_l:.2f}-{ci_u:.2f})', 
                               va='center', fontsize=9)
                    else:
                        ax.text(max_hr * 1.1, i, 'N/A (unstable)', va='center', fontsize=9, color='red')
                
                plots.append({
                    "title": "Hazard Ratios (Cox Regression)",
                    "type": "forest",
                    "base64": plot_to_base64(fig)
                })
                plt.close(fig)
            
        except Exception as e:
            test_results['cox_regression_error'] = str(e)
            print(f"Cox regression error: {e}")
    
    # 3. Cumulative Hazard Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if group_col:
        for group in groups:
            mask = df_clean[group_col] == group
            kmf_temp = KaplanMeierFitter()
            kmf_temp.fit(
                durations=df_clean[mask][duration_col],
                event_observed=df_clean[mask][event_col],
                label=str(group)
            )
            kmf_temp.plot_cumulative_density(ax=ax)
    else:
        kmf.plot_cumulative_density(ax=ax)
    
    ax.set_xlabel('Time', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cumulative Hazard', fontsize=12, fontweight='bold')
    ax.set_title('Cumulative Hazard Function', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plots.append({
        "title": "Cumulative Hazard",
        "type": "line",
        "base64": plot_to_base64(fig)
    })
    plt.close(fig)
    
    # Add summary statistics for display
    event_rate = float(df_clean[event_col].sum() / len(df_clean))
    if np.isinf(event_rate) or np.isnan(event_rate):
        event_rate = None
    
    summary_stats = {
        'n_subjects': int(len(df_clean)),
        'n_events': int(df_clean[event_col].sum()),
        'n_censored': int(len(df_clean) - df_clean[event_col].sum()),
        'event_rate': event_rate
    }
    
    if 'overall_statistics' in test_results and test_results['overall_statistics'].get('median_survival'):
        med_surv = test_results['overall_statistics']['median_survival']
        if med_surv is not None and not (np.isinf(med_surv) or np.isnan(med_surv)):
            summary_stats['median_survival'] = med_surv
    
    test_results['summary_statistics'] = summary_stats
    
    # Interpretation
    interpretation = f"Survival analysis was performed on {len(df_clean)} observations with {df_clean[event_col].sum()} events. "
    
    if group_col and 'logrank_test' in test_results:
        lr = test_results['logrank_test']
        interpretation += f"The Log-Rank test {'showed significant' if lr['significant'] else 'showed no significant'} difference between groups (p={lr['p_value']:.4f}). "
    
    if 'cox_regression' in test_results:
        cox = test_results['cox_regression']
        interpretation += f"Cox regression achieved a concordance index of {cox['concordance_index']:.3f}. "
        
        sig_covariates = [cov for cov, vals in cox['covariates'].items() if vals['significant']]
        if sig_covariates:
            interpretation += f"Significant predictors: {', '.join(sig_covariates)}. "
    
    # Recommendations
    recommendations = []
    
    if 'overall_statistics' in test_results:
        median = test_results['overall_statistics'].get('median_survival')
        if median:
            recommendations.append(f"📊 Median survival time: {median:.1f} time units")
    
    if 'logrank_test' in test_results:
        if test_results['logrank_test']['significant']:
            recommendations.append("✅ Significant difference in survival between groups")
        else:
            recommendations.append("⚠️ No significant difference in survival between groups")
    
    if 'cox_regression' in test_results:
        cox = test_results['cox_regression']
        if cox['concordance_index'] > 0.7:
            recommendations.append(f"✅ Good model discrimination (C-index: {cox['concordance_index']:.3f})")
        elif cox['concordance_index'] > 0.6:
            recommendations.append(f"⚠️ Fair model discrimination (C-index: {cox['concordance_index']:.3f})")
        else:
            recommendations.append(f"⚠️ Poor model discrimination (C-index: {cox['concordance_index']:.3f})")
        
        for cov, vals in cox['covariates'].items():
            if vals['significant']:
                if vals['hazard_ratio'] > 1:
                    recommendations.append(f"⬆️ {cov}: Increases hazard by {(vals['hazard_ratio']-1)*100:.1f}% (HR={vals['hazard_ratio']:.2f}, p={vals['p_value']:.4f})")
                else:
                    recommendations.append(f"⬇️ {cov}: Decreases hazard by {(1-vals['hazard_ratio'])*100:.1f}% (HR={vals['hazard_ratio']:.2f}, p={vals['p_value']:.4f})")
    
    recommendations.append("💡 Check proportional hazards assumption for Cox regression")
    recommendations.append("📈 Consider stratified analysis if groups have different baseline hazards")
    
    result = {
        "analysis_type": "survival",
        "summary": f"Survival Analysis: {len(df_clean)} subjects, {df_clean[event_col].sum()} events",
        "test_results": test_results,
        "plots": plots,
        "interpretation": interpretation,
        "code_snippet": generate_code_snippet("survival", opts),
        "recommendations": recommendations,
        "conclusion": interpretation
    }
    
    return convert_to_python_types(result)

def correlation_analysis(df: pd.DataFrame, opts: Dict) -> Dict:
    """Perform correlation analysis between two or more variables"""
    variables = opts.get('variables', [])
    method = opts.get('correlationMethod', 'pearson')  # pearson, spearman, kendall
    alpha = opts.get('alpha', 0.05)
    
    if len(variables) < 2:
        raise ValueError("At least 2 variables required for correlation analysis")
    
    # Clean data
    data = df[variables].dropna()
    n = len(data)
    
    if n < 3:
        raise ValueError("Insufficient data after removing missing values (need at least 3 observations)")
    
    plots = []
    test_results = {}
    
    # If exactly 2 variables, perform detailed pairwise correlation
    if len(variables) == 2:
        var1, var2 = variables
        x = data[var1].values
        y = data[var2].values
        
        # Calculate correlation based on method
        if method == 'pearson':
            r, p_value = stats.pearsonr(x, y)
            method_name = "Pearson"
            assumptions_text = "Assumes linear relationship and normally distributed variables"
        elif method == 'spearman':
            r, p_value = stats.spearmanr(x, y)
            method_name = "Spearman's Rank"
            assumptions_text = "Non-parametric, suitable for monotonic relationships and ordinal data"
        elif method == 'kendall':
            r, p_value = stats.kendalltau(x, y)
            method_name = "Kendall's Tau"
            assumptions_text = "Non-parametric, more conservative, suitable for small samples"
        else:
            raise ValueError(f"Unknown correlation method: {method}")
        
        # Calculate confidence interval for Pearson
        ci_lower, ci_upper = None, None
        if method == 'pearson' and n > 3:
            # Fisher's z-transformation for CI
            z = np.arctanh(r)
            se = 1 / np.sqrt(n - 3)
            z_crit = stats.norm.ppf(1 - alpha/2)
            ci_z_lower = z - z_crit * se
            ci_z_upper = z + z_crit * se
            ci_lower = np.tanh(ci_z_lower)
            ci_upper = np.tanh(ci_z_upper)
        
        # R-squared
        r_squared = r ** 2
        
        # Effect size interpretation
        abs_r = abs(r)
        if abs_r < 0.1:
            effect_size = "Negligible"
        elif abs_r < 0.3:
            effect_size = "Small"
        elif abs_r < 0.5:
            effect_size = "Medium"
        else:
            effect_size = "Large"
        
        # Direction
        direction = "positive" if r > 0 else "negative" if r < 0 else "no"
        
        test_results = {
            "method": method_name,
            "correlation": float(r),
            "p_value": float(p_value),
            "r_squared": float(r_squared),
            "n": int(n),
            "significant": p_value < alpha,
            "effect_size": effect_size,
            "direction": direction,
            "alpha": alpha
        }
        
        if ci_lower is not None:
            test_results["ci_lower"] = float(ci_lower)
            test_results["ci_upper"] = float(ci_upper)
            test_results["confidence_level"] = int((1 - alpha) * 100)
        
        # Scatter plot with regression line
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(x, y, alpha=0.6, s=50, edgecolors='black', linewidths=0.5)
        
        # Add regression line
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        x_line = np.linspace(x.min(), x.max(), 100)
        ax.plot(x_line, p(x_line), "r-", linewidth=2, label=f'r = {r:.3f}')
        
        ax.set_xlabel(var1, fontsize=12, fontweight='bold')
        ax.set_ylabel(var2, fontsize=12, fontweight='bold')
        ax.set_title(f'{method_name} Correlation: {var1} vs {var2}\nr = {r:.3f}, p = {format_pvalue(p_value)}', 
                    fontsize=13, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plots.append({
            "title": "Scatter Plot with Regression Line",
            "type": "scatter",
            "base64": plot_to_base64(fig)
        })
        
        # Residual plot
        fig, ax = plt.subplots(figsize=(10, 6))
        fitted = p(x)
        residuals = y - fitted
        ax.scatter(fitted, residuals, alpha=0.6, s=50, edgecolors='black', linewidths=0.5)
        ax.axhline(y=0, color='r', linestyle='--', linewidth=2)
        ax.set_xlabel('Fitted Values', fontsize=12, fontweight='bold')
        ax.set_ylabel('Residuals', fontsize=12, fontweight='bold')
        ax.set_title('Residual Plot', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        plots.append({
            "title": "Residual Plot",
            "type": "scatter",
            "base64": plot_to_base64(fig)
        })
        
        # Generate interpretation
        sig_text = "statistically significant" if p_value < alpha else "not statistically significant"
        ci_text = f" (95% CI: [{ci_lower:.3f}, {ci_upper:.3f}])" if ci_lower is not None else ""
        p_formatted = format_pvalue(p_value)
        
        interpretation = (
            f"There is a {effect_size.lower()} {direction} correlation between {var1} and {var2} "
            f"(r = {r:.3f}, p = {p_formatted}){ci_text}. "
            f"This correlation is {sig_text} at the α = {alpha} level. "
            f"The correlation coefficient of {r:.3f} indicates that approximately {r_squared*100:.1f}% "
            f"of the variance in one variable is associated with the other variable."
        )
        
        if method == 'pearson':
            interpretation += " Pearson correlation assumes a linear relationship between variables."
        elif method == 'spearman':
            interpretation += " Spearman's rank correlation is appropriate for monotonic relationships and is robust to outliers."
        else:
            interpretation += " Kendall's tau is a conservative measure suitable for small samples and ordinal data."
        
        summary = f"{method_name} correlation between {var1} and {var2}: r = {r:.3f}, p = {p_formatted}"
        
    else:
        # Multiple variables - create correlation matrix
        if method == 'pearson':
            corr_matrix = data.corr(method='pearson')
            method_name = "Pearson"
        elif method == 'spearman':
            corr_matrix = data.corr(method='spearman')
            method_name = "Spearman's Rank"
        elif method == 'kendall':
            corr_matrix = data.corr(method='kendall')
            method_name = "Kendall's Tau"
        else:
            raise ValueError(f"Unknown correlation method: {method}")
        
        # Calculate p-values for all pairs
        p_matrix = pd.DataFrame(np.zeros((len(variables), len(variables))), 
                               index=variables, columns=variables)
        
        for i, var1 in enumerate(variables):
            for j, var2 in enumerate(variables):
                if i != j:
                    if method == 'pearson':
                        _, p = stats.pearsonr(data[var1], data[var2])
                    elif method == 'spearman':
                        _, p = stats.spearmanr(data[var1], data[var2])
                    else:
                        _, p = stats.kendalltau(data[var1], data[var2])
                    p_matrix.loc[var1, var2] = p
                else:
                    p_matrix.loc[var1, var2] = 0
        
        # Correlation heatmap with significance stars
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Create annotations with significance stars
        annot = np.empty_like(corr_matrix, dtype=object)
        for i in range(len(variables)):
            for j in range(len(variables)):
                r_val = corr_matrix.iloc[i, j]
                p_val = p_matrix.iloc[i, j]
                
                if i == j:
                    annot[i, j] = f'{r_val:.2f}'
                else:
                    stars = ''
                    if p_val < 0.001:
                        stars = '***'
                    elif p_val < 0.01:
                        stars = '**'
                    elif p_val < 0.05:
                        stars = '*'
                    annot[i, j] = f'{r_val:.2f}{stars}'
        
        sns.heatmap(corr_matrix, annot=annot, fmt='', cmap='coolwarm', 
                   center=0, vmin=-1, vmax=1, square=True, ax=ax,
                   cbar_kws={'label': 'Correlation Coefficient'},
                   linewidths=0.5, linecolor='gray')
        ax.set_title(f'{method_name} Correlation Matrix\n* p<0.05, ** p<0.01, *** p<0.001', 
                    fontsize=13, fontweight='bold')
        plt.tight_layout()
        
        plots.append({
            "title": "Correlation Matrix with Significance",
            "type": "heatmap",
            "base64": plot_to_base64(fig)
        })
        
        # Find strongest correlations (excluding diagonal)
        corr_flat = []
        for i in range(len(variables)):
            for j in range(i+1, len(variables)):
                corr_flat.append({
                    'var1': variables[i],
                    'var2': variables[j],
                    'r': corr_matrix.iloc[i, j],
                    'p': p_matrix.iloc[i, j]
                })
        
        corr_flat_sorted = sorted(corr_flat, key=lambda x: abs(x['r']), reverse=True)
        
        test_results = {
            "method": method_name,
            "n_variables": len(variables),
            "n": int(n),
            "correlation_matrix": corr_matrix.to_dict(),
            "p_value_matrix": p_matrix.to_dict(),
            "strongest_correlations": [
                {
                    "variables": f"{c['var1']} & {c['var2']}",
                    "correlation": float(c['r']),
                    "p_value": float(c['p']),
                    "significant": c['p'] < alpha
                }
                for c in corr_flat_sorted[:5]  # Top 5
            ]
        }
        
        # Interpretation
        n_sig = sum(1 for c in corr_flat if c['p'] < alpha)
        n_total = len(corr_flat)
        
        interpretation = (
            f"Correlation matrix computed using {method_name} correlation for {len(variables)} variables "
            f"(N = {n}). Out of {n_total} pairwise correlations, {n_sig} are statistically significant "
            f"at the α = {alpha} level. "
        )
        
        if corr_flat_sorted:
            strongest = corr_flat_sorted[0]
            p_formatted = format_pvalue(strongest['p'])
            interpretation += (
                f"The strongest correlation is between {strongest['var1']} and {strongest['var2']} "
                f"(r = {strongest['r']:.3f}, p = {p_formatted}). "
            )
        
        interpretation += (
            "Significance levels: * p < 0.05, ** p < 0.01, *** p < 0.001. "
            "Note: Multiple comparisons may inflate Type I error rate. "
            "Consider applying Bonferroni correction for conservative interpretation."
        )
        
        summary = f"{method_name} correlation matrix for {len(variables)} variables (N = {n})"
    
    # Assumptions
    assumptions = []
    
    if method == 'pearson':
        assumptions.append({
            "name": "Linearity",
            "passed": None,
            "message": "Pearson correlation assumes a linear relationship. Check scatter plots for linearity."
        })
        assumptions.append({
            "name": "Normality",
            "passed": None,
            "message": "Pearson correlation assumes normally distributed variables. Consider Spearman for non-normal data."
        })
    else:
        assumptions.append({
            "name": "Monotonicity",
            "passed": None,
            "message": f"{method_name} correlation assumes a monotonic relationship (not necessarily linear)."
        })
    
    assumptions.append({
        "name": "Independence",
        "passed": None,
        "message": "Observations should be independent. Avoid repeated measures or clustered data."
    })
    
    # Recommendations
    recommendations = []
    
    if method == 'pearson' and len(variables) == 2:
        recommendations.append("Check scatter plot for linearity and outliers")
        recommendations.append("Consider Spearman correlation if relationship is non-linear but monotonic")
        recommendations.append("Consider Kendall's tau for small samples or ordinal data")
    
    if len(variables) > 2:
        recommendations.append("Apply Bonferroni correction (α/n) for multiple comparisons")
        recommendations.append("Focus on strongest correlations for interpretation")
        recommendations.append("Consider partial correlations to control for confounding")
    
    if test_results.get('significant'):
        recommendations.append("Correlation does not imply causation - consider experimental design")
        recommendations.append("Report effect size (correlation coefficient) along with p-value")
    
    result = {
        "analysis_type": "correlation",
        "summary": summary,
        "test_results": test_results,
        "assumptions": assumptions,
        "plots": plots,
        "interpretation": interpretation,
        "code_snippet": generate_code_snippet("correlation", opts),
        "recommendations": recommendations
    }
    
    result["conclusion"] = interpretation
    
    return convert_to_python_types(result)
