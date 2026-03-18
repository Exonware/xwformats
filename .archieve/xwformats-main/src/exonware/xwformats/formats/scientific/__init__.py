#!/usr/bin/env python3
#exonware/xwformats/src/exonware/xwformats/formats/scientific/__init__.py
"""
Scientific data serialization formats.
Note: Import these modules explicitly due to large dependencies (scipy, h5py, etc.)
These are not auto-imported to avoid loading heavy scientific packages.
"""
# Standard imports following DEV_GUIDELINES - no try/except
# Users with [full] extra have them pre-installed

from .hdf5 import Hdf5Serializer
from .feather import FeatherSerializer
from .zarr import ZarrSerializer
from .netcdf import NetcdfSerializer
from .mat import MatSerializer
__all__ = [
    "Hdf5Serializer",
    "FeatherSerializer",
    "ZarrSerializer",
    "NetcdfSerializer",
    "MatSerializer",
]
