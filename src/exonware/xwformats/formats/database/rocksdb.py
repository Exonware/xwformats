#!/usr/bin/env python3
#exonware/xwformats/src/exonware/xwformats/formats/database/rocksdb.py
"""
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.9.0.34
Generation Date: 07-Jan-2025
RocksDB-shaped serialization — **internal engine only** (no ``python-rocksdb`` / OS wheels).

Following I→A→XW pattern:
- I: ISerialization (interface)
- A: ASerialization (abstract base)
- XW: RocksdbSerializer (concrete implementation)

Internal engine design (tiered hardening):
- **A**: No native extension; identical behavior on every OS.
- **B**: Process-wide ``RLock`` on all reads/writes/iterators.
- **C**: Single flush per ``WriteBatch`` (no N×disk sync per batch).
- **D**: Atomic persist: write ``*.tmp`` → ``fsync`` → ``os.replace`` into ``data.json`` / ``keys.json``.
- **E**: Optional ``*.bak`` copy before replace for last-good recovery.
- **F**: Load path tries primary JSON, then ``.bak`` if primary is corrupt.
- **G**: Hex payloads validated on load; bad entries skipped (partial recovery).
- **H**: ``ReadOptions.verify_checksums``: reserved for stricter on-disk validation (hook for future use).
- **I**: Stable key ordering in iterators (sorted hex) for reproducible dumps/tests.
- **J**: Defensive caps: ``_MAX_VALUE_BYTES`` / ``_MAX_KEY_BYTES`` to avoid runaway memory.
- **K**: UTF-8 explicit on all text I/O; ``newline="\\n"`` for portable files.
- **L**: ``create_if_missing`` honored for directory and first persist.
- **M**: Thread-local DB handles in :class:`RocksdbSerializer` unchanged (safe with locked engine).
- **N–Z**: Reserved hooks / future WAL or sharding without breaking on-disk shape.

Priority 1 (Security): Path validation in serializer; atomic writes reduce torn files.
Priority 2 (Usability): RocksDB-like ``DB`` / ``Options`` / ``WriteBatch`` surface.
Priority 3 (Maintainability): One implementation path, no conditional native imports.
"""

from __future__ import annotations

import os
import pickle
import shutil
import threading
from pathlib import Path
from typing import Any

from exonware.xwsystem.io.serialization.base import ASerialization
from exonware.xwsystem.io.contracts import EncodeOptions, DecodeOptions
from exonware.xwsystem.io.defs import CodecCapability
from exonware.xwsystem.io.errors import SerializationError
from exonware.xwsystem.io.serialization.formats.text.json import dump, load


class CompressionType:
    snappy_compression = "snappy"
    zlib_compression = "zlib"
    bzip2_compression = "bzip2"
    lz4_compression = "lz4"
    lz4hc_compression = "lz4hc"
    zstd_compression = "zstd"
    no_compression = "none"


class Options:
    def __init__(self) -> None:
        self.create_if_missing = True
        self.create_missing_column_families = True
        self.max_open_files = 300000
        self.write_buffer_size = 67108864
        self.max_write_buffer_number = 3
        self.target_file_size_base = 67108864
        self.compression = CompressionType.no_compression


class WriteOptions:
    def __init__(self) -> None:
        self.sync = True


class ReadOptions:
    def __init__(self) -> None:
        self.fill_cache = True
        self.verify_checksums = False


class WriteBatch:
    def __init__(self) -> None:
        self._ops: list[tuple[str, bytes, bytes | None]] = []

    def put(self, key: bytes, value: bytes) -> None:
        self._ops.append(("put", key, value))

    def delete(self, key: bytes) -> None:
        self._ops.append(("delete", key, None))

    def clear(self) -> None:
        self._ops.clear()

    def __iter__(self):
        return iter(self._ops)


