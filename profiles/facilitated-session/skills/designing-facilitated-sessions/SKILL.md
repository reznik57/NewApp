---
name: designing-facilitated-sessions
description: Domain gate for a surface that runs in a room in front of people — interactive presentation, exercise playbook, tabletop drill, training deck. Forces five answers (thesis, signature, type, medium, content logic) BEFORE any CSS, and pins medium and role-visibility as design constraints. Invoke AFTER frontend-design when building or reshaping any projected, printed, or role-split view. Not for ordinary responsive web UI.
---

<!-- template-version: 2026-07.31 -->

# Designing facilitated sessions

Guardrails for a surface a facilitator drives in a room, layered on top of
`frontend-design`. Invoke `frontend-design` FIRST — it owns the aesthetic
direction and the catalogue of AI-default looks to avoid. This skill does not
restate it. It adds what a room, a projector and a role split impose, and it
gates the work: **answer the five points and get them approved before writing
a line of CSS.**

## The five-point gate

State all five, show them to the user, wait for approval. Skipping ahead to
colors is how a deck ends up looking like every other deck.

1. **THESIS — what is true here that nobody says out loud?** Not "what is the
   app" — what is the unspoken truth of the situation. The tone follows from
   it. Worked example, a crisis-response drill: "the emergency starts out
   banal" — which rules out the Hollywood war-room look and yields a sober
   protocol in which a clock quietly runs. The thesis is a finding about the
   subject, and it precedes every color decision.
2. **SIGNATURE — the one element that embodies the thesis.** Not an ornament:
   the central truth made visible. In that same drill, a 72-hour bar IS the
   statutory reporting deadline, made physical — which is why the room later
   understands why a timestamp mattered in the first briefing. A stock
   progress widget could never have carried that. Everything else stays quiet.
3. **TYPE — in which typeface does the subject's own world label its things?**
   Anchor typography in the subject, not in taste. Check SYSTEM fonts first:
   they are offline-safe, and often the truer answer (a German drill labels
   its world the way German signage does; that face may already ship with the
   OS). A constraint like "no CDN" is not an obstacle here — it is what forces
   the better choice.
4. **MEDIUM — where is this actually read?** Projector at 5 m that never
   scrolls, at a fixed 1920x1080? Phone in the hand at 390px? Paper, read
   under stress? Name the hard consequences: what does not fit is cut, not
   shrunk; a print view is its own stylesheet; contrast is decided by the
   worst room, not the best monitor.
5. **CONTENT LOGIC — what does the content forbid?** Which view must NOT show
   what, and to whom? Role and confidentiality rules are design rules: when
   the participants' views diverge, the shared screen must go quiet. Draw
   that consequence or you build a pretty surface that defeats its own
   purpose.

## After approval

Build to the approved five points, then **verify in the target medium**:
render at the real resolution and look at it — a 1036px browser window and a
1920px projection are two different layouts, and the browser window is the
one that lies. A printed view is verified as a print render, not as a screen.

The traps this domain reliably springs — target-resolution verification,
locale-dependent date formatting, a CSS class silently colliding between two
output media, and tests that assert HTML formatting instead of behavior and
so break on every redesign — are worked through with their fixes in
docs/wiki/facilitated-session-ux.md.
