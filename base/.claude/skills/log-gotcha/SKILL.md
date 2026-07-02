---
name: log-gotcha
description: Capture a hard-won lesson at the end of an incident, bug hunt, or debugging session. Files it in the right knowledge home (CLAUDE.md gotcha one-liner, wiki page, or a proposed hook/lint rule) and updates the wiki index and log.
---

<!-- template-version: 2026-07 -->

# /log-gotcha — incident capture

Filing filter first: only file what is **non-obvious, likely to recur, and
expensive to re-derive**. If it fails the filter, stop here — noise in the
knowledge base is rot.

1. **Write the lesson** in problem/rule form:
   `Problem: {{what goes wrong, concretely}} → Rule: {{the pattern that
   avoids it, naming the symbol involved}}`
2. **Choose the home** (graduation rule):
   - First occurrence, fits in ≤3 lines → one-liner in CLAUDE.md → Project
     Gotchas.
   - First occurrence, needs narrative → page in `docs/wiki/` plus a one-line
     pointer in Project Gotchas.
   - Recurring (second+ occurrence — check `docs/wiki/log.md`) → make sure
     the CLAUDE.md one-liner exists and is sharp.
   - Recurring AND mechanically checkable → propose a hook, lint rule, or CI
     gate to the user; once adopted, DELETE the prose rule it replaces.
3. **Update the registers**: add any new page to `docs/wiki/index.md`; append
   a `learned` entry to `docs/wiki/log.md` (format: CLAUDE.md → Docs &
   Knowledge Schema).
4. **Check for contradiction**: if the lesson invalidates an accepted ADR,
   write a superseding ADR (`docs/adr/README.md`) instead of editing anything.
5. **Harvest auto-memory**: if session memory holds related observations,
   fold them in — the committed repo is canon; memory is per-machine scratch.
