#!/usr/bin/env python3
#exonware/xwformats/src/exonware/xwformats/formats/text/ron.py
"""
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.9.0.20
Generation Date: 07-Jan-2025
RON Serialization - Rusty Object Notation
RON is a human-readable data serialization format with Rust-like syntax:
- Human-readable configuration format
- Supports complex data structures (structs, enums, tuples, arrays, maps)
- Rust-like syntax for familiarity
- Comments support
- More expressive than JSON for nested structures
- Common in Rust game engines and projects
Following I→A→XW pattern:
- I: ISerialization (interface)
- A: ASerialization (abstract base)
- XW: RonSerializer (concrete implementation)
Priority 1 (Security): Safe RON parsing with input validation
Priority 2 (Usability): Simple Rust-compatible config API
Priority 3 (Maintainability): Clean RON handling following patterns
Priority 4 (Performance): Efficient RON parsing
Priority 5 (Extensibility): Support complex Rust data structures
"""

from typing import Any
from pathlib import Path
# RON library - Try external packages first, then use built-in implementation
# External packages: python-ron (if available), otherwise use built-in parser
_RON_AVAILABLE = False
_USE_EXTERNAL = False
try:
    # Try python-ron package first (correct package name from PyPI)
    try:
        import python_ron as ron
        if hasattr(ron, 'dumps') and hasattr(ron, 'loads'):
            _RON_AVAILABLE = True
            _USE_EXTERNAL = True
    except ImportError:
        pass
    # If python-ron not available, try ron (might exist as namespace package)
    if not _RON_AVAILABLE:
        try:
            import ron
            if hasattr(ron, 'dumps') and hasattr(ron, 'loads'):
                _RON_AVAILABLE = True
                _USE_EXTERNAL = True
        except ImportError:
            pass
except (ImportError, AttributeError):
    pass
# If no external library available, use built-in RON parser
if not _RON_AVAILABLE:
    _RON_AVAILABLE = True  # Built-in parser is always available
    _USE_EXTERNAL = False
    # Built-in RON parser implementation
    import json
    import re

    class _BuiltinRon:
        """Built-in RON parser for basic RON syntax support."""
        @staticmethod
        def dumps(obj: Any, **kwargs) -> str:
            """
            Serialize Python object to RON format.
            Supports: dict, list, tuple, str, int, float, bool, None
            """
            if obj is None:
                return "null"
            elif isinstance(obj, bool):
                return "true" if obj else "false"
            elif isinstance(obj, (int, float)):
                return str(obj)
            elif isinstance(obj, str):
                # Escape strings properly for RON
                escaped = obj.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                return f'"{escaped}"'
            elif isinstance(obj, (list, tuple)):
                items = ', '.join(_BuiltinRon.dumps(item) for item in obj)
                return f'[{items}]'
            elif isinstance(obj, dict):
                items = []
                for key, value in obj.items():
                    key_str = f'"{key}"' if isinstance(key, str) else str(key)
                    value_str = _BuiltinRon.dumps(value)
                    items.append(f'{key_str}: {value_str}')
                return f'({", ".join(items)})'
            else:
                # Fallback to JSON for unknown types
                json_str = json.dumps(obj)
                return json_str
        @staticmethod
        def loads(s: str) -> Any:
            """
            Parse RON string to Python object.
            Basic parser that handles common RON syntax patterns.
            """
            s = s.strip()
            # Handle null
            if s == 'null' or s == 'None':
                return None
            # Handle booleans
            if s == 'true':
                return True
            if s == 'false':
                return False
            # Handle numbers
            try:
                if '.' in s:
                    return float(s)
                return int(s)
            except ValueError:
                pass
            # Handle strings
            if s.startswith('"') and s.endswith('"'):
                # Unescape string
                content = s[1:-1]
                content = content.replace('\\"', '"').replace('\\\\', '\\').replace('\\n', '\n')
                return content
            # Handle lists/arrays [item1, item2, ...]
            if s.startswith('[') and s.endswith(']'):
                content = s[1:-1].strip()
                if not content:
                    return []
                # Simple comma-split (doesn't handle nested structures perfectly, but works for basic cases)
                items = []
                current = []
                depth = 0
                for char in content:
                    if char in '[({':
                        depth += 1
                        current.append(char)
                    elif char in '])}':
                        depth -= 1
                        current.append(char)
                    elif char == ',' and depth == 0:
                        items.append(''.join(current).strip())
                        current = []
                    else:
                        current.append(char)
                if current:
                    items.append(''.join(current).strip())
                return [_BuiltinRon.loads(item.strip()) for item in items if item.strip()]
            # Handle maps/structs (key: value, key2: value2) or {key: value, ...}
            if (s.startswith('(') and s.endswith(')')) or (s.startswith('{') and s.endswith('}')):
                content = s[1:-1].strip()
                if not content:
                    return {}
                result = {}
                # Parse key: value pairs
                pairs = []
                current = []
                depth = 0
                for char in content:
                    if char in '[({':
                        depth += 1
                        current.append(char)
                    elif char in '])}':
                        depth -= 1
                        current.append(char)
                    elif char == ',' and depth == 0:
                        pairs.append(''.join(current).strip())
                        current = []
                    else:
                        current.append(char)
                if current:
                    pairs.append(''.join(current).strip())
                for pair in pairs:
                    if ':' in pair:
                        key_part, value_part = pair.split(':', 1)
                        key = _BuiltinRon.loads(key_part.strip())
                        value = _BuiltinRon.loads(value_part.strip())
                        result[key] = value
                return result
            # Fallback to JSON parsing
            try:
                return json.loads(s)
            except json.JSONDecodeError:
                raise ValueError(f"Unable to parse RON string: {s[:50]}...")
    ron = _BuiltinRon()
