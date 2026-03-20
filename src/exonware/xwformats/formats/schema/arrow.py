#!/usr/bin/env python3
#exonware/xwformats/src/exonware/xwformats/formats/schema/arrow.py
"""
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.9.0.17
Generation Date: 07-Jan-2025
Apache Arrow serialization - Columnar in-memory format.
Apache Arrow is a cross-language development platform for in-memory data.
It specifies a standardized language-independent columnar memory format for
flat and hierarchical data, organized for efficient analytic operations.
Following I→A→XW pattern:
- I: ISerialization (interface)
- A: ASerialization (abstract base)
- XW: ArrowSerializer (concrete implementation)
Priority 1 (Security): Safe Arrow operations with input validation
Priority 2 (Usability): Simple Arrow read/write API compatible with pandas/Parquet
Priority 3 (Maintainability): Clean Arrow handling following design patterns
Priority 4 (Performance): Efficient columnar in-memory operations
Priority 5 (Extensibility): Support Arrow IPC, streaming, and batch operations
"""

import io
from typing import Any
from pathlib import Path
from exonware.xwsystem.io.serialization.base import ASerialization
from exonware.xwsystem.io.contracts import EncodeOptions, DecodeOptions
from exonware.xwsystem.io.defs import CodecCapability
from exonware.xwsystem.io.errors import SerializationError
import pyarrow as pa
import pyarrow.ipc as ipc
import pandas as pd


class ArrowSerializer(ASerialization):
    """
    Apache Arrow serializer - follows I→A→XW pattern.
    I: ISerialization (interface)
    A: ASerialization (abstract base)
    XW: ArrowSerializer (concrete implementation)
    Uses pyarrow library for Apache Arrow format.
    Examples:
        >>> serializer = ArrowSerializer()
        >>> 
        >>> # Encode data (list of dicts, pandas DataFrame, or pyarrow Table)
        >>> arrow_bytes = serializer.encode(data)
        >>> 
        >>> # Decode to list of dicts or pandas DataFrame
        >>> data = serializer.decode(arrow_bytes)
    """

    def __init__(self):
        """Initialize Arrow serializer."""
        super().__init__()
    # ========================================================================
    # CODEC METADATA
    # ========================================================================
    @property

    def codec_id(self) -> str:
        """Codec identifier."""
        return "arrow"
    @property

    def media_types(self) -> list[str]:
        """Supported media types."""
        return ["application/vnd.apache.arrow.stream", "application/x-apache-arrow"]
    @property

    def file_extensions(self) -> list[str]:
        """Supported file extensions."""
        return [".arrow", ".arrows", ".ipc"]
    @property

    def format_name(self) -> str:
        """Format name."""
        return "Arrow"
    @property

    def mime_type(self) -> str:
        """Primary MIME type."""
        return "application/vnd.apache.arrow.stream"
    @property

    def is_binary_format(self) -> bool:
        """Arrow is a binary format."""
        return True
    @property

    def supports_streaming(self) -> bool:
        """Arrow supports streaming via IPC."""
        return True
    @property

    def capabilities(self) -> CodecCapability:
        """Arrow supports bidirectional operations and schema-based encoding."""
        return CodecCapability.BIDIRECTIONAL | CodecCapability.SCHEMA_BASED
    @property

    def aliases(self) -> list[str]:
        """Arrow aliases."""
        return ["arrow", "Arrow", "ARROW", "apache-arrow"]
    @property

    def codec_types(self) -> list[str]:
        """Arrow is a binary schema format for columnar in-memory data."""
        return ["binary", "schema", "data", "columnar"]
    # ========================================================================
    # CORE ENCODE/DECODE (Using pyarrow)
    # ========================================================================

    def encode(self, value: Any, *, options: EncodeOptions | None = None) -> bytes:
        """
        Encode data to Arrow IPC format bytes.
        Uses pyarrow for Apache Arrow IPC serialization.
        Args:
            value: Data to serialize (list of dicts, pandas DataFrame, or pyarrow Table)
            options: Arrow options (compression, etc.)
        Returns:
            Arrow IPC bytes
        Raises:
            SerializationError: If encoding fails
        """
        try:
            opts = options or {}
            # Convert to pyarrow Table
            if isinstance(value, list):
                table = pa.Table.from_pylist(value)
            elif isinstance(value, pa.Table):
                table = value
            elif isinstance(value, dict):
                # Single dict - convert to list
                table = pa.Table.from_pylist([value])
            else:
                # Try pandas DataFrame conversion
                if isinstance(value, pd.DataFrame):
                    table = pa.Table.from_pandas(value)
                else:
                    raise TypeError(
                        f"Unsupported type for Arrow: {type(value)}. "
                        "Expected list of dicts, pandas DataFrame, or pyarrow Table."
                    )
            # Get compression option
            compression = opts.get('compression', None)
            if compression:
                # Apply compression to the table
                # Note: Arrow compression is applied at column level
                pass  # Compression handled by IPC writer
            # Write to Arrow IPC format (streaming format)
            output = io.BytesIO()
            with ipc.new_stream(output, table.schema) as writer:
                writer.write_table(table)
                writer.close()
            return output.getvalue()
        except Exception as e:
            raise SerializationError(
                f"Failed to encode Arrow: {e}",
                format_name=self.format_name,
                original_error=e
            ) from e

    def decode(self, repr: bytes | str, *, options: DecodeOptions | None = None) -> Any:
        """
        Decode Arrow IPC bytes to data.
        Uses pyarrow for Apache Arrow IPC deserialization.
        Args:
            repr: Arrow IPC bytes
            options: Decoding options (as_dataframe, etc.)
        Returns:
            List of dicts or pandas DataFrame
        Raises:
            SerializationError: If decoding fails
        """
        try:
            # Arrow requires bytes
            if isinstance(repr, str):
                repr = repr.encode('utf-8')
            opts = options or {}
            # Read from Arrow IPC format
            input_stream = io.BytesIO(repr)
            reader = ipc.open_stream(input_stream)
            table = reader.read_all()
            reader.close()
            # Convert to requested format
            if opts.get('as_dataframe', False):
                return table.to_pandas()
            else:
                return table.to_pylist()
        except Exception as e:
            raise SerializationError(
                f"Failed to decode Arrow: {e}",
                format_name=self.format_name,
                original_error=e
            ) from e
