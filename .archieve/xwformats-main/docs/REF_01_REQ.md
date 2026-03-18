# Requirements Reference (REF_01_REQ)

**Project:** xwformats (exonware-xwformats)  
**Sponsor:** eXonware.com / eXonware Backend Team  
**Version:** 0.0.1  
**Last Updated:** 08-Feb-2026  
**Produced by:** [GUIDE_01_REQ.md](../../docs/guides/GUIDE_01_REQ.md)

---

## Purpose of This Document

This document is the **single source of raw and refined requirements** collected from the project sponsor and stakeholders. It is updated on every requirements-gathering run. When the **Clarity Checklist** (section 12) reaches the agreed threshold, use this content to fill REF_12_IDEA, REF_22_PROJECT, REF_13_ARCH, REF_14_DX, REF_15_API, and planning artifacts. Template structure: [GUIDE_01_REQ.md](../../docs/guides/GUIDE_01_REQ.md). **Note:** Sections 6–10 were populated by reverse-engineering from existing REF_15_API, REF_13_ARCH, and REF_22_PROJECT.

---

## 1. Vision and Goals

| Field | Content |
|-------|---------|
| One-sentence purpose | xwformats provides advanced, less-common, or dependency-heavy serialization formats (text, binary, archive, image, media, video, etc.) in a separate package from xwsystem so the core stays lean and only consumers who need these formats install them. |
| Primary users/beneficiaries | eXonware developers; downstream packages (e.g. xwstorage, xwquery); anyone interested in a specific format in xwformats who wants to extend or use it. |
| Success (6 mo / 1 yr) | Already successful. Primary use: xw libraries, especially xwstorage (many formats and data sources)—xwstorage should reuse xwformats. xwquery may use it (many formats) but not 100% decided. |
| Top 3–5 goals (ordered) | 1) Support at least 10 formats per serialization subcategory (schema, scientific, database, binary, text). 2) Support broader categories (archive, image, media, video) per xwsystem-style structure (serialization vs archive etc.). 3) Integration with xw libraries (xwstorage primary; xwquery possibly). 4) Keep advanced/heavy formats out of xwsystem (single responsibility). 5) Enable adopters to extend and use any format in xwformats. |
| Problem statement | Most libraries do not support serialization or codecs for advanced formats; in eXonware we support them through xwformats so users can extend from there. |

## 2. Scope and Boundaries

| In scope | Out of scope | Dependencies | Anti-goals |
|----------|--------------|--------------|------------|
| **Install modes:** Lite, lazy, full; xwlazy support is required and must remain. **xwsystem integration:** Converter/facade self-integration. **Auto-detection:** When xwformats (or xwjson, etc.) is imported, its extension support must be reflected in automatic format/codec detection—xwcodec, xwformats, xwfile, xwserialization should auto-detect by file extension and choose implementation based on what is imported. **Categories:** Serialization subcategories (schema, scientific, database, binary, text) with at least 10 formats each; broader categories (archive, image, media, video) also supported; categorization aligned with xwsystem (e.g. serialization vs archive as in xwsystem io/). | Built-in formats we write ourselves from scratch—avoid rewriting formats; reuse famous/established libraries and expose them in one place (xwformats). No net-new format implementations unless already present. | **Only:** xwlazy and xwsystem. No other dependencies. | Not to have all formats in the world. Goal: add any unique or uncommon format to xwformats only if it is used somewhere in xw libraries. |

## 3. Stakeholders and Sponsor

| Sponsor (name, role, final say) | Main stakeholders | External customers/partners | Doc consumers |
|----------------------------------|-------------------|-----------------------------|---------------|
| eXonware (company); eXonware Backend Team (author, maintainer, final say on scope and priorities). Same model as xwsystem. | eXonware library teams (xwsystem, xwlazy, xwstorage, xwquery, xwjson, xwentity, xwnode, xwdata, xwauth, xwchat, xwui); *-server maintainers; open-source contributors. | None currently. Future: open-source adopters; possible sponsorship or partnership. | Developers and internal eXonware teams; AI agents (Cursor, Cloud Code); downstream REF_22 / REF_13 / REF_15 owners. |

## 4. Compliance and Standards

| Regulatory/standards | Security & privacy | Certifications/evidence |
|----------------------|--------------------|--------------------------|
| OWASP Top 10 alignment; resource limits and secure codecs; no code execution from untrusted data; path traversal protection; input validation. Mars Standard / NASA-style traceability and compliance evidence in docs/compliance where applicable. Industry norms for serialization (e.g. safe XML with defusedxml, forbid_dtd). | Auth and secrets handled by callers (xwauth) or app; xwformats provides safe codecs, path validation, and secure defaults. No PII stored in xwformats; audit logging and classification are app-level. | SOC2 or similar only if required by production use or government contracts; for now no formal cert. Compliance gap-analysis and risk-assessment under docs/compliance. |

## 5. Product and User Experience

