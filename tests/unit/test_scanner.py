import pytest
from unittest.mock import Mock, patch
from core.scanner import OSINTScanner

class TestOSINTScanner:
    def test_scanner_initialization(self, mock_config):
        """Test scanner initializes correctly"""
        scanner = OSINTScanner(mock_config, verbose=True, test_mode=True)
        assert scanner.config == mock_config
        assert scanner.verbose is True
        assert scanner.test_mode is True
        assert len(scanner.scanners) > 0

    def test_scan_target_with_valid_data(self, mock_config, sample_target):
        """Test scanning with valid target data"""
        scanner = OSINTScanner(mock_config, test_mode=True)
        results = scanner.scan_target(sample_target, ["social"])
        
        assert "target" in results
        assert "scan_time" in results
        assert "results" in results
        assert "social" in results["results"]

    def test_validate_target(self, mock_config):
        """Test target validation"""
        scanner = OSINTScanner(mock_config)
        
        # Valid target
        assert scanner.validate_target({"email": "test@example.com"})
        
        # Invalid target
        assert not scanner.validate_target({})

    @patch('time.time')
    def test_scan_timing(self, mock_time, mock_config, sample_target):
        """Test scan timing calculation"""
        mock_time.side_effect = [0, 1]  # Start and end time
        
        scanner = OSINTScanner(mock_config, test_mode=True)
        results = scanner.scan_target(sample_target, ["social"])
        
        assert results["results"]["social"]["scan_time"] == 1.0

    def test_test_mode_simulation(self, mock_config, sample_target):
        """Test that test mode properly simulates results"""
        scanner = OSINTScanner(mock_config, test_mode=True)
        results = scanner.scan_target(sample_target, ["social", "breach"])
        
        # Check that test mode produces expected results
        assert "social" in results["results"]
        assert "breach" in results["results"]
        assert results["results"]["social"]["status"] == "completed"

    def test_invalid_search_types(self, mock_config, sample_target):
        """Test handling of invalid search types"""
        scanner = OSINTScanner(mock_config, test_mode=True)
        results = scanner.scan_target(sample_target, ["invalid_type"])
        
        # Should handle gracefully
        assert "target" in results
        assert "results" in results

    def test_empty_search_types(self, mock_config, sample_target):
        """Test handling of empty search types list"""
        scanner = OSINTScanner(mock_config, test_mode=True)
        results = scanner.scan_target(sample_target, [])
        
        # Should return basic structure even with no search types
        assert "target" in results
        assert "results" in results 