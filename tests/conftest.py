import pytest
import json
from pathlib import Path
from unittest.mock import MagicMock

@pytest.fixture
def mock_config():
    """Provide mock configuration for tests"""
    return {
        "haveibeenpwned_api_key": "test_key",
        "dehashed_api_key": "test_key",
        "veriphone_api_key": "test_key",
        "whoisxmlapi_key": "test_key",
        "tineye_api_key": "test_key",
        "peoplefinder_api_key": "test_key",
        "courtlistener_api_key": "test_key"
    }

@pytest.fixture
def sample_target():
    """Provide sample target data"""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "phone": "+1-555-123-4567",
        "domain": "example.com"
    }

@pytest.fixture
def mock_http_response():
    """Mock HTTP response"""
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {"success": True}
    return response

@pytest.fixture
def sample_scan_results():
    """Provide sample scan results"""
    return {
        "target": {"username": "testuser"},
        "scan_time": "2023-01-01T00:00:00",
        "results": {
            "social": {
                "data": {
                    "platforms": {
                        "twitter": [{"username": "testuser", "found": True}],
                        "github": [{"username": "testuser", "found": True}]
                    },
                    "summary": {"found_profiles": 2}
                },
                "status": "completed",
                "scan_time": 1.0
            }
        }
    } 