#!/usr/bin/env python3
"""
#exonware/xwformats/src/exonware/xwformats/defs.py
Type definitions and enums for xwformats.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.9.0.26
Generation Date: 07-Jan-2025
"""

from enum import Enum


class FormatCategory(Enum):
    """Format categories."""
    SCHEMA = "schema"
    SCIENTIFIC = "scientific"
    DATABASE = "database"
    BINARY = "binary"
    TEXT = "text"


class FormatType(Enum):
    """Format types."""
    PROTOBUF = "protobuf"
    AVRO = "avro"
    PARQUET = "parquet"
    THRIFT = "thrift"
    ORC = "orc"
    CAPNPROTO = "capnproto"
    FLATBUFFERS = "flatbuffers"
    HDF5 = "hdf5"
    FEATHER = "feather"
    ZARR = "zarr"
    NETCDF = "netcdf"
    MAT = "mat"
    LMDB = "lmdb"
    GRAPHDB = "graphdb"
    LEVELDB = "leveldb"
    BSON = "bson"
    UBJSON = "ubjson"
    CSV = "csv"
    YAML = "yaml"
    TOML = "toml"
    XML = "xml"


class ConversionMode(Enum):
    """Conversion modes."""
    DIRECT = "direct"
    VIA_JSON = "via_json"
    VIA_XWJSON = "via_xwjson"
