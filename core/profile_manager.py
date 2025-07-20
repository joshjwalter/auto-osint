"""
Profile Manager
Handles saving and loading target profiles for building comprehensive OSINT files.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class ProfileManager:
    """Manages target profiles and their associated data"""
    
    def __init__(self, profiles_dir: str = "profiles"):
        """Initialize profile manager"""
        self.profiles_dir = Path(profiles_dir)
        self.profiles_dir.mkdir(exist_ok=True)
    
    def save_profile(self, target: Dict[str, str], scan_results: Dict[str, Any], 
                    profile_name: Optional[str] = None) -> str:
        """Save a target profile with scan results"""
        
        # Generate profile name if not provided
        if not profile_name:
            profile_name = self._generate_profile_name(target)
        
        # Create profile data structure
        profile_data = {
            "target": target,
            "profile_name": profile_name,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "scan_history": [],
            "current_data": scan_results,
            "summary": self._generate_summary(scan_results)
        }
        
        # Load existing profile if it exists
        existing_profile = self.load_profile(profile_name)
        if existing_profile:
            # Merge with existing data
            profile_data = self._merge_profiles(existing_profile, profile_data)
        
        # Save to file
        profile_file = self.profiles_dir / f"{profile_name}.json"
        with open(profile_file, 'w') as f:
            json.dump(profile_data, f, indent=2)
        
        return profile_name
    
    def load_profile(self, profile_name: str) -> Optional[Dict[str, Any]]:
        """Load a target profile"""
        profile_file = self.profiles_dir / f"{profile_name}.json"
        
        if not profile_file.exists():
            return None
        
        try:
            with open(profile_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def list_profiles(self) -> List[Dict[str, Any]]:
        """List all available profiles"""
        profiles = []
        
        for profile_file in self.profiles_dir.glob("*.json"):
            try:
                with open(profile_file, 'r') as f:
                    profile_data = json.load(f)
                    profiles.append({
                        "name": profile_data.get("profile_name", profile_file.stem),
                        "target": profile_data.get("target", {}),
                        "created_at": profile_data.get("created_at", ""),
                        "last_updated": profile_data.get("last_updated", ""),
                        "scan_count": len(profile_data.get("scan_history", [])),
                        "file_path": str(profile_file)
                    })
            except (json.JSONDecodeError, IOError):
                continue
        
        return sorted(profiles, key=lambda x: x["last_updated"], reverse=True)
    
    def delete_profile(self, profile_name: str) -> bool:
        """Delete a target profile"""
        profile_file = self.profiles_dir / f"{profile_name}.json"
        
        if profile_file.exists():
            profile_file.unlink()
            return True
        
        return False
    
    def export_profile(self, profile_name: str, format_type: str = "json") -> Optional[str]:
        """Export a profile in various formats"""
        profile_data = self.load_profile(profile_name)
        
        if not profile_data:
            return None
        
        if format_type == "json":
            return json.dumps(profile_data, indent=2)
        elif format_type == "markdown":
            return self._export_to_markdown(profile_data)
        elif format_type == "html":
            return self._export_to_html(profile_data)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _generate_profile_name(self, target: Dict[str, str]) -> str:
        """Generate a unique profile name from target data"""
        # Try to use username first
        if target.get("username"):
            return f"profile_{target['username']}"
        
        # Use email username
        if target.get("email"):
            email_username = target["email"].split("@")[0]
            return f"profile_{email_username}"
        
        # Use domain
        if target.get("domain"):
            return f"profile_{target['domain']}"
        
        # Use full name
        if target.get("full_name"):
            name_parts = target["full_name"].split()
            if len(name_parts) >= 2:
                return f"profile_{name_parts[0]}_{name_parts[1]}"
        
        # Fallback to timestamp
        return f"profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def _generate_summary(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of scan results"""
        summary = {
            "total_scans": 0,
            "social_media_profiles": 0,
            "breaches_found": 0,
            "public_records": 0,
            "domains_checked": 0,
            "images_found": 0,
            "locations_found": 0
        }
        
        for search_type, scan_data in scan_results.get("results", {}).items():
            if isinstance(scan_data, dict) and scan_data.get("status") == "completed":
                summary["total_scans"] += 1
                
                data = scan_data.get("data", {})
                
                if search_type == "social":
                    summary["social_media_profiles"] = data.get("summary", {}).get("found_profiles", 0)
                elif search_type == "breach":
                    summary["breaches_found"] = data.get("summary", {}).get("total_breaches", 0)
                elif search_type == "public":
                    summary["public_records"] = data.get("summary", {}).get("total_records", 0)
                elif search_type == "domain":
                    summary["domains_checked"] = data.get("summary", {}).get("domains_checked", 0)
                elif search_type == "images":
                    summary["images_found"] = data.get("summary", {}).get("images_found", 0)
                elif search_type == "geolocation":
                    summary["locations_found"] = data.get("summary", {}).get("total_locations", 0)
        
        return summary
    
    def _merge_profiles(self, existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
        """Merge new scan results with existing profile data"""
        merged = existing.copy()
        
        # Update timestamps
        merged["last_updated"] = new["last_updated"]
        
        # Add to scan history
        scan_entry = {
            "timestamp": new["last_updated"],
            "scan_results": new["current_data"]
        }
        merged["scan_history"].append(scan_entry)
        
        # Merge current data
        merged["current_data"] = self._merge_scan_results(
            merged.get("current_data", {}),
            new["current_data"]
        )
        
        # Update summary
        merged["summary"] = self._generate_summary(merged["current_data"])
        
        return merged
    
    def _merge_scan_results(self, existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
        """Merge scan results, combining data from both"""
        merged = existing.copy()
        
        # Merge results by search type
        for search_type, new_data in new.get("results", {}).items():
            if search_type not in merged.get("results", {}):
                merged.setdefault("results", {})[search_type] = new_data
            else:
                # Merge data within the same search type
                existing_data = merged["results"][search_type]
                if isinstance(existing_data, dict) and isinstance(new_data, dict):
                    merged["results"][search_type] = self._merge_search_data(existing_data, new_data)
        
        return merged
    
    def _merge_search_data(self, existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
        """Merge data from the same search type"""
        merged = existing.copy()
        
        # Merge data field
        if "data" in new and "data" in existing:
            merged["data"] = self._merge_data_structures(existing["data"], new["data"])
        
        # Keep the most recent scan time
        if "scan_time" in new:
            merged["scan_time"] = new["scan_time"]
        
        # Keep the most recent status
        if "status" in new:
            merged["status"] = new["status"]
        
        return merged
    
    def _merge_data_structures(self, existing: Any, new: Any) -> Any:
        """Recursively merge data structures"""
        if isinstance(existing, dict) and isinstance(new, dict):
            merged = existing.copy()
            for key, value in new.items():
                if key in merged:
                    merged[key] = self._merge_data_structures(merged[key], value)
                else:
                    merged[key] = value
            return merged
        elif isinstance(existing, list) and isinstance(new, list):
            # For lists, we might want to append or merge based on content
            # For now, just append new items
            return existing + new
        else:
            # For other types, prefer new value
            return new
    
    def _export_to_markdown(self, profile_data: Dict[str, Any]) -> str:
        """Export profile to markdown format"""
        md_content = []
        
        target = profile_data.get("target", {})
        current_data = profile_data.get("current_data", {})
        
        md_content.append(f"# OSINT Profile: {profile_data.get('profile_name', 'Unknown')}")
        md_content.append(f"**Created:** {profile_data.get('created_at', 'Unknown')}")
        md_content.append(f"**Last Updated:** {profile_data.get('last_updated', 'Unknown')}")
        md_content.append("")
        
        # Target information
        md_content.append("## Target Information")
        for key, value in target.items():
            if value:
                md_content.append(f"- **{key.title()}:** {value}")
        md_content.append("")
        
        # Summary
        summary = profile_data.get("summary", {})
        md_content.append("## Summary")
        md_content.append(f"- **Total Scans:** {summary.get('total_scans', 0)}")
        md_content.append(f"- **Social Media Profiles:** {summary.get('social_media_profiles', 0)}")
        md_content.append(f"- **Data Breaches:** {summary.get('breaches_found', 0)}")
        md_content.append(f"- **Public Records:** {summary.get('public_records', 0)}")
        md_content.append(f"- **Domains Checked:** {summary.get('domains_checked', 0)}")
        md_content.append(f"- **Images Found:** {summary.get('images_found', 0)}")
        md_content.append(f"- **Locations Found:** {summary.get('locations_found', 0)}")
        md_content.append("")
        
        # Scan history
        scan_history = profile_data.get("scan_history", [])
        if scan_history:
            md_content.append("## Scan History")
            for i, scan in enumerate(scan_history, 1):
                md_content.append(f"### Scan {i} - {scan.get('timestamp', 'Unknown')}")
                md_content.append("")
        
        return "\n".join(md_content)
    
    def _export_to_html(self, profile_data: Dict[str, Any]) -> str:
        """Export profile to HTML format"""
        html_content = []
        
        target = profile_data.get("target", {})
        
        html_content.append("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OSINT Profile</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }
        .section { margin: 20px 0; }
        .summary { background-color: #e8f4f8; padding: 15px; border-radius: 5px; }
    </style>
</head>
<body>
""")
        
        html_content.append(f"""
    <div class="header">
        <h1>OSINT Profile: {profile_data.get('profile_name', 'Unknown')}</h1>
        <p><strong>Created:</strong> {profile_data.get('created_at', 'Unknown')}</p>
        <p><strong>Last Updated:</strong> {profile_data.get('last_updated', 'Unknown')}</p>
    </div>
""")
        
        # Target information
        html_content.append('<div class="section">')
        html_content.append('<h2>Target Information</h2>')
        html_content.append('<ul>')
        for key, value in target.items():
            if value:
                html_content.append(f'<li><strong>{key.title()}:</strong> {value}</li>')
        html_content.append('</ul>')
        html_content.append('</div>')
        
        # Summary
        summary = profile_data.get("summary", {})
        html_content.append('<div class="section summary">')
        html_content.append('<h2>Summary</h2>')
        html_content.append('<ul>')
        html_content.append(f'<li><strong>Total Scans:</strong> {summary.get("total_scans", 0)}</li>')
        html_content.append(f'<li><strong>Social Media Profiles:</strong> {summary.get("social_media_profiles", 0)}</li>')
        html_content.append(f'<li><strong>Data Breaches:</strong> {summary.get("breaches_found", 0)}</li>')
        html_content.append(f'<li><strong>Public Records:</strong> {summary.get("public_records", 0)}</li>')
        html_content.append(f'<li><strong>Domains Checked:</strong> {summary.get("domains_checked", 0)}</li>')
        html_content.append(f'<li><strong>Images Found:</strong> {summary.get("images_found", 0)}</li>')
        html_content.append(f'<li><strong>Locations Found:</strong> {summary.get("locations_found", 0)}</li>')
        html_content.append('</ul>')
        html_content.append('</div>')
        
        html_content.append("</body></html>")
        
        return "\n".join(html_content) 