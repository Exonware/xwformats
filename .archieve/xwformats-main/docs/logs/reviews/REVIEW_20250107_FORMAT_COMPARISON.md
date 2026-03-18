# Review: Format Comparison (xwsystem vs xwformats) — xwformats

**Date:** 2025-01-07  
**Source:** docs/_archive/FORMAT_COMPARISON.md (archived; value extracted here)  
**Artifact type:** Overlap analysis and design decisions  
**Scope:** BSON, CSV, YAML, TOML, XML in both xwsystem and xwformats

---

## Summary

Comparison of overlapping formats between xwsystem and xwformats. **Decision:** xwformats retains BSON, CSV, YAML, TOML, XML for a single registry and facade used by xwdata/xwjson/xwstorage; xwsystem remains the richer implementation for metadata and features (e.g. incremental YAML, XML sanitization). No removal of these formats from xwformats.

---

## Overlapping Formats

| Format | xwsystem | xwformats | Note |
|--------|----------|-----------|------|
| BSON   | Core binary | Enterprise binary | Both present; xwsystem has auto-wrap/unwrap. |
| CSV    | Core text   | Enterprise text   | xwsystem has .tsv/.psv; xwformats has encode_to_file/decode_from_file. |
| YAML   | Core text   | Enterprise text   | xwsystem has incremental streaming; xwformats has file I/O. |
| TOML   | Core text   | Enterprise text   | xwsystem has None handling, auto-wrap; xwformats has file I/O. |
| XML    | Core text   | Enterprise text   | xwsystem has xmltodict, sanitization, type preservation. |

---

## Verdicts (Preserved for Rationale)

- **xwsystem:** Stronger metadata, security, and feature set; was missing encode_to_file/decode_from_file (may be added in xwsystem).
- **xwformats:** Provides file I/O and a single facade/registry for all formats consumed by xwdata, xwjson, xwstorage; keeping overlaps avoids forcing consumers to switch codecs by layer.

---

## Action Items (Historical)

1. Add encode_to_file/decode_from_file to xwsystem serializers where applicable (xwsystem scope).
2. **Do not remove** BSON, CSV, YAML, TOML, XML from xwformats; REF_22 and REF_13 list them as part of the enterprise format set.

---

## Traceability

- **Requirements:** REF_22_PROJECT (FR-004: binary and text formats).
- **Architecture:** REF_13_ARCH (format families, delegation to xwsystem).
- **This review:** Design rationale for retaining overlapping formats in xwformats.

---

*Value extracted from _archive; original file removed. Per GUIDE_35_REVIEW.*
