#!/usr/bin/env python3
"""
Unit tests for RocksDB serializer in xwformats.
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
import shutil
# RocksDB serializer is always available (has pure Python fallback)
from exonware.xwformats.formats.database import RocksdbSerializer, open_rocksdb_database
from exonware.xwformats.formats.database.rocksdb import DB, WriteBatch, rocksdb
from exonware.xwsystem.io.errors import SerializationError
@pytest.mark.xwformats_unit

class TestInternalRocksDBEngine:
    """Direct coverage for the pure-Python DB and open_rocksdb_database (no external rocksdb)."""

    def test_open_returns_internal_db_class(self, tmp_path):
        db = open_rocksdb_database(tmp_path / "store", create_if_missing=True)
        assert isinstance(db, DB)

    def test_put_get_persist_reopen(self, tmp_path):
        path = tmp_path / "kvdir"
        db1 = open_rocksdb_database(path, create_if_missing=True)
        db1.put(b"alpha", b"one")
        db1.put(b"beta", b"two")
        db2 = open_rocksdb_database(path, create_if_missing=True)
        assert db2.get(b"alpha") == b"one"
        assert db2.get(b"beta") == b"two"

    def test_delete_persists(self, tmp_path):
        path = tmp_path / "kvdir2"
        db = open_rocksdb_database(path, create_if_missing=True)
        db.put(b"x", b"y")
        db.delete(b"x")
        again = open_rocksdb_database(path, create_if_missing=True)
        assert again.get(b"x") is None

    def test_write_batch_single_flush(self, tmp_path):
        path = tmp_path / "batchdir"
        db = open_rocksdb_database(path, create_if_missing=True)
        batch = WriteBatch()
        batch.put(b"a", b"1")
        batch.put(b"b", b"2")
        batch.delete(b"c")
        wo = rocksdb.WriteOptions()
        wo.sync = True
        db.write(batch, write_opts=wo)
        loaded = open_rocksdb_database(path, create_if_missing=True)
        assert loaded.get(b"a") == b"1"
        assert loaded.get(b"b") == b"2"
        assert loaded.get(b"c") is None

    def test_iteritems_sorted_hex_order(self, tmp_path):
        path = tmp_path / "iterdir"
        db = open_rocksdb_database(path, create_if_missing=True)
        db.put(b"\xff", b"high")
        db.put(b"\x00", b"low")
        db.put(b"\x80", b"mid")
        it = db.iteritems()
        it.seek_to_first()
        keys = [k for k, _ in it]
        assert keys == sorted(keys)

    def test_shim_module_has_no_native_binding(self):
        """Engine is always the in-tree module object, not a third-party rocksdb package."""
        assert hasattr(rocksdb, "DB")
        assert hasattr(rocksdb, "Options")
        assert rocksdb.DB is DB


@pytest.mark.xwformats_unit

class TestRocksDBSerializer:
    """Unit tests for RocksDB serializer."""

    def test_serializer_initialization(self):
        """Test that serializer initializes correctly."""
        serializer = RocksdbSerializer()
        assert serializer.codec_id == "rocksdb"
        assert ".rocksdb" in serializer.file_extensions
        assert ".rdb" in serializer.file_extensions
        assert "application/x-rocksdb" in serializer.media_types

    def test_metadata_properties(self):
        """Test all metadata properties."""
        serializer = RocksdbSerializer()
        assert serializer.codec_id == "rocksdb"
        assert serializer.format_name == "RocksDB"
        assert serializer.mime_type == "application/x-rocksdb"
        assert serializer.is_binary_format is True
        assert serializer.supports_streaming is True
        assert "rocksdb" in serializer.aliases
        assert "RocksDB" in serializer.aliases
        assert "rdb" in serializer.aliases

    def test_encode_dict_to_bytes(self):
        """Test encoding dictionary to bytes."""
        serializer = RocksdbSerializer()
        data = {"key1": "value1", "key2": "value2"}
        result = serializer.encode(data)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_encode_non_dict_raises_error(self):
        """Test that encoding non-dict raises clear error."""
        serializer = RocksdbSerializer()
        with pytest.raises(SerializationError, match="expects dict"):
            serializer.encode(["not", "a", "dict"])
        with pytest.raises(SerializationError, match="expects dict"):
            serializer.encode("not a dict")

    def test_decode_bytes_to_dict(self):
        """Test decoding bytes to dictionary."""
        serializer = RocksdbSerializer()
        original = {"key1": "value1", "key2": "value2"}
        encoded = serializer.encode(original)
        decoded = serializer.decode(encoded)
        assert isinstance(decoded, dict)
        assert decoded == original

    def test_decode_string_raises_error(self):
        """Test that decoding string raises error."""
        serializer = RocksdbSerializer()
        with pytest.raises(SerializationError, match="expects bytes"):
            serializer.decode("not bytes")

    def test_save_file_creates_database(self, tmp_path):
        """Test that saving to file creates RocksDB database."""
        serializer = RocksdbSerializer()
        output_file = tmp_path / "test.rocksdb"
        data = {"key1": "value1", "key2": "value2", "key3": "value3"}
        serializer.save_file(data, output_file)
        assert output_file.exists() or (output_file.parent / "test.rocksdb").exists()

    def test_load_file_reads_database(self, tmp_path):
        """Test that loading from file reads RocksDB database."""
        serializer = RocksdbSerializer()
        output_file = tmp_path / "test.rocksdb"
        original = {"key1": "value1", "key2": "value2", "key3": "value3"}
        serializer.save_file(original, output_file)
        decoded = serializer.load_file(output_file)
        assert isinstance(decoded, dict)
        assert decoded["key1"] == original["key1"]
        assert decoded["key2"] == original["key2"]
        assert decoded["key3"] == original["key3"]

    def test_roundtrip_file_operations(self, tmp_path):
        """Test roundtrip file operations."""
        serializer = RocksdbSerializer()
        output_file = tmp_path / "roundtrip.rocksdb"
        original = {
            "string_key": "string_value",
            "int_key": 42,
            "float_key": 3.14,
            "bool_key": True,
            "list_key": [1, 2, 3],
            "dict_key": {"nested": "value"}
        }
        serializer.save_file(original, output_file)
        decoded = serializer.load_file(output_file)
        assert decoded["string_key"] == original["string_key"]
        assert decoded["int_key"] == original["int_key"]
        assert decoded["float_key"] == original["float_key"]
        assert decoded["bool_key"] == original["bool_key"]
        assert decoded["list_key"] == original["list_key"]
        assert decoded["dict_key"] == original["dict_key"]

    def test_save_file_non_dict_raises_error(self, tmp_path):
        """Test that saving non-dict to file raises error."""
        serializer = RocksdbSerializer()
        output_file = tmp_path / "test.rocksdb"
        with pytest.raises(SerializationError, match="expects dict"):
            serializer.save_file(["not", "a", "dict"], output_file)

    def test_handles_various_value_types(self, tmp_path):
        """Test handling various value types."""
        serializer = RocksdbSerializer()
        output_file = tmp_path / "types.rocksdb"
        data = {
            "string": "text",
            "int": 42,
            "float": 3.14,
            "bool": True,
            "none": None,
            "list": [1, 2, 3],
            "dict": {"nested": "value"}
        }
        serializer.save_file(data, output_file)
        decoded = serializer.load_file(output_file)
        assert decoded["string"] == data["string"]
        assert decoded["int"] == data["int"]
        assert decoded["float"] == data["float"]
        assert decoded["bool"] == data["bool"]
        assert decoded["none"] == data["none"]
        assert decoded["list"] == data["list"]
        assert decoded["dict"] == data["dict"]

    def test_handles_various_key_types(self, tmp_path):
        """Test handling various key types."""
        serializer = RocksdbSerializer()
        output_file = tmp_path / "keys.rocksdb"
        data = {
            "string_key": "value1",
            b"bytes_key": "value2",
            123: "value3",  # Integer key
        }
        serializer.save_file(data, output_file)
        decoded = serializer.load_file(output_file)
        assert decoded["string_key"] == "value1"
        assert decoded[b"bytes_key"] == "value2"
        assert decoded[123] == "value3"

    def test_overwrite_option(self, tmp_path):
        """Test overwrite option."""
        serializer = RocksdbSerializer()
        output_file = tmp_path / "overwrite.rocksdb"
        # Write initial data
        serializer.save_file({"key1": "value1"}, output_file)
        # Overwrite with new data
        serializer.save_file({"key2": "value2"}, output_file, overwrite=True)
        decoded = serializer.load_file(output_file)
        assert "key1" not in decoded
        assert decoded["key2"] == "value2"

    def test_error_if_exists_option(self, tmp_path):
        """Test error_if_exists option."""
        serializer = RocksdbSerializer()
        output_file = tmp_path / "exists.rocksdb"
        # Create database first
        serializer.save_file({"key1": "value1"}, output_file)
        # Try to create again with error_if_exists
        with pytest.raises(SerializationError, match="already exists"):
            serializer.save_file({"key2": "value2"}, output_file, error_if_exists=True)

    def test_create_if_missing_false(self, tmp_path):
        """Test create_if_missing=False option."""
        serializer = RocksdbSerializer()
        output_file = tmp_path / "missing.rocksdb"
        with pytest.raises(SerializationError, match="does not exist"):
            serializer.save_file({"key1": "value1"}, output_file, create_if_missing=False)

    def test_load_file_nonexistent_raises_error(self, tmp_path):
        """Test that loading nonexistent file raises error."""
        serializer = RocksdbSerializer()
        output_file = tmp_path / "nonexistent.rocksdb"
        with pytest.raises(SerializationError, match="does not exist"):
            serializer.load_file(output_file)

    def test_large_dataset(self, tmp_path):
        """Test handling large dataset."""
        serializer = RocksdbSerializer()
        output_file = tmp_path / "large.rocksdb"
        # Create large dataset
        data = {f"key_{i}": f"value_{i}" for i in range(1000)}
        serializer.save_file(data, output_file)
        decoded = serializer.load_file(output_file)
        assert len(decoded) == 1000
        assert decoded["key_0"] == "value_0"
        assert decoded["key_999"] == "value_999"

    def test_nested_data_structures(self, tmp_path):
        """Test nested data structures."""
        serializer = RocksdbSerializer()
        output_file = tmp_path / "nested.rocksdb"
        data = {
            "simple": "value",
            "nested": {
                "level1": {
                    "level2": "deep_value"
                }
            },
            "list": [1, 2, [3, 4], {"nested_in_list": "value"}]
        }
        serializer.save_file(data, output_file)
        decoded = serializer.load_file(output_file)
        assert decoded["simple"] == data["simple"]
        assert decoded["nested"]["level1"]["level2"] == data["nested"]["level1"]["level2"]
        assert decoded["list"] == data["list"]

    def test_empty_dict(self, tmp_path):
        """Test empty dictionary."""
        serializer = RocksdbSerializer()
        output_file = tmp_path / "empty.rocksdb"
        data = {}
        serializer.save_file(data, output_file)
        decoded = serializer.load_file(output_file)
        assert decoded == {}

    def test_special_characters_in_keys_and_values(self, tmp_path):
        """Test special characters in keys and values."""
        serializer = RocksdbSerializer()
        output_file = tmp_path / "special.rocksdb"
        data = {
            "key with spaces": "value with spaces",
            "key-with-dashes": "value-with-dashes",
            "key_with_underscores": "value_with_underscores",
            "key.with.dots": "value.with.dots",
            "unicode_key_测试": "unicode_value_测试"
        }
        serializer.save_file(data, output_file)
        decoded = serializer.load_file(output_file)
        assert decoded["key with spaces"] == data["key with spaces"]
        assert decoded["unicode_key_测试"] == data["unicode_key_测试"]

    def test_compression_options(self, tmp_path):
        """Test compression options."""
        serializer = RocksdbSerializer()
        output_file = tmp_path / "compressed.rocksdb"
        data = {"key1": "value1", "key2": "value2"}
        # Test with different compression types
        for compression in ['snappy', 'zlib', 'lz4', 'zstd']:
            test_file = tmp_path / f"compressed_{compression}.rocksdb"
            serializer.save_file(data, test_file, compression=compression)
            decoded = serializer.load_file(test_file)
            assert decoded == data

    def test_save_file_and_load_file_methods(self, tmp_path):
        """Test save_file and load_file methods."""
        serializer = RocksdbSerializer()
        output_file = tmp_path / "methods.rocksdb"
        data = {"key1": "value1", "key2": "value2"}
        # Use save_file method
        serializer.save_file(data, output_file)
        assert output_file.exists() or (output_file.parent / "methods.rocksdb").exists()
        # Use load_file method
        decoded = serializer.load_file(output_file)
        assert decoded == data

    def test_options_passed_correctly(self, tmp_path):
        """Test that options are passed correctly."""
        serializer = RocksdbSerializer()
        output_file = tmp_path / "options.rocksdb"
        data = {"key1": "value1"}
        # Test with various options
        serializer.save_file(
            data, 
            output_file,
            create_if_missing=True,
            sync=True,
            compression='snappy',
            max_open_files=100000
        )
        decoded = serializer.load_file(output_file)
        assert decoded == data
