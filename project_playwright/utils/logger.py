"""
===============================================================================
Enterprise-Grade Logging System
===============================================================================
Provides structured logging with environment, array, and test context tracking
Supports console and file-based logging with detailed formatting

Usage:
    from utils.logger import get_logger
    
    logger = get_logger(__name__)
    logger.info("Test execution started")
    logger.error("Test failed")
===============================================================================
"""

import logging
import sys
import threading
from typing import Optional, Dict, Any


# Thread-local storage for execution context
_execution_context = threading.local()


class ContextFormatter(logging.Formatter):
    """
    Custom formatter that includes execution context (environment, array, test).
    Provides structured logging with consistent formatting.
    """
    
    def format(self, record):
        # Get context information
        env = getattr(_execution_context, "environment", "UNKNOWN")
        array = getattr(_execution_context, "array", "N/A")
        test = getattr(_execution_context, "test_name", "")
        
        # Add context to log record
        record.env = env
        record.array = array
        record.test = test
        
        return super().format(record)


def get_logger(name: str) -> logging.Logger:
    """
    Get or create logger with enterprise-grade formatting.
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        
        # Use context formatter for structured logging
        formatter = ContextFormatter(
            "%(asctime)s | %(levelname)8s | %(env)-6s | "
            "%(array)-20s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def set_execution_context(
    environment: str = None,
    array: str = None,
    test_name: str = None
):
    """
    Set execution context for logging (environment, array, test).
    
    Args:
        environment: Current environment (dev, qa, stage, prod)
        array: Current array/server (array_01, array_02, etc.)
        test_name: Current test name
    """
    if environment:
        _execution_context.environment = environment.upper()
    if array:
        _execution_context.array = f"[{array}]"
    if test_name:
        _execution_context.test_name = test_name


def clear_execution_context():
    """Clear execution context."""
    _execution_context.environment = "UNKNOWN"
    _execution_context.array = "N/A"
    _execution_context.test_name = ""


def get_execution_context() -> Dict[str, Any]:
    """
    Get current execution context.
    
    Returns:
        Dictionary with current context (environment, array, test_name)
    """
    return {
        "environment": getattr(_execution_context, "environment", "UNKNOWN"),
        "array": getattr(_execution_context, "array", "N/A"),
        "test_name": getattr(_execution_context, "test_name", "")
    }


# Initialize default context
clear_execution_context()
