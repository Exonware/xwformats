#!/usr/bin/env python3
"""
Unit tests for Dill serializer in xwformats.
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

from exonware.xwformats.formats.binary import DillSerializer
from exonware.xwsystem.io.errors import SerializationError


@pytest.mark.xwformats_unit
class TestDillSerializer:
    """Unit tests for Dill serializer."""

    def test_serializer_initialization(self):
        """Test that serializer initializes correctly."""
        serializer = DillSerializer()
        assert serializer.codec_id == "dill"
        assert ".dill" in serializer.file_extensions
        assert ".pkl" in serializer.file_extensions
        assert "application/x-dill" in serializer.media_types

    def test_metadata_properties(self):
        """Test all metadata properties."""
        serializer = DillSerializer()
        assert serializer.codec_id == "dill"
        assert serializer.format_name == "Dill"
        assert serializer.mime_type == "application/x-dill"
        assert serializer.is_binary_format is True
        assert serializer.supports_streaming is True
        assert "dill" in serializer.aliases
        assert "extended-pickle" in serializer.aliases

    def test_encode_dict(self):
        """Test encoding dictionary to Dill bytes."""
        serializer = DillSerializer()
        data = {"name": "Alice", "age": 30, "active": True}
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_encode_function(self):
        """Test encoding a function (extended capability)."""
        serializer = DillSerializer()
        def test_function(x):
            return x * 2
        result = serializer.encode(test_function)
        assert isinstance(result, bytes)
        assert len(result) > 0
        # Decode and verify function works
        decoded = serializer.decode(result)
        assert decoded(5) == 10

    def test_encode_lambda(self):
        """Test encoding a lambda function (extended capability)."""
        serializer = DillSerializer()
        lambda_func = lambda x: x + 1
        result = serializer.encode(lambda_func)
        assert isinstance(result, bytes)
        decoded = serializer.decode(result)
        assert decoded(5) == 6

    def test_encode_nested_function(self):
        """Test encoding nested function (extended capability)."""
        serializer = DillSerializer()
        def outer(x):
            def inner(y):
                return x * y
            return inner
        result = serializer.encode(outer)
        assert isinstance(result, bytes)
        decoded = serializer.decode(result)
        inner_func = decoded(3)
        assert inner_func(4) == 12

    def test_encode_generator(self):
        """Test encoding a generator function (extended capability)."""
        serializer = DillSerializer()
        def generator_func(n):
            for i in range(n):
                yield i * 2
        result = serializer.encode(generator_func)
        assert isinstance(result, bytes)
        decoded = serializer.decode(result)
        gen = decoded(5)
        assert list(gen) == [0, 2, 4, 6, 8]

    def test_decode_dill_bytes(self):
        """Test decoding Dill bytes to data."""
        serializer = DillSerializer()
        original = {"name": "Alice", "age": 30, "active": True}
        dill_bytes = serializer.encode(original)
        decoded = serializer.decode(dill_bytes)
        assert isinstance(decoded, dict)
        assert decoded["name"] == original["name"]
        assert decoded["age"] == original["age"]
        assert decoded["active"] == original["active"]

    def test_roundtrip_encoding(self):
        """Test roundtrip encoding and decoding."""
        serializer = DillSerializer()
        original = {
            "string": "test",
            "int": 42,
            "float": 3.14,
            "bool": True,
            "list": [1, 2, 3],
            "dict": {"nested": "value"}
        }
        dill_bytes = serializer.encode(original)
        decoded = serializer.decode(dill_bytes)
        assert decoded["string"] == original["string"]
        assert decoded["int"] == original["int"]
        assert decoded["float"] == original["float"]
        assert decoded["bool"] == original["bool"]
        assert decoded["list"] == original["list"]
        assert decoded["dict"] == original["dict"]

    def test_decode_string_raises_error(self):
        """Test that decoding string raises error."""
        serializer = DillSerializer()
        with pytest.raises(SerializationError, match="Failed to decode Dill"):
            serializer.decode("not bytes")

    def test_encode_empty_dict(self):
        """Test encoding empty dictionary."""
        serializer = DillSerializer()
        data = {}
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        decoded = serializer.decode(result)
        assert decoded == {}

    def test_encode_empty_list(self):
        """Test encoding empty list."""
        serializer = DillSerializer()
        data = []
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        decoded = serializer.decode(result)
        assert decoded == []

    def test_encode_nested_structures(self):
        """Test encoding nested data structures."""
        serializer = DillSerializer()
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

    def test_encode_class_instance(self):
        """Test encoding a class instance."""
        serializer = DillSerializer()
        class TestClass:
            def __init__(self, value):
                self.value = value
            def get_value(self):
                return self.value
        instance = TestClass(42)
        result = serializer.encode(instance)
        assert isinstance(result, bytes)
        decoded = serializer.decode(result)
        assert decoded.get_value() == 42

    def test_mime_types(self):
        """Test MIME type properties."""
        serializer = DillSerializer()
        assert "application/x-dill" in serializer.media_types
        assert "application/x-python-dill" in serializer.media_types

    def test_file_extensions(self):
        """Test file extension properties."""
        serializer = DillSerializer()
        assert ".dill" in serializer.file_extensions
        assert ".pkl" in serializer.file_extensions
