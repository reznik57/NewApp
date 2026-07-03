# Harness Adoption Kit — Start Here

This folder is the self-contained kit that brings the coding harness
(enforcement hooks, knowledge system, checklists) into an EXISTING
app. Two moves, nothing else needed:

1. **Copy the CONTENTS of this folder into the app's root.** When the
   copy dialog asks about existing files: SKIP, never replace.
   Command-line equivalent, run at the app root:
   `robocopy "<this-folder>" . /E /XC /XN /XO`

2. **Paste this into your coding agent** (Claude Code, Antigravity,
   Gemini CLI, ...) opened in the app:

> Read `ADOPTION.md` in this repo's root and work through the
> checklist top to bottom — it merges the just-copied harness files
> into this existing codebase. Never overwrite an existing file
> without asking; ask me at every merge conflict and decision point.

No agent? Work through `ADOPTION.md` by hand — the two gates say when
you are done: `.claude/hooks/verify_on_stop.py --self-test` and
`.claude/scripts/check_markers.py`.

ADOPTION step 10 deletes this file and both checklists again — the
harness stays, the scaffolding goes. Fresh empty repo instead? Don't
use this kit; seed from the template's `base/` per its `SETUP.md`.
