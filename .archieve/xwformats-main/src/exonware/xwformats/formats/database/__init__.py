#!/usr/bin/env python3
#exonware/xwformats/src/exonware/xwformats/formats/database/__init__.py
"""Enterprise database serialization formats."""

from .lmdb import LmdbSerializer
from .graphdb import GraphDbSerializer
from .leveldb import LeveldbSerializer
# RocksDB - uses native python-rocksdb if available, otherwise pure Python fallback
# The fallback implementation ensures RocksDB always works
from .rocksdb import RocksdbSerializer
__all__ = [
    "LmdbSerializer",
    "GraphDbSerializer",
    "LeveldbSerializer",
    "RocksdbSerializer",  # Always available (has pure Python fallback)
]
