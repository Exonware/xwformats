<!-- docs/REF_51_TEST.md (output of GUIDE_51_TEST) -->
# xwformats — Test Status and Coverage

**Last Updated:** 08-Feb-2026  
**Requirements source:** [REF_01_REQ.md](REF_01_REQ.md)

Test status and coverage (output of GUIDE_51_TEST). Evidence: repo `tests/`, `docs/logs/tests/`. Test summaries in `docs/logs/tests/` (and optionally `docs/tests/` if runner is configured there).

## Test layers

xwformats uses a 4-layer test layout per GUIDE_51_TEST. Each layer has a dedicated directory and runner.

| Layer | Path | Purpose |
|-------|------|---------|
| **0.core** | `tests/0.core/` | Import and package sanity: `test_import.py` verifies package and format modules import; **REF_01_REQ / FR-007:** facade `list_formats()`, `get_serializer()`, and auto-detection (registry extensions after import). |
| **1.unit** | `tests/1.unit/` | Unit tests by format family under `formats_tests/`: `binary_tests/`, `database_tests/`, `schema_tests/`, `scientific_tests/`, `text_tests/`, plus `test_serializers_basic.py` for metadata/capabilities. |
| **2.integration** | `tests/2.integration/` | Scenarios and end-to-end: format conversion workflows, cross-format flows. |
| **3.advance** | `tests/3.advance/` | Performance and security: `test_performance.py`, `test_security.py`. |

## Running tests

From the **xwformats repo root** (with `src` on the path, e.g. `PYTHONPATH=src` or after `pip install -e .`):

```bash
python tests/runner.py
```

- **All layers (default):** runs 0.core → 1.unit → 2.integration → 3.advance in sequence.
- **Single layer:**
  - `python tests/runner.py --core` — Layer 0: core (import) tests only.
  - `python tests/runner.py --unit` — Layer 1: unit tests only.
  - `python tests/runner.py --integration` — Layer 2: integration tests only.
  - `python tests/runner.py --advance` — Layer 3: advance tests only.
- **Advance subsets:**
  - `python tests/runner.py --security` — security tests (delegated to 3.advance runner if present).
  - `python tests/runner.py --performance` — performance tests (delegated to 3.advance runner if present).

Output: terminal (colored/formatted) and a Markdown summary file. The main runner currently writes to `docs/tests/TEST_<timestamp>_SUMMARY.md`; evidence is also collected under `docs/logs/tests/` (see Evidence below).

## Evidence

| Location | Content |
|----------|---------|
| `tests/` | Source of all test modules and layer runners. |
| [logs/tests/](logs/tests/) | Test run summaries (TEST_*_SUMMARY.md); primary evidence for runs. |

---

*Per GUIDE_00_MASTER and GUIDE_51_TEST.*
