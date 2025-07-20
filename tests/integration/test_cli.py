import pytest
import subprocess
import json
import tempfile
import os
from pathlib import Path

class TestCLI:
    def test_help_command(self):
        """Test help command works"""
        result = subprocess.run(
            ["python", "main.py", "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "Auto OSINT" in result.stdout

    def test_test_mode_execution(self):
        """Test CLI execution in test mode"""
        result = subprocess.run(
            ["python", "main.py", "--username", "testuser", "--social", "--test"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def test_json_output_format(self, tmp_path):
        """Test JSON output generation"""
        output_file = tmp_path / "test_output.json"
        
        result = subprocess.run(
            ["python", "main.py", "--username", "testuser", "--social", 
             "--test", "--save-report", str(output_file)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert output_file.exists()
        
        # Verify JSON structure
        with open(output_file) as f:
            data = json.load(f)
            assert "report_metadata" in data
            assert "results" in data

    def test_markdown_output_format(self, tmp_path):
        """Test Markdown output generation"""
        output_file = tmp_path / "test_output.md"
        
        result = subprocess.run(
            ["python", "main.py", "--username", "testuser", "--social", 
             "--test", "--save-report", str(output_file), "--format", "markdown"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert output_file.exists()
        
        # Verify Markdown content
        with open(output_file) as f:
            content = f.read()
            assert "# OSINT Report" in content

    def test_html_output_format(self, tmp_path):
        """Test HTML output generation"""
        output_file = tmp_path / "test_output.html"
        
        result = subprocess.run(
            ["python", "main.py", "--username", "testuser", "--social", 
             "--test", "--save-report", str(output_file), "--format", "html"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert output_file.exists()
        
        # Verify HTML content
        with open(output_file) as f:
            content = f.read()
            assert "<!DOCTYPE html>" in content

    def test_profile_save_and_load(self, tmp_path):
        """Test profile save and load functionality"""
        # Save profile
        result = subprocess.run(
            ["python", "main.py", "--username", "testuser", "--social", 
             "--test", "--save-profile"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "Profile saved:" in result.stdout
        
        # Load and update profile
        result = subprocess.run(
            ["python", "main.py", "--load-profile", "profile_testuser", 
             "--breach", "--test", "--update-profile"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def test_list_profiles(self):
        """Test profile listing functionality"""
        result = subprocess.run(
            ["python", "main.py", "--list-profiles"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def test_export_profile(self, tmp_path):
        """Test profile export functionality"""
        output_file = tmp_path / "exported_profile.md"
        
        result = subprocess.run(
            ["python", "main.py", "--export-profile", "profile_testuser", 
             "--format", "markdown"],
            capture_output=True,
            text=True
        )
        
        # Should work if profile exists, or show error if not
        assert result.returncode in [0, 1]

    def test_multiple_search_types(self):
        """Test CLI with multiple search types"""
        result = subprocess.run(
            ["python", "main.py", "--username", "testuser", "--social", 
             "--breach", "--test"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def test_full_scan_mode(self):
        """Test full scan mode"""
        result = subprocess.run(
            ["python", "main.py", "--username", "testuser", "--full", "--test"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def test_anonymize_output(self, tmp_path):
        """Test anonymized output generation"""
        output_file = tmp_path / "anonymized_output.json"
        
        result = subprocess.run(
            ["python", "main.py", "--username", "testuser", "--email", "test@example.com",
             "--social", "--test", "--save-report", str(output_file), "--anonymize"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert output_file.exists()
        
        # Verify anonymization
        with open(output_file) as f:
            data = json.load(f)
            content = json.dumps(data)
            # Should not contain original email
            assert "test@example.com" not in content

    def test_invalid_arguments(self):
        """Test CLI with invalid arguments"""
        result = subprocess.run(
            ["python", "main.py", "--invalid-flag"],
            capture_output=True,
            text=True
        )
        assert result.returncode != 0

    def test_no_arguments(self):
        """Test CLI with no arguments"""
        result = subprocess.run(
            ["python", "main.py"],
            capture_output=True,
            text=True
        )
        assert result.returncode != 0
        assert "Error:" in result.stdout

    def test_verbose_mode(self):
        """Test CLI in verbose mode"""
        result = subprocess.run(
            ["python", "main.py", "--username", "testuser", "--social", 
             "--test", "--verbose"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def test_debug_mode(self):
        """Test CLI in debug mode"""
        result = subprocess.run(
            ["python", "main.py", "--username", "testuser", "--social", 
             "--test", "--debug"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0 