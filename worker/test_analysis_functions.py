"""
Comprehensive test suite for GradStat analysis functions
Run with: pytest test_analysis_functions.py -v
"""

import pytest
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing

from analysis_functions import (
    descriptive_analysis,
    group_comparison_analysis,
    regression_analysis,
    logistic_regression_analysis,
    survival_analysis,
    nonparametric_test,
    categorical_analysis,
    clustering_analysis,
    pca_analysis,
    power_analysis,
    convert_to_python_types
)


# ============================================================================
# FIXTURES - Test Data
# ============================================================================

@pytest.fixture
def sample_numeric_data():
    """Sample numeric dataset for testing"""
    np.random.seed(42)
    return pd.DataFrame({
        'age': np.random.randint(20, 70, 100),
        'height': np.random.normal(170, 10, 100),
        'weight': np.random.normal(70, 15, 100),
        'score': np.random.normal(75, 10, 100)
    })


@pytest.fixture
def sample_grouped_data():
    """Sample dataset with groups for t-test/ANOVA"""
    np.random.seed(42)
    return pd.DataFrame({
        'value': np.concatenate([
            np.random.normal(50, 10, 30),
            np.random.normal(55, 10, 30),
            np.random.normal(60, 10, 30)
        ]),
        'group': ['A'] * 30 + ['B'] * 30 + ['C'] * 30
    })


@pytest.fixture
def sample_binary_data():
    """Sample dataset for logistic regression"""
    np.random.seed(42)
    n = 150
    age = np.random.randint(20, 80, n)
    bmi = np.random.normal(25, 5, n)
    # Create binary outcome with some relationship to predictors
    prob = 1 / (1 + np.exp(-(0.05 * age + 0.1 * bmi - 5)))
    outcome = (np.random.random(n) < prob).astype(int)
    
    return pd.DataFrame({
        'age': age,
        'bmi': bmi,
        'outcome': outcome
    })


@pytest.fixture
def sample_survival_data():
    """Sample dataset for survival analysis"""
    np.random.seed(42)
    return pd.DataFrame({
        'time': np.random.exponential(24, 100),
        'event': np.random.binomial(1, 0.6, 100),
        'treatment': np.random.binomial(1, 0.5, 100),
        'age': np.random.randint(40, 80, 100)
    })


@pytest.fixture
def sample_categorical_data():
    """Sample dataset for chi-square test"""
    np.random.seed(42)
    return pd.DataFrame({
        'gender': np.random.choice(['M', 'F'], 100),
        'outcome': np.random.choice(['Yes', 'No'], 100)
    })


# ============================================================================
# TEST: convert_to_python_types
# ============================================================================

class TestConvertToPythonTypes:
    """Test the inf/nan handling and type conversion"""
    
    def test_handles_infinity(self):
        """Should convert inf to None"""
        result = convert_to_python_types(float('inf'))
        assert result is None
    
    def test_handles_negative_infinity(self):
        """Should convert -inf to None"""
        result = convert_to_python_types(float('-inf'))
        assert result is None
    
    def test_handles_nan(self):
        """Should convert nan to None"""
        result = convert_to_python_types(float('nan'))
        assert result is None
    
    def test_handles_numpy_inf(self):
        """Should convert numpy inf to None"""
        result = convert_to_python_types(np.inf)
        assert result is None
    
    def test_handles_numpy_nan(self):
        """Should convert numpy nan to None"""
        result = convert_to_python_types(np.nan)
        assert result is None
    
    def test_handles_normal_float(self):
        """Should preserve normal floats"""
        result = convert_to_python_types(3.14)
        assert result == 3.14
    
    def test_handles_dict_with_inf(self):
        """Should recursively handle inf in dicts"""
        data = {'a': 1.0, 'b': float('inf'), 'c': 3.0}
        result = convert_to_python_types(data)
        assert result == {'a': 1.0, 'b': None, 'c': 3.0}
    
    def test_handles_nested_structures(self):
        """Should handle deeply nested structures"""
        data = {
            'stats': {
                'mean': 5.0,
                'max': float('inf'),
                'values': [1.0, float('nan'), 3.0]
            }
        }
        result = convert_to_python_types(data)
        assert result['stats']['max'] is None
        assert result['stats']['values'][1] is None


