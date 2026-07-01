<!--
  ============================================================================
  CLAUDE.md TEMPLATE  (stack-agnostic project guidance for Claude Code / agents)
  ============================================================================

  HOW TO USE:
    1. Copy this file to your repo root as `CLAUDE.md`.
    2. Replace every <PLACEHOLDER> with a real value.
    3. Act on every `> 📝 ADAPT:` note, then delete the note.
    4. Delete this whole comment block and any section you don't need.

  CONVENTIONS:
    <PLACEHOLDER>   — fill in.
    > 📝 ADAPT:     — guidance for tailoring; remove once done.

  Two principles below (Source of Truth, Symbol-Not-Count) are the load-bearing
  lessons this template exists to encode. Keep them even if you cut everything
  else.
  ============================================================================
-->

# CLAUDE.md

Guidance for Claude Code (and other agents) working in this repository.
**These instructions override default behavior — follow them exactly.**

## Role & Context
<ONE-LINE DESCRIPTION OF THE PROJECT AND THE PERSONA THE AGENT SHOULD ADOPT.>
- **Domain**: <e.g. fintech ledger / realtime chat / data pipeline>
- **Stance**: Be concise. Give brutal, honest engineering feedback — reject bad
  patterns and explain why, don't optimize for politeness.

> 📝 ADAPT: State the seniority/persona you want ("Principal X engineer"),
> the one quality bar that matters most here (correctness? latency? safety?),
> and anything the agent must never assume.

---

## ⛔ Critical Invariants (NEVER VIOLATE)

Non-negotiable rules. Breaking one invalidates the task.

### 1. Verification Gate
- **MUST** run `<BUILD/TYPECHECK CMD>` and `<LINT CMD>` after any code change.
- **MUST** reach **0 errors, 0 warnings** before claiming completion.
- **NEVER** suppress a warning without explicit user approval.
- A clean local build does not equal a clean CI build — verify the way CI does
  (`<RELEASE/STRICT BUILD CMD>` or `<CI INVOCATION>`) before claiming "done".

> 📝 ADAPT: e.g. `npm run build && npm run lint && npm test`,
> `cargo build --release && cargo clippy -- -D warnings`,
> `go vet ./... && go test ./...`. List any always-exempt warnings + why.

### 2. Source of Truth (anti-rot)
- **One fact lives in one place.** Link to it; never duplicate it. Duplicated
  facts drift out of sync and start contradicting each other.
- **Never document deleted or merely-planned code as if it exists.** Remove a
  section the moment the thing it describes is removed.

### 3. Cite Symbols, Not Counts or Line Numbers
- Reference **stable symbol names** (a class, function, constant, directory) —
  things a rename would break loudly.
- **Do NOT embed volatile statistics in prose** (file counts, "N modules",
  "42 endpoints", LOC totals) or `path/file:120` line references. They rot
  within weeks and mislead the next agent. Point at the source of truth instead
  ("the handlers in `src/api/`", "the `MAX_*` constant in `config.rs`").

> 📝 ADAPT: This is the #1 reason agent-guidance files become actively harmful.
> Keep this rule verbatim.

### 4. <PROJECT-SPECIFIC INVARIANT>
> 📝 ADAPT: Add the rules unique to YOUR domain that an agent could plausibly
> violate. Examples by domain:
>   - Security/CLI: never pass unsanitized input to a shell/subprocess.
>   - Data/streaming: never buffer the full dataset in memory; stream it.
>   - Money/ledger: never use floats for currency; never mutate a posted entry.
>   - Frontend: never block the UI thread; keep render paths allocation-light.
> Delete this section if you have none — but you almost certainly have at least one.

---

## Tech Stack
| Component | Version | Notes |
|-----------|---------|-------|
| <LANGUAGE> | <VER> | <constraints> |
| <FRAMEWORK> | <VER> | <version-pin reasons, if any> |
| <KEY LIB> | <VER> | <why this one> |

> 📝 ADAPT: List only versions that constrain decisions (a pin you can't break,
> a feature floor). Record *why* a version is pinned — that reasoning is what
> stops a future agent from "helpfully" upgrading and breaking you.

---

## Commands
```bash
<BUILD CMD>          # build / compile / typecheck
<TEST CMD>           # run the test suite
<TEST ONE CMD>       # run a single test (agents need this for tight loops)
<RUN CMD>            # run the app locally
<LINT/FORMAT CMD>    # lint + format
```

---

## Architecture

### Layout
```
<TOP-LEVEL DIRECTORY MAP — one line per major dir, what lives there>
```

### Data / Control Flow
<HOW A REQUEST OR INPUT MOVES THROUGH THE SYSTEM, END TO END.>

### Key Components
- **<ComponentName>** (`<path>`): <responsibility, one line>
- **<ComponentName>** (`<path>`): <responsibility, one line>

> 📝 ADAPT: Describe the seams an agent must respect (layer boundaries, the
> one service that owns X). Name the symbols; resist the urge to write counts.
> If a pattern is non-obvious or easy to get wrong, that's exactly what belongs
> here — obvious things don't.

---

## Project-Specific Gotchas
> 📝 ADAPT: This is the highest-value section over time. Capture each
> hard-won, non-obvious lesson as it's learned — the bug that took a day, the
> API that silently no-ops, the ordering that must hold. Format:
>
> ### <Short title of the trap>
> **The problem**: <what goes wrong, concretely>
> **The rule**: <the pattern that avoids it — with the symbol name involved>
>
> Start empty. Fill it from real incidents, not speculation.

---

## Development Rules
- **Batch related operations** in a single step (file edits, test runs).
- **Plan first** for new features, major refactors, or multi-file changes; ask
  when the approach is unclear.
- **File organization**: never save to repo root; use `<src dirs>`, `tests`,
  `docs`, `scripts`, `config`.
- **Match surrounding code** — its naming, idioms, comment density.

---

## Deep-Analysis Protocol
For complex or high-risk changes (new subsystems, architecture decisions,
performance-critical or security-sensitive paths), run the **UltraThink**
protocol before writing code: `<PATH TO ultrathink.md>`.

> 📝 ADAPT: Drop in the companion ultrathink.template.md (generalized) and point
> here. Skip the protocol for typo/single-file/config changes.
