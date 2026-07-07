// template-version: 2026-07.19
import { fileURLToPath } from "node:url";
import { defineConfig } from "vitest/config";

// Vitest does not read tsconfig "paths" — this alias mirrors the app's
// `@/*` mapping so alias imports resolve in tests exactly as they do
// under tsc and Next. Scaffolded without `--src-dir`? Then tsconfig maps
// `@/*` to `./*` — point the alias at "." instead of "./src".
// Config-only on purpose: no plugin dependency.
export default defineConfig({
  resolve: {
    alias: { "@": fileURLToPath(new URL("./src", import.meta.url)) },
  },
});
