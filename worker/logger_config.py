"""
Comprehensive logging configuration for GradStat
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

# Create logs directory if it doesn't exist
LOGS_DIR = Path(__file__).parent / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# Log file paths
ERROR_LOG = LOGS_DIR / 'error.log'
INFO_LOG = LOGS_DIR / 'info.log'
DEBUG_LOG = LOGS_DIR / 'debug.log'


def setup_logger(name='gradstat', level=logging.INFO):
    """
    Setup comprehensive logging with multiple handlers
    
    Args:
        name: Logger name
        level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Capture all levels
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Formatter
    detailed_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)-8s [%(name)s:%(funcName)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)-8s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console Handler (INFO and above)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # Error File Handler (ERROR and above)
    error_handler = logging.FileHandler(ERROR_LOG)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    logger.addHandler(error_handler)
    
    # Info File Handler (INFO and above)
    info_handler = logging.FileHandler(INFO_LOG)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(detailed_formatter)
    logger.addHandler(info_handler)
    
    # Debug File Handler (DEBUG and above)
    debug_handler = logging.FileHandler(DEBUG_LOG)
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(detailed_formatter)
    logger.addHandler(debug_handler)
    
    return logger


# Create default logger
logger = setup_logger()


def log_analysis_start(analysis_type, options):
    """Log the start of an analysis"""
    logger.info(f"Starting {analysis_type} analysis with options: {options}")


def log_analysis_complete(analysis_type, duration_ms):
    """Log successful completion of an analysis"""
    logger.info(f"Completed {analysis_type} analysis in {duration_ms:.2f}ms")


def log_analysis_error(analysis_type, error, options=None):
    """Log an error during analysis"""
    logger.error(
        f"Error in {analysis_type} analysis: {str(error)}",
        exc_info=True,
        extra={'options': options}
    )


def log_data_quality_warning(message, details=None):
    """Log data quality warnings"""
    logger.warning(f"Data Quality Warning: {message}")
    if details:
        logger.warning(f"Details: {details}")


def log_inf_nan_detected(location, value_name):
    """Log when inf/nan values are detected and handled"""
    logger.debug(f"Inf/NaN detected in {location}.{value_name} - converted to None")


# Example usage
if __name__ == '__main__':
    logger.info("Logger configuration test")
    logger.debug("This is a debug message")
    logger.warning("This is a warning")
    logger.error("This is an error")
    
    try:
        1 / 0
    except Exception as e:
        log_analysis_error("test", e, {"test": "options"})
