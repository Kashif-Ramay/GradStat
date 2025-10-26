"""
Statistical Test Advisor
Helps users select the appropriate statistical test based on their research question and data
"""

from typing import Dict, List, Any
import pandas as pd
from scipy import stats
from analysis_functions import convert_to_python_types


def recommend_test(answers: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Recommend statistical test(s) based on user answers
    
    Args:
        answers: Dictionary of user responses to wizard questions
        
    Returns:
        List of recommended tests with explanations
    """
    research_question = answers.get('researchQuestion')
    
    if research_question == 'compare_groups':
        return _recommend_for_group_comparison(answers)
    elif research_question == 'find_relationships':
        return _recommend_for_relationships(answers)
    elif research_question == 'predict_outcome':
        return _recommend_for_prediction(answers)
    elif research_question == 'describe_data':
        return [get_test_info('descriptive')]
    elif research_question == 'survival_analysis':
        return _recommend_for_survival(answers)
    elif research_question == 'reduce_dimensions':
        return _recommend_for_dimension_reduction(answers)
    elif research_question == 'find_groups':
        return _recommend_for_clustering(answers)
    else:
        return []


def _recommend_for_group_comparison(answers: Dict) -> List[Dict]:
    """Recommend tests for comparing groups"""
    n_groups = answers.get('nGroups')
    outcome_type = answers.get('outcomeType')
    is_normal = answers.get('isNormal')
    is_paired = answers.get('isPaired', False)
    
    recommendations = []
    
    # 2 groups, continuous outcome
    if n_groups == 2 and outcome_type == 'continuous':
        if is_paired:
            if is_normal or is_normal == 'not_sure':
                recommendations.append(get_test_info('paired_ttest', 'high'))
                recommendations.append(get_test_info('wilcoxon', 'medium'))
            else:
                recommendations.append(get_test_info('wilcoxon', 'high'))
        else:
            if is_normal or is_normal == 'not_sure':
                recommendations.append(get_test_info('independent_ttest', 'high'))
                recommendations.append(get_test_info('mann_whitney', 'medium'))
            else:
                recommendations.append(get_test_info('mann_whitney', 'high'))
    
    # 3+ groups, continuous outcome
    elif n_groups >= 3 and outcome_type == 'continuous':
        if is_normal or is_normal == 'not_sure':
            recommendations.append(get_test_info('anova', 'high'))
            recommendations.append(get_test_info('kruskal_wallis', 'medium'))
        else:
            recommendations.append(get_test_info('kruskal_wallis', 'high'))
    
    # Categorical outcome
    elif outcome_type == 'categorical':
        recommendations.append(get_test_info('chi_square', 'high'))
    
    return recommendations


def _recommend_for_relationships(answers: Dict) -> List[Dict]:
    """Recommend tests for finding relationships"""
    var1_type = answers.get('var1Type')
    var2_type = answers.get('var2Type')
    n_predictors = answers.get('nPredictors', 1)
    is_normal = answers.get('isNormal', True)
    relationship_type = answers.get('relationshipType', 'association')  # 'association' or 'prediction'
    
    recommendations = []
    
    # Both continuous
    if var1_type == 'continuous' and var2_type == 'continuous':
        # If user wants association/correlation (not prediction)
        if relationship_type == 'association' or n_predictors == 1:
            if is_normal:
                recommendations.append(get_test_info('pearson_correlation', 'high'))
                recommendations.append(get_test_info('spearman_correlation', 'medium'))
            else:
                recommendations.append(get_test_info('spearman_correlation', 'high'))
                recommendations.append(get_test_info('kendall_correlation', 'medium'))
                recommendations.append(get_test_info('pearson_correlation', 'low'))
        
        # Also offer regression for prediction
        if n_predictors == 1:
            recommendations.append(get_test_info('simple_regression', 'high'))
        else:
            recommendations.append(get_test_info('multiple_regression', 'high'))
    
    # One continuous, one categorical
    elif (var1_type == 'continuous' and var2_type == 'categorical') or \
         (var1_type == 'categorical' and var2_type == 'continuous'):
        recommendations.append(get_test_info('anova', 'high'))
    
    # Both categorical
    elif var1_type == 'categorical' and var2_type == 'categorical':
        recommendations.append(get_test_info('chi_square', 'high'))
        recommendations.append(get_test_info('fisher_exact', 'medium'))  # Alternative for small samples
    
    return recommendations


def _recommend_for_prediction(answers: Dict) -> List[Dict]:
    """Recommend tests for prediction"""
    outcome_type = answers.get('outcomeType')
    n_predictors = answers.get('nPredictors', 1)
    
    recommendations = []
    
    if outcome_type == 'continuous':
        if n_predictors == 1:
            recommendations.append(get_test_info('simple_regression', 'high'))
        else:
            recommendations.append(get_test_info('multiple_regression', 'high'))
    
    elif outcome_type == 'binary':
        recommendations.append(get_test_info('logistic_regression', 'high'))
    
    return recommendations


def _recommend_for_survival(answers: Dict) -> List[Dict]:
    """Recommend tests for survival analysis"""
    import logging
    logger = logging.getLogger(__name__)
    
    has_groups = answers.get('hasGroups', False)
    has_covariates = answers.get('hasCovariates', False)
    
    # Get detected column names from answers (passed from frontend)
    survival_data = answers.get('_survivalData', {})
    time_column = survival_data.get('time_column')
    event_column = survival_data.get('event_column')
    group_column = survival_data.get('group_column')
    covariate_columns = survival_data.get('covariate_columns', [])
    
    logger.info(f"Survival recommendation - survival_data: {survival_data}")
    logger.info(f"Detected columns - time: {time_column}, event: {event_column}, group: {group_column}")
    
    recommendations = [get_test_info('kaplan_meier', 'high')]
    
    # Fill in detected column names if available
    if recommendations and time_column and event_column:
        if 'gradstat_options' in recommendations[0]:
            recommendations[0]['gradstat_options']['durationColumn'] = time_column
            recommendations[0]['gradstat_options']['eventColumn'] = event_column
    
    if has_groups:
        test = get_test_info('logrank_test', 'high')
        if time_column and event_column and group_column:
            if 'gradstat_options' in test:
                test['gradstat_options']['durationColumn'] = time_column
                test['gradstat_options']['eventColumn'] = event_column
                test['gradstat_options']['groupColumn'] = group_column
        recommendations.append(test)
    
    if has_covariates:
        test = get_test_info('cox_regression', 'high')
        if time_column and event_column:
            if 'gradstat_options' in test:
                test['gradstat_options']['durationColumn'] = time_column
                test['gradstat_options']['eventColumn'] = event_column
                if covariate_columns:
                    test['gradstat_options']['covariates'] = covariate_columns
        recommendations.append(test)
    
    return recommendations


def _recommend_for_dimension_reduction(answers: Dict) -> List[Dict]:
    """Recommend tests for dimension reduction"""
    n_variables = answers.get('nVariables', 10)
    
    recommendations = []
    recommendations.append(get_test_info('pca', 'high'))
    
    return recommendations


def _recommend_for_clustering(answers: Dict) -> List[Dict]:
    """Recommend tests for finding groups"""
    n_expected_groups = answers.get('nExpectedGroups', 3)
    
    recommendations = []
    recommendations.append(get_test_info('clustering', 'high'))
    
    return recommendations


def get_test_info(test_key: str, confidence: str = 'high') -> Dict:
    """Get test information from library with sample size warning"""
    from test_library import TEST_LIBRARY
    test = TEST_LIBRARY.get(test_key, {}).copy()
    test['confidence'] = confidence
    
    # Add sample size warning if minimum is specified
    if 'sample_size_min' in test and test['sample_size_min'] > 1:
        test['sample_size_warning'] = f"⚠️ Minimum recommended sample size: {test['sample_size_min']}"
    
    return test


def auto_detect_from_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Automatically detect data characteristics and suggest tests
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary with data characteristics
    """
    characteristics = {
        'n_rows': len(df),
        'n_columns': len(df.columns),
        'column_types': {}
    }
    
    # Analyze each column
    for col in df.columns:
        col_info = {
            'name': col,
            'n_unique': int(df[col].nunique()),
            'has_missing': bool(df[col].isnull().any())
        }
        
        # Classify column type
        if df[col].dtype in ['int64', 'float64']:
            col_info['type'] = 'continuous'
            
            # Check normality if enough data
            if len(df[col].dropna()) >= 20:
                try:
                    _, p_value = stats.shapiro(df[col].dropna().sample(min(5000, len(df[col].dropna()))))
                    col_info['is_normal'] = bool(p_value > 0.05)
                except:
                    col_info['is_normal'] = None
                
        elif df[col].nunique() <= 10:
            col_info['type'] = 'categorical'
            col_info['is_binary'] = bool(df[col].nunique() == 2)
        else:
            col_info['type'] = 'text'
        
        characteristics['column_types'][col] = col_info
    
    return characteristics


def detect_variable_types(df: pd.DataFrame) -> Dict:
    """
    Detect variable types for Find Relationships question
    
    Returns:
        Dictionary with var1Type, var2Type, and details
    """
    numeric_cols = df.select_dtypes(include=['float64', 'int64', 'int32', 'float32']).columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    
    n_numeric = len(numeric_cols)
    n_categorical = len(categorical_cols)
    
    # Determine most likely variable combination
    if n_numeric >= 2:
        # Both continuous
        return {
            'var1Type': 'continuous',
            'var2Type': 'continuous',
            'confidence': 'high',
            'explanation': f'Found {n_numeric} numeric variables - likely continuous-continuous relationship',
            'details': {
                'numeric_columns': list(numeric_cols),
                'categorical_columns': list(categorical_cols)
            }
        }
    elif n_numeric >= 1 and n_categorical >= 1:
        # One continuous, one categorical
        return {
            'var1Type': 'continuous',
            'var2Type': 'categorical',
            'confidence': 'high',
            'explanation': f'Found {n_numeric} numeric and {n_categorical} categorical variables',
            'details': {
                'numeric_columns': list(numeric_cols),
                'categorical_columns': list(categorical_cols)
            }
        }
    elif n_categorical >= 2:
        # Both categorical
        return {
            'var1Type': 'categorical',
            'var2Type': 'categorical',
            'confidence': 'high',
            'explanation': f'Found {n_categorical} categorical variables',
            'details': {
                'numeric_columns': list(numeric_cols),
                'categorical_columns': list(categorical_cols)
            }
        }
    else:
        return {
            'var1Type': None,
            'var2Type': None,
            'confidence': 'low',
            'explanation': 'Unable to determine variable types',
            'details': {}
        }


def detect_num_predictors(df: pd.DataFrame) -> Dict:
    """
    Detect number of predictor variables
    
    Returns:
        Dictionary with nPredictors and details
    """
    numeric_cols = df.select_dtypes(include=['float64', 'int64', 'int32', 'float32']).columns
    
    # Exclude likely ID columns
    predictor_cols = [col for col in numeric_cols 
                     if not any(keyword in col.lower() 
                               for keyword in ['id', 'index', 'row', 'number'])]
    
    n_predictors = len(predictor_cols)
    
    if n_predictors <= 1:
        return {
            'nPredictors': 1,
            'confidence': 'medium',
            'explanation': f'Found {n_predictors} potential predictor variable(s)',
            'details': {'predictor_columns': list(predictor_cols)}
        }
    else:
        return {
            'nPredictors': 2,  # 2 means "multiple"
            'confidence': 'high',
            'explanation': f'Found {n_predictors} potential predictor variables',
            'details': {'predictor_columns': list(predictor_cols)}
        }


def analyze_dataset_comprehensive(df: pd.DataFrame) -> Dict:
    """
    Analyze entire dataset and answer ALL wizard questions at once
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary with all answers and confidence levels
    """
    results = {
        # Compare Groups questions
        'isNormal': None,
        'nGroups': None,
        'isPaired': None,
        'outcomeType': None,
        # Find Relationships questions
        'var1Type': None,
        'var2Type': None,
        # Predict Outcome & Find Relationships shared
        'nPredictors': None,
        'confidence': {},
        'details': {}
    }
    
    # 1. Test Normality (Compare Groups)
    try:
        normality_result = auto_detect_answer(df, 'isNormal')
        results['isNormal'] = normality_result.get('answer')
        results['confidence']['isNormal'] = normality_result.get('confidence')
        results['details']['isNormal'] = normality_result.get('details', {})
    except Exception as e:
        results['confidence']['isNormal'] = 'low'
        results['details']['isNormal'] = {'error': str(e)}
    
    # 2. Detect Number of Groups (Compare Groups)
    try:
        groups_result = auto_detect_answer(df, 'nGroups')
        results['nGroups'] = groups_result.get('answer')
        results['confidence']['nGroups'] = groups_result.get('confidence')
        results['details']['nGroups'] = groups_result.get('details', {})
    except Exception as e:
        results['confidence']['nGroups'] = 'low'
        results['details']['nGroups'] = {'error': str(e)}
    
    # 3. Detect Paired Structure (Compare Groups)
    try:
        paired_result = auto_detect_answer(df, 'isPaired')
        results['isPaired'] = paired_result.get('answer')
        results['confidence']['isPaired'] = paired_result.get('confidence')
        results['details']['isPaired'] = paired_result.get('details', {})
    except Exception as e:
        results['confidence']['isPaired'] = 'low'
        results['details']['isPaired'] = {'error': str(e)}
    
    # 4. Detect Outcome Type (Compare Groups & Predict Outcome)
    try:
        outcome_result = auto_detect_answer(df, 'outcomeType')
        results['outcomeType'] = outcome_result.get('answer')
        results['confidence']['outcomeType'] = outcome_result.get('confidence')
        results['details']['outcomeType'] = outcome_result.get('details', {})
    except Exception as e:
        results['confidence']['outcomeType'] = 'low'
        results['details']['outcomeType'] = {'error': str(e)}
    
    # 5. Detect Variable Types (Find Relationships)
    try:
        var_types_result = detect_variable_types(df)
        results['var1Type'] = var_types_result.get('var1Type')
        results['var2Type'] = var_types_result.get('var2Type')
        results['confidence']['varTypes'] = var_types_result.get('confidence')
        results['details']['varTypes'] = var_types_result.get('details', {})
    except Exception as e:
        results['confidence']['varTypes'] = 'low'
        results['details']['varTypes'] = {'error': str(e)}
    
    # 6. Detect Number of Predictors (Find Relationships & Predict Outcome)
    try:
        predictors_result = detect_num_predictors(df)
        results['nPredictors'] = predictors_result.get('nPredictors')
        results['confidence']['nPredictors'] = predictors_result.get('confidence')
        results['details']['nPredictors'] = predictors_result.get('details', {})
    except Exception as e:
        results['confidence']['nPredictors'] = 'low'
        results['details']['nPredictors'] = {'error': str(e)}
    
    # 7. Detect Survival Analysis Options
    try:
        survival_result = detect_time_event_columns(df)
        results['survival'] = survival_result
        # Add individual confidence levels
        results['confidence']['hasGroups_survival'] = survival_result['confidence'].get('has_groups', 'low')
        results['confidence']['hasCovariates'] = survival_result['confidence'].get('has_covariates', 'low')
        results['details']['survival'] = survival_result.get('details', {})
    except Exception as e:
        results['confidence']['hasGroups_survival'] = 'low'
        results['confidence']['hasCovariates'] = 'low'
        results['details']['survival'] = {'error': str(e)}
    
    # 8. Detect PCA Options
    try:
        pca_result = detect_pca_options(df)
        results['pca'] = pca_result
        results['confidence']['nComponents'] = pca_result['confidence'].get('n_components', 'low')
        results['confidence']['scaling_pca'] = pca_result['confidence'].get('scaling', 'low')
        results['details']['pca'] = pca_result.get('details', {})
    except Exception as e:
        results['confidence']['nComponents'] = 'low'
        results['confidence']['scaling_pca'] = 'low'
        results['details']['pca'] = {'error': str(e)}
    
    # 9. Detect Clustering Options
    try:
        clustering_result = detect_clustering_options(df)
        results['clustering'] = clustering_result
        results['confidence']['nClusters'] = clustering_result['confidence'].get('n_clusters', 'low')
        results['confidence']['algorithm'] = clustering_result['confidence'].get('algorithm', 'low')
        results['details']['clustering'] = clustering_result.get('details', {})
    except Exception as e:
        results['confidence']['nClusters'] = 'low'
        results['confidence']['algorithm'] = 'low'
        results['details']['clustering'] = {'error': str(e)}
    
    # Generate overall summary
    high_confidence_count = sum(1 for c in results['confidence'].values() if c == 'high')
    total_questions = len(results['confidence'])
    
    results['summary'] = {
        'total_questions': total_questions,
        'high_confidence': high_confidence_count,
        'confidence_rate': f"{(high_confidence_count/total_questions)*100:.0f}%",
        'recommendation': 'Review low-confidence answers' if high_confidence_count < total_questions else 'All answers have high confidence'
    }
    
    return results


def auto_detect_answer(df: pd.DataFrame, question_key: str) -> Dict[str, Any]:
    """
    Auto-detect answer to a specific wizard question
    
    Args:
        df: DataFrame to analyze
        question_key: The question to answer (e.g., 'isNormal', 'nGroups')
        
    Returns:
        Dictionary with answer, confidence, and explanation
    """
    
    if question_key == 'isNormal':
        # Log DataFrame info for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"DataFrame shape: {df.shape}")
        logger.info(f"DataFrame columns: {list(df.columns)}")
        logger.info(f"DataFrame dtypes: {df.dtypes.to_dict()}")
        
        # Test normality on numeric columns
        numeric_cols = df.select_dtypes(include=['float64', 'int64', 'int32', 'float32']).columns
        logger.info(f"Numeric columns found: {list(numeric_cols)}")
        
        if len(numeric_cols) == 0:
            # Try to get all column types for debugging
            col_types = {col: str(df[col].dtype) for col in df.columns}
            return {
                'answer': None,
                'confidence': 'low',
                'explanation': f'No numeric columns found in your data. Column types detected: {col_types}',
                'details': {'column_types': col_types, 'shape': df.shape}
            }
        
        normality_results = {}
        for col in numeric_cols:
            clean_data = df[col].dropna()
            if len(clean_data) >= 3:  # Minimum 3 observations for Shapiro-Wilk
                try:
                    _, p_value = stats.shapiro(clean_data.sample(min(5000, len(clean_data))))
                    normality_results[col] = {
                        'is_normal': bool(p_value > 0.05),
                        'p_value': float(p_value),
                        'test': 'Shapiro-Wilk',
                        'n': len(clean_data)
                    }
                except Exception as e:
                    normality_results[col] = {
                        'is_normal': None,
                        'error': str(e),
                        'n': len(clean_data)
                    }
            else:
                normality_results[col] = {
                    'is_normal': None,
                    'error': f'Insufficient data: only {len(clean_data)} observations',
                    'n': len(clean_data)
                }
        
        # Determine overall answer
        valid_results = [r for r in normality_results.values() if 'is_normal' in r and r['is_normal'] is not None]
        if not valid_results:
            # Return detailed error info
            error_summary = []
            for col, result in normality_results.items():
                if 'error' in result:
                    error_summary.append(f"{col}: {result['error']}")
            
            return {
                'answer': None,
                'confidence': 'low',
                'explanation': f'Unable to test normality (insufficient data or errors). {"; ".join(error_summary) if error_summary else "No valid results."}',
                'details': normality_results
            }
        
        normal_count = sum(1 for r in valid_results if r['is_normal'])
        total_count = len(valid_results)
        normal_pct = (normal_count / total_count) * 100
        
        if normal_pct >= 70:
            answer = True
            confidence = 'high' if normal_pct >= 80 else 'medium'
            explanation = f"✅ {normal_count}/{total_count} variables ({normal_pct:.0f}%) are normally distributed (Shapiro-Wilk test, p > 0.05). Your data appears normal."
        elif normal_pct <= 30:
            answer = False
            confidence = 'high' if normal_pct <= 20 else 'medium'
            explanation = f"❌ Only {normal_count}/{total_count} variables ({normal_pct:.0f}%) are normally distributed. Consider non-parametric tests."
        else:
            answer = False
            confidence = 'medium'
            explanation = f"⚠️ Mixed results: {normal_count}/{total_count} variables ({normal_pct:.0f}%) are normal. Consider non-parametric tests to be safe."
        
        return {
            'answer': answer,
            'confidence': confidence,
            'explanation': explanation,
            'details': normality_results
        }
    
    elif question_key == 'nGroups':
        # Detect number of groups from categorical columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        
        if len(categorical_cols) == 0:
            # Default to 2 groups if no categorical columns found
            return {
                'answer': 2,
                'confidence': 'low',
                'explanation': 'No categorical columns found. Defaulting to 2 groups - please verify this is correct for your analysis.',
                'details': {'categorical_columns': [], 'note': 'No groups detected, using default'}
            }
        
        # Use the categorical column with most reasonable number of groups (2-10)
        group_counts = {}
        for col in categorical_cols:
            n_unique = df[col].nunique()
            if 2 <= n_unique <= 10:
                group_counts[col] = n_unique
        
        if not group_counts:
            return {
                'answer': None,
                'confidence': 'low',
                'explanation': 'No suitable grouping variable found (need 2-10 groups).',
                'details': {}
            }
        
        # Use the first suitable column
        best_col = list(group_counts.keys())[0]
        n_groups = group_counts[best_col]
        
        return {
            'answer': n_groups,
            'confidence': 'high',
            'explanation': f"✅ Detected {n_groups} groups in column '{best_col}'",
            'details': {
                'column': best_col,
                'groups': df[best_col].unique().tolist()
            }
        }
    
    elif question_key == 'isPaired':
        try:
            # Check for paired data structure
            has_id_column = any('id' in col.lower() or 'subject' in col.lower() or 'patient' in col.lower() 
                               for col in df.columns)
            has_time_column = any('time' in col.lower() or 'visit' in col.lower() or 'period' in col.lower() 
                                 or 'pre' in col.lower() or 'post' in col.lower()
                                 for col in df.columns)
            
            # Check if we have duplicate IDs (indicating repeated measures)
            id_cols = [col for col in df.columns if 'id' in col.lower() or 'subject' in col.lower()]
            has_duplicates = False
            if id_cols:
                has_duplicates = bool(df[id_cols[0]].duplicated().any())
            
            if has_id_column and (has_time_column or has_duplicates):
                return {
                    'answer': True,
                    'confidence': 'medium',
                    'explanation': "⚠️ Detected ID and time/repeated columns - data appears to be paired or repeated measures",
                    'details': {
                        'has_id': has_id_column,
                        'has_time': has_time_column,
                        'has_duplicates': has_duplicates
                    }
                }
            else:
                return {
                    'answer': False,
                    'confidence': 'medium',
                    'explanation': "✅ No clear paired structure detected - assuming independent groups",
                    'details': {
                        'has_id': has_id_column,
                        'has_time': has_time_column
                    }
                }
        except Exception as e:
            return {
                'answer': None,
                'confidence': 'low',
                'explanation': f'Error detecting paired structure: {str(e)}',
                'details': {}
            }
    
    elif question_key == 'outcomeType':
        # Detect outcome variable type
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        
        # Look for likely outcome variables (usually last column or contains certain keywords)
        outcome_keywords = ['outcome', 'result', 'score', 'value', 'target', 'y', 'dependent']
        
        likely_outcome = None
        for col in df.columns:
            if any(keyword in col.lower() for keyword in outcome_keywords):
                likely_outcome = col
                break
        
        if not likely_outcome:
            likely_outcome = df.columns[-1]  # Default to last column
        
        if likely_outcome in numeric_cols:
            return {
                'answer': 'continuous',
                'confidence': 'high',
                'explanation': f"✅ Detected continuous outcome variable: '{likely_outcome}'",
                'details': {'column': likely_outcome, 'type': 'continuous'}
            }
        elif likely_outcome in categorical_cols:
            n_unique = df[likely_outcome].nunique()
            if n_unique == 2:
                return {
                    'answer': 'binary',
                    'confidence': 'high',
                    'explanation': f"✅ Detected binary outcome variable: '{likely_outcome}' (2 categories)",
                    'details': {'column': likely_outcome, 'type': 'binary', 'categories': df[likely_outcome].unique().tolist()}
                }
            else:
                return {
                    'answer': 'categorical',
                    'confidence': 'high',
                    'explanation': f"✅ Detected categorical outcome variable: '{likely_outcome}' ({n_unique} categories)",
                    'details': {'column': likely_outcome, 'type': 'categorical', 'n_categories': n_unique}
                }
    
    # Default response for unknown questions
    return {
        'answer': None,
        'confidence': 'low',
        'explanation': f"Unable to auto-detect answer for question: {question_key}",
        'details': {}
    }


def detect_time_event_columns(df: pd.DataFrame) -> Dict:
    """
    Detect time-to-event and censoring columns for survival analysis
    
    Returns:
        Dictionary with detected columns and confidence levels
    """
    import logging
    logger = logging.getLogger(__name__)
    
    result = {
        'time_column': None,
        'event_column': None,
        'has_groups': False,
        'group_column': None,
        'has_covariates': False,
        'covariate_columns': [],
        'confidence': {
            'time_column': 'low',
            'event_column': 'low',
            'has_groups': 'low',
            'has_covariates': 'low'
        },
        'details': {}
    }
    
    try:
        # Detect time column (numeric, likely named with time-related keywords)
        time_keywords = ['time', 'duration', 'days', 'months', 'years', 'survival', 'followup', 'follow_up']
        numeric_cols = df.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns
        
        time_candidates = []
        for col in numeric_cols:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in time_keywords):
                time_candidates.append((col, 'high'))
            elif df[col].min() >= 0 and df[col].max() > 0:  # Positive values
                time_candidates.append((col, 'medium'))
        
        if time_candidates:
            # Prefer high confidence matches
            time_candidates.sort(key=lambda x: (x[1] == 'high', df[x[0]].mean()), reverse=True)
            result['time_column'] = time_candidates[0][0]
            result['confidence']['time_column'] = time_candidates[0][1]
            result['details']['time_column_candidates'] = [c[0] for c in time_candidates]
        
        # Detect event column (binary, likely named with event-related keywords)
        event_keywords = ['event', 'status', 'censored', 'death', 'died', 'outcome', 'occurred']
        
        event_candidates = []
        for col in df.columns:
            col_lower = col.lower()
            n_unique = df[col].nunique()
            
            # Binary column (0/1 or True/False)
            if n_unique == 2:
                unique_vals = sorted(df[col].unique())
                # Check if it's 0/1 or boolean
                if (set(unique_vals) == {0, 1} or 
                    set(unique_vals) == {False, True} or
                    set(unique_vals) == {'0', '1'}):
                    
                    if any(keyword in col_lower for keyword in event_keywords):
                        event_candidates.append((col, 'high'))
                    else:
                        event_candidates.append((col, 'medium'))
        
        if event_candidates:
            event_candidates.sort(key=lambda x: x[1] == 'high', reverse=True)
            result['event_column'] = event_candidates[0][0]
            result['confidence']['event_column'] = event_candidates[0][1]
            result['details']['event_column_candidates'] = [c[0] for c in event_candidates]
            
            # Calculate censoring percentage
            event_col = result['event_column']
            censored_count = (df[event_col] == 0).sum()
            total_count = len(df)
            censoring_pct = (censored_count / total_count) * 100
            result['details']['censoring_pct'] = float(censoring_pct)
        
        # Detect group columns (categorical with 2-5 unique values)
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        
        group_candidates = []
        for col in categorical_cols:
            n_unique = df[col].nunique()
            if 2 <= n_unique <= 5:
                group_candidates.append(col)
        
        if group_candidates:
            result['has_groups'] = True
            result['group_column'] = group_candidates[0]  # Take first one
            result['confidence']['has_groups'] = 'high' if len(group_candidates) == 1 else 'medium'
            result['details']['group_column_candidates'] = group_candidates
        else:
            result['has_groups'] = False
            result['confidence']['has_groups'] = 'medium'
        
        # Detect covariates (numeric columns excluding time column)
        covariate_cols = [col for col in numeric_cols 
                         if col != result['time_column'] and col != result['event_column']]
        
        if len(covariate_cols) > 0:
            result['has_covariates'] = True
            result['covariate_columns'] = list(covariate_cols)
            result['confidence']['has_covariates'] = 'high'
        else:
            result['has_covariates'] = False
            result['confidence']['has_covariates'] = 'high'
        
        result['details']['n_covariates'] = len(covariate_cols)
        
        logger.info(f"Survival analysis detection: time={result['time_column']}, event={result['event_column']}, groups={result['has_groups']}")
        
    except Exception as e:
        logger.error(f"Error detecting survival columns: {e}")
        result['details']['error'] = str(e)
    
    # Convert numpy types to Python types for JSON serialization
    return convert_to_python_types(result)


