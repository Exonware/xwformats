#!/usr/bin/env python3
#exonware/xwformats/src/exonware/xwformats/formats/schema/__init__.py
"""Schema-based enterprise serialization formats.
Note: Avro import is separate due to known cramjam bug on Python 3.12 Windows.
This is an external dependency issue, not a bug in xwformats.
See KNOWN_ISSUES.md for details.
"""
# Protobuf - optional, may have version compatibility issues

try:
    from .protobuf import ProtobufSerializer
except (ImportError, AttributeError, Exception):
    # Protobuf not available or has version issues - skip it
    ProtobufSerializer = None  # type: ignore
from .parquet import ParquetSerializer
from .thrift import ThriftSerializer
from .orc import OrcSerializer
from .capnproto import CapnProtoSerializer
from .flatbuffers import FlatBuffersSerializer
from .avro import AvroSerializer
from .arrow import ArrowSerializer
__all__ = [
    "ProtobufSerializer",
    "ParquetSerializer",
    "ThriftSerializer",
    "OrcSerializer",
    "CapnProtoSerializer",
    "FlatBuffersSerializer",
    "AvroSerializer",
    "ArrowSerializer",
]
