"""
GradStat Analysis Worker
FastAPI service that performs statistical analyses
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import json
import os
from pathlib import Path
import tempfile
import zipfile
from typing import Dict, List, Any, Optional
import logging
from cache_manager import get_cached_result, cache_result, get_cache_stats, clear_cache
from test_advisor import recommend_test, auto_detect_from_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GradStat Analysis API",
    description="""
    ## Statistical Analysis API for Graduate Research
    
    Comprehensive statistical analysis service supporting 11 analysis types:
    
    * **Descriptive Statistics** - Summary stats, distributions, outliers
    * **Group Comparison** - t-tests, ANOVA, Tukey HSD
    * **Regression** - Linear, multiple, logistic regression
    * **Survival Analysis** - Kaplan-Meier, Log-Rank, Cox regression
    * **Non-Parametric Tests** - Mann-Whitney, Kruskal-Wallis, Wilcoxon
    * **Categorical Analysis** - Chi-square, Fisher's exact test
    * **Clustering** - K-Means, hierarchical clustering
    * **PCA** - Principal Component Analysis
    * **Time Series** - Trend analysis, forecasting
    * **Power Analysis** - Sample size, power, effect size calculations
    
    ### Features
    - Automatic assumption checking
    - Beautiful visualizations
    - Comprehensive error handling
    - Downloadable reports (HTML, Jupyter, PNG, JSON)
    
    ### Authentication
    Currently no authentication required (local deployment)
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "GradStat Support",
        "url": "https://github.com/yourusername/gradstat",
    },
    license_info={
        "name": "MIT License",
    },
)

# Configuration
TEMP_DIR = Path(os.getenv("TEMP_DIR", "./temp"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "./output"))
TEMP_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

@app.get(
    "/health",
    summary="Health Check",
    description="Check if the analysis worker service is running",
    tags=["System"]
)
async def health_check():
    """
    Minimal health check endpoint for monitoring services
    Returns only essential status information
    """
    return {"status": "healthy"}

@app.get(
    "/ping",
    summary="Minimal Ping",
    description="Ultra-minimal ping endpoint for cron monitoring",
    tags=["System"]
)
async def ping():
    """
    Ultra-minimal ping endpoint - returns just 'OK'
    Use this for cron-job.org to avoid response size limits
    """
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse("OK")

@app.get(
    "/cache/stats",
    summary="Get Cache Statistics",
    description="Get current cache statistics including hit rate and entry count",
    tags=["System"]
)
async def cache_stats():
    """
    Get cache statistics
    
    Returns:
        dict: Cache statistics including entries, hits, TTL, etc.
    """
    return get_cache_stats()

@app.post(
    "/cache/clear",
    summary="Clear Cache",
    description="Clear all cached analysis results",
    tags=["System"]
)
async def clear_analysis_cache():
    """
    Clear all cached results
    
    Returns:
        dict: Confirmation message
    """
    clear_cache()
    return {"status": "ok", "message": "Cache cleared successfully"}

