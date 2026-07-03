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

| Path                                                           | Job                                                                                                                                             |
| -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `SETUP.md`                                                     | The per-app instantiation checklist (fresh repos). Start here.                                                                                  |
| `ADOPTION.md`                                                  | The existing-app (brownfield) checklist: merge, don't overwrite; green `check` before the Stop hook goes live.                                  |
| `TEMPLATE-CHANGELOG.md`                                        | Seed version history; how seeded apps learn what they're missing.                                                                               |
| `base/CLAUDE.template.md`                                      | The always-loaded operating manual: invariants, task discipline, standing rules, knowledge schema.                                              |
| `base/.claude/settings.template.json`                          | Permission posture + hook registrations.                                                                                                        |
| `base/.claude/hooks/`                                          | `protect_files.py` (blocks edits to .env/lockfiles/.git and the harness itself), `verify_on_stop.py` (the gate runs before the agent may stop). |
| `base/.claude/scripts/`                                        | `check_markers.py` — the exit gate's single home (run by SETUP step 12 and wiki-lint).                                                          |
| `base/.claude/skills/ultrathink/`                              | Adversarial design review before complex changes; output saved as an ADR.                                                                       |
| `base/.claude/skills/log-gotcha/`                              | End-of-incident knowledge capture with a graduation rule.                                                                                       |
| `base/.claude/skills/wiki-lint/`                               | Docs health check — dead references, orphans, duplication, leftovers.                                                                           |
| `base/docs/adr/`                                               | Decision records (MADR-lite, append-only).                                                                                                      |
| `base/docs/wiki/`                                              | Index + append-only log; pages grow lazily from incidents.                                                                                      |
| `base/docs/specs/`                                             | One-page spec template (threshold: CLAUDE.md → Deep-Analysis Protocol).                                                                         |
| `base/.github/workflows/`                                      | CI template: the same gate, warnings-as-errors, full tests, audit.                                                                              |
| base/ dotfiles (`.gitignore`, `.env.example`, `.editorconfig`) | Hygiene from commit #1: secrets pattern, standard ignores, whitespace.                                                                          |
| `profiles/typescript-next/`                                    | Pre-filled overlay for TS/Next.js apps.                                                                                                         |
| `tests/`                                                       | Seed-only tests: hook scripts + base↔profile settings parity (`python -m unittest discover -s tests`).                                          |
| `docs/superpowers/`                                            | Specs/plans for the seed itself (not copied).                                                                                                   |

## Instantiation

Copy `base/*` (including dotfiles) into the new repo → overlay a profile if
one fits → work through `SETUP.md` top to bottom → its exit gate greps for
leftover `{{PLACEHOLDER}}`/`ADAPT:` markers. For an app that already has
code, follow `ADOPTION.md` instead — same harness, inverted order.

## When not to use this seed

Throwaway spikes and hackathon prototypes don't get a harness — discipline
you plan to discard is waste. The rule that keeps this safe: a spike never
graduates to production by accident. If a prototype earns a future, re-seed
fresh from this template and port the spike's code over piece by piece,
through the gate.

## Portability (other agent harnesses, other models)

Three layers, decreasingly portable:

1. **Tool-agnostic** — `docs/` (ADR/wiki/specs), the dotfiles, CI, the
   six-script contract, and `check_markers.py` are plain git/npm/CLI;
   they work under any agent, or none.
2. **Concept-portable** — CLAUDE.template.md's rules and the three
   skills are plain Markdown. Antigravity 2.0 reads the same content as
   `AGENTS.md` (skills under `.agents/skills/`), Gemini CLI as
   `GEMINI.md`. Claude Code does NOT read AGENTS.md natively (as of
   mid-2026); if multi-tool use becomes real, the known pattern is:
   content moves to `AGENTS.md`, `CLAUDE.md` becomes a one-line
   `@AGENTS.md` import shim. Not done speculatively — YAGNI.
3. **Claude-Code-bound** — `.claude/settings*.json` (permission syntax,
   hook registration) and the two hooks' stdin protocol
   (`tool_input.file_path`, `stop_hook_active`). Gemini CLI's hook
   system shares the exit-2-blocks semantics but renames the events
   (`BeforeTool`/`AfterAgent`) and payload fields; Antigravity 2.0 has
   its own JSON hooks. The enforcement CONCEPTS port; the wiring is a
   rewrite per tool.

Models are not a portability axis: within Claude Code, Opus, Sonnet, or
any other model shares the same settings, hooks, and skills. Enforcement
is model-independent — weaker instruction-following makes the hooks more
valuable, not less.

## Relationship to installed plugins

The harness deliberately does NOT duplicate generic workflows provided by
installed plugins (superpowers' TDD/brainstorming/verification, code-review,
claude-md-management). It ships only skills that encode project-local
contracts. If those plugins are absent, the harness still works — it just
enforces less.

## Upgrading seeded apps

Every copied template carries `template-version: YYYY-MM` (`YYYY-MM.N` for
a patch round within the same month). Diff an app's
stamp against `TEMPLATE-CHANGELOG.md`, then port the missing pieces by hand
(or with an agent). The seed is the canonical upstream; apps never edit
their copies expecting it to flow back — improvements land here first.
