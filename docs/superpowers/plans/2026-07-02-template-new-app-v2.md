# Template New App v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the seed folder `d:\Template New App` into the v2 harness specified in `docs/superpowers/specs/2026-07-02-template-new-app-v2-design.md`: enforcement layer (settings + 2 Python hooks + six-script contract + CI), knowledge system (ADRs + wiki + 2 skills), revised CLAUDE.md template, UltraThink as a skill, and a TypeScript/Next.js profile.

**Architecture:** Everything under `base/` is the stack-agnostic seed copied into new apps; `profiles/typescript-next/` overlays pre-filled stack files; seed-root files (README, SETUP, CHANGELOG, docs/superpowers/, tests/) never leave the seed. Enforcement is layered: Stop hook → settings permissions → CI. Knowledge follows the fact-placement law: CLAUDE.md = behavior + every-session facts, ADRs = decisions, wiki = narratives, code = what.

**Tech Stack:** Markdown templates, Python 3.9+ (stdlib only, Windows-safe) for hooks, JSON for settings, GitHub Actions YAML, npm scripts as the verification contract.

## Global Constraints

- Spec is the authority: `docs/superpowers/specs/2026-07-02-template-new-app-v2-design.md`. Every task below implements a spec section named in the task.
- Placeholder syntax is `{{DOUBLE-BRACE}}` everywhere. Tailoring notes use the exact token `ADAPT:` (inside HTML comments in markdown). No `<ANGLE>` placeholders may survive.
- Every markdown/YAML template file starts with a version stamp: `<!-- template-version: 2026-07 -->` (markdown) or `# template-version: 2026-07` (YAML). JSON files cannot carry comments — they are stamped via TEMPLATE-CHANGELOG.md instead (accepted deviation from spec acceptance criterion 6, recorded in the changelog entry).
- Python hooks: stdlib only, no syntax requiring Python 3.10+ (no `X | None` annotations), must run on Windows.
- Single source of truth across all authored files: the verification gate is defined ONLY in CLAUDE.template.md Invariant 1; the UltraThink trigger list ONLY in CLAUDE.template.md → Deep-Analysis Protocol; wiki conventions ONLY in CLAUDE.template.md → Docs & Knowledge Schema. Skills and docs POINT at these; they never restate them.
- The six-script contract names are exactly: `check`, `test`, `test:one`, `fix`, `dev`, `build`.
- Shell is Windows PowerShell 5.1: never use `&&` to chain; use `;` or separate commands.
- Commit at the end of every task. Conventional-commit subject, body explains why. Every commit message ends with the line: `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>` (use a here-string `@'...'@` for multi-line messages in PowerShell).
- Working directory for all commands: `d:\Template New App`.

---

### Task 1: Restructure seed + scaffolding files

**Files:**
- Move: `CLAUDE.template.md` → `base/CLAUDE.template.md` (revised in Task 2)
- Create: `base/.gitignore`, `base/.env.example`, `base/.editorconfig`, `TEMPLATE-CHANGELOG.md`
- Create (empty dirs via files in later tasks): `base/.claude/hooks/`, `base/.claude/skills/`, `base/docs/adr/`, `base/docs/wiki/`, `base/docs/specs/`, `base/.github/workflows/`, `profiles/typescript-next/`, `tests/hooks/`

**Interfaces:**
- Produces: the directory layout every later task writes into (spec §3). `ultrathink.template.md` stays at root until Task 3 deletes it after conversion.

