# Contributing to xwformats

**Repository:** [exonware/xwformats](https://github.com/exonware/xwformats)  
**Standards:** Monorepo `.docs/guides/` (`GUIDE_31_DEV`, `GUIDE_51_TEST`, `GUIDE_41_DOCS`)

---

## Quick setup

```bash
git clone https://github.com/exonware/xwformats.git
cd xwformats
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e ".[dev]"
# Optional: all format deps (see platform notes for Windows / native wheels)
pip install -e ".[full]"
```

Run tests:

```bash
python tests/runner.py
```

---

## Pull requests

- One logical change per PR when possible.  
- Link related **FR**/milestones in `docs/REF_22_PROJECT.md` if applicable.  
- Ensure tests pass and docs/REF snippets stay accurate.  
- Follow **Five Priorities** (`GUIDE_00_MASTER`): Security → Usability → Maintainability → Performance → Extensibility.

---

## Code and docs

- Python: `GUIDE_32_DEV_PY` (facades, contracts, lazy modes).  
- Comments explain **why**, not what (`GUIDE_31_DEV`).  
- Markdown lives under **`docs/`** except root `README.md` (`GUIDE_41_DOCS`).

---

*Questions: open a discussion or email connect@exonware.com.*
