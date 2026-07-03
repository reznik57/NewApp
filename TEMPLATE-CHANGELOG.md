# Template Changelog

Seeded apps carry a `template-version` stamp in each copied file. Diff an
app's stamp against this log to see what it is missing. JSON templates
(settings.template.json, profile settings.json, package-scripts.json) cannot
carry comment stamps — their version is tracked only here.

## 2026-07.4 — v2.3

Hardening round: three prose rules become mechanisms (touched templates
stamped 2026-07.4):

- The harness protects itself: protect_files.py blocks agent edits to
  `.claude/hooks/`, `.claude/scripts/`, and `.claude/settings*.json` —
  a Stop-hook-blocked agent could previously just edit the gate away.
  Skills stay agent-editable by design; SETUP's step order (CHECK_COMMAND
  in step 4, settings activation in step 5) is unaffected.
- Exit gate has one home: new `.claude/scripts/check_markers.py` (stdlib,
  tested) holds the scanned paths and exemptions; SETUP step 12 and
  wiki-lint step 5 just run it. Replaces four hand-maintained grep
  encodings that had already drifted once. wiki-lint no longer needs a
  marker exemption at all.
- TS/Next profile, eslint.config.mjs: `.only`/`.skip` on it/test/describe
  are errors (Invariant 2 mechanized; approved exceptions carry an
  eslint-disable comment as the visible approval trail) and
  `@ts-ignore`/undescribed suppressions are errors via ban-ts-comment
  (Invariant 1) — live-verified against eslint-config-next@16.
- Hook test suite: 30 passed, 1 skipped (10 new tests).

## 2026-07.3 — v2.2.1

Whole-seed audit round (4 lenses over all live files, 45 raw findings, 12
objective defects fixed; touched templates stamped 2026-07.3):

- Setup path unbroken: SETUP step 1 now says to run a scaffolder FIRST
  (create-next-app refuses non-empty dirs); profile README documents that
  a first test must exist (`vitest run` exits 1 with zero test files, so
  `check`/Stop hook/CI cannot go green without one — and `--passWithNoTests`
  must NOT be added).
- protect_files.py: blocks `bun.lock` (Bun ≥1.2 default) and
  `npm-shrinkwrap.json`; blocks a file NAMED `.git` (worktree/submodule
  gitdir pointer); tests added. Both hooks now carry template-version
  stamps.
- Exit gate tightened: the stale log-gotcha exemption removed from SETUP
  step 12 (both variants) and wiki-lint step 5 — the file has nothing to
  exempt.
- settings (base + profile): `Read(.env.staging.local)` added to the deny
  enumeration (the one missing `.local` twin).
- Invariant-3 cleanups: ultrathink's dependency bullets are now bare
  pointers to Standing Rules (they had drifted to a nonexistent "license
  check"); its body no longer restates the description's skip list;
  CLAUDE.template.md loses four same-file duplicates (gotcha-migration
  bullet, wiki filing filter, symbols-not-counts restatement, Git-bullet
  secrets sentence); log-gotcha step 1 and SPEC.template.md intro become
  pointers; wiki index.md drops a restated convention.

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
- CLAUDE.template.md post-fill budget raised ~150 → ~160 (absorbs the
  three new Task Discipline bullets).
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
