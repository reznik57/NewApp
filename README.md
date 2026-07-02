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

| Path                                  | Job                                                                                                                      |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `SETUP.md`                            | The per-app instantiation checklist. Start here.                                                                         |
| `TEMPLATE-CHANGELOG.md`               | Seed version history; how seeded apps learn what they're missing.                                                        |
| `base/CLAUDE.template.md`             | The always-loaded operating manual: invariants, task discipline, standing rules, knowledge schema.                       |
| `base/.claude/settings.template.json` | Permission posture + hook registrations.                                                                                 |
| `base/.claude/hooks/`                 | `protect_files.py` (blocks edits to .env/lockfiles/.git), `verify_on_stop.py` (the gate runs before the agent may stop). |
| `base/.claude/skills/ultrathink/`     | Adversarial design review before complex changes; output saved as an ADR.                                                |
| `base/.claude/skills/log-gotcha/`     | End-of-incident knowledge capture with a graduation rule.                                                                |
| `base/.claude/skills/wiki-lint/`      | Docs health check — dead references, orphans, duplication, leftovers.                                                    |
| `base/docs/adr/`                      | Decision records (MADR-lite, append-only).                                                                               |
| `base/docs/wiki/`                     | Index + append-only log; pages grow lazily from incidents.                                                               |
| `base/docs/specs/`                    | One-page spec template for >2-module or irreversible changes.                                                            |
| `base/.github/workflows/`             | CI template: the same gate, warnings-as-errors, full tests, audit.                                                       |
| `profiles/typescript-next/`           | Pre-filled overlay for TS/Next.js apps.                                                                                  |
| `tests/`                              | Seed-only tests for the hook scripts (`python -m unittest discover -s tests`).                                           |
| `docs/superpowers/`                   | Specs/plans for the seed itself (not copied).                                                                            |

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
