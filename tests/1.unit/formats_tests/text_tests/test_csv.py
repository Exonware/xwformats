#!/usr/bin/env python3
"""
Unit tests for CSV serializer in xwformats.
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
from exonware.xwformats.formats.text import CsvSerializer
from exonware.xwsystem.io.errors import SerializationError
@pytest.mark.xwformats_unit

class TestCsvSerializer:
    """Unit tests for CSV serializer."""

    def test_serializer_initialization(self):
        """Test that serializer initializes correctly."""
        serializer = CsvSerializer()
        assert serializer.codec_id == "csv"
        assert ".csv" in serializer.file_extensions
        assert "text/csv" in serializer.media_types

    def test_metadata_properties(self):
        """Test all metadata properties."""
        serializer = CsvSerializer()
        assert serializer.codec_id == "csv"
        assert serializer.format_name == "CSV"
        assert serializer.mime_type == "text/csv"
        assert serializer.is_binary_format is False
        assert "csv" in serializer.aliases

    def test_encode_list_of_dicts(self):
        """Test encoding list of dicts to CSV bytes."""
        serializer = CsvSerializer()
        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        assert len(result) > 0
        assert b"name" in result or b"Alice" in result

    def test_decode_csv_bytes(self):
        """Test decoding CSV bytes to list of dicts (values are strings from CSV)."""
        serializer = CsvSerializer()
        original = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]
        csv_bytes = serializer.encode(original)
        decoded = serializer.decode(csv_bytes)
        assert isinstance(decoded, list)
        assert len(decoded) == 2
        assert decoded[0]["name"] == "Alice"
        assert decoded[0]["age"] in (30, "30")  # CSV returns strings
        assert decoded[1]["name"] == "Bob"
        assert decoded[1]["age"] in (25, "25")

    def test_decode_csv_string(self):
        """Test decoding CSV string to list of dicts."""
        serializer = CsvSerializer()
        original = [{"a": "1", "b": "2"}]
        csv_bytes = serializer.encode(original)
        csv_str = csv_bytes.decode("utf-8")
        decoded = serializer.decode(csv_str)
        assert decoded[0]["a"] == "1"
        assert decoded[0]["b"] == "2"

    def test_roundtrip_encoding(self):
        """Test roundtrip encoding and decoding (decoded values are strings)."""
        serializer = CsvSerializer()
        original = [
            {"col1": "a", "col2": "b"},
            {"col1": "c", "col2": "d"},
        ]
        csv_bytes = serializer.encode(original)
        decoded = serializer.decode(csv_bytes)
        assert len(decoded) == len(original)
        assert decoded[0]["col1"] == original[0]["col1"]
        assert decoded[1]["col2"] == original[1]["col2"]

    def test_encode_single_dict(self):
        """Test encoding single dict as one row."""
        serializer = CsvSerializer()
        data = [{"x": "1", "y": "2"}]
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        decoded = serializer.decode(result)
        assert len(decoded) == 1
        assert decoded[0]["x"] == "1"

    def test_encode_empty_list_raises(self):
        """Test that encoding empty list raises (CSV requires at least structure)."""
        serializer = CsvSerializer()
        data = []
        with pytest.raises((SerializationError, ValueError)):
            serializer.encode(data)

    def test_decode_empty_bytes_returns_empty_list(self):
        """Test that decoding empty CSV bytes returns empty list."""
        serializer = CsvSerializer()
        decoded = serializer.decode(b"")
        assert isinstance(decoded, list)
        assert decoded == []

    def test_mime_types(self):
        """Test MIME type properties."""
        serializer = CsvSerializer()
        assert "text/csv" in serializer.media_types
        assert "application/csv" in serializer.media_types

    def test_file_extensions(self):
        """Test file extension properties."""
        serializer = CsvSerializer()
        assert ".csv" in serializer.file_extensions
