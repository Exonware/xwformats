# xwformats

**Many serialization formats, one package.** Schema (Protobuf, Parquet, Thrift, …), scientific (HDF5, Feather, Zarr, …), database (LMDB, LevelDB, …), plus binary and text. Same converter style as xwsystem; formats register on import. Pick **lite**, **lazy**, **full**, or **dev** extras to match how you deploy.

**Company:** eXonware.com · **Author:** eXonware Backend Team · **Email:** connect@exonware.com  

[![Status](https://img.shields.io/badge/status-beta-blue.svg)](https://exonware.com)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

---

## 📦 Install

| Install | What you get | When to use |
|---------|--------------|-------------|
| `pip install exonware-xwformats` | **Base** — `exonware-xwsystem[full]` (shared text/JSON stack, etc.) + lazy hooks | Heavier than core-only xwsystem; add `[full]` for extra heavyweight codecs. |
| `pip install exonware-xwformats[lazy]` | **Lazy** - `xwsystem[lazy]` + lazy extras | Matches lazy-optional stack in docs. |
| `pip install exonware-xwformats[full]` | **Full** - common format deps installed up front | Production or CI; on **Windows**, LevelDB/RocksDB wheels may be missing (see `docs/REF_54_BENCH.md`). |
| `pip install exonware-xwformats[dev]` | **Dev** - pytest, black, mypy, … | Contributors |

Base install pulls **`exonware-xwsystem[full]`** (CSV, JSON, TOML, YAML, XML, and other xwsystem optionals) and enables **xwlazy** when available. `[lazy]`, `[dev]`, and `[full]` are extras on top.

---

## 🚀 Quick start

```python
from exonware.xwformats import XWFormats

xf = XWFormats()
print(xf.list_formats())                       # All registered formats
data = xf.convert(json_bytes, "json", "yaml")  # Bidirectional conversion
ser = xf.get_serializer("parquet")
ser.encode(value)
ser.decode(data)
```

Importing xwformats registers its formats with xwsystem; use xwsystem's codec/facade for detection by file extension. See [REF_14_DX](docs/REF_14_DX.md) and [REF_15_API](docs/REF_15_API.md).

---

## ✨ What you get

| Area | What's in it |
|------|----------------|
| **Schema** | Protobuf, Parquet, Thrift, ORC, Cap'n Proto, FlatBuffers, Arrow. **Avro** is optional (may be off default import on some platforms - see `__init__.py` and `docs/_archive/KNOWN_ISSUES.md`). |
| **Scientific** | HDF5, Feather, Zarr, NetCDF, MAT. |
| **Database** | LMDB, LevelDB, RocksDB, GraphDB. |
| **Binary / text** | **UBJSON**, Bincode, Dill, Postcard, and **RON** are implemented in xwformats. **BSON**, **CSV, JSON, TOML, YAML, XML**, and other core xwsystem binaries are **xwsystem-only** — not registered or exported by xwformats. |
| **Integration** | Same converter/facade as xwsystem; codec registry updated on import. |

**Lite** = few deps. **Lazy** = optional format wheels on first use. **Full** = common optionals pre-installed. Platform notes (e.g. RocksDB on Windows): [docs/logs/setup/](docs/logs/setup/). Known issues: [docs/_archive/KNOWN_ISSUES.md](docs/_archive/KNOWN_ISSUES.md) and [REF_22_PROJECT.md](docs/REF_22_PROJECT.md#project-status-overview).

---

## 🌐 Ecosystem functional contributions

`xwformats` extends format coverage; sibling XW libs provide runtime loading strategy, registration, and downstream consumption layers.
You can use `xwformats` standalone for broad serializer coverage and conversion tasks.
Integrating with additional XW libraries is optional and mainly useful for enterprise and mission-critical pipelines that need unified runtime, storage, and query infrastructure.

| Supporting XW lib | What it provides to xwformats | Functional requirement it satisfies |
|------|----------------|----------------|
| **XWSystem** | Core codec registry/facade and serializer contracts that xwformats registers into. | One unified serialization API despite many optional format backends. |
| **XWLazy** | On-demand dependency loading/install behavior for optional format stacks. | Practical deployment of many formats without forcing heavy installs. |
| **XWData** | Higher-level data transformation workflows that consume xwformats codecs. | Real pipeline usage beyond encode/decode-only primitives. |
| **XWStorage** | Persistence engine integrations that use specialized format serializers. | Storage interoperability for scientific/schema/database-oriented payloads. |
| **XWJSON** | Binary JSON and local data-engine flows that can interoperate with format conversion paths. | Efficient local format conversion and transition workflows. |
| **XWQuery** | Query pipelines over data loaded via format serializers. | End-to-end analytics/transform use cases after format normalization. |

Competitive edge: instead of isolated serializer plugins, `xwformats` plugs into a shared runtime and data stack so advanced formats are immediately usable in storage/query/application workflows.

---

## 📖 Docs and tests

Aligned with project REFs and [docs/GUIDE_01_USAGE.md](docs/GUIDE_01_USAGE.md) (see [GUIDE_63_README](../.docs/guides/GUIDE_63_README.md) in the monorepo).

- **Start:** [docs/INDEX.md](docs/INDEX.md) - index and quick links.
- **Use:** [docs/GUIDE_01_USAGE.md](docs/GUIDE_01_USAGE.md) - usage and format list.
- **Requirements / status:** [docs/REF_01_REQ.md](docs/REF_01_REQ.md), [docs/REF_22_PROJECT.md](docs/REF_22_PROJECT.md).
- **API / design:** [docs/REF_15_API.md](docs/REF_15_API.md), [docs/REF_13_ARCH.md](docs/REF_13_ARCH.md), [docs/REF_14_DX.md](docs/REF_14_DX.md).
- **Tests:** [docs/REF_51_TEST.md](docs/REF_51_TEST.md). Summaries: [docs/logs/tests/](docs/logs/tests/). Run: `python tests/runner.py` or pytest from repo root.

---

## 📜 License and links

Apache-2.0 - see [LICENSE](LICENSE).

- **Homepage:** https://exonware.com  
- **Repository:** https://github.com/exonware/xwformats  

## ⏱️ Async Support

<!-- async-support:start -->
- xwformats is primarily synchronous in its current implementation.
- Source validation: 0 async def definitions and 0 await usages under src/.
- This module still composes with async-capable xw libraries at integration boundaries when needed.
<!-- async-support:end -->
Version: 0.9.0.30 | Updated: 10-Apr-2026

*Built with ❤️ by eXonware.com - Revolutionizing Python Development Since 2025*
