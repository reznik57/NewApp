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
