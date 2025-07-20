"""
Report Generator
Handles report generation in multiple formats (JSON, Markdown, HTML)
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any
from utils.anonymizer import Anonymizer


class ReportGenerator:
    """Generate reports in various formats"""
    
    def __init__(self):
        """Initialize the report generator"""
        self.anonymizer = Anonymizer()
    
    def generate_report(self, results: List[Dict[str, Any]], format_type: str = "json", 
                       anonymize: bool = False) -> str:
        """Generate a report in the specified format"""
        if format_type == "json":
            return self._generate_json_report(results, anonymize)
        elif format_type == "markdown":
            return self._generate_markdown_report(results, anonymize)
        elif format_type == "html":
            return self._generate_html_report(results, anonymize)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _generate_json_report(self, results: List[Dict[str, Any]], anonymize: bool) -> str:
        """Generate JSON report"""
        report_data = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_targets": len(results),
                "anonymized": anonymize
            },
            "results": results
        }
        
        if anonymize:
            report_data = self.anonymizer.anonymize_data(report_data)
        
        return json.dumps(report_data, indent=2)
    
    def _generate_markdown_report(self, results: List[Dict[str, Any]], anonymize: bool) -> str:
        """Generate Markdown report"""
        md_content = []
        
        # Header
        md_content.append("# Auto OSINT Report")
        md_content.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md_content.append(f"**Total Targets:** {len(results)}")
        md_content.append(f"**Anonymized:** {anonymize}")
        md_content.append("")
        
        # Process each target
        for i, result in enumerate(results, 1):
            target = result.get("target", {})
            scan_results = result.get("results", {})
            
            md_content.append(f"## Target {i}")
            md_content.append("")
            
            # Target information
            md_content.append("### Target Information")
            for key, value in target.items():
                if value:
                    display_value = self.anonymizer.anonymize_value(value) if anonymize else value
                    md_content.append(f"- **{key.title()}:** {display_value}")
            md_content.append("")
            
            # Scan results
            md_content.append("### Scan Results")
            for search_type, scan_data in scan_results.items():
                md_content.append(f"#### {search_type.title()} Search")
                
                if isinstance(scan_data, dict) and scan_data.get("status") == "completed":
                    data = scan_data.get("data", {})
                    scan_time = scan_data.get("scan_time", 0)
                    
                    md_content.append(f"- **Status:** Completed")
                    md_content.append(f"- **Scan Time:** {scan_time:.2f}s")
                    
                    if data:
                        md_content.append("- **Findings:**")
                        self._add_findings_to_markdown(md_content, data, anonymize)
                    else:
                        md_content.append("- **Findings:** No results found")
                else:
                    error = scan_data.get("error", "Unknown error") if isinstance(scan_data, dict) else str(scan_data)
                    md_content.append(f"- **Status:** Failed")
                    md_content.append(f"- **Error:** {error}")
                
                md_content.append("")
        
        return "\n".join(md_content)
    
    def _generate_html_report(self, results: List[Dict[str, Any]], anonymize: bool) -> str:
        """Generate HTML report"""
        html_content = []
        
        # HTML header
        html_content.append("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auto OSINT Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }
        .target { margin: 20px 0; border: 1px solid #ddd; border-radius: 5px; }
        .target-header { background-color: #e0e0e0; padding: 10px; }
        .scan-result { margin: 10px; padding: 10px; border-left: 3px solid #007acc; }
        .success { border-left-color: #28a745; }
        .error { border-left-color: #dc3545; }
        .findings { margin-left: 20px; }
        .finding { margin: 5px 0; padding: 5px; background-color: #f8f9fa; }
    </style>
</head>
<body>
""")
        
        # Report header
        html_content.append(f"""
    <div class="header">
        <h1>Auto OSINT Report</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Total Targets:</strong> {len(results)}</p>
        <p><strong>Anonymized:</strong> {anonymize}</p>
    </div>
""")
        
        # Process each target
        for i, result in enumerate(results, 1):
            target = result.get("target", {})
            scan_results = result.get("results", {})
            
            html_content.append(f"""
    <div class="target">
        <div class="target-header">
            <h2>Target {i}</h2>
        </div>
        <div style="padding: 10px;">
            <h3>Target Information</h3>
            <ul>
""")
            
            # Target information
            for key, value in target.items():
                if value:
                    display_value = self.anonymizer.anonymize_value(value) if anonymize else value
                    html_content.append(f"                <li><strong>{key.title()}:</strong> {display_value}</li>")
            
            html_content.append("            </ul>")
            
            # Scan results
            html_content.append("            <h3>Scan Results</h3>")
            
            for search_type, scan_data in scan_results.items():
                status_class = "success" if isinstance(scan_data, dict) and scan_data.get("status") == "completed" else "error"
                
                html_content.append(f"""
            <div class="scan-result {status_class}">
                <h4>{search_type.title()} Search</h4>
""")
                
                if isinstance(scan_data, dict) and scan_data.get("status") == "completed":
                    data = scan_data.get("data", {})
                    scan_time = scan_data.get("scan_time", 0)
                    
                    html_content.append(f"""
                <p><strong>Status:</strong> Completed</p>
                <p><strong>Scan Time:</strong> {scan_time:.2f}s</p>
""")
                    
                    if data:
                        html_content.append("                <div class='findings'>")
                        html_content.append("                    <p><strong>Findings:</strong></p>")
                        self._add_findings_to_html(html_content, data, anonymize)
                        html_content.append("                </div>")
                    else:
                        html_content.append("                <p><strong>Findings:</strong> No results found</p>")
                else:
                    error = scan_data.get("error", "Unknown error") if isinstance(scan_data, dict) else str(scan_data)
                    html_content.append(f"""
                <p><strong>Status:</strong> Failed</p>
                <p><strong>Error:</strong> {error}</p>
""")
                
                html_content.append("            </div>")
            
            html_content.append("        </div>")
            html_content.append("    </div>")
        
        # HTML footer
        html_content.append("""
</body>
</html>
""")
        
        return "\n".join(html_content)
    
    def _add_findings_to_markdown(self, md_content: List[str], data: Dict[str, Any], anonymize: bool):
        """Add findings to markdown content"""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    md_content.append(f"  - **{key}:**")
                    self._add_findings_to_markdown(md_content, value, anonymize)
                else:
                    display_value = self.anonymizer.anonymize_value(str(value)) if anonymize else str(value)
                    md_content.append(f"  - **{key}:** {display_value}")
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    self._add_findings_to_markdown(md_content, item, anonymize)
                else:
                    display_value = self.anonymizer.anonymize_value(str(item)) if anonymize else str(item)
                    md_content.append(f"  - {display_value}")
    
    def _add_findings_to_html(self, html_content: List[str], data: Dict[str, Any], anonymize: bool):
        """Add findings to HTML content"""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    html_content.append(f"                    <div class='finding'>")
                    html_content.append(f"                        <strong>{key}:</strong>")
                    self._add_findings_to_html(html_content, value, anonymize)
                    html_content.append("                    </div>")
                else:
                    display_value = self.anonymizer.anonymize_value(str(value)) if anonymize else str(value)
                    html_content.append(f"                    <div class='finding'>")
                    html_content.append(f"                        <strong>{key}:</strong> {display_value}")
                    html_content.append("                    </div>")
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    self._add_findings_to_html(html_content, item, anonymize)
                else:
                    display_value = self.anonymizer.anonymize_value(str(item)) if anonymize else str(item)
                    html_content.append(f"                    <div class='finding'>")
                    html_content.append(f"                        - {display_value}")
                    html_content.append("                    </div>") 