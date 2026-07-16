<!-- template-version: 2026-07.33 -->
<!-- Insert as a section in the app's AGENTS.md (the canon, never the
     CLAUDE.md bridge), after the stack profile's
     Stack Rules. Lean by design; full reference:
     docs/wiki/facilitated-session-ux.md. -->

## Domain Rules: facilitated session [Day-0]

- **The medium is an invariant, not a breakpoint.** Every view names its
  target: {{VIEW → resolution / reading distance, e.g. projector 1920x1080
  at 5 m; phone 390px in hand; paper A4 under stress}}. A projected view
  **never scrolls**: what does not fit the screen does not exist. Print
  views get their own stylesheet, not a squeezed screen layout.
- **Visibility is a design constraint.** For every view, what it must NOT
  show is written down: {{VIEW → what stays hidden, and from whom}}. Role
  and confidentiality rules decide the layout — they are never a filter
  added afterwards. When the room's views diverge, the shared screen goes
  quiet rather than leaking.
- **Verify in the target medium.** Screenshot at the real resolution, never
  "the browser window looked fine" — a 1036px window and a 1920px projection
  are two different layouts. A view that will be printed is verified as a
  print render.
- Before building or reshaping any of these surfaces, invoke
  `frontend-design` for the aesthetic direction, THEN
  `designing-facilitated-sessions`, whose five-point gate must be answered
  and approved BEFORE the first line of CSS. Full reference (the traps that
  cost real time): docs/wiki/facilitated-session-ux.md.
