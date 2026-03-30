<!-- xwformats/docs/README.md -->

# xwformats documentation

**Library:** exonware-xwformats  
**Layout:** Per [GUIDE_41_DOCS](../../.docs/guides/GUIDE_41_DOCS.md) (monorepo): Markdown lives under `docs/` except the root `README.md`.

## Start here

| Go to | For |
|-------|-----|
| [INDEX.md](INDEX.md) | Full doc map and folder layout |
| [GUIDE_01_USAGE.md](GUIDE_01_USAGE.md) | Install and use the library |
| [REF_22_PROJECT.md](REF_22_PROJECT.md) | Vision, requirements, project status |
| [REF_15_API.md](REF_15_API.md) | Public API reference |

## Folder map

```
docs/
├── INDEX.md              ← navigation hub
├── README.md             ← this file
├── GUIDE_01_USAGE.md
├── REF_*.md              ← requirements, arch, API, tests, review…
├── changes/              ← short pointers to historical notes under _archive/
├── _archive/             ← full historical narratives (fixes, known issues)
└── logs/                 ← evidence: tests, reviews, setup notes, compliance
    ├── tests/            ← TEST_* summaries (canonical per GUIDE_41)
    ├── reviews/
    └── setup/
```

`docs/tests/` only hosts a [README redirect](tests/README.md); new run summaries go under `docs/logs/tests/`.

## Production readers

- **Operators:** [REF_22_PROJECT.md](REF_22_PROJECT.md), [REF_51_TEST.md](REF_51_TEST.md), [REF_35_REVIEW.md](REF_35_REVIEW.md).
- **Platform limits:** [_archive/KNOWN_ISSUES.md](_archive/KNOWN_ISSUES.md), [logs/setup/](logs/setup/).
- **Older compliance narratives:** [_archive/](_archive/), [logs/FINAL_COMPLIANCE_REPORT.md](logs/FINAL_COMPLIANCE_REPORT.md).

---

Company-wide guides (GUIDE_31_DEV, GUIDE_41_DOCS, …) live in the monorepo `.docs/guides/`, not inside this package.
