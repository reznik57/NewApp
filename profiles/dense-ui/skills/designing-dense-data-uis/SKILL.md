---
name: designing-dense-data-uis
description: Domain guardrails for data-dense operational UIs — dashboards, monitoring, network/security consoles, admin tables. Progressive disclosure, established table/filter/permission patterns, keyboard-first, scannability over cleverness. Invoke AFTER frontend-design when building or reshaping any high-density data surface. Not for marketing pages or low-density consumer UI.
---

<!-- template-version: 2026-07.25 -->

# Designing dense data UIs

Guardrails for high-density operational UI, layered on top of
`frontend-design`. Invoke `frontend-design` FIRST for aesthetic direction;
this skill adds the constraints that direction must respect when the screen
carries a lot of data at once.

## Hard constraints

- Density must stay legible: progressive disclosure beats showing everything
  at once. Reveal detail on demand.
- Tables, filters, and permission UIs follow an established data-dense
  system (Carbon is the reference) — solved problems, don't reinvent them.
- Keyboard-first for power users; frequent actions stay reachable.
- Consistent, learnable structure over cleverness.

## The counter-example is the lesson

Dense is not cramped. The FortiGate console is the canonical
counter-example: maximum data, minimum scannability. Study the exemplars for
how they keep dense data readable — Grafana, Cloudflare, Tailscale,
Datadog — and the counter-example for what to avoid.

Full reference (Carbon / Polaris / Lightning for tables, filters,
permissions; NN/g): docs/wiki/dense-ui-ux.md.
