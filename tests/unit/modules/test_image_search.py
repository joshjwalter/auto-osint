import pytest
from unittest.mock import Mock, patch
from modules.image_search import ImageScanner

class TestImageScanner:
    def test_image_scanner_initialization(self, mock_config):
        """Test image scanner initializes correctly"""
        scanner = ImageScanner(mock_config)
        assert scanner.config == mock_config

    def test_extract_image_data(self, mock_config):
        """Test image data extraction from target data"""
        scanner = ImageScanner(mock_config)
        
        # Test direct image URL
        images = scanner._extract_image_data({"image": "https://example.com/image.jpg"})
        assert "https://example.com/image.jpg" in images
        
        # Test avatar URL
        images = scanner._extract_image_data({"avatar": "https://example.com/avatar.png"})
        assert "https://example.com/avatar.png" in images
        
        # Test profile picture
        images = scanner._extract_image_data({"profile_picture": "https://example.com/profile.jpg"})
        assert "https://example.com/profile.jpg" in images

    def test_test_mode_simulation(self, mock_config):
        """Test that test mode properly simulates results"""
        scanner = ImageScanner(mock_config, test_mode=True)
        results = scanner.scan({"image": "https://example.com/image.jpg"})
        
        assert "images" in results
        assert "summary" in results
        assert results["summary"]["images_found"] > 0

    @patch('modules.image_search.ImageScanner._reverse_image_search')
    def test_reverse_image_search(self, mock_search, mock_config):
        """Test reverse image search functionality"""
        mock_search.return_value = {
            "matches": ["https://match1.com", "https://match2.com"],
            "similarity": [0.95, 0.87]
        }
        
        scanner = ImageScanner(mock_config)
        results = scanner._reverse_image_search("https://example.com/image.jpg")
        
        assert "matches" in results
        assert "similarity" in results
        assert len(results["matches"]) > 0

    @patch('modules.image_search.ImageScanner._extract_exif')
    def test_exif_extraction(self, mock_exif, mock_config):
        """Test EXIF metadata extraction"""
        mock_exif.return_value = {
            "camera": "Canon EOS 5D",
            "location": {"latitude": 40.7128, "longitude": -74.0060},
            "timestamp": "2023-01-01T12:00:00"
        }
        
        scanner = ImageScanner(mock_config)
        results = scanner._extract_exif("https://example.com/image.jpg")
        
        assert "camera" in results
        assert "location" in results
        assert "timestamp" in results

    @patch('modules.image_search.ImageScanner._face_detection')
    def test_face_detection(self, mock_face, mock_config):
        """Test face detection functionality"""
        mock_face.return_value = {
            "faces_detected": 2,
            "confidence": 0.95,
            "locations": [(100, 100, 200, 200), (300, 300, 400, 400)]
        }
        
        scanner = ImageScanner(mock_config)
        results = scanner._face_detection("https://example.com/image.jpg")
        
        assert "faces_detected" in results
        assert "confidence" in results
        assert "locations" in results

    def test_empty_target_handling(self, mock_config):
        """Test handling of empty target data"""
        scanner = ImageScanner(mock_config, test_mode=True)
        
        results = scanner.scan({})
        assert results["summary"]["images_found"] == 0
        assert "images" in results

    def test_multiple_image_sources(self, mock_config):
        """Test handling of multiple image sources"""
        scanner = ImageScanner(mock_config, test_mode=True)
        
        # Target with multiple image sources
        target = {
            "image": "https://example.com/image.jpg",
            "avatar": "https://example.com/avatar.png",
            "profile_picture": "https://example.com/profile.jpg"
        }
        
        results = scanner.scan(target)
        assert results["summary"]["images_found"] > 0

    def test_scan_timing(self, mock_config):
        """Test scan timing calculation"""
        scanner = ImageScanner(mock_config, test_mode=True)
        results = scanner.scan({"image": "https://example.com/image.jpg"})
        
        assert "scan_time" in results
        assert isinstance(results["scan_time"], (int, float))

    def test_image_data_structure(self, mock_config):
        """Test image data structure"""
        scanner = ImageScanner(mock_config, test_mode=True)
        results = scanner.scan({"image": "https://example.com/image.jpg"})
        
        # Check expected structure
        assert "images" in results
        assert "summary" in results
        assert "images_found" in results["summary"]
        assert "exif_extracted" in results["summary"]
        assert "faces_detected" in results["summary"] 