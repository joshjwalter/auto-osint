#!/usr/bin/env python3
"""
Setup script for Auto OSINT
Handles installation and initial configuration.
"""

import os
import sys
import subprocess
from pathlib import Path
from utils.config import create_default_config


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✓ Python version: {sys.version.split()[0]}")


def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)


def create_config():
    """Create default configuration file"""
    print("Creating configuration file...")
    try:
        config = create_default_config()
        print("✓ Configuration file created: config.json")
        print("  Please add your API keys to config.json")
    except Exception as e:
        print(f"Warning: Could not create config file: {e}")


def create_example_files():
    """Create example files"""
    print("Creating example files...")
    
    # Create example targets file
    example_targets = """# Example targets file
# One target per line
john.doe@example.com
johndoe
example.com
"""
    
    try:
        with open("example_targets.txt", "w") as f:
            f.write(example_targets)
        print("✓ Example targets file created: example_targets.txt")
    except Exception as e:
        print(f"Warning: Could not create example targets file: {e}")


def test_installation():
    """Test the installation"""
    print("Testing installation...")
    try:
        result = subprocess.run([sys.executable, "main.py", "--help"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Installation test passed")
        else:
            print("✗ Installation test failed")
            print(result.stderr)
    except Exception as e:
        print(f"Warning: Could not test installation: {e}")


def main():
    """Main setup function"""
    print("Auto OSINT Setup")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Create configuration
    create_config()
    
    # Create example files
    create_example_files()
    
    # Test installation
    test_installation()
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("\nNext steps:")
    print("1. Add your API keys to config.json")
    print("2. Run: python main.py --help")
    print("3. Try: python main.py --username testuser --social --test")
    print("\nFor more information, see README.md")


if __name__ == "__main__":
    main() 