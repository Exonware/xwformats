#!/usr/bin/env python3
#exonware/xwformats/src/exonware/xwformats/__init__.py
"""
xwformats: Enterprise Serialization Formats

Extended serialization format support for enterprise applications.
This library provides heavyweight formats that are typically used in
specialized domains (scientific computing, big data, enterprise systems).

Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.9.0.32
Generation Date: 02-Nov-2025

Formats provided:
- Schema: Protobuf, Avro, Parquet, Thrift, ORC, Cap'n Proto, FlatBuffers
- Scientific: HDF5, Feather, Zarr, NetCDF, MAT
- Database: LMDB, GraphDB, LevelDB
- Binary: UBJSON, Bincode, Dill, Postcard (xwformats). **BSON** (and MsgPack, CBOR, …) live in **xwsystem** — not registered or exported from xwformats
- Text: **RON** only in xwformats. CSV, JSON, TOML, YAML, XML live in **xwsystem**
  (``exonware.xwsystem.io.serialization.formats.text``); import/register them from
  there — xwformats does **not** add them to the shared registry.

Total: 17+ enterprise formats (~87 MB dependencies with xwsystem[full])

Installation:
    pip install exonware-xwformats              # pulls exonware-xwsystem[full] (TOML/YAML/XML/JSON stack, etc.)
    pip install exonware-xwformats[lazy]        # lazy stack
    pip install exonware-xwformats[full]        # extra heavyweight format backends (see pyproject.toml)
    pip install exonware-xwformats[dev]         # pytest, black, mypy, …
"""

from exonware.xwlazy import config_package_lazy_install_enabled

config_package_lazy_install_enabled(
    __package__ or "exonware.xwformats",
    enabled=True,
    mode="smart",
)

from .version import (
    __version__,
    __author__,
    __email__,
    __company__,
)

# Import all format serializers
from .formats import *  # noqa: F401,F403

# Auto-register all serializers with UniversalCodecRegistry
from exonware.xwsystem.io.codec.registry import get_registry

_codec_registry = get_registry()

# Get all serializer classes from formats
from .formats.schema import (
    XWProtobufSerializer,
    XWParquetSerializer,
    XWThriftSerializer,
    XWOrcSerializer,
    XWCapnProtoSerializer,
    XWFlatBuffersSerializer,
    ArrowSerializer,
)
# Note: Avro excluded due to cramjam bug on Python 3.12 Windows — see docs/_archive/KNOWN_ISSUES.md
from .formats.scientific import (
    XWHdf5Serializer,
    XWFeatherSerializer,
    XWZarrSerializer,
    XWNetcdfSerializer,
    XWMatSerializer,
)
from .formats.database import (
    XWLmdbSerializer,
    XWGraphDbSerializer,
    XWLeveldbSerializer,
    RocksdbSerializer,
)
from .formats.binary import (
    BincodeSerializer,
    DillSerializer,
    PostcardSerializer,
    XWUbjsonSerializer,
)
from .formats.text import RonSerializer


# Register all serializers (xwformats-owned only; xwsystem text codecs are separate)
for _serializer_class in [
    # Schema formats (Avro excluded — see docs/_archive/KNOWN_ISSUES.md)
    XWProtobufSerializer,
    XWParquetSerializer,
    XWThriftSerializer,
    XWOrcSerializer,
    XWCapnProtoSerializer,
    XWFlatBuffersSerializer,
    ArrowSerializer,
    # Scientific formats
    XWHdf5Serializer,
    XWFeatherSerializer,
    XWZarrSerializer,
    XWNetcdfSerializer,
    XWMatSerializer,
    # Database formats
    XWLmdbSerializer,
    XWGraphDbSerializer,
    XWLeveldbSerializer,
    RocksdbSerializer,
    # Binary formats
    BincodeSerializer,
    DillSerializer,
    PostcardSerializer,
    XWUbjsonSerializer,
    RonSerializer,
]:
    _codec_registry.register(_serializer_class)

# Main public facade
from .facade import XWFormats


__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    "__company__",
    # High-level façade
    "XWFormats",
]

