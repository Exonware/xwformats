# xwformats - Known Issues

**Company:** eXonware.com  
**Author:** Eng. Muhammad AlShehri  
**Email:** connect@exonware.com  
**Date:** 04-Nov-2025

---

## Avro Support - External Dependency Bug

**Issue:** Avro serialization currently unavailable on Python 3.12 Windows due to cramjam bug

**Status:** External dependency issue (not a bug in xwformats)

**Details:**
- **Library:** fastavro depends on cramjam
- **Platform:** Python 3.12 on Windows
- **Error:** `NameError: name 'cramjam' is not defined`
- **Root Cause:** cramjam package has initialization bug on Python 3.12 Windows
- **Upstream Issue:** https://github.com/milesgranger/cramjam-python/issues

**Workaround:**
Until cramjam fixes the upstream bug, Avro support is excluded from default imports on affected platforms.

**Alternative Solutions:**
1. Use Python 3.11 or earlier on Windows
2. Use Python 3.12 on Linux/macOS (works fine)
3. Use alternative schema formats (Parquet, Protobuf, Thrift)

**Note:** This is NOT a workaround in our code - we are following DEV_GUIDELINES.md by:
- Documenting the root cause (external cramjam bug)
- Not hiding the error with try/except everywhere
- Making the limitation explicit and documented
- Waiting for upstream fix rather than maintaining complex workarounds

**Expected Resolution:**
When cramjam releases a fix for Python 3.12 Windows, Avro will work automatically without any changes to xwformats.

---

## Other Platform-Specific Issues

### LevelDB - Requires C++ Build Tools on Windows

**Issue:** plyvel (LevelDB Python bindings) requires C++ compilation on Windows

**Platforms Affected:** Windows

**Solution:**
1. Install Microsoft Visual C++ Build Tools
2. Or skip LevelDB format (other database formats available)

**Note:** This is documented in requirements.txt and is a known limitation of plyvel package.

### Cap'n Proto - Requires C++ Build Tools

**Issue:** pycapnp requires C++ compilation

**Platforms Affected:** All platforms  

**Solution:**
1. Install appropriate C++ compiler for your platform
2. Or skip Cap'n Proto format (other schema formats available)

**Note:** This is documented in requirements.txt.

---

## Installation Recommendations

### Development
```bash
pip install exonware-xwformats[lazy]
```
- Auto-installs working dependencies on demand
- Skips packages that fail to install (like plyvel on Windows without C++)
- Best for development and testing

### Production
```bash
pip install exonware-xwformats[full]
```
- Pre-install all dependencies
- Test thoroughly on target platform
- Document any platform-specific limitations

### Minimal
```bash
pip install exonware-xwformats
```
- Core dependency only
- Use with caution - format imports will fail without dependencies

