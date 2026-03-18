#!/usr/bin/env python3
"""
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
Generation Date: 04-Nov-2025
Test xwformats import and basic functionality.
Key code paths per REF_14_DX: XWFormats, list_formats, convert, get_serializer.
"""

from __future__ import annotations
import pytest
@pytest.mark.xwformats_core

def test_import_xwformats():
    """Test that xwformats can be imported."""
    import exonware.xwformats
    assert exonware.xwformats is not None
@pytest.mark.xwformats_core

def test_version_info():
    """Test that version information is available."""
    import re
    from exonware.xwformats import __version__, __author__, __email__, __company__
    assert re.match(r"^\d+\.\d+\.\d+(\.\d+)?$", __version__), f"__version__ should be semver-like, got {__version__!r}"
    assert __author__ == "eXonware Backend Team"
    assert __email__ == "connect@exonware.com"
    assert __company__ == "eXonware.com"
@pytest.mark.xwformats_core

def test_import_schema_formats():
    """Test that schema formats can be imported."""
    from exonware.xwformats.formats.schema import (
        ProtobufSerializer,
        ParquetSerializer,
        ThriftSerializer,
        OrcSerializer,
        CapnProtoSerializer,
        FlatBuffersSerializer,
        ArrowSerializer,
    )
    # Verify imports work
    assert ProtobufSerializer is not None
    assert ParquetSerializer is not None
    assert ArrowSerializer is not None
@pytest.mark.xwformats_core

def test_import_scientific_formats():
    """Test that scientific formats can be imported."""
    from exonware.xwformats.formats.scientific import (
        Hdf5Serializer,
        FeatherSerializer,
        ZarrSerializer,
        NetcdfSerializer,
        MatSerializer,
    )
    # Verify imports work
    assert Hdf5Serializer is not None
    assert FeatherSerializer is not None
@pytest.mark.xwformats_core

def test_import_database_formats():
    """Test that database formats can be imported."""
    from exonware.xwformats.formats.database import (
        LmdbSerializer,
        GraphDbSerializer,
        LeveldbSerializer,
        RocksdbSerializer,  # May be None if compilation failed
    )
    # Verify core database formats work
    assert LmdbSerializer is not None
    assert GraphDbSerializer is not None
    assert LeveldbSerializer is not None
    # RocksDB is optional - requires compilation and may not be available on Windows
    # Tests that require RocksDB use pytest.importorskip("rocksdb")
    if RocksdbSerializer is None:
        # RocksDB not available (compilation required) - this is expected on some platforms
        import warnings
        warnings.warn("RocksDB not available (requires compilation, may not work on Windows without build tools)")
    else:
        assert RocksdbSerializer is not None
@pytest.mark.xwformats_core

def test_import_text_formats():
    """Test that text formats can be imported."""
    from exonware.xwformats.formats.text import (
        CsvSerializer,
        YamlSerializer,
        TomlSerializer,
        XmlSerializer,
        RonSerializer,
    )
    # Verify imports work
    assert CsvSerializer is not None
    assert YamlSerializer is not None
    assert TomlSerializer is not None
    assert XmlSerializer is not None
    assert RonSerializer is not None
@pytest.mark.xwformats_core

def test_import_binary_formats():
    """Test that binary formats can be imported."""
    from exonware.xwformats.formats.binary import (
        UbjsonSerializer,
        BincodeSerializer,
        PostcardSerializer,
        DillSerializer,
    )
    # Verify imports work
    assert UbjsonSerializer is not None
    assert BincodeSerializer is not None
    assert PostcardSerializer is not None
    assert DillSerializer is not None
@pytest.mark.xwformats_core

def test_avro_import_handling():
    """Test that Avro import is handled gracefully if unavailable."""
    try:
        from exonware.xwformats.formats.schema import AvroSerializer
        assert AvroSerializer is not None
    except (ImportError, NameError):
        # Avro is optional (external dependency issue on some Python/OS combos).
        pass
@pytest.mark.xwformats_core

