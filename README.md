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
| `harness-kit/`                                                 | THE single user-facing entry point, new or existing app: self-contained, collision-free by name, START-HERE routes to the right checklist, inert merge sources (gitignore.template, gitattributes.template, ci.template.yml). Parity-tested mirror of base/ + the checklists. |
| `harness-kit/ADOPTION.md`                                      | The existing-app (brownfield) checklist: merge, don't overwrite; green `check` before the Stop hook goes live. Lives IN the kit.                |
| `SETUP.md`                                                     | The fresh-repo checklist (root-homed; the kit carries the working copy).                                                                        |
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
| `base/docs/COWORK.md`                                          | The Cowork/claude.ai adapter: project-instructions pointer, CI-as-gate, on-demand skills. Delete if Claude-Code-only.                            |
| `base/.github/workflows/`                                      | CI template: the same gate, warnings-as-errors, full tests, audit.                                                                              |
| base/ dotfiles (`.gitignore`, `.gitattributes`, `.env.example`, `.editorconfig`) | Hygiene from commit #1: secrets pattern, standard ignores, LF line endings, whitespace.                                                          |
| `profiles/typescript-next/`                                    | Pre-filled overlay for TS/Next.js apps.                                                                                                         |
| `tests/`                                                       | Seed-only tests: hook scripts + parity guards (settings, kit) (`python -m unittest discover -s tests`).                                         |
| `.githooks/`                                                   | Seed-only pre-push repo-identity guard (rule + activation: CLAUDE.md -> Repo identity); not copied into apps.                                   |
| `docs/superpowers/`                                            | Specs/plans for the seed itself (not copied).                                                                                                   |

## Instantiation

ONE entry point for both cases: copy the `harness-kit/` FOLDER into the
app's repo root — brand new or already grown — and follow
`harness-kit/START-HERE.md`. Its single fork (does the repo already
contain application code?) routes to SETUP.md (fresh; scaffold first,
overlay a profile if one fits) or ADOPTION.md (existing; same harness,
inverted order). Both kickoff prompts live in START-HERE (their single
home), both checklists are agent-optional, open with a STOP guard for
the opposite case, and delete the kit folder at their end.

`base/` is the canonical SOURCE both paths derive from — the kit is its
parity-tested mirror plus packaging. Nobody copies `base/` into an app;
edits land in `base/` and flow into the kit (tests enforce byte
equality).

Agent or not, the two mechanical gates say when you are done:
`verify_on_stop.py --self-test` and `check_markers.py`.

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
   skills are plain Markdown. The cross-tool instruction file is
   converging on `AGENTS.md`, an open format a broad ecosystem reads —
   OpenAI Codex and Gemini CLI among them, and Antigravity 2.0 too
   (skills under `.agents/skills/`). Gemini CLI also honors its native
   `GEMINI.md`. Claude Code does NOT read `AGENTS.md` natively (as of
   mid-2026).
3. **Claude-Code-bound** — `.claude/settings*.json` (permission syntax,
   hook registration) and the two hooks' stdin protocol
   (`tool_input.file_path`, `stop_hook_active`). The enforcement
   CONCEPTS port; the hook wiring is a rewrite per tool — Gemini CLI
   shares the exit-2-blocks semantics but renames the events
   (`BeforeTool`/`AfterAgent`) and payload fields; Antigravity 2.0 has
   its own JSON hooks. Verify the tool's current hook API when you wire
   it.

**Multi-tool activation recipe (when a real app needs it — not shipped,
YAGNI).** To drive a seeded app from an `AGENTS.md` tool (Codex,
Antigravity, and much of the ecosystem) or Gemini CLI, three moves —
none touch the shared core:

- **Manual:** move `CLAUDE.md`'s content to `AGENTS.md`; leave
  `CLAUDE.md` a one-line `@AGENTS.md` import. One home for the
  invariants, every tool reads it — the one-core rule the Cowork
  adapter already follows.
- **Skills:** already plain Markdown; point the tool at them on demand
  (Antigravity auto-surfaces `.agents/skills/`), never a second copy —
  exactly `docs/COWORK.md` §3.
- **Enforcement:** the Stop/protect hooks are Claude-Code-specific; port
  the concept per tool if it supports one, but **CI is the shared hard
  gate under every tool** — the same agent-independent, unskippable
  backstop that carries Cowork. A tool with zero hook wiring is still
  gated.

Execute this only when a real app drives one of these tools; that run
validates the wiring. Until then the pattern is ready, not carried —
still YAGNI, now with a recipe.

Models are not a portability axis: within Claude Code, Opus, Sonnet, or
any other model shares the same settings, hooks, and skills. Enforcement
is model-independent — weaker instruction-following makes the hooks more
valuable, not less.

**Second surface: Cowork / claude.ai (first-class).** Cowork and
claude.ai/code run on Claude Code's substrate but honor a different subset
of it: they do NOT fire hooks registered in `settings.json`, and they
surface `.claude/skills/` and `CLAUDE.md` less predictably than the CLI.
The harness treats this as a **second adapter over one shared core, not a
second harness** — a second full copy of the invariants or knowledge system
would drift, against Invariant 3. The tool-agnostic core (`CLAUDE.md`,
`docs/`, CI, `check_markers.py`, the six-script contract, the skills as
Markdown) is unchanged; each surface gets thin, non-overlapping wiring:
Claude Code via `.claude/settings.json` (hooks + permissions), Cowork via
`docs/COWORK.md` (a project-instructions pointer that loads the manual,
on-demand skills, CI as the gate). The two coexist on one repo without
collision because they honor disjoint mechanisms — Code fires the hooks and
ignores the Cowork doc; Cowork ignores the hooks and reads it — and the rule
that keeps it safe is the harness's own: an adapter adds wiring, never
restates substance. Honest residual: the two hooks are Claude-Code-only (a
known Cowork limitation, anthropics/claude-code#63360), so under Cowork **CI is
the shared hard gate** and carries enforcement under both; `docs/COWORK.md`
carries the mechanics and full setup.

## Relationship to installed plugins

The harness deliberately does NOT duplicate generic workflows provided by
installed plugins (superpowers' TDD/brainstorming/verification, code-review,
claude-md-management). It ships only skills that encode project-local
contracts. If those plugins are absent, the harness still works — it just
enforces less.

## Upgrading seeded apps

Every copied template carries `template-version: YYYY-MM` (`YYYY-MM.N` for
a patch round within the same month). The guided route: copy a FRESH
`harness-kit/` into the app root — ADOPTION.md's UPDATE MODE detects the
already-adopted harness and walks the version merge (stamp diff, live
wins, delegated harness edits, curated commit). For a single known
change, the light route still works: diff an app's stamp against
`TEMPLATE-CHANGELOG.md`, then port the missing pieces by hand (or with
an agent). The seed is the canonical upstream; apps never edit their
copies expecting it to flow back — improvements land here first.
