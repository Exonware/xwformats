#!/usr/bin/env python3
#exonware/xwformats/src/exonware/xwformats/__init__.py
"""
xwformats: Enterprise Serialization Formats
Extended serialization format support for enterprise applications.
This library provides heavyweight formats that are typically used in
specialized domains (scientific computing, big data, enterprise systems).
Requirements: docs/REF_01_REQ.md, REF_14_DX (key code), REF_15_API.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.9.0.6
Generation Date: 02-Nov-2025
Formats provided:
- Schema: Protobuf, Avro, Parquet, Thrift, ORC, Cap'n Proto, FlatBuffers, Arrow (8)
- Scientific: HDF5, Feather, Zarr, NetCDF, MAT (5)
- Database: LMDB, GraphDB, LevelDB, RocksDB (4)
- Binary: BSON, UBJSON, Bincode, Postcard, Dill (5)
- Text: CSV, YAML, TOML, XML, RON (5)
Total: 27 enterprise formats (~98 MB dependencies)
Installation:
    # Install with all dependencies
    pip install exonware-xwformats[full]
    # Or minimal install (dependencies required separately)
    pip install exonware-xwformats
"""
# =============================================================================
# XWLAZY INTEGRATION - Auto-install missing dependencies silently (EARLY)
# =============================================================================
# Activate xwlazy BEFORE other imports to enable auto-installation of missing dependencies
# This enables silent auto-installation of missing libraries when they are imported

try:
    from exonware.xwlazy import auto_enable_lazy
    auto_enable_lazy(__package__ or "exonware.xwformats", mode="smart")
except ImportError:
    # xwlazy not installed - lazy mode simply stays disabled (normal behavior)
    pass
from .version import __version__
# Version metadata constants
__author__ = "eXonware Backend Team"
__email__ = "connect@exonware.com"
__company__ = "eXonware.com"
# Import all format serializers
from .formats import *
# Auto-register all serializers with UniversalCodecRegistry
from exonware.xwsystem.io.codec.registry import get_registry
_codec_registry = get_registry()
# Get all serializer classes from formats
from .formats.schema import (
    ParquetSerializer, ThriftSerializer,
    OrcSerializer, CapnProtoSerializer, FlatBuffersSerializer,
    ArrowSerializer,
)
# Protobuf - conditional import (may have version compatibility issues)
from .formats.schema import ProtobufSerializer  # May be None if not available
# Note: Avro excluded due to cramjam bug on Python 3.12 Windows - see KNOWN_ISSUES.md
from .formats.scientific import (
    Hdf5Serializer, FeatherSerializer, ZarrSerializer,
    NetcdfSerializer, MatSerializer,
)
from .formats.database import (
    LmdbSerializer, GraphDbSerializer, LeveldbSerializer,
)
# RocksDB - always available (has pure Python fallback if native library unavailable)
from .formats.database import RocksdbSerializer
from .formats.binary import (
    UbjsonSerializer,
    BsonSerializer,
    BincodeSerializer,
    PostcardSerializer,
    DillSerializer,
)
from .formats.text import (
    CsvSerializer,
    YamlSerializer,
    TomlSerializer,
    XmlSerializer,
    RonSerializer,
)
# Register all serializers
_serializers_to_register = [
    # Schema formats (Avro excluded - see KNOWN_ISSUES.md)
    ParquetSerializer, ThriftSerializer,
    OrcSerializer, CapnProtoSerializer, FlatBuffersSerializer,
    ArrowSerializer,
    # Scientific formats
    Hdf5Serializer, FeatherSerializer, ZarrSerializer,
    NetcdfSerializer, MatSerializer,
    # Database formats
    LmdbSerializer, GraphDbSerializer, LeveldbSerializer,
    # Binary formats
    UbjsonSerializer,
    BsonSerializer,
    BincodeSerializer,
    PostcardSerializer,
    DillSerializer,
    # Text formats
    CsvSerializer,
    YamlSerializer,
    TomlSerializer,
    XmlSerializer,
    RonSerializer,
]
# Add RocksdbSerializer (always available with pure Python fallback)
_serializers_to_register.append(RocksdbSerializer)
# Add ProtobufSerializer if available (may be None due to version issues)
if ProtobufSerializer is not None:
    _serializers_to_register.append(ProtobufSerializer)
# Register all serializers
for _serializer_class in _serializers_to_register:
    _codec_registry.register(_serializer_class)
# Import facade for main public API
from .facade import XWFormats
__all__ = [
    # Version info
    '__version__',
    '__author__',
    '__email__',
    '__company__',
    # Main facade
    'XWFormats',
    # All formats exported from formats module
    # (will be populated by formats/__init__.py)
]
