"""
Public Records Scanner
Searches public records, court records, and people directories.
"""

import requests
from typing import Dict, List, Any, Optional
from utils.http_client import HTTPClient


class PublicRecordsScanner:
    """Scanner for public records"""
    
    def __init__(self, config: Dict[str, Any], timeout: int = 30, test_mode: bool = False):
        """Initialize public records scanner"""
        self.config = config
        self.timeout = timeout
        self.test_mode = test_mode
        self.http_client = HTTPClient(timeout=timeout)
        
        # Public records sources
        self.sources = {
            "people_finder": {
                "url": "https://api.peoplefinder.com/search",
                "method": "POST",
                "requires_key": True,
                "api_key": config.get("peoplefinder_api_key", "")
            },
            "court_records": {
                "url": "https://api.courtlistener.com/rest/v3/search/",
                "method": "GET",
                "requires_key": True,
                "api_key": config.get("courtlistener_api_key", "")
            }
        }
    
    def scan(self, target: Dict[str, str], nsfw: bool = False) -> Dict[str, Any]:
        """Scan public records"""
        results = {
            "records": {},
            "summary": {
                "total_records": 0,
                "sources_checked": 0
            }
        }
        
        # Extract search terms
        search_terms = self._extract_search_terms(target)
        
        if not search_terms:
            return results
        
        # Search each source
        for source_name, source_config in self.sources.items():
            if self.test_mode:
                # Simulate public records search in test mode
                records = self._simulate_public_search(search_terms, source_name)
            else:
                records = self._search_public_records(search_terms, source_config)
            
            if records:
                results["records"][source_name] = records
                results["summary"]["total_records"] += len(records)
            
            results["summary"]["sources_checked"] += 1
        
        return results
    
    def _extract_search_terms(self, target: Dict[str, str]) -> List[Dict[str, str]]:
        """Extract search terms from target data"""
        terms = []
        
        # Full name search
        if target.get("full_name"):
            terms.append({
                "type": "name",
                "value": target["full_name"],
                "source": "full_name"
            })
        
        # Phone number search
        if target.get("phone"):
            terms.append({
                "type": "phone",
                "value": target["phone"],
                "source": "phone"
            })
        
        # Email search
        if target.get("email"):
            terms.append({
                "type": "email",
                "value": target["email"],
                "source": "email"
            })
        
        return terms
    
    def _search_public_records(self, search_terms: List[Dict[str, str]], 
                              source_config: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """Search public records using a specific source"""
        try:
            # Skip if API key is required but not provided
            if source_config.get("requires_key", False):
                api_key = source_config.get("api_key", "")
                if not api_key:
                    return None
            
            records = []
            
            for term in search_terms:
                if source_config["method"] == "GET":
                    params = {
                        "q": term["value"],
                        "format": "json"
                    }
                    if source_config.get("api_key"):
                        params["key"] = source_config["api_key"]
                    
                    response = self.http_client.get(source_config["url"], params=params)
                    
                elif source_config["method"] == "POST":
                    data = {
                        "query": term["value"],
                        "type": term["type"]
                    }
                    if source_config.get("api_key"):
                        data["api_key"] = source_config["api_key"]
                    
                    response = self.http_client.post(source_config["url"], json=data)
                
                if response.status_code == 200:
                    data = response.json()
                    parsed_records = self._parse_records_response(data, term)
                    records.extend(parsed_records)
            
            return records
            
        except Exception as e:
            # Log error but don't fail the entire scan
            return None
    
    def _parse_records_response(self, data: Dict[str, Any], search_term: Dict[str, str]) -> List[Dict[str, Any]]:
        """Parse public records API response"""
        records = []
        
        # Generic parsing - adapt based on actual API response structure
        if isinstance(data, dict):
            results = data.get("results", data.get("data", []))
            
            for result in results:
                record = {
                    "search_term": search_term["value"],
                    "search_type": search_term["type"],
                    "source": search_term["source"],
                    "data": result,
                    "found_at": self._get_timestamp()
                }
                records.append(record)
        
        return records
    
    def _simulate_public_search(self, search_terms: List[Dict[str, str]], 
                               source_name: str) -> List[Dict[str, Any]]:
        """Simulate public records search for test mode"""
        records = []
        
        for term in search_terms:
            if source_name == "people_finder":
                records.append({
                    "search_term": term["value"],
                    "search_type": term["type"],
                    "source": term["source"],
                    "data": {
                        "name": "John Doe",
                        "address": "123 Main St, Anytown, USA",
                        "phone": "+1-555-123-4567",
                        "email": "john.doe@example.com",
                        "age": "35",
                        "relatives": ["Jane Doe", "Bob Doe"]
                    },
                    "found_at": self._get_timestamp()
                })
            elif source_name == "court_records":
                records.append({
                    "search_term": term["value"],
                    "search_type": term["type"],
                    "source": term["source"],
                    "data": {
                        "case_number": "CV-2023-001",
                        "court": "Superior Court",
                        "filing_date": "2023-01-15",
                        "case_type": "Civil",
                        "parties": ["John Doe", "Jane Smith"],
                        "status": "Closed"
                    },
                    "found_at": self._get_timestamp()
                })
        
        return records
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_description(self) -> str:
        """Get scanner description"""
        return "Public records scanner"
    
    def get_capabilities(self) -> List[str]:
        """Get scanner capabilities"""
        return list(self.sources.keys())
    
    def get_config_requirements(self) -> List[str]:
        """Get configuration requirements"""
        return ["peoplefinder_api_key", "courtlistener_api_key"] 