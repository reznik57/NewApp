# Template Changelog

Seed version history (upgrade procedure: README → Upgrading seeded apps).
JSON templates (settings.template.json, profile settings.json,
package-scripts.json) cannot carry comment stamps — their version is
tracked only here.

## 2026-07.6 — v2.4

Universality round: brownfield path, portability documented, audit
fixes (touched templates stamped 2026-07.6):

- ADOPTION.md: the existing-app checklist — inventory collisions, merge
  instead of overwrite, define `check` on the CURRENT state (narrow
  scope, never weaken rules; freeze a lint baseline and ratchet), and
  the load-bearing inversion: green `check` BEFORE the Stop hook goes
  live. Architecture [Grows] is filled at adoption (the code already
  has seams); ADR-0001 recorded retroactively. Size variants (S/M/L)
  deliberately rejected: [Grows] sections, threshold triggers, and
  delete-what-you-won't-use already scale the harness by use, and every
  variant is a drift vector (the v2.2.1 settings drift is the
  empirical case).
- README: Portability section — three layers (tool-agnostic /
  concept-portable / Claude-Code-bound). Antigravity 2.0 reads
  AGENTS.md + .agents/skills/; Gemini CLI hooks share the
  exit-2-blocks semantics under renamed events (BeforeTool/AfterAgent);
  Claude Code does not read AGENTS.md natively (mid-2026), so the
  AGENTS.md-plus-CLAUDE.md-shim pattern is named but not built (YAGNI).
  Models are not the axis: hooks/settings/skills are model-independent
  within Claude Code.
- base/.gitignore: restores the scaffold patterns lost by replacement
  (*.pem, *.tsbuildinfo, next-env.d.ts, .vercel/) and adds
  __pycache__/ (the harness ships Python hooks); SETUP step 1's
  robocopy now excludes __pycache__ (seed-test bytecode was copied
  into new apps).
- check_markers.py: ADAPT note for stacks whose template syntax is {{
  (Handlebars/Jinja/Angular/Vue/Liquid) — otherwise docs code samples
  turn wiki-lint step 5 permanently red.
- settings (base + profile): deny gains the PowerShell recursive-delete
  form (Remove-Item -Recurse) — symmetric with the PS network denies;
  parameter-order variants still slip prefix matching (accident guard,
  not a boundary).
- One-home and rot cleanups: SETUP step 5 defers the leftover-template
  deletion to profile README step 2; profile ci.yml documents why the
  full-suite step duplicates check's vitest run until check narrows;
  the v2 design spec's status was stale ("pending implementation" →
  implemented, historical record).
- Seed test suite: settings parity guard — deny lists and hook
  registrations must be identical between base and profile; the
  allow/ask delta must be exactly the documented npx quartet. The
  v2.2.1 drift class, mechanized (4 new tests; suite: 45, 1 skipped).

## 2026-07.5 — v2.3.1

Remaining audit polish (medium/small priorities; touched templates
stamped 2026-07.5):

- verify_on_stop.py --self-test now verifies the whole CHECK_COMMAND:
  segments are split on shell operators outside quotes, each segment's
  leading tool must resolve (quoted paths with spaces unwrapped, shell
  builtins skipped, npm-run segments checked against package.json), so
  a typo'd binary fails at setup instead of blocking every session
  stop. Six new tests.
- CLAUDE.template.md slimmed toward its ~160 post-fill budget: success
  footer moved into SETUP step 7 (now the single home of the fill
  procedure — the template header is a pointer), purpose line and two
  emphasis restatements dropped, Task-Discipline intro compressed. The
  "Don't refactor/rename/reformat" enumeration stays — it counters a
  known agent bias.
- wiki-lint gains a budget check (CLAUDE.md over ~160 lines → propose
  wiki migration) so the growth cap has a home inside seeded apps.
- Changelog header defers the upgrade procedure to README (one home);
  SETUP step 4's non-npm tail points at the Commands ADAPT note instead
  of restating it; ultrathink Phase 6 loses a meta-sentence.

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