def detect_pca_options(df: pd.DataFrame) -> Dict:
    """
    Detect optimal PCA settings
    
    Returns:
        Dictionary with suggested PCA options
    """
    import numpy as np
    import logging
    logger = logging.getLogger(__name__)
    
    result = {
        'n_numeric_vars': 0,
        'suggested_components': None,
        'scaling_needed': False,
        'correlation_strength': 'low',
        'confidence': {
            'n_components': 'low',
            'scaling': 'low'
        },
        'details': {}
    }
    
    try:
        # Get numeric columns
        numeric_cols = df.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns
        n_vars = len(numeric_cols)
        result['n_numeric_vars'] = n_vars
        
        if n_vars < 3:
            result['details']['warning'] = 'Need at least 3 numeric variables for PCA'
            return result
        
        # Suggest number of components (rule of thumb: sqrt or 80% variance)
        suggested_k = max(2, min(int(np.sqrt(n_vars)), n_vars // 2))
        result['suggested_components'] = suggested_k
        result['confidence']['n_components'] = 'high' if n_vars >= 5 else 'medium'
        
        # Check if scaling is needed (variance ratio > 10)
        numeric_data = df[numeric_cols].dropna()
        if len(numeric_data) > 0:
            variances = numeric_data.var()
            max_var = variances.max()
            min_var = variances.min()
            
            if min_var > 0:
                variance_ratio = max_var / min_var
                result['scaling_needed'] = variance_ratio > 10
                result['confidence']['scaling'] = 'high'
                result['details']['variance_ratio'] = float(variance_ratio)
            
            # Calculate correlation strength
            corr_matrix = numeric_data.corr()
            # Get upper triangle (excluding diagonal)
            upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
            avg_corr = abs(upper_tri.stack()).mean()
            
            if avg_corr > 0.5:
                result['correlation_strength'] = 'high'
            elif avg_corr > 0.3:
                result['correlation_strength'] = 'medium'
            else:
                result['correlation_strength'] = 'low'
            
            result['details']['avg_correlation'] = float(avg_corr)
        
        logger.info(f"PCA detection: {n_vars} vars, suggest {suggested_k} components, scaling={result['scaling_needed']}")
        
    except Exception as e:
        logger.error(f"Error detecting PCA options: {e}")
        result['details']['error'] = str(e)
    
    # Convert numpy types to Python types for JSON serialization
    return convert_to_python_types(result)


def detect_clustering_options(df: pd.DataFrame) -> Dict:
    """
    Detect optimal clustering settings
    
    Returns:
        Dictionary with suggested clustering options
    """
    import numpy as np
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    import logging
    logger = logging.getLogger(__name__)
    
    result = {
        'n_numeric_vars': 0,
        'suggested_k': None,
        'suggested_algorithm': 'kmeans',
        'scaling_needed': False,
        'has_outliers': False,
        'confidence': {
            'n_clusters': 'low',
            'algorithm': 'medium'
        },
        'details': {}
    }
    
    try:
        # Get numeric columns
        numeric_cols = df.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns
        n_vars = len(numeric_cols)
        result['n_numeric_vars'] = n_vars
        
        if n_vars < 2:
            result['details']['warning'] = 'Need at least 2 numeric variables for clustering'
            return result
        
        # Prepare data
        numeric_data = df[numeric_cols].dropna()
        if len(numeric_data) < 10:
            result['details']['warning'] = 'Need at least 10 observations for clustering'
            return result
        
        # Check scaling needed
        variances = numeric_data.var()
        max_var = variances.max()
        min_var = variances.min()
        if min_var > 0:
            variance_ratio = max_var / min_var
            result['scaling_needed'] = variance_ratio > 10
            result['details']['variance_ratio'] = float(variance_ratio)
        
        # Scale data for analysis
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(numeric_data)
        
        # Detect outliers using IQR method
        Q1 = np.percentile(scaled_data, 25, axis=0)
        Q3 = np.percentile(scaled_data, 75, axis=0)
        IQR = Q3 - Q1
        outlier_mask = np.any((scaled_data < (Q1 - 1.5 * IQR)) | (scaled_data > (Q3 + 1.5 * IQR)), axis=1)
        outlier_pct = (outlier_mask.sum() / len(scaled_data)) * 100
        result['has_outliers'] = outlier_pct > 5
        result['details']['outlier_pct'] = float(outlier_pct)
        
        # Suggest algorithm
        n_samples = len(numeric_data)
        if result['has_outliers']:
            result['suggested_algorithm'] = 'dbscan'
            result['confidence']['algorithm'] = 'medium'
        elif n_samples < 1000:
            result['suggested_algorithm'] = 'hierarchical'
            result['confidence']['algorithm'] = 'medium'
        else:
            result['suggested_algorithm'] = 'kmeans'
            result['confidence']['algorithm'] = 'high'
        
        # Suggest k using elbow method (quick version)
        if result['suggested_algorithm'] in ['kmeans', 'hierarchical']:
            inertias = []
            k_range = range(2, min(11, n_samples // 10))
            
            for k in k_range:
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                kmeans.fit(scaled_data)
                inertias.append(kmeans.inertia_)
            
            # Find elbow (simple method: max second derivative)
            if len(inertias) >= 3:
                second_derivatives = []
                for i in range(1, len(inertias) - 1):
                    second_deriv = inertias[i-1] - 2*inertias[i] + inertias[i+1]
                    second_derivatives.append(second_deriv)
                
                elbow_idx = np.argmax(second_derivatives) + 1
                result['suggested_k'] = list(k_range)[elbow_idx]
                result['confidence']['n_clusters'] = 'medium'
            else:
                result['suggested_k'] = 3  # Default
                result['confidence']['n_clusters'] = 'low'
        else:
            # DBSCAN doesn't need k
            result['suggested_k'] = None
            result['confidence']['n_clusters'] = 'high'
        
        logger.info(f"Clustering detection: {n_vars} vars, suggest k={result['suggested_k']}, algorithm={result['suggested_algorithm']}")
        
    except Exception as e:
        logger.error(f"Error detecting clustering options: {e}")
        result['details']['error'] = str(e)
    
    # Convert numpy types to Python types for JSON serialization
    return convert_to_python_types(result)
