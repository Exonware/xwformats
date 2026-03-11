#!/usr/bin/env python3
"""
Unit tests for RON serializer in xwformats.
Following GUIDE_TEST.md standards:
- Comprehensive test coverage
- Test both success and failure scenarios
- Edge cases and various data types
- Proper error handling validation
- Root cause fixing (no rigged tests)
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
"""

from __future__ import annotations
import pytest
# RON serializer now has built-in parser - always available
from exonware.xwformats.formats.text import RonSerializer
from exonware.xwsystem.io.errors import SerializationError
@pytest.mark.xwformats_unit

class TestRonSerializer:
    """Unit tests for RON serializer."""

    def test_serializer_initialization(self):
        """Test that serializer initializes correctly."""
        serializer = RonSerializer()
        assert serializer.codec_id == "ron"
        assert ".ron" in serializer.file_extensions
        assert "application/x-ron" in serializer.media_types

    def test_metadata_properties(self):
        """Test all metadata properties."""
        serializer = RonSerializer()
        assert serializer.codec_id == "ron"
        assert serializer.format_name == "RON"
        assert serializer.mime_type == "application/x-ron"
        assert serializer.is_binary_format is False
        assert serializer.supports_streaming is False
        assert "ron" in serializer.aliases
        assert "rusty-object-notation" in serializer.aliases

    def test_encode_dict(self):
        """Test encoding dictionary to RON string."""
        serializer = RonSerializer()
        data = {
            'window_size': (800, 600),
            'window_title': 'My App',
            'fullscreen': False
        }
        result = serializer.encode(data)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_encode_list(self):
        """Test encoding list to RON string."""
        serializer = RonSerializer()
        data = [1, 2, 3, "test", True]
        result = serializer.encode(data)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_decode_ron_string(self):
        """Test decoding RON string to data."""
        serializer = RonSerializer()
        original = {
            'window_size': (800, 600),
            'window_title': 'My App',
            'fullscreen': False
        }
        ron_string = serializer.encode(original)
        decoded = serializer.decode(ron_string)
        assert isinstance(decoded, dict)
        assert decoded['window_title'] == original['window_title']
        assert decoded['fullscreen'] == original['fullscreen']

    def test_decode_ron_bytes(self):
        """Test decoding RON bytes to data."""
        serializer = RonSerializer()
        original = {"name": "Alice", "age": 30}
        ron_string = serializer.encode(original)
        ron_bytes = ron_string.encode('utf-8')
        decoded = serializer.decode(ron_bytes)
        assert decoded["name"] == original["name"]
        assert decoded["age"] == original["age"]

    def test_roundtrip_encoding(self):
        """Test roundtrip encoding and decoding."""
        serializer = RonSerializer()
        original = {
            "string": "test",
            "int": 42,
            "float": 3.14,
            "bool": True,
            "tuple": (1, 2, 3),
            "list": [1, 2, 3],
            "dict": {"nested": "value"}
        }
        ron_string = serializer.encode(original)
        decoded = serializer.decode(ron_string)
        assert decoded["string"] == original["string"]
        assert decoded["int"] == original["int"]
        assert decoded["float"] == original["float"]
        assert decoded["bool"] == original["bool"]
        assert decoded["list"] == original["list"]
        assert decoded["dict"] == original["dict"]

    def test_encode_empty_dict(self):
        """Test encoding empty dictionary."""
        serializer = RonSerializer()
        data = {}
        result = serializer.encode(data)
        assert isinstance(result, str)
        decoded = serializer.decode(result)
        assert decoded == {}

    def test_encode_empty_list(self):
        """Test encoding empty list."""
        serializer = RonSerializer()
        data = []
        result = serializer.encode(data)
        assert isinstance(result, str)
        decoded = serializer.decode(result)
        assert decoded == []

    def test_encode_nested_structures(self):
        """Test encoding nested data structures."""
        serializer = RonSerializer()
        data = {
            "level1": {
                "level2": {
                    "level3": "deep_value"
                }
            },
            "list": [1, [2, [3, 4]]]
        }
        result = serializer.encode(data)
        assert isinstance(result, str)
        decoded = serializer.decode(result)
        assert decoded["level1"]["level2"]["level3"] == data["level1"]["level2"]["level3"]
        assert decoded["list"] == data["list"]

    def test_mime_types(self):
        """Test MIME type properties."""
        serializer = RonSerializer()
        assert "application/x-ron" in serializer.media_types
        assert "text/x-ron" in serializer.media_types
        assert "application/vnd.rust.ron" in serializer.media_types

    def test_file_extensions(self):
        """Test file extension properties."""
        serializer = RonSerializer()
        assert ".ron" in serializer.file_extensions
