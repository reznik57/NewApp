# Template New App v2 — Design Spec

**Date**: 2026-07-02
**Status**: Approved design, pending implementation
**Owner**: Sven

## 1. Context & Goal

The folder `d:\Template New App` is the seed copied into every new application.
It currently contains two files: `CLAUDE.template.md` (stack-agnostic CLAUDE.md
template) and `ultrathink.template.md` (adversarial design-review protocol).

**Goal**: grow this seed into a reusable harness for building apps with Claude
Code that produces amazing long-term AI-assisted coding and clean, healthy
code. Inspired by:

- github.com/multica-ai/andrej-karpathy-skills — four behavioral principles
  (Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven
  Execution)
- gist.github.com/karpathy/442a6bf555914893e9891c11519de94f — the "LLM wiki"
  pattern: a persistent, agent-maintained knowledge base with schema, index,
  log, and ingest/query/lint operations

**Design thesis** (from the deep-analysis workflow, 5 research reports +
synthesis): the current seed's rules are 100% prose, and agents ignore prose
under context pressure. *Instructions are requests; hooks are guarantees.* The
harness therefore adds an executable enforcement layer, and a knowledge system
so hard-won lessons compound instead of evaporating in chat transcripts. The
standing meta-rule: **every rule that CAN be a hook/config/CI gate SHOULD be;
CLAUDE.md keeps only judgment calls.**

## 2. User Decisions (locked)

| Decision | Choice |
|----------|--------|
| Stack focus | Stack-agnostic base + one pre-filled TypeScript/Next.js profile |
| Delivery | Copy-folder now (version stamps + changelog); revisit Claude Code plugin after 2–3 seeded apps |
| Task runner | npm/package scripts carry the verification contract |
| Wiki scope | Per-project only |
| Auto-memory | Keep built-in memory enabled; `/log-gotcha` harvests into the committed record, which is canon |
| Plugin relationship | Defer to installed plugins (superpowers, code-review) for generic workflows; ship only project-local contract skills |
| CI | GitHub Actions template, marked delete-if-not-applicable |

## 3. Target Folder Structure

```
Template New App/
├── README.md                    # what the harness is, philosophy, map of all parts
├── SETUP.md                     # per-new-app bootstrap checklist (stays in seed)
├── TEMPLATE-CHANGELOG.md        # version history of the seed
├── docs/superpowers/specs/      # design specs for the seed itself (this file)
├── base/                        # stack-agnostic canonical seed — copy into new apps
│   ├── CLAUDE.template.md       # revised (§4)
│   ├── .claude/
│   │   ├── settings.template.json           # permissions + hook registrations (§6)
│   │   ├── hooks/
│   │   │   ├── protect_files.py             # PreToolUse guard (§6)
│   │   │   └── verify_on_stop.py            # Stop-hook verification gate (§6)
│   │   └── skills/
│   │       ├── ultrathink/SKILL.md          # converted protocol (§5)
│   │       ├── log-gotcha/SKILL.md          # incident capture + graduation (§7)
│   │       └── wiki-lint/SKILL.md           # docs health check (§7)
│   ├── docs/
│   │   ├── adr/
│   │   │   ├── README.md                    # when/how to write an ADR
│   │   │   └── 0000-template.md             # MADR-lite template
│   │   ├── wiki/
│   │   │   ├── index.md                     # categorized catalog, starts near-empty
│   │   │   └── log.md                       # append-only session/incident log
│   │   └── specs/
│   │       └── SPEC.template.md             # one-page spec + plan skeleton
│   ├── .github/workflows/ci.template.yml
│   ├── .gitignore
│   ├── .env.example
│   └── .editorconfig
└── profiles/
    └── typescript-next/         # overlay files, pre-filled for TS/Next.js
        ├── README.md            # what the profile fills, how to overlay
        ├── CLAUDE.stack-sections.md   # filled Tech Stack + Commands sections
        ├── settings.json              # filled permission allowlist
        ├── package-scripts.json       # the six npm scripts, ready to paste
        └── ci.yml                     # filled GitHub Actions workflow
```

The two existing root files move into `base/` (CLAUDE.template.md revised in
place; ultrathink.template.md is replaced by the skill and deleted from root).