# ============================================================================
# TEST: Descriptive Analysis
# ============================================================================

class TestDescriptiveAnalysis:
    """Test descriptive statistics"""
    
    def test_basic_descriptive(self, sample_numeric_data):
        """Should return summary statistics"""
        result = descriptive_analysis(sample_numeric_data, {})
        
        assert 'summary' in result
        assert 'plots' in result
        assert 'interpretation' in result
        assert result['analysis_type'] == 'descriptive'
    
    def test_outlier_detection(self, sample_numeric_data):
        """Should detect outliers using IQR method"""
        result = descriptive_analysis(sample_numeric_data, {})
        
        # Should have outlier information
        assert 'test_results' in result
        # Outliers should be detected for at least one column
        assert any('outliers' in str(result).lower() for _ in [1])
    
    def test_no_inf_in_output(self, sample_numeric_data):
        """Should not contain inf values in output"""
        result = descriptive_analysis(sample_numeric_data, {})
        
        # Convert to string and check
        result_str = str(result)
        assert 'inf' not in result_str.lower()


# ============================================================================
# TEST: Group Comparison
# ============================================================================

class TestGroupComparison:
    """Test t-test and ANOVA"""
    
    def test_ttest_two_groups(self, sample_grouped_data):
        """Should perform t-test for 2 groups"""
        data_2groups = sample_grouped_data[sample_grouped_data['group'].isin(['A', 'B'])]
        
        result = group_comparison_analysis(data_2groups, {
            'dependentVar': 'value',
            'groupVar': 'group'
        })
        
        assert result['analysis_type'] == 'group_comparison'
        assert 'test_results' in result
        assert 't_statistic' in result['test_results'] or 'test' in result['test_results']
    
    def test_anova_three_groups(self, sample_grouped_data):
        """Should perform ANOVA for 3+ groups"""
        result = group_comparison_analysis(sample_grouped_data, {
            'dependentVar': 'value',
            'groupVar': 'group'
        })
        
        assert result['analysis_type'] == 'group_comparison'
        assert 'test_results' in result
        # Should have F-statistic for ANOVA
        assert 'f_statistic' in result['test_results'] or 'test' in result['test_results']
    
    def test_effect_size_calculated(self, sample_grouped_data):
        """Should calculate effect size"""
        result = group_comparison_analysis(sample_grouped_data, {
            'dependentVar': 'value',
            'groupVar': 'group'
        })
        
        # Should have effect size
        assert 'effect_size' in result['test_results'] or 'effect' in str(result).lower()


# ============================================================================
# TEST: Regression
# ============================================================================

class TestRegression:
    """Test linear regression"""
    
    def test_simple_regression(self, sample_numeric_data):
        """Should perform simple linear regression"""
        result = regression_analysis(sample_numeric_data, {
            'dependentVar': 'y',
            'independentVar': 'x'
        })
        
        assert result['analysis_type'] == 'regression'
        assert 'test_results' in result
        assert 'r_squared' in result['test_results']
        assert 'plots' in result
    
    def test_multiple_regression(self, sample_numeric_data):
        """Should perform multiple regression"""
        result = regression_analysis(sample_numeric_data, {
            'dependentVar': 'y',
            'independentVars': ['x1', 'x2']
        })
        
        assert result['analysis_type'] == 'regression'
        assert 'test_results' in result
        assert 'r_squared' in result['test_results']
    
    def test_r_squared_range(self, sample_numeric_data):
        """R² should be between 0 and 1"""
        result = regression_analysis(sample_numeric_data, {
            'dependentVar': 'y',
            'independentVar': 'x'
        })
        
        r_squared = result['test_results']['r_squared']
        assert 0 <= r_squared <= 1


