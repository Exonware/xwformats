# Idea Reference — exonware-xwformats

**Company:** eXonware.com  
**Producing guide:** GUIDE_12_IDEA  
**Last Updated:** 08-Feb-2026  
**Requirements source:** [REF_01_REQ.md](REF_01_REQ.md)

---

## Overview

xwformats provides **advanced, less-common, or dependency-heavy serialization formats** (text, binary, archive, image, media, video, etc.) in a separate package from xwsystem so the core stays lean and only consumers who need these formats install them. Serialization subcategories: schema, scientific, database, binary, text (≥10 formats per category); broader categories (archive, image, media, video) aligned with xwsystem. This document captures product direction and ideas; approved ideas flow to [REF_22_PROJECT.md](REF_22_PROJECT.md) and [REF_13_ARCH.md](REF_13_ARCH.md).

### Alignment with eXonware 5 Priorities

- **Security:** Input validation, no code execution from format data.
- **Usability:** Clear API, install guides (C++/RocksDB etc. in docs/_archive).
- **Maintainability:** Contracts/base/facade, 4-layer tests, REF_*.
- **Performance:** Optional formats; lazy loading where applicable.
- **Extensibility:** Pluggable format modules.

**Related Documents:**
- [REF_01_REQ.md](REF_01_REQ.md) — Requirements (source)
- [REF_22_PROJECT.md](REF_22_PROJECT.md) — Project requirements
- [REF_13_ARCH.md](REF_13_ARCH.md) — Architecture
- [REF_14_DX.md](REF_14_DX.md) — Developer experience
- [REF_15_API.md](REF_15_API.md) — API reference
- [REF_35_REVIEW.md](REF_35_REVIEW.md) — Review summary

---

## Product Direction (from REF_22)

### ✅ [IDEA-001] Enterprise formats layer

**Status:** ✅ Approved → Implemented  
**Date:** 07-Feb-2026

**Problem:** xwsystem must stay lean; heavyweight formats (Protobuf, Parquet, HDF5, LMDB, etc.) need a dedicated home with optional deps.

**Proposed Solution:** xwformats as single-responsibility library: schema (Protobuf, Avro, Parquet, Thrift, ORC, Cap'n Proto, FlatBuffers), scientific (HDF5, Feather, Zarr, NetCDF, MAT), database (LMDB, LevelDB, RocksDB, GraphDB), binary (UBJSON, Bincode, Dill, Postcard). **Text:** **RON** in xwformats only; CSV, JSON, TOML, YAML, XML, **BSON**, and other core xwsystem codecs stay in **xwsystem** (not registered by xwformats).

**Outcome:** Implemented; lite/lazy/full install modes; converter/facade integration with xwsystem. See REF_22_PROJECT FR-001–FR-006.

---

### ✅ [IDEA-002] Converter and facade alignment

**Status:** ✅ Approved → Implemented  
**Date:** 07-Feb-2026

**Problem:** Format conversion and Firebase replacement (storage/serialization) require a single converter/facade that delegates to xwsystem and optional xwformats format backends.

**Proposed Solution:** Converter and facade in xwformats align with xwsystem; optional deps via lazy/full install.

**Outcome:** Implemented; integration with xwdata, xwjson (format conversion pipeline).

---

### ✅ [IDEA-003] Auto-detection on import (from REF_01_REQ)

**Status:** ✅ Approved → In scope  
**Date:** 08-Feb-2026

**Problem:** When a developer imports xwformats (or xwjson), extension support should appear in automatic format/codec detection so xwcodec, xwfile, xwserialization can choose implementation by file extension based on what is imported.

**Proposed Solution:** Serializers register with xwsystem `UniversalCodecRegistry` at package import; importing xwformats adds its format extensions to auto-detection. Same pattern for xwjson when imported.

**Outcome:** In scope per REF_01_REQ sec. 2; implementation aligns with REF_15_API (registry at import time).

---

### 🔍 [IDEA-004] Broader categories (archive, image, media, video)

**Status:** 🔍 Proposed  
**Date:** 08-Feb-2026

**Problem:** REF_01_REQ calls for broader categories (archive, image, media, video) in addition to serialization subcategories (schema, scientific, database, binary, text), aligned with xwsystem structure.

**Proposed Solution:** Add or document format families for archive, image, media, video as needed by xw libraries (e.g. xwstorage); align with xwsystem io/ (e.g. serialization vs archive). Add only formats used in xw libraries (anti-goal: not “all formats in the world”).

**Outcome:** Forward-looking; track in REF_22 when new categories are needed.

---

## Idea Catalog

| ID       | Title                     | Status   | Links       |
|----------|---------------------------|----------|-------------|
| IDEA-001 | Enterprise formats layer  | Approved | REF_22 FR-* |
| IDEA-002 | Converter/facade align   | Approved | REF_22      |
| IDEA-003 | Auto-detection on import | Approved | REF_01_REQ sec. 2 |
| IDEA-004 | Broader categories (archive, image, media, video) | Proposed | REF_01_REQ |

---

*See GUIDE_12_IDEA.md for idea process. Requirements: [REF_01_REQ.md](REF_01_REQ.md) → REF_22_PROJECT.md.*
