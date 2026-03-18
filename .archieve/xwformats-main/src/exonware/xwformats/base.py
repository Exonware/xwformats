#!/usr/bin/env python3
"""
#exonware/xwformats/src/exonware/xwformats/base.py
Abstract base classes for xwformats.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.9.0.6
Generation Date: 07-Jan-2025
"""

from abc import ABC, abstractmethod
from typing import Any
from .contracts import IFormatSerializer, IFormatConverter, IFormatRegistry


class AFormatSerializer(IFormatSerializer, ABC):
    """Abstract base class for format serializers."""
    @property
    @abstractmethod

    def codec_id(self) -> str:
        """Get codec identifier."""
        pass
    @property
    @abstractmethod

    def format_name(self) -> str:
        """Get format name."""
        pass
    @property
    @abstractmethod

    def is_binary_format(self) -> bool:
        """Check if format is binary."""
        pass
    @abstractmethod

    def encode(self, data: Any, options: dict[str, Any] | None = None) -> bytes:
        """Encode data to format."""
        pass
    @abstractmethod

    def decode(self, data: bytes, options: dict[str, Any] | None = None) -> Any:
        """Decode data from format."""
        pass


class AFormatConverter(IFormatConverter, ABC):
    """Abstract base class for format conversion."""
    @abstractmethod

    def convert(
        self,
        data: Any,
        from_format: str,
        to_format: str,
        options: dict[str, Any] | None = None
    ) -> Any:
        """Convert data between formats."""
        pass


class AFormatRegistry(IFormatRegistry, ABC):
    """Abstract base class for format registry."""
    @abstractmethod

    def register(self, serializer_class: type) -> None:
        """Register a serializer class."""
        pass
    @abstractmethod

    def get(self, format_name: str) -> IFormatSerializer | None:
        """Get serializer by format name."""
        pass
    @abstractmethod

    def list_formats(self) -> list[str]:
        """List all registered formats."""
        pass
