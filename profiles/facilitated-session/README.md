<!-- template-version: 2026-07.33 -->

# Constraint profile: facilitated-session

Domain overlay for a surface that runs in a ROOM, in front of people, while
someone facilitates: an interactive presentation, an exercise playbook, a
tabletop drill, a training deck. Apply AFTER the stack profile, once
`harness-kit/` is distributed. Orthogonal to the stack — most such apps are
static HTML with no build at all, which is exactly why the aesthetic floor
(`frontend-design`) ships with the harness rather than with a stack profile.

The two things that separate this domain from a normal web app: the surface
is read at a DISTANCE it cannot renegotiate (a projector never scrolls), and
what one participant may see, another may not (roles, confidentiality) — so
visibility is a layout constraint, not a filter bolted on afterwards.

1. Insert `AGENTS.constraints-section.md` as a new section in the app's
   AGENTS.md, after the stack profile's Stack Rules (still named
   `AGENTS.template.md` at overlay time). Keep it lean — it counts against
   the AGENTS.md line budget (SETUP step 7). Its last bullet points at the
   `designing-facilitated-sessions` skill, so step 2 is REQUIRED alongside it.
2. Copy `skills/designing-facilitated-sessions/` -> `.agents/skills/` (the canonical
   home), then add its Claude discovery bridge at
   `.claude/skills/designing-facilitated-sessions/SKILL.md` — same shape as the harness's
   own bridges: the skill's frontmatter plus a `Canonical skill:` pointer,
   no substance. Claude Code reads only `.claude/skills/`; every other agent
   tool reads only `.agents/skills/`. Ship one and the skill is invisible to
   half the toolchain.
3. Copy `wiki/facilitated-session-ux.md` -> the app's `docs/wiki/`, and add
   its line to the wiki index (per the wiki-lint skill).
4. Fill the two blanks the section leaves open — the app's real target
   resolutions and its real role/visibility matrix. A view whose "must NOT
   show" list is empty is a claim, not a default: write it down or delete
   the row.
