import pytest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
from core.profile_manager import ProfileManager

class TestProfileManager:
    @pytest.fixture
    def temp_profiles_dir(self):
        """Create temporary directory for profile tests"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_profile_manager_initialization(self, temp_profiles_dir):
        """Test profile manager initializes correctly"""
        manager = ProfileManager(temp_profiles_dir)
        assert manager.profiles_dir == Path(temp_profiles_dir)
        assert manager.profiles_dir.exists()

    def test_save_profile(self, temp_profiles_dir, sample_scan_results):
        """Test saving a profile"""
        manager = ProfileManager(temp_profiles_dir)
        target = {"username": "testuser"}
        
        profile_name = manager.save_profile(target, sample_scan_results)
        
        assert profile_name == "profile_testuser"
        profile_file = Path(temp_profiles_dir) / f"{profile_name}.json"
        assert profile_file.exists()

    def test_load_profile(self, temp_profiles_dir, sample_scan_results):
        """Test loading a profile"""
        manager = ProfileManager(temp_profiles_dir)
        target = {"username": "testuser"}
        
        # Save profile first
        profile_name = manager.save_profile(target, sample_scan_results)
        
        # Load profile
        loaded_profile = manager.load_profile(profile_name)
        
        assert loaded_profile is not None
        assert loaded_profile["target"] == target
        assert "current_data" in loaded_profile

    def test_list_profiles(self, temp_profiles_dir, sample_scan_results):
        """Test listing profiles"""
        manager = ProfileManager(temp_profiles_dir)
        
        # Save a few profiles
        manager.save_profile({"username": "user1"}, sample_scan_results)
        manager.save_profile({"username": "user2"}, sample_scan_results)
        
        profiles = manager.list_profiles()
        
        assert len(profiles) == 2
        assert any(p["name"] == "profile_user1" for p in profiles)
        assert any(p["name"] == "profile_user2" for p in profiles)

    def test_delete_profile(self, temp_profiles_dir, sample_scan_results):
        """Test deleting a profile"""
        manager = ProfileManager(temp_profiles_dir)
        target = {"username": "testuser"}
        
        # Save profile first
        profile_name = manager.save_profile(target, sample_scan_results)
        
        # Delete profile
        result = manager.delete_profile(profile_name)
        
        assert result is True
        profiles = manager.list_profiles()
        assert len(profiles) == 0

    def test_export_profile(self, temp_profiles_dir, sample_scan_results):
        """Test exporting a profile"""
        manager = ProfileManager(temp_profiles_dir)
        target = {"username": "testuser"}
        
        # Save profile first
        profile_name = manager.save_profile(target, sample_scan_results)
        
        # Export in different formats
        json_export = manager.export_profile(profile_name, "json")
        markdown_export = manager.export_profile(profile_name, "markdown")
        html_export = manager.export_profile(profile_name, "html")
        
        assert json_export is not None
        assert markdown_export is not None
        assert html_export is not None
        assert "testuser" in markdown_export
        assert "<!DOCTYPE html>" in html_export

    def test_merge_profiles(self, temp_profiles_dir, sample_scan_results):
        """Test merging profile data"""
        manager = ProfileManager(temp_profiles_dir)
        target = {"username": "testuser"}
        
        # Save initial profile
        profile_name = manager.save_profile(target, sample_scan_results)
        
        # Create new scan results
        new_results = {
            "target": target,
            "scan_time": "2023-01-02T00:00:00",
            "results": {
                "breach": {
                    "data": {"breaches": []},
                    "status": "completed",
                    "scan_time": 0.5
                }
            }
        }
        
        # Update profile
        manager.save_profile(target, new_results, profile_name)
        
        # Load merged profile
        loaded_profile = manager.load_profile(profile_name)
        
        assert "social" in loaded_profile["current_data"]["results"]
        assert "breach" in loaded_profile["current_data"]["results"]
        assert len(loaded_profile["scan_history"]) == 2

    def test_generate_profile_name(self, temp_profiles_dir):
        """Test profile name generation"""
        manager = ProfileManager(temp_profiles_dir)
        
        # Test username
        name = manager._generate_profile_name({"username": "testuser"})
        assert name == "profile_testuser"
        
        # Test email
        name = manager._generate_profile_name({"email": "test@example.com"})
        assert name == "profile_test"
        
        # Test domain
        name = manager._generate_profile_name({"domain": "example.com"})
        assert name == "profile_example.com"

    def test_profile_not_found(self, temp_profiles_dir):
        """Test handling of non-existent profile"""
        manager = ProfileManager(temp_profiles_dir)
        
        # Try to load non-existent profile
        profile = manager.load_profile("nonexistent")
        assert profile is None
        
        # Try to delete non-existent profile
        result = manager.delete_profile("nonexistent")
        assert result is False 