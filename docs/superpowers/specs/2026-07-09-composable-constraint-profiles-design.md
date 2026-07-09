# Composable constraint profiles (kids-app, dense-ui) — design

Round: v2.7.0 (changelog header `2026-07.25`). Branch:
`v2.7.0-constraint-profiles`.

## Origin

User-requested, not app backflow. Prompted by a curated design-reference
list (professional products + kids products) the user shared and asked to
analyze. The analysis surfaced the useful distinction — *constraint*
references (rules, empirical UX, legal) age well; *taste* references (copy
Stripe/Linear) collapse into the AI-default look. This spec turns the
constraint half into a reusable seed asset.

Anchoring against the "real incidents, not drawing-board" rule
(CLAUDE.md → Template discipline):

- `kids-app` is anchored to a real app: `fisi-learning` (a children's
  learning app that already exists).
- `dense-ui` has NO real app incident yet. It is delivered as
  anticipatory structure, motivated by the user's own network/security
  domain. This is an explicit owner override of the backflow rule and is
  recorded as such in the changelog (precedent: v2.5.1 shipped
  forward-looking structure, honestly labeled). Validation trigger: the
  first real data-dense app seeded from the template.

## The problem

The current profile model is single-axis and stack-keyed: SETUP step 0
picks a stack, step 2 overlays exactly one matching profile
(`typescript-next`), "No profile for the chosen stack? Skip." Audience/
domain constraints (kids UX, data-density UX) are orthogonal to the
stack — a real app is `typescript-next` AND `kids-app` at once. The
one-profile-per-stack model has no home for that composition.

## The design

### 1 — Two profile kinds on orthogonal axes

- **Stack profiles** (`typescript-next`): tooling + stack CLAUDE
  sections. Exactly one per app, chosen by stack at SETUP step 0/2.
- **Constraint profiles** (`kids-app`, `dense-ui`): audience/domain
  guidance. Zero-to-many per app, overlaid AFTER the stack profile.

A new `profiles/README.md` is the single home for this concept: what the
two kinds are, that constraint profiles compose on top of the stack
profile, and the application order. Without it the second axis violates
"one fact, one home" the moment it exists.

### 2 — What each constraint profile ships

```
profiles/<name>/
  README.md                      # overlay how-to; template-version stamped
  CLAUDE.constraints-section.md  # hard invariants → app CLAUDE.md (lean)
  skills/<skill>/SKILL.md        # vendored skill, invoked before UI build
  wiki/<name>-ux.md              # full reference → app docs/wiki/
```

Split rationale (SETUP step 8 budget discipline — CLAUDE.md has a
~190-line wiki-lint ceiling that profile sections count against): the
HARD, non-negotiable invariants go lean into CLAUDE.md; the FULL
reference (good/bad examples, external pointers, the counter-examples)
goes to `docs/wiki/` with a pointer. The CLAUDE section ends with a
pointer to the vendored skill, mirroring how the stack profile's Stack
Rule points at `frontend-design`.

The vendored skills are NEW, seed-authored (no external license file —
unlike `frontend-design`, which the stack profile vendors under
Apache-2.0 with its LICENSE.txt).

### 3 — Skill composition (the key nuance)

The constraint skills must NOT restate `frontend-design`'s aesthetic
method — they layer on top of it. Order: `frontend-design` sets the
subject-first aesthetic direction, THEN the constraint skill applies the
audience guardrails. This is the process→implementation pattern from
using-superpowers, one level deeper: direction first, non-negotiable
constraints as an overlay. Each SKILL.md states "invoke AFTER
frontend-design; do not restate its method."

Shared anti-pattern encoded in both skills: reference the *mechanism*,
never the *dark pattern* (Duolingo's feedback/streak mechanics are worth
studying; its manipulative patterns are not) — the exact distinction from
the reference list that motivated this round.

### 4 — Constraint content (so the plan inherits substance, not TBDs)

**kids-app — hard invariants (→ CLAUDE section):**
- 7–10 is not homogeneous: NN/g splits 6–8 (read slowly, need image+text)
  from 9–12 (reject being treated as little kids). Design for the band,
  not the midpoint.
- Touch targets clearly larger than 44px; generous spacing — fine motor
  is still developing.
- No hover-only interactions; no hidden gestures.
- Icon PLUS word, never icon alone.
- Onboarding by doing, not by reading — kids skip text.
- Immediate, visible feedback on every action; errors never punish.
- No ads, no in-app purchases, no dark patterns.
- Legal (DE): DSGVO Art. 8 (consent, age threshold 16 in Germany);
  JMStV.

**kids-app — full reference (→ docs/wiki):** reference products studied
as MECHANISM, not skin — Scratch (a serious tool for kids), Klexikon
(text reduction), Toca Boca / Sago Mini (text-free exploration), ANTON
(DE schools). Age-band detail. Pointers: NN/g Children's UX reports
(the one solid empirical source), Apple HIG kids section, Google Play
"Designed for Families." Duolingo caveat: mechanism yes, dark patterns
no.

**dense-ui — hard invariants (→ CLAUDE section):**
- Density must stay legible: progressive disclosure over showing
  everything at once.
- Table / filter / permission patterns follow an established data-dense
  system (Carbon is the reference); don't reinvent them.
- Keyboard-first for power users; frequent actions stay reachable.
- Consistent, learnable structure over cleverness.
- The FortiGate anti-pattern: dense is not the same as cramped or
  unscannable — named explicitly as the counter-example.

**dense-ui — full reference (→ docs/wiki):** Carbon / Polaris / Salesforce
Lightning for tables, filters, permissions. Grafana / Cloudflare /
Tailscale / Datadog as legibility exemplars. FortiGate as the
counter-example. NN/g for usability grounding.

### 5 — Naming

- Profiles: `kids-app`, `dense-ui`.
- Skills: `designing-for-children`, `designing-dense-data-uis` (gerund
  convention, cf. `writing-plans`).

## SETUP & docs integration

- SETUP step 2 gains a sub-point: after the stack profile, optionally
  overlay 0..n constraint profiles, pointing at `profiles/README.md`.
- **Mirror consequence:** `SETUP.md` is byte-mirrored into the kit
  (`test_kit_parity`). The SETUP edit must re-sync the kit copy in the
  SAME commit or the parity test goes red. `profiles/` itself is
  seed-only (not mirrored) — the new profiles need no parity.

## Verification gate

- `py -m pytest tests -q` green before every commit.
- New test `tests/hooks/test_constraint_profiles.py`: for each constraint
  profile, assert README.md carries a `template-version:` stamp and that
  `CLAUDE.constraints-section.md`, `skills/<name>/SKILL.md`, and a
  `wiki/` reference exist. Light structural drift guard.
- Template-version: re-stamp every stamped file touched (each profile
  README, each CLAUDE.constraints-section.md, each SKILL.md,
  profiles/README.md) to `2026-07.25`.
- TEMPLATE-CHANGELOG entry `2026-07.25 — v2.7.0`: `kids-app` incident-
  anchored (fisi-learning); `dense-ui` honestly labeled anticipatory
  with its validation trigger.
- Release: round branch → `--no-ff` merge to master → annotated tag
  `v2.7.0` on the merge → verify remote → push master + tag together.

## Out of scope (YAGNI)

- No new `check` gate for the constraints — most (touch size, icon+word,
  no hover) are not generically lintable; accessibility is already
  mechanized by the stack profile's jsx-a11y rules. Guidance, not gate.
- No third constraint profile beyond the two chosen.
- No per-tool adapter wiring (cf. v2.5.1 rejection).
