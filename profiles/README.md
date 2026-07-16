<!-- template-version: 2026-07.33 -->

# Profiles

Overlays for the stack-agnostic harness. Two orthogonal kinds; an app may
take one stack profile and any number of constraint profiles.

## Stack profiles

Keyed to the tech stack chosen at SETUP step 0. Ship build tooling, the
AGENTS.md Tech Stack / Commands / Stack Rules sections, settings and CI.
Exactly one per app — SETUP step 2 applies it. Current: `typescript-next/`.

The `frontend-design` skill is NOT a profile's to ship: it is the aesthetic
floor every constraint profile layers on, so it lives in `base/.agents/skills/`
and reaches every app through the kit (v2.7.6 — before that it rode on the
TS/Next profile, and a stack-less app that took a constraint profile pointed
at a skill it did not have). An app with no UI deletes it, per the ADAPT note
on AGENTS.template's "Design before UI" bullet.

## Constraint profiles

Keyed to the app's AUDIENCE or DOMAIN, not its stack — orthogonal to the
stack profile and composable with it. A children's learning app is
`typescript-next` AND `kids-app`. Zero-to-many per app, overlaid AFTER the
stack profile (SETUP step 2). Current: `kids-app/`, `dense-ui/`,
`facilitated-session/`.

Each ships:
- `README.md` — the overlay how-to (which file goes where).
- `AGENTS.constraints-section.md` — the hard, non-negotiable invariants,
  inserted as a section into the app's AGENTS.md (the canon — never into the
  CLAUDE.md bridge). Kept lean: it counts against the AGENTS.md line budget
  (SETUP step 7), so the full material lives in the wiki page and this
  section points at it.
- `skills/<name>/SKILL.md` — a skill invoked BEFORE building UI for that
  audience, installed canonically into `.agents/skills/` with a Claude
  discovery bridge beside it in `.claude/skills/` (each profile README spells
  the two moves out). It layers on top of `frontend-design` (which sets the
  aesthetic direction); it does not restate it.
- `wiki/<name>-ux.md` — the full reference (worked examples, empirical
  sources, legal pointers), copied into the app's `docs/wiki/`.

Constraint profiles carry no `check` gate: touch-target size, icon+word,
no-hover and the like are not generically lintable. Accessibility that IS
mechanized (jsx-a11y) rides on the stack profile. These profiles are
guidance — enforced by review and the skill, not by the build.

Profiles live in the SEED only, never inside `harness-kit/`.
