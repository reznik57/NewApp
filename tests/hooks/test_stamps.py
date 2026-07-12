"""Every template file carries a template-version stamp, and every stamp is real.

The stamp is the seed's whole versioning contract: root CLAUDE.md makes
re-stamping a touched file a hard rule, and ADOPTION's UPDATE MODE
navigates a version merge by diffing stamps ("only changed stamps need
porting"). Nothing enforced it -- a template shipped WITHOUT a stamp, or
carrying a round that never existed, is invisible to that merge, so the
improvement silently never reaches an adopted app.

This test pins the two halves the stamp rule rests on: every template
file HAS a stamp, and every stamp NAMES a real changelog round. It
cannot see the third half (was a touched file re-stamped THIS round) --
that stays a review call, deliberately: mechanizing it would mean
diffing against git history from a unit test.
Run from the seed root: python -m unittest discover -s tests
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHANGELOG = ROOT / "TEMPLATE-CHANGELOG.md"
STAMPED_TREES = ("base", "profiles")

STAMP = re.compile(r"template-version:\s*([0-9][0-9.\-]*)")

# JSON cannot carry a comment stamp -- the changelog's header note is
# their single home (root CLAUDE.md -> Template discipline).
# The vendored frontend-design bundle is upstream's file, not a seed
# template: stamping it would fake authorship of a copy we do not own
# (the exemption is recorded in TEMPLATE-CHANGELOG v2.4.8). It moved out of
# the TS/Next profile into base/ in v2.7.6 -- it is the floor every
# constraint profile layers on, so it cannot ride on a stack choice.
VENDORED = Path("base") / ".claude" / "skills" / "frontend-design"


def is_exempt(rel):
    return rel.suffix == ".json" or VENDORED in rel.parents


def changelog_rounds():
    """The set of round identifiers a stamp is allowed to name."""
    rounds = set()
    for line in CHANGELOG.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            rounds.add(line[3:].split()[0])
    return rounds


def template_files():
    for tree in STAMPED_TREES:
        for f in (ROOT / tree).rglob("*"):
            if f.is_file() and "__pycache__" not in f.parts:
                yield f.relative_to(ROOT)


class StampTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rounds = changelog_rounds()
        cls.files = list(template_files())

    def test_the_fixtures_are_sane(self):
        # Guards against a silently empty run: a typo'd tree name or a
        # changelog whose headers stopped parsing would otherwise make
        # every assertion below pass vacuously.
        self.assertGreater(len(self.files), 20)
        self.assertIn("2026-07", self.rounds)

    def test_every_template_file_carries_a_stamp(self):
        for rel in self.files:
            if is_exempt(rel):
                continue
            text = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
            self.assertRegex(
                text, STAMP,
                "%s has no template-version stamp: UPDATE MODE diffs stamps,"
                " so an unstamped template never reaches an adopted app"
                % rel,
            )

    def test_every_stamp_names_a_real_changelog_round(self):
        for rel in self.files:
            if is_exempt(rel):
                continue
            text = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
            match = STAMP.search(text)
            if match is None:
                continue  # reported by the test above
            self.assertIn(
                match.group(1), self.rounds,
                "%s is stamped %r, which is no round in TEMPLATE-CHANGELOG.md"
                % (rel, match.group(1)),
            )

    def test_the_vendored_exemption_still_points_at_something(self):
        # An exemption that no longer matches a real path is an exemption
        # that silently widens on the next rename.
        self.assertTrue((ROOT / VENDORED).is_dir())


if __name__ == "__main__":
    unittest.main()
