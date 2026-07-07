# Existing App Adoption — Checklist

Bring the harness into an app that already has code. Work top to bottom
inside the EXISTING app's repo. The order differs from SETUP.md on
purpose: an existing codebase is rarely green, and the Stop hook must
not go live before `check` is — activated on a red `check`, it blocks
every session stop from day one.
(This checklist lives in `harness-kit/` inside the app while you work
it; step 11 deletes that folder again.)
**STOP GUARD**: repo has no application code yet (empty, or nothing
but a scaffolder's output)? Wrong checklist — use the kit's SETUP.md
instead.

**UPDATE MODE** — harness already present (`.claude/hooks/verify_on_stop.py`
exists)? Then a newer `harness-kit/` was re-dropped on an already-adopted
app; this is a version merge, not a first adoption, and the full run below
collapses to four moves:
1. **Baseline first, then stamp diff** — run step 1's repo-identity STOP
   check (`git remote -v` must point at the app's own repo, never the
   template's) and snapshot the tree (`git status --short`) BEFORE any
   move-2 edit — a mature app is usually mid-work and move 4 stages against
   this baseline. Then compare each kit file's `template-version:` against
   its live twin; only changed stamps need porting. JSON and dotfile
   templates (settings, gitignore.template, gitattributes.template) carry
   no stamp — read `TEMPLATE-CHANGELOG.md` for their changes. A kit file
   with NO live twin is NEW in this kit generation: introduce it via its
   first-adoption step (e.g. gitattributes.template → step 3), never
   skip it as "no stamp diff".
2. **Live wins** — merge kit→live per file, but the app's adaptations win:
   filled ultrathink slots, a filled `ci.yml`, a richer CLAUDE.md, PROTECTED
   lists extended for the app's crown jewels. Port only genuine template
   improvements into those files — never overwrite an adaptation with a bare
   slot.
3. **Hooks are already LIVE** — the harness blocks agent edits to itself
   (`.claude/hooks`, `.claude/scripts`, `settings.json`) from the first
   moment of this session, not the next (step 5's closing note: no grace
   window). A harness-file update is therefore the ask-the-user /
   explicit-delegation case (step 11's doctrine, `protect_files.py`
   docstring): batch those edits and have the user apply or delegate them
   (e.g. a scripted `cp` from the kit) — never a silent bypass. Files
   outside the harness you edit normally.
4. **Exit** — as step 11: marker check green, delete `harness-kit/`, commit
   ONLY the harness paths against a step-1 `git status --short` baseline (a
   mature app is usually mid-work — never `git add -A`; see step 11's
   shared-file rule for a file that mixes WIP and harness content).

- [ ] 1. **Repo identity, then inventory** — first: this must be the
      APP's own repo. Check `git remote -v` — if origin points at the
      template/seed repo (an app dropped into a template clone), STOP
      and give the app a fresh start first: delete the clone's `.git`
      and `git init` anew (the template lives on elsewhere), remove
      the template leftovers (base/, profiles/, tests/, the seed's
      root docs), keep `harness-kit/`. Never push an app onto the
      template remote. (Deliberately keeping the repo dual-role
      instead? Expect gate exemptions — the template's own docs will
      trip check_markers and wiki-lint.)
      Then note what already exists: a CLAUDE.md or
      AGENTS.md, `.claude/settings.json` and `.claude/commands/`, CI
      workflows, lint/format configs, the test runner, anything
      `check`-like in package.json. Everything on that list is
      MERGED below, never overwritten. One exception: a vendored copy
      of an older template line (docs/templates/, *.template.md
      relics) gets RETIRED, not merged — the seed is the only
      upstream; git history keeps it. Snapshot the tree state now
      (`git status --short`) — a mature repo is often mid-work, and
      step 11 curates the adoption commit against this baseline so
      pre-existing modifications (even to files inside `.claude/`)
      stay out of it.
- [ ] 2. **Distribute the kit** — the kit arrived as `harness-kit/` in
      the app root (if not: copy the FOLDER in now — one move, a
      folder of this name exists in no app, nothing can collide).
      Move the app material to its final places:
      `harness-kit/.claude/*` → `.claude/` (create it, or add into the
      existing one), `harness-kit/docs/*` → `docs/`,
      `CLAUDE.template.md` → app root, and `.env.example` +
      `.editorconfig` → app root only where the app has none. The two
      moved templates are INERT — `CLAUDE.template.md` and
      `.claude/settings.template.json` collide with nothing and stay
      inactive until steps 5–6 activate them. Same-NAME conflict
      (e.g. an existing `.claude/commands/ultrathink.md` vs the kit's
      ultrathink skill): keep ONE — merge the app-specific parts into
      the kit skill's `{{}}` slots (step 10), then retire the old
      definition; two live definitions of one name compete at trigger
      time. Everything else (this
      checklist, SETUP.md, START-HERE.md, `gitignore.template`,
      `gitattributes.template`, `ci.template.yml`) STAYS in
      `harness-kit/` — step 11 deletes the whole folder. Deliberately
      not shipped ready-to-land: a live `.gitignore` and a live
      `.gitattributes` (both merge-only, step 3) and a live CI file
      (step 8).
- [ ] 3. **Merge .gitignore + .gitattributes** — append the patterns
      from `harness-kit/gitignore.template` that the app's file lacks
      (secrets block with `!.env.example`, build output, caches,
      `__pycache__/`); never replace a grown .gitignore.
      Then `.gitattributes`: the app has none → place
      `harness-kit/gitattributes.template` as `.gitattributes` (LF
      policy — without it, `core.autocrlf=true` re-materializes tracked
      LF files as CRLF on the next checkout and a working-tree formatter
      gate goes red repo-wide, disguised as a formatting problem; a
      grown Windows repo may need a one-off normalization commit, ASK
      first). The app has one → merge only what's missing; never flip
      an existing eol policy unasked. SKIP any
      template pattern that would untrack something the app ships on
      purpose (a committed build artifact, a vendored file) — and
      leave a one-line comment in .gitignore saying why, so no future
      cleanup "fixes" it. If that shipped artifact is BUILT, put its
      build into `check` (step 4) — the gate then keeps the committed
      copy fresh, mechanically. Verify: `git check-ignore .env`
      prints `.env`.
- [ ] 4. **Define the six-script contract on the CURRENT state** — map
      or add `check`, `test`, `test:one`, `fix`, `dev`, `build`
      (semantics: CLAUDE.md → Commands; optional reference if the
      seed is at hand: `profiles/typescript-next/package-scripts.json`).
      No manifest, but its runner is already in use (node without a
      package.json, ...)? A minimal scripts-only register
      (`"private": true`, no deps) beats a bespoke CHECK_COMMAND
      mapping — standard entry points are the contract's point;
      record the no-build intent in ADR-0001 (step 7).
      `check` must exit clean on the codebase AS IT IS TODAY — narrow
      its scope rather than weaken any rule:
      - Warning backlog → start `check` without that linter step, or
        freeze a baseline (lint changed dirs only); record the debt as
        a `deferred` entry in `docs/wiki/log.md` and ratchet it down.
      - No tests yet → `check` = format + typecheck; write the first
        test before adding the test step.
      Non-npm stack: also update CHECK_COMMAND in
      `.claude/hooks/verify_on_stop.py` (as SETUP step 4).
- [ ] 5. **Green gate BEFORE live hook** — run the check yourself until
      it exits 0. Finish ALL harness edits before activating (the
      harness blocks agent edits to itself afterwards): CHECK_COMMAND
      (step 4), and protect_files.py's PROTECTED lists extended with
      the app's crown jewels (binary masters, databases — text tools
      corrupt them). Only then activate: merge the copied
      `.claude/settings.template.json` (permission posture + both hook
      registrations) into the existing `.claude/settings.json`, or
      rename it to `.claude/settings.json` if none exists; delete the
      template copy afterwards (two settings files invite drift).
      While merging: review the app's EXISTING hooks and commands —
      retire what the harness supersedes, what injects stale content,
      and anything that would regenerate or overwrite harness files
      when run (onboarding wizards, scaffolders); `{{}}` slots that
      were never filled mean a command was never truly in use —
      default to retiring it, not filling it. On a non-npm stack,
      translate the allow/ask commands to the app's toolchain (the
      POSTURE carries, not the literal npm entries); a deny that
      breaks a DOCUMENTED app workflow (a gotcha citing curl for
      local verification) moves to ask instead — the guard stays,
      the workflow survives. The app's
      `settings.local.json`, if any, stays untouched — Claude Code
      merges both. Then self-test as SETUP step 6 (`--self-test`,
      plus `protect_files.py --probe` per path) — and treat both
      hooks as potentially LIVE from the moment settings.json is
      written: Claude Code versions differ on whether hooks bind
      immediately or at the next session start, so never plan a
      harness edit on the assumption of a grace window. The live
      `.env`-edit probe still needs a fresh session.
