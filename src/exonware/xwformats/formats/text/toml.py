#!/usr/bin/env python3
#exonware/xwformats/src/exonware/xwformats/formats/text/toml.py
"""
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.9.0.2
Generation Date: 15-Nov-2025
TOML Serialization - Tom's Obvious Minimal Language
TOML is a configuration file format:
- Human-readable
- Clear syntax
- Used by many modern projects (Cargo, Poetry, etc.)
- Supports tables and arrays of tables
Priority 1 (Security): Safe TOML parsing
Priority 2 (Usability): Simple TOML read/write API
Priority 3 (Maintainability): Clean TOML handling
Priority 4 (Performance): Efficient TOML parsing
Priority 5 (Extensibility): Support TOML v1.0.0
"""

from typing import Any, Optional
from pathlib import Path
import tomli
import tomli_w
from exonware.xwsystem.io.serialization.base import ASerialization
from exonware.xwsystem.io.serialization.contracts import ISerialization
from exonware.xwsystem.io.contracts import EncodeOptions, DecodeOptions
from exonware.xwsystem.io.errors import SerializationError


class TomlSerializer(ASerialization):
    """
    TOML serializer.
    I: ISerialization (interface)
    A: ASerialization (abstract base)
    XW: TomlSerializer (concrete implementation)
    """

    def __init__(self):
        """Initialize TOML serializer."""
        super().__init__()
    @property

    def codec_id(self) -> str:
        """Codec identifier."""
        return "toml"
    @property

    def media_types(self) -> list[str]:
        """Supported media types."""
        return ["application/toml"]
    @property

    def file_extensions(self) -> list[str]:
        """Supported file extensions."""
        return [".toml"]
    @property

    def format_name(self) -> str:
        """Format name."""
        return "TOML"
    @property

    def mime_type(self) -> str:
        """MIME type."""
        return "application/toml"
    @property

    def is_binary_format(self) -> bool:
        """Whether format is binary."""
        return False
    @property

    def supports_streaming(self) -> bool:
        """Whether format supports streaming."""
        return False  # TOML typically requires full document

    def encode(
        self,
        data: Any,
        options: Optional[EncodeOptions] = None
    ) -> bytes:
        """
        Encode data to TOML.
        Args:
            data: Data to encode (dict)
            options: Encoding options
        Returns:
            TOML-encoded bytes
        Raises:
            SerializationError: If encoding fails
        """
        try:
            if hasattr(tomli_w, 'dumps'):
                toml_str = tomli_w.dumps(data)
            else:
                toml_str = tomli_w.dump(data)
            return toml_str.encode('utf-8')
        except Exception as e:
            raise SerializationError(f"TOML encoding failed: {e}") from e

    def decode(
        self,
        data: bytes | bytearray | str,
        options: Optional[DecodeOptions] = None
    ) -> Any:
        """
        Decode TOML data.
        Args:
            data: TOML-encoded bytes or string
            options: Decoding options
        Returns:
            Decoded data (dict)
        Raises:
            SerializationError: If decoding fails
        """
        try:
            if isinstance(data, (bytes, bytearray)):
                data = data.decode('utf-8')
            if hasattr(tomli, 'loads'):
                return tomli.loads(data)
            else:
                return tomli.load(data)
        except Exception as e:
            raise SerializationError(f"TOML decoding failed: {e}") from e

    def encode_to_file(
        self,
        data: Any,
        file_path: str | Path,
        options: Optional[EncodeOptions] = None
    ) -> None:
        """
        Encode data to TOML file.
        Args:
            data: Data to encode
            file_path: Path to output file
            options: Encoding options
        """
        toml_data = self.encode(data, options)
        file_path = Path(file_path)
        file_path.write_bytes(toml_data)

    def decode_from_file(
        self,
        file_path: str | Path,
        options: Optional[DecodeOptions] = None
    ) -> Any:
        """
        Decode TOML from file.
        Args:
            file_path: Path to TOML file
            options: Decoding options
        Returns:
            Decoded data
        """
        file_path = Path(file_path)
        toml_data = file_path.read_bytes()
        return self.decode(toml_data, options)
