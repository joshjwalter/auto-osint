# Auto OSINT - Help

Simple OSINT tool to gather information from various online sources.

## Usage
```
python main.py [OPTIONS]
```

## Options
```
--username USER     Search for username
--email EMAIL       Search for email address  
--domain DOMAIN     Search for domain
--social            Check social media
--breach            Check data breaches
--full              Run all searches
--test              Use test mode (simulated results)
--save-report FILE  Save results to file
--format FORMAT     Output format (json/markdown/html)
--anonymize         Hide sensitive data in reports
--help              Show this help message
```

## Profile Management
```
--save-profile      Save results to profile
--load-profile NAME Load existing profile
--update-profile    Update loaded profile
--list-profiles     List all profiles
--export-profile    Export profile to file
--delete-profile    Delete a profile
```

## Examples
```bash
# Search social media
python main.py --username johndoe --social

# Check email breaches
python main.py --email user@example.com --breach

# Full domain scan
python main.py --domain example.com --full

# Save results
python main.py --username testuser --social --save-report results.json

# Build profile over time
python main.py --username johndoe --social --save-profile
python main.py --load-profile profile_johndoe --breach --update-profile
```

## Test Mode
Use --test for safe testing with simulated results.
