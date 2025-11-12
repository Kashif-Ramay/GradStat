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

# Try to import LLM interpreter (optional feature)
try:
    from llm_interpreter import StatisticalInterpreter
    LLM_AVAILABLE = True
except Exception as e:
    logger.warning(f"LLM interpreter not available: {e}")
    StatisticalInterpreter = None
    LLM_AVAILABLE = False

# Try to import Test Advisor AI (optional feature)
try:
    from test_advisor_llm import TestAdvisorAI
    TEST_ADVISOR_AI_AVAILABLE = True
except Exception as e:
    logger.warning(f"Test Advisor AI not available: {e}")
    TestAdvisorAI = None
    TEST_ADVISOR_AI_AVAILABLE = False

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
    "/",
    summary="Root Endpoint",
    description="API root - returns service information",
    tags=["System"]
)
async def root():
    """
    Root endpoint for Render health checks and service info
    """
    return {
        "service": "GradStat Analysis Worker",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "analyze": "/analyze"
        }
    }

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

@app.get("/ping", include_in_schema=False)
async def ping():
    """Ultra-minimal ping - returns plain text OK"""
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse("OK", media_type="text/plain")

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

# Initialize LLM interpreter (if available)
llm_interpreter = StatisticalInterpreter() if LLM_AVAILABLE else None

# Initialize Test Advisor AI (if available)
test_advisor_ai = TestAdvisorAI() if TEST_ADVISOR_AI_AVAILABLE else None

