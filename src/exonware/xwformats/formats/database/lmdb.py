"""
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.9.0.16
Generation Date: November 2, 2025

LMDB serialization - Lightning Memory-Mapped Database.

Following I→A→XW pattern:
- I: ISerialization (interface)
- A: ASerialization (abstract base)
- XW: XWLmdbSerializer (concrete implementation)
"""

from typing import Any

from exonware.xwsystem.io.serialization.base import ASerialization
from exonware.xwsystem.io.contracts import EncodeOptions, DecodeOptions
from exonware.xwsystem.io.defs import CodecCapability


class XWLmdbSerializer(ASerialization):
    """LMDB serializer - follows I→A→XW pattern."""
    
    def __init__(self):
        """Initialize LMDB serializer."""
        super().__init__()
    
    @property
    def codec_id(self) -> str:
        return "lmdb"
    
    @property
    def media_types(self) -> list[str]:
        return ["application/x-lmdb"]
    
    @property
    def file_extensions(self) -> list[str]:
        return [".lmdb", ".mdb"]
    
    @property
    def format_name(self) -> str:
        return "LMDB"
    
    @property
    def mime_type(self) -> str:
        return "application/x-lmdb"
    
    @property
    def is_binary_format(self) -> bool:
        return True
    
    @property
    def supports_streaming(self) -> bool:
        return True
    
    @property
    def capabilities(self) -> CodecCapability:
        return CodecCapability.BIDIRECTIONAL
    
    @property
    def aliases(self) -> list[str]:
        return ["lmdb", "LMDB"]
    
    def encode(self, value: Any, *, options: EncodeOptions | None = None) -> bytes | str:
        """LMDB encode requires file path - use save_file() instead."""
        raise NotImplementedError("LMDB requires file-based operations - use save_file()")
    
    def decode(self, repr: bytes | str, *, options: DecodeOptions | None = None) -> Any:
        """LMDB decode requires file path - use load_file() instead."""
        raise NotImplementedError("LMDB requires file-based operations - use load_file()")


LmdbSerializer = XWLmdbSerializer

