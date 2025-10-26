"""
Main entry point for GradStat analysis worker
Imports all analysis functions and report generation
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from analyze import app
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
    time_series_analysis,
    power_analysis,
    correlation_analysis
)
from report_generator import generate_report_package

# Import analysis functions into analyze module
import analyze
analyze.descriptive_analysis = descriptive_analysis
analyze.group_comparison_analysis = group_comparison_analysis
analyze.regression_analysis = regression_analysis
analyze.logistic_regression_analysis = logistic_regression_analysis
analyze.survival_analysis = survival_analysis
analyze.nonparametric_test = nonparametric_test
analyze.categorical_analysis = categorical_analysis
analyze.clustering_analysis = clustering_analysis
analyze.pca_analysis = pca_analysis
analyze.time_series_analysis = time_series_analysis
analyze.power_analysis = power_analysis
analyze.correlation_analysis = correlation_analysis
analyze.generate_report_package = generate_report_package

if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.getenv("WORKER_PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
