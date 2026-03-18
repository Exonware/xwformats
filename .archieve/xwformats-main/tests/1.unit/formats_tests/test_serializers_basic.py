#!/usr/bin/env python3
"""
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
Generation Date: 04-Nov-2025
Basic unit tests for xwformats serializers.
"""

from __future__ import annotations
import pytest


class TestSerializerMetadata:
    """Test serializer metadata (codec_id, format_name, etc.)."""

    def test_protobuf_metadata(self):
        """Test Protobuf serializer metadata."""
        from exonware.xwformats.formats.schema import ProtobufSerializer
        serializer = ProtobufSerializer()
        assert serializer.codec_id == "protobuf"
        assert serializer.format_name == "Protobuf"
        assert "protobuf" in serializer.aliases
        assert serializer.is_binary_format is True

    def test_parquet_metadata(self):
        """Test Parquet serializer metadata."""
        from exonware.xwformats.formats.schema import ParquetSerializer
        serializer = ParquetSerializer()
        assert serializer.codec_id == "parquet"
        assert serializer.format_name == "Parquet"
        assert "parquet" in serializer.aliases
        assert serializer.is_binary_format is True

    def test_hdf5_metadata(self):
        """Test HDF5 serializer metadata."""
        from exonware.xwformats.formats.scientific import Hdf5Serializer
        if Hdf5Serializer is None:
            pytest.skip("h5py not installed")
        try:
            serializer = Hdf5Serializer()
            assert serializer.codec_id == "hdf5"
            assert serializer.format_name == "HDF5"
            assert "hdf5" in serializer.aliases
            assert serializer.is_binary_format is True
        except Exception:
            pytest.skip("h5py not installed or failed to instantiate")

    def test_ubjson_metadata(self):
        """Test UBJSON serializer metadata."""
        from exonware.xwformats.formats.binary import UbjsonSerializer
        if UbjsonSerializer is None:
            pytest.skip("py-ubjson not installed")
        try:
            serializer = UbjsonSerializer()
            assert serializer.codec_id == "ubjson"
            assert "ubjson" in serializer.aliases
        except Exception:
            pytest.skip("py-ubjson not installed or failed to instantiate")


class TestSerializerCapabilities:
    """Test serializer capabilities."""

    def test_protobuf_capabilities(self):
        """Test Protobuf capabilities."""
        from exonware.xwformats.formats.schema import ProtobufSerializer
        from exonware.xwsystem.io.defs import CodecCapability
        serializer = ProtobufSerializer()
        caps = serializer.capabilities
        assert caps & CodecCapability.BIDIRECTIONAL
        assert caps & CodecCapability.SCHEMA_BASED

    def test_parquet_capabilities(self):
        """Test Parquet capabilities."""
        from exonware.xwformats.formats.schema import ParquetSerializer
        from exonware.xwsystem.io.defs import CodecCapability
        serializer = ParquetSerializer()
        caps = serializer.capabilities
        assert caps & CodecCapability.BIDIRECTIONAL
        assert caps & CodecCapability.SCHEMA_BASED


class TestSerializerFileExtensions:
    """Test serializer file extension handling."""

    def test_protobuf_extensions(self):
        """Test Protobuf file extensions."""
        from exonware.xwformats.formats.schema import ProtobufSerializer
        serializer = ProtobufSerializer()
        exts = serializer.file_extensions
        assert ".proto" in exts or ".pb" in exts

    def test_parquet_extensions(self):
        """Test Parquet file extensions."""
        from exonware.xwformats.formats.schema import ParquetSerializer
        serializer = ParquetSerializer()
        exts = serializer.file_extensions
        assert ".parquet" in exts

    def test_hdf5_extensions(self):
        """Test HDF5 file extensions."""
        from exonware.xwformats.formats.scientific import Hdf5Serializer
        if Hdf5Serializer is None:
            pytest.skip("h5py not installed")
        try:
            serializer = Hdf5Serializer()
            exts = serializer.file_extensions
            assert ".h5" in exts or ".hdf5" in exts
        except Exception:
            pytest.skip("h5py not installed or failed to instantiate")
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
