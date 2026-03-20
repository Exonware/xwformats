#!/usr/bin/env python3
"""
Unit tests for TOML serializer in xwformats.
Regression: list/tuple roots must round-trip (TOML requires a root table).
Aligned with GUIDE_51_TEST.md (layer 1.unit, text_tests mirror).
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
"""

from __future__ import annotations

import pytest

from exonware.xwformats.formats.text import TomlSerializer
from exonware.xwsystem.io.errors import SerializationError

pytest.importorskip("tomli")
pytest.importorskip("tomli_w")


@pytest.mark.xwformats_unit
class TestTomlSerializer:
    """Unit tests for TOML serializer."""

    def test_serializer_initialization(self):
        serializer = TomlSerializer()
        assert serializer.codec_id == "toml"
        assert ".toml" in serializer.file_extensions
        assert "application/toml" in serializer.media_types

    def test_encode_decode_dict_roundtrip(self):
        serializer = TomlSerializer()
        original = {"name": "Alice", "age": 30, "nested": {"k": 1}}
        blob = serializer.encode(original)
        assert isinstance(blob, bytes)
        assert serializer.decode(blob) == original

    def test_list_root_roundtrip_list_of_dicts(self):
        """Regression: integration JSON→YAML→TOML with list root must not fail."""
        serializer = TomlSerializer()
        original = [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25, "city": "London"},
        ]
        blob = serializer.encode(original)
        assert serializer.decode(blob) == original

    def test_list_root_roundtrip_primitive_list(self):
        serializer = TomlSerializer()
        original = [1, 2, 3]
        assert serializer.decode(serializer.encode(original)) == original

    def test_tuple_root_roundtrips_as_list(self):
        serializer = TomlSerializer()
        assert serializer.decode(serializer.encode((1, 2))) == [1, 2]

    def test_dict_with_reserved_keys_not_unwrapped(self):
        """Single-key dict must not be confused with our wrapper (two-key sentinel)."""
        serializer = TomlSerializer()
        original = {"_xwformats_list_root_": [1, 2, 3]}
        assert serializer.decode(serializer.encode(original)) == original

    def test_decode_invalid_toml_raises(self):
        serializer = TomlSerializer()
        with pytest.raises(SerializationError):
            serializer.decode(b"not valid toml <<<")
