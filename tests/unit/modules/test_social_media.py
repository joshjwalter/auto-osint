import pytest
from unittest.mock import Mock, patch
from modules.social_media import SocialMediaScanner

class TestSocialMediaScanner:
    def test_extract_usernames(self, mock_config):
        """Test username extraction from target data"""
        scanner = SocialMediaScanner(mock_config)
        
        # Test direct username
        usernames = scanner._extract_usernames({"username": "johndoe"})
        assert "johndoe" in usernames
        
        # Test email extraction
        usernames = scanner._extract_usernames({"email": "john.doe@example.com"})
        assert "john.doe" in usernames
        
        # Test full name extraction
        usernames = scanner._extract_usernames({"full_name": "John Doe"})
        assert "johndoe" in usernames
        assert "john.doe" in usernames

    @patch('modules.social_media.SocialMediaScanner._check_platform')
    def test_scan_with_mocked_platform_check(self, mock_check, mock_config):
        """Test social media scan with mocked platform checks"""
        mock_check.return_value = True
        
        scanner = SocialMediaScanner(mock_config)
        results = scanner.scan({"username": "testuser"})
        
        assert results["summary"]["found_profiles"] > 0
        assert "platforms" in results

    def test_test_mode_simulation(self, mock_config):
        """Test that test mode properly simulates results"""
        scanner = SocialMediaScanner(mock_config, test_mode=True)
        results = scanner.scan({"username": "testuser"})
        
        assert results["summary"]["found_profiles"] == 3
        assert results["platforms"]["twitter"][0]["found"] is True
        assert results["platforms"]["github"][0]["found"] is True

    def test_platform_check_methods(self, mock_config):
        """Test individual platform check methods"""
        scanner = SocialMediaScanner(mock_config, test_mode=True)
        
        # Test each platform check method exists
        assert hasattr(scanner, '_check_twitter')
        assert hasattr(scanner, '_check_linkedin')
        assert hasattr(scanner, '_check_github')
        assert hasattr(scanner, '_check_instagram')

    def test_nsfw_flag_handling(self, mock_config):
        """Test NSFW flag handling"""
        scanner = SocialMediaScanner(mock_config, test_mode=True)
        
        # Test without NSFW flag
        results = scanner.scan({"username": "testuser"}, nsfw=False)
        platforms = results["platforms"].keys()
        assert "onlyfans" not in platforms
        
        # Test with NSFW flag
        results = scanner.scan({"username": "testuser"}, nsfw=True)
        platforms = results["platforms"].keys()
        # In test mode, should include NSFW platforms

    def test_empty_target_handling(self, mock_config):
        """Test handling of empty target data"""
        scanner = SocialMediaScanner(mock_config, test_mode=True)
        
        results = scanner.scan({})
        assert results["summary"]["found_profiles"] == 0
        assert "platforms" in results

    def test_multiple_usernames(self, mock_config):
        """Test handling of multiple usernames"""
        scanner = SocialMediaScanner(mock_config, test_mode=True)
        
        # Target with multiple username sources
        target = {
            "username": "testuser",
            "email": "john.doe@example.com",
            "full_name": "John Doe"
        }
        
        results = scanner.scan(target)
        assert results["summary"]["found_profiles"] > 0

    def test_scan_timing(self, mock_config):
        """Test scan timing calculation"""
        scanner = SocialMediaScanner(mock_config, test_mode=True)
        results = scanner.scan({"username": "testuser"})
        
        assert "scan_time" in results
        assert isinstance(results["scan_time"], (int, float)) 