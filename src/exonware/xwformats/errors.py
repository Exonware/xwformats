#!/usr/bin/env python3
"""
#exonware/xwformats/src/exonware/xwformats/errors.py
Error classes for xwformats.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.9.0.34
Generation Date: 07-Jan-2025
"""


class XWFormatsError(Exception):
    """Base error for xwformats."""
    pass


class XWFormatsSerializationError(XWFormatsError):
    """Serialization-related errors."""
    pass


class XWFormatsConversionError(XWFormatsError):
    """Format conversion errors."""
    pass


class XWFormatsFormatNotSupportedError(XWFormatsError):
    """Format not supported error."""
    pass


class XWFormatsDependencyError(XWFormatsError):
    """Missing dependency errors."""
    pass
