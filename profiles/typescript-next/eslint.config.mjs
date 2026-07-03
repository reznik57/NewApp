// template-version: 2026-07.1
// Profile ESLint config — replaces the one create-next-app generates.
// Layers two enforced rule sets on the Next.js defaults (this header is
// the sole home for how they gate):
//   - jsx-a11y recommended: accessibility violations are errors and fail
//     `check` outright.
//   - no-warning-comments (warn) fails `check` via `--max-warnings 0`:
//     stale-marker comments don't ship — record deferred work with
//     /log-gotcha as a `deferred` entry in docs/wiki/log.md instead.
// eslint-config-next already registers the jsx-a11y plugin, so only rule
// severities are layered here — re-registering the plugin object makes
// ESLint crash with "Cannot redefine plugin".
import nextCoreWebVitals from "eslint-config-next/core-web-vitals";
import nextTypescript from "eslint-config-next/typescript";
import jsxA11y from "eslint-plugin-jsx-a11y";

const eslintConfig = [
  ...nextCoreWebVitals,
  ...nextTypescript,
  {
    files: ["**/*.{jsx,tsx}"],
    rules: { ...jsxA11y.flatConfigs.recommended.rules },
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
    ignores: [
      "node_modules/**",
      ".next/**",
      "out/**",
      "build/**",
      "coverage/**",
      "next-env.d.ts",
    ],
  },
];

export default eslintConfig;
