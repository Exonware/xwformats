# Architecture Reference — exonware-xwformats

**Library:** exonware-xwformats  
**Producing guide:** GUIDE_13_ARCH  
**Last Updated:** 08-Feb-2026  
**Requirements source:** [REF_01_REQ.md](REF_01_REQ.md)

---

## Overview

xwformats provides **advanced, less-common, or dependency-heavy serialization formats** as an extended layer on top of xwsystem, keeping the core lightweight. Architecture follows eXonware contracts/base/facade patterns; format modules are pluggable and optional (lite/lazy/full install). **xwlazy support is required** and must remain; when xwformats is imported, its format extensions are reflected in automatic format/codec detection (xwcodec, xwfile, xwserialization).

**Design Philosophy:** Single responsibility for heavyweight formats; converter and facade align with xwsystem; optional deps via lazy/full install; add only formats used in xw libraries (anti-goal: not “all formats in the world”).

---

## High-Level Structure

```
xwformats/
+-- contracts.py      # Interfaces (IClass)
+-- base.py            # Abstract bases (AClass)
+-- facade.py          # Public API and converter
+-- converter.py       # Format conversion (xwsystem integration)
+-- errors.py          # Exceptions
+-- defs.py            # Constants, enums
+-- config.py          # Configuration
+-- version.py
+-- formats/
    +-- binary/        # BSON, UBJSON, bincode, dill, postcard
    +-- database/      # LMDB, LevelDB, RocksDB, GraphDB
    +-- schema/        # Protobuf, Avro, Parquet, Thrift, ORC, Cap'n Proto, FlatBuffers, Arrow
    +-- scientific/    # HDF5, Feather, Zarr, NetCDF, MAT
    +-- text/          # XML, RON, TOML, YAML, CSV
```

---

## Boundaries

- **Public API:** Facade and converter expose format registration, encode/decode, and conversion to/from xwsystem formats. Entry points used by xwdata, xwjson, xwstorage. Serializers register with xwsystem `UniversalCodecRegistry` at import so auto-detection (by file extension) includes xwformats formats when the package is imported.
- **Formats:** Each format family (binary, database, schema, scientific, text) lives in its own subpackage; each format module implements contracts and is registered for discovery. **Broader categories** (archive, image, media, video) are in scope per REF_01_REQ—structure aligned with xwsystem io/ when added.
- **Converter:** Single converter bridges xwsystem and xwformats; delegates to format-specific serializers.
- **Dependencies:** Only xwlazy and xwsystem; no other dependencies.

---

## Design Patterns

- **Strategy:** Per-format encode/decode; format selection by media type or name.
- **Registry:** Format registration and discovery (align with xwsystem codec registry where applicable).
- **Facade:** Public API hides format set and optional-dependency loading.
- **Contract/base:** Interfaces in `contracts.py`, abstract bases in `base.py`.

---

## Delegation

- **xwsystem:** Core serialization, codec base, validation, security; xwformats extends with enterprise formats.
- **xwjson:** XWJSON as universal intermediate; format conversion pipeline (xwformats ↔ xwjson ↔ xwdata).
- **xwdata:** Consumes xwformats for format-agnostic data load/save.

---

## Layering

1. **Contracts:** Serializer/format interfaces.
2. **Base:** Abstract format implementations and shared logic.
3. **Facade / Converter:** Public API and format conversion.
4. **Formats:** Per-format modules (binary, database, schema, scientific, text).

---

## Install Modes

- **Lite:** Minimal or no optional format deps; core converter/facade.
- **Lazy:** Optional deps loaded on first use (per GUIDE_00_MASTER lazy install).
- **Full:** All format backends available; C++/native build required for RocksDB on some platforms.

**Platform / build notes:** On Windows, RocksDB (python-rocksdb) typically requires Microsoft Visual C++ Build Tools and a Developer Command Prompt for a source build. Detailed steps and troubleshooting: [logs/setup/ROCKSDB_WINDOWS_BUILD.md](logs/setup/ROCKSDB_WINDOWS_BUILD.md).

---

## Traceability

- **Requirements:** [REF_01_REQ.md](REF_01_REQ.md) (source) → [REF_22_PROJECT.md](REF_22_PROJECT.md)
- **Ideas:** [REF_12_IDEA.md](REF_12_IDEA.md)
- **DX:** [REF_14_DX.md](REF_14_DX.md)
- **API:** [REF_15_API.md](REF_15_API.md)

---

*See GUIDE_13_ARCH.md for architecture process.*
