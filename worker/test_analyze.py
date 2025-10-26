"""
Tests for analysis worker
"""

import pytest
import pandas as pd
import numpy as np
from io import BytesIO
from analysis_functions import (
    descriptive_analysis,
    group_comparison_analysis,
    regression_analysis,
    clustering_analysis,
    pca_analysis
)

@pytest.fixture
def sample_dataframe():
    """Create a sample dataframe for testing"""
    np.random.seed(42)
    return pd.DataFrame({
        'age': np.random.randint(20, 60, 100),
        'score': np.random.normal(75, 10, 100),
        'group': np.random.choice(['A', 'B'], 100),
        'income': np.random.normal(50000, 15000, 100)
    })

def test_descriptive_analysis(sample_dataframe):
    """Test descriptive statistics analysis"""
    opts = {}
    result = descriptive_analysis(sample_dataframe, opts)
    
    assert result['analysis_type'] == 'descriptive'
    assert 'summary' in result
    assert 'test_results' in result
    assert 'plots' in result
    assert len(result['plots']) > 0

def test_group_comparison_analysis(sample_dataframe):
    """Test group comparison analysis"""
    opts = {
        'groupVar': 'group',
        'dependentVar': 'score',
        'alpha': 0.05
    }
    result = group_comparison_analysis(sample_dataframe, opts)
    
    assert result['analysis_type'] == 'group-comparison'
    assert 'test_results' in result
    assert 'assumptions' in result
    assert 'p_value' in result['test_results']
    assert len(result['assumptions']) > 0

def test_regression_analysis(sample_dataframe):
    """Test regression analysis"""
    opts = {
        'dependentVar': 'score',
        'independentVar': 'age',
        'alpha': 0.05
    }
    result = regression_analysis(sample_dataframe, opts)
    
    assert result['analysis_type'] == 'regression'
    assert 'test_results' in result
    assert 'r_squared' in result['test_results']
    assert 'coefficients' in result['test_results']
    assert len(result['plots']) >= 2  # Regression plot and residual plot

def test_clustering_analysis(sample_dataframe):
    """Test clustering analysis"""
    opts = {
        'nClusters': 3
    }
    result = clustering_analysis(sample_dataframe, opts)
    
    assert result['analysis_type'] == 'clustering'
    assert 'test_results' in result
    assert result['test_results']['n_clusters'] == 3
    assert 'cluster_sizes' in result['test_results']

def test_pca_analysis(sample_dataframe):
    """Test PCA analysis"""
    opts = {
        'nComponents': 2
    }
    result = pca_analysis(sample_dataframe, opts)
    
    assert result['analysis_type'] == 'pca'
    assert 'test_results' in result
    assert 'explained_variance_ratio' in result['test_results']
    assert len(result['plots']) >= 1

def test_group_comparison_missing_variables(sample_dataframe):
    """Test that analysis raises error with missing variables"""
    opts = {}
    
    with pytest.raises(ValueError):
        group_comparison_analysis(sample_dataframe, opts)

def test_regression_missing_variables(sample_dataframe):
    """Test that regression raises error with missing variables"""
    opts = {}
    
    with pytest.raises(ValueError):
        regression_analysis(sample_dataframe, opts)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
