#!/usr/bin/env python3
#exonware/xwformats/src/exonware/xwformats/formats/binary/dill.py
"""
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1.4
Generation Date: 07-Jan-2025
Dill Serialization - Extended Pickle for Complex Python Objects
Dill extends Python's pickle to serialize complex objects:
- Serializes functions, lambdas, closures
- Serializes nested functions, generators
- Can save/load entire Python interpreter sessions
- Serializes modules, code objects
- Useful for distributed computing and scientific workflows
- Machine learning model serialization (extended capabilities)
Following I→A→XW pattern:
- I: ISerialization (interface)
- A: ASerialization (abstract base)
- XW: DillSerializer (concrete implementation)
Priority 1 (Security): Safe deserialization (same security considerations as pickle)
Priority 2 (Usability): Extended Python object serialization API
Priority 3 (Maintainability): Clean extended pickle handling
Priority 4 (Performance): Efficient serialization of complex objects
Priority 5 (Extensibility): Support functions, lambdas, sessions, and more
"""

from typing import Any, Optional
from pathlib import Path
import io
import dill
from exonware.xwsystem.io.serialization.base import ASerialization
from exonware.xwsystem.io.contracts import EncodeOptions, DecodeOptions
from exonware.xwsystem.io.defs import CodecCapability
from exonware.xwsystem.io.errors import SerializationError


class DillSerializer(ASerialization):
    """
    Dill serializer - Extended pickle for complex Python objects.
    I: ISerialization (interface)
    A: ASerialization (abstract base)
    XW: DillSerializer (concrete implementation)
    Uses dill library for extended Python object serialization.
    Examples:
        >>> serializer = DillSerializer()
        >>> 
        >>> # Serialize a function (not possible with standard pickle)
        >>> def complex_function(x):
        ...     def inner(y):
        ...         return x * y
        ...     return inner
        >>> 
        >>> dill_bytes = serializer.encode(complex_function)
        >>> decoded = serializer.decode(dill_bytes)
    """

    def __init__(self):
        """Initialize Dill serializer."""
        super().__init__()
    @property

    def codec_id(self) -> str:
        """Codec identifier."""
        return "dill"
    @property

    def media_types(self) -> list[str]:
        """Supported MIME types."""
        return ["application/x-dill", "application/x-python-dill"]
    @property

    def file_extensions(self) -> list[str]:
        """Supported file extensions."""
        return [".dill", ".pkl"]  
    @property

    def format_name(self) -> str:
        """Format name."""
        return "Dill"
    @property

    def mime_type(self) -> str:
        """Primary MIME type."""
        return "application/x-dill"
    @property

    def is_binary_format(self) -> bool:
        """Dill is a binary format."""
        return True
    @property

    def supports_streaming(self) -> bool:
        """Dill supports streaming operations."""
        return True
    @property

    def capabilities(self) -> CodecCapability:
        """Dill supports bidirectional operations."""
        return CodecCapability.BIDIRECTIONAL
    @property

    def aliases(self) -> list[str]:
        """Dill aliases."""
        return ["dill", "Dill", "DILL", "extended-pickle"]
    @property

    def codec_types(self) -> list[str]:
        """Dill is an extended binary serialization format for Python objects."""
        return ["binary", "serialization", "python", "extended"]

    def encode(self, value: Any, *, options: Optional[EncodeOptions] = None) -> bytes:
        """
        Encode data to Dill bytes.
        Uses dill library for extended Python object serialization.
        Args:
            value: Data to serialize (any Python object, including functions, lambdas, etc.)
            options: Encoding options:
                - protocol (int): Pickle protocol version (default: dill default)
                - recurse (bool): Recursive serialization (default: True)
        Returns:
            Dill bytes
        Raises:
            SerializationError: If encoding fails
        """
        try:
            opts = options or {}
            # Get protocol option
            protocol = opts.get('protocol', None)
            # Use BytesIO for in-memory serialization
            output = io.BytesIO()
            if protocol is not None:
                dill.dump(value, output, protocol=protocol)
            else:
                dill.dump(value, output)
            return output.getvalue()
        except Exception as e:
            raise SerializationError(
                f"Failed to encode Dill: {e}",
                format_name=self.format_name,
                original_error=e
            ) from e

    def decode(self, repr: bytes | str, *, options: Optional[DecodeOptions] = None) -> Any:
        """
        Decode Dill bytes to data.
        Uses dill library for extended Python object deserialization.
        Args:
            repr: Dill bytes
            options: Decoding options
        Returns:
            Decoded Python object (can be functions, lambdas, etc.)
        Raises:
            SerializationError: If decoding fails
        """
        try:
            # Dill requires bytes
            if isinstance(repr, str):
                repr = repr.encode('utf-8')
            opts = options or {}
            # Use BytesIO for in-memory deserialization
            input_stream = io.BytesIO(repr)
            return dill.load(input_stream)
        except Exception as e:
            raise SerializationError(
                f"Failed to decode Dill: {e}",
                format_name=self.format_name,
                original_error=e
            ) from e
