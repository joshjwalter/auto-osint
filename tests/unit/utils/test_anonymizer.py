import pytest
from utils.anonymizer import Anonymizer

class TestAnonymizer:
    def test_anonymize_email(self):
        """Test email anonymization"""
        anonymizer = Anonymizer()
        
        text = "Contact me at john.doe@example.com"
        result = anonymizer._anonymize_string(text)
        
        assert "john.doe@example.com" not in result
        assert "@example.com" in result  # Domain preserved

    def test_anonymize_phone(self):
        """Test phone number anonymization"""
        anonymizer = Anonymizer()
        
        text = "Call me at 555-123-4567"
        result = anonymizer._anonymize_string(text)
        
        assert "555-123-4567" not in result
        assert "***-***-4567" in result  # Last 4 digits preserved

    def test_anonymize_nested_data(self):
        """Test anonymization of nested data structures"""
        anonymizer = Anonymizer()
        
        data = {
            "user": {
                "email": "test@example.com",
                "profile": {
                    "phone": "555-123-4567"
                }
            }
        }
        
        result = anonymizer.anonymize_data(data)
        assert "test@example.com" not in str(result)
        assert "555-123-4567" not in str(result)

    def test_anonymize_list_data(self):
        """Test anonymization of list data"""
        anonymizer = Anonymizer()
        
        data = [
            {"email": "user1@example.com", "phone": "555-111-1111"},
            {"email": "user2@example.com", "phone": "555-222-2222"}
        ]
        
        result = anonymizer.anonymize_data(data)
        assert "user1@example.com" not in str(result)
        assert "user2@example.com" not in str(result)
        assert "555-111-1111" not in str(result)
        assert "555-222-2222" not in str(result)

    def test_preserve_structure(self):
        """Test that data structure is preserved during anonymization"""
        anonymizer = Anonymizer()
        
        original_data = {
            "user": {
                "email": "test@example.com",
                "profile": {
                    "phone": "555-123-4567",
                    "name": "John Doe"  # Should not be anonymized
                }
            }
        }
        
        result = anonymizer.anonymize_data(original_data)
        
        # Structure should be preserved
        assert "user" in result
        assert "profile" in result["user"]
        assert "name" in result["user"]["profile"]
        assert result["user"]["profile"]["name"] == "John Doe"  # Name preserved

    def test_custom_patterns(self):
        """Test custom anonymization patterns"""
        anonymizer = Anonymizer()
        
        # Test custom pattern
        text = "SSN: 123-45-6789"
        result = anonymizer._anonymize_string(text)
        
        assert "123-45-6789" not in result
        assert "***-**-6789" in result  # Last 4 digits preserved

    def test_empty_data(self):
        """Test handling of empty data"""
        anonymizer = Anonymizer()
        
        result = anonymizer.anonymize_data({})
        assert result == {}
        
        result = anonymizer.anonymize_data([])
        assert result == []

    def test_non_string_data(self):
        """Test handling of non-string data"""
        anonymizer = Anonymizer()
        
        data = {
            "number": 123,
            "boolean": True,
            "none": None
        }
        
        result = anonymizer.anonymize_data(data)
        assert result["number"] == 123
        assert result["boolean"] is True
        assert result["none"] is None

    def test_multiple_emails_in_text(self):
        """Test anonymization of multiple emails in text"""
        anonymizer = Anonymizer()
        
        text = "Contact john@example.com and jane@test.com"
        result = anonymizer._anonymize_string(text)
        
        assert "john@example.com" not in result
        assert "jane@test.com" not in result
        assert "@example.com" in result
        assert "@test.com" in result 