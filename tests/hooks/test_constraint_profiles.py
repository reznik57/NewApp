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
CONSTRAINT_PROFILES = ("kids-app", "dense-ui", "facilitated-session")
STAMP = re.compile(r"template-version:\s*\d{4}-\d{2}\.\d+")


def is_stamped(path):
    return bool(STAMP.search(path.read_text(encoding="utf-8")))


class LayeringFoundationTests(unittest.TestCase):
    """The floor every constraint profile stands on must not move again.

    Each constraint skill says "invoke frontend-design FIRST, this layers on
    top". Until v2.7.6 that floor was vendored by the typescript-next STACK
    profile, so a stack-less app (static HTML, no npm) with a constraint
    profile pointed at a skill its repo did not contain. The floor now ships
    with base/ -> the kit -> every app. These two assertions pin both halves:
    the floor is in base, and every profile that claims to layer on it says so.
    """

    def test_frontend_design_ships_with_the_harness_not_with_a_profile(self):
        self.assertTrue(
            (ROOT / "base" / ".claude" / "skills" / "frontend-design"
             / "SKILL.md").is_file(),
            "frontend-design must live in base/.claude/skills/ — a constraint"
            " profile cannot depend on a STACK profile having vendored it",
        )
        strays = list(PROFILES.rglob("frontend-design"))
        self.assertEqual(
            [], strays,
            "frontend-design is back inside a profile (%s): a stack-less app"
            " taking a constraint profile would lose its aesthetic floor"
            % strays,
        )

    def test_each_constraint_skill_names_the_skill_it_layers_on(self):
        for name in CONSTRAINT_PROFILES:
            for skill in (PROFILES / name / "skills").glob("*/SKILL.md"):
                self.assertIn(
                    "frontend-design",
                    skill.read_text(encoding="utf-8"),
                    "%s does not name frontend-design: a constraint profile"
                    " ADDS to the aesthetic direction, it never replaces it"
                    % skill.relative_to(ROOT),
                )


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
