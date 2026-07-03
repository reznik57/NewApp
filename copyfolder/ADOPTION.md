# Existing App Adoption — Checklist

Bring the harness into an app that already has code. Work top to bottom
inside the EXISTING app's repo. The order differs from SETUP.md on
purpose: an existing codebase is rarely green, and the Stop hook must
not go live before `check` is — activated on a red `check`, it blocks
every session stop from day one.
(This checklist lives in `copyfolder/` inside the app while you work
it; step 11 deletes that folder again. Fresh empty repo? Use SETUP.md
instead.)

- [ ] 1. **Inventory collisions** — note what already exists: a
      CLAUDE.md or AGENTS.md, `.claude/settings.json`, CI workflows,
      lint/format configs, the test runner, anything `check`-like in
      package.json. Everything on that list is MERGED below, never
      overwritten.
- [ ] 2. **Distribute the kit** — the kit arrived as `copyfolder/` in
      the app root (if not: copy the FOLDER in now — one move, a
      folder of this name exists in no app, nothing can collide).
      Move the app material to its final places:
      `copyfolder/.claude/*` → `.claude/` (create it, or add into the
      existing one), `copyfolder/docs/*` → `docs/`,
      `CLAUDE.template.md` → app root, and `.env.example` +
      `.editorconfig` → app root only where the app has none. The two
      moved templates are INERT — `CLAUDE.template.md` and
      `.claude/settings.template.json` collide with nothing and stay
      inactive until steps 5–6 activate them. Everything else (this
      checklist, SETUP.md, START-HERE.md, `gitignore.template`,
      `ci.template.yml`) STAYS in `copyfolder/` — step 11 deletes the
      whole folder. Deliberately not shipped ready-to-land: a live
      `.gitignore` (merge-only, step 3) and a live CI file (step 8).
- [ ] 3. **Merge .gitignore** — append the patterns from
      `copyfolder/gitignore.template` that the app's file lacks
      (secrets block with `!.env.example`, build output, caches,
      `__pycache__/`); never replace a grown .gitignore. Verify:
      `git check-ignore .env` prints `.env`.
- [ ] 4. **Define the six-script contract on the CURRENT state** — map
      or add `check`, `test`, `test:one`, `fix`, `dev`, `build`
      (semantics: CLAUDE.md → Commands; optional reference if the
      seed is at hand: `profiles/typescript-next/package-scripts.json`).
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
      it exits 0. Only then activate: merge the copied
      `.claude/settings.template.json` (permission posture + both hook
      registrations) into the existing `.claude/settings.json`, or
      rename it to `.claude/settings.json` if none exists; delete the
      template copy afterwards (two settings files invite drift). The
      app's `settings.local.json`, if any, stays untouched — Claude
      Code merges both. Then self-test as SETUP step 6
      (`--self-test`, then the live `.env`-edit probe).
- [ ] 6. **Merge CLAUDE.md** — rename the copied `CLAUDE.template.md`
      → `CLAUDE.md`, then move the old instructions INTO its sections;
      the template's Invariants and Task Discipline win over softer
      duplicates of the same rule. Unlike a fresh app, fill
      `Architecture [Grows]` NOW — the code already has seams worth
      naming. Otherwise follow SETUP step 7 (markers, ADAPT notes,
      line budget).
- [ ] 7. **ADR-0001 retroactively** — record the stack AS IT IS and why
      it stays (migration cost is a valid reason). Future decisions
      get ADRs the normal way.
- [ ] 8. **CI** — merge the gate into the existing workflow (check →
      full tests → build → audit) instead of adding a second one; no
      workflow yet → copy `copyfolder/ci.template.yml` to
      `.github/workflows/ci.yml` and fill it (inside copyfolder/ the
      unfilled copy is never parsed by GitHub).
- [ ] 9. **Debt baseline — inventory, don't fix** — one timeboxed
      pass over the codebase: obvious legacy files (`*_old`, `*.bak`,
      commented-out blocks), unused dependencies (e.g. `npx
      depcheck`), dead exports, known-fragile areas. Register each as
      a `deferred` entry in `docs/wiki/log.md` (what, why it stays,
      what triggers paying it down) — fix now ONLY what blocks the
      green `check`. From here the harness holds the line: the gate
      blocks new debt, `/log-gotcha` records deliberate shortcuts,
      and registered debt is paid down surgically when a real task
      touches that area — no big-bang refactors.
- [ ] 10. **Adapt the ultrathink skill** — as SETUP step 8.
- [ ] 11. **EXIT GATE** — as SETUP step 12:
      `python .claude/scripts/check_markers.py` prints
      `marker check OK` (Windows: `py`). Then delete the whole
      `copyfolder/` from the app (all remaining scaffolding lives
      there) and commit at a green `check`.
