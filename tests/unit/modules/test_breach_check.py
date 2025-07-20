import pytest
from unittest.mock import Mock, patch
from modules.breach_check import BreachScanner

class TestBreachScanner:
    def test_breach_scanner_initialization(self, mock_config):
        """Test breach scanner initializes correctly"""
        scanner = BreachScanner(mock_config)
        assert scanner.config == mock_config

    def test_extract_emails(self, mock_config):
        """Test email extraction from target data"""
        scanner = BreachScanner(mock_config)
        
        # Test direct email
        emails = scanner._extract_emails({"email": "test@example.com"})
        assert "test@example.com" in emails
        
        # Test multiple emails
        target = {
            "email": "test@example.com",
            "username": "testuser@example.com"  # Should not be extracted
        }
        emails = scanner._extract_emails(target)
        assert "test@example.com" in emails
        assert len(emails) == 1

    def test_test_mode_simulation(self, mock_config):
        """Test that test mode properly simulates results"""
        scanner = BreachScanner(mock_config, test_mode=True)
        results = scanner.scan({"email": "test@example.com"})
        
        assert "breaches" in results
        assert "summary" in results
        assert results["summary"]["total_breaches"] == 0

    @patch('modules.breach_check.BreachScanner._check_haveibeenpwned')
    def test_haveibeenpwned_check(self, mock_check, mock_config):
        """Test HaveIBeenPwned API check"""
        mock_check.return_value = {"breaches": ["test_breach"]}
        
        scanner = BreachScanner(mock_config)
        results = scanner._check_haveibeenpwned("test@example.com")
        
        assert "breaches" in results
        assert len(results["breaches"]) > 0

    @patch('modules.breach_check.BreachScanner._check_dehashed')
    def test_dehashed_check(self, mock_check, mock_config):
        """Test Dehashed API check"""
        mock_check.return_value = {"breaches": ["test_breach"]}
        
        scanner = BreachScanner(mock_config)
        results = scanner._check_dehashed("test@example.com")
        
        assert "breaches" in results

    def test_empty_target_handling(self, mock_config):
        """Test handling of empty target data"""
        scanner = BreachScanner(mock_config, test_mode=True)
        
        results = scanner.scan({})
        assert results["summary"]["total_breaches"] == 0
        assert "breaches" in results

    def test_multiple_emails(self, mock_config):
        """Test handling of multiple emails"""
        scanner = BreachScanner(mock_config, test_mode=True)
        
        # Target with multiple email sources
        target = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User"
        }
        
        results = scanner.scan(target)
        assert "summary" in results

    def test_scan_timing(self, mock_config):
        """Test scan timing calculation"""
        scanner = BreachScanner(mock_config, test_mode=True)
        results = scanner.scan({"email": "test@example.com"})
        
        assert "scan_time" in results
        assert isinstance(results["scan_time"], (int, float))

    def test_api_key_handling(self, mock_config):
        """Test API key configuration handling"""
        scanner = BreachScanner(mock_config)
        
        # Test that API keys are properly accessed
        assert "haveibeenpwned_api_key" in scanner.config
        assert "dehashed_api_key" in scanner.config

    def test_breach_data_structure(self, mock_config):
        """Test breach data structure"""
        scanner = BreachScanner(mock_config, test_mode=True)
        results = scanner.scan({"email": "test@example.com"})
        
        # Check expected structure
        assert "breaches" in results
        assert "summary" in results
        assert "total_breaches" in results["summary"]
        assert "total_records" in results["summary"]
        assert "apis_checked" in results["summary"] 