#!/usr/bin/env python3
# exonware/xwformats/src/exonware/xwformats/formats/text/__init__.py
"""
xwformats text formats — **RON only**.

For CSV, JSON, TOML, YAML, and XML, use
``exonware.xwsystem.io.serialization.formats.text`` (import and register there).
"""

from .ron import RonSerializer

__all__ = ["RonSerializer"]