| Main user journeys/use cases | Developer persona & 1–3 line tasks | Usability/accessibility | UX/DX benchmarks |
|-----------------------------|------------------------------------|--------------------------|------------------|
| (1) **Import and auto-detect:** Developer imports xwformats; extension support is reflected in auto-detection—use codec/facade without specifying format. (2) **Direct format use:** Use a specific format (e.g. Parquet, HDF5) directly when needed. (3) **Bidirectional conversion:** Convert from and to any supported format via xwsystem converter; simple, bidirectional. | Developer who cares about inputs and outputs: minimal code to read/write or convert between advanced formats; no specific persona beyond that. | Reuse 100% whatever is in xwsystem; minimize code writing. Same patterns, contracts, and defaults as xwsystem serialization. | Seamless experience for the developer—same feel as serialization in xwsystem; no friction when moving between xwsystem formats and xwformats formats. |

## 6. API and Surface Area

| Main entry points / "key code" | Easy (1–3 lines) vs advanced | Integration/existing APIs | Not in public API |
|--------------------------------|------------------------------|---------------------------|-------------------|
| **Facade:** `XWFormats` — conversion, serializer lookup, format listing. **Converter:** `FormatConverter` for convert(data, from_format, to_format). **Discovery:** Serializers register with xwsystem `UniversalCodecRegistry` at import; access via registry or facade. **Per-format:** get_serializer(format_name) then encode/decode. (Code-derived from REF_15_API, `__init__.py`.) | **Easy:** `from exonware.xwformats import XWFormats`; `xf.list_formats()`; `xf.convert(data, "json", "yaml")`; `ser = xf.get_serializer("yaml")` then encode/decode. **Advanced:** Format-specific options (e.g. Parquet compression, CSV dialect); registry access; streaming or custom codecs. | Must integrate with xwsystem codec registry, XWIO, converter; xwdata, xwjson, xwstorage consume for format-agnostic load/save and conversion pipeline. | Internal format-module implementation details; raw backend APIs; registry internals. Only expose what is stable and documented in REF_15_API. |

## 7. Architecture and Technology

| Required/forbidden tech | Preferred patterns | Scale & performance | Multi-language/platform |
|-------------------------|--------------------|----------------------|-------------------------|
| **Required:** Python 3.x (per pyproject); xwlazy and xwsystem only. **Forbidden:** No hard dependency on external services or DBs for core; no code execution from untrusted format data. Optional native builds (e.g. RocksDB on Windows) documented in logs/setup/. | Strategy (per-format encode/decode); Registry (format registration, xwsystem codec alignment); Facade (XWFormats); Contract/base (contracts.py, base.py). Format families in subpackages: binary, database, schema, scientific, text. (REF_13_ARCH.) | Optional formats; lazy loading to avoid loading unused backends. No explicit SLA; same expectations as xwsystem for common serialization (e.g. sub-50ms for 1MB where applicable). | Python reference implementation; multi-language via xwsystem contracts/specs if later. Windows, Linux, macOS; platform build notes (e.g. RocksDB) in docs. |

## 8. Non-Functional Requirements (Five Priorities)

| Security | Usability | Maintainability | Performance | Extensibility |
|----------|-----------|-----------------|-------------|---------------|
| Input validation; no code execution from format data; safe codecs and path validation; auth/secrets at app level. (Section 4 and REF_22.) | Clear API; platform build notes (e.g. RocksDB on Windows) in logs/setup/; reuse xwsystem patterns to minimize code. | Contracts/base/facade; 4-layer tests; REF_* traceability; format modules pluggable. | Optional formats; lazy loading; no mandatory heavy backends for lite install. | Pluggable format modules; registry-based discovery; add formats used in xw libraries. |

## 9. Milestones and Timeline

| Major milestones | Definition of done (first) | Fixed vs flexible |
|------------------|----------------------------|-------------------|
| **M1 — Core format set and converter:** v0.1.x (Done). **M2 — All enterprise format families:** v0.1.x (Done). **M3 — REF_* and doc placement compliance:** v0.1.x (Done). (From REF_22_PROJECT.) Future: 10+ formats per category; broader categories (archive, image, media, video) as needed by xw libraries. | M1 DoD: Core format set available; converter/facade integrated with xwsystem; lite/lazy/full modes. | Dates flexible; scope (formats used in xw libraries, xwsystem alignment) is fixed. |

## 10. Risks and Assumptions

| Top risks | Assumptions | Kill/pivot criteria |
|-----------|-------------|---------------------|
| (1) Heavy optional deps (e.g. RocksDB, HDF5) can make install/build hard on some platforms—mitigate with docs (logs/setup/), lite/lazy. (2) Registry/auto-detect consistency across xwsystem, xwformats, xwjson—maintain single contract. (3) Format proliferation—only add formats used in xw libraries (anti-goal). | xwsystem and xwlazy remain stable and provide codec registry and lazy install; downstream (xwstorage, xwquery, xwdata, xwjson) consume via facade/registry; no net-new format implementations (reuse existing libs). | If xwsystem drops codec registry or lazy model, or if scope expands to “all formats in the world,” direction would need to change. |

## 11. Workshop / Session Log (Optional)

