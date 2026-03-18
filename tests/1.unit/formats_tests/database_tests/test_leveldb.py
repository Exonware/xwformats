#!/usr/bin/env python3
"""
Unit tests for LevelDB serializer in xwformats.
"""

import pytest

_ = pytest.importorskip("plyvel")

from exonware.xwformats.formats.database import XWLeveldbSerializer
from exonware.xwsystem.io.errors import SerializationError


@pytest.mark.xwformats_unit
class TestLevelDBSerializer:
    """Unit tests for LevelDB serializer."""

    def test_serializer_initialization(self):
        serializer = XWLeveldbSerializer()
        assert serializer.codec_id == "leveldb"
        assert ".leveldb" in serializer.file_extensions

    def test_encode_dict_to_bytes(self):
        serializer = XWLeveldbSerializer()
        data = {"key1": "value1", "key2": "value2"}

        result = serializer.encode(data)
        assert isinstance(result, bytes)

    def test_encode_non_dict_raises_error(self):
        serializer = XWLeveldbSerializer()
        with pytest.raises(SerializationError, match="expects dict"):
            serializer.encode(["not", "a", "dict"])

    def test_decode_bytes_to_dict(self):
        serializer = XWLeveldbSerializer()
        original = {"key1": "value1", "key2": "value2"}
        encoded = serializer.encode(original)
        decoded = serializer.decode(encoded)
        assert decoded == original

    def test_encode_to_file_creates_database(self, tmp_path):
        serializer = XWLeveldbSerializer()
        db_path = tmp_path / "test.ldb"
        data = {"user:1": "Alice", "user:2": "Bob"}

        serializer.encode_to_file(data, db_path)
        assert db_path.exists()

    def test_decode_from_file_reads_database(self, tmp_path):
        serializer = XWLeveldbSerializer()
        db_path = tmp_path / "test.ldb"
        data = {"user:1": "Alice", "user:2": "Bob"}

        serializer.encode_to_file(data, db_path)
        result = serializer.decode_from_file(db_path)
        assert result == data

    def test_roundtrip_file_operations(self, tmp_path):
        serializer = XWLeveldbSerializer()
        db_path = tmp_path / "roundtrip.ldb"
        original = {
            "config:timeout": 30,
            "config:retries": 3,
            "user:admin": {"role": "admin", "active": True},
        }

        serializer.encode_to_file(original, db_path)
        decoded = serializer.decode_from_file(db_path)
        assert decoded == original

    def test_encode_to_file_non_dict_raises_error(self, tmp_path):
        serializer = XWLeveldbSerializer()
        db_path = tmp_path / "invalid.ldb"

        with pytest.raises(SerializationError, match="expects dict"):
            serializer.encode_to_file([1, 2, 3], db_path)

    def test_handles_various_value_types(self, tmp_path):
        serializer = XWLeveldbSerializer()
        db_path = tmp_path / "types.ldb"
        data = {
            "string": "value",
            "int": 42,
            "float": 3.14,
            "bool": True,
            "none": None,
            "list": [1, 2, 3],
            "dict": {"nested": "value"},
        }

        serializer.encode_to_file(data, db_path)
        decoded = serializer.decode_from_file(db_path)
        assert decoded == data

    def test_mime_types(self):
        serializer = XWLeveldbSerializer()
        assert "application/x-leveldb" in serializer.media_types

    def test_file_extensions(self):
        serializer = XWLeveldbSerializer()
        assert ".ldb" in serializer.file_extensions
        assert ".leveldb" in serializer.file_extensions

