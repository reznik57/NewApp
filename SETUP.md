# New App Setup — Checklist

Work top to bottom inside the NEW app's repo. Do not skip the exit gate.
This file reaches an app inside `harness-kit/` (see its START-HERE.md);
step 11 deletes that folder again.
**STOP GUARD**: repo already contains application code? Wrong
checklist — use the kit's ADOPTION.md instead; the step order differs
on purpose. (If you copied the SEED folder wholesale instead of the
kit, delete README.md, TEMPLATE-CHANGELOG.md, docs/superpowers/,
tests/, profiles/, and harness-kit/ from the app now.)

- [ ] 1. **Scaffold, then distribute the kit** — the kit arrived as
      `harness-kit/` in the repo root (if not: copy the FOLDER in now,
      per its START-HERE.md). If the stack has a scaffolder
      (create-next-app, cargo new, ...), run it FIRST — scaffolders
      refuse non-empty directories, so if it balks at the kit folder,
      move `harness-kit/` aside, scaffold, move it back. Then move the
      app material to its final places:
      `harness-kit/.claude/*` → `.claude/`,
      `harness-kit/docs/*` → `docs/`, `CLAUDE.template.md`,
      `.env.example` and `.editorconfig` → app root,
      `gitignore.template` → `.gitignore` (replacing the scaffold's —
      it covers the scaffold's ignore patterns), and
      `ci.template.yml` → `.github/workflows/ci.template.yml` (filled
      in step 10). The checklists and START-HERE.md STAY in
      `harness-kit/` — step 11 deletes the folder.
- [ ] 2. **Overlay a profile** (optional) — TS/Next.js: follow
      `profiles/typescript-next/README.md` steps 1–5 (profiles live in
      the SEED, not the kit — this step needs the seed folder at hand).
- [ ] 3. **Git + env hygiene** — `git init` if needed. Create `.env` from
      `.env.example`. Verify: `git check-ignore .env` prints `.env`.
- [ ] 4. **Fill the six-script contract** in `package.json`: `check`,
      `test`, `test:one`, `fix`, `dev`, `build` (the profile's
      `package-scripts.json` provides them). Non-npm stack: act on the
      ADAPT note in CLAUDE.md → Commands now — including its
      `CHECK_COMMAND` update, which step 6's self-test verifies.
- [ ] 5. **Activate settings** — rename `.claude/settings.template.json` →
      `.claude/settings.json` (skip if the profile's `settings.json` was
      copied — profile README step 2 includes deleting the leftover
      template; two settings files invite drift). Review the permission
      posture; it encodes moderate autonomy — an accident guard, not a
      security boundary. Tighten toward ask-heavy if this app handles
      untrusted input or you run walk-away sessions.
      Claude Code ignores project settings until the workspace trust dialog
      is accepted — open the app interactively once before relying on the
      harness.
- [ ] 6. **Self-test the hooks** —
      `python .claude/hooks/verify_on_stop.py --self-test` prints
      `self-test OK` (Windows: use `py` if `python` resolves to the
      Microsoft Store alias — the registered hook commands probe
      python3/python/py by execution and fail closed if none works).
      Then `python .claude/hooks/protect_files.py --probe .env` exits 2
      (BLOCKED) and `--probe .env.example` exits 0 — the probe
      exercises the block/allow logic only, not the settings
      registration. On the
      app's first live session, confirm enforcement end-to-end: ask the
      agent to edit `.env` — the hook must block it.
- [ ] 7. **Fill CLAUDE.md** — rename `CLAUDE.template.md` → `CLAUDE.md`.
      Replace every `{{PLACEHOLDER}}`, act on and delete every `ADAPT:`
      note, delete sections that don't apply. `[Day-0]` sections are
      filled now; `[Grows]` sections stay empty (they fill from real
      incidents). Delete the header comment block — but KEEP the
      `template-version:` stamp on line 1; it survives the fill and is
      what "Upgrading seeded apps" diffs against. Budget: ~160 lines
      post-fill; past that, migrate content to docs/wiki/ and leave
      pointers. The fill worked if: sessions start
      without re-explaining the project; agents cite ADRs when
      questioning decisions; the verification gate never needs
      mentioning in chat.
- [ ] 8. **Adapt the ultrathink skill** — fill or delete the `{{}}` rows in
      `.claude/skills/ultrathink/SKILL.md` (Phase 2 stack/domain rows,
      Phase 5 project gate).
- [ ] 9. **Write ADR-0001** — copy `docs/adr/0000-template.md` to
      `docs/adr/0001-stack-choice.md`; record the stack decision and the
      alternatives you rejected.
- [ ] 10. **CI** — fill and rename `.github/workflows/ci.template.yml` →
      `ci.yml`, or use the profile's `ci.yml`, or delete it if the app is
      not on GitHub. Keep the `template-version:` stamp when you strip the
      ADAPT header comments — same reason as step 7.
- [ ] 11. **First commit at green** — delete the whole `harness-kit/`
      from the app first (all remaining scaffolding lives there), then
      `npm run check` (or your check equivalent) exits clean, then
      commit everything.
- [ ] 12. **EXIT GATE** — run the marker check from the app root; it must
      print `marker check OK`: `python .claude/scripts/check_markers.py`
      (Windows: `py` if `python` resolves to the Microsoft Store alias).
      It lists every leftover placeholder/`ADAPT:` marker; the scanned
      paths and the exemptions (reusable templates, marker-quoting hooks)
      live IN the script — its single home. A live CLAUDE.md containing
      unfilled placeholders actively misleads agents — do not finish with
      leftovers.
