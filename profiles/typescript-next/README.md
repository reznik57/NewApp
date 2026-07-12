<!-- template-version: 2026-07.31 -->

# Profile: TypeScript / Next.js

Overlay for the stack-agnostic harness. Apply AFTER SETUP.md step 1 has
distributed `harness-kit/` — this README IS the substance of SETUP
step 2 (`base/` is seed-internal source material; nobody copies it into
an app):

1. Merge `package-scripts.json` → the `"scripts"` block of the app's
   `package.json` (created by `create-next-app` or `npm init`). On a name
   collision the profile's entry WINS. Scaffold leftovers: delete `lint`
   (it lives in `check`/`fix` — a second, laxer lint entry drifts);
   keeping `start` is fine (`next start` serves deployments).
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
   points at the `frontend-design` skill, which SETUP step 1 already
   distributed with the harness (`base/.claude/skills/` → the app's
   `.claude/skills/`); this profile no longer vendors it. If the app's
   `.claude/skills/frontend-design/` is missing, the kit was distributed
   incompletely — restore it before continuing, or step 5 leaves a dead
   pointer in the app's CLAUDE.md.
6. Copy `vitest.config.ts` → repo root. Vitest does not read tsconfig
   `paths`: without this alias bridge the first test importing via the
   project-canonical `@/*` form fails module resolution while `tsc`
   stays green — a red check/Stop-hook/CI with a misleading error.
   Match the alias target to the app's tsconfig `paths` mapping:
   `./src` with `--src-dir`, `.` without.
7. Copy `.npmrc` → repo root, before step 8's installs so they already
   resolve under it. The file's header comments are the sole home for
   what the two keys do and the npm-version caveat.
8. Install the dev dependencies the scripts expect (create-next-app
   provides only some): typescript, vitest, eslint (flat config),
   eslint-config-next (>= 16 — flat-native; needs `next` present at
   lint time), eslint-plugin-jsx-a11y, prettier. After a create-next-app
   scaffold, `npm i -D vitest prettier eslint-plugin-jsx-a11y` usually
   covers the gap.

Still manual afterwards: Role & Context, the project-specific invariant,
Invariant 1's `{{CHECK CMD}}` (fill with `npm run check`) and
`{{CI-EQUIVALENT CMD}}` (fill with `npm run check; npm test; npm run build`),
`{{FORMATTER}}` (Prettier), ADR-0001, and the app's first test —
`vitest run` exits 1 when no test files exist, so `check` (and with it the
Stop hook and CI) cannot go green until one is written; SETUP step 11
ASKs the user for it. Do NOT add `--passWithNoTests`; that weakens the
gate.

When the test suite gets slow, narrow the `check` script's test step to
changed/affected tests (e.g. `vitest run --changed`) — the gate must stay
fast; CI runs the full suite.
