# Documentation index — xwformats

**Last Updated:** 25-Mar-2026  

Navigation hub for xwformats. **Rule:** only `README.md` at repo root; everything else is under `docs/` ([GUIDE_41_DOCS](../../.docs/guides/GUIDE_41_DOCS.md)).

---

## Repo layout (documentation)

```
xwformats/
├── README.md                 ← only Markdown at root
├── LICENSE
├── docs/                     ← all project docs
│   ├── INDEX.md              ← this file
│   ├── README.md             ← docs landing
│   ├── REF_*.md, GUIDE_01_USAGE.md
│   ├── changes/              ← stubs → _archive
│   ├── _archive/             ← full historical write-ups
│   └── logs/                 ← evidence (tests, reviews, compliance)
└── src/, tests/, …
```

---

## References (REF_*)

| Document | Purpose |
|----------|---------|
| [REF_01_REQ.md](REF_01_REQ.md) | Requirements |
| [REF_22_PROJECT.md](REF_22_PROJECT.md) | Vision, milestones, **status overview** |
| [REF_12_IDEA.md](REF_12_IDEA.md) | Ideas / direction |
| [REF_13_ARCH.md](REF_13_ARCH.md) | Architecture |
| [REF_14_DX.md](REF_14_DX.md) | Developer experience |
| [REF_15_API.md](REF_15_API.md) | API reference |
| [REF_35_REVIEW.md](REF_35_REVIEW.md) | Review summary |
| [REF_51_TEST.md](REF_51_TEST.md) | Test status |
| [REF_21_PLAN.md](REF_21_PLAN.md) | Lifecycle / planning pointer |
| [REF_50_QA.md](REF_50_QA.md) | Quality gates & readiness |
| [REF_54_BENCH.md](REF_54_BENCH.md) | Benchmarks & performance notes |

---

## Usage

| Document | Purpose |
|----------|---------|
| [GUIDE_01_USAGE.md](GUIDE_01_USAGE.md) | Install modes, examples, key workflows |

---

## Historical and compliance (not root-level)

| Location | Contents |
|----------|----------|
| [_archive/](_archive/) | **Full** KNOWN_ISSUES, CRITICAL_FIXES_APPLIED, XWFORMATS_COMPLETE_FIX_GUIDE |
| [changes/](changes/) | Short redirects into `_archive/` (keeps deep links aligned with GUIDE_41 `changes/`) |
| [logs/reviews/](logs/reviews/) | REVIEW_* evidence |
| [logs/tests/](logs/tests/) | TEST_* summaries ([INDEX](logs/tests/INDEX.md)) |
| [logs/feedback/](logs/feedback/) | Feedback routing ([INDEX](logs/feedback/INDEX.md)) |
| [logs/setup/](logs/setup/) | Platform build notes (e.g. RocksDB on Windows) |
| [logs/FINAL_COMPLIANCE_REPORT.md](logs/FINAL_COMPLIANCE_REPORT.md) | Compliance report snapshot |
| [logs/REVIEW_SUMMARY.md](logs/REVIEW_SUMMARY.md) | Review summary (Nov 2025) |
| [logs/STATUS.md](logs/STATUS.md) | Legacy status snapshot |

---

## Standards

Company-wide **GUIDE_*** documents stay in the monorepo `.docs/guides/`. This package publishes **REF_***, **GUIDE_01_USAGE**, and evidence under `docs/` only.

---

*Per GUIDE_00_MASTER and GUIDE_41_DOCS.*
