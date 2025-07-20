# Auto OSINT - Comprehensive OSINT Intelligence Gathering Tool

A powerful Python-based OSINT (Open Source Intelligence) tool that automates the collection and analysis of publicly available information from various sources.

## Features

### 🔍 Search Capabilities
- **Social Media Search**: Check presence on Twitter, LinkedIn, Instagram, Facebook, TikTok, Reddit, GitHub, Quora, Medium
- **Data Breach Checks**: Verify email addresses against HaveIBeenPwned, Dehashed, and other breach databases
- **Public Records Lookup**: Search court records, people directories, and public databases
- **Image & Avatar Search**: Reverse image search and EXIF metadata extraction
- **Geolocation Inference**: Infer location from IP addresses, phone numbers, and domain data
- **Domain Intelligence**: WHOIS lookup, DNS records, SSL certificates, SPF records

### 📊 Output Formats
- **JSON**: Structured data output
- **Markdown**: Human-readable reports
- **HTML**: Web-friendly formatted reports
- **Anonymization**: Optional data anonymization for privacy

### 🛠️ Advanced Features
- **Batch Processing**: Process multiple targets from file
- **Modular Architecture**: Extensible scanner modules
- **Test Mode**: Sandbox testing with simulated results
- **Verbose Logging**: Detailed operation logging
- **Error Handling**: Robust error handling and recovery

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd Auto-OSINT
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Create configuration file** (optional):
```bash
python -c "from utils.config import create_default_config; create_default_config()"
```

## Quick Start

### Basic Usage

```bash
# Search for social media presence
python main.py --username johndoe --social

# Check for data breaches
python main.py --email john.doe@example.com --breach

# Full comprehensive scan
python main.py --email john.doe@example.com --full --save-report report.json

# Domain intelligence
python main.py --domain example.com --images --geolocation
```

### Advanced Usage

```bash
# Batch processing from file
python main.py --input-file targets.txt --social --public --verbose

# Test mode with simulated results
python main.py --username testuser --full --test

# Anonymized report
python main.py --email user@example.com --social --anonymize --save-report report.md --format markdown

# Custom timeout and verbose output
python main.py --domain example.com --timeout 60 --verbose --debug
```

## Command Line Options

### Input Options
- `--email`: Target email address
- `--username`: Target username
- `--full-name`: Target full name
- `--phone`: Target phone number
- `--domain`: Target domain
- `--input-file`: File containing multiple targets (one per line)

### Search Options
- `--social`: Social media search
- `--breach`: Data breach checks
- `--public`: Public records lookup
- `--images`: Image and avatar search
- `--geolocation`: Geolocation inference
- `--full`: Run all searches

### Output Options
- `--save-report`: Save report to file
- `--format`: Report format (json, markdown, html)
- `--anonymize`: Anonymize sensitive data in report

### Additional Options
- `--nsfw`: Include NSFW platforms in username search
- `--verbose`: Verbose output
- `--headless`: Run in headless mode
- `--debug`: Enable debug mode
- `--test`: Sandbox test mode
- `--timeout`: Request timeout in seconds

## Configuration

### API Keys

The application supports various API services. Add your API keys to the configuration:

```json
{
  "api_keys": {
    "haveibeenpwned_api_key": "your_hibp_key",
    "dehashed_api_key": "your_dehashed_key",
    "veriphone_api_key": "your_veriphone_key",
    "whoisxmlapi_key": "your_whoisxmlapi_key",
    "tineye_api_key": "your_tineye_key",
    "peoplefinder_api_key": "your_peoplefinder_key",
    "courtlistener_api_key": "your_courtlistener_key"
  }
}
```

### Environment Variables

You can also set API keys via environment variables:

```bash
export HIBP_API_KEY="your_key"
export DEHASHED_API_KEY="your_key"
export VERIPHONE_API_KEY="your_key"
# ... etc
```

## Project Structure

```
Auto-OSINT/
├── main.py                 # CLI entry point
├── core/                   # Core application logic
│   ├── scanner.py         # Main scanning engine
│   └── reporter.py        # Report generation
├── modules/               # Search modules
│   ├── social_media.py    # Social media search
│   ├── breach_check.py    # Data breach checks
│   ├── public_records.py  # Public records lookup
│   ├── image_search.py    # Image search & metadata
│   ├── geolocation.py     # Geolocation inference
│   └── domain_intelligence.py # Domain analysis
├── utils/                 # Utility modules
│   ├── http_client.py     # HTTP client
│   ├── logger.py          # Logging utility
│   ├── config.py          # Configuration management
│   └── anonymizer.py      # Data anonymization
├── requirements.txt       # Python dependencies
├── config.json           # Configuration file (optional)
└── README.md             # This file
```

## Examples

### Example 1: Social Media Search
```bash
python main.py --username johndoe --social --verbose
```

**Output**: JSON report showing presence on various social media platforms.

### Example 2: Data Breach Check
```bash
python main.py --email john.doe@example.com --breach --save-report breach_report.json
```

**Output**: JSON file with breach information from various databases.

### Example 3: Comprehensive Domain Analysis
```bash
python main.py --domain example.com --full --format html --save-report domain_report.html
```

**Output**: HTML report with WHOIS, DNS, SSL certificate, and geolocation information.

### Example 4: Batch Processing
```bash
# targets.txt contains:
# john.doe@example.com
# johndoe
# example.com

python main.py --input-file targets.txt --social --breach --public --save-report batch_report.json
```

**Output**: Comprehensive JSON report for all targets.

## API Services

The application integrates with various third-party services:

- **HaveIBeenPwned**: Data breach database
- **Dehashed**: Data breach and leak database
- **Veriphone**: Phone number validation and geolocation
- **WHOIS XML API**: Domain registration information
- **TinEye**: Reverse image search
- **PeopleFinder**: Public records and people search
- **CourtListener**: Court records and legal documents

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Security & Privacy

- **Data Anonymization**: Built-in anonymization for sensitive data
- **API Key Security**: Secure handling of API keys
- **Error Handling**: Robust error handling to prevent data leaks
- **Test Mode**: Safe testing environment with simulated results

## Legal Notice

This tool is designed for legitimate OSINT purposes only. Users are responsible for:

- Complying with applicable laws and regulations
- Respecting terms of service for target platforms
- Obtaining proper authorization before scanning
- Using the tool ethically and responsibly

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions:

1. Check the existing issues
2. Create a new issue with detailed information
3. Provide logs and configuration details when applicable

## Roadmap

- [ ] Additional social media platforms
- [ ] Advanced image analysis
- [ ] Machine learning integration
- [ ] Web interface
- [ ] Real-time monitoring
- [ ] Custom plugin system 