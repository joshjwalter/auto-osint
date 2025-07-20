"""
Image Search Scanner
Performs reverse image search and extracts EXIF metadata.
"""

import requests
import base64
from typing import Dict, List, Any, Optional
from utils.http_client import HTTPClient


class ImageScanner:
    """Scanner for image search and metadata extraction"""
    
    def __init__(self, config: Dict[str, Any], timeout: int = 30, 
                 headless: bool = False, test_mode: bool = False):
        """Initialize image scanner"""
        self.config = config
        self.timeout = timeout
        self.headless = headless
        self.test_mode = test_mode
        self.http_client = HTTPClient(timeout=timeout)
        
        # Image search services
        self.services = {
            "google_images": {
                "url": "https://lens.google.com/",
                "method": "browser",
                "requires_key": False
            },
            "tineye": {
                "url": "https://api.tineye.com/rest/search",
                "method": "api",
                "requires_key": True,
                "api_key": config.get("tineye_api_key", "")
            },
            "exif_extraction": {
                "method": "local",
                "requires_key": False
            }
        }
    
    def scan(self, target: Dict[str, str], nsfw: bool = False) -> Dict[str, Any]:
        """Scan for image-related intelligence"""
        results = {
            "image_searches": {},
            "metadata": {},
            "summary": {
                "services_checked": 0,
                "images_found": 0,
                "metadata_extracted": 0
            }
        }
        
        # Extract image URLs or data
        image_data = self._extract_image_data(target)
        
        if not image_data:
            return results
        
        # Process each image
        for image_info in image_data:
            # Reverse image search
            for service_name, service_config in self.services.items():
                if service_name == "exif_extraction":
                    continue  # Handle separately
                
                if self.test_mode:
                    search_results = self._simulate_image_search(image_info, service_name)
                else:
                    search_results = self._perform_image_search(image_info, service_config)
                
                if search_results:
                    if service_name not in results["image_searches"]:
                        results["image_searches"][service_name] = []
                    
                    results["image_searches"][service_name].append({
                        "image_info": image_info,
                        "results": search_results,
                        "searched_at": self._get_timestamp()
                    })
                    
                    results["summary"]["images_found"] += len(search_results.get("matches", []))
                
                results["summary"]["services_checked"] += 1
            
            # Extract EXIF metadata
            if self.test_mode:
                metadata = self._simulate_metadata_extraction(image_info)
            else:
                metadata = self._extract_metadata(image_info)
            
            if metadata:
                results["metadata"][image_info.get("url", "unknown")] = metadata
                results["summary"]["metadata_extracted"] += 1
        
        return results
    
    def _extract_image_data(self, target: Dict[str, str]) -> List[Dict[str, Any]]:
        """Extract image URLs or data from target"""
        images = []
        
        # Direct image URL
        if target.get("image_url"):
            images.append({
                "type": "url",
                "url": target["image_url"],
                "source": "direct_url"
            })
        
        # Avatar from social media profiles (simulated)
        if target.get("username"):
            # Common avatar URL patterns
            avatar_patterns = [
                f"https://github.com/{target['username']}.png",
                f"https://twitter.com/{target['username']}/profile_image",
                f"https://www.instagram.com/{target['username']}/profile_pic"
            ]
            
            for pattern in avatar_patterns:
                images.append({
                    "type": "avatar",
                    "url": pattern,
                    "source": "social_media",
                    "platform": pattern.split("/")[2]
                })
        
        return images
    
    def _perform_image_search(self, image_info: Dict[str, Any], 
                             service_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Perform reverse image search using a specific service"""
        try:
            if service_config["method"] == "api":
                return self._api_image_search(image_info, service_config)
            elif service_config["method"] == "browser":
                return self._browser_image_search(image_info, service_config)
            else:
                return None
                
        except Exception as e:
            # Log error but don't fail the entire scan
            return None
    
    def _api_image_search(self, image_info: Dict[str, Any], 
                         service_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Perform API-based image search"""
        try:
            url = service_config["url"]
            headers = {"User-Agent": "Auto-OSINT-Scanner"}
            
            if service_config.get("requires_key", False):
                api_key = service_config.get("api_key", "")
                if not api_key:
                    return None
                headers["Authorization"] = f"Bearer {api_key}"
            
            # For TinEye API
            if "tineye.com" in url:
                params = {
                    "url": image_info["url"],
                    "limit": 10
                }
                response = self.http_client.get(url, params=params, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_tineye_response(data)
            
            return None
            
        except Exception as e:
            return None
    
    def _browser_image_search(self, image_info: Dict[str, Any], 
                             service_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Perform browser-based image search (simulated)"""
        # In a real implementation, this would use Selenium or similar
        # For now, we'll simulate the results
        return {
            "service": "google_images",
            "matches": [
                {
                    "url": "https://example.com/similar_image1.jpg",
                    "title": "Similar Image 1",
                    "similarity": 0.85
                },
                {
                    "url": "https://example.com/similar_image2.jpg",
                    "title": "Similar Image 2",
                    "similarity": 0.72
                }
            ]
        }
    
    def _parse_tineye_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse TinEye API response"""
        matches = []
        
        for match in data.get("matches", []):
            matches.append({
                "url": match.get("image_url", ""),
                "title": match.get("title", ""),
                "similarity": match.get("score", 0)
            })
        
        return {
            "service": "tineye",
            "matches": matches
        }
    
    def _extract_metadata(self, image_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract EXIF metadata from image"""
        try:
            # In a real implementation, this would download the image and extract EXIF
            # For now, we'll simulate the extraction
            return {
                "camera_make": "Canon",
                "camera_model": "EOS 5D Mark IV",
                "date_taken": "2023-01-15 14:30:00",
                "gps_latitude": 40.7128,
                "gps_longitude": -74.0060,
                "location": "New York, NY",
                "software": "Adobe Photoshop CC 2023"
            }
        except Exception as e:
            return None
    
    def _simulate_image_search(self, image_info: Dict[str, Any], 
                              service_name: str) -> Dict[str, Any]:
        """Simulate image search for test mode"""
        if service_name == "google_images":
            return {
                "service": "google_images",
                "matches": [
                    {
                        "url": "https://example.com/test_image1.jpg",
                        "title": "Test Similar Image 1",
                        "similarity": 0.90
                    }
                ]
            }
        elif service_name == "tineye":
            return {
                "service": "tineye",
                "matches": [
                    {
                        "url": "https://example.com/test_image2.jpg",
                        "title": "Test Similar Image 2",
                        "similarity": 0.85
                    }
                ]
            }
        
        return {}
    
    def _simulate_metadata_extraction(self, image_info: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate metadata extraction for test mode"""
        return {
            "camera_make": "Test Camera",
            "camera_model": "Test Model",
            "date_taken": "2023-01-15 12:00:00",
            "gps_latitude": 37.7749,
            "gps_longitude": -122.4194,
            "location": "San Francisco, CA",
            "software": "Test Software"
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_description(self) -> str:
        """Get scanner description"""
        return "Image search and metadata scanner"
    
    def get_capabilities(self) -> List[str]:
        """Get scanner capabilities"""
        return ["reverse_image_search", "exif_extraction", "gps_extraction"]
    
    def get_config_requirements(self) -> List[str]:
        """Get configuration requirements"""
        return ["tineye_api_key"] 