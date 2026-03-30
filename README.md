# xwformats

**Many serialization formats, one package.** Schema (Protobuf, Parquet, Thrift, …), scientific (HDF5, Feather, Zarr, …), database (LMDB, LevelDB, …), plus binary and text. Same converter style as xwsystem; formats register on import. Pick **lite**, **lazy**, **full**, or **dev** extras to match how you deploy.

**Company:** eXonware.com · **Author:** eXonware Backend Team · **Email:** connect@exonware.com  

[![Status](https://img.shields.io/badge/status-beta-blue.svg)](https://exonware.com)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Install

| Install | What you get | When to use |
|---------|--------------|-------------|
| `pip install exonware-xwformats` | **Lite** - `exonware-xwsystem` + `exonware-xwlazy` | Small install; add formats via `[full]` or lazy hooks. |
| `pip install exonware-xwformats[lazy]` | **Lazy** - `xwsystem[lazy]` + lazy extras | Matches lazy-optional stack in docs. |
| `pip install exonware-xwformats[full]` | **Full** - common format deps installed up front | Production or CI; on **Windows**, LevelDB/RocksDB wheels may be missing (see `docs/REF_54_BENCH.md`). |
| `pip install exonware-xwformats[dev]` | **Dev** - pytest, black, mypy, … | Contributors |

Base install always pulls **`exonware-xwsystem`** and **`exonware-xwlazy`**. `[lazy]`, `[dev]`, and `[full]` are extras.

---

## Quick start

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

## What you get

| Area | What's in it |
|------|----------------|
| **Schema** | Protobuf, Parquet, Thrift, ORC, Cap'n Proto, FlatBuffers, Arrow. **Avro** is optional (may be off default import on some platforms - see `__init__.py` and `docs/_archive/KNOWN_ISSUES.md`). |
| **Scientific** | HDF5, Feather, Zarr, NetCDF, MAT. |
| **Database** | LMDB, LevelDB, RocksDB, GraphDB. |
| **Binary / text** | BSON, UBJSON; CSV, YAML, TOML, XML, RON. |
| **Integration** | Same converter/facade as xwsystem; codec registry updated on import. |

**Lite** = few deps. **Lazy** = optional format wheels on first use. **Full** = common optionals pre-installed. Platform notes (e.g. RocksDB on Windows): [docs/logs/setup/](docs/logs/setup/). Known issues: [docs/_archive/KNOWN_ISSUES.md](docs/_archive/KNOWN_ISSUES.md) and [REF_22_PROJECT.md](docs/REF_22_PROJECT.md#project-status-overview).

---

## Docs and tests

Aligned with project REFs and [docs/GUIDE_01_USAGE.md](docs/GUIDE_01_USAGE.md) (see [GUIDE_63_README](../.docs/guides/GUIDE_63_README.md) in the monorepo).

- **Start:** [docs/INDEX.md](docs/INDEX.md) - index and quick links.
- **Use:** [docs/GUIDE_01_USAGE.md](docs/GUIDE_01_USAGE.md) - usage and format list.
- **Requirements / status:** [docs/REF_01_REQ.md](docs/REF_01_REQ.md), [docs/REF_22_PROJECT.md](docs/REF_22_PROJECT.md).
- **API / design:** [docs/REF_15_API.md](docs/REF_15_API.md), [docs/REF_13_ARCH.md](docs/REF_13_ARCH.md), [docs/REF_14_DX.md](docs/REF_14_DX.md).
- **Tests:** [docs/REF_51_TEST.md](docs/REF_51_TEST.md). Summaries: [docs/logs/tests/](docs/logs/tests/). Run: `python tests/runner.py` or pytest from repo root.

---

## License and links

MIT - see [LICENSE](LICENSE).

- **Homepage:** https://exonware.com  
- **Repository:** https://github.com/exonware/xwformats  

## Async Support

<!-- async-support:start -->
- xwformats is primarily synchronous in its current implementation.
- Source validation: 0 async def definitions and 0 await usages under src/.
- This module still composes with async-capable xw libraries at integration boundaries when needed.
<!-- async-support:end -->
Version: 0.9.0.24 | Updated: 31-Mar-2026

*Built with ❤️ by eXonware.com - Revolutionizing Python Development Since 2025*
