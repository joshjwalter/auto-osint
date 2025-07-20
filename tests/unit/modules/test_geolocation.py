import pytest
from unittest.mock import Mock, patch
from modules.geolocation import GeolocationScanner

class TestGeolocationScanner:
    def test_geolocation_scanner_initialization(self, mock_config):
        """Test geolocation scanner initializes correctly"""
        scanner = GeolocationScanner(mock_config)
        assert scanner.config == mock_config

    def test_extract_location_data(self, mock_config):
        """Test location data extraction from target data"""
        scanner = GeolocationScanner(mock_config)
        
        # Test IP address
        locations = scanner._extract_location_data({"ip": "192.168.1.1"})
        assert "192.168.1.1" in locations
        
        # Test phone number
        locations = scanner._extract_location_data({"phone": "+1-555-123-4567"})
        assert "+1-555-123-4567" in locations
        
        # Test domain
        locations = scanner._extract_location_data({"domain": "example.com"})
        assert "example.com" in locations

    def test_test_mode_simulation(self, mock_config):
        """Test that test mode properly simulates results"""
        scanner = GeolocationScanner(mock_config, test_mode=True)
        results = scanner.scan({"ip": "192.168.1.1"})
        
        assert "locations" in results
        assert "summary" in results
        assert results["summary"]["total_locations"] > 0

    @patch('modules.geolocation.GeolocationScanner._ip_geolocation')
    def test_ip_geolocation(self, mock_ip, mock_config):
        """Test IP geolocation functionality"""
        mock_ip.return_value = {
            "country": "United States",
            "city": "New York",
            "latitude": 40.7128,
            "longitude": -74.0060
        }
        
        scanner = GeolocationScanner(mock_config)
        results = scanner._ip_geolocation("192.168.1.1")
        
        assert "country" in results
        assert "city" in results
        assert "latitude" in results
        assert "longitude" in results

    @patch('modules.geolocation.GeolocationScanner._phone_geolocation')
    def test_phone_geolocation(self, mock_phone, mock_config):
        """Test phone geolocation functionality"""
        mock_phone.return_value = {
            "country": "United States",
            "carrier": "Test Carrier",
            "line_type": "mobile"
        }
        
        scanner = GeolocationScanner(mock_config)
        results = scanner._phone_geolocation("+1-555-123-4567")
        
        assert "country" in results
        assert "carrier" in results
        assert "line_type" in results

    @patch('modules.geolocation.GeolocationScanner._domain_geolocation')
    def test_domain_geolocation(self, mock_domain, mock_config):
        """Test domain geolocation functionality"""
        mock_domain.return_value = {
            "country": "United States",
            "city": "San Francisco",
            "latitude": 37.7749,
            "longitude": -122.4194
        }
        
        scanner = GeolocationScanner(mock_config)
        results = scanner._domain_geolocation("example.com")
        
        assert "country" in results
        assert "city" in results
        assert "latitude" in results
        assert "longitude" in results

    def test_empty_target_handling(self, mock_config):
        """Test handling of empty target data"""
        scanner = GeolocationScanner(mock_config, test_mode=True)
        
        results = scanner.scan({})
        assert results["summary"]["total_locations"] == 0
        assert "locations" in results

    def test_multiple_location_sources(self, mock_config):
        """Test handling of multiple location sources"""
        scanner = GeolocationScanner(mock_config, test_mode=True)
        
        # Target with multiple location sources
        target = {
            "ip": "192.168.1.1",
            "phone": "+1-555-123-4567",
            "domain": "example.com"
        }
        
        results = scanner.scan(target)
        assert results["summary"]["total_locations"] > 0

    def test_scan_timing(self, mock_config):
        """Test scan timing calculation"""
        scanner = GeolocationScanner(mock_config, test_mode=True)
        results = scanner.scan({"ip": "192.168.1.1"})
        
        assert "scan_time" in results
        assert isinstance(results["scan_time"], (int, float))

    def test_location_data_structure(self, mock_config):
        """Test location data structure"""
        scanner = GeolocationScanner(mock_config, test_mode=True)
        results = scanner.scan({"ip": "192.168.1.1"})
        
        # Check expected structure
        assert "locations" in results
        assert "summary" in results
        assert "total_locations" in results["summary"]
        assert "countries_found" in results["summary"]
        assert "cities_found" in results["summary"] 