# Auto-OSINT Developer Guide

Welcome to the Auto-OSINT codebase! This guide will help you understand the architecture, coding practices, and how to contribute to this project.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Project Structure](#project-structure)
4. [Core Components](#core-components)
5. [Coding Standards](#coding-standards)
6. [Module Development](#module-development)
7. [Data Flow](#data-flow)
8. [Testing](#testing)
9. [API Integration](#api-integration)
10. [Common Patterns](#common-patterns)
11. [Development Workflow](#development-workflow)
12. [Troubleshooting](#troubleshooting)

## Project Overview

Auto-OSINT is a comprehensive Open Source Intelligence (OSINT) gathering tool that automates the collection and analysis of publicly available information. It's designed with modularity, extensibility, and ease of use in mind.

### Key Features
- **Modular Scanner System**: Each type of search (social media, breach checks, etc.) is a separate module
- **Multiple Output Formats**: JSON, Markdown, and HTML reports
- **Profile Management**: Save and update profiles over time
- **Test Mode**: Safe testing with simulated results
- **Data Anonymization**: Built-in privacy protection

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   CLI       │────▶│     Core     │────▶│   Modules   │
│  (main.py)  │     │  (scanner)   │     │  (scanners) │
└─────────────┘     └──────────────┘     └─────────────┘
                            │                     │
                            ▼                     ▼
                    ┌──────────────┐     ┌─────────────┐
                    │   Reporter   │     │    Utils    │
                    │              │     │             │
                    └──────────────┘     └─────────────┘
```

### Component Responsibilities

- **CLI (main.py)**: Handles command-line arguments and orchestrates the application
- **Core Scanner**: Coordinates all search modules and manages the scanning process
- **Modules**: Individual scanners for specific data sources (social media, breaches, etc.)
- **Reporter**: Generates reports in various formats
- **Utils**: Shared utilities (HTTP client, logging, config, anonymization)

## Project Structure

```
Auto-OSINT/
├── main.py                    # Entry point - CLI application
├── core/                      # Core application logic
│   ├── __init__.py
│   ├── scanner.py            # Main scanning engine
│   ├── reporter.py           # Report generation
│   └── profile_manager.py    # Profile management
├── modules/                   # Search modules
│   ├── __init__.py
│   ├── social_media.py       # Social media scanner
│   ├── breach_check.py       # Data breach scanner
│   ├── public_records.py     # Public records scanner
│   ├── image_search.py       # Image search & metadata
│   ├── geolocation.py        # Geolocation scanner
│   └── domain_intelligence.py # Domain analysis
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── http_client.py        # HTTP request handling
│   ├── logger.py             # Logging configuration
│   ├── config.py             # Configuration management
│   └── anonymizer.py         # Data anonymization
├── profiles/                  # Profile storage directory
├── requirements.txt          # Python dependencies
├── setup.py                  # Installation script
└── config.json              # Configuration file (optional)
```

## Core Components

### 1. CLI Entry Point (main.py)

The main entry point handles:
- Argument parsing using `argparse`
- Input validation
- Profile operations
- Scanner initialization
- Report generation

**Key Functions:**
- `create_parser()`: Defines all CLI arguments
- `validate_inputs()`: Ensures valid input
- `handle_profile_operations()`: Manages profile CRUD operations
- `main()`: Orchestrates the entire flow

### 2. Core Scanner (core/scanner.py)

The scanning engine that coordinates all modules:

```python
class OSINTScanner:
    def __init__(self, config, verbose, debug, timeout, headless, test_mode):
        # Initialize with configuration
        self.scanners = {
            "social": SocialMediaScanner(...),
            "breach": BreachScanner(...),
            # ... other scanners
        }
    
    def scan_target(self, target, search_types, nsfw=False):
        # Orchestrate scanning across modules
```

**Key Methods:**
- `scan_target()`: Main scanning method
- `validate_target()`: Validates target data
- `get_available_scanners()`: Lists available modules

### 3. Scanner Modules

Each scanner module follows a consistent pattern:

```python
class ScannerModule:
    def __init__(self, config, timeout, test_mode):
        # Initialize scanner
        
    def scan(self, target, nsfw=False):
        # Perform the scan
        return {
            "data": {...},
            "summary": {...}
        }
    
    def get_description(self):
        # Return module description
        
    def get_capabilities(self):
        # Return list of capabilities
        
    def get_config_requirements(self):
        # Return required API keys
```

#### Module Types:

1. **SocialMediaScanner**: Checks social media platforms
2. **BreachScanner**: Searches data breach databases
3. **PublicRecordsScanner**: Searches public records
4. **ImageScanner**: Reverse image search & EXIF extraction
5. **GeolocationScanner**: Location inference
6. **DomainScanner**: WHOIS, DNS, SSL analysis

### 4. Report Generator (core/reporter.py)

Handles report generation in multiple formats:

```python
class ReportGenerator:
    def generate_report(self, results, format_type="json", anonymize=False):
        if format_type == "json":
            return self._generate_json_report(results, anonymize)
        # ... other formats
```

**Supported Formats:**
- JSON: Structured data output
- Markdown: Human-readable format
- HTML: Web-friendly with styling

### 5. Profile Manager (core/profile_manager.py)

Manages persistent profiles:

```python
class ProfileManager:
    def save_profile(self, target, scan_results, profile_name=None):
        # Save or update profile
        
    def load_profile(self, profile_name):
        # Load existing profile
        
    def list_profiles(self):
        # List all profiles
```

**Profile Structure:**
```json
{
    "target": {...},
    "profile_name": "profile_username",
    "created_at": "ISO timestamp",
    "last_updated": "ISO timestamp",
    "scan_history": [...],
    "current_data": {...},
    "summary": {...}
}
```

## Coding Standards

### 1. Python Style

- **PEP 8 Compliance**: Follow PEP 8 style guide
- **Type Hints**: Use type hints for function parameters and returns
- **Docstrings**: Every module, class, and function must have docstrings

Example:
```python
from typing import Dict, List, Any, Optional

def scan_target(self, target: Dict[str, str], 
                search_types: List[str], 
                nsfw: bool = False) -> Dict[str, Any]:
    """
    Scan a single target with specified search types
    
    Args:
        target: Dictionary containing target information
        search_types: List of search types to perform
        nsfw: Include NSFW platforms
        
    Returns:
        Dictionary containing scan results
    """
```

### 2. Error Handling

- Never let a single module failure crash the entire scan
- Log errors appropriately
- Return empty/default results on failure

```python
try:
    result = self._perform_scan(target)
except Exception as e:
    self.logger.error(f"Scan failed: {e}")
    return {"data": {}, "error": str(e), "status": "failed"}
```

### 3. Configuration Management

- All API keys stored in config or environment variables
- Never hardcode sensitive information
- Gracefully handle missing configuration

```python
api_key = self.config.get("api_key", "")
if not api_key and self.requires_key:
    return None  # Skip this service
```

## Module Development

### Creating a New Scanner Module

1. **Create the module file** in `modules/`:
```python
# modules/new_scanner.py
from typing import Dict, List, Any
from utils.http_client import HTTPClient

class NewScanner:
    def __init__(self, config: Dict[str, Any], timeout: int = 30, 
                 test_mode: bool = False):
        self.config = config
        self.timeout = timeout
        self.test_mode = test_mode
        self.http_client = HTTPClient(timeout=timeout)
    
    def scan(self, target: Dict[str, str], nsfw: bool = False) -> Dict[str, Any]:
        results = {
            "data": {},
            "summary": {}
        }
        
        if self.test_mode:
            return self._simulate_scan(target)
        
        # Implement actual scanning logic
        return results
    
    def _simulate_scan(self, target: Dict[str, str]) -> Dict[str, Any]:
        # Return test data
        return {"data": {"test": True}, "summary": {"count": 1}}
    
    def get_description(self) -> str:
        return "Description of what this scanner does"
    
    def get_capabilities(self) -> List[str]:
        return ["capability1", "capability2"]
    
    def get_config_requirements(self) -> List[str]:
        return ["api_key_name"]
```

2. **Register in the scanner engine** (core/scanner.py):
```python
from modules.new_scanner import NewScanner

# In __init__:
self.scanners = {
    # ... existing scanners
    "new": NewScanner(config, timeout, test_mode)
}
```

3. **Add to CLI arguments** (main.py):
```python
search_group.add_argument("--new", action="store_true", 
                         help="New scanner description")
```

### Module Best Practices

1. **Extract Target Data**: Create helper methods to extract relevant data
```python
def _extract_emails(self, target: Dict[str, str]) -> List[str]:
    emails = []
    if target.get("email"):
        emails.append(target["email"])
    return emails
```

2. **Consistent Result Format**: Always return consistent structure
```python
return {
    "platforms": {...},     # Main data
    "summary": {           # Summary statistics
        "total": 0,
        "found": 0
    }
}
```

3. **Test Mode**: Always implement test mode
```python
if self.test_mode:
    return self._simulate_results(target)
```

## Data Flow

### 1. Input Processing
```
CLI Arguments → Target Extraction → Validation → Scanner
```

### 2. Scanning Process
```
Scanner → Module Selection → Parallel Execution → Result Aggregation
```

### 3. Output Generation
```
Raw Results → Anonymization (optional) → Formatting → Output
```

### Example Flow:
```python
# 1. User input
python main.py --email user@example.com --social --breach

# 2. Target created
target = {"email": "user@example.com"}

# 3. Scanners executed
results = {
    "social": social_scanner.scan(target),
    "breach": breach_scanner.scan(target)
}

# 4. Report generated
report = reporter.generate_report(results, format="json")
```

## Testing

### 1. Test Mode

Always test with `--test` flag first:
```bash
python main.py --username testuser --full --test
```

### 2. Unit Testing Pattern

```python
# tests/test_social_media.py
import unittest
from modules.social_media import SocialMediaScanner

class TestSocialMediaScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = SocialMediaScanner({}, test_mode=True)
    
    def test_scan_with_username(self):
        target = {"username": "testuser"}
        result = self.scanner.scan(target)
        self.assertIn("platforms", result)
        self.assertIn("summary", result)
```

### 3. Integration Testing

Test the full flow:
```python
def test_full_scan():
    # Test CLI → Scanner → Report
    result = subprocess.run([
        "python", "main.py", 
        "--username", "testuser", 
        "--social", "--test"
    ], capture_output=True)
    assert result.returncode == 0
```

## API Integration

### 1. Adding New APIs

1. **Add to config template**:
```python
# utils/config.py
"api_keys": {
    "new_api_key": "",
    # ...
}
```

2. **Environment variable mapping**:
```python
env_mappings = {
    "NEW_API_KEY": "new_api_key",
    # ...
}
```

3. **Use in module**:
```python
api_key = self.config.get("new_api_key", "")
if not api_key:
    return None  # Skip if no key
```

### 2. API Request Pattern

```python
def _check_api(self, query: str) -> Optional[Dict[str, Any]]:
    try:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = self.http_client.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {}  # Not found
        else:
            return None  # Error
            
    except Exception as e:
        self.logger.error(f"API error: {e}")
        return None
```

## Common Patterns

### 1. Username Extraction
```python
def _extract_usernames(self, target: Dict[str, str]) -> List[str]:
    usernames = []
    
    # Direct username
    if target.get("username"):
        usernames.append(target["username"])
    
    # From email
    if target.get("email"):
        usernames.append(target["email"].split("@")[0])
    
    # From full name
    if target.get("full_name"):
        names = target["full_name"].split()
        usernames.extend([
            f"{names[0].lower()}{names[1].lower()}",
            f"{names[0].lower()}.{names[1].lower()}"
        ])
    
    return list(set(usernames))
```

### 2. Platform Checking
```python
platforms = {
    "twitter": "https://twitter.com/{}",
    "github": "https://github.com/{}"
}

for platform, url_template in platforms.items():
    url = url_template.format(username)
    if self._check_url_exists(url):
        results[platform] = {"found": True, "url": url}
```

### 3. Summary Generation
```python
summary = {
    "total_checked": len(platforms),
    "found": sum(1 for p in results if p["found"]),
    "not_found": sum(1 for p in results if not p["found"])
}
```

## Development Workflow

### 1. Setting Up Development Environment

```bash
# Clone repository
git clone <repository-url>
cd Auto-OSINT

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run setup
python setup.py

# Create config
cp config.json.example config.json
# Edit config.json with your API keys
```

### 2. Development Cycle

1. **Create feature branch**:
```bash
git checkout -b feature/new-scanner
```

2. **Develop with test mode**:
```bash
python main.py --username test --new --test --verbose --debug
```

3. **Test thoroughly**:
```bash
# Test individual module
python -m pytest tests/test_new_scanner.py

# Test integration
python main.py --username realuser --new --timeout 60
```

4. **Update documentation**:
- Add to README.md
- Update this guide if needed
- Add docstrings

### 3. Code Review Checklist

- [ ] Type hints added
- [ ] Docstrings complete
- [ ] Error handling implemented
- [ ] Test mode works
- [ ] No hardcoded secrets
- [ ] Follows existing patterns
- [ ] Documentation updated

## Troubleshooting

### Common Issues

1. **Module Import Errors**
```python
# Ensure __init__.py exists in all directories
# Use absolute imports: from modules.scanner import Scanner
```

2. **API Key Issues**
```python
# Check config loading
config = load_config()
print(config.get("api_keys", {}))

# Check environment variables
import os
print(os.getenv("HIBP_API_KEY"))
```

3. **Timeout Issues**
```python
# Increase timeout for slow APIs
scanner = Scanner(config, timeout=60)
```

4. **Test Mode Not Working**
```python
# Ensure test_mode is passed through
def __init__(self, config, test_mode=False):
    self.test_mode = test_mode
    
# Check in scan method
if self.test_mode:
    return self._simulate_scan()
```

### Debugging Tips

1. **Enable debug logging**:
```bash
python main.py --username test --social --debug --verbose
```

2. **Print scanner state**:
```python
print(f"Scanner config: {self.config}")
print(f"Test mode: {self.test_mode}")
```

3. **Check HTTP responses**:
```python
response = self.http_client.get(url)
print(f"Status: {response.status_code}")
print(f"Headers: {response.headers}")
print(f"Body: {response.text[:200]}")
```

## Contributing

1. **Follow the patterns**: Look at existing modules for examples
2. **Add tests**: Every new feature needs tests
3. **Document everything**: Update relevant documentation
4. **Handle errors gracefully**: Never crash the entire scan
5. **Respect privacy**: Follow data protection best practices

## Summary

The Auto-OSINT codebase is designed to be:
- **Modular**: Easy to add new scanners
- **Robust**: Handles failures gracefully
- **Extensible**: Clear patterns for enhancement
- **User-friendly**: Comprehensive CLI and output options

When in doubt, look at existing modules for patterns and examples. The codebase prioritizes consistency and maintainability over clever solutions.

Happy coding! 🚀
