"""
Configuration Utility
Handles loading and managing application configuration.
"""

import os
import json
from typing import Dict, Any
from pathlib import Path


def load_config(config_file: str = "config.json") -> Dict[str, Any]:
    """Load configuration from file or environment variables"""
    config = {}
    
    # Try to load from config file
    config_path = Path(config_file)
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load config file {config_file}: {e}")
    
    # Override with environment variables
    config.update(_load_env_config())
    
    return config


def _load_env_config() -> Dict[str, Any]:
    """Load configuration from environment variables"""
    env_config = {}
    
    # API keys
    env_mappings = {
        "HIBP_API_KEY": "haveibeenpwned_api_key",
        "DEHASHED_API_KEY": "dehashed_api_key",
        "VERIPHONE_API_KEY": "veriphone_api_key",
        "WHOISXMLAPI_KEY": "whoisxmlapi_key",
        "TINEYE_API_KEY": "tineye_api_key",
        "PEOPLEFINDER_API_KEY": "peoplefinder_api_key",
        "COURTLISTENER_API_KEY": "courtlistener_api_key"
    }
    
    for env_var, config_key in env_mappings.items():
        value = os.getenv(env_var)
        if value:
            env_config[config_key] = value
    
    return env_config


def save_config(config: Dict[str, Any], config_file: str = "config.json") -> bool:
    """Save configuration to file"""
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except IOError as e:
        print(f"Error saving config file {config_file}: {e}")
        return False


def create_default_config(config_file: str = "config.json") -> Dict[str, Any]:
    """Create a default configuration file"""
    default_config = {
        "api_keys": {
            "haveibeenpwned_api_key": "",
            "dehashed_api_key": "",
            "veriphone_api_key": "",
            "whoisxmlapi_key": "",
            "tineye_api_key": "",
            "peoplefinder_api_key": "",
            "courtlistener_api_key": ""
        },
        "settings": {
            "default_timeout": 30,
            "max_retries": 3,
            "user_agent": "Auto-OSINT-Scanner/1.0"
        },
        "features": {
            "enable_nsfw_search": False,
            "enable_test_mode": False,
            "enable_verbose_logging": False
        }
    }
    
    if save_config(default_config, config_file):
        print(f"Default configuration created: {config_file}")
        print("Please add your API keys to the configuration file.")
    
    return default_config


def get_api_key(config: Dict[str, Any], key_name: str) -> str:
    """Get API key from configuration"""
    # Try direct key first
    if key_name in config:
        return config[key_name]
    
    # Try nested structure
    if "api_keys" in config and key_name in config["api_keys"]:
        return config["api_keys"][key_name]
    
    return ""


def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Validate configuration and return missing keys"""
    required_keys = [
        "haveibeenpwned_api_key",
        "dehashed_api_key",
        "veriphone_api_key",
        "whoisxmlapi_key",
        "tineye_api_key",
        "peoplefinder_api_key",
        "courtlistener_api_key"
    ]
    
    missing_keys = []
    for key in required_keys:
        if not get_api_key(config, key):
            missing_keys.append(key)
    
    return {
        "valid": len(missing_keys) == 0,
        "missing_keys": missing_keys,
        "total_keys": len(required_keys),
        "available_keys": len(required_keys) - len(missing_keys)
    } 