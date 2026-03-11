#!/usr/bin/env python3
"""
#exonware/xwformats/src/exonware/xwformats/contracts.py
Protocol interfaces for xwformats.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.1.0.2
Generation Date: 07-Jan-2025
"""

from typing import Any, Optional, Protocol, runtime_checkable
from pathlib import Path
@runtime_checkable

class IFormatSerializer(Protocol):
    """Interface for format serializers."""
    @property

    def codec_id(self) -> str:
        """Get codec identifier."""
        ...
    @property

    def format_name(self) -> str:
        """Get format name."""
        ...
    @property

    def is_binary_format(self) -> bool:
        """Check if format is binary."""
        ...

    def encode(self, data: Any, options: Optional[dict[str, Any]] = None) -> bytes:
        """Encode data to format."""
        ...

    def decode(self, data: bytes, options: Optional[dict[str, Any]] = None) -> Any:
        """Decode data from format."""
        ...
@runtime_checkable

class IFormatConverter(Protocol):
    """Interface for format conversion."""

    def convert(
        self,
        data: Any,
        from_format: str,
        to_format: str,
        options: Optional[dict[str, Any]] = None
    ) -> Any:
        """Convert data between formats."""
        ...
@runtime_checkable

class IFormatRegistry(Protocol):
    """Interface for format registry."""

    def register(self, serializer_class: type) -> None:
        """Register a serializer class."""
        ...

    def get(self, format_name: str) -> Optional[IFormatSerializer]:
        """Get serializer by format name."""
        ...

    def list_formats(self) -> list[str]:
        """List all registered formats."""
        ...
