"""
Data Quality Checks
Comprehensive data validation and quality assessment
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import logging

logger = logging.getLogger(__name__)


def analyze_data_quality(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Comprehensive data quality analysis
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary with quality report
    """
    report = {
        'overall_score': 100,
        'issues': [],
        'visualizations': [],
        'recommendations': [],
        'summary': {
            'total_issues': 0,
            'errors': 0,
            'warnings': 0,
            'info': 0
        }
    }
    
    try:
        # 1. Missing data analysis
        missing_issues = analyze_missing_data(df)
        report['issues'].extend(missing_issues['issues'])
        if missing_issues['visualization']:
            report['visualizations'].append(missing_issues['visualization'])
        
        # 2. Outlier detection
        outlier_issues = detect_outliers(df)
        report['issues'].extend(outlier_issues['issues'])
        if outlier_issues['visualization']:
            report['visualizations'].append(outlier_issues['visualization'])
        
        # 3. Data type validation
        type_issues = validate_data_types(df)
        report['issues'].extend(type_issues['issues'])
        
        # 4. Sample size check
        sample_issues = check_sample_size(df)
        report['issues'].extend(sample_issues['issues'])
        
        # 5. Distribution analysis
        dist_issues = analyze_distributions(df)
        report['issues'].extend(dist_issues['issues'])
        if dist_issues['visualization']:
            report['visualizations'].append(dist_issues['visualization'])
        
        # 6. Correlation warnings
        corr_issues = check_correlations(df)
        report['issues'].extend(corr_issues['issues'])
        
        # Calculate summary
        for issue in report['issues']:
            report['summary']['total_issues'] += 1
            
            # Increment severity count (handle 'info' vs 'infos')
            severity_key = issue['severity'] + 's' if issue['severity'] != 'info' else 'info'
            report['summary'][severity_key] += 1
            
            # Reduce score based on severity
            if issue['severity'] == 'error':
                report['overall_score'] -= 15
            elif issue['severity'] == 'warning':
                report['overall_score'] -= 5
        
        # Ensure score doesn't go below 0
        report['overall_score'] = max(0, report['overall_score'])
        
        # Generate overall recommendations
        if report['overall_score'] < 60:
            report['recommendations'].append('⚠️ Significant data quality issues detected. Review and address before analysis.')
        elif report['overall_score'] < 80:
            report['recommendations'].append('⚠️ Some data quality issues detected. Consider addressing them for better results.')
        else:
            report['recommendations'].append('✅ Data quality is good. Ready for analysis.')
        
        logger.info(f"Data quality analysis complete. Score: {report['overall_score']}/100")
        
    except Exception as e:
        logger.error(f"Error in data quality analysis: {e}")
        report['issues'].append({
            'severity': 'error',
            'category': 'system',
            'message': f'Error during quality analysis: {str(e)}'
        })
    
    return report


