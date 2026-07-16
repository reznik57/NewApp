<!-- template-version: 2026-07.33 -->

# CLAUDE.md

@AGENTS.md

<!--
  Claude Code compatibility bridge — rename to CLAUDE.md at SETUP step 7,
  unchanged. The import line above is the whole job: Claude Code does not
  read AGENTS.md natively, so this file loads it.

  This bridge stays THIN on purpose. AGENTS.md is the canonical instruction
  home (Invariant 3: one fact, one home) — never copy its invariants,
  architecture, commands or gotchas down here. An unmaintained mirror rots
  into actively wrong guidance while the canon moves on.

  Only Claude-Code-specific DELTAS belong below: things that are true of
  this tool's wiring and of no other. Everything else goes in AGENTS.md.
-->

## Claude-Code-specific wiring

These are mechanics of this tool, not project rules — the rules live in
`AGENTS.md`.

- **Hooks enforce what AGENTS.md instructs.** `.claude/settings.json`
  registers `verify_on_stop.py` (the Verification Gate at the end of a turn)
  and `protect_files.py` (blocks edits to secrets, lockfiles, and the harness
  itself). They are LIVE from the moment `settings.json` exists. Other agent
  tools read `AGENTS.md` and register none of this — there CI is the gate.
- **Skills load from `.claude/skills/`.** Each file there is a bridge to the
  canonical skill in `.agents/skills/`; the substance lives in the canonical
  copy only. Add a Claude-only skill here, never a second copy of one that
  already exists under `.agents/skills/`.
- **Permissions** (`allow`/`ask`/`deny` in `.claude/settings.json`) are an
  accident guard, not a security boundary — see SETUP step 5.