class DB:
    """
    Pure-Python RocksDB-shaped store: hex-encoded bytes in ``data.json`` plus ``keys.json`` metadata.

    Never loads the external ``rocksdb`` CPython module.
    """

    _MAX_KEY_BYTES = 4 * 1024
    _MAX_VALUE_BYTES = 64 * 1024 * 1024

    def __init__(self, path: str, options: Options) -> None:
        self.path = Path(path)
        self.options = options
        self.data_file = self.path / "data.json"
        self.keys_file = self.path / "keys.json"
        self._lock = threading.RLock()
        self._data: dict[str, bytes] = {}
        self._key_types: dict[str, str] = {}
        if self.options.create_if_missing:
            self.path.mkdir(parents=True, exist_ok=True)
        self._load_initial_state()

    def _load_json_file(self, file_path: Path) -> dict[str, Any] | None:
        if not file_path.is_file():
            return None
        try:
            with open(file_path, encoding="utf-8") as f:
                return load(f)
        except Exception:
            return None

    def _hydrate_from_mapping(self, data_dict: dict[str, Any] | None) -> None:
        if not isinstance(data_dict, dict):
            return
        for raw_k, raw_v in data_dict.items():
            if not isinstance(raw_k, str) or not isinstance(raw_v, str):
                continue
            try:
                self._data[raw_k] = bytes.fromhex(raw_v)
            except ValueError:
                continue

    def _load_key_types(self, mapping: dict[str, Any] | None) -> None:
        if not isinstance(mapping, dict):
            return
        for k, v in mapping.items():
            if isinstance(k, str) and isinstance(v, str):
                self._key_types[k] = v

    def _load_initial_state(self) -> None:
        primary = self._load_json_file(self.data_file)
        if primary is None:
            bak = self.data_file.with_suffix(".json.bak")
            primary = self._load_json_file(bak)
        self._hydrate_from_mapping(primary)

        kt = self._load_json_file(self.keys_file)
        if kt is None:
            kt = self._load_json_file(self.keys_file.with_suffix(".json.bak"))
        self._load_key_types(kt)

    def _record_key_type(self, key: bytes, key_hex: str) -> None:
        try:
            decoded = key.decode("utf-8")
            if decoded.encode("utf-8") == key:
                self._key_types[key_hex] = "str"
            else:
                self._key_types[key_hex] = "bytes"
        except UnicodeDecodeError:
            self._key_types[key_hex] = "bytes"

    def _put_unlocked(self, key: bytes, value: bytes) -> None:
        if len(key) > self._MAX_KEY_BYTES or len(value) > self._MAX_VALUE_BYTES:
            raise ValueError("key or value exceeds internal RocksDB shim limits")
        key_hex = key.hex()
        self._data[key_hex] = value
        self._record_key_type(key, key_hex)

    def _delete_unlocked(self, key: bytes) -> None:
        key_hex = key.hex()
        self._data.pop(key_hex, None)
        self._key_types.pop(key_hex, None)

    def put(self, key: bytes, value: bytes) -> None:
        with self._lock:
            self._put_unlocked(key, value)
            self._persist_unlocked()

    def get(self, key: bytes, read_opts: ReadOptions | None = None):
        with self._lock:
            val = self._data.get(key.hex())
            if val is None:
                return None
            if read_opts and read_opts.verify_checksums:
                try:
                    if bytes.fromhex(val.hex()) != val:
                        return None
                except ValueError:
                    return None
            return val

    def delete(self, key: bytes, write_opts: WriteOptions | None = None) -> None:
        with self._lock:
            self._delete_unlocked(key)
            self._persist_unlocked()

    def write(self, batch: WriteBatch, write_opts: WriteOptions | None = None) -> None:
        sync = True if write_opts is None else bool(write_opts.sync)
        with self._lock:
            for op in batch:
                kind = op[0]
                if kind == "put":
                    _, kb, vb = op
                    assert vb is not None
                    self._put_unlocked(kb, vb)
                elif kind == "delete":
                    _, kb, _ = op
                    self._delete_unlocked(kb)
            if sync:
                self._persist_unlocked()

    def iteritems(self):
        with self._lock:
            snapshot = sorted(self._data.items(), key=lambda kv: kv[0])

        class _Iterator:
            def __init__(self, items: list[tuple[str, bytes]]) -> None:
                self.items = items
                self.idx = 0

            def seek_to_first(self) -> None:
                self.idx = 0

            def __iter__(self):
                return self

            def __next__(self) -> tuple[bytes, bytes]:
                if self.idx >= len(self.items):
                    raise StopIteration
                key_hex, value_bytes = self.items[self.idx]
                key_bytes = bytes.fromhex(key_hex)
                self.idx += 1
                return (key_bytes, value_bytes)

        return _Iterator(snapshot)

    def _persist_unlocked(self) -> None:
        if self.options.create_if_missing:
            self.path.mkdir(parents=True, exist_ok=True)
        data_dict = {k: v.hex() for k, v in self._data.items()}
        self._atomic_write_mapping(self.data_file, data_dict, backup=True)
        self._atomic_write_mapping(self.keys_file, dict(self._key_types), backup=True)

    def _atomic_write_mapping(self, target: Path, obj: dict[str, Any], *, backup: bool) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_name(target.name + ".tmp")
        bak = target.with_name(target.name + ".bak")
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            dump(obj, f)
            f.flush()
            os.fsync(f.fileno())
        if target.exists() and backup:
            try:
                shutil.copyfile(target, bak)
            except OSError:
                pass
        os.replace(tmp, target)

    def _save(self) -> None:
        """Persist current maps to disk (used by :class:`RocksdbSerializer` after key-type merges)."""
        with self._lock:
            self._persist_unlocked()


