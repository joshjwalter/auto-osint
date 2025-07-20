"""
Domain Intelligence Scanner
Performs WHOIS lookup, DNS checks, and domain analysis.
"""

import requests
import socket
import dns.resolver
from typing import Dict, List, Any, Optional
from utils.http_client import HTTPClient


class DomainScanner:
    """Scanner for domain intelligence"""
    
    def __init__(self, config: Dict[str, Any], timeout: int = 30, test_mode: bool = False):
        """Initialize domain scanner"""
        self.config = config
        self.timeout = timeout
        self.test_mode = test_mode
        self.http_client = HTTPClient(timeout=timeout)
        
        # Domain intelligence services
        self.services = {
            "whois": {
                "url": "https://whois.whoisxmlapi.com/api/v1",
                "method": "GET",
                "requires_key": True,
                "api_key": config.get("whoisxmlapi_key", "")
            },
            "dns_lookup": {
                "method": "local",
                "requires_key": False
            },
            "ssl_certificate": {
                "method": "local",
                "requires_key": False
            }
        }
    
    def scan(self, target: Dict[str, str], nsfw: bool = False) -> Dict[str, Any]:
        """Scan for domain intelligence"""
        results = {
            "domain_info": {},
            "dns_records": {},
            "ssl_certificates": {},
            "summary": {
                "domains_checked": 0,
                "records_found": 0,
                "certificates_found": 0
            }
        }
        
        # Extract domains to check
        domains = self._extract_domains(target)
        
        if not domains:
            return results
        
        # Process each domain
        for domain in domains:
            domain_results = {
                "whois": {},
                "dns": {},
                "ssl": {},
                "checked_at": self._get_timestamp()
            }
            
            # WHOIS lookup
            if self.test_mode:
                whois_data = self._simulate_whois_lookup(domain)
            else:
                whois_data = self._get_whois_info(domain)
            
            if whois_data:
                domain_results["whois"] = whois_data
                results["domain_info"][domain] = whois_data
            
            # DNS lookup
            if self.test_mode:
                dns_data = self._simulate_dns_lookup(domain)
            else:
                dns_data = self._get_dns_records(domain)
            
            if dns_data:
                domain_results["dns"] = dns_data
                results["dns_records"][domain] = dns_data
                results["summary"]["records_found"] += len(dns_data.get("records", {}))
            
            # SSL certificate
            if self.test_mode:
                ssl_data = self._simulate_ssl_certificate(domain)
            else:
                ssl_data = self._get_ssl_certificate(domain)
            
            if ssl_data:
                domain_results["ssl"] = ssl_data
                results["ssl_certificates"][domain] = ssl_data
                results["summary"]["certificates_found"] += 1
            
            results["summary"]["domains_checked"] += 1
        
        return results
    
    def _extract_domains(self, target: Dict[str, str]) -> List[str]:
        """Extract domains from target data"""
        domains = []
        
        # Direct domain
        if target.get("domain"):
            domains.append(target["domain"])
        
        # Extract from email
        if target.get("email"):
            email_domain = target["email"].split("@")[1]
            domains.append(email_domain)
        
        # Remove duplicates
        return list(set(domains))
    
    def _get_whois_info(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get WHOIS information for a domain"""
        try:
            url = self.services["whois"]["url"]
            params = {
                "domainName": domain,
                "apiKey": self.services["whois"].get("api_key", ""),
                "outputFormat": "json"
            }
            
            # Skip if API key is not provided
            if not params["apiKey"]:
                return None
            
            response = self.http_client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "registrar": data.get("registrar", {}).get("name", ""),
                    "creation_date": data.get("creationDate", ""),
                    "expiration_date": data.get("expirationDate", ""),
                    "updated_date": data.get("updatedDate", ""),
                    "status": data.get("status", []),
                    "name_servers": data.get("nameServers", []),
                    "registrant": {
                        "organization": data.get("registrant", {}).get("organization", ""),
                        "country": data.get("registrant", {}).get("country", ""),
                        "state": data.get("registrant", {}).get("state", ""),
                        "city": data.get("registrant", {}).get("city", "")
                    }
                }
            
            return None
            
        except Exception as e:
            return None
    
    def _get_dns_records(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get DNS records for a domain"""
        try:
            records = {}
            
            # Common DNS record types
            record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]
            
            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    records[record_type] = [str(answer) for answer in answers]
                except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
                    continue
            
            # SPF record (usually in TXT)
            spf_records = []
            if "TXT" in records:
                for txt_record in records["TXT"]:
                    if txt_record.startswith("v=spf1"):
                        spf_records.append(txt_record)
            
            return {
                "records": records,
                "spf_records": spf_records,
                "has_spf": len(spf_records) > 0
            }
            
        except Exception as e:
            return None
    
    def _get_ssl_certificate(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get SSL certificate information"""
        try:
            import ssl
            import socket
            from datetime import datetime
            
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    return {
                        "subject": dict(x[0] for x in cert["subject"]),
                        "issuer": dict(x[0] for x in cert["issuer"]),
                        "version": cert["version"],
                        "serial_number": cert["serialNumber"],
                        "not_before": cert["notBefore"],
                        "not_after": cert["notAfter"],
                        "san": cert.get("subjectAltName", []),
                        "signature_algorithm": cert.get("signatureAlgorithm", "")
                    }
            
        except Exception as e:
            return None
    
    def _simulate_whois_lookup(self, domain: str) -> Dict[str, Any]:
        """Simulate WHOIS lookup for test mode"""
        return {
            "registrar": "Test Registrar Inc.",
            "creation_date": "2020-01-15T00:00:00Z",
            "expiration_date": "2025-01-15T00:00:00Z",
            "updated_date": "2023-01-15T00:00:00Z",
            "status": ["clientTransferProhibited"],
            "name_servers": ["ns1.test.com", "ns2.test.com"],
            "registrant": {
                "organization": "Test Organization",
                "country": "US",
                "state": "CA",
                "city": "San Francisco"
            }
        }
    
    def _simulate_dns_lookup(self, domain: str) -> Dict[str, Any]:
        """Simulate DNS lookup for test mode"""
        return {
            "records": {
                "A": ["192.168.1.1"],
                "AAAA": ["2001:db8::1"],
                "MX": ["mail.test.com"],
                "NS": ["ns1.test.com", "ns2.test.com"],
                "TXT": ["v=spf1 include:_spf.test.com ~all"],
                "CNAME": ["www.test.com"]
            },
            "spf_records": ["v=spf1 include:_spf.test.com ~all"],
            "has_spf": True
        }
    
    def _simulate_ssl_certificate(self, domain: str) -> Dict[str, Any]:
        """Simulate SSL certificate for test mode"""
        return {
            "subject": {"commonName": domain},
            "issuer": {"commonName": "Test CA"},
            "version": 3,
            "serial_number": "1234567890",
            "not_before": "Jan 15 00:00:00 2023 GMT",
            "not_after": "Jan 15 00:00:00 2024 GMT",
            "san": [("DNS", domain)],
            "signature_algorithm": "sha256WithRSAEncryption"
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_description(self) -> str:
        """Get scanner description"""
        return "Domain intelligence scanner"
    
    def get_capabilities(self) -> List[str]:
        """Get scanner capabilities"""
        return ["whois_lookup", "dns_records", "ssl_certificates", "spf_records"]
    
    def get_config_requirements(self) -> List[str]:
        """Get configuration requirements"""
        return ["whoisxmlapi_key"] 