#!/usr/bin/env python3
"""
#exonware/xwformats/src/exonware/xwformats/facade.py
XWFormats Facade - Main Public API
This module provides the main public API for xwformats following GUIDE_DEV.md facade pattern.
Public API per REF_15_API and REF_01_REQ sec. 6.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.9.0.10
Generation Date: 07-Jan-2025
"""

from typing import Any
from .converter import FormatConverter
from .config import XWFormatsConfig
from .defs import ConversionMode
from .errors import XWFormatsError


class XWFormats:
    """
    Main XWFormats class providing enterprise serialization formats.
    This class implements the facade pattern, providing a unified API for
    format serialization and conversion across 21+ enterprise formats.
    """

    def __init__(
        self,
        conversion_mode: str | ConversionMode = ConversionMode.DIRECT,
        enable_caching: bool = True,
        **options
    ):
        """
        Initialize XWFormats.
        Args:
            conversion_mode: Conversion mode ('direct', 'via_json', 'via_xwjson') or ConversionMode enum
            enable_caching: Enable conversion caching
            **options: Additional configuration options
        """
        # Convert string to enum if needed
        if isinstance(conversion_mode, str):
            try:
                conversion_mode = ConversionMode[conversion_mode.upper()]
            except KeyError:
                conversion_mode = ConversionMode.DIRECT
        self._config = XWFormatsConfig(
            conversion_mode=conversion_mode,
            enable_caching=enable_caching
        )
        self._converter = FormatConverter()

    def convert(
        self,
        data: Any,
        from_format: str,
        to_format: str,
        options: dict[str, Any] | None = None
    ) -> Any:
        """
        Convert data between formats.
        Args:
            data: Data to convert
            from_format: Source format name
            to_format: Target format name
            options: Conversion options
        Returns:
            Converted data
        """
        return self._converter.convert(data, from_format, to_format, options)

    def get_serializer(self, format_name: str):
        """
        Get serializer for a format.
        Args:
            format_name: Format name
        Returns:
            Serializer instance
        """
        from exonware.xwsystem.io.codec.registry import get_registry
        registry = get_registry()
        return registry.get_by_id(format_name)

    def list_formats(self) -> list[str]:
        """
        List all available formats (codec IDs). Per REF_01_REQ, formats registered
        at import are reflected here and in auto-detection (xwcodec, xwfile, xwserialization).
        Returns:
            List of format names (codec_id)
        """
        from exonware.xwsystem.io.codec.registry import get_registry
        registry = get_registry()
        return registry.list_codecs()
