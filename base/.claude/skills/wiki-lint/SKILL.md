---
name: wiki-lint
description: Docs health check for CLAUDE.md, ADRs, and the wiki. Finds dead symbol references, orphan or unindexed pages, contradicted decisions without superseded-by links, duplicated facts, and leftover placeholders. Run monthly or before major work.
---

<!-- template-version: 2026-07 -->

# /wiki-lint — docs health check

Produce a fix-list. NEVER auto-delete or auto-edit — flag findings for the
user (docs may encode intent the code lost).

1. **Dead references**: extract every code symbol cited in `CLAUDE.md`,
   `docs/adr/*.md`, and `docs/wiki/*.md` (backticked identifiers, paths,
   command names). Grep each against the codebase. Report symbols that no
   longer exist.
2. **Index integrity**: every file in `docs/wiki/` listed in `index.md`?
   Every index entry pointing at an existing file?
3. **ADR integrity**: any accepted ADR contradicted by a later one without a
   superseded-by link? Any `proposed` ADR older than ~30 days?
4. **Duplication drift**: any fact stated in both CLAUDE.md and a wiki/ADR
   page? Propose which single home keeps it (fact-placement law in
   CLAUDE.md → Docs & Knowledge Schema).
5. **Leftovers**: grep `CLAUDE.md`, `.claude/`, `docs/`, `.github/` for
   `{{` and `ADAPT:` — both must return nothing, excluding the reusable
   templates (`docs/adr/0000-template.md`, `docs/specs/SPEC.template.md`)
   and the files that legitimately keep ADAPT: markers or quote this syntax
   (`.claude/hooks/protect_files.py`, `.claude/hooks/verify_on_stop.py`,
   this file, `.claude/skills/log-gotcha/SKILL.md`).
6. **Report**: a fix-list grouped by file — finding + suggested action.
