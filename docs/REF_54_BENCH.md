# Benchmarks & performance — xwformats

**Library:** exonware-xwformats  
**Produced by:** `GUIDE_54_BENCH.md`  
**Last Updated:** 26-Mar-2026

---

## Purpose

Performance expectations, **SLAs** (when defined), and where benchmark campaigns live. Methodology: `.docs/guides/GUIDE_54_BENCH.md`.

---

## SLAs

| Area | Target | Notes |
|------|--------|--------|
| Import / cold start | Keep lite install lean | Base deps: `exonware-xwlazy`, `exonware-xwsystem` |
| Format encode/decode | Per-format; no global SLA yet | Add when campaigns exist |
| Optional native deps | **Windows:** `plyvel`, `python-rocksdb` are excluded from `[full]` (PEP 508 markers) | Install via conda / WSL / Linux CI if needed |

---

## Benchmark layout

| Location | Contents |
|----------|----------|
| `benchmarks/` (repo root) | Dated campaigns: `YYYYMMDD-benchmark <title>/` with `scripts/`, `data/`, `benchmarks/` per guide |
| `docs/logs/tests/` | Test orchestration summaries (not perf benches) |

---

## Next steps

When performance work is scheduled: add a campaign under `benchmarks/`, record baselines, and link runs here.

---

*Measure before optimizing; route regressions via `GUIDE_62_FEED`.*