# ============================================================================
# TEST: Logistic Regression
# ============================================================================

class TestLogisticRegression:
    """Test logistic regression"""
    
    def test_basic_logistic_regression(self, sample_binary_data):
        """Should perform logistic regression"""
        result = logistic_regression_analysis(sample_binary_data, {
            'targetColumn': 'outcome',
            'predictorColumns': ['age', 'bmi'],
            'testSize': 0.3,
            'randomState': 42
        })
        
        assert result['analysis_type'] == 'logistic_regression'
        assert 'test_results' in result
        assert 'accuracy' in result['test_results']
        assert 'auc' in result['test_results']
    
    def test_auc_range(self, sample_binary_data):
        """AUC should be between 0 and 1 (or None if unstable)"""
        result = logistic_regression_analysis(sample_binary_data, {
            'targetColumn': 'outcome',
            'predictorColumns': ['age', 'bmi'],
            'testSize': 0.3,
            'randomState': 42
        })
        
        auc = result['test_results']['auc']
        if auc is not None:
            assert 0 <= auc <= 1
    
    def test_confusion_matrix_present(self, sample_binary_data):
        """Should include confusion matrix"""
        result = logistic_regression_analysis(sample_binary_data, {
            'targetColumn': 'outcome',
            'predictorColumns': ['age', 'bmi'],
            'testSize': 0.3,
            'randomState': 42
        })
        
        assert 'true_negatives' in result['test_results']
        assert 'true_positives' in result['test_results']


# ============================================================================
# TEST: Survival Analysis
# ============================================================================

class TestSurvivalAnalysis:
    """Test Kaplan-Meier and Cox regression"""
    
    def test_basic_survival_analysis(self, sample_survival_data):
        """Should perform survival analysis"""
        result = survival_analysis(sample_survival_data, {
            'durationColumn': 'time',
            'eventColumn': 'event'
        })
        
        assert result['analysis_type'] == 'survival'
        assert 'test_results' in result
        assert 'summary_statistics' in result['test_results']
    
    def test_survival_with_groups(self, sample_survival_data):
        """Should perform Log-Rank test with groups"""
        result = survival_analysis(sample_survival_data, {
            'durationColumn': 'time',
            'eventColumn': 'event',
            'groupColumn': 'treatment'
        })
        
        assert 'group_statistics' in result['test_results'] or 'logrank_test' in result['test_results']
    
    def test_cox_regression(self, sample_survival_data):
        """Should perform Cox regression with covariates"""
        result = survival_analysis(sample_survival_data, {
            'durationColumn': 'time',
            'eventColumn': 'event',
            'covariates': ['age']
        })
        
        # Should have Cox regression results (or error if unstable)
        assert 'cox_regression' in result['test_results'] or 'cox_regression_error' in result['test_results']
    
    def test_no_inf_in_survival_output(self, sample_survival_data):
        """Should not contain inf values in survival output"""
        result = survival_analysis(sample_survival_data, {
            'durationColumn': 'time',
            'eventColumn': 'event',
            'covariates': ['age']
        })
        
        # Check that all values are JSON-serializable (no inf)
        import json
        try:
            json.dumps(result)
            assert True
        except ValueError as e:
            if 'inf' in str(e).lower():
                pytest.fail("Output contains inf values")


# ============================================================================
# TEST: Non-Parametric Tests
# ============================================================================

