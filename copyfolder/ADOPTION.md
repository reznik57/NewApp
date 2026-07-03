# Existing App Adoption — Checklist

Bring the harness into an app that already has code. Work top to bottom
inside the EXISTING app's repo. The order differs from SETUP.md on
purpose: an existing codebase is rarely green, and the Stop hook must
not go live before `check` is — activated on a red `check`, it blocks
every session stop from day one.
(This checklist travels with `copyfolder/` into the app and is deleted
again at step 10. Fresh empty repo? Use SETUP.md instead.)

- [ ] 1. **Inventory collisions** — note what already exists: a
      CLAUDE.md or AGENTS.md, `.claude/settings.json`, CI workflows,
      lint/format configs, the test runner, anything `check`-like in
      package.json. Everything on that list is MERGED below, never
      overwritten.
- [ ] 2. **Copy the collision-free set** — usually already done: if
      this checklist sits in the app root, the copyfolder contents are
      in place → continue with step 3. Otherwise, one command at the
      app root: `robocopy "<seed>\copyfolder" . /E /XC /XN /XO`
      (the three /X flags skip every file the app already has; in a
      GUI copy, choose "skip" for existing files). The set: `docs/`
      (adr, wiki, specs), `.claude/` (hooks, scripts, skills),
      `.env.example`/`.editorconfig` where missing, the kit docs
      (`START-HERE.md` + both checklists — deleted again at step 10),
      and the two INERT templates — `CLAUDE.template.md` and
      `.claude/settings.template.json` collide with nothing and stay
      inactive until steps 5–6 activate them. Deliberately NOT in the
      set: `.gitignore` (merge-only, step 3), CI (step 8), and the
      seed's own docs (README, TEMPLATE-CHANGELOG, profiles/, tests/).
- [ ] 3. **Merge .gitignore** — append the seed patterns the app's file
      lacks (secrets block with `!.env.example`, build output, caches,
      `__pycache__/`); never replace a grown .gitignore. Verify:
      `git check-ignore .env` prints `.env`.
- [ ] 4. **Define the six-script contract on the CURRENT state** — map
      or add `check`, `test`, `test:one`, `fix`, `dev`, `build`
      (reference: `profiles/typescript-next/package-scripts.json`).
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
      workflow yet → use the template/profile CI (SETUP step 10).
- [ ] 9. **Adapt the ultrathink skill** — as SETUP step 8.
- [ ] 10. **EXIT GATE** — as SETUP step 12:
      `python .claude/scripts/check_markers.py` prints
      `marker check OK` (Windows: `py`). Then delete `START-HERE.md`,
      `ADOPTION.md`, and `SETUP.md` from the app (setup scaffolding,
      not app docs) and commit at a green `check`.
