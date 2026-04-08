#!/usr/bin/env python3
"""
Unit tests for Parquet serializer in xwformats.
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

from exonware.xwformats.formats.schema import ParquetSerializer
from exonware.xwsystem.io.errors import SerializationError


@pytest.mark.xwformats_unit
class TestParquetSerializer:
    """Unit tests for Parquet serializer."""

    def test_serializer_initialization(self):
        """Test that serializer initializes correctly."""
        serializer = ParquetSerializer()
        assert serializer.codec_id == "parquet"
        assert ".parquet" in serializer.file_extensions
        assert "application/parquet" in serializer.media_types

    def test_metadata_properties(self):
        """Test all metadata properties."""
        serializer = ParquetSerializer()
        assert serializer.codec_id == "parquet"
        assert serializer.format_name == "Parquet"
        assert serializer.mime_type == "application/parquet"
        assert serializer.is_binary_format is True
        assert serializer.supports_streaming is True
        assert "parquet" in serializer.aliases
        assert "parq" in serializer.aliases

    def test_encode_list_of_dicts(self):
        """Test encoding list of dicts to Parquet bytes."""
        serializer = ParquetSerializer()
        data = [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25, "city": "London"},
        ]
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_encode_single_dict(self):
        """Test encoding single dict (as single-row) to Parquet bytes."""
        serializer = ParquetSerializer()
        data = [{"name": "Alice", "age": 30}]
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_decode_parquet_bytes(self):
        """Test decoding Parquet bytes to list of dicts."""
        serializer = ParquetSerializer()
        original = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]
        parquet_bytes = serializer.encode(original)
        decoded = serializer.decode(parquet_bytes)
        assert isinstance(decoded, list)
        assert len(decoded) == 2
        assert decoded[0]["name"] == "Alice"
        assert decoded[0]["age"] == 30
        assert decoded[1]["name"] == "Bob"
        assert decoded[1]["age"] == 25

    def test_roundtrip_encoding(self):
        """Test roundtrip encoding and decoding."""
        serializer = ParquetSerializer()
        original = [
            {"a": 1, "b": 2.5, "c": "hello"},
            {"a": 3, "b": 4.0, "c": "world"},
        ]
        parquet_bytes = serializer.encode(original)
        decoded = serializer.decode(parquet_bytes)
        assert len(decoded) == len(original)
        assert decoded[0]["a"] == original[0]["a"]
        assert decoded[0]["c"] == original[0]["c"]

    def test_encode_unsupported_type_raises_error(self):
        """Test that encoding unsupported type raises clear error."""
        serializer = ParquetSerializer()
        with pytest.raises((SerializationError, TypeError), match=r"(Unsupported|Failed to encode)"):
            serializer.encode("not a list or dict")
        with pytest.raises((SerializationError, TypeError), match=r"(Unsupported|Failed to encode)"):
            serializer.encode(123)

    def test_decode_invalid_bytes_raises_error(self):
        """Test that decoding invalid bytes raises error."""
        serializer = ParquetSerializer()
        with pytest.raises(SerializationError, match=r"(Failed to decode|Parquet)"):
            serializer.decode(b"not valid parquet")

    def test_encode_empty_list(self):
        """Test encoding empty list."""
        serializer = ParquetSerializer()
        data = []
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        decoded = serializer.decode(result)
        assert decoded == []

    def test_mime_types(self):
        """Test MIME type properties."""
        serializer = ParquetSerializer()
        assert "application/parquet" in serializer.media_types
        assert "application/x-parquet" in serializer.media_types

    def test_file_extensions(self):
        """Test file extension properties."""
        serializer = ParquetSerializer()
        assert ".parquet" in serializer.file_extensions
        assert ".parq" in serializer.file_extensions
