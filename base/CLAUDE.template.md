<!-- template-version: 2026-07.27 -->
<!--
  CLAUDE.md TEMPLATE — fill per SETUP.md step 7 (the fill checklist and
  the post-fill line budget live there; this comment block is deleted).
  Load-bearing principles: Invariants 3 and 4 (Source of Truth,
  Symbols-Not-Counts). Keep them even if you cut everything else.
-->

# CLAUDE.md

**These instructions override default behavior — follow them exactly.**

## Role & Context [Day-0]

{{ONE-LINE DESCRIPTION OF THE PROJECT}}

- **Domain**: {{e.g. fintech ledger / realtime chat / data pipeline}}
- **Stance**: Be concise. Give brutal, honest engineering feedback — reject
  bad patterns and explain why; don't optimize for politeness.
- **Never assume**: {{THE ONE THING AGENTS MUST ALWAYS ASK ABOUT — or delete}}

## ⛔ Critical Invariants (NEVER VIOLATE)

Breaking one invalidates the task.

### 1. Verification Gate

- Run `{{CHECK CMD — e.g. npm run check}}` (format + lint + typecheck + fast
  tests) **before claiming completion or committing**. It must exit clean:
  **0 errors, 0 warnings**. Under Claude Code the Stop hook
  (`.claude/hooks/verify_on_stop.py`) enforces this mechanically; where no
  hook fires (e.g. Cowork/claude.ai) it stands as an instruction, with CI as
  the backstop. Don't argue with a red gate — fix the failure.
- **NEVER** suppress a warning without explicit user approval.
- A clean local check does not equal a clean CI run — CI runs the full suite
  and strict build. Verify the way CI does ({{CI-EQUIVALENT CMD}}) before
  claiming "done" on release-bound work.

### 2. Test Integrity

- **NEVER** weaken, skip, delete, or `.only` a test to make the suite pass.
  A failing test is a finding, not an obstacle.
- Changing a test's assertions requires explicit user approval.

### 3. Source of Truth (anti-rot)

- **One fact lives in one place.** Link to it; never duplicate it.
- **Never document deleted or merely-planned code as if it exists.** Remove a
  section the moment the thing it describes is removed.

### 4. Cite Symbols, Not Counts or Line Numbers

- Reference **stable symbol names** (a class, function, constant, directory) —
  things a rename would break loudly.
