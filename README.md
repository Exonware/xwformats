# xwformats

**Advanced serialization formats for xwsystem.** 20+ heavy or specialized formats (schema, scientific, database, binary, text) behind one facade; imports register into the xwsystem codec registry.

**Company:** eXonware.com · **Author:** eXonware Backend Team · **Email:** connect@exonware.com  
**Version:** See [version.py](src/exonware/xwformats/version.py) or PyPI. · **Updated:** See [version.py](src/exonware/xwformats/version.py) (`__date__`)

[![Status](https://img.shields.io/badge/status-beta-blue.svg)](https://exonware.com)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Install

| Install | What you get | When to use |
|---------|--------------|-------------|
| `pip install exonware-xwformats` | **Lite** - core + xwsystem only | Minimal footprint; you add formats as needed. |
| `pip install exonware-xwformats[lazy]` | **Lazy** - missing format deps install on first use | Development; optional formats without pre-installing everything. |
| `pip install exonware-xwformats[full]` | **Full** - common format deps pre-installed | Production or CI when you want all formats up front. |

Requires `exonware-xwsystem`. Same package; `[lazy]` and `[full]` are extras.

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

Importing xwformats registers its formats with xwsystem; use xwsystem’s codec/facade for auto-detection by file extension. See [REF_14_DX](docs/REF_14_DX.md) and [REF_15_API](docs/REF_15_API.md).

---

## What you get

| Area | What's in it |
|------|----------------|
| **Core formats from xwsystem** | Through the xwsystem dependency you get its 20+ built-in formats (JSON, YAML, TOML, XML, CSV, INI, JSON Lines, form data, multipart, MsgPack, BSON, CBOR, Pickle, Marshal, Plist, Sqlite3, Dbm, Shelve, and related archive formats). |
| **Schema** | Protobuf, Avro, Parquet, Thrift, ORC, Cap'n Proto, FlatBuffers, Arrow. |
| **Scientific** | HDF5, Feather, Zarr, NetCDF, MAT. |
| **Database** | LMDB, LevelDB, RocksDB, GraphDB. |
| **Binary** | BSON, UBJSON, bincode, dill, postcard. |
| **Text** | XML, RON, TOML, YAML, CSV. |
| **Integration** | Same converter/facade as xwsystem; auto-registration with codec registry on import. |

Lite = minimal deps. Lazy = optional format deps install on first use. Full = common optionals pre-installed. Platform notes (e.g. RocksDB on Windows) in [docs/logs/setup/](docs/logs/setup/). Known issues: [docs/_archive/KNOWN_ISSUES.md](docs/_archive/KNOWN_ISSUES.md) and [REF_22_PROJECT.md](docs/REF_22_PROJECT.md#project-status-overview).

---

## Docs and tests

Content in this README is aligned with the project REFs and [docs/GUIDE_01_USAGE.md](docs/GUIDE_01_USAGE.md) (per [GUIDE_63_README](../docs/guides/GUIDE_63_README.md)).

- **Start:** [docs/INDEX.md](docs/INDEX.md) — doc index and quick links.
- **Use it:** [docs/GUIDE_01_USAGE.md](docs/GUIDE_01_USAGE.md) — usage, key code, formats.
- **Requirements and status:** [docs/REF_01_REQ.md](docs/REF_01_REQ.md), [docs/REF_22_PROJECT.md](docs/REF_22_PROJECT.md).
- **API and design:** [docs/REF_15_API.md](docs/REF_15_API.md), [docs/REF_13_ARCH.md](docs/REF_13_ARCH.md), [docs/REF_14_DX.md](docs/REF_14_DX.md).
- **Tests:** See [docs/REF_51_TEST.md](docs/REF_51_TEST.md). Run via project test runner or pytest from project root.

---

## License and links

MIT — see [LICENSE](LICENSE).

- **Homepage:** https://exonware.com  
- **Repository:** https://github.com/exonware/xwformats  
- **Version:** `from exonware.xwformats import __version__` or `import exonware.xwformats; print(exonware.xwformats.__version__)`  

Contributing → CONTRIBUTING.md · Security → SECURITY.md (when present).

*Built with ❤️ by eXonware.com - Revolutionizing Python Development Since 2025*
