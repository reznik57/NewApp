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
