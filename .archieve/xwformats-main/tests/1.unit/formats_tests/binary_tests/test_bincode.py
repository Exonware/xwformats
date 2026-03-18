#!/usr/bin/env python3
"""
Unit tests for Bincode serializer in xwformats.
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
pytest.importorskip("attrs2bin")
from exonware.xwformats.formats.binary import BincodeSerializer
from exonware.xwsystem.io.errors import SerializationError
@pytest.mark.xwformats_unit

class TestBincodeSerializer:
    """Unit tests for Bincode serializer."""

    def test_serializer_initialization(self):
        """Test that serializer initializes correctly."""
        serializer = BincodeSerializer()
        assert serializer.codec_id == "bincode"
        assert ".bincode" in serializer.file_extensions
        assert ".bin" in serializer.file_extensions
        assert "application/x-bincode" in serializer.media_types

    def test_metadata_properties(self):
        """Test all metadata properties."""
        serializer = BincodeSerializer()
        assert serializer.codec_id == "bincode"
        assert serializer.format_name == "Bincode"
        assert serializer.mime_type == "application/x-bincode"
        assert serializer.is_binary_format is True
        assert serializer.supports_streaming is True
        assert "bincode" in serializer.aliases
        assert "rust-bincode" in serializer.aliases

    def test_encode_dict(self):
        """Test encoding dictionary to Bincode bytes."""
        serializer = BincodeSerializer()
        data = {"name": "Alice", "age": 30, "active": True}
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        assert len(result) > 0
        # Decode and verify
        decoded = serializer.decode(result)
        assert isinstance(decoded, dict)
        assert decoded["name"] == data["name"]
        assert decoded["age"] == data["age"]

    def test_encode_attrs_object(self):
        """Test encoding attrs-based object to Bincode bytes."""
        import attr
        @attr.s(auto_attribs=True)
        class TestData:
            name: str
            age: int
            active: bool
        serializer = BincodeSerializer()
        data = TestData(name="Alice", age=30, active=True)
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        assert len(result) > 0
        # Decode with target_type
        decoded = serializer.decode(result, options={"target_type": TestData})
        assert decoded.name == data.name
        assert decoded.age == data.age
        assert decoded.active == data.active

    def test_decode_bincode_bytes(self):
        """Test decoding Bincode bytes to data."""
        serializer = BincodeSerializer()
        original = {"name": "Alice", "age": 30, "active": True}
        bincode_bytes = serializer.encode(original)
        decoded = serializer.decode(bincode_bytes)
        assert isinstance(decoded, dict)
        assert decoded["name"] == original["name"]
        assert decoded["age"] == original["age"]
        assert decoded["active"] == original["active"]

    def test_roundtrip_encoding(self):
        """Test roundtrip encoding and decoding."""
        serializer = BincodeSerializer()
        original = {
            "string": "test",
            "int": 42,
            "float": 3.14,
            "bool": True,
            "list": [1, 2, 3],
            "dict": {"nested": "value"}
        }
        bincode_bytes = serializer.encode(original)
        decoded = serializer.decode(bincode_bytes)
        assert decoded["string"] == original["string"]
        assert decoded["int"] == original["int"]
        assert decoded["float"] == original["float"]
        assert decoded["bool"] == original["bool"]
        assert decoded["list"] == original["list"]
        assert decoded["dict"] == original["dict"]

    def test_decode_string_raises_error(self):
        """Test that decoding string raises error."""
        serializer = BincodeSerializer()
        with pytest.raises(SerializationError, match="Failed to decode Bincode"):
            serializer.decode("not bytes")

    def test_encode_empty_dict(self):
        """Test encoding empty dictionary."""
        serializer = BincodeSerializer()
        data = {}
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        decoded = serializer.decode(result)
        assert decoded == {}

    def test_encode_empty_list(self):
        """Test encoding empty list."""
        serializer = BincodeSerializer()
        data = []
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        decoded = serializer.decode(result)
        assert decoded == []

    def test_encode_nested_structures(self):
        """Test encoding nested data structures."""
        serializer = BincodeSerializer()
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
        serializer = BincodeSerializer()
        assert "application/x-bincode" in serializer.media_types
        assert "application/vnd.rust.bincode" in serializer.media_types

    def test_file_extensions(self):
        """Test file extension properties."""
        serializer = BincodeSerializer()
        assert ".bincode" in serializer.file_extensions
        assert ".bin" in serializer.file_extensions
