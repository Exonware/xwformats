# RocksDB on Windows — Build and Install Notes

**Source:** docs/_archive/INSTALL_CXX_BUILD_TOOLS.md and INSTALL_ROCKSDB_WINDOWS.md (archived; value preserved here)  
**Last Updated:** 08-Feb-2026  
**Scope:** xwformats dependency python-rocksdb on Windows

---

## Overview

`python-rocksdb` on Windows typically requires compilation from source (Cython + RocksDB C++). This needs **Microsoft Visual C++ Build Tools** and, for a reliable build, the **Developer Command Prompt** or a properly configured PATH.

---

## 1. Install C++ Build Tools (Windows)

### Option 1: Visual Studio Build Tools (recommended)

1. **Download:** [Build Tools for Visual Studio 2022](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022).
2. **Install:** Run installer → select **"Desktop development with C++"** workload (MSVC, Windows SDK, CMake).
3. **Verify:** Open a new terminal and run:
   ```powershell
   where cl
   # Should show path under Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC\...
   ```

### Option 2: Full Visual Studio Community

- Download Visual Studio Community 2022, select **"Desktop development with C++"** workload.

### Option 3: Chocolatey

```powershell
choco install visualstudio2022buildtools --package-parameters "--add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
```

After install, **restart the terminal** (and if needed, the machine) so PATH is updated.

---

## 2. Install python-rocksdb

### Recommended: Developer Command Prompt

1. Open **"Developer Command Prompt for VS 2022"** (or **"x64 Native Tools Command Prompt"**).
2. Navigate to project and install:
   ```cmd
   cd d:\OneDrive\DEV\exonware\xwformats
   pip install python-rocksdb --no-cache-dir
   ```
3. Verify:
   ```cmd
   python -c "import rocksdb; print('Success!')"
   ```

### Alternative: Regular terminal after PATH is set

If `cl` is on PATH (e.g. after restarting terminal):

```powershell
cd d:\OneDrive\DEV\exonware\xwformats
pip install python-rocksdb
```

### Pre-built wheels (if available)

```powershell
pip install --only-binary :all: python-rocksdb
```

If this fails, a source build (with C++ tools) is required.

---

## 3. Troubleshooting

| Error | Action |
|-------|--------|
| "Microsoft Visual C++ 14.0 or greater is required" | Install Build Tools with "Desktop development with C++"; use Developer Command Prompt for install. |
| "Cannot open include file: 'rocksdb/db.h'" | python-rocksdb builds RocksDB from source; ensure network/disk space; use Developer Command Prompt. |
| Cython / CompileError on .pyx | Try `pip install Cython==3.0.0` then reinstall; or try `python-rocksdb==0.6.9`. |
| LINK LNK1104 'python312.lib' | Ensure Python dev headers (usually with standard Python install). |

---

## 4. After Installation

- Run tests: `python tests/runner.py` or `python -m pytest tests/1.unit/formats_tests/database_tests/test_rocksdb.py -v`.
- REF_13_ARCH and REF_22_PROJECT reference this log for RocksDB/Windows platform notes.

---

*Value extracted from _archive; original install docs removed. Per GUIDE_41_DOCS.*
