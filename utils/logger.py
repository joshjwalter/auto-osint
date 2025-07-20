"""
Logging Utility
Provides centralized logging configuration for the application.
"""

import logging
import sys
from typing import Optional


def setup_logger(debug: bool = False, verbose: bool = False) -> logging.Logger:
    """Setup and configure the application logger"""
    logger = logging.getLogger("auto_osint")
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Set log level
    if debug:
        log_level = logging.DEBUG
    elif verbose:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING
    
    logger.setLevel(log_level)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Create formatter
    if debug:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Suppress noisy third-party loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance"""
    if name:
        return logging.getLogger(f"auto_osint.{name}")
    return logging.getLogger("auto_osint") 