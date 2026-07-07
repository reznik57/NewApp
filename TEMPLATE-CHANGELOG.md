# Template Changelog

Seed version history (upgrade procedure: README → Upgrading seeded apps).
JSON templates (settings.template.json, profile settings.json,
package-scripts.json) cannot carry comment stamps — their version is
tracked only here.

## 2026-07.20 — v2.6.1

Second backflow from fisi-learning: its first session with live hooks hit
two Windows bugs in verify_on_stop.py. Both were fixed in the app the same
day (under explicit user delegation — the hook path is protect_files-
guarded) and transferred here so no future app inherits them.

- verify_on_stop.py (base + kit, stamp 2026-07.20) decodes the check's
  output as UTF-8 (`encoding="utf-8", errors="replace"`): with `text=True`
  and no encoding, the pipe was decoded with the Windows locale (cp1252) —
  vitest's UTF-8 marks killed the subprocess reader threads, the
  diagnostic tail was lost, and a filled pipe buffer could flip a green
  check into a bogus exit 1.
- verify_on_stop.py canonicalizes its cwd (`os.chdir(os.path.realpath(
  os.getcwd()))`) before running the check: launched from a lowercase
  drive letter (d:\..., as inherited from a VS Code workspace), Vitest
  keys module identities case-sensitively and every suite dies at
  describe() ("reading 'config'") before collecting a single test.
- tests/hooks/test_verify_on_stop.py: regression guards for both — raw
  UTF-8 tail survival under a pinned legacy codec, and the check command
  observing a canonical-case cwd; each verified to FAIL against the
  pre-fix hook. run_hook() gains an env_overrides parameter.

## 2026-07.19 — v2.6.0

First-run backflow: the SETUP fresh-app path ran for real for the first
time (fisi-learning, Next.js 16, typescript-next profile — 12/12 steps,
exit gate green) and an adversarially verified audit of the run produced
15 confirmed findings (5 high / 8 medium / 2 low; plan doc
2026-07-07-v2.6.0-first-run-backflow.md). Everything template-shaped
folds back here; the app itself was hardened the same day.

- SETUP gains **step 0 — Discovery**: interview before anything is
  scaffolded (purpose, users, data/persistence, platform/offline, auth,
  integrations, GitHub, Cowork), stack settled only AFTER the answers,
  premarked recommendations forbidden, delegation recorded honestly,
  answers routed to named homes (steps 3/7/9/10). The observed failure:
  the stack recommendation was premarked in the same question round that
  first asked what the app IS; ADR-0001 then rationalized it circularly
  ("profile exists" as decisive) and invented a never-stated requirement.
  Three skip-anchors (step 0 first; step 2: profiles never justify a
  stack; step 9 flags an ADR invented from scratch). Existing step
  numbers deliberately unchanged — cross-refs in ADOPTION/profile stay
  valid.
- SETUP header ties the paste-prompt's "ask me at every decision point"
  to step 0 + inline **ASK** markers (steps 0/2/7/11); closing
  **GitHub note**: setup is complete only when origin exists, the first
  push is up and the ci.yml run went green (the fisi run ended "done"
  with CI that had never parsed).
