# Harness Adoption Kit — Start Here

This folder is the self-contained kit that brings the coding harness
(enforcement hooks, knowledge system, checklists) into an EXISTING
app. Two moves, nothing else needed:

1. **Copy this FOLDER into the app's root** (so it sits at
   `<app>/copyfolder/`). One move — a folder of this name exists in
   no app, so nothing can collide or be overwritten. Direction
   matters: the kit goes INTO your app's repo — never drop your app
   into the template's folder or a clone of it.

2. **Paste this into your coding agent** (Claude Code, Antigravity,
   Gemini CLI, ...) opened in the app:

> Read `copyfolder/ADOPTION.md` and work through the checklist top to
> bottom — it distributes and merges the harness files from
> `copyfolder/` into this existing codebase. Never overwrite an
> existing file without asking; ask me at every merge conflict and
> decision point.

No agent? Work through `copyfolder/ADOPTION.md` by hand — the two
gates say when you are done:
`.claude/hooks/verify_on_stop.py --self-test` and
`.claude/scripts/check_markers.py`.

ADOPTION step 11 deletes this whole folder again — the harness stays,
the scaffolding goes. Fresh empty repo instead? Don't use this kit;
seed from the template's `base/` per its `SETUP.md`.
