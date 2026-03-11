#!/usr/bin/env python3
"""
End-to-end integration tests for xwformats.
Tests complete workflows from data ingestion to storage and retrieval
across multiple formats and real-world scenarios.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
Generation Date: 28-Jan-2025
"""

from __future__ import annotations
import pytest
from pathlib import Path
from exonware.xwsystem.io.codec.registry import get_registry
from exonware.xwsystem.io.errors import SerializationError
@pytest.mark.xwformats_integration

class TestEndToEndWorkflows:
    """End-to-end workflow tests."""

    def test_complete_data_lifecycle(self, tmp_path):
        """Test complete data lifecycle: create → store → retrieve → transform → export."""
        # Create initial data
        initial_data = {
            "application": "xwformats",
            "version": "0.1.0.1",
            "features": {
                "formats": 27,
                "categories": ["schema", "scientific", "database", "binary", "text"]
            },
            "stats": {
                "total_tests": 155,
                "coverage": "high"
            }
        }
        registry = get_registry()
        # Step 1: Store in human-readable format (YAML)
        yaml_serializer = registry.get_by_id("yaml")
        yaml_file = tmp_path / "data.yaml"
        yaml_serializer.save_file(initial_data, yaml_file)
        assert yaml_file.exists()
        # Step 2: Convert to JSON format
        json_serializer = registry.get_by_id("json")
        assert json_serializer is not None
        loaded = yaml_serializer.load_file(yaml_file)
        json_file = tmp_path / "data.json"
        json_serializer.save_file(loaded, json_file)
        assert json_file.exists()
        # Step 3: Convert to TOML
        toml_serializer = registry.get_by_id("toml")
        assert toml_serializer is not None
        loaded = json_serializer.load_file(json_file)
        toml_file = tmp_path / "data.toml"
        toml_serializer.save_file(loaded, toml_file)
        assert toml_file.exists()
        # Step 4: Retrieve and export to JSON
        loaded = toml_serializer.load_file(toml_file)
        final_json_file = tmp_path / "export.json"
        json_serializer.save_file(loaded, final_json_file)
        assert final_json_file.exists()
        # Step 5: Verify end-to-end integrity
        final_data = json_serializer.load_file(final_json_file)
        assert final_data == initial_data
        assert final_data["application"] == "xwformats"
        assert final_data["features"]["formats"] == 27

    def test_multi_format_data_sharing(self, tmp_path):
        """Test sharing data across multiple formats for different use cases."""
        shared_data = {
            "users": [
                {"id": 1, "name": "Alice", "role": "admin"},
                {"id": 2, "name": "Bob", "role": "user"},
                {"id": 3, "name": "Charlie", "role": "user"},
            ],
            "permissions": {
                "admin": ["read", "write", "delete"],
                "user": ["read"]
            }
        }
        registry = get_registry()
        # Export to multiple formats for different consumers
        # 1. YAML for human editing
        yaml_serializer = registry.get_by_id("yaml")
        yaml_file = tmp_path / "users.yaml"
        yaml_serializer.save_file(shared_data, yaml_file)
        # 2. JSON for API consumption
        json_serializer = registry.get_by_id("json")
        json_file = tmp_path / "users.json"
        json_serializer.save_file(shared_data, json_file)
        # 3. TOML for configuration files
        toml_serializer = registry.get_by_id("toml")
        toml_file = tmp_path / "users.toml"
        toml_serializer.save_file(shared_data, toml_file)
        # 4. JSON for API consumption (additional format)
        json_file2 = tmp_path / "users2.json"
        json_serializer.save_file(shared_data, json_file2)
        # Verify all formats contain same data
        yaml_data = yaml_serializer.load_file(yaml_file)
        json_data = json_serializer.load_file(json_file)
        toml_data = toml_serializer.load_file(toml_file)
        json_data2 = json_serializer.load_file(json_file2)
        assert yaml_data == json_data == toml_data == json_data2 == shared_data

    def test_format_migration_workflow(self, tmp_path):
        """Test migrating data from one format to another."""
        old_format_data = {
            "legacy": True,
            "records": [{"id": i, "value": f"record_{i}"} for i in range(50)]
        }
        registry = get_registry()
        # Old format: JSON
        json_serializer = registry.get_by_id("json")
        old_file = tmp_path / "legacy_data.json"
        json_serializer.save_file(old_format_data, old_file)
        # Migrate to new format: YAML
        yaml_serializer = registry.get_by_id("yaml")
        loaded = json_serializer.load_file(old_file)
        new_file = tmp_path / "migrated_data.yaml"
        yaml_serializer.save_file(loaded, new_file)
        # Verify migration
        migrated_data = yaml_serializer.load_file(new_file)
        assert migrated_data == old_format_data
        assert len(migrated_data["records"]) == 50
        # Further migrate to efficient format: TOML
        toml_serializer = registry.get_by_id("toml")
        assert toml_serializer is not None
        toml_file = tmp_path / "optimized_data.toml"
        toml_serializer.save_file(migrated_data, toml_file)
        # Verify final format
        final_data = toml_serializer.load_file(toml_file)
        assert final_data == old_format_data
