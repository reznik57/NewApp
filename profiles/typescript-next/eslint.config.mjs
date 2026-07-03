// template-version: 2026-07.1
// Profile ESLint config — replaces the one create-next-app generates.
// Layers two enforced rules on the Next.js defaults; both fail the `check`
// gate via `eslint . --max-warnings 0` (and CI with it):
//   - jsx-a11y flat recommended: accessibility violations block the turn.
//   - no-warning-comments: TODO/FIXME/HACK don't ship — deferred work is
//     recorded via /log-gotcha as a `deferred` entry in docs/wiki/log.md.
import { FlatCompat } from "@eslint/eslintrc";
import jsxA11y from "eslint-plugin-jsx-a11y";

const compat = new FlatCompat({ baseDirectory: import.meta.dirname });

export default [
  ...compat.extends("next/core-web-vitals", "next/typescript"),
  {
    ...jsxA11y.flatConfigs.recommended,
    files: ["**/*.{jsx,tsx}"],
  },
  {
    rules: {
      "no-warning-comments": [
        "warn",
        { terms: ["todo", "fixme", "hack"], location: "anywhere" },
      ],
    },
  },
  {
    ignores: [".next/**", "node_modules/**", "coverage/**"],
  },
];
