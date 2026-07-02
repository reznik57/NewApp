<!-- template-version: 2026-07 -->
<!-- Replaces the Tech Stack and Commands sections of CLAUDE.md.
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