| Date | Type | Participants | Outcomes |
|------|------|---------------|----------|
| 08-Feb-2026 | REF_01 discovery | Sponsor / Requirements Collector | REF_01_REQ created; Section 1 questions posed |
| 08-Feb-2026 | REF_01 discovery | Sponsor / Requirements Collector | Section 1 (Vision and Goals) filled from sponsor answers |
| 08-Feb-2026 | REF_01 discovery | Sponsor / Requirements Collector | Section 1 category clarification (A+B: serialization subcategories + broader archive/image/media/video); Section 2 (Scope and Boundaries) filled |
| 08-Feb-2026 | REF_01 discovery | Sponsor / Requirements Collector | Section 3 (Stakeholders and Sponsor) filled—generic, aligned with xwsystem |
| 08-Feb-2026 | REF_01 discovery | Sponsor / Requirements Collector | Section 4 (Compliance and Standards) filled—same as xwsystem |
| 08-Feb-2026 | REF_01 discovery | Sponsor / Requirements Collector | Section 5 (Product and UX) filled: import + auto-detect or direct format; bidirectional conversion; reuse xwsystem; seamless like xwsystem serialization |
| 08-Feb-2026 | REF_01 discovery | Sponsor / Requirements Collector | Sections 6–10 filled by reverse-engineering from REF_15_API, REF_13_ARCH, REF_22_PROJECT |
| 08-Feb-2026 | REF_01 discovery | Sponsor / Requirements Collector | Confirmation summary added; clarity checklist set to 14/14; Ready to fill downstream docs |
| 08-Feb-2026 | REF_01 feed | Requirements Collector | Fed REF_01_REQ into REF_12_IDEA, REF_22_PROJECT, REF_13_ARCH, REF_15_API; created REF_14_DX |
| 08-Feb-2026 | Downstream | Requirements Collector | Code: facade/converter use get_by_id/list_codecs (xwsystem API). Tests: 0.core facade + auto-detection tests. Docs: INDEX, REF_51_TEST, README. FR-007 → Done. |
| 08-Feb-2026 | CONT DOWNSTREAM | Requirements Collector | Verified REF_12_IDEA, REF_22_PROJECT, REF_13_ARCH, REF_14_DX, REF_15_API aligned with REF_01_REQ; added NFR sec. 8 traceability to REF_22 |
| 08-Feb-2026 | CONT DOWNSTREAM (codebase + tests) | Requirements Collector | Package __init__ (REF_01, REF_14_DX, REF_15_API); tests/conftest (REF_01, REF_51, REF_14_DX); 0.core/test_import docstring REF_14_DX key code |

---

## Requirements Understood — Summary (for sponsor confirmation)

- **Vision:** xwformats provides advanced, less-common, or heavy serialization formats (text, binary, archive, image, media, video, etc.) in a separate package from xwsystem so the core stays lean and only consumers who need these formats install them.
- **In scope:** Lite/lazy/full install; xwlazy required; xwsystem converter/facade integration; auto-detection so importing xwformats (or xwjson) registers extensions with codec/facade; serialization subcategories (schema, scientific, database, binary, text) with ≥10 formats each; broader categories (archive, image, media, video) aligned with xwsystem.
- **Out of scope:** Writing our own format implementations; reuse established libraries and expose in xwformats only.
- **Top goals (ordered):** (1) ≥10 formats per serialization subcategory; (2) broader categories (archive, image, media, video); (3) integration with xw libraries (xwstorage primary, xwquery possibly); (4) keep xwsystem lean (single responsibility); (5) enable adopters to extend and use formats.
- **Main constraints:** Dependencies only xwlazy and xwsystem; anti-goal = not “all formats in the world”—add only formats used in xw libraries; compliance and NFRs same as xwsystem.

*If this summary is accurate, requirements phase is complete and downstream docs (REF_12_IDEA, REF_22_PROJECT, REF_13_ARCH, REF_14_DX, REF_15_API, plans) can be filled from this REF_01_REQ. Correct any item above if needed.*

---

## 12. Clarity Checklist

| # | Criterion | ☐ |
|---|-----------|---|
| 1 | Vision and one-sentence purpose filled and confirmed | ☑ |
| 2 | Primary users and success criteria defined | ☑ |
| 3 | Top 3–5 goals listed and ordered | ☑ |
| 4 | In-scope and out-of-scope clear | ☑ |
| 5 | Dependencies and anti-goals documented | ☑ |
| 6 | Sponsor and main stakeholders identified | ☑ |
| 7 | Compliance/standards stated or deferred | ☑ |
| 8 | Main user journeys / use cases listed | ☑ |
| 9 | API / "key code" expectations captured | ☑ |
| 10 | Architecture/technology constraints captured | ☑ |
| 11 | NFRs (Five Priorities) addressed | ☑ |
| 12 | Milestones and DoD for first milestone set | ☑ |
| 13 | Top risks and assumptions documented | ☑ |
| 14 | Sponsor confirmed vision, scope, priorities | ☑ |

**Clarity score:** 14 / 14. **Ready to fill downstream docs?** ☑ Yes
