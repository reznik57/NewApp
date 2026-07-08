"""The ultrathink trigger list must stay identical in its two homes.

CLAUDE.md -> Deep-Analysis Protocol is the SOLE home of the trigger list;
the ultrathink skill's `description:` restates it because a skill
description must be self-contained for auto-invocation (v2.2 changelog:
"the one allowed restatement"). Two hand-synced copies with no guard is
exactly the drift class the seed mechanizes elsewhere (kit parity, root
docs). This test derives the clause from the sole home and asserts the
mirror contains it verbatim (whitespace-normalized) -- it keeps NO third
copy of the list itself. base/ is enough: test_kit_parity pins base <->
harness-kit byte equality, so the kit skill cannot diverge from base's.
Run from the seed root: python -m unittest discover -s tests
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLAUDE = ROOT / "base" / "CLAUDE.template.md"
SKILL = ROOT / "base" / ".claude" / "skills" / "ultrathink" / "SKILL.md"


def normalize(text):
    """Collapse all whitespace runs so line-wrapping never affects match."""
    return " ".join(text.split())


def sole_home_triggers():
    """The trigger clause as written in CLAUDE.md -> Deep-Analysis Protocol.

    Anchored on the parenthetical that names this the sole home, up to the
    first sentence-ending period. If the paragraph is restructured the
    match fails loudly -- that is the guard, not a bug.
    """
    text = CLAUDE.read_text(encoding="utf-8")
    m = re.search(r"auto-invocation description\):\s*(.+?)\.\s", text, re.DOTALL)
    return normalize(m.group(1)) if m else None


def skill_description():
    """The `description:` value from the skill's YAML frontmatter."""
    for line in SKILL.read_text(encoding="utf-8").splitlines():
        if line.startswith("description:"):
            return normalize(line[len("description:"):])
    return None


class UltrathinkTriggerParityTests(unittest.TestCase):
    def test_sole_home_clause_is_extractable(self):
        clause = sole_home_triggers()
        self.assertIsNotNone(
            clause, "trigger clause anchor moved in CLAUDE.template.md"
        )
        # Guard against a vacuous pass if the anchor ever matches empty.
        self.assertIn("architecture decisions", clause)
        self.assertGreater(len(clause), 40, "extracted clause implausibly short")

    def test_skill_description_exists(self):
        self.assertIsNotNone(
            skill_description(), "no description: line in ultrathink SKILL.md"
        )

    def test_description_mirrors_the_sole_home_verbatim(self):
        clause = sole_home_triggers()
        desc = skill_description()
        self.assertIn(
            clause, desc,
            "ultrathink description drifted from CLAUDE.md Deep-Analysis "
            "triggers (the sole home). Re-sync the description.",
        )


if __name__ == "__main__":
    unittest.main()