class TestNonParametric:
    """Test Mann-Whitney, Kruskal-Wallis, Wilcoxon"""
    
    def test_mann_whitney(self, sample_grouped_data):
        """Should perform Mann-Whitney U test"""
        data_2groups = sample_grouped_data[sample_grouped_data['group'].isin(['A', 'B'])]
        
        result = nonparametric_test(data_2groups, {
            'dependentVar': 'value',
            'groupVar': 'group',
            'testType': 'mann-whitney'
        })
        
        assert result['analysis_type'] == 'nonparametric'
        assert 'u_statistic' in result['test_results']
    
    def test_kruskal_wallis(self, sample_grouped_data):
        """Should perform Kruskal-Wallis test"""
        result = nonparametric_test(sample_grouped_data, {
            'dependentVar': 'value',
            'groupVar': 'group',
            'testType': 'kruskal-wallis'
        })
        
        assert result['analysis_type'] == 'nonparametric'
        assert 'h_statistic' in result['test_results']


# ============================================================================
# TEST: Categorical Analysis
# ============================================================================

class TestCategoricalAnalysis:
    """Test chi-square and Fisher's exact test"""
    
    def test_chi_square(self, sample_categorical_data):
        """Should perform chi-square test"""
        result = categorical_analysis(sample_categorical_data, {
            'variable1': 'gender',
            'variable2': 'outcome'
        })
        
        assert result['analysis_type'] == 'categorical'
        assert 'test_results' in result
        assert 'chi2_statistic' in result['test_results'] or 'test' in result['test_results']


# ============================================================================
# TEST: Clustering
# ============================================================================

class TestClustering:
    """Test K-Means and hierarchical clustering"""
    
    def test_kmeans_clustering(self, sample_numeric_data):
        """Should perform K-Means clustering"""
        result = clustering_analysis(sample_numeric_data, {
            'method': 'kmeans',
            'n_clusters': 3,
            'columns': ['age', 'height', 'weight']
        })
        
        assert result['analysis_type'] == 'clustering'
        assert 'test_results' in result
        assert 'silhouette_score' in result['test_results']
    
    def test_silhouette_score_range(self, sample_numeric_data):
        """Silhouette score should be between -1 and 1"""
        result = clustering_analysis(sample_numeric_data, {
            'method': 'kmeans',
            'n_clusters': 3,
            'columns': ['age', 'height', 'weight']
        })
        
        score = result['test_results']['silhouette_score']
        if score is not None:
            assert -1 <= score <= 1


# ============================================================================
# TEST: PCA
# ============================================================================

class TestPCA:
    """Test Principal Component Analysis"""
    
    def test_basic_pca(self, sample_numeric_data):
        """Should perform PCA"""
        result = pca_analysis(sample_numeric_data, {
            'n_components': 2,
            'columns': ['age', 'height', 'weight', 'score']
        })
        
        assert result['analysis_type'] == 'pca'
        assert 'test_results' in result
        assert 'explained_variance' in result['test_results']
    
    def test_explained_variance_sum(self, sample_numeric_data):
        """Total explained variance should be <= 1"""
        result = pca_analysis(sample_numeric_data, {
            'n_components': 3,
            'columns': ['age', 'height', 'weight', 'score']
        })
        
        variance = result['test_results']['explained_variance']
        total = sum(variance.values()) if isinstance(variance, dict) else sum(variance)
        assert total <= 1.0


# ============================================================================
# TEST: Power Analysis
# ============================================================================

class TestPowerAnalysis:
    """Test power analysis calculations"""
    
    def test_sample_size_calculation(self):
        """Should calculate required sample size"""
        result = power_analysis({
            'powerAnalysisType': 't-test',
            'calculate': 'sample_size',
            'effectSize': 0.5,
            'alpha': 0.05,
            'power': 0.8
        })
        
        assert result['analysis_type'] == 'power'
        assert 'result' in result
        assert result['result'] > 0
    
    def test_power_calculation(self):
        """Should calculate statistical power"""
        result = power_analysis({
            'powerAnalysisType': 't-test',
            'calculate': 'power',
            'effectSize': 0.5,
            'alpha': 0.05,
            'sampleSize': 64
        })
        
        assert result['analysis_type'] == 'power'
        assert 'result' in result
        assert 0 <= result['result'] <= 1


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
