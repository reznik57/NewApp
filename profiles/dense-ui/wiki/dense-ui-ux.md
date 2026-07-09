<!-- template-version: 2026-07.25 -->

# Dense-UI UX reference

Full reference behind the `dense-ui` constraint profile. The hard rules live
in CLAUDE.md (Domain Rules: data-dense UI); this page carries the patterns,
exemplars, and sources.

## Status: anticipatory

No real app has driven this profile yet (v2.7.0). Treat it as a starting
hypothesis and correct it against the first real data-dense app.

## Pattern references — for the reasoning, not the skin

- IBM Carbon — the best fit for data-dense enterprise surfaces; explains
  WHY, not just how it looks.
- Atlassian, Shopify Polaris, Salesforce Lightning — tables, filters,
  permissions worked out in depth.
- Grafana, Cloudflare, Tailscale, Datadog — exemplars of keeping dense
  network/security data readable.

## The counter-example

The FortiGate console: dense but not scannable — the reference for what to
avoid. Density is a means to legibility, never an excuse to lose it.

## The rules that outweigh any reference

- Progressive disclosure over everything-at-once.
- Established table/filter/permission patterns, not reinvented ones.
- Keyboard-first; frequent actions reachable.
- Consistent, learnable structure over cleverness.

## Sources

- NN/g — usability studies over taste.
- The design systems above — public docs that justify their table, filter,
  and permission patterns.
