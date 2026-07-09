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
