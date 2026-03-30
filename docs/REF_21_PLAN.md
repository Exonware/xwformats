# Planning reference — xwformats

**Library:** exonware-xwformats  
**Produced by:** `GUIDE_21_PLAN.md`  
**Last Updated:** 26-Mar-2026

---

## Purpose

Single place for **lifecycle position** and **where plans live** for this package. Detailed templates live in the monorepo `.docs/guides/GUIDE_21_PLAN.md`.

---

## Current phase

| Phase | Focus | Status |
|-------|--------|--------|
| III — Development | Format modules, codec registration, tests | Active (beta) |
| IV — Quality loop | TEST → DEBUG → FIX → BENCH → QA | Ongoing |
| V — Release | Version bump, PyPI (per `GUIDE_61_DEP`) | As needed |

---

## Plan artifacts

| Location | Use |
|----------|-----|
| `docs/logs/plans/PLAN_*.md` | Time-stamped execution plans when used |
| `REF_22_PROJECT.md` | Milestones and FR/NFR |
| `REF_50_QA.md` | Release readiness gates |

---

## Routing

- **Ideas / scope:** `REF_12_IDEA.md` → `REF_22_PROJECT.md`  
- **Execution:** `GUIDE_21_PLAN` → DEV (`GUIDE_31` / `GUIDE_32_DEV_PY`) → REVIEW → TEST  

---

*Keep this file short; link to plans and REF_22_PROJECT for detail.*
