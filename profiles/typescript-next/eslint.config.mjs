// template-version: 2026-07.4
// Profile ESLint config — replaces the one create-next-app generates.
// Layers enforced rule sets on the Next.js defaults (this header is the
// sole home for how they gate):
//   - jsx-a11y recommended: accessibility violations are errors and fail
//     `check` outright.
//   - no-warning-comments (warn) fails `check` via `--max-warnings 0`:
//     stale-marker comments don't ship — record deferred work with
//     /log-gotcha as a `deferred` entry in docs/wiki/log.md instead.
//   - no-restricted-syntax: focused/skipped tests (.only/.skip) are
//     errors — CLAUDE.md Invariant 2 (Test Integrity), mechanized. An
//     approved exception carries an eslint-disable comment whose diff is
//     the approval trail.
//   - ban-ts-comment: type-check suppressions are errors; @ts-expect-error
//     needs a description — CLAUDE.md Invariant 1's no-silent-suppression
//     rule, mechanized.
// eslint-config-next already registers the jsx-a11y and @typescript-eslint
// plugins, so only rule severities are layered here — re-registering a
// plugin object makes ESLint crash with "Cannot redefine plugin".
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
      "no-restricted-syntax": [
        "error",
        // Four selectors: bare (it.only) and one chained modifier deep
        // (it.concurrent.skip), each in dot and bracket notation — the
        // forms Vitest documents.
        {
          selector:
            "MemberExpression[object.name=/^(it|test|describe)$/][property.name=/^(only|skip)$/]",
          message:
            "Focused/skipped tests violate Invariant 2 (Test Integrity). An approved exception carries an eslint-disable comment — its diff is the approval trail.",
        },
        {
          selector:
            "MemberExpression[object.object.name=/^(it|test|describe)$/][property.name=/^(only|skip)$/]",
          message:
            "Focused/skipped tests violate Invariant 2 (Test Integrity). An approved exception carries an eslint-disable comment — its diff is the approval trail.",
        },
        {
          selector:
            "MemberExpression[object.name=/^(it|test|describe)$/][property.value=/^(only|skip)$/]",
          message:
            "Focused/skipped tests violate Invariant 2 (Test Integrity). An approved exception carries an eslint-disable comment — its diff is the approval trail.",
        },
        {
          selector:
            "MemberExpression[object.object.name=/^(it|test|describe)$/][property.value=/^(only|skip)$/]",
          message:
            "Focused/skipped tests violate Invariant 2 (Test Integrity). An approved exception carries an eslint-disable comment — its diff is the approval trail.",
        },
      ],
    },
  },
  {
    files: ["**/*.{ts,tsx,mts,cts}"],
    rules: {
      "@typescript-eslint/ban-ts-comment": [
        "error",
        { "ts-expect-error": "allow-with-description" },
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