def analyze_missing_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze missing data patterns"""
    result = {
        'issues': [],
        'visualization': None
    }
    
    try:
        # Calculate missing values
        missing_counts = df.isnull().sum()
        missing_pct = (missing_counts / len(df)) * 100
        
        # Check each column
        for col in df.columns:
            if missing_counts[col] > 0:
                pct = missing_pct[col]
                count = int(missing_counts[col])
                
                if pct > 50:
                    result['issues'].append({
                        'severity': 'error',
                        'category': 'missing',
                        'column': col,
                        'message': f"Column '{col}' has {pct:.1f}% missing values ({count} rows)",
                        'count': count,
                        'percentage': float(pct),
                        'recommendation': 'Consider removing this column or collecting more data'
                    })
                elif pct > 20:
                    result['issues'].append({
                        'severity': 'warning',
                        'category': 'missing',
                        'column': col,
                        'message': f"Column '{col}' has {pct:.1f}% missing values ({count} rows)",
                        'count': count,
                        'percentage': float(pct),
                        'recommendation': 'Consider imputation or investigate missing pattern'
                    })
                elif pct > 5:
                    result['issues'].append({
                        'severity': 'info',
                        'category': 'missing',
                        'column': col,
                        'message': f"Column '{col}' has {pct:.1f}% missing values ({count} rows)",
                        'count': count,
                        'percentage': float(pct),
                        'recommendation': 'Minor missing data - imputation recommended'
                    })
        
        # Create visualization if there's missing data
        if missing_counts.sum() > 0:
            result['visualization'] = create_missing_data_viz(df, missing_pct)
    
    except Exception as e:
        logger.error(f"Error analyzing missing data: {e}")
    
    return result


def detect_outliers(df: pd.DataFrame) -> Dict[str, Any]:
    """Detect outliers using IQR method"""
    result = {
        'issues': [],
        'visualization': None
    }
    
    try:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        outlier_data = []
        for col in numeric_cols:
            data = df[col].dropna()
            if len(data) < 4:
                continue
            
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = data[(data < lower_bound) | (data > upper_bound)]
            n_outliers = len(outliers)
            
            if n_outliers > 0:
                pct = (n_outliers / len(data)) * 100
                outlier_data.append({
                    'column': col,
                    'count': n_outliers,
                    'percentage': pct
                })
                
                if pct > 10:
                    result['issues'].append({
                        'severity': 'warning',
                        'category': 'outliers',
                        'column': col,
                        'message': f"Column '{col}' has {n_outliers} outliers ({pct:.1f}%)",
                        'count': n_outliers,
                        'percentage': float(pct),
                        'recommendation': 'Review outliers - may indicate data quality issues or interesting cases'
                    })
                elif pct > 5:
                    result['issues'].append({
                        'severity': 'info',
                        'category': 'outliers',
                        'column': col,
                        'message': f"Column '{col}' has {n_outliers} outliers ({pct:.1f}%)",
                        'count': n_outliers,
                        'percentage': float(pct),
                        'recommendation': 'Minor outliers detected - consider reviewing'
                    })
        
        # Create visualization if outliers found
        if outlier_data:
            result['visualization'] = create_outlier_viz(df, outlier_data)
    
    except Exception as e:
        logger.error(f"Error detecting outliers: {e}")
    
    return result


def validate_data_types(df: pd.DataFrame) -> Dict[str, Any]:
    """Validate data types and suggest improvements"""
    result = {
        'issues': []
    }
    
    try:
        for col in df.columns:
            dtype = df[col].dtype
            
            # Check for numeric columns stored as object
            if dtype == 'object':
                # Try to convert to numeric
                try:
                    pd.to_numeric(df[col], errors='raise')
                    result['issues'].append({
                        'severity': 'warning',
                        'category': 'types',
                        'column': col,
                        'message': f"Column '{col}' appears numeric but stored as text",
                        'recommendation': 'Convert to numeric type for proper analysis'
                    })
                except:
                    # Check if it's a date
                    try:
                        pd.to_datetime(df[col], errors='raise')
                        result['issues'].append({
                            'severity': 'info',
                            'category': 'types',
                            'column': col,
                            'message': f"Column '{col}' appears to be a date stored as text",
                            'recommendation': 'Convert to datetime type if needed for time series analysis'
                        })
                    except:
                        pass
            
            # Check for categorical with many unique values
            if dtype == 'object':
                n_unique = df[col].nunique()
                if n_unique > len(df) * 0.5:
                    result['issues'].append({
                        'severity': 'info',
                        'category': 'types',
                        'column': col,
                        'message': f"Column '{col}' has {n_unique} unique values ({n_unique/len(df)*100:.1f}% of rows)",
                        'recommendation': 'High cardinality - may not be suitable for categorical analysis'
                    })
    
    except Exception as e:
        logger.error(f"Error validating data types: {e}")
    
    return result


def check_sample_size(df: pd.DataFrame) -> Dict[str, Any]:
    """Check if sample size is adequate"""
    result = {
        'issues': []
    }
    
    try:
        n = len(df)
        
        if n < 10:
            result['issues'].append({
                'severity': 'error',
                'category': 'sample_size',
                'message': f'Sample size too small (n={n}). Most statistical tests require n≥10',
                'recommendation': 'Collect more data before analysis'
            })
        elif n < 30:
            result['issues'].append({
                'severity': 'warning',
                'category': 'sample_size',
                'message': f'Small sample size (n={n}). Some tests may have low power',
                'recommendation': 'Consider non-parametric tests or collect more data'
            })
        elif n < 50:
            result['issues'].append({
                'severity': 'info',
                'category': 'sample_size',
                'message': f'Moderate sample size (n={n}). Adequate for basic tests',
                'recommendation': 'Sample size is acceptable for most common analyses'
            })
        else:
            result['issues'].append({
                'severity': 'info',
                'category': 'sample_size',
                'message': f'Good sample size (n={n})',
                'recommendation': 'Sample size is adequate for robust statistical analysis'
            })
    
    except Exception as e:
        logger.error(f"Error checking sample size: {e}")
    
    return result


def analyze_distributions(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze distributions of numeric variables"""
    result = {
        'issues': [],
        'visualization': None
    }
    
    try:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            data = df[col].dropna()
            if len(data) < 3:
                continue
            
            # Calculate skewness
            skewness = data.skew()
            if abs(skewness) > 2:
                result['issues'].append({
                    'severity': 'warning',
                    'category': 'distribution',
                    'column': col,
                    'message': f"Column '{col}' is highly skewed (skewness={skewness:.2f})",
                    'recommendation': 'Consider log or sqrt transformation for normality'
                })
            elif abs(skewness) > 1:
                result['issues'].append({
                    'severity': 'info',
                    'category': 'distribution',
                    'column': col,
                    'message': f"Column '{col}' is moderately skewed (skewness={skewness:.2f})",
                    'recommendation': 'May benefit from transformation if normality is required'
                })
    
    except Exception as e:
        logger.error(f"Error analyzing distributions: {e}")
    
    return result