@app.post(
    "/test-advisor/recommend",
    summary="Get Test Recommendations",
    description="Get statistical test recommendations based on research question and data characteristics",
    tags=["Test Advisor"]
)
async def get_test_recommendations(request: Request):
    """
    Recommend statistical tests based on user answers
    
    Args:
        request: User responses to wizard questions
        
    Returns:
        List of recommended tests with explanations
    """
    try:
        body = await request.json()
        logger.info(f"Received test advisor request: {body}")
        recommendations = recommend_test(body)
        logger.info(f"Generated {len(recommendations)} recommendations")
        return {"ok": True, "recommendations": recommendations}
    except Exception as e:
        logger.error(f"Test recommendation error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/test-advisor/auto-detect",
    summary="Auto-Detect Data Characteristics",
    description="Analyze uploaded data and detect characteristics for test recommendation",
    tags=["Test Advisor"]
)
async def auto_detect_data(file: UploadFile = File(...)):
    """
    Automatically detect data characteristics
    
    Args:
        file: CSV or Excel file to analyze
        
    Returns:
        Data characteristics and suggested tests
    """
    try:
        content = await file.read()
        df = read_datafile(content, file.filename)
        
        characteristics = auto_detect_from_data(df)
        
        return {"ok": True, "characteristics": characteristics}
    except Exception as e:
        logger.error(f"Auto-detection error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/test-advisor/auto-answer",
    summary="Auto-Answer Wizard Question",
    description="Automatically answer a specific wizard question based on data analysis",
    tags=["Test Advisor"]
)
async def auto_answer_question(file: UploadFile = File(...), question_key: str = Form(...)):
    """
    Auto-answer a specific wizard question
    
    Args:
        file: CSV or Excel file to analyze
        question_key: The question to answer (e.g., 'isNormal', 'nGroups', 'isPaired')
        
    Returns:
        Answer with confidence level and explanation
    """
    try:
        from test_advisor import auto_detect_answer
        
        content = await file.read()
        df = read_datafile(content, file.filename)
        
        result = auto_detect_answer(df, question_key)
        
        return {"ok": True, **result}
    except Exception as e:
        logger.error(f"Auto-answer error for {question_key}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/test-advisor/analyze-dataset",
    summary="Comprehensive Dataset Analysis",
    description="Analyze entire dataset and answer ALL wizard questions at once",
    tags=["Test Advisor"]
)
async def analyze_dataset(file: UploadFile = File(...)):
    """
    Analyze entire dataset comprehensively
    
    Args:
        file: CSV or Excel file to analyze
        
    Returns:
        All wizard answers with confidence levels and summary
    """
    try:
        from test_advisor import analyze_dataset_comprehensive
        
        content = await file.read()
        df = read_datafile(content, file.filename)
        
        result = analyze_dataset_comprehensive(df)
        
        return {"ok": True, **result}
    except Exception as e:
        logger.error(f"Dataset analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/validate",
    summary="Validate Data File",
    description="Validate uploaded CSV/Excel file and return data preview with column information",
    tags=["Data"]
)
async def validate_data(file: UploadFile = File(...)):
    """
    Validate uploaded data file
    
    Args:
        file: CSV or Excel file to validate
        
    Returns:
        dict: Validation results including:
            - columns: List of column names
            - numeric_columns: List of numeric column names
            - categorical_columns: List of categorical column names
            - preview: First 10 rows of data
            - row_count: Total number of rows
            
    Raises:
        HTTPException: If file format is invalid or cannot be read
    """
    try:
        # Read file
        content = await file.read()
        df = read_datafile(content, file.filename)
        
        # Infer types
        types_dict = infer_column_types(df)
        
        # Run comprehensive data quality checks
        from data_quality import analyze_data_quality
        quality_report = analyze_data_quality(df)
        
        # Legacy issues format (for backward compatibility)
        issues = check_data_quality(df)
        
        # Generate recommendations
        recommendations = generate_recommendations(df, issues)
        
        # Create preview
        preview = {
            "columns": list(df.columns),
            "rows": df.head(10).fillna("").values.tolist(),
            "types": types_dict,
            "rowCount": len(df),
            "issues": issues,  # Legacy format
            "recommendations": recommendations,  # Legacy format
            "quality_report": quality_report  # New comprehensive report
        }
        
        return {"ok": True, "preview": preview}
        
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post(
    "/analyze",
    summary="Perform Statistical Analysis",
    description="""
    Perform comprehensive statistical analysis on uploaded data.
    
    Supports 11 analysis types with automatic assumption checking,
    beautiful visualizations, and comprehensive results.
    """,
    tags=["Analysis"]
)
async def analyze_data(
    file: UploadFile = File(..., description="CSV or Excel data file"),
    options: str = Form(..., description="JSON string with analysis options including analysisType and type-specific parameters")
):
    """
    Perform statistical analysis
    
    Args:
        file: Data file (CSV or Excel)
        options: JSON string containing:
            - analysisType: One of [descriptive, group-comparison, regression, 
                           logistic-regression, survival, nonparametric, categorical,
                           clustering, pca, time-series, power]
            - Type-specific options (see documentation for each type)
            
    Returns:
        dict: Analysis results including:
            - analysis_type: Type of analysis performed
            - summary: Brief summary of results
            - test_results: Statistical test results
            - plots: Base64-encoded visualization images
            - interpretation: Natural language interpretation
            - recommendations: Actionable recommendations
            - conclusion: Summary conclusion
            
    Raises:
        HTTPException: If analysis fails or invalid parameters provided
        
    Example:
        ```json
        {
            "analysisType": "group-comparison",
            "valueColumn": "score",
            "groupColumn": "treatment"
        }
        ```
    """
    try:
        # Parse options
        opts = json.loads(options)
        analysis_type = opts.get("analysisType", "descriptive")
        
        # Power analysis doesn't need data file
        if analysis_type == "power":
            results = power_analysis(opts)
            # Create empty dataframe for report generation
            df = pd.DataFrame()
        else:
            # Read data for other analyses
            content = await file.read()
            
            # Check cache first
            cached_result = get_cached_result(content, opts)
            if cached_result is not None:
                logger.info(f"Returning cached result for {analysis_type}")
                return cached_result
            
            # Cache miss - perform analysis
            df = read_datafile(content, file.filename)
            
            # Route to appropriate analysis
            if analysis_type == "descriptive":
                results = descriptive_analysis(df, opts)
            elif analysis_type == "group-comparison":
                results = group_comparison_analysis(df, opts)
            elif analysis_type == "regression":
                results = regression_analysis(df, opts)
            elif analysis_type == "logistic-regression":
                results = logistic_regression_analysis(df, opts)
            elif analysis_type == "survival":
                results = survival_analysis(df, opts)
            elif analysis_type == "nonparametric":
                results = nonparametric_test(df, opts)
            elif analysis_type == "categorical":
                results = categorical_analysis(df, opts)
            elif analysis_type == "clustering":
                results = clustering_analysis(df, opts)
            elif analysis_type == "pca":
                results = pca_analysis(df, opts)
            elif analysis_type == "time-series":
                results = time_series_analysis(df, opts)
            elif analysis_type == "correlation":
                results = correlation_analysis(df, opts)
            elif analysis_type == "ancova":
                from advanced_tests import ancova_analysis
                results = ancova_analysis(df, opts)
            elif analysis_type == "repeated-measures":
                from advanced_tests import repeated_measures_anova
                results = repeated_measures_anova(df, opts)
            elif analysis_type == "posthoc-tukey":
                from advanced_tests import posthoc_tukey
                results = posthoc_tukey(df, opts)
            else:
                raise ValueError(f"Unknown analysis type: {analysis_type}")
        
        # Generate report ZIP
        report_zip_b64 = generate_report_package(results, df, opts)
        
        response = {
            "results": results,
            "report_zip": report_zip_b64
        }
        
        # Cache the result (only for non-power analyses with file content)
        if analysis_type != "power" and 'content' in locals():
            cache_result(content, opts, response)
            logger.info(f"Cached result for {analysis_type}")
        
        return response
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def read_datafile(content: bytes, filename: str) -> pd.DataFrame:
    """Read CSV or Excel file"""
    if filename.endswith('.csv'):
        # Try to read with explicit encoding and error handling
        try:
            df = pd.read_csv(io.BytesIO(content), encoding='utf-8')
        except UnicodeDecodeError:
            # Try with different encoding
            df = pd.read_csv(io.BytesIO(content), encoding='latin-1')
        
        # Log for debugging
        logger.info(f"CSV read successfully: {df.shape[0]} rows, {df.shape[1]} columns")
        logger.info(f"Columns: {list(df.columns)}")
        logger.info(f"Dtypes: {df.dtypes.to_dict()}")
        
        return df
    elif filename.endswith(('.xlsx', '.xls')):
        return pd.read_excel(io.BytesIO(content))
    else:
        raise ValueError("Unsupported file format")

