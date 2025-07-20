import pytest
import json
from unittest.mock import Mock, patch
from core.reporter import ReportGenerator

class TestReportGenerator:
    def test_reporter_initialization(self):
        """Test reporter initializes correctly"""
        reporter = ReportGenerator()
        assert reporter is not None

    def test_generate_json_report(self, sample_scan_results):
        """Test JSON report generation"""
        reporter = ReportGenerator()
        report = reporter.generate_report([sample_scan_results], format_type="json")
        
        # Should return JSON string
        assert isinstance(report, str)
        data = json.loads(report)
        assert "report_metadata" in data
        assert "results" in data

    def test_generate_markdown_report(self, sample_scan_results):
        """Test Markdown report generation"""
        reporter = ReportGenerator()
        report = reporter.generate_report([sample_scan_results], format_type="markdown")
        
        # Should return markdown string
        assert isinstance(report, str)
        assert "# OSINT Report" in report
        assert "testuser" in report

    def test_generate_html_report(self, sample_scan_results):
        """Test HTML report generation"""
        reporter = ReportGenerator()
        report = reporter.generate_report([sample_scan_results], format_type="html")
        
        # Should return HTML string
        assert isinstance(report, str)
        assert "<!DOCTYPE html>" in report
        assert "testuser" in report

    def test_anonymize_report(self, sample_scan_results):
        """Test report anonymization"""
        reporter = ReportGenerator()
        report = reporter.generate_report([sample_scan_results], format_type="json", anonymize=True)
        
        data = json.loads(report)
        # Check that sensitive data is anonymized
        assert "testuser" not in str(data)

    def test_multiple_targets_report(self, sample_scan_results):
        """Test report generation with multiple targets"""
        reporter = ReportGenerator()
        
        # Create multiple scan results
        scan_results = [
            sample_scan_results,
            {
                "target": {"email": "user2@example.com"},
                "scan_time": "2023-01-01T00:00:00",
                "results": {"breach": {"data": {}, "status": "completed"}}
            }
        ]
        
        report = reporter.generate_report(scan_results, format_type="json")
        data = json.loads(report)
        
        assert len(data["results"]) == 2

    def test_invalid_format_type(self, sample_scan_results):
        """Test handling of invalid format type"""
        reporter = ReportGenerator()
        
        with pytest.raises(ValueError):
            reporter.generate_report([sample_scan_results], format_type="invalid")

    def test_empty_results(self):
        """Test handling of empty results"""
        reporter = ReportGenerator()
        report = reporter.generate_report([], format_type="json")
        
        data = json.loads(report)
        assert "report_metadata" in data
        assert len(data["results"]) == 0 