#!/usr/bin/env python3
"""
#exonware/xwformats/src/exonware/xwformats/config.py
Configuration classes for xwformats.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.9.0.20
Generation Date: 07-Jan-2025
"""

from dataclasses import dataclass

from .defs import ConversionMode
@dataclass

class XWFormatsConfig:
    """Configuration for XWFormats."""
    conversion_mode: ConversionMode = ConversionMode.DIRECT
    enable_caching: bool = True
    cache_size: int = 1000
    lazy_loading: bool = True
    validate_inputs: bool = True
    strict_mode: bool = False