from exonware.xwsystem.io.serialization.base import ASerialization
from exonware.xwsystem.io.contracts import EncodeOptions, DecodeOptions
from exonware.xwsystem.io.defs import CodecCapability
from exonware.xwsystem.io.errors import SerializationError


class RonSerializer(ASerialization):
    """
    RON (Rusty Object Notation) serializer.
    I: ISerialization (interface)
    A: ASerialization (abstract base)
    XW: RonSerializer (concrete implementation)
    Uses python-ron library for RON format support.
    Examples:
        >>> serializer = RonSerializer()
        >>> 
        >>> # Encode data with Rust-like syntax
        >>> ron_string = serializer.encode({
        ...     'window_size': (800, 600),
        ...     'window_title': 'My App',
        ...     'fullscreen': False
        ... })
        >>> 
        >>> # Decode RON string
        >>> data = serializer.decode(ron_string)
    """

    def __init__(self):
        """Initialize RON serializer."""
        super().__init__()
    @property

    def codec_id(self) -> str:
        """Codec identifier."""
        return "ron"
    @property

    def media_types(self) -> list[str]:
        """Supported MIME types."""
        return ["application/x-ron", "text/x-ron", "application/vnd.rust.ron"]
    @property

    def file_extensions(self) -> list[str]:
        """Supported file extensions."""
        return [".ron"]
    @property

    def format_name(self) -> str:
        """Format name."""
        return "RON"
    @property

    def mime_type(self) -> str:
        """Primary MIME type."""
        return "application/x-ron"
    @property

    def is_binary_format(self) -> bool:
        """RON is a text format."""
        return False
    @property

    def supports_streaming(self) -> bool:
        """RON supports streaming operations."""
        return False  # RON typically requires full document
    @property

    def capabilities(self) -> CodecCapability:
        """RON supports bidirectional operations."""
        return CodecCapability.BIDIRECTIONAL
    @property

    def aliases(self) -> list[str]:
        """RON aliases."""
        return ["ron", "RON", "rusty-object-notation"]
    @property

    def codec_types(self) -> list[str]:
        """RON is a text serialization format with Rust-like syntax."""
        return ["text", "serialization", "rust", "config"]

    def encode(self, value: Any, *, options: EncodeOptions | None = None) -> bytes | str:
        """
        Encode data to RON string.
        Uses ron library for RON serialization.
        Args:
            value: Data to serialize (dict, list, etc.)
            options: Encoding options
        Returns:
            RON-encoded string
        Raises:
            SerializationError: If encoding fails or RON library not available
        """
        if not _RON_AVAILABLE:
            raise SerializationError(
                "RON library not available. RON format requires manual installation. "
                "See: https://github.com/ron-rs/ron",
                format_name=self.format_name
            )
        if not _RON_AVAILABLE:
            raise SerializationError(
                "RON library not available. RON format requires manual installation. "
                "See: https://github.com/ron-rs/ron",
                format_name=self.format_name
            )
        try:
            opts = options or {}
            # Use ron.dumps (works for both external and built-in implementations)
            ron_string = ron.dumps(value, **opts)
            # Return as string (text format)
            return ron_string
        except Exception as e:
            raise SerializationError(
                f"Failed to encode RON: {e}",
                format_name=self.format_name,
                original_error=e
            ) from e

    def decode(self, repr: bytes | str, *, options: DecodeOptions | None = None) -> Any:
        """
        Decode RON string to data.
        Uses ron library for RON deserialization.
        Args:
            repr: RON string or bytes
            options: Decoding options
        Returns:
            Decoded Python data
        Raises:
            SerializationError: If decoding fails or RON library not available
        """
        if not _RON_AVAILABLE:
            raise SerializationError(
                "RON library not available. RON format requires manual installation. "
                "See: https://github.com/ron-rs/ron",
                format_name=self.format_name
            )
        try:
            # RON requires string input
            if isinstance(repr, bytes):
                ron_string = repr.decode('utf-8')
            else:
                ron_string = str(repr)
            opts = options or {}
            # Use ron.loads (works for both external and built-in implementations)
            return ron.loads(ron_string)
        except Exception as e:
            raise SerializationError(
                f"Failed to decode RON: {e}",
                format_name=self.format_name,
                original_error=e
            ) from e