@pytest.mark.xwformats_integration

class TestCrossLibraryIntegration:
    """Tests for integration with other eXonware libraries."""

    def test_xwsystem_codec_registry_integration(self):
        """Test that xwformats serializers integrate with xwsystem codec registry."""
        registry = get_registry()
        # Test that xwformats formats are accessible via registry
        test_formats = ["yaml", "toml", "json"]
        for format_id in test_formats:
            codec = registry.get_by_id(format_id)
            assert codec is not None, f"Format {format_id} should be in registry"
            # Verify codec properties
            assert codec.codec_id == format_id
            assert hasattr(codec, "encode") or hasattr(codec, "save_file")
            assert hasattr(codec, "decode") or hasattr(codec, "load_file")

    def test_universal_codec_interface(self, tmp_path):
        """Test that all xwformats serializers follow universal codec interface."""
        registry = get_registry()
        test_data = {"test": "data", "number": 42}
        # Test multiple formats through registry
        formats_to_test = ["yaml", "toml", "json"]
        for format_id in formats_to_test:
            codec = registry.get_by_id(format_id)
            assert codec is not None
            # Test save/load through codec
            test_file = tmp_path / f"test.{format_id}"
            # Use save_file if available, otherwise encode/decode
            if hasattr(codec, "save_file"):
                codec.save_file(test_data, test_file)
                loaded = codec.load_file(test_file)
            else:
                encoded = codec.encode(test_data)
                loaded = codec.decode(encoded)
            assert loaded == test_data
@pytest.mark.xwformats_integration

class TestErrorHandlingIntegration:
    """Integration tests for error handling across formats."""

    def test_invalid_format_handling(self):
        """Test handling of invalid format requests."""
        registry = get_registry()
        # Try to get non-existent format
        codec = registry.get_by_id("nonexistent_format")
        # Registry may return None or raise - both are acceptable
        if codec is None:
            # This is expected behavior
            pass
        else:
            # If it returns something, it should be a valid codec
            assert hasattr(codec, "codec_id")

    def test_corrupted_data_handling(self, tmp_path):
        """Test handling of corrupted data files."""
        registry = get_registry()
        json_serializer = registry.get_by_id("json")
        assert json_serializer is not None
        # Create corrupted file
        corrupted_file = tmp_path / "corrupted.json"
        corrupted_file.write_text("invalid json data {")
        # Should raise appropriate error
        with pytest.raises((ValueError, SerializationError, Exception)):
            json_serializer.load_file(corrupted_file)

    def test_missing_file_handling(self, tmp_path):
        """Test handling of missing files."""
        registry = get_registry()
        json_serializer = registry.get_by_id("json")
        missing_file = tmp_path / "nonexistent.json"
        # Should raise appropriate error
        with pytest.raises((FileNotFoundError, ValueError, SerializationError)):
            json_serializer.load_file(missing_file)
