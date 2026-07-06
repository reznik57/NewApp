<!-- template-version: 2026-07.16 -->

# Working under Cowork / claude.ai

Cowork and claude.ai/code run on Claude Code's substrate but honor a different
subset of it: they do **not** fire the hooks registered in
`.claude/settings.json`, and they surface `.claude/skills/` and `CLAUDE.md`
less predictably than the CLI. This file is the **Cowork adapter** — the same
job `.claude/settings.json` does for Claude Code, done with the mechanisms
Cowork honors. The harness core (`CLAUDE.md`, `docs/`, CI, the six-script
contract, `check_markers.py`, the skills) is shared and unchanged; only the
wiring below is Cowork-specific. One harness, two adapters — never two
harnesses (a second copy of the invariants or knowledge system would drift,
against Invariant 3).

> **Claude-Code-only project?** Delete this file — an unused adapter just rots.

## 1. Load the operating manual (required)

Cowork does not auto-inject `CLAUDE.md` the way the CLI does, so the invariants
are invisible until you load them. Paste this pointer into the project's
custom instructions (claude.ai → this project → **Instructions**), so every
session picks it up:

    At the start of each session, read and follow this project's CLAUDE.md —
    especially the Critical Invariants and the Verification Gate. Before
    claiming any task done or committing, run the repo's `check` script and
    confirm it is green.

Keep it a **pointer, never a copy**: the rules live in `CLAUDE.md` (one fact,
one home). When `CLAUDE.md` changes, this pointer keeps working untouched.

## 2. Enforcement: CI is the hard gate

Under Claude Code two hooks enforce mechanically — the Stop hook blocks the
agent from stopping on a red `check`, and `protect_files.py` blocks edits to
secrets, lockfiles, and the harness itself. **Neither fires under Cowork** (a
known limitation — anthropics/claude-code#63360). So here:

- **CI is the sole mechanical gate.** It runs server-side, agent-independent,
  and cannot be skipped by the agent. Everything that must hold the line lives
  in CI (`check` → full tests → build → audit) — that is the real backstop.
- **The Verification Gate is a standing instruction**, not a hook — loaded via
  the pointer in §1. The agent is told to run `check` before "done"; CI
  catches it if the agent forgets. This is exactly what Invariant 1 already
  says; Cowork only removes the local hook that also forced it.
- **File protection is advisory.** The guard that blocks edits to `.env`,
  lockfiles, and the harness under Claude Code does not fire here — nothing
  stops such an edit locally, so review the agent's diffs before you commit.

## 3. Skills: invoke on demand

Cowork does not reliably surface `.claude/skills/`, so they will not trigger
themselves. Invoke one by pointing the agent at its file — e.g. "follow
`.claude/skills/ultrathink/SKILL.md` for this design," or run the docs check in
`.claude/skills/wiki-lint/SKILL.md`. Each skill's trigger lives where it
always did — ultrathink's in `CLAUDE.md` (Deep-Analysis Protocol), wiki-lint's
in its own description; only the invocation is manual. Skills that ship
per-app slots (e.g. ultrathink's filled rows) work unchanged, because the
agent reads this app's own copy.

## 4. Permissions are user-mediated

The allow/ask/deny posture in `.claude/settings.json` does not apply under
Cowork; it gates actions through its own approval prompts plus your oversight.
That posture was always an accident guard, not a security boundary (SETUP
step 5), so there is nothing to port — just know the guard here is you.