def check_correlations(df: pd.DataFrame) -> Dict[str, Any]:
    """Check for problematic correlations"""
    result = {
        'issues': []
    }
    
    try:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            return result
        
        corr_matrix = df[numeric_cols].corr()
        
        # Check for perfect correlations (excluding diagonal)
        for i in range(len(corr_matrix)):
            for j in range(i+1, len(corr_matrix)):
                corr_val = abs(corr_matrix.iloc[i, j])
                col1 = corr_matrix.index[i]
                col2 = corr_matrix.columns[j]
                
                if corr_val > 0.99:
                    result['issues'].append({
                        'severity': 'error',
                        'category': 'correlation',
                        'column': f'{col1}, {col2}',
                        'message': f"Perfect correlation between '{col1}' and '{col2}' (r={corr_val:.3f})",
                        'recommendation': 'Remove one of these variables - they contain redundant information'
                    })
                elif corr_val > 0.9:
                    result['issues'].append({
                        'severity': 'warning',
                        'category': 'correlation',
                        'column': f'{col1}, {col2}',
                        'message': f"Very high correlation between '{col1}' and '{col2}' (r={corr_val:.3f})",
                        'recommendation': 'Consider removing one variable to avoid multicollinearity'
                    })
    
    except Exception as e:
        logger.error(f"Error checking correlations: {e}")
    
    return result


def create_missing_data_viz(df: pd.DataFrame, missing_pct: pd.Series) -> Dict[str, str]:
    """Create missing data visualization"""
    try:
        # Filter to columns with missing data
        missing_cols = missing_pct[missing_pct > 0].sort_values(ascending=False)
        
        if len(missing_cols) == 0:
            return None
        
        fig, ax = plt.subplots(figsize=(10, max(4, len(missing_cols) * 0.4)))
        missing_cols.plot(kind='barh', ax=ax, color='#ef4444')
        ax.set_xlabel('Missing Data (%)')
        ax.set_title('Missing Data by Column')
        ax.grid(axis='x', alpha=0.3)
        
        # Convert to base64
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        
        return {
            'title': 'Missing Data Analysis',
            'type': 'bar',
            'base64': img_base64,
            'description': f'{len(missing_cols)} columns have missing data'
        }
    
    except Exception as e:
        logger.error(f"Error creating missing data viz: {e}")
        return None


def create_outlier_viz(df: pd.DataFrame, outlier_data: List[Dict]) -> Dict[str, str]:
    """Create outlier visualization"""
    try:
        # Limit to top 6 columns with most outliers
        outlier_data_sorted = sorted(outlier_data, key=lambda x: x['percentage'], reverse=True)[:6]
        cols_to_plot = [item['column'] for item in outlier_data_sorted]
        
        fig, ax = plt.subplots(figsize=(10, max(4, len(cols_to_plot) * 0.8)))
        df[cols_to_plot].boxplot(ax=ax, vert=False)
        ax.set_xlabel('Value')
        ax.set_title('Outlier Detection (Box Plots)')
        ax.grid(axis='x', alpha=0.3)
        
        # Convert to base64
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        
        return {
            'title': 'Outlier Detection',
            'type': 'box',
            'base64': img_base64,
            'description': f'{len(outlier_data)} columns have outliers'
        }
    
    except Exception as e:
        logger.error(f"Error creating outlier viz: {e}")
        return None
