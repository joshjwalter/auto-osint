import pytest
from unittest.mock import Mock, patch
from modules.domain_intelligence import DomainScanner

class TestDomainScanner:
    def test_domain_scanner_initialization(self, mock_config):
        """Test domain scanner initializes correctly"""
        scanner = DomainScanner(mock_config)
        assert scanner.config == mock_config

    def test_extract_domains(self, mock_config):
        """Test domain extraction from target data"""
        scanner = DomainScanner(mock_config)
        
        # Test direct domain
        domains = scanner._extract_domains({"domain": "example.com"})
        assert "example.com" in domains
        
        # Test email domain extraction
        domains = scanner._extract_domains({"email": "test@example.com"})
        assert "example.com" in domains
        
        # Test multiple domains
        target = {
            "domain": "example.com",
            "email": "test@another.com"
        }
        domains = scanner._extract_domains(target)
        assert "example.com" in domains
        assert "another.com" in domains

    def test_test_mode_simulation(self, mock_config):
        """Test that test mode properly simulates results"""
        scanner = DomainScanner(mock_config, test_mode=True)
        results = scanner.scan({"domain": "example.com"})
        
        assert "domains" in results
        assert "summary" in results
        assert results["summary"]["domains_checked"] > 0

    @patch('modules.domain_intelligence.DomainScanner._whois_lookup')
    def test_whois_lookup(self, mock_whois, mock_config):
        """Test WHOIS lookup functionality"""
        mock_whois.return_value = {
            "registrar": "Test Registrar",
            "creation_date": "2020-01-01",
            "expiration_date": "2025-01-01"
        }
        
        scanner = DomainScanner(mock_config)
        results = scanner._whois_lookup("example.com")
        
        assert "registrar" in results
        assert "creation_date" in results

    @patch('modules.domain_intelligence.DomainScanner._dns_lookup')
    def test_dns_lookup(self, mock_dns, mock_config):
        """Test DNS lookup functionality"""
        mock_dns.return_value = {
            "a": ["192.168.1.1"],
            "mx": ["mail.example.com"],
            "ns": ["ns1.example.com"]
        }
        
        scanner = DomainScanner(mock_config)
        results = scanner._dns_lookup("example.com")
        
        assert "a" in results
        assert "mx" in results
        assert "ns" in results

    @patch('modules.domain_intelligence.DomainScanner._ssl_cert_check')
    def test_ssl_cert_check(self, mock_ssl, mock_config):
        """Test SSL certificate check"""
        mock_ssl.return_value = {
            "issuer": "Test CA",
            "valid_from": "2023-01-01",
            "valid_until": "2024-01-01"
        }
        
        scanner = DomainScanner(mock_config)
        results = scanner._ssl_cert_check("example.com")
        
        assert "issuer" in results
        assert "valid_from" in results

    def test_empty_target_handling(self, mock_config):
        """Test handling of empty target data"""
        scanner = DomainScanner(mock_config, test_mode=True)
        
        results = scanner.scan({})
        assert results["summary"]["domains_checked"] == 0
        assert "domains" in results

    def test_multiple_domains(self, mock_config):
        """Test handling of multiple domains"""
        scanner = DomainScanner(mock_config, test_mode=True)
        
        # Target with multiple domain sources
        target = {
            "domain": "example.com",
            "email": "test@another.com"
        }
        
        results = scanner.scan(target)
        assert results["summary"]["domains_checked"] > 0

    def test_scan_timing(self, mock_config):
        """Test scan timing calculation"""
        scanner = DomainScanner(mock_config, test_mode=True)
        results = scanner.scan({"domain": "example.com"})
        
        assert "scan_time" in results
        assert isinstance(results["scan_time"], (int, float))

    def test_domain_data_structure(self, mock_config):
        """Test domain data structure"""
        scanner = DomainScanner(mock_config, test_mode=True)
        results = scanner.scan({"domain": "example.com"})
        
        # Check expected structure
        assert "domains" in results
        assert "summary" in results
        assert "domains_checked" in results["summary"]
        assert "ssl_certs_checked" in results["summary"]
        assert "dns_records_found" in results["summary"] 