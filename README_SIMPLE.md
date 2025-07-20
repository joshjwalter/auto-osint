# Auto OSINT - Quick Start Guide

A simple OSINT tool to gather information from various online sources.

## Quick Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the tool:**
```bash
python main.py --help
```

## Basic Usage

### Search for someone on social media:
```bash
python main.py --username johndoe --social
```

### Check if an email was in a data breach:
```bash
python main.py --email john.doe@example.com --breach
```

### Full scan of a domain:
```bash
python main.py --domain example.com --full
```

### Save results to a file:
```bash
python main.py --username testuser --social --save-report results.json
```

## Profile Management (NEW!)

### Save a profile for later:
```bash
python main.py --username johndoe --social --save-profile
```

### Update an existing profile:
```bash
python main.py --load-profile profile_johndoe --breach --update-profile
```

### List all your profiles:
```bash
python main.py --list-profiles
```

### Export a profile:
```bash
python main.py --export-profile profile_johndoe --format markdown
```

### Delete a profile:
```bash
python main.py --delete-profile profile_johndoe
```

## Common Commands

| Command | What it does |
|---------|-------------|
| `--username johndoe` | Search for username |
| `--email user@example.com` | Search for email |
| `--domain example.com` | Search for domain |
| `--social` | Check social media |
| `--breach` | Check data breaches |
| `--full` | Run all searches |
| `--test` | Use test mode (safe) |
| `--save-report file.json` | Save results |
| `--save-profile` | Save to profile file |
| `--load-profile name` | Load existing profile |
| `--list-profiles` | Show all profiles |

## Examples

**Check if someone exists on social media:**
```bash
python main.py --username johndoe --social --test
```

**Check if email was leaked:**
```bash
python main.py --email test@example.com --breach --test
```

**Full domain analysis:**
```bash
python main.py --domain example.com --full --test --save-report domain_report.json
```

**Build a profile over time:**
```bash
# First scan - social media
python main.py --username johndoe --social --save-profile

# Later - add breach data
python main.py --load-profile profile_johndoe --breach --update-profile

# Later - add domain info
python main.py --load-profile profile_johndoe --domain johndoe.com --update-profile
```

**Batch process multiple targets:**
```bash
# Create targets.txt with one target per line:
echo "johndoe" > targets.txt
echo "john.doe@example.com" >> targets.txt

python main.py --input-file targets.txt --social --breach
```

## Output Formats

- **JSON** (default): `--format json`
- **Markdown**: `--format markdown --save-report report.md`
- **HTML**: `--format html --save-report report.html`

## Test Mode

Use `--test` for safe testing with simulated results:
```bash
python main.py --username testuser --social --test
```

## Need Help?

```bash
python main.py --help
```

## What It Searches

- **Social Media**: Twitter, LinkedIn, Instagram, Facebook, GitHub, etc.
- **Data Breaches**: HaveIBeenPwned, Dehashed
- **Public Records**: Court records, people directories
- **Domain Info**: WHOIS, DNS, SSL certificates
- **Images**: Reverse image search, metadata
- **Location**: IP geolocation, phone location

## Privacy

Use `--anonymize` to hide sensitive data in reports:
```bash
python main.py --email user@example.com --social --anonymize
```

## Profile Files

Profiles are saved in the `profiles/` directory and contain:
- Target information
- All scan results
- Scan history
- Summary statistics
- Timestamps

You can build comprehensive files on people over time by running multiple scans and updating the same profile.

That's it! The tool is ready to use. 