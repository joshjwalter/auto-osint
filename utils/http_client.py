"""
HTTP Client Utility
Provides a centralized HTTP client for making requests with proper error handling.
"""

import requests
import time
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class HTTPClient:
    """HTTP client with retry logic and proper error handling"""
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        """Initialize HTTP client"""
        self.timeout = timeout
        self.session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set default headers
        self.session.headers.update({
            "User-Agent": "Auto-OSINT-Scanner/1.0"
        })
    
    def get(self, url: str, params: Optional[Dict[str, Any]] = None, 
            headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """Make a GET request"""
        try:
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            return response
        except requests.exceptions.RequestException as e:
            # Re-raise with more context
            raise requests.exceptions.RequestException(f"GET request failed for {url}: {e}")
    
    def post(self, url: str, data: Optional[Dict[str, Any]] = None,
             json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """Make a POST request"""
        try:
            response = self.session.post(
                url,
                data=data,
                json=json,
                headers=headers,
                timeout=self.timeout
            )
            return response
        except requests.exceptions.RequestException as e:
            # Re-raise with more context
            raise requests.exceptions.RequestException(f"POST request failed for {url}: {e}")
    
    def head(self, url: str, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """Make a HEAD request"""
        try:
            response = self.session.head(
                url,
                headers=headers,
                timeout=self.timeout
            )
            return response
        except requests.exceptions.RequestException as e:
            # Re-raise with more context
            raise requests.exceptions.RequestException(f"HEAD request failed for {url}: {e}")
    
    def close(self):
        """Close the session"""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close() 