- **Do NOT embed volatile statistics in prose** (file counts, "N modules",
  LOC totals) or `path/file:120` line references. They rot within weeks and
  mislead the next agent. Point at the source of truth instead ("the handlers
  in `src/api/`", "the `MAX_*` constant in `config.rs`").

### 5. {{PROJECT-SPECIFIC INVARIANT}}

<!-- ADAPT: the rules unique to YOUR domain that an agent could plausibly
violate. Examples:
  - Security/CLI: never pass unsanitized input to a shell/subprocess.
  - Data/streaming: never buffer the full dataset in memory; stream it.
  - Data/DB: schema changes ship only as reversible migrations; never mutate
    schema or data in place.
  - LLM/agent features: no prompt or model change ships without its eval
    set passing — tests verify the deterministic parts, evals the rest.
  - Money/ledger: never use floats for currency; never mutate a posted entry.
  - Frontend: never block the UI thread; keep render paths allocation-light.
You almost certainly have at least one. -->

## Everyday Task Discipline

Applies to EVERY task; high-risk work additionally gets the Deep-Analysis
Protocol below.

- **Surgical changes**: every changed line must trace to the user's request.
  Don't refactor, rename, reformat, or "improve" code the task didn't touch.
  Notice an adjacent problem? Report it; don't fix it unasked.
- **Simplicity first**: no speculative abstractions, no unrequested features,
  no defensive boilerplate for conditions that can't occur. Self-check before
  finishing: "would a senior reviewer call this over-engineered?"
- **Reuse first**: before creating a component, util, or helper, search the
  codebase for an existing one — extend it, or state why it doesn't fit.
- **Think before coding**: state your assumptions. If the request has two
  plausible readings, ask — or state the reading you chose and why.
- **Verify, don't invent**: never reference an env var, config key, route,
  schema field, or third-party capability you haven't confirmed exists —
  inspect first; if you can't verify, say so and ask.
- **Goal-driven execution**: restate the task as steps of the form
  `[step] → verify: [check]`. A step without a verify is not a step.
- **User first**: never trade user-facing quality for implementation
  convenience; between technically equivalent options, pick the better
  user experience.
- **Calibration**: bias toward caution; for trivial tasks, use judgment.

## Tech Stack [Day-0]

| Component     | Version | Why this / why pinned              |
| ------------- | ------- | ---------------------------------- |
| {{LANGUAGE}}  | {{VER}} | {{constraint, or "latest stable"}} |
| {{FRAMEWORK}} | {{VER}} | {{version-pin reason, if any}}     |
| {{KEY LIB}}   | {{VER}} | {{why this one}}                   |

<!-- ADAPT: list only versions that constrain decisions. Record WHY a version
is pinned — that reasoning stops a future agent from "helpfully" upgrading. -->

## Commands [Day-0]

The six-script contract lives in `package.json` (single source of truth):
`check` (THE gate), `test`, `test:one`, `fix`, `dev`, `build`.
<!-- ADAPT (non-JS stacks): replace with a table mapping the six contract
names to your real commands, e.g. check = `cargo clippy -- -D warnings;
cargo test --lib`. The six semantics stay; the tool changes. Update
CHECK_COMMAND in .claude/hooks/verify_on_stop.py to match. Stack with two
strictness tiers (Debug/Release builds, dev/prod lint)? `check` is the
fast lenient tier, `build` the strict one CI runs — mapping both to the
same command makes the gate too slow or CI too lax. -->

## Architecture [Grows]

### Layout

{{TOP-LEVEL DIRECTORY MAP — one line per major dir, what lives there}}

### Data / Control Flow

{{HOW A REQUEST OR INPUT MOVES THROUGH THE SYSTEM, END TO END}}

### Key Components

- **{{ComponentName}}** (`{{path}}`): {{responsibility, one line}}

<!-- ADAPT: fill as the code grows. Describe the seams an agent must respect
(layer boundaries, the one service that owns X). Name symbols, never counts.
Non-obvious patterns belong here; obvious things don't. Name one canonical
example file per recurring pattern — agents copy patterns better than they
follow prose. -->

## Project Gotchas [Grows]

<!-- Start empty. Fill from real incidents, not speculation — via /log-gotcha.
One-liners only; narratives longer than ~3 lines live in docs/wiki/ with a
pointer here. Format:

### <Short title of the trap>
**Problem**: <what goes wrong, concretely> → **Rule**: <the pattern that
avoids it, with the symbol name involved>
-->

## Standing Rules

- **Git**: atomic commits, only at a green `check`. Conventional-commit
  subject; the _why_ in the body. Stage explicit paths — never
  `git add -A` / `git add .` — and never discard state you didn't create
  (`git reset --hard`, `git clean`): a parallel session's work may share
  the worktree.
- **Dependencies**: stdlib first → existing deps → a NEW dependency needs
  explicit approval plus a stated alternative you considered and a
  maintenance check (recent releases, active upstream). Lockfile always
  committed.
- **Security**: secrets live in env vars only (`.env` ignored,
  `.env.example` committed). Parameterize all queries. Never log secrets
  or personal data (PII).
- **Errors**: fail fast. No bare catch-and-continue; errors surface to the
  user or the log, never silently vanish.
- **Style**: enforced by `{{FORMATTER}}` config. Never hand-format against
  it. No style rules belong in this file.
- **Session workflow**: at start, skim Project Gotchas and recent titles in
  `docs/adr/`. At end, run `/log-gotcha` for anything hard-won or
  deliberately deferred this session.

## Docs & Knowledge Schema

**Fact-placement law** — one fact, one home:

| Kind of fact                                        | Home                                             |
| --------------------------------------------------- | ------------------------------------------------ |
| What the code does                                  | The code (+ Architecture section for the seams)  |
| Agent behavior + facts needed every session         | This file                                        |
| Decisions and their why                             | `docs/adr/` (append-only; supersede, never edit) |
| Narratives: incidents, investigations, domain notes | `docs/wiki/`                                     |

- **ADR discipline**: before changing architecture, grep `docs/adr/` titles.
  Never contradict an accepted ADR without writing a superseding one.
- **Wiki conventions**: `docs/wiki/index.md` lists every page — read the
  relevant section before working in an unfamiliar area. `docs/wiki/log.md`
  is append-only: `## [YYYY-MM-DD] <verb> | <title>` plus 1–3 lines. Stale
  content is deleted, not kept "just in case".

## Deep-Analysis Protocol

For complex or high-risk changes, run the **ultrathink** skill BEFORE writing
code. Triggers (sole home — restated only in the ultrathink skill's auto-invocation description): architecture decisions, new
subsystems, security-sensitive or performance-critical paths, LLM-powered
features, irreversible data/schema changes. Changes touching more than
2 modules or with irreversible consequences also get a one-page spec
first (copy `docs/specs/SPEC.template.md`); ultrathink then reviews the
spec.