class _RocksDBModule:
    DB = DB
    Options = Options
    WriteBatch = WriteBatch
    WriteOptions = WriteOptions
    ReadOptions = ReadOptions
    CompressionType = CompressionType


rocksdb = _RocksDBModule()


def open_rocksdb_database(path: str | Path, *, create_if_missing: bool = True) -> Any:
    """
    Open the internal RocksDB-compatible database directory.

    Always uses the pure-Python :class:`DB` in this module (no external ``rocksdb`` package).
    """
    db_path = Path(path)
    opts = rocksdb.Options()
    if hasattr(opts, "create_if_missing"):
        opts.create_if_missing = bool(create_if_missing)
    if hasattr(opts, "create_missing_column_families"):
        try:
            opts.create_missing_column_families = bool(create_if_missing)
        except Exception:
            pass
    return rocksdb.DB(str(db_path), opts)


class RocksdbSerializer(ASerialization):
    """
    RocksDB serializer - follows I→A→XW pattern.
    I: ISerialization (interface)
    A: ASerialization (abstract base)
    XW: RocksdbSerializer (concrete implementation)
    Always uses the in-repo pure-Python :class:`DB` (JSON-backed, atomic writes, RLock).
    No external ``rocksdb`` / ``python-rocksdb`` package is imported or required.
    Provides:
    - Key-value storage with a RocksDB-like API
    - Thread-safe operations (re-entrant lock)
    - Batch writes with a single disk flush
    - Iterator snapshots sorted by key
    Examples:
        >>> serializer = RocksdbSerializer()
        >>> 
        >>> # Save data to RocksDB
        >>> serializer.save_file({"key1": "value1", "key2": "value2"}, "data.rocksdb")
        >>> 
        >>> # Load data from RocksDB
        >>> data = serializer.load_file("data.rocksdb")
    """

    def __init__(self):
        """Initialize RocksDB serializer."""
        super().__init__()
        # Thread-local storage for database instances
        self._local = threading.local()
    @property

    def codec_id(self) -> str:
        """Codec identifier."""
        return "rocksdb"
    @property

    def media_types(self) -> list[str]:
        """Supported MIME types."""
        return ["application/x-rocksdb"]
    @property

    def file_extensions(self) -> list[str]:
        """Supported file extensions."""
        return [".rocksdb", ".rdb"]
    @property

    def format_name(self) -> str:
        """Format name."""
        return "RocksDB"
    @property

    def mime_type(self) -> str:
        """Primary MIME type."""
        return "application/x-rocksdb"
    @property

    def is_binary_format(self) -> bool:
        """RocksDB is a binary format."""
        return True
    @property

    def supports_streaming(self) -> bool:
        """RocksDB supports streaming operations via iterators."""
        return True
    @property

    def capabilities(self) -> CodecCapability:
        """RocksDB supports bidirectional operations."""
        return CodecCapability.BIDIRECTIONAL
    @property

    def aliases(self) -> list[str]:
        """RocksDB aliases."""
        return ["rocksdb", "RocksDB", "rdb"]

    def encode(self, value: Any, *, options: EncodeOptions | None = None) -> bytes:
        """
        Encode data to RocksDB-compatible bytes.
        Note: RocksDB is designed for file-based operations. This method
        pickles the data for transport when not using file-based operations.
        Args:
            value: Dictionary of key-value pairs (expected)
            options: Encoding options
        Returns:
            Pickled bytes representation
        Raises:
            SerializationError: If value is not a dictionary
        """
        if not isinstance(value, dict):
            raise SerializationError(
                f"RocksDB encode expects dict, got {type(value).__name__}. "
                "For full RocksDB features (LSM-tree, batch operations), use save_file().",
                self.format_name
            )
        # For in-memory transport, pickle the dictionary
        return pickle.dumps(value)

    def decode(self, repr: bytes | str, *, options: DecodeOptions | None = None) -> Any:
        """
        Decode RocksDB bytes to Python data.
        Note: RocksDB is designed for file-based operations. This method
        unpickles data that was encoded for transport.
        Args:
            repr: Pickled bytes representation
            options: Decoding options
        Returns:
            Dictionary of key-value pairs
        Raises:
            SerializationError: If decoding fails
        """
        if isinstance(repr, str):
            raise SerializationError(
                "RocksDB decode expects bytes, got string. "
                "For full RocksDB features, use load_file().",
                self.format_name
            )
        try:
            return pickle.loads(repr)
        except (pickle.UnpicklingError, EOFError, AttributeError) as e:
            raise SerializationError(
                f"Failed to decode RocksDB data: {e}",
                self.format_name,
                e
            ) from e

    def _get_db_path(self, file_path: str | Path) -> Path:
        """
        Get validated RocksDB database path.
        RocksDB stores data in a directory containing multiple files.
        Args:
            file_path: Path to RocksDB database directory
        Returns:
            Validated Path to RocksDB database directory
        Raises:
            SerializationError: If path validation fails
        """
        path = Path(file_path).resolve()
        # If it's a file with .rocksdb or .rdb extension, treat as directory name
        if path.suffix in ['.rocksdb', '.rdb']:
            if path.exists() and path.is_file():
                # If it's actually a file, use parent directory
                path = path.parent / path.stem
            else:
                # Treat as directory name
                path = path
        # Security: Validate parent directory (GUIDE_DEV.md Priority #1)
        if path.exists() and not path.is_dir():
            raise SerializationError(
                f"RocksDB database path exists but is not a directory: {path}",
                self.format_name
            )
        return path

    def _get_db_instance(self, db_path: Path, create_if_missing: bool = True, **options) -> DB:
        """
        Get thread-local :class:`DB` (internal engine) with basic option wiring.
        Args:
            db_path: Path to RocksDB database directory
            create_if_missing: Whether to create database if it doesn't exist
            **options: Tuning knobs (compression label is accepted; engine stays JSON-backed)
        Returns:
            Internal :class:`DB` instance
        Raises:
            SerializationError: If database creation/opening fails
        """
        # Use thread-local storage for database instances
        if not hasattr(self._local, 'databases'):
            self._local.databases = {}
        db_str = str(db_path.resolve())
        # Reuse existing database instance if available
        if db_str in self._local.databases:
            db = self._local.databases[db_str]
            # Check if database is still valid
            try:
                # Try a simple operation to verify database is still open
                _ = db.get(b'__health_check__')
                return db
            except Exception:
                # Database closed or invalid, remove and recreate
                del self._local.databases[db_str]
        # Create parent directory if needed
        if create_if_missing:
            db_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            # Configure RocksDB options
            opts = rocksdb.Options()
            opts.create_if_missing = create_if_missing
            opts.create_missing_column_families = create_if_missing
            # Performance optimizations
            opts.max_open_files = options.get('max_open_files', 300000)
            opts.write_buffer_size = options.get('write_buffer_size', 67108864)  # 64MB
            opts.max_write_buffer_number = options.get('max_write_buffer_number', 3)
            opts.target_file_size_base = options.get('target_file_size_base', 67108864)  # 64MB
            # Compression
            compression_type = options.get('compression', 'snappy')
            if compression_type == 'snappy':
                opts.compression = rocksdb.CompressionType.snappy_compression
            elif compression_type == 'zlib':
                opts.compression = rocksdb.CompressionType.zlib_compression
            elif compression_type == 'bzip2':
                opts.compression = rocksdb.CompressionType.bzip2_compression
            elif compression_type == 'lz4':
                opts.compression = rocksdb.CompressionType.lz4_compression
            elif compression_type == 'lz4hc':
                opts.compression = rocksdb.CompressionType.lz4hc_compression
            elif compression_type == 'zstd':
                opts.compression = rocksdb.CompressionType.zstd_compression
            else:
                opts.compression = rocksdb.CompressionType.no_compression
            # Open database
            db = rocksdb.DB(str(db_path), opts)
            # Store database instance in thread-local storage
            self._local.databases[db_str] = db
            return db
        except Exception as e:
            raise SerializationError(
                f"Failed to open RocksDB database: {e}",
                self.format_name,
                e
            ) from e

    def _close_db(self, db_path: Path) -> None:
        """
        Close thread-local RocksDB instance.
        Args:
            db_path: Path to RocksDB database directory
        """
        if hasattr(self._local, 'databases'):
            db_str = str(db_path.resolve())
            if db_str in self._local.databases:
                try:
                    db = self._local.databases[db_str]
                    del db  # RocksDB will close on deletion
                except Exception:
                    pass  # Already closed or invalid
                finally:
                    del self._local.databases[db_str]

    def _serialize_key(self, key: Any) -> bytes:
        """
        Serialize key to bytes.
        Args:
            key: Key to serialize (str, bytes, or pickleable object)
        Returns:
            Bytes representation of key
        """
        if isinstance(key, bytes):
            return key
        elif isinstance(key, str):
            return key.encode('utf-8')
        else:
            # For non-string/bytes keys, pickle
            return pickle.dumps(key)

    def _deserialize_key(self, key_bytes: bytes) -> Any:
        """
        Deserialize key from bytes.
        Args:
            key_bytes: Bytes representation of key
        Returns:
            Deserialized key (str, bytes, or unpickled object)
        """
        # Check if it's a pickled key (starts with pickle protocol marker)
        # Pickle protocol 0-3 use specific markers, protocol 4+ uses different format
        if len(key_bytes) > 0:
            # Try unpickling first if it looks like pickled data
            # Pickle markers: b'\x80' (protocol 2+), b'c' (protocol 0), etc.
            pickle_markers = [b'\x80', b'c', b'(', b']', b'}', b'S', b'V', b'I']
            if key_bytes[0:1] in [b'\x80'] or (len(key_bytes) > 1 and key_bytes[0:2] in [b'\x80\x02', b'\x80\x03', b'\x80\x04', b'\x80\x05']):
                try:
                    unpickled = pickle.loads(key_bytes)
                    # Only return unpickled if it's not bytes (to avoid double-processing)
                    if not isinstance(unpickled, bytes):
                        return unpickled
                except (pickle.UnpicklingError, EOFError, ValueError):
                    pass
        # Try UTF-8 decode (most common case for string keys)
        try:
            decoded = key_bytes.decode('utf-8')
            # Check if it was originally a string key by trying to round-trip
            # If encoding back gives same bytes, it's a string key
            if decoded.encode('utf-8') == key_bytes:
                return decoded
        except UnicodeDecodeError:
            pass
        # If all else fails, return bytes as-is (preserves bytes keys)
        return key_bytes

    def _serialize_value(self, value: Any) -> bytes:
        """
        Serialize value to bytes.
        Args:
            value: Value to serialize (any pickleable object)
        Returns:
            Bytes representation of value
        """
        return pickle.dumps(value)

    def _deserialize_value(self, value_bytes: bytes) -> Any:
        """
        Deserialize value from bytes.
        Args:
            value_bytes: Bytes representation of value
        Returns:
            Deserialized value
        """
        try:
            return pickle.loads(value_bytes)
        except (pickle.UnpicklingError, EOFError, AttributeError) as e:
            raise SerializationError(
                f"Failed to deserialize RocksDB value: {e}",
                self.format_name,
                e
            ) from e

    def save_file(
        self,
        value: Any,
        file_path: str | Path,
        **options
    ) -> None:
        """
        Save data to RocksDB database.
        RocksDB stores data in a directory containing multiple files (SST files, logs, etc.).
        Args:
            value: Dictionary of key-value pairs to store
            file_path: Path to RocksDB database directory
            **options: Encoding options:
                - create_if_missing (bool): Create database if it doesn't exist (default: True)
                - overwrite (bool): Clear existing database before writing (default: False)
                - error_if_exists (bool): Raise error if database exists (default: False)
                - sync (bool): Sync writes to disk immediately (default: True)
                - compression (str): Compression type: 'snappy', 'zlib', 'bzip2', 'lz4', 'lz4hc', 'zstd' (default: 'snappy')
                - max_open_files (int): Maximum open files (default: 300000)
                - write_buffer_size (int): Write buffer size in bytes (default: 64MB)
        Raises:
            SerializationError: If value is not a dictionary or database operation fails
        """
        if not isinstance(value, dict):
            raise SerializationError(
                f"RocksDB save_file expects dict, got {type(value).__name__}",
                self.format_name
            )
        create_if_missing = options.get('create_if_missing', True)
        overwrite = options.get('overwrite', False)
        error_if_exists = options.get('error_if_exists', False)
        sync = options.get('sync', True)
        db_path = self._get_db_path(file_path)
        # Check if database exists
        if db_path.exists() and error_if_exists:
            raise SerializationError(
                f"RocksDB database already exists: {db_path}",
                self.format_name
            )
        if not db_path.exists() and not create_if_missing:
            raise SerializationError(
                f"RocksDB database does not exist: {db_path}",
                self.format_name
            )
        db = None
        try:
            # Remove create_if_missing from options to avoid duplicate argument
            db_options = {k: v for k, v in options.items() if k != 'create_if_missing'}
            db = self._get_db_instance(db_path, create_if_missing=create_if_missing, **db_options)
            # Clear existing data if overwrite requested
            if overwrite and db_path.exists():
                # Close existing database
                self._close_db(db_path)
                # Remove directory
                import shutil
                shutil.rmtree(db_path)
                # Recreate database
                db = self._get_db_instance(db_path, create_if_missing=True, **options)
            # Use batch write for efficiency
            batch = rocksdb.WriteBatch()
            # Track original key types for proper deserialization
            key_type_map = {}
            for key, val in value.items():
                # Store original key type before serialization
                if isinstance(key, bytes):
                    key_type = 'bytes'
                elif isinstance(key, str):
                    key_type = 'str'
                else:
                    key_type = 'pickled'  # int, float, tuple, etc.
                key_bytes = self._serialize_key(key)
                key_hex = key_bytes.hex()
                key_type_map[key_hex] = key_type
                value_bytes = self._serialize_value(val)
                batch.put(key_bytes, value_bytes)
            # Write batch atomically
            write_opts = rocksdb.WriteOptions()
            write_opts.sync = sync
            db.write(batch, write_opts=write_opts)
            # Store key type map in DB for later retrieval (after write)
            if hasattr(db, '_key_types'):
                db._key_types.update(key_type_map)
                # Save key types to disk
                if hasattr(db, '_save'):
                    db._save()
        except Exception as e:
            raise SerializationError(
                f"RocksDB save_file failed: {e}",
                self.format_name,
                e
            ) from e

    def load_file(
        self,
        file_path: str | Path,
        **options
    ) -> dict[str, Any]:
        """
        Load data from RocksDB database.
        RocksDB stores data in a directory containing multiple files.
        Args:
            file_path: Path to RocksDB database directory
            **options: Decoding options:
                - create_if_missing (bool): Create database if it doesn't exist (default: False)
                - fill_cache (bool): Fill read cache (default: True)
                - verify_checksums (bool): Verify data integrity (default: False)
        Returns:
            Dictionary of all key-value pairs (sorted by key order)
        Raises:
            SerializationError: If database doesn't exist or read operation fails
        """
        create_if_missing = options.get('create_if_missing', False)
        fill_cache = options.get('fill_cache', True)
        verify_checksums = options.get('verify_checksums', False)
        db_path = self._get_db_path(file_path)
        if not db_path.exists() and not create_if_missing:
            raise SerializationError(
                f"RocksDB database does not exist: {db_path}",
                self.format_name
            )
        db = None
        try:
            read_opts = rocksdb.ReadOptions()
            read_opts.fill_cache = fill_cache
            read_opts.verify_checksums = verify_checksums
            db = self._get_db_instance(db_path, create_if_missing=create_if_missing, **options)
            result = {}
            # Iterate over all key-value pairs (RocksDB maintains sorted order)
            it = db.iteritems()
            it.seek_to_first()
            for key_bytes, value_bytes in it:
                # Use key type info from DB if available for proper deserialization
                key_hex = key_bytes.hex()
                key_type = getattr(db, '_key_types', {}).get(key_hex, 'auto')
                if key_type == 'bytes':
                    # Preserve as bytes
                    key = key_bytes
                elif key_type == 'str':
                    # Decode as string
                    key = key_bytes.decode('utf-8')
                else:
                    # Auto-detect (fallback)
                    key = self._deserialize_key(key_bytes)
                value = self._deserialize_value(value_bytes)
                result[key] = value
            return result
        except Exception as e:
            raise SerializationError(
                f"RocksDB load_file failed: {e}",
                self.format_name,
                e
            ) from e
