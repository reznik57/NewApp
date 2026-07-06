<!-- template-version: 2026-07.14 -->

# Profile: TypeScript / Next.js

Overlay for the stack-agnostic `base/`. Apply AFTER copying `base/*` into
the new repo (SETUP.md step 2):

1. Merge `package-scripts.json` → the `"scripts"` block of the app's
   `package.json` (created by `create-next-app` or `npm init`).
2. Copy `settings.json` → `.claude/settings.json` (replaces renaming the
   base template; already filled for npm/next/vitest/eslint/tsc).
   Delete `.claude/settings.template.json` afterwards.
3. Copy `ci.yml` → `.github/workflows/ci.yml`, then DELETE the leftover
   `.github/workflows/ci.template.yml` that SETUP step 1 placed there —
   GitHub parses every `*.yml` in that dir and the exit-gate marker check
   (SETUP step 12) scans `.github/`, so an unfilled template fails both.
4. Copy `eslint.config.mjs` → repo root, replacing the one create-next-app
   generated. It layers the profile's enforced rules on the Next.js
   defaults — the file's header is the sole home for what they are and
   how they gate.
5. Replace the `Tech Stack` and `Commands` sections of CLAUDE.md — still
   named `CLAUDE.template.md` at overlay time; SETUP step 7 renames it and
   fills the rest — with the contents of `CLAUDE.stack-sections.md`
   (includes the `Stack Rules` section — keep it). Its third Stack Rule
   points at the `frontend-design` skill, so it REQUIRES step 6 — do both
   or neither; step 5 alone leaves a dead pointer in the app's CLAUDE.md.
6. Copy `skills/frontend-design/` → `.claude/skills/frontend-design/`
   (both `SKILL.md` and its `LICENSE.txt` — Apache-2.0, keep them
   together). The other half of step 5: this profile vendors the
   `frontend-design` skill from claude-plugins-official so a seeded TS/Next
   app has it without the plugin installed, and step 5's design pointer
   invokes it by name.

Still manual afterwards: Role & Context, the project-specific invariant,
Invariant 1's `{{CHECK CMD}}` (fill with `npm run check`) and
`{{CI-EQUIVALENT CMD}}` (fill with `npm run check; npm test; npm run build`),
`{{FORMATTER}}` (Prettier), ADR-0001, and the app's first test —
`vitest run` exits 1 when no test files exist, so `check` (and with it the
Stop hook and CI) cannot go green until one is written. Do NOT add
`--passWithNoTests`; that weakens the gate. Dev dependencies expected by the
scripts: typescript, vitest, eslint (flat config), eslint-config-next
(>= 16 — flat-native; needs `next` present at lint time),
eslint-plugin-jsx-a11y, prettier.

When the test suite gets slow, narrow the `check` script's test step to
changed/affected tests (e.g. `vitest run --changed`) — the gate must stay
fast; CI runs the full suite.
