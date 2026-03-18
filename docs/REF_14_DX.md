# Developer Experience Reference — xwformats (REF_14_DX)

**Library:** exonware-xwformats  
**Last Updated:** 08-Feb-2026  
**Requirements source:** [REF_01_REQ.md](REF_01_REQ.md) sec. 5–6  
**Producing guide:** [GUIDE_14_DX.md](../../docs/guides/GUIDE_14_DX.md)

---

## Purpose

DX contract for xwformats: happy paths, "key code," and ergonomics. Filled from REF_01_REQ. Developer experience should be **seamless**—same feel as serialization in xwsystem; no friction when moving between xwsystem formats and xwformats formats. Reuse 100% whatever is in xwsystem; minimize code writing.

---

## Key code (1–3 lines)

| Task | Code |
|------|------|
| Import and list formats | `from exonware.xwformats import XWFormats` then `xf = XWFormats()`; `xf.list_formats()` |
| Convert between formats | `xf.convert(data, "json", "yaml")` (bidirectional; uses xwsystem converter) |
| Use a specific format (encode/decode) | `ser = xf.get_serializer("yaml")` then `ser.encode(value)`, `ser.decode(data)` |
| Auto-detect by extension | Import xwformats once; then use xwsystem codec/facade (xwcodec, xwfile, xwserialization)—extension support is reflected automatically when xwformats is imported. |

---

## Developer persona (from REF_01_REQ sec. 5)

Developer who cares about **inputs and outputs**: minimal code to read/write or convert between advanced formats. No specific persona beyond that. Primary users: eXonware developers; downstream packages (xwstorage, xwquery); anyone interested in a specific format who wants to extend or use it.

---

## Easy vs advanced

| Easy (1–3 lines) | Advanced |
|------------------|----------|
| `XWFormats()`; `list_formats()`; `convert(data, from_fmt, to_fmt)`; `get_serializer(name)` then encode/decode. Auto-detect by extension after importing xwformats. | Format-specific options (e.g. Parquet compression, CSV dialect); registry access (`get_registry().get(format_name)`); streaming or custom codecs. |

---

## Main entry points (from REF_01_REQ sec. 6)

- **Facade:** `XWFormats` — conversion, serializer lookup, format listing.
- **Converter:** `FormatConverter` (direct use for convert without facade).
- **Discovery:** Serializers register with xwsystem `UniversalCodecRegistry` at import; access via registry or facade.
- **Per-format:** `get_serializer(format_name)` then `encode(value, options=None)` / `decode(data, options=None)`.

---

## Usability expectations (from REF_01_REQ sec. 5, sec. 8)

Clear API; reuse 100% xwsystem patterns; same contracts and defaults as xwsystem serialization. Platform build notes (e.g. RocksDB on Windows) in [logs/setup/](logs/setup/). Seamless experience—like serialization in xwsystem; no friction between xwsystem and xwformats formats.

---

## User journeys (from REF_01_REQ sec. 5)

1. **Import and auto-detect:** Developer imports xwformats; extension support is reflected in auto-detection; use codec/facade without specifying format.
2. **Direct format use:** Use a specific format (e.g. Parquet, HDF5) directly when needed.
3. **Bidirectional conversion:** Convert from and to any supported format via xwsystem converter; simple, bidirectional.

---

*See [REF_01_REQ.md](REF_01_REQ.md), [REF_15_API.md](REF_15_API.md), and [REF_22_PROJECT.md](REF_22_PROJECT.md). Per GUIDE_14_DX.*
