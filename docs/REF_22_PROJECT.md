# Project Reference — xwformats

**Library:** exonware-xwformats  
**Last Updated:** 08-Feb-2026  
**Requirements source:** [REF_01_REQ.md](REF_01_REQ.md)

Requirements and project status (output of GUIDE_22_PROJECT). Per REF_35_REVIEW.

---

## Vision

xwformats provides **advanced, less-common, or dependency-heavy serialization formats** (text, binary, archive, image, media, video, etc.) in a separate package from xwsystem so the core stays lean and only consumers who need these formats install them. It delivers schema (Protobuf, Avro, Parquet, Thrift, ORC, Cap'n Proto, FlatBuffers), scientific (HDF5, Feather, Zarr, NetCDF, MAT), database (LMDB, LevelDB, RocksDB, GraphDB), binary (BSON, UBJSON), text (XML, RON, TOML, YAML, CSV), integrates with xwsystem converter/facade for format conversion and Firebase replacement (storage/serialization), and supports broader categories (archive, image, media, video) aligned with xwsystem.

---

## Goals (from REF_01_REQ, ordered)

1. **≥10 formats per serialization subcategory:** Schema, scientific, database, binary, text—each with at least 10 formats.
2. **Broader categories:** Archive, image, media, video per xwsystem-style structure (serialization vs archive etc.).
3. **Integration with xw libraries:** xwstorage primary; xwquery possibly; xwdata, xwjson (format conversion pipeline).
4. **Single responsibility:** Heavyweight formats live here; xwsystem stays lean.
5. **Traceability and extensibility:** REF_22_PROJECT, REF_35_REVIEW, logs under docs/; enable adopters to extend and use any format in xwformats.

---

## Scope boundaries (from REF_01_REQ)

| In scope | Out of scope | Dependencies | Anti-goals |
|----------|--------------|--------------|------------|
| Lite/lazy/full install; xwlazy required; xwsystem converter/facade integration; auto-detection (import xwformats → extensions in codec/facade); serialization subcategories + broader categories. | Writing our own format implementations; reuse established libraries and expose in xwformats only. | **Only:** xwlazy and xwsystem. | Not “all formats in the world”—add only formats used in xw libraries. |

---

## Functional Requirements (Summary)

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-001 | Schema formats (Protobuf, Avro, Parquet, Thrift, ORC, Cap'n Proto, FlatBuffers) | High | Done |
| FR-002 | Scientific formats (HDF5, Feather, Zarr, NetCDF, MAT) | High | Done |
| FR-003 | Database formats (LMDB, LevelDB, RocksDB, GraphDB) | Medium | Done |
| FR-004 | Binary (BSON, UBJSON) and text (XML, RON, TOML, YAML, CSV) | High | Done |
| FR-005 | Converter/facade integration with xwsystem | High | Done |
| FR-006 | Lite/lazy/full install modes; xwlazy support required | High | Done |
| FR-007 | Auto-detection: importing xwformats (or xwjson) registers extension support with codec/facade (xwcodec, xwfile, xwserialization) | High | Done |

---

## Non-Functional Requirements (5 Priorities — from REF_01_REQ sec. 8)

1. **Security:** Input validation; no code execution from format data; safe codecs and path validation; auth/secrets at app level.
2. **Usability:** Clear API; platform build notes (e.g. RocksDB on Windows) in [logs/setup/](logs/setup/); reuse xwsystem patterns to minimize code.
3. **Maintainability:** Contracts/base/facade; 4-layer tests; REF_* traceability; format modules pluggable.
4. **Performance:** Optional formats; lazy loading; no mandatory heavy backends for lite install.
5. **Extensibility:** Pluggable format modules; registry-based discovery; add formats used in xw libraries.

---

## Project Status Overview

- **Current phase:** Beta (High). Binary, database, schema, scientific, text formats; converter, facade; 0.core, 1.unit, 2.integration, 3.advance.
- **Docs:** docs/ with REF_*, test logs under docs/logs/tests/; REF_22_PROJECT (this file), REF_35_REVIEW; historical change notes and fix guides in [docs/_archive/](_archive/).
- **Integration:** xwsystem, xwdata, xwjson (format conversion pipeline).
- **Known issues:** See [docs/_archive/KNOWN_ISSUES.md](_archive/KNOWN_ISSUES.md) for platform/dependency issues (e.g. Avro on Python 3.12 Windows); current status in REF_35_REVIEW and REF_51_TEST.

---

## Milestones (from REF_01_REQ)

| Milestone | Target | Status |
|-----------|--------|--------|
| M1 — Core format set and converter | v0.1.x | Done |
| M2 — All enterprise format families | v0.1.x | Done |
| M3 — REF_* and doc placement compliance | v0.1.x | Done (REF_22, root .md → docs/) |
| Future | — | ≥10 formats per category; broader categories (archive, image, media, video) as needed by xw libraries |

---

## Traceability

- **Requirements:** [REF_01_REQ.md](REF_01_REQ.md) (source).
- **Project → Arch/Idea/DX/API:** This document → [REF_13_ARCH.md](REF_13_ARCH.md), [REF_12_IDEA.md](REF_12_IDEA.md), [REF_14_DX.md](REF_14_DX.md), [REF_15_API.md](REF_15_API.md).
- **Review evidence:** [REF_35_REVIEW.md](REF_35_REVIEW.md), [logs/reviews/REVIEW_20260207_PROJECT_STATUS.md](logs/reviews/REVIEW_20260207_PROJECT_STATUS.md).

---

*See GUIDE_22_PROJECT.md for requirements process.*
