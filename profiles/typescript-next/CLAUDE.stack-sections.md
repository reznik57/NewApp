<!-- template-version: 2026-07.31 -->
<!-- Replaces the Tech Stack and Commands sections of CLAUDE.md and adds a
     Stack Rules section — insert it after Commands.
     Fill {{FORMATTER}} elsewhere in CLAUDE.md with: Prettier. -->

## Tech Stack [Day-0]

| Component                       | Version          | Why this / why pinned                              |
| ------------------------------- | ---------------- | -------------------------------------------------- |
| TypeScript                      | see package.json | strict mode on; the compiler is the first reviewer |
| Next.js (App Router)            | see package.json | file-based routing, server components              |
| Vitest                          | see package.json | fast, TS-native test runner                        |
| ESLint (flat config) + Prettier | see package.json | lint logic; formatting is Prettier's job alone     |

## Commands [Day-0]

The six-script contract lives in `package.json` (single source of truth):
`check` (THE gate), `test`, `test:one` (`npm run test:one -- "pattern"`),
`fix`, `dev`, `build`.

## Stack Rules [Day-0]

- Every UI surface handles all four states — loading, empty, error,
  success — and mutating actions tolerate double-clicks and mid-request
  refreshes.
- All input validation happens server-side (route handlers / server
  actions); client-side validation is UX, never enforcement.
- **Visual design is guidance, not a gate.** Accessibility IS mechanized
  — jsx-a11y violations fail `check` (see `eslint.config.mjs`) — but
  layout, typography, spacing, and color carry no rule here and can't be
  linted. When building or reshaping UI, invoke the `frontend-design`
  skill (ships with the harness at `.claude/skills/`) BEFORE writing
  component code — it steers palette, type, and layout away from templated
  defaults. A workflow pointer (like the ultrathink Deep-Analysis
  Protocol), not a style rule; Standing Rules keeps those out of CLAUDE.md.
