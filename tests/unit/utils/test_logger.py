import pytest
import logging
from unittest.mock import Mock, patch
from utils.logger import setup_logger

class TestLogger:
    def test_logger_initialization(self):
        """Test logger initializes correctly"""
        logger = setup_logger("test_logger")
        assert logger is not None
        assert logger.name == "test_logger"

    def test_logger_verbose_mode(self):
        """Test logger in verbose mode"""
        logger = setup_logger("test_logger", verbose=True)
        
        # Should have DEBUG level in verbose mode
        assert logger.level == logging.DEBUG

    def test_logger_debug_mode(self):
        """Test logger in debug mode"""
        logger = setup_logger("test_logger", debug=True)
        
        # Should have DEBUG level in debug mode
        assert logger.level == logging.DEBUG

    def test_logger_normal_mode(self):
        """Test logger in normal mode"""
        logger = setup_logger("test_logger", verbose=False, debug=False)
        
        # Should have INFO level in normal mode
        assert logger.level == logging.INFO

    def test_logger_handlers(self):
        """Test logger has proper handlers"""
        logger = setup_logger("test_logger")
        
        # Should have at least one handler
        assert len(logger.handlers) > 0
        
        # Check for console handler
        has_console_handler = any(
            isinstance(handler, logging.StreamHandler) 
            for handler in logger.handlers
        )
        assert has_console_handler

    def test_logger_formatter(self):
        """Test logger formatter configuration"""
        logger = setup_logger("test_logger")
        
        # Check that handlers have formatters
        for handler in logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                assert handler.formatter is not None

    def test_logger_propagation(self):
        """Test logger propagation settings"""
        logger = setup_logger("test_logger")
        
        # Should not propagate to root logger
        assert not logger.propagate

    def test_logger_different_names(self):
        """Test logger with different names"""
        logger1 = setup_logger("logger1")
        logger2 = setup_logger("logger2")
        
        assert logger1.name == "logger1"
        assert logger2.name == "logger2"
        assert logger1 is not logger2

    def test_logger_levels(self):
        """Test logger can log at different levels"""
        logger = setup_logger("test_logger", verbose=True)
        
        # Test that we can log at different levels
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        
        # No exceptions should be raised

    def test_logger_file_handler(self):
        """Test logger with file handler"""
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            logger = setup_logger("test_logger", log_file=tmp_file.name)
            
            # Should have file handler
            has_file_handler = any(
                isinstance(handler, logging.FileHandler) 
                for handler in logger.handlers
            )
            assert has_file_handler
            
            # Clean up
            os.unlink(tmp_file.name)

    def test_logger_custom_level(self):
        """Test logger with custom log level"""
        logger = setup_logger("test_logger", log_level=logging.WARNING)
        
        assert logger.level == logging.WARNING

    def test_logger_singleton_behavior(self):
        """Test that logger with same name returns same instance"""
        logger1 = setup_logger("singleton_test")
        logger2 = setup_logger("singleton_test")
        
        assert logger1 is logger2 