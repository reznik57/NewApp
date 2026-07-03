<!-- template-version: 2026-07.1 -->

# Profile: TypeScript / Next.js

Overlay for the stack-agnostic `base/`. Apply AFTER copying `base/*` into
the new repo (SETUP.md step 2):

1. Merge `package-scripts.json` → the `"scripts"` block of the app's
   `package.json` (created by `create-next-app` or `npm init`).
2. Copy `settings.json` → `.claude/settings.json` (replaces renaming the
   base template; already filled for npm/next/vitest/eslint/tsc).
   Delete `.claude/settings.template.json` afterwards.
3. Copy `ci.yml` → `.github/workflows/ci.yml` (replaces ci.template.yml).
4. Copy `eslint.config.mjs` → repo root, replacing the one create-next-app
   generated. It layers two enforced rules on the Next.js defaults —
   jsx-a11y (accessibility) and no-warning-comments (no TODO/FIXME in
   shipped code); both fail `check` via `--max-warnings 0`.
5. Replace the `Tech Stack` and `Commands` sections of CLAUDE.md with the
   contents of `CLAUDE.stack-sections.md` (includes the `Stack Rules`
   section — keep it).

Still manual afterwards: Role & Context, the project-specific invariant,
Invariant 1's `{{CHECK CMD}}` (fill with `npm run check`) and
`{{CI-EQUIVALENT CMD}}` (fill with `npm run check; npm test; npm run build`),
`{{FORMATTER}}` (Prettier), and ADR-0001. Dev dependencies expected by the
scripts: typescript, vitest, eslint (flat config), @eslint/eslintrc,
eslint-plugin-jsx-a11y, prettier.

When the test suite gets slow, narrow the `check` script's test step to
changed/affected tests (e.g. `vitest run --changed`) — the gate must stay
fast; CI runs the full suite.
