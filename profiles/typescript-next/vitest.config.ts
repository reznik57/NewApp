// template-version: 2026-07.19
import { fileURLToPath } from "node:url";
import { defineConfig } from "vitest/config";

// Vitest does not read tsconfig "paths" — this alias mirrors the scaffold's
// `@/*` → `./src/*` mapping so alias imports resolve in tests exactly as
// they do under tsc and Next. Config-only on purpose: no plugin dependency.
export default defineConfig({
  resolve: {
    alias: { "@": fileURLToPath(new URL("./src", import.meta.url)) },
  },
});