**Instantiation flow**: copy `base/*` into the new repo → overlay
`profiles/<stack>/*` if applicable → work through SETUP.md → exit gate.

## 4. CLAUDE.template.md — Revision Requirements

**Keep verbatim** (rated the strongest content): Invariant "Source of Truth
(anti-rot)"; Invariant "Cite Symbols, Not Counts or Line Numbers" incl.
rationale; Gotchas problem/rule format and "Start empty. Fill it from real
incidents, not speculation."; the CI-parity line; the test-one command entry;
the why-pinned Tech Stack rationale; the header meta-instruction naming the
load-bearing principles.

**Changes**:

1. **Fix the gate contradiction**: Invariant 1 (Verification Gate) adds
   `{{TEST CMD}}` to the required checks and is reworded from "after any code
   change" to "before claiming completion or committing". Note in-file that the
   Stop hook enforces this mechanically. One definition of "done" — consumed
   identically by CLAUDE.md, the Stop hook, and CI.
2. **New invariant — test integrity**: "Never weaken, skip, delete, or `.only`
   a test to make the suite pass. A failing test is a finding, not an
   obstacle. Changing a test's assertions requires explicit user approval."
3. **New section — Everyday Task Discipline (~25 lines)**, the always-on
   Karpathy layer for every task (UltraThink covers only big ones):
   - *Surgical Changes*: every changed line must trace to the user's request;
     don't refactor, rename, or "improve" code the task didn't touch; if you
     notice adjacent problems, report them instead of fixing them unasked.
   - *Simplicity First*: no speculative abstractions, no unrequested features,
     no defensive boilerplate for conditions that can't occur; the
     senior-engineer self-check ("would a senior reviewer call this
     over-engineered?").
   - *Think Before Coding*: state assumptions; if the request has two plausible
     interpretations, ask (or state the one chosen and why).
   - *Goal-Driven Execution*: transform tasks into `[step] → verify: [check]`
     form; a step without a verify is not a step.
   - *Calibration clause*: "Bias toward caution; for trivial tasks, use
     judgment" — prevents ceremony from spilling onto typo fixes.
4. **New short standing sections** (~5 lines each):
   - *Git discipline*: atomic commits at green check only; conventional-commit
     style subject; the why in the body; never commit secrets or `.env`.
   - *Dependencies*: stdlib first → existing deps → new dep only with explicit
     approval and a stated alternative considered; lockfile always committed.
   - *Security baseline*: secrets live in env vars only (`.env` ignored,
     `.env.example` committed); parameterize all queries; never log secrets.
   - *Error handling*: fail fast; no bare catch-and-continue; errors surface to
     the user or the log, never silently swallowed.
   - *Session workflow*: at session start, skim the Gotchas section and recent
     ADR titles; at session end, propose gotcha/wiki/ADR updates for anything
     hard-won (via `/log-gotcha`).
5. **New section — Docs & Knowledge Schema** (the wiki schema lives here, not
   in a separate file):
   - Fact-placement law: **code owns WHAT; CLAUDE.md owns agent behavior plus
     facts needed every session; ADRs own DECISIONS (append-only, superseded
     not edited); wiki pages own WHY/narratives/investigations read on
     demand.**
   - Gotcha migration rule: gotchas start as one-line problem/rule entries in
     CLAUDE.md; when an entry exceeds ~3 lines it moves to a wiki page and
     leaves a one-line pointer.
   - Before changing architecture, grep `docs/adr/` for a decision on it;
     never contradict an accepted ADR without writing a superseding one.
   - Wiki conventions: `docs/wiki/index.md` is the entry point and must list
     every page; `docs/wiki/log.md` is append-only, entries are
     `## [YYYY-MM-DD] <verb> | <title>`; pages cite stable symbols, never
     counts or line numbers; delete-over-stale is the standing policy.
6. **Structural**:
   - Placeholder syntax switches from `<ANGLE>` to `{{DOUBLE-BRACE}}` (angle
     placeholders silently vanish in markdown preview/HTML contexts).
   - Every section is tagged **[Day-0]** (fill at setup) or **[Grows]**
     (starts empty, fills from real incidents) — fixes the day-0
     chicken-and-egg problem where Architecture sections can't be filled
     before code exists.
   - Version stamp comment at top: `<!-- template-version: 2026-07 -->`.
   - Stated budget in the header: ~150 lines post-fill; if it grows past that,
     migrate content to the wiki or `.claude/rules/`.
   - Footer: "These guidelines are working if: sessions start without
     re-explaining the project; agents cite ADRs when questioning decisions;
     the verification gate never has to be mentioned in chat."
7. **Update the Deep-Analysis Protocol pointer section**: it now points at the
   ultrathink *skill* (not a copied command file) and is the single home of
   the trigger list (architecture decisions, new subsystems,
   security-sensitive or performance-critical paths, irreversible data/schema
   changes); the skill references this list rather than restating it.
8. **Cut**: persona/seniority theater in Role & Context (keep the Stance line
   and never-assume note); "Batch related operations" (default tooling
   behavior now); prose style rules — replaced by "Style is enforced by
   `{{FORMATTER}}` config. Never hand-format against it. No style rules belong
   in this file."

## 5. UltraThink → `.claude/skills/ultrathink/SKILL.md`

Converted from a copy-to-commands template into a skill (on-demand loading;
commands and skills merged in current Claude Code).

**Keep**: the three stances (builds it / uses it / breaks it); the universal
red-flag list; anti-ceremony escape hatches (Phase 0 skip, minor concerns
don't stop); Options Considered with reasons; the self-updating idea.

**Changes**:

1. Frontmatter `description` written for auto-invocation: triggers on
   architecture decisions, new subsystems, security-sensitive or
   performance-critical paths, irreversible data/schema changes. **Drop
   "multi-file changes"** as a trigger — it matches nearly every task, gets
   ignored, and tolerated MUST-violations train the agent to ignore other
   MUSTs. The trigger list is stated once, in CLAUDE.md's pointer section; the
   skill references it.
2. Phase 1 reads CLAUDE.md's ⛔ Critical Invariants live ("read them now")
   instead of instructing users to mirror-copy them into the skill.
3. Phase 3 output is **saved as `docs/adr/NNNN-<slug>.md` before
   implementation begins** — the review compounds into a decision record
   instead of evaporating.
4. Devil's Advocate gains four entropy rows: unnecessary abstraction,
   defensive boilerplate, new dependency, deprecated API.
5. When a spec exists (`docs/specs/`), UltraThink reviews the spec, not a
   finished diff.
6. The CHECKPOINT becomes: "present Phase 3 via plan mode; plan approval IS
   the checkpoint."
7. Phase 6 (verification) is one pointer sentence to CLAUDE.md's Invariant 1 —
   no restated ritual.

**Cut**: Quick Reference (keep only the one-line Flow); Post-Mortem table
(reduced to one sentence); the Integration Points map (most rot-prone artifact
in the seed — it hand-mirrors the Architecture section, violating the
Source-of-Truth invariant; derive integration points fresh from the live
Architecture section per review); the Maintenance Contract shrinks to a 2-line
pointer at CLAUDE.md's Symbols-Not-Counts invariant. Synthesis table trimmed
to "one non-obvious key concern + resolution per perspective".

`ultrathink.template.md` at the seed root is deleted after conversion.

## 6. Enforcement Layer

### settings.template.json
Committed to the repo (`.claude/settings.json` after fill-in). Contents:

- **Permissions** (moderate autonomy posture):
  - allow: project build/test/lint/dev commands (filled per profile), `git status/diff/log/add/commit`, file reads within the repo
  - ask: `git push`, package installs, `gh` operations
  - deny: `Read(.env)` and `Read(.env.*)` (except `.env.example`), `rm -rf`,
    `curl`/`wget`/`Invoke-WebRequest` to arbitrary hosts
- **Hook registrations**: PreToolUse → `protect_files.py` (matcher:
  Edit|Write); Stop → `verify_on_stop.py`. Optionally PostToolUse format hook,
  added per profile where the formatter is known.

### Hook scripts — Python 3, stdlib only (Windows-safe; doc examples assume bash+jq)

- **protect_files.py** (PreToolUse): reads the tool-call JSON from stdin;
  blocks (exit 2 with reason) edits/writes targeting `.env*` (except
  `.env.example`), lockfiles (`package-lock.json`, `pnpm-lock.yaml`, etc.),
  and `.git/` internals. Configurable list at top of file.
- **verify_on_stop.py** (Stop): guards `stop_hook_active` to prevent loops;
  runs the fast gate (`npm run check` or the project's equivalent, read from a
  single config point); on failure exits 2 and emits the failure output so the
  agent must fix before stopping. Runs the fast subset only — full suite
  belongs to CI. Supports a `--self-test` flag that verifies the configured
  check command exists and the hook wiring is sound (used by SETUP.md step 4).
- Exact hook JSON schema/exit-code semantics must be verified against current
  Claude Code docs at implementation time (they have changed before).

### The six-script contract (package.json scripts)
`check` (format-check + lint + typecheck + fast tests — THE gate), `test`
(full suite), `test:one -- <pattern>`, `fix` (auto-format + lint-fix), `dev`,
`build`. One definition of "done", three consumers (CLAUDE.md, Stop hook, CI).
Non-JS projects document equivalents in CLAUDE.md's Commands section; the
contract is the six *names/semantics*, not npm itself.

### ci.template.yml (GitHub Actions)
One workflow, commented slots: format check → lint with **warnings-as-errors**
→ strict typecheck → tests → build → dependency audit. Coverage: diff-coverage
ratchet on changed lines only if desired later — never a repo-wide floor.
Marked delete-if-not-applicable for non-GitHub projects.

## 7. Knowledge System

### docs/adr/
- `0000-template.md`: MADR-lite, ~25 lines — Title, Date, Status
  (proposed/accepted/superseded-by-NNNN), Context, Options considered (with
  one-line pros/cons), Decision, Consequences.
- `README.md`: when to write one (any decision you'd have to re-derive or
  might relitigate: stack choices, data model, auth approach, build tooling,
  any UltraThink Phase 3); the append-only rule; ADR-0001 is always "stack
  choice" written at setup.

### docs/wiki/
- `index.md`: categorized catalog (Architecture / Gotchas & incidents /
  Investigations / Domain notes), one line per page. Read-before-working rule
  lives in CLAUDE.md's session workflow.
- `log.md`: append-only; `## [YYYY-MM-DD] <verb> | <title>` + 1–3 lines.
  Cheap cross-session memory, greppable.
- No other pages ship with the template — pages are created lazily from real
  incidents. Filing filter: only non-obvious, recurring, not-cheaply-
  rederivable knowledge.

### .claude/skills/log-gotcha/SKILL.md
End-of-incident capture. Steps: (1) write the lesson in problem/rule format;
(2) apply the **graduation rule** — first occurrence → wiki page (or CLAUDE.md
one-liner if ≤3 lines); recurring → CLAUDE.md one-liner; recurring AND
mechanically checkable → propose a hook/lint/CI rule and delete the prose;
(3) update `index.md` and append to `log.md`; (4) if the lesson corrects an
accepted ADR, write a superseding ADR instead.

### .claude/skills/wiki-lint/SKILL.md
Periodic docs health check (run monthly or before major work): grep every
code symbol cited in CLAUDE.md/ADRs/wiki against the codebase and list dead
references; find wiki pages missing from `index.md` and index entries with no
page; find ADRs contradicted by later ADRs without superseded-by links; find
CLAUDE.md↔wiki duplication; grep for leftover `{{PLACEHOLDER}}`/`ADAPT:`
notes. Output: a fix-list; never auto-delete — flag for the user (Karpathy:
never delete unilaterally).

### docs/specs/SPEC.template.md
One page: Problem / Desired behavior / Non-goals / Acceptance criteria / Open
questions, followed by a numbered plan skeleton where each step carries its
verification (`[step] → verify: [check]`). Threshold (stated in CLAUDE.md):
changes touching >2 modules or with irreversible consequences get a spec;
UltraThink reviews the spec.

## 8. SETUP.md — Bootstrap Checklist

Ordered checkboxes (~20), the instantiation ritual per new app:

1. Copy `base/*` (including dotfiles) into the new repo root.
2. If TS/Next: overlay `profiles/typescript-next/*` per its README.
3. Fill package.json six-script contract (or document equivalents).
4. Rename/fill `settings.template.json` → `.claude/settings.json`; confirm
   hook paths run (`python .claude/hooks/verify_on_stop.py --self-test`).
5. Fill CLAUDE.template.md → CLAUDE.md: all `{{PLACEHOLDERS}}`, act on every
   `ADAPT:` note, delete unused sections, keep [Grows] sections empty.
6. Write `docs/adr/0001-stack-choice.md`.
7. Fill or delete `ci.template.yml` → `.github/workflows/ci.yml`.
8. Create `.env` from `.env.example`; verify `.env` is git-ignored.
9. First commit must pass `npm run check`.
10. **Exit gate**: `grep -rn "{{" CLAUDE.md .claude/ docs/` and
    `grep -rn "ADAPT:" CLAUDE.md .claude/ docs/` return nothing. (SETUP.md
    itself is never copied — it lives only in the seed; if the whole seed
    folder was copied wholesale, delete SETUP.md, README.md and
    TEMPLATE-CHANGELOG.md from the new repo now.)

## 9. README.md (seed root)

Explains: the philosophy (enforcement over prose; knowledge compounds;
YAGNI applies to the harness itself), a map of every file and its job, the
instantiation flow, the relationship to installed plugins (defer to
superpowers/code-review for generic workflows), and the upgrade story
(version stamps + TEMPLATE-CHANGELOG.md; diff a seeded app's stamp against
the changelog to see what it's missing).

## 10. TypeScript/Next.js Profile

Pre-filled overlays (exact versions/tools chosen at implementation time
against current stable): `CLAUDE.stack-sections.md` (Tech Stack table +
Commands for Next.js/TypeScript/Vitest/ESLint/Prettier or Biome),
`package-scripts.json` (six scripts filled), `settings.json` (allowlist for
npm/npx/next/vitest/eslint/tsc), `ci.yml` (Node setup, cache, the six-script
gate). Profile README explains the overlay step and what remains manual
(domain invariant, architecture sections).

## 11. Risks & Mitigations (accepted)

- **Template bloat / dead markdown** → core list deliberately small; SETUP.md
  step "delete what you won't use"; harness applies its own Simplicity rules.
- **Doc rot** → symbols-not-counts makes staleness greppable; `/wiki-lint`;
  append-only ADRs; delete-over-stale policy.
- **Prose rules ignored** → three-layer enforcement ladder (Stop hook →
  settings/permissions → CI); meta-rule that checkable rules become checks.
- **Over-process for a solo dev** → risk-based thresholds everywhere;
  calibration clause; escape hatches preserved.
- **Propagation drift across seeded apps** → version stamps + changelog now;
  plugin packaging revisited after 2–3 apps.
- **CLAUDE.md length ratchet** → ~150-line budget; gotcha migration rule;
  `.claude/rules/` as future pressure valve.
- **Dual memory stores** → committed record is canon; `/log-gotcha` harvests
  auto-memory.

## 12. Non-Goals / Deferred

- No adversarial-reviewer subagent (built-in /code-review + plugins suffice
  for now).
- No auto-setup skill that interviews and fills placeholders (build after the
  templates stabilize across 2–3 apps; SETUP.md must exist manually first).
- No `.claude/rules/` content, no Renovate config, no standalone
  DEPENDENCIES.md (the 6-line CLAUDE.md rule carries the policy).
- No plugin packaging yet.
- No global cross-project wiki.
- No heavyweight spec machinery (Spec Kit/Kiro-style) — two markdown pages
  capture ~90% of the value at ~5% of the ceremony.

## 13. Acceptance Criteria

1. Folder structure matches §3 exactly; the two legacy root templates are
   relocated/replaced as specified.
2. CLAUDE.template.md implements every change in §4; a fresh read finds no
   contradiction between the Verification Gate, the Stop hook description,
   and the skill's Phase 6.
3. All skills have valid frontmatter and load in Claude Code (verified via
   skill invocation in a scratch project).
4. Both hooks are Python-stdlib-only, run on Windows, and `verify_on_stop.py`
   self-test passes; hook JSON schema verified against current docs.
5. Instantiating a scratch app by following SETUP.md end-to-end (with the TS
   profile) reaches the exit gate with zero leftover placeholders/ADAPT
   notes, and `npm run check` passes on the first commit.
6. Every template file carries a `template-version` stamp;
   TEMPLATE-CHANGELOG.md has its first entry.
7. No fact appears in two places across CLAUDE.template.md, the skills, and
   the docs templates (spot-check: verification gate, trigger list, wiki
   schema each stated exactly once with pointers elsewhere).
