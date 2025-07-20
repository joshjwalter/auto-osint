#!/usr/bin/env python3
"""
Auto OSINT CLI Application
A comprehensive OSINT tool for gathering intelligence from various sources.
"""

import argparse
import sys
import json
from pathlib import Path
from core.scanner import OSINTScanner
from core.reporter import ReportGenerator
from core.profile_manager import ProfileManager
from utils.config import load_config


def create_parser():
    """Create and configure the argument parser"""
    parser = argparse.ArgumentParser(
        description="Auto OSINT - Comprehensive OSINT Intelligence Gathering Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --email john.doe@example.com --social --breach
  python main.py --username johndoe --full --save-report report.json
  python main.py --input-file targets.txt --social --public --verbose
  python main.py --domain example.com --images --geolocation
  python main.py --username johndoe --social --save-profile
  python main.py --load-profile profile_johndoe --social --update-profile
        """
    )
    
    # Input arguments
    input_group = parser.add_argument_group("Input Options")
    input_group.add_argument("--email", help="Target email address")
    input_group.add_argument("--username", help="Target username")
    input_group.add_argument("--full-name", help="Target full name")
    input_group.add_argument("--phone", help="Target phone number")
    input_group.add_argument("--domain", help="Target domain")
    input_group.add_argument("--input-file", help="File containing multiple targets (one per line)")
    
    # Profile management
    profile_group = parser.add_argument_group("Profile Management")
    profile_group.add_argument("--save-profile", action="store_true", help="Save results to profile file")
    profile_group.add_argument("--profile-name", help="Custom name for profile file")
    profile_group.add_argument("--load-profile", help="Load existing profile for updates")
    profile_group.add_argument("--update-profile", action="store_true", help="Update existing profile with new data")
    profile_group.add_argument("--list-profiles", action="store_true", help="List all available profiles")
    profile_group.add_argument("--export-profile", help="Export profile to file (specify profile name)")
    profile_group.add_argument("--delete-profile", help="Delete a profile (specify profile name)")
    
    # Search type flags
    search_group = parser.add_argument_group("Search Options")
    search_group.add_argument("--social", action="store_true", help="Social media search")
    search_group.add_argument("--breach", action="store_true", help="Data breach checks")
    search_group.add_argument("--public", action="store_true", help="Public records lookup")
    search_group.add_argument("--images", action="store_true", help="Image and avatar search")
    search_group.add_argument("--geolocation", action="store_true", help="Geolocation inference")
    search_group.add_argument("--full", action="store_true", help="Run all searches")
    
    # Output options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument("--save-report", help="Save report to file")
    output_group.add_argument("--format", choices=["json", "markdown", "html"], default="json", help="Report format")
    output_group.add_argument("--anonymize", action="store_true", help="Anonymize sensitive data in report")
    
    # Additional options
    other_group = parser.add_argument_group("Additional Options")
    other_group.add_argument("--nsfw", action="store_true", help="Include NSFW platforms in username search")
    other_group.add_argument("--verbose", action="store_true", help="Verbose output")
    other_group.add_argument("--headless", action="store_true", help="Run in headless mode")
    other_group.add_argument("--debug", action="store_true", help="Enable debug mode")
    other_group.add_argument("--test", action="store_true", help="Sandbox test mode")
    other_group.add_argument("--timeout", type=int, default=30, help="Request timeout in seconds")
    
    return parser


def validate_inputs(args):
    """Validate that at least one input method is provided"""
    inputs = [args.email, args.username, args.full_name, args.phone, args.domain, args.input_file]
    profile_ops = [args.load_profile, args.list_profiles, args.export_profile, args.delete_profile]
    
    if not any(inputs) and not any(profile_ops):
        print("Error: At least one input method must be specified.")
        print("Use --help for usage information.")
        sys.exit(1)


def load_targets_from_file(file_path):
    """Load targets from input file"""
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Input file '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)


def handle_profile_operations(args, profile_manager):
    """Handle profile-related operations"""
    
    # List profiles
    if args.list_profiles:
        profiles = profile_manager.list_profiles()
        if not profiles:
            print("No profiles found.")
            return
        
        print("Available profiles:")
        print("-" * 80)
        for profile in profiles:
            target_info = []
            for key, value in profile["target"].items():
                if value:
                    target_info.append(f"{key}: {value}")
            
            print(f"Name: {profile['name']}")
            print(f"Target: {', '.join(target_info) if target_info else 'N/A'}")
            print(f"Created: {profile['created_at']}")
            print(f"Updated: {profile['last_updated']}")
            print(f"Scans: {profile['scan_count']}")
            print("-" * 80)
        return
    
    # Delete profile
    if args.delete_profile:
        if profile_manager.delete_profile(args.delete_profile):
            print(f"Profile '{args.delete_profile}' deleted successfully.")
        else:
            print(f"Profile '{args.delete_profile}' not found.")
        return
    
    # Export profile
    if args.export_profile:
        export_data = profile_manager.export_profile(args.export_profile, args.format)
        if export_data:
            output_file = f"{args.export_profile}.{args.format}"
            with open(output_file, 'w') as f:
                f.write(export_data)
            print(f"Profile exported to: {output_file}")
        else:
            print(f"Profile '{args.export_profile}' not found.")
        return


def main():
    """Main application entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Validate inputs
    validate_inputs(args)
    
    # Load configuration
    config = load_config()
    
    # Initialize profile manager
    profile_manager = ProfileManager()
    
    # Handle profile-only operations
    if args.list_profiles or args.delete_profile or args.export_profile:
        handle_profile_operations(args, profile_manager)
        return
    
    # Determine search types
    if args.full:
        search_types = ["social", "breach", "public", "images", "geolocation"]
    else:
        search_types = []
        if args.social:
            search_types.append("social")
        if args.breach:
            search_types.append("breach")
        if args.public:
            search_types.append("public")
        if args.images:
            search_types.append("images")
        if args.geolocation:
            search_types.append("geolocation")
    
    if not search_types:
        print("Warning: No search types specified. Use --full or specify individual search types.")
        return
    
    # Initialize scanner
    scanner = OSINTScanner(
        config=config,
        verbose=args.verbose,
        debug=args.debug,
        timeout=args.timeout,
        headless=args.headless,
        test_mode=args.test
    )
    
    # Handle profile loading
    target = None
    if args.load_profile:
        profile_data = profile_manager.load_profile(args.load_profile)
        if not profile_data:
            print(f"Profile '{args.load_profile}' not found.")
            sys.exit(1)
        
        target = profile_data["target"]
        print(f"Loaded profile: {args.load_profile}")
        print(f"Target: {target}")
        
        if args.verbose:
            summary = profile_data.get("summary", {})
            print(f"Previous scans: {summary.get('total_scans', 0)}")
    else:
        # Prepare targets
        targets = []
        
        if args.input_file:
            targets.extend(load_targets_from_file(args.input_file))
        else:
            target = {
                "email": args.email,
                "username": args.username,
                "full_name": args.full_name,
                "phone": args.phone,
                "domain": args.domain
            }
            # Remove None values
            target = {k: v for k, v in target.items() if v is not None}
            if target:
                targets.append(target)
        
        if not targets:
            print("Error: No valid targets found.")
            sys.exit(1)
        
        # For now, handle single target
        target = targets[0]
    
    # Process target
    try:
        scan_results = scanner.scan_target(target, search_types, nsfw=args.nsfw)
        
        # Save to profile if requested
        if args.save_profile or args.update_profile:
            profile_name = args.profile_name or args.load_profile
            saved_name = profile_manager.save_profile(target, scan_results, profile_name)
            print(f"Profile saved: {saved_name}")
        
        # Prepare results for reporting
        all_results = [{
            "target": scan_results["target"],
            "results": scan_results["results"],
            "timestamp": scan_results["scan_time"]
        }]
        
        # Generate report
        if all_results:
            reporter = ReportGenerator()
            report = reporter.generate_report(all_results, format_type=args.format, anonymize=args.anonymize)
            
            if args.save_report:
                try:
                    with open(args.save_report, 'w') as f:
                        if args.format == "json":
                            json.dump(report, f, indent=2)
                        else:
                            f.write(report)
                    print(f"\nReport saved to: {args.save_report}")
                except Exception as e:
                    print(f"Error saving report: {e}")
            else:
                if args.format == "json":
                    print(json.dumps(report, indent=2))
                else:
                    print(report)
        else:
            print("No results to report.")
            
    except Exception as e:
        print(f"Error processing target {target}: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()

