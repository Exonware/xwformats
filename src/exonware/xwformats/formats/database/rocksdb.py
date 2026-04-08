#!/usr/bin/env python3
#exonware/xwformats/src/exonware/xwformats/formats/database/rocksdb.py
"""
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.9.0.27
Generation Date: 07-Jan-2025
RocksDB Serialization - High-Performance Key-Value Store
RocksDB is a persistent key-value store for fast storage based on a log-structured
merge-tree (LSM) data structure. It's optimized for fast storage and is used by
many production systems including Facebook, LinkedIn, and Netflix.
Following I→A→XW pattern:
- I: ISerialization (interface)
- A: ASerialization (abstract base)
- XW: RocksdbSerializer (concrete implementation)
Priority 1 (Security): Secure file operations with path validation
Priority 2 (Usability): Simple key-value API compatible with RocksDB interface
Priority 3 (Maintainability): Clean, well-structured code following design patterns
Priority 4 (Performance): Fast LSM-tree operations with optimized settings
Priority 5 (Extensibility): Supports RocksDB options and advanced features
"""

from typing import Any
from pathlib import Path
import pickle
import threading
from exonware.xwsystem.io.serialization.base import ASerialization
from exonware.xwsystem.io.contracts import EncodeOptions, DecodeOptions
from exonware.xwsystem.io.defs import CodecCapability
from exonware.xwsystem.io.errors import SerializationError

try:
    import rocksdb as _rocksdb_mod
except ImportError:
    _rocksdb_mod = None  # type: ignore[assignment, misc]

_has_native_rocksdb = False
if _rocksdb_mod is not None:
    # Lazy-import shims (e.g. xwlazy) may succeed at `import rocksdb` but fail
    # when attributes are resolved; treat that as "no native binding".
    try:
        _has_native_rocksdb = hasattr(_rocksdb_mod, "DB") and hasattr(
            _rocksdb_mod, "Options"
        )
    except (ImportError, ModuleNotFoundError, OSError):
        _has_native_rocksdb = False

if _has_native_rocksdb:
    rocksdb = _rocksdb_mod
else:
    # Pure Python fallback (e.g. Windows or env without python-rocksdb): JSON-backed KV store.
    from exonware.xwsystem.io.serialization.formats.text.json import dump, load, loads
    from pathlib import Path as _Path

    class CompressionType:
        snappy_compression = "snappy"
        zlib_compression = "zlib"
        bzip2_compression = "bzip2"
        lz4_compression = "lz4"
        lz4hc_compression = "lz4hc"
        zstd_compression = "zstd"
        no_compression = "none"

    class Options:
        def __init__(self):
            self.create_if_missing = True
            self.create_missing_column_families = True
            self.max_open_files = 300000
            self.write_buffer_size = 67108864
            self.max_write_buffer_number = 3
            self.target_file_size_base = 67108864
            self.compression = CompressionType.no_compression

    class WriteOptions:
        def __init__(self):
            self.sync = True

    class ReadOptions:
        def __init__(self):
            self.fill_cache = True
            self.verify_checksums = False

    class WriteBatch:
        def __init__(self):
            self._ops = []

        def put(self, key: bytes, value: bytes):
            self._ops.append(("put", key, value))

        def delete(self, key: bytes):
            self._ops.append(("delete", key))

        def clear(self):
            self._ops.clear()

        def __iter__(self):
            return iter(self._ops)

    class DB:
        """Pure Python RocksDB-shaped implementation using JSON files."""

        def __init__(self, path: str, options: Options):
            self.path = _Path(path)
            self.options = options
            self.data_file = self.path / "data.json"
            self.keys_file = self.path / "keys.json"
            self._data: dict[str, bytes] = {}
            self._key_types: dict[str, str] = {}
            if self.options.create_if_missing:
                self.path.mkdir(parents=True, exist_ok=True)
            if self.data_file.exists():
                try:
                    with open(self.data_file, "rb") as f:
                        content = f.read().decode("utf-8")
                        data_dict = loads(content)
                        self._data = {k: bytes.fromhex(v) for k, v in data_dict.items()}
                    if self.keys_file.exists():
                        with open(self.keys_file, "r") as f:
                            self._key_types = load(f)
                except Exception:
                    self._data = {}
                    self._key_types = {}

        def put(self, key: bytes, value: bytes):
            key_hex = key.hex()
            self._data[key_hex] = value
            try:
                decoded = key.decode("utf-8")
                if decoded.encode("utf-8") == key:
                    self._key_types[key_hex] = "str"
                else:
                    self._key_types[key_hex] = "bytes"
            except UnicodeDecodeError:
                self._key_types[key_hex] = "bytes"
            self._save()

        def get(self, key: bytes, read_opts=None):
            return self._data.get(key.hex())

        def delete(self, key: bytes, write_opts=None):
            key_hex = key.hex()
            if key_hex in self._data:
                del self._data[key_hex]
                self._save()

        def write(self, batch: WriteBatch, write_opts: WriteOptions = None):
            for op in batch:
                if op[0] == "put":
                    _, key, value = op
                    self.put(key, value)
                elif op[0] == "delete":
                    _, key = op
                    self.delete(key)
            if write_opts and write_opts.sync:
                self._save()

        def iteritems(self):
            class _Iterator:
                def __init__(self, db_instance: "DB"):
                    self.items = list(db_instance._data.items())
                    self.idx = 0

                def seek_to_first(self):
                    self.idx = 0

                def __iter__(self):
                    return self

                def __next__(self):
                    if self.idx >= len(self.items):
                        raise StopIteration
                    key_hex, value_bytes = self.items[self.idx]
                    key_bytes = bytes.fromhex(key_hex)
                    self.idx += 1
                    return (key_bytes, value_bytes)

            return _Iterator(self)

        def _save(self):
            if self.options.create_if_missing:
                self.path.mkdir(parents=True, exist_ok=True)
            data_dict = {k: v.hex() for k, v in self._data.items()}
            with open(self.data_file, "w") as f:
                dump(data_dict, f)
            with open(self.keys_file, "w") as f:
                dump(self._key_types, f)

    class _RocksDBModule:
        DB = DB
        Options = Options
        WriteBatch = WriteBatch
        WriteOptions = WriteOptions
        ReadOptions = ReadOptions
        CompressionType = CompressionType

    rocksdb = _RocksDBModule()  # type: ignore[assignment, misc]


class RocksdbSerializer(ASerialization):
    """
    RocksDB serializer - follows I→A→XW pattern.
    I: ISerialization (interface)
    A: ASerialization (abstract base)
    XW: RocksdbSerializer (concrete implementation)
    Uses ``python-rocksdb`` when importable (typical on Linux/macOS with the extra
    installed); otherwise a pure-Python JSON-backed store with the same surface API
    (typical on Windows).
    RocksDB provides:
    - High-performance key-value storage
    - LSM-tree structure for fast writes
    - Configurable compression and caching
    - Thread-safe operations
    - Batch write operations
    - Snapshot support
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

    def _get_db_instance(self, db_path: Path, create_if_missing: bool = True, **options) -> rocksdb.DB:
        """
        Get thread-local RocksDB instance with proper configuration.
        Args:
            db_path: Path to RocksDB database directory
            create_if_missing: Whether to create database if it doesn't exist
            **options: RocksDB options
        Returns:
            RocksDB database instance
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
