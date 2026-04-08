# Security policy — xwformats

**Project:** exonware-xwformats  
**Contact:** connect@exonware.com

---

## Supported versions

Security fixes are applied to the **latest release line** on PyPI unless otherwise announced. See `src/exonware/xwformats/version.py` and release notes.

---

## Reporting a vulnerability

Please **do not** open a public GitHub issue for undisclosed security problems.

1. Email **connect@exonware.com** with subject line `[SECURITY] xwformats`.  
2. Include: description, affected version(s), reproduction steps (if safe), and impact assessment.  
3. Allow a reasonable window for investigation and patch before public disclosure.

We aim to acknowledge receipt within **72 hours** and coordinate next steps.

---

## Security expectations

- Serialization formats can execute **data-dependent** native code; only use **trusted inputs** or validate before decode.  
- Follow `REF_22_PROJECT.md` and `GUIDE_31_DEV` (Five Priorities: **Security first**).  

---

*Aligned with `GUIDE_64_SECURITY` and `GUIDE_41_DOCS`.*
