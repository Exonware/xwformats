#!/usr/bin/env python3
"""
Unit tests for Postcard serializer in xwformats.
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
pytest.importorskip("pypostcard")
from exonware.xwformats.formats.binary import PostcardSerializer
from exonware.xwsystem.io.errors import SerializationError
@pytest.mark.xwformats_unit

class TestPostcardSerializer:
    """Unit tests for Postcard serializer."""

    def test_serializer_initialization(self):
        """Test that serializer initializes correctly."""
        serializer = PostcardSerializer()
        assert serializer.codec_id == "postcard"
        assert ".postcard" in serializer.file_extensions
        assert ".pcd" in serializer.file_extensions
        assert "application/x-postcard" in serializer.media_types

    def test_metadata_properties(self):
        """Test all metadata properties."""
        serializer = PostcardSerializer()
        assert serializer.codec_id == "postcard"
        assert serializer.format_name == "Postcard"
        assert serializer.mime_type == "application/x-postcard"
        assert serializer.is_binary_format is True
        assert serializer.supports_streaming is True
        assert "postcard" in serializer.aliases
        assert "rust-postcard" in serializer.aliases

    def test_encode_dict(self):
        """Test encoding dictionary to Postcard bytes."""
        serializer = PostcardSerializer()
        data = {"sensor_id": 42, "temperature": 23.5, "timestamp": 1234567890}
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_encode_list(self):
        """Test encoding list to Postcard bytes."""
        serializer = PostcardSerializer()
        data = [1, 2, 3, "test", True]
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_decode_postcard_bytes(self):
        """Test decoding Postcard bytes to data."""
        serializer = PostcardSerializer()
        original = {"sensor_id": 42, "temperature": 23.5, "timestamp": 1234567890}
        postcard_bytes = serializer.encode(original)
        decoded = serializer.decode(postcard_bytes)
        assert isinstance(decoded, dict)
        assert decoded["sensor_id"] == original["sensor_id"]
        assert decoded["temperature"] == original["temperature"]
        assert decoded["timestamp"] == original["timestamp"]

    def test_roundtrip_encoding(self):
        """Test roundtrip encoding and decoding."""
        serializer = PostcardSerializer()
        original = {
            "string": "test",
            "int": 42,
            "float": 3.14,
            "bool": True,
            "list": [1, 2, 3],
            "dict": {"nested": "value"}
        }
        postcard_bytes = serializer.encode(original)
        decoded = serializer.decode(postcard_bytes)
        assert decoded["string"] == original["string"]
        assert decoded["int"] == original["int"]
        assert decoded["float"] == original["float"]
        assert decoded["bool"] == original["bool"]
        assert decoded["list"] == original["list"]
        assert decoded["dict"] == original["dict"]

    def test_decode_string_raises_error(self):
        """Test that decoding string raises error."""
        serializer = PostcardSerializer()
        with pytest.raises(SerializationError, match="Failed to decode Postcard"):
            serializer.decode("not bytes")

    def test_encode_empty_dict(self):
        """Test encoding empty dictionary."""
        serializer = PostcardSerializer()
        data = {}
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        decoded = serializer.decode(result)
        assert decoded == {}

    def test_encode_empty_list(self):
        """Test encoding empty list."""
        serializer = PostcardSerializer()
        data = []
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        decoded = serializer.decode(result)
        assert decoded == []

    def test_compact_encoding(self):
        """Test that Postcard produces compact encoding."""
        serializer = PostcardSerializer()
        data = {"sensor_id": 42, "temperature": 23.5}
        postcard_bytes = serializer.encode(data)
        # Postcard encoding (using pickle fallback for dicts since pypostcard doesn't support dict directly)
        # Should be reasonably compact
        assert len(postcard_bytes) < 100

    def test_encode_nested_structures(self):
        """Test encoding nested data structures."""
        serializer = PostcardSerializer()
        data = {
            "level1": {
                "level2": {
                    "level3": "deep_value"
                }
            },
            "list": [1, [2, [3, 4]]]
        }
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        decoded = serializer.decode(result)
        assert decoded["level1"]["level2"]["level3"] == data["level1"]["level2"]["level3"]
        assert decoded["list"] == data["list"]

    def test_mime_types(self):
        """Test MIME type properties."""
        serializer = PostcardSerializer()
        assert "application/x-postcard" in serializer.media_types
        assert "application/vnd.rust.postcard" in serializer.media_types

    def test_file_extensions(self):
        """Test file extension properties."""
        serializer = PostcardSerializer()
        assert ".postcard" in serializer.file_extensions
        assert ".pcd" in serializer.file_extensions