- Kit ships **gitattributes.template** (source base/.gitattributes, an
  inert RENAMED merge source like gitignore.template): with
  core.autocrlf=true and no .gitattributes, six fisi files were CRLF on
  disk right after setup and a branch switch re-materialized more —
  prettier --check then fails repo-wide, disguised as a formatting
  problem. SETUP step 1 distributes it, step 11 carries the CRLF-warning
  tripwire. Root .gitattributes pins harness-kit/** and /SETUP.md so the
  parity-tested mirror pairs materialize identically on Windows.
- SETUP step 1 covers the second scaffolder failure mode (invalid
  package name: spaces/capitals → sibling temp dir, kebab-case, move
  dotfiles too; the fisi agent had to improvise this in D:\tmp) and the
  scaffold-generated instruction files (scaffold CLAUDE.md yields to the
  kit template; AGENTS.md survives only WIRED — fisi's lay unloaded, its
  Next-16 warning reaching no session).
- Profile typescript-next: ships **vitest.config.ts** (Vitest reads no
  tsconfig paths — the first `@/*`-alias test failed resolution while
  tsc stayed green); the vitest config and the devDependencies install
  become numbered steps 7/8 and the script-collision rule (profile wins;
  scaffold `lint` dies, `start` stays) lands in step 1 — devDeps and the
  first test were prose the numbered path never reached (SETUP said
  "steps 1–5" while the README had 6 coupled steps; now "ALL numbered
  steps"); README head no longer instructs the
  retired copy-base/*-flow; ci.yml comment no longer leaks a dead base/
  path into apps. Re-stamped 2026-07.19 (README, ci.yml,
  vitest.config.ts).
- CLAUDE.md budget: ~160 was structurally unreachable on the profile
  path (bare template ~167 post-deletion; fisi shipped at 188) and
  hard-coded twice. Now ~190 with wiki-lint as its single home (SETUP
  step 7 defers there); findings must name the concrete overflowing
  blocks. wiki-lint re-stamped 2026-07.19.
- START-HERE's SETUP paste prompt carries a seed-path placeholder;
  SETUP step 2 says ASK for the seed's location, never scan drives (the
  fisi agent enumerated all of D:\ and guessed by name similarity, with
  "Template New App - Kopie" sitting right there).
- SETUP step 7 also replaces the scaffold's boilerplate README (fisi
  committed one with a dead `app/page.tsx` path and yarn/pnpm/bun advice
  against the npm-fixed harness).

Rejected, with reason (don't relitigate): renumbering SETUP steps for a
"cleaner" discovery phase (cross-reference rot is exactly the class the
"steps 1–5" finding documents; step 0 preserves every number); a
numbered-cross-reference lint test (the "ALL numbered steps" wording
removes the rot class at the source — revisit on a second incident); a
second profile to de-bias the stack choice (graduation rule stands:
profiles graduate from real apps); discovery enforcement in the exit
gate (check_markers checks markers, not meaning; the three step-0
anchors are the proportionate guard).

## 2026-07.18 — v2.5.2

Test-suite hardening only — no template content changes, so no stamp
advances. Closes the guard gap the v2.5.0 round exposed: root-singleton
docs (README.md, TEMPLATE-CHANGELOG.md, and the KIT_ONLY
harness-kit/ADOPTION.md + START-HERE.md) had no byte-twin in the kit
parity manifest, so no test read their content — README.md shipped
truncated (whole "Upgrading seeded apps" section gone) with a green
suite.

- New tests/hooks/test_root_docs.py: per-doc load-bearing anchors
  (ASCII-only), trailing-newline check, 500-byte size floor, and a
  15-entry changelog floor. In-memory fixture tests prove the checker
  flags both v2.5.0 truncation signatures (dropped section, lost
  trailing newline); live-doc tests pin the four real docs. Suite:
  58 -> 64 tests.
- Deliberate friction: restructuring a guarded doc now requires
  updating REQUIRED in the same commit.

Rejected, with reason (don't relitigate): end-of-file "mid-sentence"
heuristic (v2.5.0 truncation ended on a period — it would not have
fired); a general cross-reference-integrity engine (more code, only
guards referenced content; the one cited section is already an anchor).
Design: docs/superpowers/specs/2026-07-06-root-docs-guard-design.md.

## 2026-07.17 — v2.5.1

Multi-tool readiness as a recipe, not shipped wiring — README Portability
only; base/ templates untouched, so no stamp advances (suite unchanged: 58,
1 env-gated skip). Future-proofing for the AGENTS.md ecosystem (Codex,
Antigravity, Gemini CLI, and more) without reversing the section's own YAGNI
stance.

- README Portability layer 2 sharpened: the cross-tool instruction file is
  converging on AGENTS.md — an open standard a broad ecosystem reads
  (verified via agents.md: OpenAI Codex and Gemini CLI among them;
  Antigravity per the prior note). Claude Code does not read it natively
  (mid-2026).
- Layer 3: enforcement concepts port, hook wiring is a rewrite per tool;
  added "verify the tool's current hook API when you wire it" — the
  specifics move fast.
- New "Multi-tool activation recipe": three core-neutral moves (CLAUDE.md
  content -> AGENTS.md + a one-line @AGENTS.md shim; skills on-demand; CI as
  the shared hard gate under every tool, the same backstop that carries
  Cowork). Executed only when a real app drives one of these tools; ready,
  not carried.

Rejected, with reason (don't relitigate): shipping docs/CODEX.md +
docs/ANTIGRAVITY.md adapters now (Cowork-style, approach C). Blind and
unvalidated against the real tools, reverses the documented YAGNI stance for
zero current users, touches the core (instruction-loading forces a CLAUDE.md
shim), and adds two root-only docs the kit-parity net does not guard. The
recipe captures the pattern; a real app later validates the wiring.

## 2026-07.16 — v2.5.0

Cowork / claude.ai promoted from a degraded-mode caveat to a first-class
second surface: one shared core, two adapters — never two harnesses (a second
copy of the invariants or knowledge system would drift, against Invariant 3).
v2.4.9 documented Cowork as advisory-plus-CI in the README; this ships the
wiring, an honest enforcement story, and a manual that reads correctly on both
surfaces.

- New `base/docs/COWORK.md` (mirrored to the kit) — the Cowork adapter, the
  twin of `.claude/settings.json`: a project-instructions pointer that loads
  CLAUDE.md (Cowork does not auto-inject it), CI as the sole hard gate (hooks
  don't fire — anthropics/claude-code#63360), on-demand skill invocation, and
  a user-mediated-permissions note. Pointer-only, no substance duplicated
  (Invariant 3); ships ready-to-use (no `{{}}`/`ADAPT:` markers) and carries
  its own "delete if Claude-Code-only".
- CLAUDE.template.md Invariant 1 reworded surface-neutral: under Claude Code
  the Stop hook enforces mechanically; where no hook fires (e.g. Cowork) it
  stands as an instruction, with CI as the backstop. Stamp -> 2026-07.16.
- README Portability: the same-vendor paragraph rewritten from "loses the top
  two rungs / advisory-plus-CI mode" to the one-core-two-adapters model, with
  the honest residual (the two hooks stay Claude-Code-only; CI is the shared
  hard gate). New Map row for `base/docs/COWORK.md`.
- SETUP / ADOPTION / START-HERE gain an optional, unnumbered Cowork wiring
  note — deliberately not renumbered, since the hooks' docstrings,
  check_markers, and ADOPTION all cite "SETUP step N".

Supersedes v2.4.9's "documented, not mechanized — keep the per-tool caveat out
of Invariant 1." Correct while Cowork was an afterthought; once it is
first-class, the most-read file asserting "the Stop hook enforces this" is a
live falsehood for half its readers, not portability trivia. The reword is
surface-neutral (mechanical where the runtime supports it, CI as backstop), so
it states a truer general principle rather than adding per-tool bloat; the
operational how-to still lives in docs/COWORK.md, not CLAUDE.md
(fact-placement law).

Rejected, with reason (don't relitigate):
- Packaging the skills as an installable plugin so they auto-surface under
  Cowork. Gives a second home for skill content (drift vs. Invariant 3),
  cannot carry the per-app `{{}}` fills (ultrathink Phase 2/5) that on-demand
  invocation reads straight from the app's own copy, and adds the product
  coupling the harness avoids. On-demand invocation (COWORK.md section 3)
  keeps one home and the fills.
- Seeding the invariants into Cowork memory. Wrong scope (space-wide, not
  per-repo) and a second, drifting copy of the rules; the pointer loads the
  one home instead.
- A third, Cowork-only checklist. The optional notes on SETUP/ADOPTION cover
  it without a new entry point.

Re-stamped 2026-07.16: base/CLAUDE.template.md (+ kit mirror). New:
base/docs/COWORK.md (+ kit mirror). Updated, no stamp carried: README.md,
SETUP.md (+ kit mirror), harness-kit/ADOPTION.md, harness-kit/START-HERE.md.
Suite: green — 58 tests, 0 failures, 1 skipped (the symlink case in
test_protect_files.py, environment-gated; 0 skipped where symlinks resolve).

## 2026-07.15 — v2.4.9

Cowork / hook-less-agent portability note — README only; base/ templates
untouched, so no stamp advances (suite unchanged: 58, 1 skipped).

- README Portability gains the same-vendor edge case: Claude Cowork and
  claude.ai/code run on Claude Code's substrate but do NOT fire hooks
  registered in settings.json, and surface a project's .claude/skills/
  less predictably than the CLI. Under them the enforcement ladder loses
  its top two rungs (Stop gate + protect_files guard → advisory) and CI
  is the sole hard backstop; layers 1–2 (knowledge system, dotfiles,
  check_markers.py, six-script contract, on-demand skills) carry
  unchanged, and Invariant 1's gate stays a standing instruction, only
  un-hooked. The harness is fully usable under Cowork in advisory-plus-CI
  mode.
- Documented, not mechanized: there is nothing to enforce here that CI
  does not already, and per the fact-placement law a per-tool enforcement
  difference lives in README Portability (alongside the Antigravity /
  Gemini CLI notes), not in CLAUDE.md.
- Rejected, with reason (don't relitigate): a per-tool caveat inside
  CLAUDE.template.md Invariant 1 ("the Stop hook enforces this — except
  where no hook fires"). It bloats the most-read file with portability
  trivia the README already owns, and Invariant 1 is already a standing
  instruction independent of the hook — Cowork changes nothing about what
  it tells the agent to do, only whether a hook also forces it.

## 2026-07.14 — v2.4.8

Visual-design guidance seam + profile-scoped skill bundle. The TS/Next
profile gated UI *behavior* (four states, server-side validation) and
*accessibility* (jsx-a11y as `check` errors) but said nothing about
layout, typography, spacing, or color — the one profile that by definition
ships a visible frontend had no home for "make it not read as templated
defaults." Aesthetics aren't gate-able, so the "mechanize only what a gate
can prove" doctrine correctly kept hard rules out; what was missing was the
*pointer* to where such judgment lives, and the skill it points at.

- CLAUDE.stack-sections.md gains a third Stack Rule: a workflow pointer,
  not a style rule. It names the boundary explicitly — accessibility is
  mechanized (jsx-a11y fails `check`), visual design is not and carries no
  rule — then points UI work at the `frontend-design` skill. Mirrors the
  ultrathink Deep-Analysis Protocol pointer; honors the Standing Rules "no
  style rules in CLAUDE.md" line by staying guidance, not a rule.
- frontend-design is now bundled *by the profile*, not the core kit:
  profiles/typescript-next/skills/frontend-design/ (SKILL.md + LICENSE.txt,
  vendored byte-for-byte from claude-plugins-official, Apache-2.0). README
  step 6 copies it into .claude/skills/ during overlay. Chosen over a core
  bundle because base/ ↔ harness-kit/ parity is byte-exact — a kit skill
  MUST also live in base/ and would then ship to every app, including
  CLI/lib/data ones with no frontend. Profile-scoping keeps the skill with
  the one stack that has a UI, matching the kit's own "except optional
  profiles" caveat; profiles sit outside the parity manifest, so no test
  churn. The pointer therefore drops its "if available" hedge — post-overlay
  the skill is present. The vendored copy drifts from upstream by design;
  its version is tracked here (like the JSON templates), not by a stamp. A
  scoped `.gitattributes` pins these files to `eol=lf` so `core.autocrlf` on
  Windows can't rewrite the working copy away from the upstream bytes.
- Reliability is invocation, not presence: a bundled skill is auto-surfaced
  to the model, but the model still *decides* to call it — no hook forces
  it. So the pointer is imperative ("invoke … BEFORE writing component
  code," mirroring the ultrathink protocol), not a soft suggestion. Going
  *global* (core bundle) was considered and rejected: it would add the
  skill to every app but NOT change whether it fires for a GUI app — the
  skill sits in that app's `.claude/skills/` either way and the model
  judges identically — so it buys scope-creep (frontend skill in every
  CLI/lib/data app) with zero trigger gain. README steps 5 (pointer) and 6
  (skill) are now cross-linked "do both or neither," so a partial overlay
  can't leave a dead pointer.

Re-stamped 2026-07.14: profiles/typescript-next/CLAUDE.stack-sections.md,
profiles/typescript-next/README.md.

## 2026-07.13 — v2.4.7

Static audit of the SETUP fresh-app path — the one route never run on a
real app (all prior validation was brownfield ADOPTION). Done inline (the
5-lens adversarial workflow hit the account session limit mid-run, so the
findings are inline-verified against the files, not workflow-cross-checked).
Most of the path is sound: every referenced artifact exists, the hook
commands and the `--self-test` OK-path check out (package.json is required
only for `npm run` segments — correct), and the settings.json handshake
between SETUP step 5 and the TS/Next profile holds both ways. Three fixes,
all on the fresh + profile path:

- SETUP step 3 gains the repo-identity guard ADOPTION step 1 already has:
  `git remote -v` must be empty or the app's own repo, never the
  template/seed — a fresh app scaffolded inside a seed clone inherits the
  seed's `origin` (the documented push-onto-template incident, now guarded
  on the greenfield path too).
- profiles/typescript-next/README.md step 5 no longer says to edit
  "CLAUDE.md" at overlay time (SETUP step 2) — the file is still named
  CLAUDE.template.md until SETUP step 7 renames it; the step now says so in
  place.
- profiles/typescript-next/README.md step 3 now tells you to DELETE the
  leftover .github/workflows/ci.template.yml after copying the profile
  ci.yml — GitHub parses every *.yml there and check_markers scans .github/
  (ci.template.yml is not EXEMPT), so a leftover fails both; the exit gate
  already catches it, this just saves the red round-trip.

Re-stamped 2026-07.13: profiles/typescript-next/README.md. SETUP.md carries
no stamp (process doc, versioned only here).

## 2026-07.12 — v2.4.6

Run-4 close — findings from the first UPDATE run: a newer `harness-kit/`
re-dropped on an already-adopted app (a Node games repo, harness already
live from an earlier kit). ADOPTION.md only knew first-adoption, so the
agent had to invent the whole update path — stamp diff, live-wins merge,
delegated harness edits, curated blob staging. The generic mechanics held
(11/11, both guards fired live); the four findings all cluster at the
update seam the checklist never named:

- ADOPTION.md gains an **UPDATE MODE** block at the top: detected by
  `.claude/hooks/verify_on_stop.py` already existing, it collapses the full
  run to stamp-diff → live-wins merge → delegated harness edits → curated
  exit. START-HERE.md now routes an already-adopted app down the same
  ADOPTION.md door instead of implying only greenfield-vs-brownfield.
- Hooks-are-live doctrine, carried from run-3 into UPDATE mode: the harness
  blocks agent edits to itself from move one (no green window — unlike first
  adoption, where step 5 activates the hooks last). A harness-file update is
  therefore the ask-the-user / explicit-delegation case: batch the edits and
  have the user apply or delegate them (a scripted `cp` from the kit), never
  a silent bypass.
- **Stamp-survives-fill**: SETUP steps 7 and 10 now state the
  `template-version:` line outlives the fill — deleting "the header comment
  block" must not take the stamp with it, or "Upgrading seeded apps" has
  nothing to diff. ci.template.yml re-stamped 2026-07.12 with the stamp
  visually split from the ADAPT prose plus a keep-it note; ADOPTION step 6
  inherits the rule through its SETUP-step-7 pointer.
- **Shared-file rule** (ADOPTION step 11): one file that mixes WIP and
  adoption content (a `docs/wiki/log.md` carrying both an app entry and the
  harness-update entry) can't be split by path — DEFAULT is the user commits
  their WIP first, so the adoption commit is clean; hand-crafting a partial
  blob (`git hash-object`) to stage only the adoption lines is a deliberate
  exception, not the norm.

Re-stamped 2026-07.12: ci.template.yml. ADOPTION.md, START-HERE.md, and
SETUP.md carry no stamp (process docs, versioned only here).

## 2026-07.11 — v2.4.5

Run-3 close — findings from the third brownfield adoption (PCAP
.NET 10/Avalonia, ~420K LOC): the first non-Node stack, the first app
with a rich pre-existing harness (own CLAUDE.md/agents/skills/CI), and
the first exit gate run on a cp1252 Windows console. The generic
mechanics held (11/11 steps, both guards fired correctly live); the
findings cluster at exactly those three new edges. Touched templates
stamped 2026-07.11:

- check_markers.py, two defects: (1) printing a hit line containing an
  emoji crashed on cp1252 consoles — a crashed gate exits 1 like a red
  gate but without the list; stdout is now reconfigured to utf-8 with
  errors=replace, making the "Windows-safe" promise cover output too.
  (2) `${{` no longer counts as a marker: GitHub Actions expressions
  live in the scanned .github/. Handled in the marker logic, NOT as a
  path exemption, so an unfilled {{SLOT}} in ci.yml still fails —
  test-pinned in both directions.
- ADOPTION step 5 no longer claims hooks bind "only the NEXT session":
  the run proved PreToolUse live in the SAME session it was activated.
  New doctrine: treat hooks as potentially LIVE the moment
  settings.json is written; never plan a harness edit on the
  assumption of a grace window.
- ADOPTION step 8 + the CI template's audit step get the
  red-on-adoption-day path: run the audit locally BEFORE wiring it;
  red today with the fix deferred → wire the step non-failing plus a
  `deferred` log entry naming the trigger that turns it hard again
  (step 4's ratchet doctrine, applied to audit). Never day-one-red CI,
  never silent yellow — the log entry is the difference.
- ADOPTION step 6, second-instruction-file doctrine sharpened: when
  other tools actively read AGENTS.md/GEMINI.md, the surviving shape
  is tool delta + compact invariant summary + pointer. The duplicated
  detail substance must go — the run found an unmaintained AGENTS.md
  mandating "NO lazy loading" against the app's real hybrid
  architecture: mirrors rot into actively WRONG guidance. Also named:
  the merge DIRECTION is a judgment call — an existing CLAUDE.md
  substantially richer than the template stays base, and the
  template's load-bearing pieces graft in.
- ADOPTION steps 1+11, dirty-tree curation: snapshot
  `git status --short` at step 1; a dirty tree means the adoption
  commits on a dedicated branch, staging ONLY adoption paths checked
  against that baseline (the run had 169 unrelated WIP files plus
  pre-existing modifications inside .claude/ that path-based staging
  would have swept in). Never `git add -A`.
- ADOPTION step 11 + protect_files docstring name the sanctioned
  escape hatch: the guard blocking a late harness edit is the
  ask-the-user case working as designed — the user applies the edit
  or explicitly delegates it; Bash is deliberately unmatched (the
  guard is friction plus forced user involvement, not a security
  boundary); never a silent bypass.
- protect_files.py grows `--probe <path>`: setup-time seam with the
  hook's exact exit contract (2 blocked / 0 allowed). Replaces
  hand-built stdin JSON, where a payload typo hits the fail-open path
  and reads as "allowed". SETUP step 6 and ADOPTION step 5 use it; the
  live .env probe in a fresh session still verifies registration.
- CLAUDE.template Commands ADAPT: stacks with two strictness tiers
  (Debug/Release builds, dev/prod lint) map `check` to the fast
  lenient tier and `build` to the strict one CI runs — the same
  command for both makes the gate too slow or CI too lax.
- .env.example header: an app that doesn't auto-load .env documents
  its REAL process env vars instead and says so in the header — an
  aspirational example the app never reads misleads agents.

Rejected, with reasons (don't relitigate):

- Blanket EXEMPT of .github/workflows/ (the run's improvised fix):
  would pass unfilled ci.yml slots silently; the in-logic `${{` fix
  is strictly better.
- Scanning only git-tracked files: untracked template relics mislead
  agents just as much (agents read the filesystem, not the index);
  the crash was the bug, not the scan scope.
- Matching Bash in protect_files: brittle (quoting, heredocs,
  variables) and unclosable in principle — documented intent instead.
- More rm deny variants (`rm -r` after `rm -rf`): the posture is an
  accident guard by design; the variant chase is unbounded and would
  block legitimate cleanup.
- Git micro-lessons in the checklist (pathspec abort aborts the whole
  `git add`; tracked-aware delete): generic git knowledge, agents
  recover in one step; checklists that teach git grow without end.
- A dotnet profile from a single run: the graduation rule holds (wait
  for the second .NET app); the two-tier principle was adopted
  instead.

(Suite: 58, 1 skipped.)

## 2026-07.10 — v2.4.4

Single-entry round — the pick-the-wrong-folder error class is removed
structurally instead of warned about (kit structure and seed docs
only; base/ templates untouched, so no stamp advances):

- copyfolder/ → harness-kit/: direction-neutral (the kit now serves
  BOTH instantiation paths) and still collision-proof by name (a bare
  kit/ is plausible inside real apps; harness-kit/ is not).
- ONE user-facing entry point: copy harness-kit/ into ANY app's repo
  root; START-HERE routes via a single fork — does the repo already
  contain application code? — to ADOPTION (yes) or SETUP (no), with a
  `git ls-files` tiebreaker. Both kickoff prompts live in START-HERE
  (single home); README's Instantiation shrinks to a pointer. base/
  is never copied into an app anymore — it is the canonical source
  the kit mirrors (parity-tested), stated as such in the README.
- SETUP now works from inside the kit, as ADOPTION always did:
  step 1 becomes scaffold-first-then-distribute (a scaffolder that
  balks at the kit folder → move it aside, scaffold, move it back;
  gitignore.template → .gitignore and ci.template.yml →
  .github/workflows/ land by rename), step 2 notes profiles stay
  seed-side, step 11 deletes the kit before the first commit. The
  robocopy-from-base instruction leaves the user path.
- STOP guards, belt to the router's suspenders: both checklists open
  with a guard for the opposite case (ADOPTION on a code-less repo,
  SETUP on a repo with application code), so a wrong pick fails at
  step 0, not at step 8.
- check_markers.py needed no change: SCAN_TOPS never scanned the kit
  folder, so the exit gate ignores it under either name.
- Parity test renamed test_copyfolder_parity.py → test_kit_parity.py;
  manifest comments and re-sync commands updated (suite: 52,
  1 skipped). The fresh-app path remains unvalidated — first real
  SETUP run doubles as its validation.

## 2026-07.9 — v2.4.3

Unknowns round — mapping "Know your unknowns" (Thariq Shihipar's "The
Unreasonable Effectiveness of HTML", 2026) against the seed. Its frame
(Johari quadrants × pre/during/post implementation) confirms the
harness's coverage of execution unknowns (gates/hooks) and memory
unknowns (knowledge schema); three small adoptions close the
intent-phase flank (touched templates stamped 2026-07.9):

- ultrathink Phase 0: clarifying questions are asked in blast-radius
  order — the answer that could invalidate the most downstream design
  (or is hardest to reverse) comes first. The 1–2 question cap and the
  skip rule are unchanged.
- ultrathink CHECKPOINT: tweakables first — the plan-mode presentation
  opens with the decisions the user is most likely to want differently
  (schema shape, naming, user-facing placement); the mechanical rest is
  compressed. Approval is the gate; reviewer attention is what it
  spends.
- ultrathink Phase 4 + wiki log: deviations are data. The moment
  execution forces a change to an approved step or the ADR, a
  `deviated` line lands in docs/wiki/log.md (new verb, symmetric with
  v2.1's `deferred`) — never reconstructed at session end; the standing
  /log-gotcha sweep graduates the durable ones. ADR-contradicting
  deviations follow the existing ADR discipline.
- Rejected with reasons (don't re-litigate): HTML artifacts as seed
  content (portability layer 1 is plain markdown; a session-level
  practice, not a project contract), buy-in doc and merge quiz (team
  artifacts / no incident evidence — the graduation rule waits for
  one), a standalone blindspot-pass step (duplicates Phase 0 plus
  "Verify, don't invent").

## 2026-07.8 — v2.4.2

Second live adoption round (deliberately-no-build node tool with
committed dist/standalone.html and a v1-era vendored template line):

- protect_files.py: binary-suffix block by DEFAULT (stamped
  2026-07.8) — the graduation rule applied to the seed itself:
  both live adoptions needed the same class (workbooks/DB, then
  png/pdf masters). A text Edit/Write into a binary is always
  corruption, wherever the file lives — suffix rule beats path
  lists; ADAPT extends it with app-specific formats. 3 new tests
  (suite: 52, 1 skipped).
- ADOPTION step 3: a template .gitignore pattern that would untrack
  something the app ships on purpose is SKIPPED, with a one-line
  why-comment in .gitignore so no future cleanup "fixes" it (the
  committed-dist case).
- ADOPTION step 4: runner already in use but no manifest → a
  minimal scripts-only package.json ("private": true, no deps)
  beats a bespoke CHECK_COMMAND mapping; record the no-build intent
  in ADR-0001.
- ADOPTION step 1: vendored copies of an older template line get
  RETIRED, not merged — the seed is the only upstream.
- ADOPTION step 5: a deny that breaks a documented app workflow
  (gotcha citing curl for local verification) moves to ask — the
  guard stays, the workflow survives.
- ADOPTION step 6: loose narratives under docs/ move into
  docs/wiki/ with index entries; process history (old plans/specs
  folders) stays put — knowledge gets indexed, history doesn't.

## 2026-07.7 — v2.4.1

Adoption-kit round — seed structure only; base/ templates untouched,
so no stamp advances. Battle-tested the same day against the first
real brownfield adoption (13 findings, six fix rounds):

- copyfolder/ is the self-contained, SINGLE-USE adoption kit: copied
  as a FOLDER into the app (collision-proof by name — nothing to
  skip or overwrite), distributed by the checklist (step 2 moves app
  material to its places; scaffolding stays inside), deleted whole
  at step 11. Ships both checklists, START-HERE (the kickoff
  prompt's single home — the README points there, path-free), inert
  merge sources (gitignore.template; ci.template.yml at kit root so
  GitHub never parses the unfilled copy), and the harness set.
  Parity-tested against its sources (MANIFEST / RENAMED / KIT_ONLY;
  suite: 49, 1 skipped).
- One-home cleanup: ADOPTION.md's home IS the kit (root copy
  removed); SETUP.md stays root-homed with a parity-pinned reference
  copy in the kit (ADOPTION and the CLAUDE template header cite its
  steps).
- ADOPTION hardened by the live run: repo-identity gate first (never
  push an app onto the template remote; dual-role cost named);
  same-name AND same-effect collision rules (retire wizards that
  regenerate harness files; never-filled {{}} slots mean never in
  use); all harness edits BEFORE activation (CHECK_COMMAND +
  PROTECTED crown jewels); existing-hook review; permission-posture
  translation for non-npm stacks; CLAUDE-merge doctrine (narrative
  overflow → wiki with pointers, volatile stats dropped, second
  instruction file merged then shrunk to a pointer); debt baseline
  with a security-exposure lens and immediate escalation for live
  exposure (an open door is not deferred debt); curated first commit
  + remote re-check before the first push.

## 2026-07.6 — v2.4

Universality round: brownfield path, portability documented, audit
fixes (touched templates stamped 2026-07.6):

- ADOPTION.md: the existing-app checklist — inventory collisions, merge
  instead of overwrite, define `check` on the CURRENT state (narrow
  scope, never weaken rules; freeze a lint baseline and ratchet), and
  the load-bearing inversion: green `check` BEFORE the Stop hook goes
  live. Architecture [Grows] is filled at adoption (the code already
  has seams); ADR-0001 recorded retroactively. Size variants (S/M/L)
  deliberately rejected: [Grows] sections, threshold triggers, and
  delete-what-you-won't-use already scale the harness by use, and every
  variant is a drift vector (the v2.2.1 settings drift is the
  empirical case).
- README: Portability section — three layers (tool-agnostic /
  concept-portable / Claude-Code-bound). Antigravity 2.0 reads
  AGENTS.md + .agents/skills/; Gemini CLI hooks share the
  exit-2-blocks semantics under renamed events (BeforeTool/AfterAgent);
  Claude Code does not read AGENTS.md natively (mid-2026), so the
  AGENTS.md-plus-CLAUDE.md-shim pattern is named but not built (YAGNI).
  Models are not the axis: hooks/settings/skills are model-independent
  within Claude Code.
- base/.gitignore: restores the scaffold patterns lost by replacement
  (*.pem, *.tsbuildinfo, next-env.d.ts, .vercel/) and adds
  __pycache__/ (the harness ships Python hooks); SETUP step 1's
  robocopy now excludes __pycache__ (seed-test bytecode was copied
  into new apps).
- check_markers.py: ADAPT note for stacks whose template syntax is {{
  (Handlebars/Jinja/Angular/Vue/Liquid) — otherwise docs code samples
  turn wiki-lint step 5 permanently red.
- settings (base + profile): deny gains the PowerShell recursive-delete
  form (Remove-Item -Recurse) — symmetric with the PS network denies;
  parameter-order variants still slip prefix matching (accident guard,
  not a boundary).
- One-home and rot cleanups: SETUP step 5 defers the leftover-template
  deletion to profile README step 2; profile ci.yml documents why the
  full-suite step duplicates check's vitest run until check narrows;
  the v2 design spec's status was stale ("pending implementation" →
  implemented, historical record).
- Seed test suite: settings parity guard — deny lists and hook
  registrations must be identical between base and profile; the
  allow/ask delta must be exactly the documented npx quartet. The
  v2.2.1 drift class, mechanized (4 new tests; suite: 45, 1 skipped).

## 2026-07.5 — v2.3.1

Remaining audit polish (medium/small priorities; touched templates
stamped 2026-07.5):

- verify_on_stop.py --self-test now verifies the whole CHECK_COMMAND:
  segments are split on shell operators outside quotes, each segment's
  leading tool must resolve (quoted paths with spaces unwrapped, shell
  builtins skipped, npm-run segments checked against package.json), so
  a typo'd binary fails at setup instead of blocking every session
  stop. Six new tests.
- CLAUDE.template.md slimmed toward its ~160 post-fill budget: success
  footer moved into SETUP step 7 (now the single home of the fill
  procedure — the template header is a pointer), purpose line and two
  emphasis restatements dropped, Task-Discipline intro compressed. The
  "Don't refactor/rename/reformat" enumeration stays — it counters a
  known agent bias.
- wiki-lint gains a budget check (CLAUDE.md over ~160 lines → propose
  wiki migration) so the growth cap has a home inside seeded apps.
- Changelog header defers the upgrade procedure to README (one home);
  SETUP step 4's non-npm tail points at the Commands ADAPT note instead
  of restating it; ultrathink Phase 6 loses a meta-sentence.

## 2026-07.4 — v2.3

Hardening round: three prose rules become mechanisms (touched templates
stamped 2026-07.4):

- The harness protects itself: protect_files.py blocks agent edits to
  `.claude/hooks/`, `.claude/scripts/`, and `.claude/settings*.json` —
  a Stop-hook-blocked agent could previously just edit the gate away.
  Skills stay agent-editable by design; SETUP's step order (CHECK_COMMAND
  in step 4, settings activation in step 5) is unaffected.
- Exit gate has one home: new `.claude/scripts/check_markers.py` (stdlib,
  tested) holds the scanned paths and exemptions; SETUP step 12 and
  wiki-lint step 5 just run it. Replaces four hand-maintained grep
  encodings that had already drifted once. wiki-lint no longer needs a
  marker exemption at all.
- TS/Next profile, eslint.config.mjs: `.only`/`.skip` on it/test/describe
  are errors (Invariant 2 mechanized; approved exceptions carry an
  eslint-disable comment as the visible approval trail) and
  `@ts-ignore`/undescribed suppressions are errors via ban-ts-comment
  (Invariant 1) — live-verified against eslint-config-next@16.
- Hook test suite: 30 passed, 1 skipped (10 new tests).

## 2026-07.3 — v2.2.1

Whole-seed audit round (4 lenses over all live files, 45 raw findings, 12
objective defects fixed; touched templates stamped 2026-07.3):

- Setup path unbroken: SETUP step 1 now says to run a scaffolder FIRST
  (create-next-app refuses non-empty dirs); profile README documents that
  a first test must exist (`vitest run` exits 1 with zero test files, so
  `check`/Stop hook/CI cannot go green without one — and `--passWithNoTests`
  must NOT be added).
- protect_files.py: blocks `bun.lock` (Bun ≥1.2 default) and
  `npm-shrinkwrap.json`; blocks a file NAMED `.git` (worktree/submodule
  gitdir pointer); tests added. Both hooks now carry template-version
  stamps.
- Exit gate tightened: the stale log-gotcha exemption removed from SETUP
  step 12 (both variants) and wiki-lint step 5 — the file has nothing to
  exempt.
- settings (base + profile): `Read(.env.staging.local)` added to the deny
  enumeration (the one missing `.local` twin).
- Invariant-3 cleanups: ultrathink's dependency bullets are now bare
  pointers to Standing Rules (they had drifted to a nonexistent "license
  check"); its body no longer restates the description's skip list;
  CLAUDE.template.md loses four same-file duplicates (gotcha-migration
  bullet, wiki filing filter, symbols-not-counts restatement, Git-bullet
  secrets sentence); log-gotcha step 1 and SPEC.template.md intro become
  pointers; wiki index.md drops a restated convention.

## 2026-07.2 — v2.2

Deltas from mapping Google's "The New SDLC with Vibe Coding" whitepaper
(May 2026) against the seed. Three small additions; the paper otherwise
independently converges with the seed's design (hooks as guarantees,
static-context budget, skills as progressive disclosure). Touched
template files carry the stamp 2026-07.2 (README is an unstamped
seed-root doc).

- CLAUDE.template.md: Invariant-5 ADAPT example for LLM/agent features
  (no prompt or model change ships without its eval set — tests verify
  the deterministic parts, evals the rest); "LLM-powered features" joins
  the Deep-Analysis triggers (mirrored in ultrathink's description, the
  one allowed restatement); Architecture ADAPT note asks for one
  canonical example file per recurring pattern.
- README: "When not to use this seed" — spikes don't get a harness, and
  a spike never graduates to production by accident.

## 2026-07.1 — v2.1

Gap-analysis round against an external "enterprise guardrails" prompt
(30 candidate gaps adversarially verified; 14 adopted, 16 rejected as
bloat or duplication of plugins/ultrathink). Touched files carry the
stamp 2026-07.1.

- CLAUDE.template.md: three new Everyday Task Discipline bullets (Reuse
  first; Verify, don't invent; User first); Security rule now covers PII;
  Dependencies rule adds a maintenance check; Invariant-5 ADAPT example
  for reversible DB migrations; session workflow includes deferred debt.
- Debt capture: log-gotcha gains a deferred-debt branch; docs/wiki/log.md
  gains the `deferred` verb. Replaces an external TECHNICAL_DEBT.md-style
  register — same function, existing append-only home.
- ultrathink: Phase-1 red flag for endpoints/routes/actions changed
  without an explicit authn/authz decision; Devil's Advocate row for
  idempotency under retries/replays/double-fires.
- SPEC.template.md: Rollback section (git revert alone, or explicit
  data/schema backout steps).
- CLAUDE.template.md post-fill budget raised ~150 → ~160 (absorbs the
  three new Task Discipline bullets).
- TS/Next profile: eslint.config.mjs added — jsx-a11y recommended
  (accessibility) + no-warning-comments (stale-marker comments), both
  enforced by the `check` gate (mechanism documented in the file header);
  new Stack Rules section in CLAUDE.stack-sections.md (UI four-state
  matrix, server-side validation); README gains the copy step (now 1–5).

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
- Verified live (2026-07-02, headless Claude Code session against a seeded
  scratch app): all three skills load; hook enforcement initially FAILED
  SILENTLY on Windows (`python` resolved to the Microsoft Store alias stub,
  exit 49 — any non-0/2 hook exit is non-blocking). Hook commands now probe
  python3/python/py by execution and fail closed if none works; re-probe
  confirmed both protected operations blocked. Also learned: Claude Code
  ignores project settings until the workspace trust dialog is accepted
  (noted in SETUP step 5).

## (pre-2026-07) — v1

- Two files: CLAUDE.template.md, ultrathink.template.md. Advisory-only.
