<!-- template-version: 2026-07.33 -->

# Constraint profile: kids-app

Audience overlay for apps whose users are children (roughly 7-10). Apply
AFTER the stack profile, once `harness-kit/` is distributed. Orthogonal to
the stack — compose it with `typescript-next` or any other.

1. Insert `AGENTS.constraints-section.md` as a new section in the app's
   AGENTS.md, after the stack profile's Stack Rules (still named
   `AGENTS.template.md` at overlay time). Keep it lean — it counts against
   the AGENTS.md line budget (SETUP step 7). Its last bullet points at the
   `designing-for-children` skill, so step 2 is REQUIRED alongside it.
2. Copy `skills/designing-for-children/` -> `.agents/skills/` (the canonical
   home), then add its Claude discovery bridge at
   `.claude/skills/designing-for-children/SKILL.md` — same shape as the harness's
   own bridges: the skill's frontmatter plus a `Canonical skill:` pointer,
   no substance. Claude Code reads only `.claude/skills/`; every other agent
   tool reads only `.agents/skills/`. Ship one and the skill is invisible to
   half the toolchain.
3. Copy `wiki/kids-app-ux.md` -> the app's `docs/wiki/`, and add its line to
   the wiki index (per the wiki-lint skill).

Non-negotiable regardless of stack: the legal pointers (DSGVO Art. 8,
JMStV) are jurisdiction facts, not style — keep them even if you trim.
