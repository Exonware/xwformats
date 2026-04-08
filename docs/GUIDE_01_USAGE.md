<!-- docs/GUIDE_01_USAGE.md (project usage, GUIDE_41_DOCS) -->
# xwformats — Usage Guide

**Last Updated:** 08-Feb-2026  
**Requirements source:** [REF_01_REQ.md](REF_01_REQ.md)

How to use xwformats (output of GUIDE_41_DOCS).

## Quick start

- **Facade:** `from exonware.xwformats import XWFormats as xf`, `xf.list_formats()`, `xf.get_serializer("parquet")` or `"ron"` then encode/decode. Converting between JSON/YAML/etc. works only if those codecs are registered (usually by importing xwsystem’s text serializers).
- **Auto-detection:** Importing xwformats registers **its** codecs (e.g. Parquet, RON, UBJSON) with xwsystem’s registry; extensions for CSV/JSON/TOML/YAML/XML appear when xwsystem registers them.

See [REF_14_DX.md](REF_14_DX.md) (key code, DX) and [REF_15_API.md](REF_15_API.md) (API reference). Project: [REF_22_PROJECT.md](REF_22_PROJECT.md). Format details: _archive/, changes/.

---

*Per GUIDE_00_MASTER and GUIDE_41_DOCS.*
