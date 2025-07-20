"""
Data Breach Scanner
Checks for email addresses in various data breach databases.
"""

import hashlib
import requests
from typing import Dict, List, Any, Optional
from utils.http_client import HTTPClient


class BreachScanner:
    """Scanner for data breach checks"""
    
    def __init__(self, config: Dict[str, Any], timeout: int = 30, test_mode: bool = False):
        """Initialize breach scanner"""
        self.config = config
        self.timeout = timeout
        self.test_mode = test_mode
        self.http_client = HTTPClient(timeout=timeout)
        
        # API endpoints for breach checks
        self.apis = {
            "haveibeenpwned": {
                "url": "https://haveibeenpwned.com/api/v3/breachedaccount/{}",
                "headers": {
                    "User-Agent": "Auto-OSINT-Scanner",
                    "hibp-api-key": config.get("haveibeenpwned_api_key", "")
                },
                "requires_key": True
            },
            "dehashed": {
                "url": "https://api.dehashed.com/search?q={}",
                "headers": {
                    "Authorization": f"Bearer {config.get('dehashed_api_key', '')}",
                    "Accept": "application/json"
                },
                "requires_key": True
            }
        }
    
    def scan(self, target: Dict[str, str], nsfw: bool = False) -> Dict[str, Any]:
        """Scan for data breaches"""
        results = {
            "breaches": {},
            "summary": {
                "total_breaches": 0,
                "total_records": 0,
                "apis_checked": 0
            }
        }
        
        # Get emails to check
        emails = self._extract_emails(target)
        
        if not emails:
            return results
        
        # Check each API for each email
        for email in emails:
            for api_name, api_config in self.apis.items():
                if self.test_mode:
                    # Simulate breach check in test mode
                    breach_data = self._simulate_breach_check(email, api_name)
                else:
                    breach_data = self._check_breach_api(email, api_config)
                
                if api_name not in results["breaches"]:
                    results["breaches"][api_name] = []
                
                if breach_data:
                    results["breaches"][api_name].append({
                        "email": email,
                        "breaches": breach_data,
                        "checked_at": self._get_timestamp()
                    })
                    
                    # Update summary
                    results["summary"]["total_breaches"] += len(breach_data)
                    for breach in breach_data:
                        results["summary"]["total_records"] += breach.get("pwn_count", 0)
                
                results["summary"]["apis_checked"] += 1
        
        return results
    
    def _extract_emails(self, target: Dict[str, str]) -> List[str]:
        """Extract email addresses from target data"""
        emails = []
        
        if target.get("email"):
            emails.append(target["email"])
        
        return emails
    
    def _check_breach_api(self, email: str, api_config: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """Check email against a breach API"""
        try:
            url = api_config["url"].format(email)
            headers = api_config.get("headers", {})
            
            # Skip if API key is required but not provided
            if api_config.get("requires_key", False):
                api_key = headers.get("hibp-api-key") or headers.get("Authorization")
                if not api_key or api_key == "Bearer ":
                    return None
            
            response = self.http_client.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if api_config["url"].startswith("https://haveibeenpwned.com"):
                    return self._parse_hibp_response(data)
                elif api_config["url"].startswith("https://api.dehashed.com"):
                    return self._parse_dehashed_response(data)
                
            elif response.status_code == 404:
                # No breaches found
                return []
            
            return None
            
        except Exception as e:
            # Log error but don't fail the entire scan
            return None
    
    def _parse_hibp_response(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse HaveIBeenPwned API response"""
        breaches = []
        for breach in data:
            breaches.append({
                "name": breach.get("Name", ""),
                "domain": breach.get("Domain", ""),
                "breach_date": breach.get("BreachDate", ""),
                "pwn_count": breach.get("PwnCount", 0),
                "description": breach.get("Description", ""),
                "data_classes": breach.get("DataClasses", [])
            })
        return breaches
    
    def _parse_dehashed_response(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse Dehashed API response"""
        breaches = []
        entries = data.get("entries", [])
        
        for entry in entries:
            breaches.append({
                "email": entry.get("email", ""),
                "username": entry.get("username", ""),
                "password": entry.get("password", ""),
                "hash": entry.get("hash", ""),
                "database": entry.get("database_name", ""),
                "breach_date": entry.get("date", "")
            })
        
        return breaches
    
    def _simulate_breach_check(self, email: str, api_name: str) -> List[Dict[str, Any]]:
        """Simulate breach check for test mode"""
        if api_name == "haveibeenpwned":
            return [
                {
                    "name": "Test Breach 1",
                    "domain": "test.com",
                    "breach_date": "2023-01-01",
                    "pwn_count": 1000,
                    "description": "Test data breach",
                    "data_classes": ["email", "password"]
                }
            ]
        elif api_name == "dehashed":
            return [
                {
                    "email": email,
                    "username": "testuser",
                    "password": "hashed_password",
                    "hash": "hash_value",
                    "database": "test_database",
                    "breach_date": "2023-01-01"
                }
            ]
        
        return []
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_description(self) -> str:
        """Get scanner description"""
        return "Data breach scanner"
    
    def get_capabilities(self) -> List[str]:
        """Get scanner capabilities"""
        return list(self.apis.keys())
    
    def get_config_requirements(self) -> List[str]:
        """Get configuration requirements"""
        return ["haveibeenpwned_api_key", "dehashed_api_key"] 