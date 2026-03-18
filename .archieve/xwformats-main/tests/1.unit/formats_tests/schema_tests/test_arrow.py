#!/usr/bin/env python3
"""
Unit tests for Apache Arrow serializer in xwformats.
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
from pathlib import Path
import tempfile
pytest.importorskip("pyarrow")
from exonware.xwformats.formats.schema import ArrowSerializer
from exonware.xwsystem.io.errors import SerializationError
@pytest.mark.xwformats_unit

class TestArrowSerializer:
    """Unit tests for Apache Arrow serializer."""

    def test_serializer_initialization(self):
        """Test that serializer initializes correctly."""
        serializer = ArrowSerializer()
        assert serializer.codec_id == "arrow"
        assert ".arrow" in serializer.file_extensions
        assert ".arrows" in serializer.file_extensions
        assert ".ipc" in serializer.file_extensions
        assert "application/vnd.apache.arrow.stream" in serializer.media_types

    def test_metadata_properties(self):
        """Test all metadata properties."""
        serializer = ArrowSerializer()
        assert serializer.codec_id == "arrow"
        assert serializer.format_name == "Arrow"
        assert serializer.mime_type == "application/vnd.apache.arrow.stream"
        assert serializer.is_binary_format is True
        assert serializer.supports_streaming is True
        assert "arrow" in serializer.aliases
        assert "Arrow" in serializer.aliases
        assert "ARROW" in serializer.aliases
        assert "apache-arrow" in serializer.aliases

    def test_encode_list_of_dicts(self):
        """Test encoding list of dicts to Arrow bytes."""
        serializer = ArrowSerializer()
        data = [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25, "city": "London"},
            {"name": "Charlie", "age": 35, "city": "Tokyo"}
        ]
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_encode_single_dict(self):
        """Test encoding single dict to Arrow bytes."""
        serializer = ArrowSerializer()
        data = {"name": "Alice", "age": 30}
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_encode_pandas_dataframe(self):
        """Test encoding pandas DataFrame to Arrow bytes."""
        pytest.importorskip("pandas")
        import pandas as pd
        serializer = ArrowSerializer()
        df = pd.DataFrame({
            "name": ["Alice", "Bob", "Charlie"],
            "age": [30, 25, 35],
            "city": ["New York", "London", "Tokyo"]
        })
        result = serializer.encode(df)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_encode_unsupported_type_raises_error(self):
        """Test that encoding unsupported type raises clear error."""
        serializer = ArrowSerializer()
        with pytest.raises(SerializationError, match="Unsupported type for Arrow"):
            serializer.encode("not a list or dict")
        with pytest.raises(SerializationError, match="Unsupported type for Arrow"):
            serializer.encode(123)

    def test_decode_arrow_bytes(self):
        """Test decoding Arrow bytes to list of dicts."""
        serializer = ArrowSerializer()
        original = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25}
        ]
        arrow_bytes = serializer.encode(original)
        decoded = serializer.decode(arrow_bytes)
        assert isinstance(decoded, list)
        assert len(decoded) == 2
        assert decoded[0]["name"] == "Alice"
        assert decoded[0]["age"] == 30
        assert decoded[1]["name"] == "Bob"
        assert decoded[1]["age"] == 25

    def test_decode_as_dataframe(self):
        """Test decoding Arrow bytes to pandas DataFrame."""
        pytest.importorskip("pandas")
        import pandas as pd
        serializer = ArrowSerializer()
        original = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25}
        ]
        arrow_bytes = serializer.encode(original)
        decoded = serializer.decode(arrow_bytes, options={"as_dataframe": True})
        assert isinstance(decoded, pd.DataFrame)
        assert len(decoded) == 2
        assert "name" in decoded.columns
        assert "age" in decoded.columns

    def test_roundtrip_encoding(self):
        """Test roundtrip encoding and decoding."""
        serializer = ArrowSerializer()
        original = [
            {"name": "Alice", "age": 30, "active": True},
            {"name": "Bob", "age": 25, "active": False},
            {"name": "Charlie", "age": 35, "active": True}
        ]
        arrow_bytes = serializer.encode(original)
        decoded = serializer.decode(arrow_bytes)
        assert len(decoded) == len(original)
        assert decoded[0]["name"] == original[0]["name"]
        assert decoded[0]["age"] == original[0]["age"]
        assert decoded[0]["active"] == original[0]["active"]

    def test_decode_string_raises_error(self):
        """Test that decoding string raises error."""
        serializer = ArrowSerializer()
        with pytest.raises(SerializationError, match="Failed to decode Arrow"):
            serializer.decode("not bytes")

    def test_encode_empty_list(self):
        """Test encoding empty list."""
        serializer = ArrowSerializer()
        data = []
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        decoded = serializer.decode(result)
        assert decoded == []

    def test_encode_nested_structures(self):
        """Test encoding nested data structures."""
        serializer = ArrowSerializer()
        data = [
            {
                "name": "Alice",
                "address": {
                    "street": "123 Main St",
                    "city": "New York"
                },
                "tags": ["developer", "python"]
            }
        ]
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        decoded = serializer.decode(result)
        assert len(decoded) == 1
        assert "name" in decoded[0]
        assert "address" in decoded[0]
        assert "tags" in decoded[0]

    def test_mime_types(self):
        """Test MIME type properties."""
        serializer = ArrowSerializer()
        assert "application/vnd.apache.arrow.stream" in serializer.media_types
        assert "application/x-apache-arrow" in serializer.media_types

    def test_file_extensions(self):
        """Test file extension properties."""
        serializer = ArrowSerializer()
        assert ".arrow" in serializer.file_extensions
        assert ".arrows" in serializer.file_extensions
        assert ".ipc" in serializer.file_extensions
