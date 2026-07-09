---
name: designing-for-children
description: Audience guardrails for UI aimed at children (roughly 7-10) — touch-target sizing, text-free onboarding, icon+word labeling, non-punishing feedback, and DE legal constraints (DSGVO Art. 8, JMStV). Invoke AFTER frontend-design when building or reshaping any child-facing surface. Not for general-audience or enterprise UI.
---

<!-- template-version: 2026-07.25 -->

# Designing for children

Guardrails for child-facing UI, layered on top of `frontend-design`. Invoke
`frontend-design` FIRST for the aesthetic direction; this skill does not
restate it — it adds the audience constraints that direction must respect.

## Design for the band, not the midpoint

7-10 is not homogeneous. NN/g splits 6-8 (read slowly, need image+text)
from 9-12 (want to be taken seriously, reject "little kid" treatment). The
gap between 7 and 10 is larger than between 30 and 40. Name the target band
before designing.

## Hard constraints

- Touch targets clearly larger than 44px; generous spacing — fine motor is
  still developing.
- No hover-only interactions; no hidden gestures.
- Icon PLUS word, never icon alone.
- Onboard by doing, not by reading — kids skip text consistently.
- Immediate, visible feedback on every action; errors never punish.
- No ads, no in-app purchases, no dark patterns.
- Legal (DE): DSGVO Art. 8 (consent; age threshold 16 in Germany), JMStV.

## Study the mechanism, not the skin

Reference products for HOW they work, never to copy a look: Scratch (a
serious tool that respects kids), Klexikon (text reduction), Toca Boca /
Sago Mini (text-free exploration), ANTON (DE schools). Duolingo's feedback
and error-tolerance mechanics are worth studying — its manipulative streak
patterns are not. Reference the mechanism, never the dark pattern.

Full reference and sources (NN/g Children's UX, Apple HIG kids, Google Play
Designed for Families): docs/wiki/kids-app-ux.md.
