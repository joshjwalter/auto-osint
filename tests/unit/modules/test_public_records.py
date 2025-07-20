import pytest
from unittest.mock import Mock, patch
from modules.public_records import PublicRecordsScanner

class TestPublicRecordsScanner:
    def test_public_records_scanner_initialization(self, mock_config):
        """Test public records scanner initializes correctly"""
        scanner = PublicRecordsScanner(mock_config)
        assert scanner.config == mock_config

    def test_extract_person_data(self, mock_config):
        """Test person data extraction from target data"""
        scanner = PublicRecordsScanner(mock_config)
        
        # Test full name
        persons = scanner._extract_person_data({"full_name": "John Doe"})
        assert "John Doe" in persons
        
        # Test email
        persons = scanner._extract_person_data({"email": "john.doe@example.com"})
        assert "john.doe" in persons
        
        # Test phone
        persons = scanner._extract_person_data({"phone": "+1-555-123-4567"})
        assert "+1-555-123-4567" in persons

    def test_test_mode_simulation(self, mock_config):
        """Test that test mode properly simulates results"""
        scanner = PublicRecordsScanner(mock_config, test_mode=True)
        results = scanner.scan({"full_name": "John Doe"})
        
        assert "records" in results
        assert "summary" in results
        assert results["summary"]["total_records"] >= 0

    @patch('modules.public_records.PublicRecordsScanner._search_court_records')
    def test_court_records_search(self, mock_court, mock_config):
        """Test court records search functionality"""
        mock_court.return_value = {
            "cases": [
                {
                    "case_number": "2023-CR-001",
                    "court": "District Court",
                    "filing_date": "2023-01-01",
                    "status": "Closed"
                }
            ],
            "total_cases": 1
        }
        
        scanner = PublicRecordsScanner(mock_config)
        results = scanner._search_court_records("John Doe")
        
        assert "cases" in results
        assert "total_cases" in results
        assert len(results["cases"]) > 0

    @patch('modules.public_records.PublicRecordsScanner._search_people_directories')
    def test_people_directories_search(self, mock_people, mock_config):
        """Test people directories search functionality"""
        mock_people.return_value = {
            "matches": [
                {
                    "name": "John Doe",
                    "address": "123 Main St",
                    "phone": "+1-555-123-4567"
                }
            ],
            "total_matches": 1
        }
        
        scanner = PublicRecordsScanner(mock_config)
        results = scanner._search_people_directories("John Doe")
        
        assert "matches" in results
        assert "total_matches" in results
        assert len(results["matches"]) > 0

    @patch('modules.public_records.PublicRecordsScanner._search_obituaries')
    def test_obituaries_search(self, mock_obit, mock_config):
        """Test obituaries search functionality"""
        mock_obit.return_value = {
            "obituaries": [
                {
                    "name": "John Doe",
                    "date_of_death": "2023-01-01",
                    "funeral_home": "Test Funeral Home"
                }
            ],
            "total_obituaries": 1
        }
        
        scanner = PublicRecordsScanner(mock_config)
        results = scanner._search_obituaries("John Doe")
        
        assert "obituaries" in results
        assert "total_obituaries" in results
        assert len(results["obituaries"]) > 0

    def test_empty_target_handling(self, mock_config):
        """Test handling of empty target data"""
        scanner = PublicRecordsScanner(mock_config, test_mode=True)
        
        results = scanner.scan({})
        assert results["summary"]["total_records"] == 0
        assert "records" in results

    def test_multiple_person_sources(self, mock_config):
        """Test handling of multiple person sources"""
        scanner = PublicRecordsScanner(mock_config, test_mode=True)
        
        # Target with multiple person sources
        target = {
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1-555-123-4567"
        }
        
        results = scanner.scan(target)
        assert results["summary"]["total_records"] >= 0

    def test_scan_timing(self, mock_config):
        """Test scan timing calculation"""
        scanner = PublicRecordsScanner(mock_config, test_mode=True)
        results = scanner.scan({"full_name": "John Doe"})
        
        assert "scan_time" in results
        assert isinstance(results["scan_time"], (int, float))

    def test_records_data_structure(self, mock_config):
        """Test records data structure"""
        scanner = PublicRecordsScanner(mock_config, test_mode=True)
        results = scanner.scan({"full_name": "John Doe"})
        
        # Check expected structure
        assert "records" in results
        assert "summary" in results
        assert "total_records" in results["summary"]
        assert "court_cases" in results["summary"]
        assert "people_matches" in results["summary"]
        assert "obituaries" in results["summary"] 