# Template Changelog

Seeded apps carry a `template-version` stamp in each copied file. Diff an
app's stamp against this log to see what it is missing. JSON templates
(settings.template.json, profile settings.json, package-scripts.json) cannot
carry comment stamps — their version is tracked only here.

## 2026-07.2 — v2.2

Deltas from mapping Google's "The New SDLC with Vibe Coding" whitepaper
(May 2026) against the seed. Three small additions; the paper otherwise
independently converges with the seed's design (hooks as guarantees,
static-context budget, skills as progressive disclosure). Touched
template files carry the stamp 2026-07.2 (README is an unstamped
seed-root doc).

- CLAUDE.template.md: Invariant-5 ADAPT example for LLM/agent features
  (no prompt or model change ships without its eval set — tests verify
  the deterministic parts, evals the rest); "LLM-powered features" joins
  the Deep-Analysis triggers (mirrored in ultrathink's description, the
  one allowed restatement); Architecture ADAPT note asks for one
  canonical example file per recurring pattern.
- README: "When not to use this seed" — spikes don't get a harness, and
  a spike never graduates to production by accident.

## 2026-07.1 — v2.1

Gap-analysis round against an external "enterprise guardrails" prompt
(30 candidate gaps adversarially verified; 14 adopted, 16 rejected as
bloat or duplication of plugins/ultrathink). Touched files carry the
stamp 2026-07.1.

- CLAUDE.template.md: three new Everyday Task Discipline bullets (Reuse
  first; Verify, don't invent; User first); Security rule now covers PII;
  Dependencies rule adds a maintenance check; Invariant-5 ADAPT example
  for reversible DB migrations; session workflow includes deferred debt.
- Debt capture: log-gotcha gains a deferred-debt branch; docs/wiki/log.md
  gains the `deferred` verb. Replaces an external TECHNICAL_DEBT.md-style
  register — same function, existing append-only home.
- ultrathink: Phase-1 red flag for endpoints/routes/actions changed
  without an explicit authn/authz decision; Devil's Advocate row for
  idempotency under retries/replays/double-fires.
- SPEC.template.md: Rollback section (git revert alone, or explicit
  data/schema backout steps).
- TS/Next profile: eslint.config.mjs added — jsx-a11y recommended
  (accessibility) + no-warning-comments (stale-marker comments), both
  enforced by the `check` gate (mechanism documented in the file header);
  new Stack Rules section in CLAUDE.stack-sections.md (UI four-state
  matrix, server-side validation); README gains the copy step (now 1–5).

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
- Verified live (2026-07-02, headless Claude Code session against a seeded
  scratch app): all three skills load; hook enforcement initially FAILED
  SILENTLY on Windows (`python` resolved to the Microsoft Store alias stub,
  exit 49 — any non-0/2 hook exit is non-blocking). Hook commands now probe
  python3/python/py by execution and fail closed if none works; re-probe
  confirmed both protected operations blocked. Also learned: Claude Code
  ignores project settings until the workspace trust dialog is accepted
  (noted in SETUP step 5).

## (pre-2026-07) — v1

- Two files: CLAUDE.template.md, ultrathink.template.md. Advisory-only.