- [ ] 6. **Merge CLAUDE.md** — rename the copied `CLAUDE.template.md`
      → `CLAUDE.md`, then move the old instructions INTO its sections;
      the template's Invariants and Task Discipline win over softer
      duplicates of the same rule. (Direction flips when the EXISTING
      CLAUDE.md is substantially richer than the template: keep it as
      the base and graft IN the template's load-bearing pieces — the
      source-of-truth and no-volatile-counts Invariants, the Commands
      table, the docs & knowledge schema, the deep-analysis pointer.
      The goal is fixed — ONE file with every frame piece present;
      only the direction is the judgment call.) Narrative overflow (feature docs,
      changelog prose) becomes `docs/wiki/` pages with pointers —
      registered in the wiki index — and volatile statistics are
      dropped, not migrated (Invariant 4). A SECOND instruction file
      (AGENTS.md, .cursorrules, GEMINI.md): merge its rules the same
      way — domain rules often make a strong Invariant 5 — then
      shrink that file to a pointer at CLAUDE.md. Other tools
      actively read it (the AGENTS.md convention, GEMINI.md)? Then
      its surviving shape is: tool-specific delta (persona, loading
      mechanics, tool-own protocols) + a compact invariant summary +
      the pointer — a small, deliberate duplication. What must NOT
      survive is duplicated detail substance (architecture, versions,
      counts): unmaintained mirrors rot into actively wrong guidance
      while CLAUDE.md moves on. Loose narratives already under `docs/`
      move into `docs/wiki/` (git mv + index entry); process history
      (old plans/specs folders) stays put — knowledge gets indexed,
      history doesn't. Unlike a fresh app, fill
      `Architecture [Grows]` NOW — the code already has seams worth
      naming. Otherwise follow SETUP step 7 (markers, ADAPT notes,
      stamp-survives-fill, line budget).
