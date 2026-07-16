# Template New App — a harness for AI-assisted development

The seed folder copied into every new application. Goal: long-term healthy
code with Claude Code — rules that enforce themselves, and knowledge that
compounds instead of evaporating in chat transcripts.

## Philosophy

1. **Instructions are requests; hooks are guarantees.** Every rule that can
   be a hook, config, or CI gate is one. AGENTS.md keeps only judgment calls.
   Enforcement is layered: Stop hook → permissions → CI.
2. **Knowledge compounds.** Decisions land in ADRs (append-only), narratives
   in a lazily-grown wiki, hard-won gotchas in AGENTS.md one-liners — each
   fact in exactly one home (fact-placement law in the AGENTS.md template).
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
| `base/AGENTS.template.md`                                      | THE canonical always-loaded operating manual: invariants, task discipline, standing rules, knowledge schema. Every agent tool reads it.         |
| `base/CLAUDE.template.md`                                      | Claude Code's bridge to it — an `@AGENTS.md` import plus Claude-only wiring. Thin by contract: no substance, nothing to keep in sync.           |
| `base/.agents/skills/ultrathink/`                              | Adversarial design review before complex changes; output saved as an ADR.                                                                       |
| `base/.agents/skills/log-gotcha/`                              | End-of-incident knowledge capture with a graduation rule.                                                                                       |
| `base/.agents/skills/wiki-lint/`                               | Docs health check — dead references, orphans, duplication, leftovers.                                                                           |
| `base/.agents/skills/frontend-design/`                         | The aesthetic floor every constraint profile layers on (vendored upstream, ships with its LICENSE.txt).                                          |
| `base/.claude/skills/`                                         | One discovery bridge per canonical skill — frontmatter plus a pointer. Claude Code reads only this path; the substance lives in `.agents/`.     |
| `base/.claude/settings.template.json`                          | Permission posture + hook registrations. Genuinely Claude-Code-specific — no canonical twin.                                                     |
| `base/.claude/hooks/`                                          | `protect_files.py` (blocks edits to .env/lockfiles/.git and the harness itself), `verify_on_stop.py` (the gate runs before the agent may stop). |
| `base/.claude/scripts/`                                        | `check_markers.py` — the exit gate's single home (run by SETUP step 12 and wiki-lint); fails outright on a missing AGENTS.md.                    |
| `base/docs/adr/`                                               | Decision records (MADR-lite, append-only).                                                                                                      |
| `base/docs/wiki/`                                              | Index + append-only log; pages grow lazily from incidents.                                                                                      |
| `base/docs/specs/`                                             | One-page spec template (threshold: AGENTS.md → Deep-Analysis Protocol).                                                                        |
| `base/docs/COWORK.md`                                          | The Cowork/claude.ai adapter: project-instructions pointer at AGENTS.md, CI-as-gate, on-demand skills. Delete if Claude-Code-only.               |
| `base/.github/workflows/`                                      | CI template: the same gate, warnings-as-errors, full tests, audit.                                                                              |
| base/ dotfiles (`.gitignore`, `.gitattributes`, `.env.example`, `.editorconfig`) | Hygiene from commit #1: secrets pattern, standard ignores, LF line endings, whitespace.                                                          |
| `profiles/typescript-next/`                                    | Pre-filled overlay for TS/Next.js apps (stack profile).                                                                                          |
| `profiles/kids-app/`, `profiles/dense-ui/`                     | Constraint overlays (audience/domain), composable atop a stack profile — see `profiles/README.md`.                                              |
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
2. **Tool-portable, and now shipped that way** — `AGENTS.template.md`'s
   rules and the four skills under `.agents/skills/` are plain Markdown
   in the open formats the ecosystem converged on. `AGENTS.md` is read
   natively by OpenAI Codex, Gemini CLI and Antigravity, which also
   auto-surfaces `.agents/skills/`. Gemini CLI additionally honors its
   native `GEMINI.md`. Claude Code reads neither path (as of mid-2026) —
   which is why the harness ships bridges rather than a second copy:
   `CLAUDE.md` is an `@AGENTS.md` import, and each `.claude/skills/*`
   file is a pointer at its canonical twin. One home per fact, every
   tool served.
3. **Claude-Code-bound** — `.claude/settings*.json` (permission syntax,
   hook registration) and the two hooks' stdin protocol
   (`tool_input.file_path`, `stop_hook_active`). These have no canonical
   twin and are not bridged: they are the genuinely tool-specific layer.
   The enforcement CONCEPTS port; the hook wiring is a rewrite per tool —
   Gemini CLI shares the exit-2-blocks semantics but renames the events
   (`BeforeTool`/`AfterAgent`) and payload fields; Antigravity has
   its own JSON hooks. Verify the tool's current hook API when you wire
   it.

**Driving a seeded app from another tool.** Nothing to activate: layers 1
and 2 are already in the app. Point Codex, Antigravity or Gemini CLI at
the repo and it reads `AGENTS.md` and the canonical skills as they are.
Only enforcement needs a decision — the Stop/protect hooks are
Claude-Code-specific, so port the concept per tool if it supports one, but
**CI is the shared hard gate under every tool**: the same
agent-independent, unskippable backstop that carries Cowork. A tool with
zero hook wiring is still gated.

This replaced a recipe. Until v2.8.0 the seed put its substance in
CLAUDE.md and documented the AGENTS.md move as a manual, unshipped
procedure (YAGNI). Real apps then arrived that needed it, and the honest
reading of the evidence was that the ecosystem had converged while the
seed had not — a recipe every app would eventually run by hand is just a
default with extra steps, and one written down in twenty-five places
drifts in twenty-five ways.

Models are not a portability axis: within Claude Code, Opus, Sonnet, or
any other model shares the same settings, hooks, and skills. Enforcement
is model-independent — weaker instruction-following makes the hooks more
valuable, not less.

**Second surface: Cowork / claude.ai (first-class).** Cowork and
claude.ai/code run on Claude Code's substrate but honor a different subset
of it: they do NOT fire hooks registered in `settings.json`, and they
surface the skills and the manual less predictably than the CLI.
The harness treats this as a **second adapter over one shared core, not a
second harness** — a second full copy of the invariants or knowledge system
would drift, against Invariant 3. The tool-agnostic core (`AGENTS.md`,
`.agents/skills/`, `docs/`, CI, `check_markers.py`, the six-script
contract) is unchanged; each surface gets thin, non-overlapping wiring:
Claude Code via `.claude/settings.json` (hooks + permissions) plus its
`CLAUDE.md` / `.claude/skills/` bridges, Cowork via
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
