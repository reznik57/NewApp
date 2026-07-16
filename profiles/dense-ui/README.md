<!-- template-version: 2026-07.33 -->

# Constraint profile: dense-ui

Domain overlay for data-dense operational UIs — dashboards, monitoring,
network/security consoles, admin tables. Apply AFTER the stack profile.
Orthogonal to the stack; compose it freely.

1. Insert `AGENTS.constraints-section.md` as a new section in the app's
   AGENTS.md, after the stack profile's Stack Rules. Keep it lean — it
   counts against the AGENTS.md line budget (SETUP step 7). Its last bullet
   points at the `designing-dense-data-uis` skill, so step 2 is REQUIRED
   alongside it.
2. Copy `skills/designing-dense-data-uis/` -> `.agents/skills/` (the canonical
   home), then add its Claude discovery bridge at
   `.claude/skills/designing-dense-data-uis/SKILL.md` — same shape as the harness's
   own bridges: the skill's frontmatter plus a `Canonical skill:` pointer,
   no substance. Claude Code reads only `.claude/skills/`; every other agent
   tool reads only `.agents/skills/`. Ship one and the skill is invisible to
   half the toolchain.
3. Copy `wiki/dense-ui-ux.md` -> the app's `docs/wiki/`, and add its line to
   the wiki index (per the wiki-lint skill).

Status: anticipatory. No real app has driven this profile yet (v2.7.0
changelog) — validate and correct it against the first real data-dense app.