- [ ] **Step 1: Move the CLAUDE template into base/**

```powershell
New-Item -ItemType Directory -Force base | Out-Null
git mv "CLAUDE.template.md" "base/CLAUDE.template.md"
```

- [ ] **Step 2: Create base/.gitignore**

Create `base/.gitignore` with exactly:

```
# Dependencies
node_modules/

# Env & secrets — .env.example IS committed
.env
.env.*
!.env.example

# Build output
dist/
build/
.next/
out/

# Logs & caches
*.log
.cache/
coverage/

# OS noise
.DS_Store
Thumbs.db
```

- [ ] **Step 3: Create base/.env.example**

Create `base/.env.example` with exactly:

```
# Every variable the app needs, with safe placeholder values.
# Copy to .env and fill locally. NEVER commit .env (see .gitignore).
# EXAMPLE_API_KEY=your-key-here
```

- [ ] **Step 4: Create base/.editorconfig**

Create `base/.editorconfig` with exactly:

```
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
indent_style = space
indent_size = 2
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false
```

- [ ] **Step 5: Create TEMPLATE-CHANGELOG.md**

Create `TEMPLATE-CHANGELOG.md` (seed root) with exactly:

```markdown
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
```

- [ ] **Step 6: Verify layout and commit**

```powershell
git status --short
```
Expected: rename `CLAUDE.template.md -> base/CLAUDE.template.md`, plus 4 new files.

```powershell
git add -A
git commit -m @'
chore: restructure seed into base/ + scaffolding dotfiles and changelog

Implements spec section 3 layout. base/ is what gets copied into new apps;
seed-root files stay in the seed.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
'@
```

---

### Task 2: Revise base/CLAUDE.template.md (spec §4)

**Files:**
- Rewrite: `base/CLAUDE.template.md` (full replacement — content below)

**Interfaces:**
- Produces: section names other files point at (exact headings): `⛔ Critical Invariants (NEVER VIOLATE)`, `Everyday Task Discipline`, `Project Gotchas`, `Standing Rules`, `Docs & Knowledge Schema`, `Deep-Analysis Protocol`. The check command placeholder is `{{CHECK CMD — e.g. npm run check}}`. Tasks 3, 7, 8 reference these headings verbatim.

- [ ] **Step 1: Replace the file content entirely**

Overwrite `base/CLAUDE.template.md` with exactly:

```markdown
<!-- template-version: 2026-07 -->
<!--
  ============================================================================
  CLAUDE.md TEMPLATE  (stack-agnostic project guidance for Claude Code / agents)
  ============================================================================
  HOW TO USE: follow the seed's SETUP.md checklist. In short:
    1. Replace every {{PLACEHOLDER}} with a real value.
    2. Act on every "ADAPT:" note, then delete the note.
    3. [Day-0] sections are filled at setup. [Grows] sections start empty and
       fill from real incidents — never pre-fill them.
    4. Delete this comment block. Budget: ~150 lines post-fill; past that,
       migrate content to docs/wiki/ and leave pointers.
  Load-bearing principles: Invariants 3 and 4 (Source of Truth,
  Symbols-Not-Counts). Keep them even if you cut everything else.
  ============================================================================
-->

# CLAUDE.md

Guidance for Claude Code (and other agents) working in this repository.
**These instructions override default behavior — follow them exactly.**

## Role & Context  [Day-0]

{{ONE-LINE DESCRIPTION OF THE PROJECT}}

- **Domain**: {{e.g. fintech ledger / realtime chat / data pipeline}}
- **Stance**: Be concise. Give brutal, honest engineering feedback — reject
  bad patterns and explain why; don't optimize for politeness.
- **Never assume**: {{THE ONE THING AGENTS MUST ALWAYS ASK ABOUT — or delete}}

## ⛔ Critical Invariants (NEVER VIOLATE)

Non-negotiable. Breaking one invalidates the task.

### 1. Verification Gate
- Run `{{CHECK CMD — e.g. npm run check}}` (format + lint + typecheck + fast
  tests) **before claiming completion or committing**. It must exit clean:
  **0 errors, 0 warnings**. The Stop hook (`.claude/hooks/verify_on_stop.py`)
  enforces this mechanically — don't argue with it; fix the failure.
- **NEVER** suppress a warning without explicit user approval.
- A clean local check does not equal a clean CI run — CI runs the full suite
  and strict build. Verify the way CI does ({{CI-EQUIVALENT CMD}}) before
  claiming "done" on release-bound work.

### 2. Test Integrity
- **NEVER** weaken, skip, delete, or `.only` a test to make the suite pass.
  A failing test is a finding, not an obstacle.
- Changing a test's assertions requires explicit user approval.

### 3. Source of Truth (anti-rot)
- **One fact lives in one place.** Link to it; never duplicate it. Duplicated
  facts drift out of sync and start contradicting each other.
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
  - Money/ledger: never use floats for currency; never mutate a posted entry.
  - Frontend: never block the UI thread; keep render paths allocation-light.
You almost certainly have at least one. -->

## Everyday Task Discipline

Applies to EVERY task. (Complex or risky work additionally gets the
UltraThink review — see Deep-Analysis Protocol below.)

- **Surgical changes**: every changed line must trace to the user's request.
  Don't refactor, rename, reformat, or "improve" code the task didn't touch.
  Notice an adjacent problem? Report it; don't fix it unasked.
- **Simplicity first**: no speculative abstractions, no unrequested features,
  no defensive boilerplate for conditions that can't occur. Self-check before
  finishing: "would a senior reviewer call this over-engineered?"
- **Think before coding**: state your assumptions. If the request has two
  plausible readings, ask — or state the reading you chose and why.
- **Goal-driven execution**: restate the task as steps of the form
  `[step] → verify: [check]`. A step without a verify is not a step.
- **Calibration**: bias toward caution; for trivial tasks, use judgment.

## Tech Stack  [Day-0]

| Component | Version | Why this / why pinned |
|-----------|---------|-----------------------|
| {{LANGUAGE}} | {{VER}} | {{constraint, or "latest stable"}} |
| {{FRAMEWORK}} | {{VER}} | {{version-pin reason, if any}} |
| {{KEY LIB}} | {{VER}} | {{why this one}} |
<!-- ADAPT: list only versions that constrain decisions. Record WHY a version
is pinned — that reasoning stops a future agent from "helpfully" upgrading. -->

## Commands  [Day-0]

The six-script contract lives in `package.json` (single source of truth):
`check` (THE gate), `test`, `test:one`, `fix`, `dev`, `build`.
<!-- ADAPT (non-JS stacks): replace with a table mapping the six contract
names to your real commands, e.g. check = `cargo clippy -- -D warnings;
cargo test --lib`. The six semantics stay; the tool changes. Update
CHECK_COMMAND in .claude/hooks/verify_on_stop.py to match. -->

## Architecture  [Grows]

### Layout
{{TOP-LEVEL DIRECTORY MAP — one line per major dir, what lives there}}

### Data / Control Flow
{{HOW A REQUEST OR INPUT MOVES THROUGH THE SYSTEM, END TO END}}

### Key Components
- **{{ComponentName}}** (`{{path}}`): {{responsibility, one line}}
<!-- ADAPT: fill as the code grows. Describe the seams an agent must respect
(layer boundaries, the one service that owns X). Name symbols, never counts.
Non-obvious patterns belong here; obvious things don't. -->

## Project Gotchas  [Grows]

<!-- Start empty. Fill from real incidents, not speculation — via /log-gotcha.
One-liners only; narratives longer than ~3 lines live in docs/wiki/ with a
pointer here. Format:

### {{Short title of the trap}}
**Problem**: {{what goes wrong, concretely}} → **Rule**: {{the pattern that
avoids it, with the symbol name involved}}
-->

## Standing Rules

- **Git**: atomic commits, only at a green `check`. Conventional-commit
  subject; the *why* in the body. Never commit secrets or `.env`.
- **Dependencies**: stdlib first → existing deps → a NEW dependency needs
  explicit approval plus a stated alternative you considered. Lockfile always
  committed.
- **Security**: secrets live in env vars only (`.env` ignored,
  `.env.example` committed). Parameterize all queries. Never log secrets.
- **Errors**: fail fast. No bare catch-and-continue; errors surface to the
  user or the log, never silently vanish.
- **Style**: enforced by `{{FORMATTER}}` config. Never hand-format against
  it. No style rules belong in this file.
- **Session workflow**: at start, skim Project Gotchas and recent titles in
  `docs/adr/`. At end, run `/log-gotcha` for anything hard-won this session.

## Docs & Knowledge Schema

**Fact-placement law** — one fact, one home:

| Kind of fact | Home |
|---|---|
| What the code does | The code (+ Architecture section for the seams) |
| Agent behavior + facts needed every session | This file |
| Decisions and their why | `docs/adr/` (append-only; supersede, never edit) |
| Narratives: incidents, investigations, domain notes | `docs/wiki/` |

- **Gotcha migration**: gotchas start as one-liners above; past ~3 lines they
  move to a wiki page, leaving a one-line pointer.
- **ADR discipline**: before changing architecture, grep `docs/adr/` titles.
  Never contradict an accepted ADR without writing a superseding one.
- **Wiki conventions**: `docs/wiki/index.md` lists every page — read the
  relevant section before working in an unfamiliar area. `docs/wiki/log.md`
  is append-only: `## [YYYY-MM-DD] <verb> | <title>` plus 1–3 lines. Pages
  cite stable symbols, never counts. Stale content is deleted, not kept
  "just in case". File only what is non-obvious, recurring, or expensive to
  re-derive.

## Deep-Analysis Protocol

For complex or high-risk changes, run the **ultrathink** skill BEFORE writing
code. Triggers (sole home of this list): architecture decisions, new
subsystems, security-sensitive or performance-critical paths, irreversible
data/schema changes. Changes touching more than 2 modules or with
irreversible consequences also get a one-page spec first (copy
`docs/specs/SPEC.template.md`); ultrathink then reviews the spec.

---

*These guidelines are working if: sessions start without re-explaining the
project; agents cite ADRs when questioning decisions; the verification gate
never needs mentioning in chat.*
```

- [ ] **Step 2: Verify required content (Grep tool, path `base/CLAUDE.template.md`)**

| Pattern | Expected |
|---|---|
| `Test Integrity` | 1+ match |
| `Everyday Task Discipline` | 1+ match |
| `before claiming completion or committing` | 1 match |
| `verify_on_stop.py` | 1+ match |
| `Fact-placement law` | 1 match |
| `sole home of this list` | 1 match |
| `<PLACEHOLDER` (angle style) | 0 matches |
| `multi-file changes` | 0 matches |
| `Batch related operations` | 0 matches |
| `template-version: 2026-07` | 1 match |

- [ ] **Step 3: Commit**

```powershell
git add base/CLAUDE.template.md
git commit -m @'
feat: revise CLAUDE.md template per v2 spec section 4

Adds test-integrity invariant, Everyday Task Discipline (Karpathy layer),
standing rules, Docs & Knowledge Schema (fact-placement law), Day-0/Grows
tags, {{}} placeholders, version stamp, 150-line post-fill budget. Fixes the
gate contradiction (tests now inside the gate) and cuts persona theater,
batch-ops, and prose style rules.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
'@
```

---

### Task 3: Convert UltraThink to a skill (spec §5)

**Files:**
- Create: `base/.claude/skills/ultrathink/SKILL.md`
- Delete: `ultrathink.template.md` (seed root)

**Interfaces:**
- Consumes: CLAUDE.template.md heading `Deep-Analysis Protocol` (Task 2) as the sole home of the trigger list, and `⛔ Critical Invariants (NEVER VIOLATE)` as Phase 1 stop conditions.
- Produces: ADR-saving convention `docs/adr/NNNN-<slug>.md` consumed by Task 7's ADR README.

- [ ] **Step 1: Create `base/.claude/skills/ultrathink/SKILL.md`**

With exactly:

```markdown
---
name: ultrathink
description: Adversarial multi-perspective design review run BEFORE complex or high-risk changes — architecture decisions, new subsystems, security-sensitive or performance-critical paths, irreversible data/schema changes. Output is saved as an ADR. Not for single-file edits, typo fixes, or trivial config changes.
---

<!-- template-version: 2026-07 -->

# UltraThink Protocol

An adversarial design review run **before** building anything non-trivial.
Surfaces architecture, correctness, and edge-case risk while it's still
cheap — on paper, not in a failed deploy.

**When to run**: the trigger list lives in CLAUDE.md → Deep-Analysis Protocol
(sole home — do not restate it here). **Skip for** single-file edits, typo
fixes, trivial config changes. If a spec exists in `docs/specs/`, review THE
SPEC, not a finished diff.

## Phase 0: Clarification Gate

Identify 1–2 critical unknowns. Ask only if genuinely ambiguous:
- **Scope**: production-grade or proof-of-concept?
- **Trade-off**: optimize for speed, memory, simplicity, or maintainability?
- **Integration**: which existing component should own this?

**Skip** if requirements are unambiguous from context.

## Phase 1: Critical Rejection Check

Open CLAUDE.md and read the **⛔ Critical Invariants now** — every one of
them is a stop condition here. STOP and challenge the user if the request
implies violating one, or any universal red flag:
- Untrusted input reaching a shell, query, or interpreter without sanitization.
- Secrets/credentials logged, hardcoded, or committed.
- Irreversible data loss or unsafe migration without a backout path.
- Breaking a public contract (API shape, schema, file format) without
  versioning.

**Minor concerns**: flag them in the synthesis; don't stop.

## Phase 2: Multi-Perspective Debate

Simulate the debate internally — reason, don't tick boxes.

### The Architect — system design, performance, maintainability
| Question | Why it matters |
|----------|----------------|
| Which existing component should own this? | Reuse before inventing |
| Does it fit the established data/control flow? | Don't bypass layer boundaries |
| What's the performance/memory cost at scale? | Hot paths and large inputs |
| Simplest design that's still correct? | Complexity is debt; justify every abstraction |
| {{STACK-SPECIFIC DESIGN QUESTION — or delete this row}} | {{why}} |

### The User / Domain Advocate — utility, trust, workflow
| Question | Why it matters |
|----------|----------------|
| Does this solve the user's real problem? | Don't build the wrong thing well |
| Is it discoverable and predictable? | Surprising behavior erodes trust |
| Can the user verify what happened? | Don't hide state behind magic |
| Does it match existing patterns and visuals? | Consistency over novelty |
| {{DOMAIN-SPECIFIC USER QUESTION — or delete this row}} | {{why}} |

### The Devil's Advocate — edge cases, failures, security, entropy
| Question | Why it matters |
|----------|----------------|
| Malformed / hostile / empty input? | Graceful degradation, not a crash |
| Largest realistic input — still holds? | Memory, timeouts, back-pressure |
| Concurrency / race conditions? | Shared state, ordering, cancellation |
| Is failure observable, or silently swallowed? | Errors must surface |
| Is cancellation / timeout honored throughout? | No orphaned work |
| Does this add an abstraction the task doesn't need? | Speculative structure is debt |
| Any defensive boilerplate for impossible conditions? | Noise that buries real handling |
| Does it pull in a NEW dependency? | Needs approval + alternative (CLAUDE.md → Standing Rules) |
| Does it lean on a deprecated or legacy API? | Agents reproduce stale idioms; check current docs |

## Phase 3: Debate Output

- **Synthesis**: ONE non-obvious key concern + its resolution per
  perspective. Skip perspectives with nothing non-obvious to say.
- **Options Considered**: Option A (selected) — why it wins. Option B
  (discarded) — why it lost.
- **Architecture Decision**: owner (component/layer), integration point,
  data flow (source → transform → sink).

**Save it**: write Phase 3 as `docs/adr/NNNN-<slug>.md` (next free number,
status: proposed) BEFORE implementation starts. See `docs/adr/README.md`.

## CHECKPOINT

Present Phase 3 via plan mode. **Plan approval IS the checkpoint** — it also
flips the ADR to accepted.

## Phase 4: Implementation Plan

Only after approval.
- New external dependency? Apply CLAUDE.md → Standing Rules (approval +
  alternative considered + license check).
- Existing pattern to reuse? Search before creating.
- Derive integration points fresh from CLAUDE.md → Architecture — do NOT
  maintain a copy of that map here.
- 3–7 atomic steps, each written as `[step] → verify: [check]`.

## Phase 5: Design-Review Gates

- [ ] Input validation covers any new entry point.
- [ ] Cancellation / timeout propagated throughout.
- [ ] Thread-safe where state is shared.
- [ ] Failures surface to the user (no silent catch).
- [ ] {{PROJECT-SPECIFIC PERFORMANCE/SAFETY GATE — or delete}}

## Phase 6: Verification

Governed entirely by CLAUDE.md → ⛔ Critical Invariants (Verification Gate +
Test Integrity). Nothing to restate here.

---

If this protocol missed something, update this file — cite symbols, never
counts or line numbers (CLAUDE.md Invariant 4).

**Flow**: Clarify → Reject-Critical → Debate → Output+ADR → Approve → Plan → Gates → Verify
```

- [ ] **Step 2: Delete the old root template**

```powershell
git rm "ultrathink.template.md"
```

- [ ] **Step 3: Verify (Grep tool, path `base/.claude/skills/ultrathink/SKILL.md`)**

| Pattern | Expected |
|---|---|
| `sole home` | 1 match |
| `docs/adr/NNNN-` | 1 match |
| `Plan approval IS the checkpoint` | 1 match |
| `deprecated or legacy API` | 1 match |
| `Integration Points` | 0 matches |
| `Quick Reference` | 0 matches |
| `Post-Mortem` | 0 matches |
| `multi-file changes` | 0 matches |

Also verify frontmatter: file starts with `---`, has `name: ultrathink` and a `description:` line, closed by `---`.

- [ ] **Step 4: Commit**

```powershell
git add -A
git commit -m @'
feat: convert ultrathink protocol to a skill, saving reviews as ADRs

Skill loads on demand instead of always-on. Trigger list now lives only in
CLAUDE.md (dropped over-broad "multi-file changes"). Phase 3 output persists
as docs/adr/NNNN instead of evaporating in the transcript. Adds entropy rows
to Devil's Advocate; cuts Integration Points map, Quick Reference, and
Post-Mortem table (rot magnets duplicating CLAUDE.md).

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
'@
```

---

### Task 4: protect_files.py hook (spec §6, TDD)

**Files:**
- Create: `base/.claude/hooks/protect_files.py`
- Test: `tests/hooks/test_protect_files.py` (seed-level; NOT copied into apps)

**Interfaces:**
- Consumes: PreToolUse hook contract — JSON on stdin `{"tool_name": "Edit", "tool_input": {"file_path": "..."}}`; exit 0 = allow, exit 2 = block (stderr fed back to the agent).
- Produces: `base/.claude/hooks/protect_files.py` registered by Task 6's settings.template.json under matcher `Edit|Write`.

- [ ] **Step 0: Verify Python is available**

```powershell
python --version
```
Expected: `Python 3.9` or higher. If missing, stop and report — the hooks tasks cannot proceed.

- [ ] **Step 1: Write the failing test**

Create `tests/hooks/__init__.py` (empty file) and `tests/hooks/test_protect_files.py` with exactly:

```python
"""Tests for base/.claude/hooks/protect_files.py — run from the seed root:
python -m unittest discover -s tests -v
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[2] / "base" / ".claude" / "hooks" / "protect_files.py"


def run_hook(tool_input):
    payload = json.dumps({"tool_name": "Edit", "tool_input": tool_input})
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=payload, capture_output=True, text=True, timeout=30,
    )


class ProtectFilesTests(unittest.TestCase):
    def test_blocks_env_file(self):
        result = run_hook({"file_path": "C:/proj/.env"})
        self.assertEqual(result.returncode, 2)
        self.assertIn("secrets", result.stderr)

    def test_blocks_env_variant(self):
        result = run_hook({"file_path": "/home/u/proj/.env.production"})
        self.assertEqual(result.returncode, 2)

    def test_allows_env_example(self):
        result = run_hook({"file_path": "C:/proj/.env.example"})
        self.assertEqual(result.returncode, 0)

    def test_blocks_lockfile(self):
        result = run_hook({"file_path": "C:/proj/package-lock.json"})
        self.assertEqual(result.returncode, 2)
        self.assertIn("lockfile", result.stderr)

    def test_blocks_git_internals(self):
        result = run_hook({"file_path": "C:/proj/.git/config"})
        self.assertEqual(result.returncode, 2)

    def test_allows_normal_source_file(self):
        result = run_hook({"file_path": "C:/proj/src/app.ts"})
        self.assertEqual(result.returncode, 0)

    def test_allows_on_malformed_input(self):
        result = subprocess.run(
            [sys.executable, str(HOOK)],
            input="not json", capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0)

    def test_allows_on_missing_file_path(self):
        result = run_hook({})
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

```powershell
python -m unittest discover -s tests -v
```
Expected: errors — the hook file does not exist yet (`FileNotFoundError` / non-zero exit).

- [ ] **Step 3: Write the hook**

Create `base/.claude/hooks/protect_files.py` with exactly:

```python
#!/usr/bin/env python3
"""PreToolUse hook: block agent edits to protected files.

Reads the tool-call JSON from stdin. Exit 2 blocks the call and feeds the
stderr message back to the agent; exit 0 allows it. Stdlib only; Windows-safe.
Registered in .claude/settings.json under PreToolUse, matcher "Edit|Write".
"""
import json
import sys
from pathlib import PurePath

# ADAPT: extend these per project.
PROTECTED_BASENAMES = {
    "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb",
}
PROTECTED_SEGMENTS = {".git"}
ALLOWED_ENV_FILES = {".env.example"}


def is_protected(file_path):
    """Return a human-readable reason if the path is protected, else None."""
    path = PurePath(file_path.replace("\\", "/"))
    name = path.name.lower()
    if name in ALLOWED_ENV_FILES:
        return None
    if name == ".env" or name.startswith(".env."):
        return "%s may contain secrets; the user edits it manually" % path.name
    if name in PROTECTED_BASENAMES:
        return "%s is a lockfile; change deps via the package manager" % path.name
    for segment in path.parts[:-1]:
        if segment.lower() in PROTECTED_SEGMENTS:
            return "%s/ internals must not be edited directly" % segment
    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # malformed input: never block on our own bug
    file_path = (payload.get("tool_input") or {}).get("file_path", "")
    if not file_path:
        return 0
    reason = is_protected(file_path)
    if reason:
        print("BLOCKED by protect_files hook: %s." % reason, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

```powershell
python -m unittest discover -s tests -v
```
Expected: `OK` with 8 tests passed.

- [ ] **Step 5: Commit**

```powershell
git add tests/hooks base/.claude/hooks/protect_files.py
git commit -m @'
feat: add protect_files PreToolUse hook with tests

Blocks agent edits to .env* (except .env.example), lockfiles, and .git/
internals. Python stdlib only so it runs on Windows without bash/jq.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
'@
```

---

### Task 5: verify_on_stop.py hook (spec §6, TDD)

**Files:**
- Create: `base/.claude/hooks/verify_on_stop.py`
- Test: `tests/hooks/test_verify_on_stop.py`

**Interfaces:**
- Consumes: Stop hook contract — JSON on stdin (field `stop_hook_active: bool`); exit 0 = allow stop, exit 2 = block stop (stderr fed back).
- Produces: `CHECK_COMMAND` default `npm run check`, overridable via env var `HARNESS_CHECK_CMD` (the single configuration point + test seam). `--self-test` flag consumed by SETUP.md (Task 12).

- [ ] **Step 1: Write the failing test**

Create `tests/hooks/test_verify_on_stop.py` with exactly:

```python
"""Tests for base/.claude/hooks/verify_on_stop.py — run from the seed root:
python -m unittest discover -s tests -v
"""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[2] / "base" / ".claude" / "hooks" / "verify_on_stop.py"

PASS_CMD = '%s -c "raise SystemExit(0)"' % sys.executable
FAIL_CMD = '%s -c "print(\'boom\'); raise SystemExit(1)"' % sys.executable


def run_hook(stdin_obj, check_cmd, extra_args=None):
    env = dict(os.environ, HARNESS_CHECK_CMD=check_cmd)
    return subprocess.run(
        [sys.executable, str(HOOK)] + (extra_args or []),
        input=json.dumps(stdin_obj), capture_output=True, text=True,
        timeout=60, env=env,
    )


class VerifyOnStopTests(unittest.TestCase):
    def test_allows_stop_when_check_passes(self):
        result = run_hook({"stop_hook_active": False}, PASS_CMD)
        self.assertEqual(result.returncode, 0)

    def test_blocks_stop_when_check_fails(self):
        result = run_hook({"stop_hook_active": False}, FAIL_CMD)
        self.assertEqual(result.returncode, 2)
        self.assertIn("failed", result.stderr)
        self.assertIn("boom", result.stderr)

    def test_skips_check_when_already_looping(self):
        # stop_hook_active=True must exit 0 WITHOUT running the (failing) command
        result = run_hook({"stop_hook_active": True}, FAIL_CMD)
        self.assertEqual(result.returncode, 0)

    def test_tolerates_malformed_stdin(self):
        env = dict(os.environ, HARNESS_CHECK_CMD=PASS_CMD)
        result = subprocess.run(
            [sys.executable, str(HOOK)], input="not json",
            capture_output=True, text=True, timeout=60, env=env,
        )
        self.assertEqual(result.returncode, 0)

    def test_self_test_passes_for_non_npm_command(self):
        result = run_hook({}, PASS_CMD, extra_args=["--self-test"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("self-test OK", result.stdout)

    def test_self_test_fails_when_npm_script_missing(self):
        # Runs in the seed root, which has no package.json — npm-run commands must fail self-test
        result = run_hook({}, "npm run check", extra_args=["--self-test"])
        self.assertEqual(result.returncode, 1)
        self.assertIn("self-test FAIL", result.stdout)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify the new ones fail**

```powershell
python -m unittest discover -s tests -v
```
Expected: the 8 protect_files tests pass; all 6 verify_on_stop tests error (hook file missing).

- [ ] **Step 3: Write the hook**

Create `base/.claude/hooks/verify_on_stop.py` with exactly:

```python
#!/usr/bin/env python3
"""Stop hook: run the fast verification gate before the agent stops.

Exit 0 lets the agent stop; exit 2 blocks the stop and feeds stderr back so
the agent fixes the failure first. Stdlib only; Windows-safe.
Registered in .claude/settings.json under Stop.

--self-test verifies the wiring (used by SETUP.md step 4).
"""
import json
import os
import subprocess
import sys

# ADAPT: the single configuration point. Must match CLAUDE.md's Verification
# Gate and CI. HARNESS_CHECK_CMD env override exists as a test seam.
CHECK_COMMAND = os.environ.get("HARNESS_CHECK_CMD", "npm run check")
TIMEOUT_SECONDS = 300
OUTPUT_TAIL_CHARS = 3000


def run_check():
    try:
        result = subprocess.run(
            CHECK_COMMAND, shell=True, capture_output=True, text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        print(
            "verify_on_stop: '%s' timed out after %ss."
            % (CHECK_COMMAND, TIMEOUT_SECONDS),
            file=sys.stderr,
        )
        return 2
    if result.returncode == 0:
        return 0
    output = (result.stdout or "") + (result.stderr or "")
    print(
        "verify_on_stop: '%s' failed (exit %s). Fix before stopping.\n%s"
        % (CHECK_COMMAND, result.returncode, output[-OUTPUT_TAIL_CHARS:]),
        file=sys.stderr,
    )
    return 2


def self_test():
    if CHECK_COMMAND.startswith("npm run "):
        script = CHECK_COMMAND[len("npm run "):].split()[0]
        try:
            with open("package.json", encoding="utf-8") as f:
                scripts = json.load(f).get("scripts", {})
        except (OSError, ValueError) as exc:
            print("self-test FAIL: cannot read package.json (%s)" % exc)
            return 1
        if script not in scripts:
            print("self-test FAIL: package.json has no '%s' script" % script)
            return 1
    print("self-test OK: check command is '%s'" % CHECK_COMMAND)
    return 0


def main():
    if "--self-test" in sys.argv:
        return self_test()
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        payload = {}
    if payload.get("stop_hook_active"):
        return 0  # this stop was already triggered by us once; let it through
    return run_check()


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

```powershell
python -m unittest discover -s tests -v
```
Expected: `OK`, 14 tests passed.

- [ ] **Step 5: Commit**

```powershell
git add tests/hooks base/.claude/hooks/verify_on_stop.py
git commit -m @'
feat: add verify_on_stop Stop hook with tests

Runs the fast gate (npm run check by default, single config point) before
the agent may stop; exit 2 feeds the failure back. Guards stop_hook_active
against loops. --self-test validates wiring for SETUP.md.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
'@
```

---

### Task 6: settings.template.json (spec §6)

**Files:**
- Create: `base/.claude/settings.template.json`

**Interfaces:**
- Consumes: both hook scripts from Tasks 4–5 at their `.claude/hooks/` paths (paths are relative to a seeded app's root, where the file is renamed to `.claude/settings.json`).
- Produces: the permission posture SETUP.md (Task 12) tells users to review.

- [ ] **Step 1: Verify the current settings/hooks schema before writing**

Dispatch the `claude-code-guide` agent (Agent tool) with: "What is the current settings.json schema for (a) permissions allow/ask/deny arrays including Read() and Bash() rule syntax, and (b) hooks registration for PreToolUse with a matcher and Stop, type command? Show a complete valid example. Also: are unknown top-level keys rejected?" Adjust Step 2's JSON if the schema differs from it. This fulfills the spec §6 requirement to verify the hook schema against current docs.

- [ ] **Step 2: Create `base/.claude/settings.template.json`**

With exactly (adjusted per Step 1 findings if needed):

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run check:*)",
      "Bash(npm run test:*)",
      "Bash(npm run fix:*)",
      "Bash(npm run build:*)",
      "Bash(npm run dev:*)",
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)"
    ],
    "ask": [
      "Bash(git push:*)",
      "Bash(npm install:*)",
      "Bash(npx:*)",
      "Bash(gh:*)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.local)",
      "Read(./.env.development)",
      "Read(./.env.production)",
      "Bash(rm -rf:*)",
      "Bash(curl:*)",
      "Bash(wget:*)",
      "Bash(Invoke-WebRequest:*)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/protect_files.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/verify_on_stop.py"
          }
        ]
      }
    ]
  }
}
```

Note: `.env.example` stays readable because deny rules enumerate specific env files instead of using a wildcard (permission rules have no "except" syntax). The npm-flavored allowlist is intentional — non-JS stacks edit it during SETUP.md; JSON cannot carry ADAPT comments.

- [ ] **Step 3: Verify it is valid JSON**

```powershell
python -c "import json; json.load(open('base/.claude/settings.template.json', encoding='utf-8')); print('valid JSON')"
```
Expected: `valid JSON`

- [ ] **Step 4: Commit**

```powershell
git add base/.claude/settings.template.json
git commit -m @'
feat: add settings template with permissions and hook registrations

Moderate autonomy posture: allow project scripts and local git; ask on
push/install/npx/gh; deny env-file reads, rm -rf, and raw network fetches.
Registers protect_files (PreToolUse Edit|Write) and verify_on_stop (Stop).

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
'@
```

---

### Task 7: Knowledge-system docs — ADRs, wiki, spec template (spec §7)

**Files:**
- Create: `base/docs/adr/README.md`, `base/docs/adr/0000-template.md`, `base/docs/wiki/index.md`, `base/docs/wiki/log.md`, `base/docs/specs/SPEC.template.md`

**Interfaces:**
- Consumes: ADR naming `docs/adr/NNNN-<slug>.md` (Task 3); wiki conventions defined in CLAUDE.template.md → Docs & Knowledge Schema (Task 2) — these files POINT there, never restate.
- Produces: `0000-template.md` structure consumed by the ultrathink skill and Task 12's "write ADR-0001" step; wiki index categories consumed by the log-gotcha skill (Task 8).

- [ ] **Step 1: Create `base/docs/adr/README.md`**

With exactly:

```markdown
<!-- template-version: 2026-07 -->
# Architecture Decision Records

Write one for any decision you would otherwise re-derive or relitigate:
stack choices, data model, auth approach, build tooling — and every
UltraThink Phase 3 output. ADR-0001 is always the stack choice, written at
setup.

Rules:
- Copy `0000-template.md` to `NNNN-<slug>.md` (next free number).
- Append-only: never edit an accepted ADR. Write a superseding one and link
  both directions ("superseded by NNNN" / "supersedes NNNN").
- Keep it ~25 lines. Cite symbols, not counts (CLAUDE.md Invariant 4).
```

- [ ] **Step 2: Create `base/docs/adr/0000-template.md`**

With exactly:

```markdown
<!-- template-version: 2026-07 -->
# {{NNNN}}. {{Decision title}}

- **Date**: {{YYYY-MM-DD}}
- **Status**: {{proposed | accepted | superseded by NNNN}}

## Context

{{What forces this decision? 2–5 lines.}}

## Options considered

- **{{Option A}}** — {{one-line pros / cons}}
- **{{Option B}}** — {{one-line pros / cons}}

## Decision

{{What we chose, and the decisive reason.}}

## Consequences

{{What becomes easier/harder; follow-ups; what would trigger revisiting.}}
```

- [ ] **Step 3: Create `base/docs/wiki/index.md`**

With exactly:

```markdown
<!-- template-version: 2026-07 -->
# Project Wiki — Index

Entry point for on-demand knowledge. Every page in `docs/wiki/` MUST be
listed here, one line each, with a one-line summary. Read the relevant
section before working in an unfamiliar area. Conventions live in
CLAUDE.md → Docs & Knowledge Schema.

## Architecture

(none yet)

## Gotchas & incidents

(none yet)

## Investigations

(none yet)

## Domain notes

(none yet)
```

- [ ] **Step 4: Create `base/docs/wiki/log.md`**

With exactly:

```markdown
<!-- template-version: 2026-07 -->
# Project Log (append-only)

Newest entries at the top. Entry format is defined in CLAUDE.md → Docs &
Knowledge Schema. Verbs: added, fixed, decided, investigated, learned.
```

- [ ] **Step 5: Create `base/docs/specs/SPEC.template.md`**

With exactly:

```markdown
<!-- template-version: 2026-07 -->
# Spec: {{Feature name}} ({{YYYY-MM-DD}})

Use for changes touching more than 2 modules or with irreversible
consequences (threshold defined in CLAUDE.md → Deep-Analysis Protocol).
One page, then stop. UltraThink reviews this spec, not a finished diff.

## Problem

{{What hurts today, for whom, concretely.}}

## Desired behavior

{{Observable behavior after the change. Examples beat adjectives.}}

## Non-goals

{{What this change deliberately does NOT do.}}

## Acceptance criteria

1. {{Verifiable statement.}}

## Open questions

- {{Only things the user must decide.}}

## Plan

1. {{step}} → verify: {{check}}
2. {{step}} → verify: {{check}}
```

- [ ] **Step 6: Verify single-source rule**

Grep `base/docs/` for `YYYY-MM-DD] <verb>` — expected 0 matches (the log entry format lives only in CLAUDE.template.md; log.md points at it). Grep `base/docs/adr/README.md` for `NNNN-<slug>` — expected 1 match.

- [ ] **Step 7: Commit**

```powershell
git add base/docs
git commit -m @'
feat: add knowledge-system docs — ADRs, wiki index/log, spec template

MADR-lite decision records (append-only, superseded not edited), minimal
lazily-grown wiki (index + log), one-page spec template with verify-per-step
plan skeleton. Conventions live in CLAUDE.md; these files point at them.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
'@
```

---

### Task 8: log-gotcha and wiki-lint skills (spec §7)

**Files:**
- Create: `base/.claude/skills/log-gotcha/SKILL.md`, `base/.claude/skills/wiki-lint/SKILL.md`

**Interfaces:**
- Consumes: CLAUDE.template.md headings `Project Gotchas`, `Docs & Knowledge Schema` (Task 2); wiki files from Task 7; ADR rules from Task 7's README.

- [ ] **Step 1: Create `base/.claude/skills/log-gotcha/SKILL.md`**

With exactly:

```markdown
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
```

- [ ] **Step 2: Create `base/.claude/skills/wiki-lint/SKILL.md`**

With exactly:

```markdown
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
   `{{` and `ADAPT:` — both must return nothing in a live project.
6. **Report**: a fix-list grouped by file — finding + suggested action.
```

- [ ] **Step 3: Verify frontmatter of both skills**

Each file starts with `---`, contains `name:` matching its directory name and a `description:`, closed by `---`. Grep `base/.claude/skills/` for `template-version: 2026-07` — expected 3 matches (including ultrathink).

- [ ] **Step 4: Commit**

```powershell
git add base/.claude/skills
git commit -m @'
feat: add log-gotcha and wiki-lint skills

log-gotcha: end-of-incident capture with the graduation rule (one-liner ->
wiki page -> mechanical check, prose deleted once enforced). wiki-lint:
periodic docs health check exploiting symbols-not-counts to make staleness
greppable. Both point at CLAUDE.md conventions instead of restating them.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
'@
```

---

### Task 9: CI template (spec §6)

**Files:**
- Create: `base/.github/workflows/ci.template.yml`

**Interfaces:**
- Consumes: the six-script contract semantics (Global Constraints). The filled profile variant is Task 10's `ci.yml`.

- [ ] **Step 1: Create `base/.github/workflows/ci.template.yml`**

With exactly:

```yaml
# template-version: 2026-07
# ADAPT: fill every {{}} slot for your stack, or overlay profiles/<stack>/ci.yml
# from the seed. Rename to ci.yml. Delete this file if not hosted on GitHub.
# Policy: lint treats warnings as errors — any new warning fails the build.
name: CI

on:
  push:
    branches: [main, master]
  pull_request:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup toolchain
        run: {{TOOLCHAIN SETUP — or replace with a setup action, e.g. actions/setup-node@v4}}
      - name: Install
        run: {{INSTALL CMD — e.g. npm ci}}
      - name: Check (format + lint w/ zero warnings + typecheck + fast tests)
        run: {{CHECK CMD — same gate as CLAUDE.md Invariant 1}}
      - name: Test (full suite)
        run: {{TEST CMD}}
      - name: Build
        run: {{BUILD CMD}}
      - name: Dependency audit
        run: {{AUDIT CMD — e.g. npm audit --audit-level=high}}
```

- [ ] **Step 2: Verify**

Grep `base/.github/workflows/ci.template.yml` for `template-version` (1 match) and `same gate as CLAUDE.md` (1 match). No YAML parser check is needed — the file intentionally contains `{{}}` slots that only become valid YAML after fill-in; the filled profile variant in Task 10 is the syntax-checked one.

- [ ] **Step 3: Commit**

```powershell
git add base/.github
git commit -m @'
feat: add stack-agnostic CI workflow template

One job mirroring the six-script contract: check gate, full tests, build,
dependency audit. Warnings-as-errors is the stated policy. Delete-if-not-
GitHub is documented in the header.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
'@
```

---

### Task 10: TypeScript/Next.js profile (spec §10)

**Files:**
- Create: `profiles/typescript-next/README.md`, `profiles/typescript-next/CLAUDE.stack-sections.md`, `profiles/typescript-next/package-scripts.json`, `profiles/typescript-next/settings.json`, `profiles/typescript-next/ci.yml`

**Interfaces:**
- Consumes: six-script contract names; base settings structure (Task 6); CLAUDE.template.md section headings `Tech Stack`/`Commands` (Task 2), which the stack-sections file replaces verbatim.

- [ ] **Step 1: Confirm current stable tooling**

Use the context7 MCP tools (or WebSearch) to confirm the current stable major versions and idiomatic commands for: Next.js, TypeScript, Vitest, ESLint (flat config), Prettier — specifically that `eslint . --max-warnings 0`, `tsc --noEmit`, `vitest run`, and `prettier --check .` remain the correct invocations. Adjust Step 3/5 commands only if something changed; do NOT pin version numbers into the profile (versions live in a seeded app's package.json — source of truth).

- [ ] **Step 2: Create `profiles/typescript-next/README.md`**

With exactly:

```markdown
<!-- template-version: 2026-07 -->
# Profile: TypeScript / Next.js

Overlay for the stack-agnostic `base/`. Apply AFTER copying `base/*` into
the new repo (SETUP.md step 2):

1. Merge `package-scripts.json` → the `"scripts"` block of the app's
   `package.json` (created by `create-next-app` or `npm init`).
2. Copy `settings.json` → `.claude/settings.json` (replaces renaming the
   base template; already filled for npm/next/vitest/eslint/tsc).
3. Copy `ci.yml` → `.github/workflows/ci.yml` (replaces ci.template.yml).
4. Replace the `Tech Stack` and `Commands` sections of CLAUDE.md with the
   contents of `CLAUDE.stack-sections.md`.

Still manual afterwards: Role & Context, the project-specific invariant,
Invariant 1's `{{CHECK CMD}}` (fill with `npm run check`) and
`{{CI-EQUIVALENT CMD}}` (fill with `npm run check; npm test; npm run build`),
`{{FORMATTER}}` (Prettier), and ADR-0001. Dev dependencies expected by the
scripts: typescript, vitest, eslint (flat config), prettier.

When the test suite gets slow, narrow the `check` script's test step to
changed/affected tests (e.g. `vitest run --changed`) — the gate must stay
fast; CI runs the full suite.
```

- [ ] **Step 3: Create `profiles/typescript-next/package-scripts.json`**

With exactly:

```json
{
  "scripts": {
    "check": "prettier --check . && eslint . --max-warnings 0 && tsc --noEmit && vitest run",
    "test": "vitest run",
    "test:one": "vitest run -t",
    "fix": "prettier --write . && eslint . --fix",
    "dev": "next dev",
    "build": "next build"
  }
}
```

(Note: `&&` inside npm scripts is fine — npm runs them in its own shell; the no-`&&` rule in Global Constraints applies to PowerShell commands only. `test:one` usage: `npm run test:one -- "test name pattern"`.)

- [ ] **Step 4: Create `profiles/typescript-next/settings.json`**

Copy of Task 6's `settings.template.json` content with these additions to `"allow"` (insert after the `npm run dev` entry, keeping the rest identical):

```json
      "Bash(npx tsc:*)",
      "Bash(npx vitest run:*)",
      "Bash(npx eslint:*)",
      "Bash(npx prettier:*)",
```

And remove `"Bash(npx:*)"` from `"ask"` (the specific npx allows above replace the blanket ask; anything else npx still prompts by default).

- [ ] **Step 5: Create `profiles/typescript-next/ci.yml`**

With exactly:

```yaml
# template-version: 2026-07
# Filled TS/Next.js variant of base/.github/workflows/ci.template.yml
name: CI

on:
  push:
    branches: [main, master]
  pull_request:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm
      - name: Install
        run: npm ci
      - name: Check (format + lint w/ zero warnings + typecheck + fast tests)
        run: npm run check
      - name: Test (full suite)
        run: npm test
      - name: Build
        run: npm run build
      - name: Dependency audit
        run: npm audit --audit-level=high
```

- [ ] **Step 6: Create `profiles/typescript-next/CLAUDE.stack-sections.md`**

With exactly:

```markdown
<!-- template-version: 2026-07 -->
<!-- Replaces the Tech Stack and Commands sections of CLAUDE.md.
     Fill {{FORMATTER}} elsewhere in CLAUDE.md with: Prettier. -->

## Tech Stack  [Day-0]

| Component | Version | Why this / why pinned |
|-----------|---------|-----------------------|
| TypeScript | see package.json | strict mode on; the compiler is the first reviewer |
| Next.js (App Router) | see package.json | file-based routing, server components |
| Vitest | see package.json | fast, TS-native test runner |
| ESLint (flat config) + Prettier | see package.json | lint logic; formatting is Prettier's job alone |

## Commands  [Day-0]

The six-script contract lives in `package.json` (single source of truth):
`check` (THE gate), `test`, `test:one` (`npm run test:one -- "pattern"`),
`fix`, `dev`, `build`.
```

- [ ] **Step 7: Verify**

```powershell
python -c "import json; json.load(open('profiles/typescript-next/package-scripts.json', encoding='utf-8')); json.load(open('profiles/typescript-next/settings.json', encoding='utf-8')); print('valid JSON')"
```
Expected: `valid JSON`. Then grep `profiles/typescript-next/package-scripts.json` for `"check"`, `"test"`, `"test:one"`, `"fix"`, `"dev"`, `"build"` — all present (the six names exactly).

- [ ] **Step 8: Commit**

```powershell
git add profiles
git commit -m @'
feat: add TypeScript/Next.js profile overlay

Pre-filled six-script contract, settings allowlist, CI workflow, and
CLAUDE.md stack sections. No version pins - package.json is the source of
truth for versions. Cuts per-app setup from ~45 to ~5 minutes.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
'@
```

---

### Task 11: Seed README.md (spec §9)

**Files:**
- Create: `README.md` (seed root)

**Interfaces:**
- Consumes: every artifact from Tasks 1–10 (the map must list exactly what exists). Seed-root docs (README, SETUP, CHANGELOG) carry no template-version stamp — they never leave the seed; stamps exist to track propagation.

- [ ] **Step 1: Create `README.md`**

With exactly:

```markdown
# Template New App — a harness for AI-assisted development

The seed folder copied into every new application. Goal: long-term healthy
code with Claude Code — rules that enforce themselves, and knowledge that
compounds instead of evaporating in chat transcripts.

## Philosophy

1. **Instructions are requests; hooks are guarantees.** Every rule that can
   be a hook, config, or CI gate is one. CLAUDE.md keeps only judgment calls.
   Enforcement is layered: Stop hook → permissions → CI.
2. **Knowledge compounds.** Decisions land in ADRs (append-only), narratives
   in a lazily-grown wiki, hard-won gotchas in CLAUDE.md one-liners — each
   fact in exactly one home (fact-placement law in the CLAUDE.md template).
   Inspired by Karpathy's LLM-wiki pattern.
3. **YAGNI applies to the harness itself.** Nothing here is speculative;
   [Grows] sections start empty and fill from real incidents. Delete what a
   given app won't use — unused templates rot and erode trust in the rest.

## Map

| Path | Job |
|------|-----|
| `SETUP.md` | The per-app instantiation checklist. Start here. |
| `TEMPLATE-CHANGELOG.md` | Seed version history; how seeded apps learn what they're missing. |
| `base/CLAUDE.template.md` | The always-loaded operating manual: invariants, task discipline, standing rules, knowledge schema. |
| `base/.claude/settings.template.json` | Permission posture + hook registrations. |
| `base/.claude/hooks/` | `protect_files.py` (blocks edits to .env/lockfiles/.git), `verify_on_stop.py` (the gate runs before the agent may stop). |
| `base/.claude/skills/ultrathink/` | Adversarial design review before complex changes; output saved as an ADR. |
| `base/.claude/skills/log-gotcha/` | End-of-incident knowledge capture with a graduation rule. |
| `base/.claude/skills/wiki-lint/` | Docs health check — dead references, orphans, duplication, leftovers. |
| `base/docs/adr/` | Decision records (MADR-lite, append-only). |
| `base/docs/wiki/` | Index + append-only log; pages grow lazily from incidents. |
| `base/docs/specs/` | One-page spec template for >2-module or irreversible changes. |
| `base/.github/workflows/` | CI template: the same gate, warnings-as-errors, full tests, audit. |
| `profiles/typescript-next/` | Pre-filled overlay for TS/Next.js apps. |
| `tests/` | Seed-only tests for the hook scripts (`python -m unittest discover -s tests`). |
| `docs/superpowers/` | Specs/plans for the seed itself (not copied). |

## Instantiation

Copy `base/*` (including dotfiles) into the new repo → overlay a profile if
one fits → work through `SETUP.md` top to bottom → its exit gate greps for
leftover `{{PLACEHOLDER}}`/`ADAPT:` markers.

## Relationship to installed plugins

The harness deliberately does NOT duplicate generic workflows provided by
installed plugins (superpowers' TDD/brainstorming/verification, code-review,
claude-md-management). It ships only skills that encode project-local
contracts. If those plugins are absent, the harness still works — it just
enforces less.

## Upgrading seeded apps

Every copied template carries `template-version: YYYY-MM`. Diff an app's
stamp against `TEMPLATE-CHANGELOG.md`, then port the missing pieces by hand
(or with an agent). The seed is the canonical upstream; apps never edit
their copies expecting it to flow back — improvements land here first.
```

- [ ] **Step 2: Verify the map against reality**

```powershell
git ls-files
```
Every path named in the README table exists in the listing (profiles/, base/, tests/, SETUP.md pending Task 12 — if executing tasks in order, SETUP.md lands next; that forward reference is acceptable within this same plan).

- [ ] **Step 3: Commit**

```powershell
git add README.md
git commit -m @'
docs: add seed README - philosophy, map, instantiation, upgrade story

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
'@
```

---

### Task 12: SETUP.md bootstrap checklist (spec §8)

**Files:**
- Create: `SETUP.md` (seed root)

**Interfaces:**
- Consumes: `verify_on_stop.py --self-test` (Task 5), profile overlay steps (Task 10 README), the six-script contract, ADR-0001 convention (Task 7).

- [ ] **Step 1: Create `SETUP.md`**

With exactly:

```markdown
# New App Setup — Checklist

Work top to bottom inside the NEW app's repo. Do not skip the exit gate.
(This file lives in the seed and is never copied. If you copied the seed
folder wholesale, delete SETUP.md, README.md, TEMPLATE-CHANGELOG.md,
docs/superpowers/, tests/, and profiles/ from the app now.)

- [ ] 1. **Copy the base** — from the seed: `robocopy "<seed>\base" . /E`
      run at the new repo root (robocopy exit codes 0–3 are success), or any
      copy that includes dotfiles (`.gitignore`, `.env.example`,
      `.editorconfig`, `.claude/`, `.github/`).
- [ ] 2. **Overlay a profile** (optional) — TS/Next.js: follow
      `profiles/typescript-next/README.md` steps 1–4.
- [ ] 3. **Git + env hygiene** — `git init` if needed. Create `.env` from
      `.env.example`. Verify: `git check-ignore .env` prints `.env`.
- [ ] 4. **Fill the six-script contract** in `package.json`: `check`,
      `test`, `test:one`, `fix`, `dev`, `build` (the profile's
      `package-scripts.json` provides them). Non-npm stack: document the
      equivalents in CLAUDE.md → Commands AND update `CHECK_COMMAND` in
      `.claude/hooks/verify_on_stop.py`.
- [ ] 5. **Activate settings** — rename `.claude/settings.template.json` →
      `.claude/settings.json` (skip if the profile's `settings.json` was
      copied). Review the permission posture; it encodes moderate autonomy.
- [ ] 6. **Self-test the hooks** —
      `python .claude/hooks/verify_on_stop.py --self-test` prints
      `self-test OK`.
- [ ] 7. **Fill CLAUDE.md** — rename `CLAUDE.template.md` → `CLAUDE.md`.
      Replace every `{{PLACEHOLDER}}`, act on and delete every `ADAPT:`
      note, delete sections that don't apply, keep `[Grows]` sections
      empty, delete the header comment block. Budget: ~150 lines.
- [ ] 8. **Adapt the ultrathink skill** — fill or delete the `{{}}` rows in
      `.claude/skills/ultrathink/SKILL.md` (Phase 2 stack/domain rows,
      Phase 5 project gate).
- [ ] 9. **Write ADR-0001** — copy `docs/adr/0000-template.md` to
      `docs/adr/0001-stack-choice.md`; record the stack decision and the
      alternatives you rejected.
- [ ] 10. **CI** — fill and rename `.github/workflows/ci.template.yml` →
      `ci.yml`, or use the profile's `ci.yml`, or delete it if the app is
      not on GitHub.
- [ ] 11. **First commit at green** — `npm run check` exits clean, then
      commit everything.
- [ ] 12. **EXIT GATE** — both commands print nothing:

      Get-ChildItem -Recurse -File -Path CLAUDE.md, .claude, docs, .github | Select-String -Pattern '\{\{'
      Get-ChildItem -Recurse -File -Path CLAUDE.md, .claude, docs, .github | Select-String -Pattern 'ADAPT:'

      (POSIX: `grep -rn "{{" CLAUDE.md .claude/ docs/ .github/` and the same
      for `ADAPT:`.) A live CLAUDE.md containing unfilled placeholders
      actively misleads agents — do not finish with leftovers.
```

- [ ] **Step 2: Commit**

```powershell
git add SETUP.md
git commit -m @'
docs: add SETUP.md bootstrap checklist with placeholder exit gate

Ordered instantiation ritual: copy base, overlay profile, wire scripts and
settings, self-test hooks, fill CLAUDE.md, ADR-0001, CI, first green
commit. Exit gate greps for leftover {{}} and ADAPT: markers.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
'@
```

---

### Task 13: Integration verification — acceptance criteria + scratch instantiation (spec §13)

**Files:**
- Create (temporary, outside the repo): a scratch app under the session scratchpad directory
- Possibly modify: any seed file a check exposes as wrong (fix + commit)

**Interfaces:**
- Consumes: everything from Tasks 1–12.

- [ ] **Step 1: Single-source spot checks (spec acceptance criterion 7)**

Using the Grep tool over the whole seed:

| Pattern | Expected |
|---|---|
| `architecture decisions, new subsystems` | exactly 1 file: `base/CLAUDE.template.md` (trigger list has one home) |
| `format + lint + typecheck + fast` | matches only in `base/CLAUDE.template.md`; CI files may echo it only inside the step *name* labeled as pointing at the gate |
| `YYYY-MM-DD] <verb>` | exactly 1 file: `base/CLAUDE.template.md` (log format has one home) |
| `never weaken` (case-insensitive) | exactly 1 file: `base/CLAUDE.template.md` |
| `<PLACEHOLDER` | 0 matches anywhere |

- [ ] **Step 2: Version stamps + changelog (criterion 6)**

Grep the seed for `template-version: 2026-07` — expected in: base/CLAUDE.template.md, all 3 SKILL.md files, adr/README.md, adr/0000-template.md, wiki/index.md, wiki/log.md, SPEC.template.md, ci.template.yml, and 3 profile files (README, CLAUDE.stack-sections, ci.yml) = 12 files. JSON files are the documented exception. TEMPLATE-CHANGELOG.md has the `2026-07 — v2` entry.

- [ ] **Step 3: Hook test suite still green (criterion 4)**

```powershell
python -m unittest discover -s tests -v
```
Expected: `OK`, 14 tests.

- [ ] **Step 4: Scratch instantiation (criterion 5, adapted)**

Full `create-next-app` is slow and network-heavy; instead validate the harness mechanics end-to-end on a minimal TypeScript project using the profile's scripts (adapted where Next.js itself would be needed: `dev`/`build` become `tsc` variants). The Next-specific script lines were already syntax-confirmed in Task 10 Step 1. Record this adaptation in the final report.

In the session scratchpad directory (never `/tmp`, never inside the seed):

```powershell
$seed = "d:\Template New App"
$scratch = Join-Path $env:CLAUDE_SCRATCHPAD "harness-scratch"  # or any scratchpad-based path
Remove-Item -Recurse -Force $scratch -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force $scratch | Out-Null
robocopy "$seed\base" $scratch /E
```
robocopy exit code ≤ 3 is success.

Then, inside `$scratch`:

1. `git init`; `npm init -y`
2. `npm install -D typescript vitest eslint prettier @eslint/js typescript-eslint`
3. Merge the profile scripts into package.json, with scratch-appropriate dev/build:
   ```json
   "scripts": {
     "check": "prettier --check . && eslint . --max-warnings 0 && tsc --noEmit && vitest run",
     "test": "vitest run",
     "test:one": "vitest run -t",
     "fix": "prettier --write . && eslint . --fix",
     "dev": "tsc --watch",
     "build": "tsc --noEmit"
   }
   ```
4. Create `tsconfig.json`:
   ```json
   {
     "compilerOptions": {
       "target": "ES2022",
       "module": "ESNext",
       "moduleResolution": "Bundler",
       "strict": true,
       "skipLibCheck": true,
       "noEmit": true
     },
     "include": ["src"]
   }
   ```
5. Create `eslint.config.mjs`:
   ```js
   import js from "@eslint/js";
   import tseslint from "typescript-eslint";

   export default tseslint.config(
     js.configs.recommended,
     ...tseslint.configs.recommended,
     { ignores: ["node_modules"] }
   );
   ```
6. Create `.prettierignore` containing:
   ```
   package.json
   package-lock.json
   ```
7. Create `src/sum.ts`:
   ```ts
   export function sum(a: number, b: number): number {
     return a + b;
   }
   ```
   and `src/sum.test.ts`:
   ```ts
   import { describe, expect, it } from "vitest";
   import { sum } from "./sum";

   describe("sum", () => {
     it("adds two numbers", () => {
       expect(sum(2, 3)).toBe(5);
     });
   });
   ```
8. `Rename-Item .claude\settings.template.json settings.json`
9. Fill CLAUDE.template.md → CLAUDE.md with quick scratch values for every `{{}}`; delete all ADAPT comment blocks, the header block, and the `{{}}` rows in the ultrathink skill; delete `ci.template.yml`; create `.env` from `.env.example`.

**Verify, in order:**

| Check | Command (in $scratch) | Expected |
|---|---|---|
| Hook self-test | `python .claude/hooks/verify_on_stop.py --self-test` | `self-test OK`, exit 0 |
| Gate passes | `npm run check` | exit 0, no warnings |
| Stop hook end-to-end | `'{"stop_hook_active": false}' | python .claude/hooks/verify_on_stop.py` | exit 0 (runs the real npm gate) |
| Protect hook blocks | `'{"tool_name":"Edit","tool_input":{"file_path":".env"}}' | python .claude/hooks/protect_files.py` | exit 2, BLOCKED message |
| env ignored | `git check-ignore .env` | prints `.env` |
| Exit gate | both SETUP.md step-12 commands | no output |

- [ ] **Step 5: Fix anything the scratch run exposed**

Apply fixes to the SEED files (not just the scratch copy), rerun the failing check, and commit each fix:

```powershell
git add -A
git commit -m @'
fix: corrections from scratch instantiation run

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
'@
```

- [ ] **Step 6: Clean up and close out**

```powershell
Remove-Item -Recurse -Force $scratch -Confirm:$false
git log --oneline
```
Expected: one commit per task. Report results against all seven acceptance criteria in the final summary, including the criterion-5 adaptation and criterion-6 JSON exception.

---

## Plan Self-Review Notes

- **Spec coverage**: §3→Task 1, §4→Task 2, §5→Task 3, §6→Tasks 4/5/6/9, §7→Tasks 7/8, §8→Task 12, §9→Task 11, §10→Task 10, §11/§12→encoded in file contents (risk mitigations live inside the authored files; deferred items intentionally absent), §13→Task 13.
- **Known deviations from the spec (intentional, report at the end)**: (1) exit-gate grep extended to `.github/` (spec §8 omitted it — ci.template.yml holds `{{}}` slots); (2) JSON files carry no version stamp, tracked via changelog (criterion 6); (3) criterion 5 validated on a minimal TS project instead of a full Next.js app (network/time; profile's Next commands syntax-confirmed in Task 10 Step 1); (4) criterion 3 ("skills load in Claude Code") verified via frontmatter structure checks, not a live skill invocation — live invocation happens on the first real seeded app.
- **Type consistency**: script names `check/test/test:one/fix/dev/build`; env override `HARNESS_CHECK_CMD`; hook exit codes 0/2; ADR pattern `NNNN-<slug>.md`; headings referenced across tasks match Task 2's file verbatim.



