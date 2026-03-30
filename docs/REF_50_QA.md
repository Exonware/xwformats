# Quality assurance — xwformats

**Library:** exonware-xwformats  
**Produced by:** `GUIDE_50_QA.md`  
**Last Updated:** 26-Mar-2026

---

## Purpose

Quality **gates** and **readiness state** for releases. Full methodology: `.docs/guides/GUIDE_50_QA.md`.

---

## Gates (summary)

| Gate | Check | Owner |
|------|--------|--------|
| Tests | `python tests/runner.py` (layers 0–3 as configured) | TEST |
| Coverage | pytest-cov in `[dev]` when run in CI/local | TEST |
| Benchmarks | See `REF_54_BENCH.md` / `benchmarks/` when SLAs apply | BENCH |
| Docs | REF_* aligned with code; README matches `REF_14_DX` / `REF_15_API` | DOCS |

---

## Current readiness

| Criterion | State |
|-----------|--------|
| Core import / registration | Expected passing with `exonware-xwformats` + `exonware-xwlazy` |
| Full extra | Resolves on Windows (LevelDB/RocksDB wheels omitted on Win; see `REF_54_BENCH`) |
| Known platform issues | `docs/_archive/KNOWN_ISSUES.md`, `docs/logs/setup/` |

**Release go/no-go:** Record decisions under `docs/logs/releases/` when publishing (per `GUIDE_61_DEP`).

---

*QA orchestrates; TEST/DEBUG/FIX execute.*
