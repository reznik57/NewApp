# Template Changelog

Seeded apps carry a `template-version` stamp in each copied file. Diff an
app's stamp against this log to see what it is missing. JSON templates
(settings.template.json, profile settings.json, package-scripts.json) cannot
carry comment stamps — their version is tracked only here.

## 2026-07 — v2

- Enforcement layer: `.claude/settings.template.json`, `protect_files.py`,
  `verify_on_stop.py`, six-script contract (check/test/test:one/fix/dev/build),
  CI template with warnings-as-errors.
- Knowledge system: `docs/adr/` (MADR-lite), `docs/wiki/` (index + log,
  lazily grown), `log-gotcha` and `wiki-lint` skills.
- CLAUDE.template.md revised: test-integrity invariant, Everyday Task
  Discipline (Karpathy layer), standing rules, Docs & Knowledge Schema,
  {{PLACEHOLDER}} syntax, Day-0/Grows tags, ~150-line post-fill budget.
- ultrathink converted from a copy-in command template to a skill; Phase 3
  output now saved as an ADR.
- TypeScript/Next.js profile added.

## (pre-2026-07) — v1

- Two files: CLAUDE.template.md, ultrathink.template.md. Advisory-only.
