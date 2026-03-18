<!-- docs/REF_15_API.md (output of GUIDE_15_API) -->
# xwformats - API Reference

**Last Updated:** 08-Feb-2026  
**Requirements source:** [REF_01_REQ.md](REF_01_REQ.md) sec. 6

API reference for xwformats (output of GUIDE_15_API). Serializers and format support. See [REF_22_PROJECT.md](REF_22_PROJECT.md); legacy format docs in _archive/.

**Auto-detection (REF_01_REQ):** When xwformats is imported, its format extensions must be reflected in automatic format/codec detection (xwcodec, xwfile, xwserialization). Serializers register with xwsystem `UniversalCodecRegistry` at import time so that choosing by file extension includes xwformats formats when the package is loaded.

## Public surface (alignment with `__all__`)

The package exposes the following from `exonware.xwformats` (aligned with `src/exonware/xwformats/__init__.py`):

| Symbol | Description |
|--------|-------------|
| `__version__` | Package version string. |
| `__author__`, `__email__`, `__company__` | Version metadata. |
| `XWFormats` | Main facade: format conversion, serializer lookup, format listing. |

All format serializers are registered with xwsystem’s `UniversalCodecRegistry` at import time and are available via the registry or the facade.

## Main entry points

### 1. Facade: `XWFormats`

Primary public API. Use for conversion, serializer access, and listing formats.

- **Import:** `from exonware.xwformats import XWFormats`
- **Constructor:** `XWFormats(conversion_mode='direct'|'via_json'|'via_xwjson', enable_caching=True, **options)`
- **Methods:**
  - `convert(data, from_format, to_format, options=None)` — Convert data between two formats (by codec_id).
  - `get_serializer(format_name)` — Return the serializer instance for a format (by codec_id).
  - `list_formats()` — Return list of registered format codec IDs.

### 2. Converter: `FormatConverter`

Used internally by the facade; can be used directly for conversion without the facade.

- **Import:** `from exonware.xwformats.converter import FormatConverter`
- **Constructor:** `FormatConverter()`
- **Methods:** `convert(data, from_format, to_format, options=None)` — Same semantics as facade `convert`; uses xwsystem registry for serializers.

### 3. Format registration and discovery

- Serializers are registered with xwsystem’s codec registry at package import (see `__init__.py`).
- **Registry access:** `from exonware.xwsystem.io.codec.registry import get_registry` then `get_registry().get_by_id(format_name)` or `get_registry().list_codecs()`.
- **Serializer usage:** Each serializer implements encode/decode per xwsystem contracts: `encode(value, options=None)`, `decode(data, options=None)`; `codec_id`, `file_extensions`, `media_types`, etc.

### 4. Encode / decode (per-format)

Get a serializer from the facade or registry, then call encode/decode:

- `serializer.encode(value, options=None)` → bytes or str (depending on format).
- `serializer.decode(data, options=None)` → Python data (dict, list, etc.) or format-specific type.

Options are format-specific (e.g. Parquet compression, CSV dialect).

## Quick start

```python
from exonware.xwformats import XWFormats

xf = XWFormats()
# List available formats
print(xf.list_formats())

# Convert between formats (e.g. JSON bytes → YAML string)
# (Obtain JSON bytes from your source; here assumed as bytes.)
json_bytes = b'{"a": 1, "b": 2}'
yaml_result = xf.convert(json_bytes, "json", "yaml")

# Or use a serializer directly
ser = xf.get_serializer("yaml")
encoded = ser.encode({"key": "value"})
decoded = ser.decode(encoded)
```

For format-specific options and capabilities, see [REF_13_ARCH.md](REF_13_ARCH.md) (format families) and the implementation under `src/exonware/xwformats/formats/`.

---

*Per GUIDE_00_MASTER and GUIDE_15_API. Requirements: [REF_01_REQ.md](REF_01_REQ.md).*