def infer_column_types(df: pd.DataFrame) -> Dict[str, str]:
    """Infer and return column types"""
    types = {}
    for col in df.columns:
        dtype = str(df[col].dtype)
        if dtype.startswith('int'):
            types[col] = 'int64'
        elif dtype.startswith('float'):
            types[col] = 'float64'
        elif dtype == 'object':
            types[col] = 'string'
        elif dtype == 'datetime64':
            types[col] = 'datetime'
        else:
            types[col] = dtype
    return types

def check_data_quality(df: pd.DataFrame) -> List[Dict]:
    """Check for data quality issues"""
    issues = []
    
    # Missing values
    missing = df.isnull().sum()
    for col, count in missing.items():
        if count > 0:
            pct = (count / len(df)) * 100
            severity = "error" if pct > 50 else "warning" if pct > 10 else "info"
            issues.append({
                "severity": severity,
                "column": col,
                "message": f"{pct:.1f}% missing values",
                "count": int(count)
            })
    
    # Check for duplicates
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        issues.append({
            "severity": "warning",
            "message": f"{dup_count} duplicate rows found",
            "count": int(dup_count)
        })
    
    return issues

def generate_recommendations(df: pd.DataFrame, issues: List[Dict]) -> List[str]:
    """Generate data cleaning recommendations"""
    recs = []
    
    if any(i['severity'] == 'error' for i in issues):
        recs.append("Consider removing or imputing columns with >50% missing values")
    
    if len(df) < 30:
        recs.append("Small sample size (n<30) may limit statistical power")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        recs.append(f"Dataset contains {len(numeric_cols)} numeric columns suitable for analysis")
    
    return recs

# Analysis functions continue in next file...
