# New App Setup — Checklist

Work top to bottom inside the NEW app's repo. Do not skip the exit gate.
(This file lives in the seed and is never copied. If you copied the seed
folder wholesale, delete SETUP.md, README.md, TEMPLATE-CHANGELOG.md,
docs/superpowers/, tests/, and profiles/ from the app now.)

- [ ] 1. **Copy the base** — from the seed: `robocopy "<seed>\base" . /E`
      run at the new repo root (robocopy exit codes 0–3 are success), or any
      copy that includes dotfiles (`.gitignore`, `.env.example`,
      `.editorconfig`, `.claude/`, `.github/`).
- [ ] 2. **Overlay a profile** (optional) — TS/Next.js: follow
      `profiles/typescript-next/README.md` steps 1–5.
- [ ] 3. **Git + env hygiene** — `git init` if needed. Create `.env` from
      `.env.example`. Verify: `git check-ignore .env` prints `.env`.
- [ ] 4. **Fill the six-script contract** in `package.json`: `check`,
      `test`, `test:one`, `fix`, `dev`, `build` (the profile's
      `package-scripts.json` provides them). Non-npm stack: document the
      equivalents in CLAUDE.md → Commands AND update `CHECK_COMMAND` in
      `.claude/hooks/verify_on_stop.py`.
- [ ] 5. **Activate settings** — rename `.claude/settings.template.json` →
      `.claude/settings.json` (skip if the profile's `settings.json` was
      copied). Review the permission posture; it encodes moderate autonomy —
      an accident guard, not a security boundary. Tighten toward ask-heavy
      if this app handles untrusted input or you run walk-away sessions.
      If you copied the profile's `settings.json`, delete the leftover
      `.claude/settings.template.json` — two settings files invite drift.
      Claude Code ignores project settings until the workspace trust dialog
      is accepted — open the app interactively once before relying on the
      harness.
- [ ] 6. **Self-test the hooks** —
      `python .claude/hooks/verify_on_stop.py --self-test` prints
      `self-test OK` (Windows: use `py` if `python` resolves to the
      Microsoft Store alias — the registered hook commands probe
      python3/python/py by execution and fail closed if none works). On the
      app's first live session, confirm enforcement end-to-end: ask the
      agent to edit `.env` — the hook must block it.
- [ ] 7. **Fill CLAUDE.md** — rename `CLAUDE.template.md` → `CLAUDE.md`.
      Replace every `{{PLACEHOLDER}}`, act on and delete every `ADAPT:`
      note, delete sections that don't apply, keep `[Grows]` sections
      empty, delete the header comment block. Budget: ~150 lines.
- [ ] 8. **Adapt the ultrathink skill** — fill or delete the `{{}}` rows in
      `.claude/skills/ultrathink/SKILL.md` (Phase 2 stack/domain rows,
      Phase 5 project gate).
- [ ] 9. **Write ADR-0001** — copy `docs/adr/0000-template.md` to
      `docs/adr/0001-stack-choice.md`; record the stack decision and the
      alternatives you rejected.
- [ ] 10. **CI** — fill and rename `.github/workflows/ci.template.yml` →
      `ci.yml`, or use the profile's `ci.yml`, or delete it if the app is
      not on GitHub.
- [ ] 11. **First commit at green** — `npm run check` (or your check
      equivalent) exits clean, then commit everything.
- [ ] 12. **EXIT GATE** — both commands print nothing. (Drop `.github` from
      the path lists if you deleted it in step 10.) Excludes
      `docs/adr/0000-template.md` and `docs/specs/SPEC.template.md` (reusable
      templates that ship with placeholders forever — copy them, never fill
      them in place) and the hooks/skills that legitimately keep `ADAPT:`
      tailoring markers or quote the `{{` syntax
      (`.claude/hooks/protect_files.py`,
      `.claude/hooks/verify_on_stop.py`, `.claude/skills/wiki-lint/SKILL.md`,
      `.claude/skills/log-gotcha/SKILL.md`):

  ```powershell
  $exempt = 'docs[\\/]adr[\\/]0000-template\.md$|docs[\\/]specs[\\/]SPEC\.template\.md$|\.claude[\\/]skills[\\/]wiki-lint[\\/]SKILL\.md$|\.claude[\\/]skills[\\/]log-gotcha[\\/]SKILL\.md$|\.claude[\\/]hooks[\\/](protect_files|verify_on_stop)\.py$'
  Get-ChildItem -Recurse -File -Path CLAUDE.md, .claude, docs, .github |
    Where-Object { ($_.FullName.Substring((Get-Location).Path.Length + 1)) -notmatch $exempt } |
    Select-String -Pattern '\{\{'
  Get-ChildItem -Recurse -File -Path CLAUDE.md, .claude, docs, .github |
    Where-Object { ($_.FullName.Substring((Get-Location).Path.Length + 1)) -notmatch $exempt } |
    Select-String -Pattern 'ADAPT:'
  ```

  (POSIX: `grep -rn "{{" CLAUDE.md .claude/ docs/ .github/ --exclude=0000-template.md --exclude=SPEC.template.md --exclude=protect_files.py --exclude=verify_on_stop.py --exclude-dir=wiki-lint --exclude-dir=log-gotcha` and the
  same for `ADAPT:`. grep's `--exclude` matches basenames only, hence
  `--exclude-dir` for the two skill directories.) A live CLAUDE.md containing
  unfilled placeholders actively misleads agents — do not finish with
  leftovers.
