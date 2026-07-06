# Harness Kit — Start Here

This folder is the self-contained kit that brings the coding harness
(enforcement hooks, knowledge system, checklists) into an app — brand
new OR already grown. It is the ONLY folder you ever copy; the
new-vs-existing fork comes afterwards, guided.

1. **Copy this FOLDER into the app's repo root** (so it sits at
   `<app>/harness-kit/`). One move — a folder of this name exists in
   no app, so nothing can collide or be overwritten. Direction
   matters: the kit goes INTO your app's repo — never drop your app
   into the template's folder or a clone of it.

2. **Pick the checklist — the one decision.** Not sure? Run
   `git ls-files` (ignore `harness-kit/` itself): anything real in
   the output means the repo has application code. Both checklists
   open with a STOP guard for the opposite case, so a wrong pick
   fails at step 0, not at step 8.

   **Repo already contains application code** — paste this into your
   coding agent (Claude Code, Antigravity, Gemini CLI, ...) opened in
   the app:

   > Read `harness-kit/ADOPTION.md` and work through the checklist
   > top to bottom — it distributes and merges the harness files from
   > `harness-kit/` into this existing codebase. Never overwrite an
   > existing file without asking; ask me at every merge conflict and
   > decision point.

   (Already carries the harness from an earlier kit? Same route —
   ADOPTION.md's UPDATE MODE detects it and switches to a version-diff
   merge instead of a first adoption.)

   **Repo is fresh** (empty, or nothing but a scaffolder's output) —
   paste this instead:

   > Read `harness-kit/SETUP.md` and work through the checklist top
   > to bottom in this repo. Do not skip the exit gate. Ask me at
   > every decision point.

No agent? Work through the chosen checklist by hand — the two gates
say when you are done:
`.claude/hooks/verify_on_stop.py --self-test` and
`.claude/scripts/check_markers.py`.

Either checklist deletes this whole folder at its end — the harness
stays, the scaffolding goes. The kit is SINGLE-USE: files move out of
it and the folder dies, so for the next app always copy a fresh
`harness-kit/` from the seed — it also carries the latest checklist
fixes.

Driving this from **Cowork / claude.ai** rather than a CLI? Same steps — the
checklist runs anywhere. Afterward, wire the Cowork adapter per
`docs/COWORK.md` (hooks don't fire there; CI is the gate).
