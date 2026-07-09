# Composable Constraint Profiles Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a second, orthogonal profile axis to the seed — constraint profiles (`kids-app`, `dense-ui`) that overlay on top of the stack profile — plus the structural guard, SETUP pointer, and changelog for the v2.7.0 round.

**Architecture:** Constraint profiles live in `profiles/` (seed-only, never mirrored into the kit). Each ships a stamped README, a lean CLAUDE section (hard invariants), a vendored skill that layers on `frontend-design`, and a docs/wiki reference. `profiles/README.md` is the single home for the two-axis concept. A new structural test pins each profile's shape. All guidance, no new `check` gate.

**Tech Stack:** Plain Markdown, one Python `unittest` test (the seed suite is stdlib unittest, run via `py -m pytest tests -q`). No app runtime.

## Global Constraints

- Template-version stamp on every stamped file: `2026-07.25` (this round's changelog header). Format: `<!-- template-version: 2026-07.25 -->`. SKILL.md files carry the stamp on the line AFTER the frontmatter `---`, matching `harness-kit/.claude/skills/ultrathink/SKILL.md`.
- The test suite must be GREEN before every commit (`py -m pytest tests -q` from the seed root; one env-gated symlink skip on Windows is normal). No committing a red test — build structure first, add its guard once green.
- `profiles/` is seed-only and NOT in the kit manifest — new profiles need no parity.
- `SETUP.md` IS byte-mirrored into `harness-kit/SETUP.md` (`tests/hooks/test_kit_parity.py`, MANIFEST). Any SETUP edit must re-sync the kit copy in the SAME commit: `cp SETUP.md harness-kit/SETUP.md`.
- `SETUP.md` is NOT in `tests/hooks/test_root_docs.py` REQUIRED, and `TEMPLATE-CHANGELOG.md` is only appended to (anchors preserved) — so no REQUIRED update is needed this round.
- Skill composition rule (verbatim intent): each constraint skill layers on `frontend-design` and must NOT restate its aesthetic method — direction first, guardrails second.
- Anti-pattern encoded in both skills: reference the mechanism, never the dark pattern.
- Working on branch `v2.7.0-constraint-profiles` (already created; the spec is committed there as `54f5514`).

---

### Task 1: Axis home — `profiles/README.md`

**Files:**
- Create: `profiles/README.md`

**Interfaces:**
- Produces: the documented concept "stack profiles vs constraint profiles" that SETUP step 2 (Task 5) and the changelog (Task 6) point at. No code symbols.

- [ ] **Step 1: Create `profiles/README.md`** with exactly:

```markdown
<!-- template-version: 2026-07.25 -->

# Profiles

Overlays for the stack-agnostic harness. Two orthogonal kinds; an app may
take one stack profile and any number of constraint profiles.

## Stack profiles

Keyed to the tech stack chosen at SETUP step 0. Ship build tooling, the
CLAUDE.md Tech Stack / Commands / Stack Rules sections, settings, CI, and
(for TS/Next) a vendored `frontend-design` skill. Exactly one per app —
SETUP step 2 applies it. Current: `typescript-next/`.

## Constraint profiles

Keyed to the app's AUDIENCE or DOMAIN, not its stack — orthogonal to the
stack profile and composable with it. A children's learning app is
`typescript-next` AND `kids-app`. Zero-to-many per app, overlaid AFTER the
stack profile (SETUP step 2). Current: `kids-app/`, `dense-ui/`.

Each ships:
- `README.md` — the overlay how-to (which file goes where).
- `CLAUDE.constraints-section.md` — the hard, non-negotiable invariants,
  inserted as a section into the app's CLAUDE.md. Kept lean: it counts
  against the CLAUDE.md line budget (SETUP step 8), so the full material
  lives in the wiki page and this section points at it.
- `skills/<name>/SKILL.md` — a skill invoked BEFORE building UI for that
  audience. It layers on top of `frontend-design` (which sets the aesthetic
  direction); it does not restate it.
- `wiki/<name>-ux.md` — the full reference (worked examples, empirical
  sources, legal pointers), copied into the app's `docs/wiki/`.

Constraint profiles carry no `check` gate: touch-target size, icon+word,
no-hover and the like are not generically lintable. Accessibility that IS
mechanized (jsx-a11y) rides on the stack profile. These profiles are
guidance — enforced by review and the skill, not by the build.

Profiles live in the SEED only, never inside `harness-kit/`.
```

- [ ] **Step 2: Verify the suite is still green**

Run: `py -m pytest tests -q`
Expected: PASS (no test references this file yet; nothing broke).

- [ ] **Step 3: Commit**

```bash
git add profiles/README.md
git commit -m "docs(profiles): axis home for stack vs constraint profiles (v2.7.0)"
```

---

### Task 2: `kids-app` constraint profile

**Files:**
- Create: `profiles/kids-app/README.md`
- Create: `profiles/kids-app/CLAUDE.constraints-section.md`
- Create: `profiles/kids-app/skills/designing-for-children/SKILL.md`
- Create: `profiles/kids-app/wiki/kids-app-ux.md`

**Interfaces:**
- Consumes: the axis concept from Task 1 (referenced in prose only).
- Produces: a constraint profile with the four parts Task 4's test asserts — a stamped `README.md`, `CLAUDE.constraints-section.md`, `skills/*/SKILL.md`, `wiki/*.md`.

- [ ] **Step 1: Create `profiles/kids-app/README.md`** with exactly:

```markdown
<!-- template-version: 2026-07.25 -->

# Constraint profile: kids-app

Audience overlay for apps whose users are children (roughly 7-10). Apply
AFTER the stack profile, once `harness-kit/` is distributed. Orthogonal to
the stack — compose it with `typescript-next` or any other.

1. Insert `CLAUDE.constraints-section.md` as a new section in the app's
   CLAUDE.md, after the stack profile's Stack Rules (still named
   `CLAUDE.template.md` at overlay time). Keep it lean — it counts against
   the CLAUDE.md line budget (SETUP step 8). Its last bullet points at the
   `designing-for-children` skill, so step 2 is REQUIRED alongside it.
2. Copy `skills/designing-for-children/` -> `.claude/skills/`.
3. Copy `wiki/kids-app-ux.md` -> the app's `docs/wiki/`, and add its line to
   the wiki index (per the wiki-lint skill).

Non-negotiable regardless of stack: the legal pointers (DSGVO Art. 8,
JMStV) are jurisdiction facts, not style — keep them even if you trim.
```

- [ ] **Step 2: Create `profiles/kids-app/CLAUDE.constraints-section.md`** with exactly:

```markdown
<!-- template-version: 2026-07.25 -->
<!-- Insert as a section in the app's CLAUDE.md, after the stack profile's
     Stack Rules. Lean by design; full reference: docs/wiki/kids-app-ux.md. -->

## Audience Rules: children (7-10) [Day-0]

- 7-10 is not one audience: design for the band (6-8 read slowly, need
  image+text; 9-12 reject being treated as little kids), not the midpoint.
- Touch targets clearly larger than 44px, with generous spacing — fine
  motor is still developing.
- No hover-only interactions and no hidden gestures; icon PLUS word, never
  icon alone.
- Onboard by doing, not by reading — kids skip text. Every action gets
  immediate, visible feedback; errors never punish.
- No ads, no in-app purchases, no dark patterns.
- Legal (DE): DSGVO Art. 8 (consent; age threshold 16 in Germany), JMStV.
- Before building or reshaping UI, invoke `frontend-design` for aesthetic
  direction, THEN `designing-for-children` for these guardrails. Full
  reference (worked examples, sources): docs/wiki/kids-app-ux.md.
```

- [ ] **Step 3: Create `profiles/kids-app/skills/designing-for-children/SKILL.md`** with exactly:

```markdown
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
```

- [ ] **Step 4: Create `profiles/kids-app/wiki/kids-app-ux.md`** with exactly:

```markdown
<!-- template-version: 2026-07.25 -->

# Kids-app UX reference

Full reference behind the `kids-app` constraint profile. The hard, always-on
rules live in CLAUDE.md (Audience Rules: children); this page carries the
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
```

- [ ] **Step 5: Verify the suite is still green**

Run: `py -m pytest tests -q`
Expected: PASS (no test references these files yet).

- [ ] **Step 6: Commit**

```bash
git add profiles/kids-app
git commit -m "feat(profiles): kids-app constraint profile, fisi-learning-anchored (v2.7.0)"
```

---

### Task 3: `dense-ui` constraint profile

**Files:**
- Create: `profiles/dense-ui/README.md`
- Create: `profiles/dense-ui/CLAUDE.constraints-section.md`
- Create: `profiles/dense-ui/skills/designing-dense-data-uis/SKILL.md`
- Create: `profiles/dense-ui/wiki/dense-ui-ux.md`

**Interfaces:**
- Produces: the second constraint profile Task 4's test asserts (same four parts as Task 2).

- [ ] **Step 1: Create `profiles/dense-ui/README.md`** with exactly:

```markdown
<!-- template-version: 2026-07.25 -->

# Constraint profile: dense-ui

Domain overlay for data-dense operational UIs — dashboards, monitoring,
network/security consoles, admin tables. Apply AFTER the stack profile.
Orthogonal to the stack; compose it freely.

1. Insert `CLAUDE.constraints-section.md` as a new section in the app's
   CLAUDE.md, after the stack profile's Stack Rules. Keep it lean — it
   counts against the CLAUDE.md line budget (SETUP step 8). Its last bullet
   points at the `designing-dense-data-uis` skill, so step 2 is REQUIRED
   alongside it.
2. Copy `skills/designing-dense-data-uis/` -> `.claude/skills/`.
3. Copy `wiki/dense-ui-ux.md` -> the app's `docs/wiki/`, and add its line to
   the wiki index (per the wiki-lint skill).

Status: anticipatory. No real app has driven this profile yet (v2.7.0
changelog) — validate and correct it against the first real data-dense app.
```

- [ ] **Step 2: Create `profiles/dense-ui/CLAUDE.constraints-section.md`** with exactly:

```markdown
<!-- template-version: 2026-07.25 -->
<!-- Insert as a section in the app's CLAUDE.md, after the stack profile's
     Stack Rules. Lean by design; full reference: docs/wiki/dense-ui-ux.md. -->

## Domain Rules: data-dense UI [Day-0]

- Density must stay legible: progressive disclosure over showing everything
  at once.
- Follow an established data-dense system for tables, filters, and
  permissions (Carbon is the reference) — don't reinvent them.
- Keyboard-first for power users; frequent actions stay reachable, never
  buried.
- Consistent, learnable structure over cleverness.
- Dense is not cramped: the FortiGate console is the counter-example — data
  density must never cost scannability.
- Before building or reshaping UI, invoke `frontend-design` for aesthetic
  direction, THEN `designing-dense-data-uis` for these guardrails. Full
  reference: docs/wiki/dense-ui-ux.md.
```

- [ ] **Step 3: Create `profiles/dense-ui/skills/designing-dense-data-uis/SKILL.md`** with exactly:

```markdown
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
```

- [ ] **Step 4: Create `profiles/dense-ui/wiki/dense-ui-ux.md`** with exactly:

```markdown
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
```

- [ ] **Step 5: Verify the suite is still green**

Run: `py -m pytest tests -q`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add profiles/dense-ui
git commit -m "feat(profiles): dense-ui constraint profile, anticipatory (v2.7.0)"
```

---

### Task 4: Structural guard test

**Files:**
- Create: `tests/hooks/test_constraint_profiles.py`

**Interfaces:**
- Consumes: the profile trees from Tasks 1-3 (`profiles/README.md`, `profiles/kids-app/`, `profiles/dense-ui/`).
- Produces: `ConstraintProfileShapeTests` in the seed suite.

- [ ] **Step 1: Write the test** `tests/hooks/test_constraint_profiles.py` with exactly:

```python
"""Structural guard for constraint profiles (the second profile axis).

Stack profiles (typescript-next) are keyed to the tech stack; constraint
profiles are keyed to audience/domain and compose on top. profiles/README.md
is the single home for that distinction. This test pins the shape of each
constraint profile so a half-added one (missing skill, unstamped README,
absent wiki reference) fails the suite instead of shipping silently.
Run from the seed root: python -m unittest discover -s tests
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROFILES = ROOT / "profiles"
CONSTRAINT_PROFILES = ("kids-app", "dense-ui")
STAMP = re.compile(r"template-version:\s*\d{4}-\d{2}\.\d+")


def is_stamped(path):
    return bool(STAMP.search(path.read_text(encoding="utf-8")))


class ConstraintProfileShapeTests(unittest.TestCase):
    def test_axis_readme_exists_and_is_stamped(self):
        readme = PROFILES / "README.md"
        self.assertTrue(readme.is_file(), "profiles/README.md missing")
        self.assertTrue(is_stamped(readme), "profiles/README.md unstamped")

    def test_each_constraint_profile_has_its_four_parts(self):
        for name in CONSTRAINT_PROFILES:
            base = PROFILES / name
            readme = base / "README.md"
            claude = base / "CLAUDE.constraints-section.md"
            self.assertTrue(readme.is_file(), "%s: README.md missing" % name)
            self.assertTrue(is_stamped(readme), "%s: README unstamped" % name)
            self.assertTrue(
                claude.is_file(),
                "%s: CLAUDE.constraints-section.md missing" % name,
            )
            skills = list((base / "skills").glob("*/SKILL.md"))
            self.assertTrue(skills, "%s: no skills/*/SKILL.md" % name)
            wiki = list((base / "wiki").glob("*.md"))
            self.assertTrue(wiki, "%s: no wiki/*.md reference" % name)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Prove the guard bites (temporary red)**

Temporarily rename one part to a NON-`.md` extension (renaming to another
`.md` name would still satisfy the `*.md` glob and falsely pass), run only
the new test, confirm it FAILS, then restore:

```bash
mv profiles/kids-app/wiki/kids-app-ux.md profiles/kids-app/wiki/kids-app-ux.bak
py -m pytest tests/hooks/test_constraint_profiles.py -q   # expect FAIL: "kids-app: no wiki/*.md reference"
mv profiles/kids-app/wiki/kids-app-ux.bak profiles/kids-app/wiki/kids-app-ux.md
```

Expected: the middle command FAILS on the wiki assertion; after restore the file is back.

- [ ] **Step 3: Run the full suite green**

Run: `py -m pytest tests -q`
Expected: PASS (profiles from Tasks 1-3 satisfy every assertion).

- [ ] **Step 4: Commit**

```bash
git add tests/hooks/test_constraint_profiles.py
git commit -m "test(profiles): structural guard for constraint profiles (v2.7.0)"
```

---

### Task 5: SETUP step 2 pointer + kit re-sync

**Files:**
- Modify: `SETUP.md` (step 2, after the "No profile for the chosen stack? Skip" sentence)
- Modify: `harness-kit/SETUP.md` (re-synced copy — do NOT hand-edit; `cp` from root)

**Interfaces:**
- Consumes: `profiles/README.md` (Task 1), referenced by name in the new sentence.

- [ ] **Step 1: Edit `SETUP.md` step 2.** Find this line (end of step 2):

```
      No profile for the chosen stack? Skip — CLAUDE.template.md's
      ADAPT notes and step 4 carry the non-npm path.
```

Replace it with:

```
      No profile for the chosen stack? Skip — CLAUDE.template.md's
      ADAPT notes and step 4 carry the non-npm path.
      Then, orthogonally, overlay any CONSTRAINT profiles — audience/domain
      guardrails composable with the stack profile (e.g. `kids-app`,
      `dense-ui`). Zero is fine; `profiles/README.md` explains the two
      profile kinds, and each constraint profile's README lists its steps.
```

- [ ] **Step 2: Re-sync the kit copy (do not hand-edit it)**

```bash
cp SETUP.md harness-kit/SETUP.md
```

- [ ] **Step 3: Re-stamp check for SETUP.md**

SETUP.md carries no `template-version` stamp of its OWN (it is a checklist,
not a stamped template). It does mention the concept twice in prose (steps
telling the user to KEEP other files' stamps — CLAUDE.template.md line 1,
ci.yml), so a raw count is non-zero. Confirm those are the only matches and
take no action:

Run: `grep -n "template-version" SETUP.md`
Expected: only prose mentions (no `<!-- template-version: ... -->` stamp
line). If a real stamp line appears, re-stamp it to `2026-07.25` and re-run
Step 2.

- [ ] **Step 4: Run the full suite green (kit parity must pass)**

Run: `py -m pytest tests -q`
Expected: PASS — `test_kit_parity` confirms `SETUP.md` == `harness-kit/SETUP.md` byte-for-byte.

- [ ] **Step 5: Commit**

```bash
git add SETUP.md harness-kit/SETUP.md
git commit -m "docs(setup): step 2 points at constraint profiles; kit re-synced (v2.7.0)"
```

---

### Task 6: Changelog entry + README Map check + final green

**Files:**
- Modify: `TEMPLATE-CHANGELOG.md` (prepend the v2.7.0 entry after the intro block, before `## 2026-07.24 — v2.6.5`)
- Possibly modify: `README.md` (only if its `## Map` enumerates profiles — see Step 2)

**Interfaces:**
- Consumes: everything from Tasks 1-5.

- [ ] **Step 1: Measure the suite size for the changelog line**

Run: `py -m pytest tests -q | tail -1`
Note the passed count as `M` (the after-count). The v2.6.5 entry recorded 87; `M` is that plus the new test methods.

- [ ] **Step 2: Check `README.md` `## Map`.** Read the `## Map` section:

Run: `grep -n "typescript-next\|profiles/" README.md`

- If it does NOT name individual profiles (only a generic `profiles/` mention or none), make NO change to README.md — the profile-axis concept's home is `profiles/README.md`.
- If it enumerates `typescript-next` explicitly, add one sentence in the same list: `Constraint profiles (\`kids-app\`, \`dense-ui\`) overlay on top — see \`profiles/README.md\`.` Keep every existing `## Map` anchor intact (root-docs guard).

- [ ] **Step 3: Prepend the v2.7.0 entry** to `TEMPLATE-CHANGELOG.md`, immediately before the `## 2026-07.24 — v2.6.5` line, with exactly (replace `M` with the measured count from Step 1):

```markdown
## 2026-07.25 — v2.7.0

Composable constraint profiles — a user-requested asset, not app backflow.
Origin: a design-reference analysis (professional vs. kids product lists)
that separated durable CONSTRAINT references (rules, empirical UX, legal)
from taste references (copy Stripe/Linear) that collapse into the AI-default
look. This round turns the constraint half into a reusable seed asset.

- **Second profile axis** (profiles/README.md — the concept's single home):
  the existing model is one stack-keyed profile per app. Audience/domain
  constraints are orthogonal — a real app is `typescript-next` AND
  `kids-app` at once. Constraint profiles overlay on top of the stack
  profile; zero-to-many per app. SETUP step 2 gained the overlay pointer
  (re-mirrored into the kit, test_kit_parity).
- **kids-app profile** — incident-anchored to the real fisi-learning app.
  Ships lean CLAUDE Audience Rules (touch>44px, icon+word, no hover,
  text-free onboarding, non-punishing feedback, DSGVO Art. 8 / JMStV), a
  `designing-for-children` skill that layers on frontend-design (not a
  restatement), and a docs/wiki reference. Guidance, not a check gate — the
  constraints are not generically lintable; a11y rides on the stack profile.
- **dense-ui profile** — HONESTLY anticipatory: no real data-dense app has
  driven it (owner override of the "real incidents, not drawing-board" rule;
  precedent v2.5.1's forward-looking recipe). Same shape; Carbon patterns,
  the FortiGate counter-example, keyboard-first. Validation trigger: the
  first real data-dense app seeded from the template.
- **Structural guard** (tests/hooks/test_constraint_profiles.py): pins each
  constraint profile's four parts (stamped README, CLAUDE section, a skill,
  a wiki reference) and the axis README. Suite 87 -> M passed.

Deliberately open, with owner and trigger (not gaps — decisions):
- A third constraint profile beyond kids-app/dense-ui — trigger: a real app
  in a new audience/domain. No drawing-board additions.
- Mechanized enforcement of any constraint — trigger: a constraint that is
  genuinely lintable in a real app's stack. Today all are guidance.

```

- [ ] **Step 4: Final full-suite green**

Run: `py -m pytest tests -q`
Expected: PASS (root-docs guard still green — changelog anchors intact, README anchors intact).

- [ ] **Step 5: Commit**

```bash
git add TEMPLATE-CHANGELOG.md README.md
git commit -m "docs(changelog): v2.7.0 constraint profiles round"
```

---

### Task 7: Release (requires user authorization for the push)

**Not auto-run.** Pushing is outward-facing — confirm with the user first, and honor the repo-identity guard (CLAUDE.md).

- [ ] **Step 1: Verify repo identity before anything**

Run: `git remote -v`
Expected: `origin` points at the TEMPLATE repo, never an app. If the pre-push guard is not yet active in this clone, run `git config core.hooksPath .githooks` and `py .githooks/pre_push_guard.py --self-test`.

- [ ] **Step 2: Merge no-ff into master**

```bash
git checkout master
git merge --no-ff v2.7.0-constraint-profiles -m "Merge v2.7.0-constraint-profiles: composable constraint profiles (kids-app, dense-ui)"
```

- [ ] **Step 3: Annotated tag on the merge commit**

```bash
git tag -a v2.7.0 -m "v2.7.0 — composable constraint profiles"
```

- [ ] **Step 4: Push master + tag together (AFTER user go-ahead)**

```bash
git push origin master v2.7.0
```

---

## Self-Review

**1. Spec coverage:**
- Axis model (spec §1) → Task 1 (profiles/README.md) + Task 5 (SETUP pointer). ✓
- Per-profile file layout (spec §2) → Tasks 2, 3 (four files each). ✓
- Skill composition, layered on frontend-design (spec §3) → SKILL.md bodies in Tasks 2, 3. ✓
- Constraint content (spec §4) → CLAUDE sections + wiki refs in Tasks 2, 3. ✓
- Naming (spec §5) → `kids-app`/`dense-ui`, `designing-for-children`/`designing-dense-data-uis`, used consistently. ✓
- SETUP + mirror consequence → Task 5 (edit + `cp` re-sync + parity run). ✓
- Verification gate: new test → Task 4; stamps → inline on every created file; changelog → Task 6; release (branch/merge/tag/push, repo-identity) → Task 7. ✓
- Honest dense-ui anchoring → Task 3 README status line, Task 6 changelog "HONESTLY anticipatory". ✓
- Out-of-scope: no check gate (stated in profiles/README + changelog), no third profile, no per-tool wiring — none added. ✓

**2. Placeholder scan:** No TBD/TODO. The single measured value `M` (suite count) has an exact command to produce it (Task 6 Step 1) and is not a vague placeholder. The README `## Map` branch (Task 6 Step 2) specifies both outcomes concretely. ✓

**3. Type consistency:** No code symbols cross task boundaries except the test helper `is_stamped` and class `ConstraintProfileShapeTests`, both self-contained in Task 4. Profile directory names and file names used in the test (Task 4) match exactly those created in Tasks 1-3 (`profiles/README.md`, `CLAUDE.constraints-section.md`, `skills/*/SKILL.md`, `wiki/*.md`). ✓