@app.post(
    "/interpret",
    summary="AI Interpretation",
    description="Get AI-powered interpretation of analysis results",
    tags=["AI Assistant"]
)
async def interpret_results(request: Request):
    """
    Generate AI interpretation of statistical results using GPT
    
    Request body should contain:
    - analysis_type: Type of analysis performed
    - sample_size: Number of observations
    - variables: List of variable names
    - results: Dictionary of statistical results
    - assumptions: Dictionary of assumption check results
    """
    if not LLM_AVAILABLE or llm_interpreter is None:
        return {
            "error": "LLM service not available",
            "interpretation": "AI interpretation requires the OpenAI package. Install with: pip install openai>=1.0.0",
            "key_findings": [],
            "concerns": [],
            "next_steps": []
        }
    
    try:
        data = await request.json()
        interpretation = llm_interpreter.interpret_results(data)
        return interpretation
    except Exception as e:
        logger.error(f"Interpretation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/ask",
    summary="Ask Question",
    description="Ask a question about your analysis results",
    tags=["AI Assistant"]
)
async def ask_question(request: Request):
    """
    Answer questions about analysis results using AI
    
    Request body should contain:
    - question: The question to answer
    - analysis_data: Full analysis context
    - conversation_history: Optional previous messages
    """
    if not LLM_AVAILABLE or llm_interpreter is None:
        return {"answer": "AI question answering requires the OpenAI package. Install with: pip install openai>=1.0.0"}
    
    try:
        data = await request.json()
        question = data.get('question')
        analysis_data = data.get('analysis_data')
        history = data.get('conversation_history', [])
        
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
        if not analysis_data:
            raise HTTPException(status_code=400, detail="Analysis data is required")
        
        answer = llm_interpreter.answer_question(
            question, 
            analysis_data, 
            history
        )
        
        return {"answer": answer}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Question answering error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/what-if",
    summary="What-If Analysis",
    description="Explore hypothetical scenarios based on your results",
    tags=["AI Assistant"]
)
async def what_if_scenario(request: Request):
    """
    Answer "what if" questions about the analysis
    
    Request body should contain:
    - scenario: The hypothetical scenario to explore
    - analysis_data: Full analysis context
    """
    if not LLM_AVAILABLE or llm_interpreter is None:
        return {"response": "AI scenario analysis requires the OpenAI package. Install with: pip install openai>=1.0.0"}
    
    try:
        data = await request.json()
        scenario = data.get('scenario')
        analysis_data = data.get('analysis_data')
        
        if not scenario:
            raise HTTPException(status_code=400, detail="Scenario is required")
        if not analysis_data:
            raise HTTPException(status_code=400, detail="Analysis data is required")
        
        response = llm_interpreter.what_if_analysis(scenario, analysis_data)
        
        return {"response": response}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"What-if analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/test-advisor/recommend",
    summary="AI Test Recommendation",
    description="Get AI-powered test recommendations from research description",
    tags=["Test Advisor AI"]
)
async def ai_recommend_test(request: Request):
    """
    Get statistical test recommendations based on user's research description
    
    Request body should contain:
    - description: User's description of their research scenario
    - data_summary: Optional summary of uploaded data
    """
    if not TEST_ADVISOR_AI_AVAILABLE or test_advisor_ai is None:
        return {
            "error": "Test Advisor AI not available",
            "message": "Test Advisor AI requires the OpenAI package. Install with: pip install openai>=1.0.0"
        }
    
    try:
        data = await request.json()
        description = data.get('description', '')
        data_summary = data.get('data_summary')
        
        if not description:
            raise HTTPException(status_code=400, detail="Description is required")
        
        result = test_advisor_ai.recommend_from_description(description, data_summary)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AI recommendation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/test-advisor/ask",
    summary="Ask AI Question",
    description="Ask AI a question about statistical tests or concepts",
    tags=["Test Advisor AI"]
)
async def ai_ask_question(request: Request):
    """
    Answer user's question about statistical tests or concepts
    
    Request body should contain:
    - question: User's question
    - context: Optional context (current wizard state, data info)
    """
    if not TEST_ADVISOR_AI_AVAILABLE or test_advisor_ai is None:
        return {"answer": "Test Advisor AI requires the OpenAI package. Install with: pip install openai>=1.0.0"}
    
    try:
        data = await request.json()
        question = data.get('question', '')
        context = data.get('context')
        
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
        
        answer = test_advisor_ai.answer_question(question, context)
        return {"answer": answer}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AI question error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/test-advisor/explain",
    summary="Explain Assumption",
    description="Get plain-language explanation of statistical assumption",
    tags=["Test Advisor AI"]
)
async def ai_explain_assumption(request: Request):
    """
    Explain a statistical assumption in plain language
    
    Request body should contain:
    - assumption: Name of the assumption
    - test_type: Optional test type for context
    """
    if not TEST_ADVISOR_AI_AVAILABLE or test_advisor_ai is None:
        return {"explanation": "Test Advisor AI requires the OpenAI package. Install with: pip install openai>=1.0.0"}
    
    try:
        data = await request.json()
        assumption = data.get('assumption', '')
        test_type = data.get('test_type')
        
        if not assumption:
            raise HTTPException(status_code=400, detail="Assumption name is required")
        
        explanation = test_advisor_ai.explain_assumption(assumption, test_type)
        return {"explanation": explanation}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AI explanation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/test-advisor/compare",
    summary="Compare Tests",
    description="Compare two statistical tests with AI guidance",
    tags=["Test Advisor AI"]
)
async def ai_compare_tests(request: Request):
    """
    Compare two statistical tests and explain when to use each
    
    Request body should contain:
    - test1: First test name
    - test2: Second test name
    - context: Optional context about the data/scenario
    """
    if not TEST_ADVISOR_AI_AVAILABLE or test_advisor_ai is None:
        return {
            "error": "Test Advisor AI not available",
            "message": "Test Advisor AI requires the OpenAI package. Install with: pip install openai>=1.0.0"
        }
    
    try:
        data = await request.json()
        test1 = data.get('test1', '')
        test2 = data.get('test2', '')
        context = data.get('context')
        
        if not test1 or not test2:
            raise HTTPException(status_code=400, detail="Both test names are required")
        
        result = test_advisor_ai.compare_tests(test1, test2, context)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AI comparison error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/test-advisor/enhance-detection",
    summary="Enhance Auto-Detection",
    description="Enhance auto-detection results with AI explanation",
    tags=["Test Advisor AI"]
)
async def ai_enhance_detection(request: Request):
    """
    Enhance auto-detection results with AI-generated explanation
    
    Request body should contain:
    - detection_result: Result from auto-detection
    - question_type: Type of question (isNormal, isPaired, etc.)
    """
    if not TEST_ADVISOR_AI_AVAILABLE or test_advisor_ai is None:
        return {"enhanced_explanation": "Test Advisor AI requires the OpenAI package."}
    
    try:
        data = await request.json()
        detection_result = data.get('detection_result', {})
        question_type = data.get('question_type', '')
        
        if not detection_result or not question_type:
            raise HTTPException(status_code=400, detail="Detection result and question type are required")
        
        enhanced = test_advisor_ai.enhance_auto_detection(detection_result, question_type)
        return {"enhanced_explanation": enhanced}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AI enhancement error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/test-advisor/sample-size",
    summary="Sample Size Guidance",
    description="Get AI-powered sample size guidance",
    tags=["Test Advisor AI"]
)
async def ai_sample_size_guidance(request: Request):
    """
    Provide sample size guidance for a given test
    
    Request body should contain:
    - test_type: Type of statistical test
    - current_n: Current sample size
    - effect_size: Expected effect size (small/medium/large)
    """
    if not TEST_ADVISOR_AI_AVAILABLE or test_advisor_ai is None:
        return {
            "error": "Test Advisor AI not available",
            "message": "Test Advisor AI requires the OpenAI package."
        }
    
    try:
        data = await request.json()
        test_type = data.get('test_type', '')
        current_n = data.get('current_n', 0)
        effect_size = data.get('effect_size', 'medium')
        
        if not test_type:
            raise HTTPException(status_code=400, detail="Test type is required")
        
        result = test_advisor_ai.suggest_sample_size(test_type, current_n, effect_size)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AI sample size guidance error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Analysis functions continue in next file...
