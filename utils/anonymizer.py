"""
Anonymization Utility
Provides data anonymization capabilities for sensitive information.
"""

import hashlib
import re
from typing import Dict, List, Any, Union


class Anonymizer:
    """Data anonymization utility"""
    
    def __init__(self):
        """Initialize anonymizer"""
        self.sensitive_patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "ip_address": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            "credit_card": r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b'
        }
    
    def anonymize_data(self, data: Union[Dict, List, str]) -> Union[Dict, List, str]:
        """Anonymize sensitive data in the given structure"""
        if isinstance(data, dict):
            return self._anonymize_dict(data)
        elif isinstance(data, list):
            return self._anonymize_list(data)
        elif isinstance(data, str):
            return self._anonymize_string(data)
        else:
            return data
    
    def _anonymize_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize dictionary data"""
        anonymized = {}
        
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                anonymized[key] = self.anonymize_data(value)
            elif isinstance(value, str):
                anonymized[key] = self._anonymize_string(value)
            else:
                anonymized[key] = value
        
        return anonymized
    
    def _anonymize_list(self, data: List[Any]) -> List[Any]:
        """Anonymize list data"""
        return [self.anonymize_data(item) for item in data]
    
    def _anonymize_string(self, text: str) -> str:
        """Anonymize sensitive patterns in text"""
        if not isinstance(text, str):
            return text
        
        anonymized = text
        
        # Anonymize emails
        anonymized = re.sub(
            self.sensitive_patterns["email"],
            lambda m: self._hash_email(m.group()),
            anonymized
        )
        
        # Anonymize phone numbers
        anonymized = re.sub(
            self.sensitive_patterns["phone"],
            lambda m: self._hash_phone(m.group()),
            anonymized
        )
        
        # Anonymize IP addresses
        anonymized = re.sub(
            self.sensitive_patterns["ip_address"],
            lambda m: self._hash_ip(m.group()),
            anonymized
        )
        
        # Anonymize credit card numbers
        anonymized = re.sub(
            self.sensitive_patterns["credit_card"],
            lambda m: self._hash_credit_card(m.group()),
            anonymized
        )
        
        # Anonymize SSNs
        anonymized = re.sub(
            self.sensitive_patterns["ssn"],
            lambda m: self._hash_ssn(m.group()),
            anonymized
        )
        
        return anonymized
    
    def anonymize_value(self, value: str) -> str:
        """Anonymize a single value"""
        if not isinstance(value, str):
            return str(value)
        
        # Check for common sensitive field names
        sensitive_fields = ["email", "phone", "password", "ssn", "credit_card", "ip"]
        
        for field in sensitive_fields:
            if field in value.lower():
                return self._hash_value(value)
        
        return self._anonymize_string(value)
    
    def _hash_email(self, email: str) -> str:
        """Hash email address"""
        if "@" not in email:
            return email
        
        username, domain = email.split("@", 1)
        hashed_username = self._hash_value(username)
        return f"{hashed_username}@{domain}"
    
    def _hash_phone(self, phone: str) -> str:
        """Hash phone number"""
        cleaned = re.sub(r'[^\d]', '', phone)
        if len(cleaned) == 10:
            return f"***-***-{cleaned[-4:]}"
        elif len(cleaned) == 11 and cleaned.startswith('1'):
            return f"+1-***-***-{cleaned[-4:]}"
        else:
            return self._hash_value(phone)
    
    def _hash_ip(self, ip: str) -> str:
        """Hash IP address"""
        parts = ip.split('.')
        if len(parts) == 4:
            return f"{parts[0]}.{parts[1]}.*.*"
        return self._hash_value(ip)
    
    def _hash_credit_card(self, card: str) -> str:
        """Hash credit card number"""
        cleaned = re.sub(r'[^\d]', '', card)
        if len(cleaned) >= 4:
            return f"****-****-****-{cleaned[-4:]}"
        return self._hash_value(card)
    
    def _hash_ssn(self, ssn: str) -> str:
        """Hash SSN"""
        cleaned = re.sub(r'[^\d]', '', ssn)
        if len(cleaned) == 9:
            return f"***-**-{cleaned[-4:]}"
        return self._hash_value(ssn)
    
    def _hash_value(self, value: str) -> str:
        """Create a hash of the value"""
        if not value:
            return value
        
        # Create a short hash for readability
        hash_obj = hashlib.md5(value.encode())
        return f"[HASH:{hash_obj.hexdigest()[:8]}]"
    
    def is_sensitive_field(self, field_name: str) -> bool:
        """Check if a field name indicates sensitive data"""
        sensitive_keywords = [
            "email", "phone", "password", "ssn", "credit", "card",
            "address", "name", "ip", "key", "secret", "token"
        ]
        
        field_lower = field_name.lower()
        return any(keyword in field_lower for keyword in sensitive_keywords)
    
    def anonymize_field(self, field_name: str, value: Any) -> Any:
        """Anonymize a field based on its name and value"""
        if self.is_sensitive_field(field_name):
            if isinstance(value, str):
                return self.anonymize_value(value)
            elif isinstance(value, (dict, list)):
                return self.anonymize_data(value)
        
        return value 