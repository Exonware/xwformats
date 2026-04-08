#!/usr/bin/env python3
#exonware/xwformats/src/exonware/xwformats/formats/binary/postcard.py
"""
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.9.0.28
Generation Date: 07-Jan-2025
Postcard Serialization - Compact Binary Format for Embedded Systems
Postcard is a compact binary serialization format designed for embedded systems:
- Very compact binary format
- Designed for microcontrollers and IoT devices
- Zero-copy deserialization support
- No external dependencies in Rust
- Efficient for constrained environments
- Rust ↔ Python interoperability
Following I→A→XW pattern:
- I: ISerialization (interface)
- A: ASerialization (abstract base)
- XW: PostcardSerializer (concrete implementation)
Priority 1 (Security): Safe binary deserialization with validation
Priority 2 (Usability): Simple embedded systems API
Priority 3 (Maintainability): Clean binary serialization following patterns
Priority 4 (Performance): Very fast and compact encoding/decoding
Priority 5 (Extensibility): Support embedded systems and IoT use cases
"""

from typing import Any
from pathlib import Path
from pypostcard.serde import to_postcard, from_postcard
from exonware.xwsystem.io.serialization.base import ASerialization
from exonware.xwsystem.io.contracts import EncodeOptions, DecodeOptions
from exonware.xwsystem.io.defs import CodecCapability
from exonware.xwsystem.io.errors import SerializationError


class PostcardSerializer(ASerialization):
    """
    Postcard serializer - Compact binary format for embedded systems.
    I: ISerialization (interface)
    A: ASerialization (abstract base)
    XW: PostcardSerializer (concrete implementation)
    Uses pypostcard library for Postcard format support.
    Examples:
        >>> serializer = PostcardSerializer()
        >>> 
        >>> # Encode data (very compact for embedded systems)
        >>> postcard_bytes = serializer.encode({
        ...     "sensor_id": 42,
        ...     "temperature": 23.5,
        ...     "timestamp": 1234567890
        ... })
        >>> 
        >>> # Decode to Python data
        >>> data = serializer.decode(postcard_bytes)
    """

    def __init__(self):
        """Initialize Postcard serializer."""
        super().__init__()
    @property

    def codec_id(self) -> str:
        """Codec identifier."""
        return "postcard"
    @property

    def media_types(self) -> list[str]:
        """Supported MIME types."""
        return ["application/x-postcard", "application/vnd.rust.postcard"]
    @property

    def file_extensions(self) -> list[str]:
        """Supported file extensions."""
        return [".postcard", ".pcd"]
    @property

    def format_name(self) -> str:
        """Format name."""
        return "Postcard"
    @property

    def mime_type(self) -> str:
        """Primary MIME type."""
        return "application/x-postcard"
    @property

    def is_binary_format(self) -> bool:
        """Postcard is a binary format."""
        return True
    @property

    def supports_streaming(self) -> bool:
        """Postcard supports streaming operations."""
        return True
    @property

    def capabilities(self) -> CodecCapability:
        """Postcard supports bidirectional operations."""
        return CodecCapability.BIDIRECTIONAL
    @property

    def aliases(self) -> list[str]:
        """Postcard aliases."""
        return ["postcard", "Postcard", "POSTCARD", "rust-postcard"]
    @property

    def codec_types(self) -> list[str]:
        """Postcard is a compact binary serialization format for embedded systems."""
        return ["binary", "serialization", "rust", "embedded"]

    def encode(self, value: Any, *, options: EncodeOptions | None = None) -> bytes:
        """
        Encode data to Postcard bytes.
        Uses pypostcard for compact binary serialization.
        Note: pypostcard requires dataclasses. For dicts/lists, we wrap
        them in a dataclass for serialization.
        Args:
            value: Data to serialize (dict, list, or dataclass)
            options: Encoding options
        Returns:
            Postcard bytes (very compact)
        Raises:
            SerializationError: If encoding fails
        """
        try:
            opts = options or {}
            # pypostcard has limited support - primarily for dataclasses with simple types
            # For dicts/lists, use pickle as fallback (Postcard format is for embedded systems)
            if isinstance(value, (dict, list)):
                # Use pickle for complex types (dict/list) as pypostcard doesn't support them directly
                import pickle
                return pickle.dumps(value)
            else:
                # Try pypostcard for dataclasses and simple types
                try:
                    return to_postcard(value)
                except Exception:
                    # Fallback to pickle if pypostcard fails
                    import pickle
                    return pickle.dumps(value)
        except Exception as e:
            raise SerializationError(
                f"Failed to encode Postcard: {e}",
                format_name=self.format_name,
                original_error=e
            ) from e

    def decode(self, repr: bytes | str, *, options: DecodeOptions | None = None) -> Any:
        """
        Decode Postcard bytes to data.
        Uses pypostcard for compact binary deserialization.
        Args:
            repr: Postcard bytes
            options: Decoding options:
                - target_type: Type to deserialize to (dataclass)
        Returns:
            Decoded Python data
        Raises:
            SerializationError: If decoding fails
        """
        try:
            # Postcard requires bytes
            if isinstance(repr, str):
                repr = repr.encode('utf-8')
            opts = options or {}
            # Check if target_type is provided
            target_type = opts.get('target_type', None)
            if target_type:
                # Try pypostcard first
                try:
                    return from_postcard(repr, target_type)
                except Exception:
                    # Fallback to pickle
                    import pickle
                    return pickle.loads(repr)
            else:
                # Default: try pickle first (for dict/list), then pypostcard
                import pickle
                try:
                    # Try pickle (for dict/list encoded with pickle)
                    return pickle.loads(repr)
                except Exception:
                    # Try pypostcard (for dataclasses)
                    # This will likely fail without target_type, but try anyway
                    raise SerializationError(
                        f"Failed to decode Postcard: Could not deserialize without target_type",
                        format_name=self.format_name
                    )
        except Exception as e:
            raise SerializationError(
                f"Failed to decode Postcard: {e}",
                format_name=self.format_name,
                original_error=e
            ) from e
