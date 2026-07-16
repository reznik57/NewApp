<!-- template-version: 2026-07.33 -->

# Kids-app UX reference

Full reference behind the `kids-app` constraint profile. The hard, always-on
rules live in AGENTS.md (Audience Rules: children); this page carries the
worked examples, sources, and reasoning.

## The two age bands

NN/g's children's research splits the range this profile targets:
- 6-8: read slowly, rely on image + text together, need heavy scaffolding.
- 9-12: read fluently, want to be taken seriously, resent being treated as
  little kids.
7 vs 10 therefore differ more than 30 vs 40. Pick the band per screen and
per feature; "7-10" as a single target is a smell.

## Reference products — studied as mechanism

- Scratch (MIT) — the reference for a serious tool that still fits kids.
- Klexikon — Wikipedia for kids; a masterclass in text reduction.
- Toca Boca, Sago Mini — interaction and exploration without text.
- ANTON — widely used in DE schools; a familiarity baseline.
- Duolingo — study its feedback, streaks, and error-tolerance; do NOT copy
  its manipulative patterns. Mechanism yes, dark pattern no.

## The rules that outweigh any reference

- Touch targets well above 44px; generous spacing (fine motor).
- No hover-only, no hidden gestures.
- Icon plus word, never icon alone.
- Onboarding by doing, not reading — kids skip text.
- Immediate, visible feedback; errors never sanction.
- No ads, no in-app purchases, no dark patterns.

## Sources and regulation

- NN/g Children's UX reports — the one solid empirical source.
- Apple HIG — kids-apps section. Google Play — "Designed for Families".
- DE legal: DSGVO Art. 8 (consent, age threshold 16 in Germany); JMStV.
