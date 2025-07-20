"""
Main OSINT Scanner Engine
Coordinates all search modules and manages the scanning process.
"""

import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from modules.social_media import SocialMediaScanner
from modules.breach_check import BreachScanner
from modules.public_records import PublicRecordsScanner
from modules.image_search import ImageScanner
from modules.geolocation import GeolocationScanner
from modules.domain_intelligence import DomainScanner
from utils.logger import setup_logger


class OSINTScanner:
    """Main OSINT scanning engine that coordinates all search modules"""
    
    def __init__(self, config: Dict[str, Any], verbose: bool = False, 
                 debug: bool = False, timeout: int = 30, headless: bool = False, 
                 test_mode: bool = False):
        """Initialize the OSINT scanner"""
        self.config = config
        self.verbose = verbose
        self.debug = debug
        self.timeout = timeout
        self.headless = headless
        self.test_mode = test_mode
        
        # Setup logging
        self.logger = setup_logger(debug=debug, verbose=verbose)
        
        # Initialize scanners
        self.scanners = {
            "social": SocialMediaScanner(config, timeout, headless, test_mode),
            "breach": BreachScanner(config, timeout, test_mode),
            "public": PublicRecordsScanner(config, timeout, test_mode),
            "images": ImageScanner(config, timeout, headless, test_mode),
            "geolocation": GeolocationScanner(config, timeout, test_mode),
            "domain": DomainScanner(config, timeout, test_mode)
        }
        
        self.logger.info("OSINT Scanner initialized")
    
    def scan_target(self, target: Dict[str, str], search_types: List[str], 
                   nsfw: bool = False) -> Dict[str, Any]:
        """Scan a single target with specified search types"""
        results = {
            "target": target,
            "scan_time": datetime.now().isoformat(),
            "search_types": search_types,
            "results": {}
        }
        
        self.logger.info(f"Starting scan for target: {target}")
        
        for search_type in search_types:
            if search_type in self.scanners:
                try:
                    self.logger.info(f"Running {search_type} scan...")
                    start_time = time.time()
                    
                    scanner = self.scanners[search_type]
                    scan_results = scanner.scan(target, nsfw=nsfw)
                    
                    scan_time = time.time() - start_time
                    results["results"][search_type] = {
                        "data": scan_results,
                        "scan_time": scan_time,
                        "status": "completed"
                    }
                    
                    self.logger.info(f"{search_type} scan completed in {scan_time:.2f}s")
                    
                except Exception as e:
                    self.logger.error(f"Error in {search_type} scan: {e}")
                    results["results"][search_type] = {
                        "data": {},
                        "error": str(e),
                        "status": "failed"
                    }
            else:
                self.logger.warning(f"Unknown search type: {search_type}")
        
        return results
    
    def get_timestamp(self) -> str:
        """Get current timestamp"""
        return datetime.now().isoformat()
    
    def validate_target(self, target: Dict[str, str]) -> bool:
        """Validate target data"""
        required_fields = ["email", "username", "full_name", "phone", "domain"]
        return any(target.get(field) for field in required_fields)
    
    def get_available_scanners(self) -> List[str]:
        """Get list of available scanners"""
        return list(self.scanners.keys())
    
    def get_scanner_info(self, scanner_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific scanner"""
        if scanner_name in self.scanners:
            scanner = self.scanners[scanner_name]
            return {
                "name": scanner_name,
                "description": scanner.get_description(),
                "capabilities": scanner.get_capabilities(),
                "config_required": scanner.get_config_requirements()
            }
        return None 