def test_codec_registry_integration():
    """Test that xwformats integrates with UniversalCodecRegistry."""
    from exonware.xwsystem.io.codec.registry import get_registry
    registry = get_registry()
    codecs = registry.list_codecs()
    # Check that enterprise formats are registered (some may be optional)
    # These should always be available (core formats)
    always_available_codecs = [
        'protobuf', 'parquet', 'thrift', 'flatbuffers', 'graphdb', 'leveldb',
    ]
    # Optional codecs (may not be available if dependencies not installed)
    optional_codecs = [
        'orc', 'capnproto', 'lmdb', 'rocksdb', 'ubjson',
        'hdf5', 'feather', 'zarr', 'netcdf', 'mat',
    ]
    # Check always available codecs
    for codec_id in always_available_codecs:
        assert codec_id in codecs, f"Codec {codec_id} not found in registry"
    # Optional codecs - check if they're available, but don't fail if not
    for codec_id in optional_codecs:
        if codec_id not in codecs:
            # Log that it's missing but don't fail - it's optional
            import warnings
            warnings.warn(f"Optional codec {codec_id} not available (dependency may be missing)")
@pytest.mark.xwformats_core

def test_get_codec_by_id():
    """Test that we can get codecs by ID from registry."""
    from exonware.xwsystem.io.codec.registry import get_registry
    registry = get_registry()
    # Test getting a few codecs (always available)
    protobuf_codec = registry.get_by_id('protobuf')
    assert protobuf_codec is not None
    assert protobuf_codec.format_name == "Protobuf"
    parquet_codec = registry.get_by_id('parquet')
    assert parquet_codec is not None
    assert parquet_codec.format_name == "Parquet"
    # Test optional codec (may not be available)
    hdf5_codec = registry.get_by_id('hdf5')
    if hdf5_codec is not None:
        assert hdf5_codec.format_name == "HDF5"
@pytest.mark.xwformats_core

def test_serializer_instantiation():
    """Test that serializers can be instantiated."""
    from exonware.xwformats.formats.schema import ProtobufSerializer, ParquetSerializer
    from exonware.xwformats.formats.scientific import Hdf5Serializer
    from exonware.xwformats.formats.binary import UbjsonSerializer
    # Test instantiation
    protobuf = ProtobufSerializer()
    assert protobuf.codec_id == "protobuf"
    parquet = ParquetSerializer()
    assert parquet.codec_id == "parquet"
    hdf5 = Hdf5Serializer()
    assert hdf5.codec_id == "hdf5"
    ubjson = UbjsonSerializer()
    assert ubjson.codec_id == "ubjson"
# ---------------------------------------------------------------------------
# REF_01_REQ / FR-007: Auto-detection and facade (import → registry + list_formats)
# ---------------------------------------------------------------------------
@pytest.mark.xwformats_core

def test_facade_list_formats_after_import():
    """After importing xwformats, XWFormats().list_formats() returns non-empty and includes xwformats codecs (REF_01_REQ auto-detection)."""
    import exonware.xwformats  # noqa: F401 - ensure registration happened
    from exonware.xwformats import XWFormats
    xf = XWFormats()
    formats = xf.list_formats()
    assert isinstance(formats, list)
    assert len(formats) > 0
    # At least one known xwformats codec should be present (core formats always registered)
    known_xwformats = {"parquet", "protobuf", "ubjson", "yaml", "csv", "toml", "xml"}
    assert known_xwformats.intersection(formats), f"Expected some of {known_xwformats} in list_formats(), got {formats[:20]}..."
@pytest.mark.xwformats_core

def test_facade_get_serializer_returns_codec():
    """XWFormats().get_serializer(name) returns a codec instance with encode/decode (REF_01_REQ sec. 6)."""
    from exonware.xwformats import XWFormats
    xf = XWFormats()
    ser = xf.get_serializer("ubjson")
    assert ser is not None
    assert hasattr(ser, "encode") and hasattr(ser, "decode")
    assert getattr(ser, "codec_id", None) == "ubjson" or "ubjson" in getattr(ser, "aliases", [])
@pytest.mark.xwformats_core

def test_auto_detection_extensions_after_import():
    """After importing xwformats, registry list_extensions includes extensions from xwformats (REF_01_REQ FR-007)."""
    from exonware.xwsystem.io.codec.registry import get_registry
    import exonware.xwformats  # noqa: F401
    registry = get_registry()
    exts = registry.list_extensions()
    # xwformats adds e.g. .parquet, .ubjson, .yaml, .csv
    expected_extensions = {".parquet", ".ubjson", ".yaml", ".csv", ".toml", ".xml"}
    found = expected_extensions.intersection(exts)
    assert found, f"Expected some of {expected_extensions} in registry.list_extensions() after import, got sample: {list(exts)[:30]}"
if __name__ == "__main__":
    pytest.main([__file__, "-v"])


