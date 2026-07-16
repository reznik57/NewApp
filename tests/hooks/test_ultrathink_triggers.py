"""The ultrathink trigger list must stay identical in all of its homes.

AGENTS.md -> Deep-Analysis Protocol is the SOLE home of the trigger list;
the ultrathink skill's `description:` restates it because a skill
description must be self-contained for auto-invocation (v2.2 changelog:
"the one allowed restatement"). Two hand-synced copies with no guard is
exactly the drift class the seed mechanizes elsewhere (kit parity, root
docs). This test derives the clause from the sole home and asserts every
mirror contains it verbatim (whitespace-normalized) -- it keeps NO third
copy of the list itself.

Since v2.8.0 there are TWO mirrors, not one: the canonical skill under
.agents/skills/ and the Claude bridge under .claude/skills/, which keeps
its own frontmatter because that is what Claude Code reads to decide
whether to auto-invoke. A bridge is thin, not description-less -- so it
drifts exactly like the canonical one can, and both are pinned here.
base/ is enough: test_kit_parity pins base <-> harness-kit byte equality,
so the kit skills cannot diverge from base's.
Run from the seed root: python -m unittest discover -s tests
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AGENTS = ROOT / "base" / "AGENTS.template.md"
CANONICAL_SKILL = ROOT / "base" / ".agents" / "skills" / "ultrathink" / "SKILL.md"
BRIDGE_SKILL = ROOT / "base" / ".claude" / "skills" / "ultrathink" / "SKILL.md"
MIRRORS = (CANONICAL_SKILL, BRIDGE_SKILL)


def normalize(text):
    """Collapse all whitespace runs so line-wrapping never affects match."""
    return " ".join(text.split())


def sole_home_triggers():
    """The trigger clause as written in AGENTS.md -> Deep-Analysis Protocol.

    Anchored on the parenthetical that names this the sole home, up to the
    first sentence-ending period. If the paragraph is restructured the
    match fails loudly -- that is the guard, not a bug.
    """
    text = AGENTS.read_text(encoding="utf-8")
    m = re.search(r"auto-invocation description\):\s*(.+?)\.\s", text, re.DOTALL)
    return normalize(m.group(1)) if m else None


def skill_description(path):
    """The `description:` value from a skill's YAML frontmatter."""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("description:"):
            return normalize(line[len("description:"):])
    return None


class UltrathinkTriggerParityTests(unittest.TestCase):
    def test_sole_home_clause_is_extractable(self):
        clause = sole_home_triggers()
        self.assertIsNotNone(
            clause, "trigger clause anchor moved in AGENTS.template.md"
        )
        # Guard against a vacuous pass if the anchor ever matches empty.
        self.assertIn("architecture decisions", clause)
        self.assertGreater(len(clause), 40, "extracted clause implausibly short")

    def test_every_mirror_has_a_description(self):
        for path in MIRRORS:
            self.assertIsNotNone(
                skill_description(path),
                "no description: line in %s" % path.relative_to(ROOT),
            )

    def test_every_mirror_restates_the_sole_home_verbatim(self):
        clause = sole_home_triggers()
        for path in MIRRORS:
            self.assertIn(
                clause, skill_description(path),
                "%s drifted from AGENTS.md Deep-Analysis triggers (the sole"
                " home). Re-sync the description."
                % path.relative_to(ROOT),
            )

    def test_the_two_mirrors_agree_with_each_other(self):
        # The bridge is generated from the canonical skill's frontmatter.
        # Both matching the sole-home CLAUSE still allows their surrounding
        # prose (the skip list) to diverge -- and Claude Code auto-invokes
        # off the BRIDGE, so a stale skip list there changes real behavior.
        self.assertEqual(
            skill_description(CANONICAL_SKILL),
            skill_description(BRIDGE_SKILL),
            "the Claude bridge's description drifted from the canonical"
            " skill's: they are one description with two homes",
        )


if __name__ == "__main__":
    unittest.main()
