import pytest
import os
import tempfile
from unittest.mock import Mock, patch
from utils.config import load_config

class TestConfig:
    def test_load_config_default(self):
        """Test loading default configuration"""
        config = load_config()
        
        # Should return a dictionary
        assert isinstance(config, dict)
        
        # Should have expected keys
        expected_keys = [
            "haveibeenpwned_api_key",
            "dehashed_api_key",
            "veriphone_api_key",
            "whoisxmlapi_key",
            "tineye_api_key",
            "peoplefinder_api_key",
            "courtlistener_api_key"
        ]
        
        for key in expected_keys:
            assert key in config

    @patch.dict(os.environ, {
        "HAVEIBEENPWNED_API_KEY": "test_key_1",
        "DEHASHED_API_KEY": "test_key_2"
    })
    def test_load_config_from_environment(self):
        """Test loading configuration from environment variables"""
        config = load_config()
        
        assert config["haveibeenpwned_api_key"] == "test_key_1"
        assert config["dehashed_api_key"] == "test_key_2"

    def test_load_config_from_file(self):
        """Test loading configuration from file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            config_content = """
            {
                "haveibeenpwned_api_key": "file_key_1",
                "dehashed_api_key": "file_key_2"
            }
            """
            tmp_file.write(config_content)
            tmp_file.flush()
            
            config = load_config(config_file=tmp_file.name)
            
            assert config["haveibeenpwned_api_key"] == "file_key_1"
            assert config["dehashed_api_key"] == "file_key_2"
            
            # Clean up
            os.unlink(tmp_file.name)

    def test_load_config_file_not_found(self):
        """Test handling of non-existent config file"""
        config = load_config(config_file="nonexistent.json")
        
        # Should return default config
        assert isinstance(config, dict)
        assert "haveibeenpwned_api_key" in config

    def test_load_config_invalid_json(self):
        """Test handling of invalid JSON in config file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            invalid_json = "{ invalid json content"
            tmp_file.write(invalid_json)
            tmp_file.flush()
            
            config = load_config(config_file=tmp_file.name)
            
            # Should return default config
            assert isinstance(config, dict)
            assert "haveibeenpwned_api_key" in config
            
            # Clean up
            os.unlink(tmp_file.name)

    def test_config_environment_override(self):
        """Test that environment variables override file config"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            config_content = """
            {
                "haveibeenpwned_api_key": "file_key",
                "dehashed_api_key": "file_key"
            }
            """
            tmp_file.write(config_content)
            tmp_file.flush()
            
            with patch.dict(os.environ, {"HAVEIBEENPWNED_API_KEY": "env_key"}):
                config = load_config(config_file=tmp_file.name)
                
                # Environment should override file
                assert config["haveibeenpwned_api_key"] == "env_key"
                # File value should remain for non-env keys
                assert config["dehashed_api_key"] == "file_key"
            
            # Clean up
            os.unlink(tmp_file.name)

    def test_config_default_values(self):
        """Test that default values are set correctly"""
        config = load_config()
        
        # Check that all expected keys exist
        expected_keys = [
            "haveibeenpwned_api_key",
            "dehashed_api_key",
            "veriphone_api_key",
            "whoisxmlapi_key",
            "tineye_api_key",
            "peoplefinder_api_key",
            "courtlistener_api_key"
        ]
        
        for key in expected_keys:
            assert key in config
            # Default values should be empty strings
            assert config[key] == ""

    def test_config_custom_path(self):
        """Test loading config from custom path"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = os.path.join(temp_dir, "custom_config.json")
            
            config_content = """
            {
                "custom_key": "custom_value",
                "haveibeenpwned_api_key": "custom_api_key"
            }
            """
            
            with open(config_file, 'w') as f:
                f.write(config_content)
            
            config = load_config(config_file=config_file)
            
            assert config["custom_key"] == "custom_value"
            assert config["haveibeenpwned_api_key"] == "custom_api_key"

    def test_config_merge_behavior(self):
        """Test that config properly merges defaults with custom values"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            config_content = """
            {
                "haveibeenpwned_api_key": "custom_key"
            }
            """
            tmp_file.write(config_content)
            tmp_file.flush()
            
            config = load_config(config_file=tmp_file.name)
            
            # Custom value should be set
            assert config["haveibeenpwned_api_key"] == "custom_key"
            # Default keys should still exist
            assert "dehashed_api_key" in config
            assert config["dehashed_api_key"] == ""
            
            # Clean up
            os.unlink(tmp_file.name) 