"""
Geolocation Scanner
Infers location from various data sources and metadata.
"""

import requests
import re
from typing import Dict, List, Any, Optional
from utils.http_client import HTTPClient


class GeolocationScanner:
    """Scanner for geolocation inference"""
    
    def __init__(self, config: Dict[str, Any], timeout: int = 30, test_mode: bool = False):
        """Initialize geolocation scanner"""
        self.config = config
        self.timeout = timeout
        self.test_mode = test_mode
        self.http_client = HTTPClient(timeout=timeout)
        
        # Geolocation services
        self.services = {
            "ip_geolocation": {
                "url": "https://ipapi.co/{}/json/",
                "method": "GET",
                "requires_key": False
            },
            "phone_geolocation": {
                "url": "https://api.veriphone.io/v2/verify",
                "method": "GET",
                "requires_key": True,
                "api_key": config.get("veriphone_api_key", "")
            },
            "domain_geolocation": {
                "url": "https://api.ipapi.com/{}",
                "method": "GET",
                "requires_key": False
            }
        }
    
    def scan(self, target: Dict[str, str], nsfw: bool = False) -> Dict[str, Any]:
        """Scan for geolocation intelligence"""
        results = {
            "locations": {},
            "summary": {
                "total_locations": 0,
                "services_checked": 0,
                "confidence_levels": {}
            }
        }
        
        # Extract location-related data
        location_data = self._extract_location_data(target)
        
        if not location_data:
            return results
        
        # Process each data type
        for data_type, data_value in location_data.items():
            if self.test_mode:
                location_info = self._simulate_geolocation(data_type, data_value)
            else:
                location_info = self._get_geolocation(data_type, data_value)
            
            if location_info:
                results["locations"][data_type] = {
                    "source": data_value,
                    "location": location_info,
                    "checked_at": self._get_timestamp()
                }
                
                results["summary"]["total_locations"] += 1
                
                # Track confidence levels
                confidence = location_info.get("confidence", "low")
                if confidence not in results["summary"]["confidence_levels"]:
                    results["summary"]["confidence_levels"][confidence] = 0
                results["summary"]["confidence_levels"][confidence] += 1
            
            results["summary"]["services_checked"] += 1
        
        return results
    
    def _extract_location_data(self, target: Dict[str, str]) -> Dict[str, str]:
        """Extract location-related data from target"""
        location_data = {}
        
        # IP address
        if target.get("ip"):
            location_data["ip"] = target["ip"]
        
        # Phone number
        if target.get("phone"):
            location_data["phone"] = target["phone"]
        
        # Domain
        if target.get("domain"):
            location_data["domain"] = target["domain"]
        
        # Extract IP from email domain (simulated)
        if target.get("email"):
            domain = target["email"].split("@")[1]
            location_data["email_domain"] = domain
        
        return location_data
    
    def _get_geolocation(self, data_type: str, data_value: str) -> Optional[Dict[str, Any]]:
        """Get geolocation information for a specific data type"""
        try:
            if data_type == "ip":
                return self._get_ip_geolocation(data_value)
            elif data_type == "phone":
                return self._get_phone_geolocation(data_value)
            elif data_type in ["domain", "email_domain"]:
                return self._get_domain_geolocation(data_value)
            else:
                return None
                
        except Exception as e:
            # Log error but don't fail the entire scan
            return None
    
    def _get_ip_geolocation(self, ip_address: str) -> Optional[Dict[str, Any]]:
        """Get geolocation from IP address"""
        try:
            url = self.services["ip_geolocation"]["url"].format(ip_address)
            response = self.http_client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "country": data.get("country_name", ""),
                    "region": data.get("region", ""),
                    "city": data.get("city", ""),
                    "latitude": data.get("latitude", 0),
                    "longitude": data.get("longitude", 0),
                    "timezone": data.get("timezone", ""),
                    "isp": data.get("org", ""),
                    "confidence": "high"
                }
            
            return None
            
        except Exception as e:
            return None
    
    def _get_phone_geolocation(self, phone_number: str) -> Optional[Dict[str, Any]]:
        """Get geolocation from phone number"""
        try:
            url = self.services["phone_geolocation"]["url"]
            params = {
                "phone": phone_number
            }
            
            api_key = self.services["phone_geolocation"].get("api_key", "")
            if api_key:
                params["key"] = api_key
            
            response = self.http_client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "country": data.get("country", ""),
                    "region": data.get("region", ""),
                    "carrier": data.get("carrier", ""),
                    "type": data.get("type", ""),
                    "confidence": "medium"
                }
            
            return None
            
        except Exception as e:
            return None
    
    def _get_domain_geolocation(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get geolocation from domain"""
        try:
            # First, resolve domain to IP
            import socket
            try:
                ip_address = socket.gethostbyname(domain)
                return self._get_ip_geolocation(ip_address)
            except socket.gaierror:
                return None
            
        except Exception as e:
            return None
    
    def _simulate_geolocation(self, data_type: str, data_value: str) -> Dict[str, Any]:
        """Simulate geolocation for test mode"""
        if data_type == "ip":
            return {
                "country": "United States",
                "region": "California",
                "city": "San Francisco",
                "latitude": 37.7749,
                "longitude": -122.4194,
                "timezone": "America/Los_Angeles",
                "isp": "Test ISP",
                "confidence": "high"
            }
        elif data_type == "phone":
            return {
                "country": "United States",
                "region": "New York",
                "carrier": "Test Carrier",
                "type": "mobile",
                "confidence": "medium"
            }
        elif data_type in ["domain", "email_domain"]:
            return {
                "country": "United States",
                "region": "Texas",
                "city": "Austin",
                "latitude": 30.2672,
                "longitude": -97.7431,
                "timezone": "America/Chicago",
                "isp": "Test Hosting",
                "confidence": "medium"
            }
        
        return None
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_description(self) -> str:
        """Get scanner description"""
        return "Geolocation inference scanner"
    
    def get_capabilities(self) -> List[str]:
        """Get scanner capabilities"""
        return ["ip_geolocation", "phone_geolocation", "domain_geolocation"]
    
    def get_config_requirements(self) -> List[str]:
        """Get configuration requirements"""
        return ["veriphone_api_key"] 