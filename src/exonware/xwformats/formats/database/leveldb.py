#!/usr/bin/env python3
#exonware/xwsystem/src/exonware/xwsystem/io/serialization/formats/database/leveldb.py
"""
Company: eXonware.com
Author: Eng. Muhammad AlShehri
Email: connect@exonware.com
Version: 0.0.1.2
Generation Date: 02-Nov-2025

LevelDB Serialization - Google's Fast Key-Value Store

LevelDB is a fast key-value storage library:
- Sorted key-value pairs
- Fast writes and reads
- Compression support
- Used by Bitcoin and many databases

Priority 1 (Security): Safe key-value operations
Priority 2 (Usability): Simple key-value API
Priority 3 (Maintainability): Clean database integration
Priority 4 (Performance): Very fast operations
Priority 5 (Extensibility): Embeddable database
"""

from typing import Any, Dict, Optional, Union
from pathlib import Path
import pickle
import plyvel

from exonware.xwsystem.io.serialization.base import ASerialization
from exonware.xwsystem.io.serialization.contracts import ISerialization
from exonware.xwsystem.io.errors import SerializationError


class XWLeveldbSerializer(ASerialization):
    """
    LevelDB serializer for persistent key-value storage.
    
    I: ISerialization (interface)
    A: ASerialization (abstract base)
    XW: XWLeveldbSerializer (concrete implementation)
    
    Note: plyvel requires C++ build tools on Windows. If installation fails,
    install exonware-xwformats[full] excluding plyvel, or use other database formats.
    """
    
    def __init__(self):
        """Initialize LevelDB serializer."""
        super().__init__()
    
    @property
    def codec_id(self) -> str:
        """Codec identifier."""
        return "leveldb"
    
    @property
    def media_types(self) -> list[str]:
        """Supported MIME types."""
        return ["application/x-leveldb"]
    
    @property
    def file_extensions(self) -> list[str]:
        """Supported file extensions."""
        return [".ldb", ".leveldb"]
    
    def encode(self, data: Any, options: Optional[Dict[str, Any]] = None) -> bytes:
        """
        Encode data to LevelDB-compatible bytes.
        
        Note: LevelDB requires file-based operations.
        This method pickles the data for transport.
        
        Args:
            data: Dictionary of key-value pairs
            options: Encoding options
            
        Returns:
            Pickled bytes
        """
        if not isinstance(data, dict):
            raise SerializationError(f"LevelDB expects dict, got {type(data)}")
        
        return pickle.dumps(data)
    
    def decode(self, data: bytes, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Decode LevelDB bytes to Python dict.
        
        Args:
            data: Pickled dict bytes
            options: Decoding options
            
        Returns:
            Dictionary of key-value pairs
        """
        return pickle.loads(data)
    
    def encode_to_file(self, data: Any, file_path: Union[str, Path], options: Optional[Dict[str, Any]] = None) -> None:
        """
        Encode data to LevelDB database file.
        
        Args:
            data: Dictionary of key-value pairs
            file_path: Path to LevelDB directory
            options: Encoding options (create_if_missing, etc.)
        """
        if not isinstance(data, dict):
            raise SerializationError(f"LevelDB expects dict, got {type(data)}")
        
        opts = options or {}
        create_if_missing = opts.get('create_if_missing', True)
        
        # Open LevelDB database
        db = plyvel.DB(str(file_path), create_if_missing=create_if_missing)
        
        try:
            # Write all key-value pairs
            for key, value in data.items():
                # Convert key to bytes
                key_bytes = key.encode('utf-8') if isinstance(key, str) else pickle.dumps(key)
                # Convert value to bytes
                value_bytes = pickle.dumps(value)
                db.put(key_bytes, value_bytes)
        finally:
            db.close()
    
    def decode_from_file(self, file_path: Union[str, Path], options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Decode LevelDB database file to Python dict.
        
        Args:
            file_path: Path to LevelDB directory
            options: Decoding options
            
        Returns:
            Dictionary of all key-value pairs
        """
        db = plyvel.DB(str(file_path), create_if_missing=False)
        
        try:
            result = {}
            # Read all key-value pairs
            for key_bytes, value_bytes in db:
                # Try to decode key as string first, then pickle
                try:
                    key = key_bytes.decode('utf-8')
                except UnicodeDecodeError:
                    key = pickle.loads(key_bytes)
                
                # Decode value
                value = pickle.loads(value_bytes)
                result[key] = value
            
            return result
        finally:
            db.close()


# Backward compatibility alias
LeveldbSerializer = XWLeveldbSerializer

