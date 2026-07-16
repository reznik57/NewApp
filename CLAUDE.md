# CLAUDE.md - working on the SEED itself

**This repo is the template seed, not an app.** These instructions bind
agents editing the seed. Building an app FROM the seed? Wrong file: copy
`harness-kit/` into the app and follow its START-HERE.md.

## Repo identity

- `origin` must point at the TEMPLATE repo — an app has pushed onto
  this remote before: the push-onto-template incident behind SETUP
  step 3's repo-identity guard (changelog, v2.4.7 entry). The seed side
  of that rule is mechanized by the pre-push guard in `.githooks/`
  (the docs' single home of the exact URL). Activate it once per
  clone — git config is not cloned: `git config core.hooksPath
  .githooks`, then `py .githooks/pre_push_guard.py --self-test`. Until
  the self-test passes in a clone, verify `git remote -v` before EVERY
  push by hand — and re-run it after checking out old states: a tree
  without `.githooks/` silently suspends the guard.
- Never commit an app into this repo; never push this repo onto an app
  remote.

## Source-of-truth map

- `base/` is the SOURCE of the harness; `harness-kit/` is its
  parity-tested byte mirror (plus the kit-only checklists ADOPTION.md and
  START-HERE.md). Root `SETUP.md` is the source of the kit's SETUP.md.
  NEVER edit only the kit side — edit the source, then mirror; the
  re-sync recipe's single home is the `tests/hooks/test_kit_parity.py`
  docstring.
- **Inside the template, `AGENTS.template.md` and `.agents/skills/` are
  the canon** (v2.8.0): they carry all substance and become the app's
  `AGENTS.md` and `.agents/skills/`. `CLAUDE.template.md` and
  `.claude/skills/` are BRIDGES — frontmatter plus a pointer, nothing
  else. Adding a rule to a bridge is the mistake this split exists to
  prevent; put it in the canon. `.claude/settings.template.json` and
  `.claude/hooks/` are the exception: genuinely Claude-Code-specific,
  no canonical twin, not bridges.
- This seed's OWN instructions stay in this CLAUDE.md — it is a template
  repo, not an app built from the template, and it ships no AGENTS.md.
- Profiles live in `profiles/` only (seed-side, never inside the kit).
- One fact lives in one place; the docs link to it instead of restating
  it. Volatile counts and line numbers don't belong in prose.

## Verification gate

- The test suite must be green before every commit:
  `py -m pytest tests -q` from the seed root (the one env-gated symlink
  skip on Windows is normal). The suite IS this repo's check gate:
  kit parity, settings parity, hook behavior, root-doc truncation
  guards.
- Restructuring a guarded root doc (README.md, TEMPLATE-CHANGELOG.md,
  this file, the kit's ADOPTION.md or START-HERE.md) requires updating
  REQUIRED in `tests/hooks/test_root_docs.py` in the SAME commit —
  deliberate friction against silent truncation.

## Template discipline

- Touched a file that carries a `template-version:` stamp? Re-stamp it
  to the round's changelog header. Only JSON templates carry no stamp —
  TEMPLATE-CHANGELOG.md's header note tracks them.
- Every round gets a TEMPLATE-CHANGELOG entry, including what was
  REJECTED and why. Before proposing structural changes, search the
  changelog for prior rejections — do not relitigate them.
- Improvements come from real incidents in real apps (backflow), not
  from drawing-board speculation. This file is that rule's home.

## Release discipline

- Work on a round branch; merge `--no-ff` into master; annotated tag
  (vX.Y.Z) on the merge commit; verify the remote, then push master and
  the tag together.
- A direct commit to master (e.g. from a parallel session) is the
  exception: tag it where it lies, record the deviation in the
  changelog entry, and return to the branch flow.