- [ ] 7. **ADR-0001 retroactively** — record the stack AS IT IS and why
      it stays (migration cost is a valid reason). Future decisions
      get ADRs the normal way.
- [ ] 8. **CI** — merge the gate into the existing workflow (check →
      full tests → build → audit) instead of adding a second one; no
      workflow yet → copy `harness-kit/ci.template.yml` to
      `.github/workflows/ci.yml` and fill it (inside harness-kit/ the
      unfilled copy is never parsed by GitHub). No remote yet? Create
      it anyway — inert until the first push, and after step 11 the
      template is gone; skip only if the repo will NEVER be hosted
      (then record that in ADR-0001). Run the dependency audit
      locally BEFORE wiring its CI step. Red today with the fix
      deferred (step 9's exception decides what is surfaced to the
      user immediately)? Wire the step non-failing
      (`continue-on-error: true`) and record a `deferred` entry in
      `docs/wiki/log.md` naming the trigger that turns it hard —
      the same ratchet doctrine as step 4's warning backlog. Never
      day-one-red CI for debt you just catalogued, and never silent
      yellow either; the log entry is the difference.
- [ ] 9. **Debt baseline — inventory, don't fix** — one timeboxed
      pass over the codebase: obvious legacy files (`*_old`, `*.bak`,
      commented-out blocks), unused dependencies (e.g. `npx
      depcheck`), dead exports, known-fragile areas — and security
      exposure (unauthenticated endpoints, 0.0.0.0 binds, secrets in
      code, raw errors sent to clients). Register each as a
      `deferred` entry in `docs/wiki/log.md` (what, why it stays,
      what triggers paying it down) — fix now ONLY what blocks the
      green `check`. EXCEPTION: live security exposure is surfaced
      to the user immediately with options (fix / mitigate / retire
      the surface) — an open door is not deferred debt. When
      mitigating, prefer a secure default plus an explicitly NAMED
      opt-in (a `dev:lan` script) over a permissive default plus a
      deferred note — the opening stays deliberate and diff-visible.
      From here the harness holds the line: the gate
      blocks new debt, `/log-gotcha` records deliberate shortcuts,
      and registered debt is paid down surgically when a real task
      touches that area — no big-bang refactors.
- [ ] 10. **Adapt the ultrathink skill** — as SETUP step 8.
- [ ] 11. **EXIT GATE** — as SETUP step 12:
      `python .claude/scripts/check_markers.py` prints
      `marker check OK` (Windows: `py`). The gate surfacing a harness
      adaptation (an EXEMPT extension, a MARKERS tweak) is the
      ask-the-user case working as designed: the user applies the
      edit or explicitly delegates it — never bypass the guard
      silently. Then delete the whole
      `harness-kit/` from the app (all remaining scaffolding lives
      there) and make the first commit at a green `check` — curated:
      app code and harness in; junk, backups/, and private data
      (databases, master files) out and .gitignore'd. Tree was dirty
      at step 1? Commit on a dedicated branch and stage ONLY adoption
      paths, checked against the step-1 baseline so pre-existing
      modifications ride along nowhere; never `git add -A`. One file
      that mixes WIP and adoption content (e.g. a `docs/wiki/log.md`
      carrying both an app entry and the harness-update entry) cannot
      be split by path — DEFAULT: have the user commit their WIP first,
      so the adoption commit is clean; hand-crafting a partial blob
      (`git hash-object`) to stage only the adoption lines is a
      deliberate exception, not the norm. Re-check
      `git remote -v` BEFORE the first push: it must point at the
      app's own repo, never the template's (step 1).

**Cowork / claude.ai (optional).** Adopting into an app you'll also drive
from Cowork? Its hooks don't fire there — follow `docs/COWORK.md` to wire the
Cowork adapter (a project-instructions pointer that loads CLAUDE.md; CI stays
the hard gate). Claude-Code-only? Delete `docs/COWORK.md`.
