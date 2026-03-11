#!/usr/bin/env python3
"""
Unit tests for YAML serializer in xwformats.
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
pytest.importorskip("yaml")
from exonware.xwformats.formats.text import YamlSerializer
from exonware.xwsystem.io.errors import SerializationError
@pytest.mark.xwformats_unit

class TestYamlSerializer:
    """Unit tests for YAML serializer."""

    def test_serializer_initialization(self):
        """Test that serializer initializes correctly."""
        serializer = YamlSerializer()
        assert serializer.codec_id == "yaml"
        assert ".yaml" in serializer.file_extensions
        assert ".yml" in serializer.file_extensions
        assert "text/yaml" in serializer.media_types

    def test_metadata_properties(self):
        """Test all metadata properties."""
        serializer = YamlSerializer()
        assert serializer.codec_id == "yaml"
        assert serializer.format_name == "YAML"
        assert serializer.mime_type == "text/yaml"
        assert serializer.is_binary_format is False
        assert "yaml" in serializer.aliases

    def test_encode_dict(self):
        """Test encoding dictionary to YAML bytes."""
        serializer = YamlSerializer()
        data = {"name": "Alice", "age": 30, "active": True}
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_encode_list(self):
        """Test encoding list to YAML bytes."""
        serializer = YamlSerializer()
        data = [1, 2, 3, "test", True]
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_decode_yaml_bytes(self):
        """Test decoding YAML bytes to data."""
        serializer = YamlSerializer()
        original = {"name": "Alice", "age": 30}
        yaml_bytes = serializer.encode(original)
        decoded = serializer.decode(yaml_bytes)
        assert isinstance(decoded, dict)
        assert decoded["name"] == original["name"]
        assert decoded["age"] == original["age"]

    def test_decode_yaml_string(self):
        """Test decoding YAML string to data."""
        serializer = YamlSerializer()
        original = {"key": "value"}
        yaml_bytes = serializer.encode(original)
        yaml_str = yaml_bytes.decode("utf-8")
        decoded = serializer.decode(yaml_str)
        assert decoded == original

    def test_roundtrip_encoding(self):
        """Test roundtrip encoding and decoding."""
        serializer = YamlSerializer()
        original = {
            "string": "test",
            "int": 42,
            "float": 3.14,
            "bool": True,
            "list": [1, 2, 3],
            "dict": {"nested": "value"},
        }
        yaml_bytes = serializer.encode(original)
        decoded = serializer.decode(yaml_bytes)
        assert decoded["string"] == original["string"]
        assert decoded["int"] == original["int"]
        assert decoded["float"] == original["float"]
        assert decoded["bool"] == original["bool"]
        assert decoded["list"] == original["list"]
        assert decoded["dict"] == original["dict"]

    def test_encode_empty_dict(self):
        """Test encoding empty dictionary."""
        serializer = YamlSerializer()
        data = {}
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        decoded = serializer.decode(result)
        assert decoded == {}

    def test_encode_empty_list(self):
        """Test encoding empty list."""
        serializer = YamlSerializer()
        data = []
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        decoded = serializer.decode(result)
        assert decoded == []

    def test_encode_nested_structures(self):
        """Test encoding nested data structures."""
        serializer = YamlSerializer()
        data = {
            "level1": {"level2": {"level3": "deep_value"}},
            "list": [1, [2, [3, 4]]],
        }
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        decoded = serializer.decode(result)
        assert decoded["level1"]["level2"]["level3"] == data["level1"]["level2"]["level3"]
        assert decoded["list"] == data["list"]

    def test_mime_types(self):
        """Test MIME type properties."""
        serializer = YamlSerializer()
        assert "text/yaml" in serializer.media_types
        assert "application/yaml" in serializer.media_types
        assert "text/x-yaml" in serializer.media_types

    def test_file_extensions(self):
        """Test file extension properties."""
        serializer = YamlSerializer()
        assert ".yaml" in serializer.file_extensions
        assert ".yml" in serializer.file_extensions
