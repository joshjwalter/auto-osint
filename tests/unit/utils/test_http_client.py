import pytest
from unittest.mock import Mock, patch
from utils.http_client import HTTPClient

class TestHTTPClient:
    def test_http_client_initialization(self):
        """Test HTTP client initializes correctly"""
        client = HTTPClient()
        assert client is not None

    @patch('requests.get')
    def test_get_request_success(self, mock_get):
        """Test successful GET request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_get.return_value = mock_response
        
        client = HTTPClient()
        response = client.get("https://api.example.com/test")
        
        assert response.status_code == 200
        assert response.json() == {"success": True}

    @patch('requests.get')
    def test_get_request_with_headers(self, mock_get):
        """Test GET request with custom headers"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_get.return_value = mock_response
        
        client = HTTPClient()
        headers = {"Authorization": "Bearer token"}
        response = client.get("https://api.example.com/test", headers=headers)
        
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[1]["headers"] == headers

    @patch('requests.get')
    def test_get_request_retry_on_failure(self, mock_get):
        """Test retry mechanism on request failure"""
        mock_response_fail = Mock()
        mock_response_fail.status_code = 500
        
        mock_response_success = Mock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = {"success": True}
        
        mock_get.side_effect = [mock_response_fail, mock_response_success]
        
        client = HTTPClient(max_retries=2)
        response = client.get("https://api.example.com/test")
        
        assert response.status_code == 200
        assert mock_get.call_count == 2

    @patch('requests.get')
    def test_get_request_max_retries_exceeded(self, mock_get):
        """Test behavior when max retries exceeded"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        client = HTTPClient(max_retries=2)
        response = client.get("https://api.example.com/test")
        
        assert response.status_code == 500
        assert mock_get.call_count == 3  # Initial + 2 retries

    @patch('requests.post')
    def test_post_request_success(self, mock_post):
        """Test successful POST request"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 123}
        mock_post.return_value = mock_response
        
        client = HTTPClient()
        data = {"name": "test"}
        response = client.post("https://api.example.com/test", data=data)
        
        assert response.status_code == 201
        assert response.json() == {"id": 123}

    def test_timeout_handling(self):
        """Test timeout configuration"""
        client = HTTPClient(timeout=30)
        assert client.timeout == 30

    def test_user_agent_setting(self):
        """Test user agent configuration"""
        client = HTTPClient(user_agent="TestBot/1.0")
        assert "User-Agent" in client.session.headers
        assert client.session.headers["User-Agent"] == "TestBot/1.0"

    @patch('requests.get')
    def test_session_reuse(self, mock_get):
        """Test that session is reused across requests"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_get.return_value = mock_response
        
        client = HTTPClient()
        
        # Make multiple requests
        client.get("https://api.example.com/test1")
        client.get("https://api.example.com/test2")
        
        # Session should be reused
        assert mock_get.call_count == 2

    def test_invalid_url_handling(self):
        """Test handling of invalid URLs"""
        client = HTTPClient()
        
        with pytest.raises(Exception):
            client.get("invalid-url")

    @patch('requests.get')
    def test_connection_error_handling(self, mock_get):
        """Test handling of connection errors"""
        from requests.exceptions import ConnectionError
        
        mock_get.side_effect = ConnectionError("Connection failed")
        
        client = HTTPClient(max_retries=1)
        
        with pytest.raises(ConnectionError):
            client.get("https://api.example.com/test") 