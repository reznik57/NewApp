# New App Setup — Checklist

Work top to bottom inside the NEW app's repo. Do not skip the exit gate.
The paste-prompt's "ask me at every decision point" has its checklist
counterpart in step 0's interview and the **ASK** markers below — ask at
the step where the context exists, with recommendations only AFTER the
answers they depend on.
This file reaches an app inside `harness-kit/` (see its START-HERE.md);
step 11 deletes that folder again.
**STOP GUARD**: repo already contains application code? Wrong
checklist — use the kit's ADOPTION.md instead; the step order differs
on purpose. (If you copied the SEED folder wholesale instead of the
kit, strip ALL seed material from the app now — README.md,
TEMPLATE-CHANGELOG.md, the seed's own CLAUDE.md, .gitattributes and
.gitignore, the root SETUP.md copy, base/, docs/superpowers/, tests/,
profiles/, .githooks/,
any seed-local .claude/ or cache folders, and the stale harness-kit/ —
then copy a FRESH `harness-kit/` in per its START-HERE.md. Leftover
seed trees survive the exit gate silently; it scans only the app's
CLAUDE.md, .claude/, docs/ and .github/.)

- [ ] 0. **Discovery — ASK before anything is scaffolded.** Interview the
      user in small, focused rounds (never premark a recommendation the
      answers haven't earned yet): What is the app, for whom? What data
      does it hold — persistence needed, where? Platform (web/CLI/native,
      offline use)? Auth? External integrations? GitHub + CI (feeds
      step 10 and the GitHub note at the end)? Cowork/claude.ai as a
      second surface (see the Cowork note)? Has it a UI — then WHERE is it
      read (browser, projector at a distance, paper, phone in hand) and may
      every viewer see the same thing (roles, confidentiality)? Both answers
      are design constraints, not settings; "projected / printed / role-split"
      routes to the `facilitated-session` profile in step 2. Then — and only then — settle
      the stack, noting the rejected alternatives for step 9's ADR. The
      catalog is a minimum, not a form: stop once the answers carry the
      decisions. The user may delegate ("you pick") — then the ADR
      records that delegation honestly instead of invented requirements.
      Route the answers to their homes as the checklist reaches them:
      purpose/users → CLAUDE.md Role & Context (step 7); requirements,
      decision, alternatives → ADR-0001 (step 9); foreseeable variables
      → `.env.example` (step 3).
- [ ] 1. **Scaffold, then distribute the kit** — the kit arrived as
      `harness-kit/` in the repo root (if not: copy the FOLDER in now,
      per its START-HERE.md). If the stack has a scaffolder
      (create-next-app, cargo new, ...), run it FIRST — scaffolders
      refuse non-empty directories, so if it balks at the kit folder,
      move `harness-kit/` aside, scaffold, move it back. A scaffolder can
      also refuse the folder NAME (npm forbids spaces and capitals — both
      common in Windows folder names): then scaffold in a sibling temp
      directory under a valid kebab-case name, delete what must not
      survive (build output, a scaffold-generated CLAUDE.md — see below),
      move everything INCLUDING dotfiles into the repo, delete the temp
      dir; the valid name stays as the package name. Then move the
      app material to its final places:
      `harness-kit/.claude/*` → `.claude/`,
      `harness-kit/docs/*` → `docs/`, `CLAUDE.template.md`,
      `.env.example` and `.editorconfig` → app root,
      `gitignore.template` → `.gitignore` (replacing the scaffold's —
      it covers the scaffold's ignore patterns),
      `gitattributes.template` → `.gitattributes` (line-ending policy:
      without it, `core.autocrlf=true` — the Git-for-Windows default —
      re-materializes LF files as CRLF on the next checkout and turns a
      repo-wide formatter gate red), and
      `ci.template.yml` → `.github/workflows/ci.template.yml` (filled
      in step 10). A scaffolder may also generate its own instruction
      files: a scaffold CLAUDE.md yields to the kit's CLAUDE.template.md
      (step 7) — merge any load-bearing content into the kept file; an
      AGENTS.md survives only WIRED (an `@AGENTS.md` reference from
      CLAUDE.md, or merged and shrunk to a pointer) — an instruction
      file no session loads misleads by existing. The checklists and
      START-HERE.md STAY in `harness-kit/` — step 11 deletes the folder.
- [ ] 2. **Overlay a profile** (if one exists for the stack chosen in
      step 0 — a profile accelerates a decision, it never justifies
      one) — TS/Next.js: follow ALL numbered steps of
      `profiles/typescript-next/README.md` (profiles live in the SEED,
      not the kit — the paste-prompt names the seed's path; missing?
      ASK the user where the seed lives, never scan drives for it).
      No profile for the chosen stack? Skip — CLAUDE.template.md's
      ADAPT notes and step 4 carry the non-npm path.
      Then, orthogonally, overlay any CONSTRAINT profiles — audience/domain
      guardrails composable with the stack profile (`kids-app`, `dense-ui`,
      `facilitated-session`). Zero is fine; `profiles/README.md` explains the
      two profile kinds, and each constraint profile's README lists its steps.
      They all layer on the `frontend-design` skill, which step 1 already
      distributed with the harness — it is not a profile's to ship.
- [ ] 3. **Git + env hygiene** — `git init` if needed, then confirm repo
      identity: `git remote -v` must be empty or point at the app's OWN
      repo, never the template/seed. A fresh app scaffolded inside a seed
      clone inherits the seed's `origin` — delete `.git` and `git init`
      anew, or repoint `origin`, so the app never pushes onto the template
      remote. Then env hygiene, and mind who owns which half: the AGENT
      fills `.env.example` with the names and placeholder values step 0
      surfaced (committed); the USER creates `.env` from it and pastes the
      real values in. `.env` is protected — `protect_files` blocks agent
      Edit/Write on it (already live from step 2 if a stack profile copied
      `settings.json`), and a shell copy to route around that block is the
      silent bypass the hook exists to prevent. Verify:
      `git check-ignore .env` prints `.env`.
- [ ] 4. **Fill the six-script contract** in `package.json`: `check`,
      `test`, `test:one`, `fix`, `dev`, `build` (the profile's
      `package-scripts.json` provides them). **Every server this app runs
      locally binds a port ROLLED ONCE from 9000–9999** —
      `py -c "import random;print(random.randint(9000,9999))"` — wired hard
      into the command that starts it (`next dev -p 9427`,
      `uvicorn app:api --port 9427`, `npx serve -l 9427`), never the framework
      default: 3000/5173/8000 collide the moment a second app runs, and the
      expensive failure is the silent one — you reach a server, just
      yesterday's. Rolled ONCE, not per start: a moving port breaks Playwright
      `baseUrl`s, CORS origins and OAuth callbacks. Two servers (frontend +
      backend) take two ports from the range. On the profile path the roll
      fills `{{DEV_PORT}}` in `dev` and `start`, and step 12's gate catches a
      forgotten one; a non-npm server has no such slot — there the rule is on
      you. Non-npm stack: act on the ADAPT note in CLAUDE.md → Commands now —
      including its `CHECK_COMMAND` update, which step 6's self-test verifies.
      **Every harness edit belongs in this step**, before activation
      (step 5 — or step 2, if a stack profile already copied
      `settings.json`): afterwards the harness blocks agent edits to
      itself. Same window for the app's binary crown jewels — an `.xlsm`
      master, a `.duckdb` file: extend `PROTECTED_BASENAMES` /
      `BINARY_SUFFIXES` in `.claude/hooks/protect_files.py` NOW
      (ADOPTION step 5 carries the same rule).
- [ ] 5. **Activate settings** — rename `.claude/settings.template.json` →
      `.claude/settings.json` (skip if the profile's `settings.json` was
      copied — profile README step 2 includes deleting the leftover
      template; two settings files invite drift). Review the permission
      posture; it encodes moderate autonomy — an accident guard, not a
      security boundary. Tighten toward ask-heavy if this app handles
      untrusted input or you run walk-away sessions.
      **Activation is the point of no return**: treat both hooks as LIVE
      from the moment `settings.json` exists — the running session picks it
      up, there is no grace window until the next one — and on the profile
      path that moment already passed in step 2. Every harness edit belongs
      before it (step 4). (One exception, in the other direction: a
      workspace never opened interactively ignores project settings
      entirely, trust dialog unaccepted — open the app once before RELYING
      on the harness.)
      From here until step 11 the app has no test, so `check` is red BY
      DESIGN and the Stop hook will block the first stop of each turn and
      hand you the failure. **That is the gate working, not a broken
      harness** — do not weaken `check` to silence it (no
      `--passWithNoTests`); carry on to step 11, which is where the red
      goes green. (ADOPTION inverts this — an existing app CAN be green
      before the hook goes live, so there it must be.)
- [ ] 6. **Self-test the hooks — the scripts, then the REGISTRATION.**
      `python .claude/hooks/verify_on_stop.py --self-test` prints
      `self-test OK` (Windows: use `py` if `python` resolves to the
      Microsoft Store alias — the registered hook commands probe
      python3/python/py by execution and fail closed if none works).
      Then `python .claude/hooks/protect_files.py --probe .env` exits 2
      (BLOCKED) and `--probe .env.example` exits 0.
      Both probes exercise the SCRIPTS only — they cannot see whether the
      registration works, and a broken registration fails OPEN: Claude Code
      treats any hook exit other than 2 as a non-blocking error and lets the
      write through. So prove the registration too: run the `command` string
      from `.claude/settings.json`'s PreToolUse entry verbatim (with
      `CLAUDE_PROJECT_DIR` set to the app root), piping in
      `{"tool_input":{"file_path":".env"}}` — it must exit 2. On a Windows
      box WITHOUT Git Bash it will not: Claude Code passes a command hook to
      Git Bash there, or to PowerShell when Git Bash is absent, and
      PowerShell has no `sh` to run the wrapper — both hooks are then
      silently dead. Install Git Bash, or re-register for the shell you have.
      Finally, in the app's first live session, confirm enforcement
      end-to-end: ask the agent to edit `.env` — the hook must block it.
      **The harness is not live until you have watched it block once.**
- [ ] 7. **Fill CLAUDE.md** — rename `CLAUDE.template.md` → `CLAUDE.md`.
      Replace every `{{PLACEHOLDER}}`, act on and delete every `ADAPT:`
      note, delete sections that don't apply. `[Day-0]` sections are
      filled now; `[Grows]` sections stay empty (they fill from real
      incidents). Delete the header comment block — but KEEP the
      `template-version:` stamp on line 1; it survives the fill and is
      what "Upgrading seeded apps" diffs against. **ASK** the user for
      the project-specific invariant (⛔ 5) and any Role & Context facts
      step 0 didn't surface. Budget: the wiki-lint skill's CLAUDE.md
      line ceiling (the number's single home; a stack profile's sections
      count against it) — past it, MEASURE which blocks overflow and
      migrate those to docs/wiki/ with pointers, never a guessed
      culprit. Also replace the scaffold's README.md — stack boilerplate,
      often with paths this layout doesn't even have — with a minimal
      app README: name, purpose, the six-script contract. The fill
      worked if: sessions start
      without re-explaining the project; agents cite ADRs when
      questioning decisions; the verification gate never needs
      mentioning in chat.
- [ ] 8. **Adapt the ultrathink skill** — fill or delete the `{{}}` rows in
      `.claude/skills/ultrathink/SKILL.md` (Phase 2 stack/domain rows,
      Phase 5 project gate).
- [ ] 9. **Write ADR-0001** — copy `docs/adr/0000-template.md` to
      `docs/adr/0001-stack-choice.md`; record the stack decision MADE in
      step 0 and the alternatives rejected there. If this ADR has to be
      invented from scratch here, step 0 was skipped — and requirements
      nobody stated (persistence, auth, offline) don't belong in its
      Context. "A profile exists" may appear as convenience, never as
      the decisive reason.
- [ ] 10. **CI** — fill and rename `.github/workflows/ci.template.yml` →
      `ci.yml`, or use the profile's `ci.yml`, or delete it if the app is
      not on GitHub. Keep the `template-version:` stamp when you strip the
      ADAPT header comments — same reason as step 7.
- [ ] 11. **First commit at green** — a `check` whose test step finds
      ZERO tests is red by design (never add a pass-with-no-tests
      flag — that weakens the gate): **ASK** the user which small, real
      first test the app gets, and write it now if none exists. Then
      delete the whole `harness-kit/` from the app (all remaining
      scaffolding lives there), `npm run check` (or your check
      equivalent) exits clean, run step 12's marker check and get
      `marker check OK` — the first commit is the one the app's history is
      anchored on; it must not carry unfilled placeholders (ADOPTION orders
      it the same way) — then commit everything. A burst of
      `LF will be replaced by CRLF` warnings at `git add` means step 1's
      `.gitattributes` never landed — fix that before committing. (The
      opposite direction, `CRLF will be replaced by LF`, is the policy
      WORKING: normalization, not a missing file.)
- [ ] 12. **EXIT GATE** — run the marker check from the app root; it must
      print `marker check OK`: `python .claude/scripts/check_markers.py`
      (Windows: `py` if `python` resolves to the Microsoft Store alias).
      It lists every leftover placeholder/`ADAPT:` marker; the scanned
      paths and the exemptions (reusable templates, marker-quoting hooks)
      live IN the script — its single home. A live CLAUDE.md containing
      unfilled placeholders actively misleads agents — do not finish with
      leftovers.

**GitHub (if step 0 said yes).** The setup is complete only when the repo
exists on GitHub, `origin` points at it, the first push is up, and the
`ci.yml` run came back green — an unparsed workflow file is not a
backstop. Can't create the remote right now? Hand it off EXPLICITLY as an
open item; never let a passed exit gate imply the CI decision is done.

**Cowork / claude.ai (optional).** Driving this app from Cowork too? Its
hooks don't fire there — follow `docs/COWORK.md` to wire the Cowork adapter
(a project-instructions pointer that loads CLAUDE.md; CI stays the hard
gate). Claude-Code-only? Delete `docs/COWORK.md` — an unused adapter rots.
