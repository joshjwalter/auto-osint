"""
Social Media Scanner
Searches for presence on various social media platforms.
"""

import requests
import re
from typing import Dict, List, Any, Optional
from urllib.parse import quote_plus
from utils.http_client import HTTPClient


class SocialMediaScanner:
    """Scanner for social media presence"""
    
    def __init__(self, config: Dict[str, Any], timeout: int = 30, 
                 headless: bool = False, test_mode: bool = False):
        """Initialize social media scanner"""
        self.config = config
        self.timeout = timeout
        self.headless = headless
        self.test_mode = test_mode
        self.http_client = HTTPClient(timeout=timeout)
        
        # Social media platforms
        self.platforms = {
            "twitter": {
                "url": "https://twitter.com/{}",
                "check_method": "status_code",
                "success_codes": [200]
            },
            "linkedin": {
                "url": "https://www.linkedin.com/in/{}",
                "check_method": "status_code",
                "success_codes": [200]
            },
            "instagram": {
                "url": "https://www.instagram.com/{}",
                "check_method": "status_code",
                "success_codes": [200]
            },
            "facebook": {
                "url": "https://www.facebook.com/{}",
                "check_method": "status_code",
                "success_codes": [200]
            },
            "tiktok": {
                "url": "https://www.tiktok.com/@{}",
                "check_method": "status_code",
                "success_codes": [200]
            },
            "reddit": {
                "url": "https://www.reddit.com/user/{}",
                "check_method": "status_code",
                "success_codes": [200]
            },
            "github": {
                "url": "https://github.com/{}",
                "check_method": "status_code",
                "success_codes": [200]
            },
            "quora": {
                "url": "https://www.quora.com/profile/{}",
                "check_method": "status_code",
                "success_codes": [200]
            },
            "medium": {
                "url": "https://medium.com/@{}",
                "check_method": "status_code",
                "success_codes": [200]
            }
        }
    
    def scan(self, target: Dict[str, str], nsfw: bool = False) -> Dict[str, Any]:
        """Scan for social media presence"""
        results = {
            "platforms": {},
            "summary": {
                "total_platforms": len(self.platforms),
                "found_profiles": 0,
                "not_found": 0
            }
        }
        
        # Get usernames to check
        usernames = self._extract_usernames(target)
        
        if not usernames:
            return results
        
        # Check each platform for each username
        for username in usernames:
            for platform_name, platform_config in self.platforms.items():
                if self.test_mode:
                    # Simulate results in test mode
                    found = self._simulate_social_check(username, platform_name)
                else:
                    found = self._check_platform(username, platform_config)
                
                if platform_name not in results["platforms"]:
                    results["platforms"][platform_name] = []
                
                profile_info = {
                    "username": username,
                    "url": platform_config["url"].format(username),
                    "found": found,
                    "checked_at": self._get_timestamp()
                }
                
                results["platforms"][platform_name].append(profile_info)
                
                if found:
                    results["summary"]["found_profiles"] += 1
                else:
                    results["summary"]["not_found"] += 1
        
        return results
    
    def _extract_usernames(self, target: Dict[str, str]) -> List[str]:
        """Extract usernames from target data"""
        usernames = []
        
        # Direct username
        if target.get("username"):
            usernames.append(target["username"])
        
        # Extract from email
        if target.get("email"):
            email_username = target["email"].split("@")[0]
            usernames.append(email_username)
        
        # Extract from full name (create potential usernames)
        if target.get("full_name"):
            name_parts = target["full_name"].split()
            if len(name_parts) >= 2:
                # Common username patterns
                usernames.extend([
                    f"{name_parts[0].lower()}{name_parts[1].lower()}",
                    f"{name_parts[0].lower()}.{name_parts[1].lower()}",
                    f"{name_parts[0][0].lower()}{name_parts[1].lower()}",
                    f"{name_parts[0].lower()}_{name_parts[1].lower()}"
                ])
        
        # Remove duplicates and empty strings
        return list(set([u for u in usernames if u.strip()]))
    
    def _check_platform(self, username: str, platform_config: Dict[str, Any]) -> bool:
        """Check if username exists on a specific platform"""
        try:
            url = platform_config["url"].format(quote_plus(username))
            response = self.http_client.get(url)
            
            if platform_config["check_method"] == "status_code":
                return response.status_code in platform_config["success_codes"]
            
            return False
            
        except Exception as e:
            # Log error but don't fail the entire scan
            return False
    
    def _simulate_social_check(self, username: str, platform: str) -> bool:
        """Simulate social media check for test mode"""
        # Simulate some platforms being found
        test_found = ["twitter", "github", "linkedin"]
        return platform in test_found and len(username) > 3
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_description(self) -> str:
        """Get scanner description"""
        return "Social media presence scanner"
    
    def get_capabilities(self) -> List[str]:
        """Get scanner capabilities"""
        return list(self.platforms.keys())
    
    def get_config_requirements(self) -> List[str]:
        """Get configuration requirements"""
        return [] 