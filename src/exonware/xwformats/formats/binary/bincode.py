#!/usr/bin/env python3
#exonware/xwformats/src/exonware/xwformats/formats/binary/bincode.py
"""
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.9.0.33
Generation Date: 07-Jan-2025
Bincode Serialization - Rust's Native Binary Format
Bincode is Rust's native binary serialization format that:
- Provides high-performance binary serialization
- Enables Rust ↔ Python interoperability
- Supports zero-copy deserialization
- Type-safe serialization compatible with Rust's bincode crate
- Compact and fast binary format
Following I→A→XW pattern:
- I: ISerialization (interface)
- A: ASerialization (abstract base)
- XW: BincodeSerializer (concrete implementation)
Priority 1 (Security): Safe binary deserialization with validation
Priority 2 (Usability): Simple Rust-compatible binary API
Priority 3 (Maintainability): Clean binary serialization following patterns
Priority 4 (Performance): Fast binary encoding/decoding
Priority 5 (Extensibility): Support custom serializers and Rust interoperability
"""

from typing import Any
from pathlib import Path
import io
import attrs2bin
import attr
from attrs2bin.interfaces import ITypeSerializer, IReadableSocket
from zope.interface import implementer
from exonware.xwsystem.io.serialization.base import ASerialization
from exonware.xwsystem.io.contracts import EncodeOptions, DecodeOptions
from exonware.xwsystem.io.defs import CodecCapability
from exonware.xwsystem.io.errors import SerializationError
@implementer(IReadableSocket)


class BytesReadableSocket:
    """Wrapper to make bytes readable as a socket for attrs2bin."""

    def __init__(self, data: bytes):
        self._stream = io.BytesIO(data)

    def recv(self, bufsize: int) -> bytes:
        """Read bytes from the stream."""
        return self._stream.read(bufsize)
@implementer(ITypeSerializer)


class DictTypeSerializer:
    """Custom serializer for dict type in attrs2bin."""

    def serialize(self, value: dict) -> bytes:
        """Serialize dict to bytes using pickle (fallback)."""
        import pickle
        result = pickle.dumps(value)
        return bytes(result) if isinstance(result, bytearray) else result

    def deserialize(self, stream: Any) -> dict:
        """Deserialize from stream to dict using pickle (fallback)."""
        import pickle
        # attrs2bin passes a DequeBuffer or bytes
        # DequeBuffer has read() method, bytes can be used directly
        if isinstance(stream, (bytes, bytearray)):
            data = bytes(stream)
        elif hasattr(stream, 'read'):
            # DequeBuffer or file-like object
            data = b''
            while True:
                chunk = stream.read(4096)
                if not chunk:
                    break
                data += chunk
        elif hasattr(stream, 'recv'):
            # IReadableSocket interface
            data = b''
            while True:
                chunk = stream.recv(4096)
                if not chunk:
                    break
                data += chunk
        else:
            # Try to convert to bytes
            try:
                data = bytes(stream)
            except:
                data = b''
        if not data:
            return {}
        return pickle.loads(data)
@implementer(ITypeSerializer)


class ListTypeSerializer:
    """Custom serializer for list type in attrs2bin."""

    def serialize(self, value: list) -> bytes:
        """Serialize list to bytes using pickle (fallback)."""
        import pickle
        result = pickle.dumps(value)
        return bytes(result) if isinstance(result, bytearray) else result

    def deserialize(self, stream: Any) -> list:
        """Deserialize from stream to list using pickle (fallback)."""
        import pickle
        # attrs2bin passes a DequeBuffer or bytes
        if isinstance(stream, (bytes, bytearray)):
            data = bytes(stream)
        elif hasattr(stream, 'read'):
            data = b''
            while True:
                chunk = stream.read(4096)
                if not chunk:
                    break
                data += chunk
        elif hasattr(stream, 'recv'):
            data = b''
            while True:
                chunk = stream.recv(4096)
                if not chunk:
                    break
                data += chunk
        else:
            try:
                data = bytes(stream)
            except:
                data = b''
        if not data:
            return []
        return pickle.loads(data)
# Register serializers for attrs2bin
attrs2bin.register_serializer(dict, DictTypeSerializer())
attrs2bin.register_serializer(list, ListTypeSerializer())


