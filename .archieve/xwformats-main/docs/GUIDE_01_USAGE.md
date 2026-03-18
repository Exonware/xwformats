<!-- docs/GUIDE_01_USAGE.md (project usage, GUIDE_41_DOCS) -->
# xwformats - Usage Guide

**Last Updated:** 08-Feb-2026  
**Requirements source:** [REF_01_REQ.md](REF_01_REQ.md)

How to use xwformats (output of GUIDE_41_DOCS).

## Quick start

- **Facade:** `from exonware.xwformats import XWFormats` → `xf = XWFormats()`, `xf.list_formats()`, `xf.convert(data, "json", "yaml")`, `xf.get_serializer("parquet")` then encode/decode.
- **Auto-detection:** Importing xwformats registers its formats with xwsystem’s codec registry; xwcodec, xwfile, xwserialization then include xwformats extensions when choosing by file extension.

See [REF_14_DX.md](REF_14_DX.md) (key code, DX) and [REF_15_API.md](REF_15_API.md) (API reference). Project: [REF_22_PROJECT.md](REF_22_PROJECT.md). Format details: _archive/, changes/.

---

*Per GUIDE_00_MASTER and GUIDE_41_DOCS.*
