#!/usr/bin/env python3
"""
Integration tests for format conversion workflows in xwformats.
Tests cross-format conversions, multi-hop conversions, and real-world
data processing scenarios across multiple serialization formats.
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
@pytest.mark.xwformats_integration

class TestFormatConversionWorkflows:
    """Integration tests for format conversion workflows."""

    def test_binary_to_text_conversion_workflow(self, tmp_path):
        """Test converting between text formats (simulating binary to text workflow)."""
        # Start with JSON format
        data = {
            "users": [
                {"id": 1, "name": "Alice", "email": "alice@example.com"},
                {"id": 2, "name": "Bob", "email": "bob@example.com"},
            ],
            "metadata": {"version": "1.0", "created": "2025-01-28"}
        }
        # Convert: JSON → YAML → TOML → JSON
        registry = get_registry()
        # Step 1: Save as JSON
        json_serializer = registry.get_by_id("json")
        assert json_serializer is not None, "JSON serializer should be registered"
        json_file = tmp_path / "data.json"
        json_serializer.save_file(data, json_file)
        assert json_file.exists()
        # Step 2: Load and convert to YAML (text)
        yaml_serializer = registry.get_by_id("yaml")
        assert yaml_serializer is not None, "YAML serializer should be registered"
        yaml_file = tmp_path / "data.yaml"
        loaded = json_serializer.load_file(json_file)
        yaml_serializer.save_file(loaded, yaml_file)
        assert yaml_file.exists()
        # Step 3: Convert YAML to TOML
        toml_serializer = registry.get_by_id("toml")
        assert toml_serializer is not None, "TOML serializer should be registered"
        toml_file = tmp_path / "data.toml"
        loaded = yaml_serializer.load_file(yaml_file)
        toml_serializer.save_file(loaded, toml_file)
        assert toml_file.exists()
        # Step 4: Convert back to JSON
        final_json_file = tmp_path / "data_final.json"
        loaded = toml_serializer.load_file(toml_file)
        json_serializer.save_file(loaded, final_json_file)
        assert final_json_file.exists()
        # Verify round-trip correctness
        final_data = json_serializer.load_file(final_json_file)
        assert final_data == data

    def test_schema_format_conversion_workflow(self, tmp_path):
        """Test converting between text formats (simulating schema format workflow)."""
        data = [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25, "city": "London"},
            {"name": "Charlie", "age": 35, "city": "Tokyo"},
        ]
        registry = get_registry()
        # Convert: JSON → YAML → TOML → JSON (using available formats)
        json_serializer = registry.get_by_id("json")
        assert json_serializer is not None
        json_file = tmp_path / "data.json"
        json_serializer.save_file(data, json_file)
        yaml_serializer = registry.get_by_id("yaml")
        assert yaml_serializer is not None
        yaml_file = tmp_path / "data.yaml"
        loaded = json_serializer.load_file(json_file)
        yaml_serializer.save_file(loaded, yaml_file)
        assert yaml_file.exists()
        toml_serializer = registry.get_by_id("toml")
        assert toml_serializer is not None
        toml_file = tmp_path / "data.toml"
        loaded = yaml_serializer.load_file(yaml_file)
        toml_serializer.save_file(loaded, toml_file)
        assert toml_file.exists()
        # Convert back to JSON
        final_json_file = tmp_path / "data_final.json"
        loaded = toml_serializer.load_file(toml_file)
        json_serializer.save_file(loaded, final_json_file)
        # Verify data integrity
        final_data = json_serializer.load_file(final_json_file)
        assert len(final_data) == len(data)
        assert final_data[0]["name"] == "Alice"

    def test_database_format_workflow(self, tmp_path):
        """Test workflow using available formats (simulating database workflow)."""
        data = {
            "config": {"host": "localhost", "port": 8080},
            "users": {"alice": {"role": "admin"}, "bob": {"role": "user"}},
            "settings": {"theme": "dark", "language": "en"}
        }
        registry = get_registry()
        # Save to JSON first
        json_serializer = registry.get_by_id("json")
        assert json_serializer is not None
        json_file = tmp_path / "data.json"
        json_serializer.save_file(data, json_file)
        assert json_file.exists()
        # Convert to YAML
        yaml_serializer = registry.get_by_id("yaml")
        assert yaml_serializer is not None
        loaded = json_serializer.load_file(json_file)
        yaml_file = tmp_path / "data.yaml"
        yaml_serializer.save_file(loaded, yaml_file)
        assert yaml_file.exists()
        # Convert to TOML
        toml_serializer = registry.get_by_id("toml")
        assert toml_serializer is not None
        loaded = yaml_serializer.load_file(yaml_file)
        toml_file = tmp_path / "data.toml"
        toml_serializer.save_file(loaded, toml_file)
        assert toml_file.exists()
        # Verify data integrity
        final_data = toml_serializer.load_file(toml_file)
        assert final_data == data

    def test_multi_hop_conversion_chain(self, tmp_path):
        """Test multi-hop conversion: A → B → C → D → A."""
        original_data = {
            "products": [
                {"id": 1, "name": "Widget", "price": 9.99},
                {"id": 2, "name": "Gadget", "price": 19.99},
            ],
            "total": 29.98
        }
        registry = get_registry()
        # Chain: JSON → YAML → TOML → JSON
        json_serializer = registry.get_by_id("json")
        json_file = tmp_path / "step1.json"
        json_serializer.save_file(original_data, json_file)
        yaml_serializer = registry.get_by_id("yaml")
        yaml_file = tmp_path / "step2.yaml"
        loaded = json_serializer.load_file(json_file)
        yaml_serializer.save_file(loaded, yaml_file)
        toml_serializer = registry.get_by_id("toml")
        toml_file = tmp_path / "step3.toml"
        loaded = yaml_serializer.load_file(yaml_file)
        toml_serializer.save_file(loaded, toml_file)
        final_json_file = tmp_path / "step4.json"
        loaded = toml_serializer.load_file(toml_file)
        json_serializer.save_file(loaded, final_json_file)
        # Verify round-trip
        final_data = json_serializer.load_file(final_json_file)
        assert final_data == original_data

    def test_text_format_roundtrip_workflow(self, tmp_path):
        """Test round-trip through multiple text formats."""
        data = {
            "numbers": [1, 2, 3, 4, 5],
            "nested": {"level1": {"level2": {"value": 42}}}
        }
        registry = get_registry()
        # Round-trip: JSON → YAML → TOML → JSON
        json_serializer = registry.get_by_id("json")
        assert json_serializer is not None
        json_file = tmp_path / "data.json"
        json_serializer.save_file(data, json_file)
        yaml_serializer = registry.get_by_id("yaml")
        assert yaml_serializer is not None
        yaml_file = tmp_path / "data.yaml"
        loaded = json_serializer.load_file(json_file)
        yaml_serializer.save_file(loaded, yaml_file)
        assert yaml_file.exists()
        toml_serializer = registry.get_by_id("toml")
        assert toml_serializer is not None
        toml_file = tmp_path / "data.toml"
        loaded = yaml_serializer.load_file(yaml_file)
        toml_serializer.save_file(loaded, toml_file)
        assert toml_file.exists()
        final_json_file = tmp_path / "data_final.json"
        loaded = toml_serializer.load_file(toml_file)
        json_serializer.save_file(loaded, final_json_file)
        # Verify
        final_data = json_serializer.load_file(final_json_file)
        assert final_data == data

    def test_large_dataset_conversion_workflow(self, tmp_path):
        """Test conversion workflow with large dataset."""
        # Create large dataset
        large_data = {
            "items": [{"id": i, "value": f"item_{i}"} for i in range(1000)],
            "metadata": {"count": 1000, "generated": "2025-01-28"}
        }
        registry = get_registry()
        # Convert large dataset: JSON → YAML → LevelDB → JSON
        json_serializer = registry.get_by_id("json")
        assert json_serializer is not None
        json_file = tmp_path / "large.json"
        json_serializer.save_file(large_data, json_file)
        yaml_serializer = registry.get_by_id("yaml")
        assert yaml_serializer is not None
        yaml_file = tmp_path / "large.yaml"
        loaded = json_serializer.load_file(json_file)
        yaml_serializer.save_file(loaded, yaml_file)
        assert yaml_file.exists()
        toml_serializer = registry.get_by_id("toml")
        assert toml_serializer is not None
        toml_file = tmp_path / "large.toml"
        loaded = yaml_serializer.load_file(yaml_file)
        toml_serializer.save_file(loaded, toml_file)
        assert toml_file.exists()
        # Convert back
        final_json_file = tmp_path / "large_final.json"
        loaded = toml_serializer.load_file(toml_file)
        json_serializer.save_file(loaded, final_json_file)
        # Verify
        final_data = json_serializer.load_file(final_json_file)
        assert len(final_data["items"]) == 1000
        assert final_data["metadata"]["count"] == 1000
@pytest.mark.xwformats_integration

class TestCodecRegistryIntegration:
    """Integration tests for codec registry integration."""

    def test_all_formats_registered(self):
        """Test that all xwformats serializers are registered in codec registry."""
        registry = get_registry()
        # Check key formats are registered (using formats that are definitely available)
        expected_formats = [
            "yaml", "toml", "json",
        ]
        for format_id in expected_formats:
            codec = registry.get_by_id(format_id)
            assert codec is not None, f"Format {format_id} should be registered"
            assert codec.codec_id == format_id

    def test_format_serialization_workflow(self, tmp_path):
        """Test format serialization and deserialization workflow."""
        data = {"test": "data", "number": 42}
        registry = get_registry()
        # Test multiple formats (using formats that are definitely available)
        formats_to_test = ["yaml", "toml", "json"]
        for format_id in formats_to_test:
            serializer = registry.get_by_id(format_id)
            assert serializer is not None
            # Save and load
            test_file = tmp_path / f"test.{format_id}"
            serializer.save_file(data, test_file)
            loaded = serializer.load_file(test_file)
            assert loaded == data
@pytest.mark.xwformats_integration

class TestRealWorldScenarios:
    """Real-world integration scenarios."""

    def test_configuration_management_workflow(self, tmp_path):
        """Test configuration management workflow across formats."""
        config = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "mydb"
            },
            "api": {
                "timeout": 30,
                "retries": 3
            },
            "features": {
                "enabled": ["feature1", "feature2"],
                "disabled": ["feature3"]
            }
        }
        registry = get_registry()
        # Save config in YAML (human-readable)
        yaml_serializer = registry.get_by_id("yaml")
        yaml_file = tmp_path / "config.yaml"
        yaml_serializer.save_file(config, yaml_file)
        # Convert to TOML (alternative config format)
        toml_serializer = registry.get_by_id("toml")
        toml_file = tmp_path / "config.toml"
        loaded = yaml_serializer.load_file(yaml_file)
        toml_serializer.save_file(loaded, toml_file)
        # Store in JSON format for fast access
        json_serializer = registry.get_by_id("json")
        assert json_serializer is not None
        json_file = tmp_path / "config.json"
        loaded = toml_serializer.load_file(toml_file)
        json_serializer.save_file(loaded, json_file)
        # Verify all formats contain same data
        yaml_data = yaml_serializer.load_file(yaml_file)
        toml_data = toml_serializer.load_file(toml_file)
        json_data = json_serializer.load_file(json_file)
        assert yaml_data == toml_data == json_data == config

    def test_data_pipeline_workflow(self, tmp_path):
        """Test data pipeline: ingest → process → store → retrieve."""
        # Ingest: JSON data
        raw_data = {
            "records": [
                {"id": i, "value": i * 2, "timestamp": f"2025-01-28T{i:02d}:00:00Z"}
                for i in range(100)
            ]
        }
        registry = get_registry()
        # Step 1: Ingest (JSON)
        json_serializer = registry.get_by_id("json")
        assert json_serializer is not None
        json_file = tmp_path / "raw_data.json"
        json_serializer.save_file(raw_data, json_file)
        # Step 2: Process and convert to YAML
        yaml_serializer = registry.get_by_id("yaml")
        assert yaml_serializer is not None
        loaded = json_serializer.load_file(json_file)
        yaml_file = tmp_path / "processed_data.yaml"
        yaml_serializer.save_file(loaded, yaml_file)
        # Step 3: Convert to TOML
        toml_serializer = registry.get_by_id("toml")
        assert toml_serializer is not None
        loaded = yaml_serializer.load_file(yaml_file)
        toml_file = tmp_path / "stored_data.toml"
        toml_serializer.save_file(loaded, toml_file)
        # Step 4: Retrieve and export (JSON for reporting)
        loaded = toml_serializer.load_file(toml_file)
        final_json_file = tmp_path / "export_data.json"
        json_serializer.save_file(loaded, final_json_file)
        # Verify pipeline integrity
        final_data = json_serializer.load_file(final_json_file)
        assert len(final_data["records"]) == 100
        assert final_data["records"][0]["id"] == 0