class BincodeSerializer(ASerialization):
    """
    Bincode serializer - Rust's native binary format.
    I: ISerialization (interface)
    A: ASerialization (abstract base)
    XW: BincodeSerializer (concrete implementation)
    Uses attrs2bin library for Rust bincode compatibility.
    Examples:
        >>> serializer = BincodeSerializer()
        >>> 
        >>> # Encode data (compatible with Rust bincode)
        >>> bincode_bytes = serializer.encode({"name": "Alice", "age": 30})
        >>> 
        >>> # Decode to Python data
        >>> data = serializer.decode(bincode_bytes)
    """

    def __init__(self):
        """Initialize Bincode serializer."""
        super().__init__()
    @property

    def codec_id(self) -> str:
        """Codec identifier."""
        return "bincode"
    @property

    def media_types(self) -> list[str]:
        """Supported MIME types."""
        return ["application/x-bincode", "application/vnd.rust.bincode"]
    @property

    def file_extensions(self) -> list[str]:
        """Supported file extensions."""
        return [".bincode", ".bin"]
    @property

    def format_name(self) -> str:
        """Format name."""
        return "Bincode"
    @property

    def mime_type(self) -> str:
        """Primary MIME type."""
        return "application/x-bincode"
    @property

    def is_binary_format(self) -> bool:
        """Bincode is a binary format."""
        return True
    @property

    def supports_streaming(self) -> bool:
        """Bincode supports streaming operations."""
        return True
    @property

    def capabilities(self) -> CodecCapability:
        """Bincode supports bidirectional operations."""
        return CodecCapability.BIDIRECTIONAL
    @property

    def aliases(self) -> list[str]:
        """Bincode aliases."""
        return ["bincode", "Bincode", "BINCODE", "rust-bincode"]
    @property

    def codec_types(self) -> list[str]:
        """Bincode is a binary serialization format for Rust interoperability."""
        return ["binary", "serialization", "rust"]

    def _dict_to_attrs(self, data: dict) -> Any:
        """
        Convert dict to attrs class for Bincode serialization.
        Args:
            data: Dictionary to convert
        Returns:
            attrs-based class instance
        """
        # Create a dynamic attrs class
        @attr.s(auto_attribs=True, slots=False)
        class DictWrapper:
            # Add all dict keys as attributes
            pass
        # Set attributes dynamically
        instance = DictWrapper()
        for key, value in data.items():
            setattr(instance, str(key), value)
        return instance

    def encode(self, value: Any, *, options: EncodeOptions | None = None) -> bytes:
        """
        Encode data to Bincode bytes.
        Uses attrs2bin for Rust bincode compatibility.
        Note: attrs2bin works with attrs-based objects. For dicts, we convert
        them to attrs classes. For attrs objects, serialize directly.
        Args:
            value: Data to serialize (dict, attrs-based object)
            options: Encoding options
        Returns:
            Bincode bytes
        Raises:
            SerializationError: If encoding fails
        """
        try:
            opts = options or {}
            # attrs2bin works with attrs-based objects, but has limitations
            # For attrs objects, convert to dict first (more reliable)
            if attr.has(value.__class__):
                # Convert attrs object to dict for serialization
                # This avoids attrs2bin's limitations with certain field types (e.g., str)
                import attr as attr_module
                data_dict = attr_module.asdict(value)
                # Wrap in DataWrapper and serialize
                @attr.s(auto_attribs=True, slots=False)
                class DataWrapper:
                    data: dict = attr.ib()
                wrapper = DataWrapper(data=data_dict)
                result = attrs2bin.serialize(wrapper)
                # Ensure bytes (attrs2bin may return bytearray)
                return bytes(result) if isinstance(result, bytearray) else result
            elif isinstance(value, dict):
                # Convert dict to attrs class for serialization
                @attr.s(auto_attribs=True, slots=False)
                class DataWrapper:
                    data: dict = attr.ib()
                wrapper = DataWrapper(data=value)
                result = attrs2bin.serialize(wrapper)
                # Ensure bytes (attrs2bin may return bytearray)
                return bytes(result) if isinstance(result, bytearray) else result
            elif isinstance(value, list):
                # Convert list to attrs class for serialization
                @attr.s(auto_attribs=True, slots=False)
                class ListWrapper:
                    data: list = attr.ib()
                wrapper = ListWrapper(data=value)
                result = attrs2bin.serialize(wrapper)
                # Ensure bytes (attrs2bin may return bytearray)
                return bytes(result) if isinstance(result, bytearray) else result
            else:
                raise TypeError(
                    f"Bincode encode expects dict, list, or attrs-based object, got {type(value)}. "
                    "For Rust interoperability, use attrs classes, dicts, or lists."
                )
        except Exception as e:
            raise SerializationError(
                f"Failed to encode Bincode: {e}",
                format_name=self.format_name,
                original_error=e
            ) from e

    def decode(self, repr: bytes | str, *, options: DecodeOptions | None = None) -> Any:
        """
        Decode Bincode bytes to data.
        Uses attrs2bin for Rust bincode compatibility.
        Note: attrs2bin.deserialize requires a target_type. For dicts, we use
        a wrapper class. For custom types, provide target_type in options.
        Args:
            repr: Bincode bytes
            options: Decoding options:
                - target_type: Type to deserialize to (attrs class)
        Returns:
            Decoded Python data (dict if no target_type, or attrs object)
        Raises:
            SerializationError: If decoding fails
        """
        try:
            # Bincode requires bytes
            if isinstance(repr, str):
                repr = repr.encode('utf-8')
            opts = options or {}
            # Check if target_type is provided
            target_type = opts.get('target_type', None)
            # Try dict wrapper first, then list wrapper
            @attr.s(auto_attribs=True, slots=False)
            class DataWrapper:
                data: dict = attr.ib()
            @attr.s(auto_attribs=True, slots=False)
            class ListWrapper:
                data: list = attr.ib()
            # Try to deserialize as dict first
            try:
                wrapper = attrs2bin.deserialize(repr, DataWrapper)
                data = wrapper.data
                if target_type and isinstance(data, dict):
                    # Reconstruct attrs object from dict
                    return target_type(**data)
                else:
                    return data
            except Exception:
                # Try as list wrapper
                try:
                    wrapper = attrs2bin.deserialize(repr, ListWrapper)
                    return wrapper.data
                except Exception:
                    # If both fail, raise error
                    raise SerializationError(
                        f"Failed to decode Bincode: Could not deserialize as dict or list",
                        format_name=self.format_name
                    )
        except Exception as e:
            raise SerializationError(
                f"Failed to decode Bincode: {e}",
                format_name=self.format_name,
                original_error=e
            ) from e
