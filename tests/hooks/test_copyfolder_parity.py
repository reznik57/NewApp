"""copyfolder/ must stay a byte-identical subset of base/.

copyfolder/ is the one-command copy set for existing apps (ADOPTION.md
step 2): everything an adoption needs, nothing that can collide. Its
files are COPIES of their base/ twins; this test pins the manifest and
byte equality, so a base/ edit fails here until mirrored. Re-sync with:
robocopy base copyfolder /E /XD __pycache__ .github /XF .gitignore
Run from the seed root: python -m unittest discover -s tests
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "base"
COPY = ROOT / "copyfolder"

# Top-level entries copyfolder may contain (same relative layout as
# base/). Deliberately absent: .gitignore (merge-only, ADOPTION step 3)
# and .github/ (CI is a merge step, ADOPTION step 8).
INCLUDED_TOPS = {
    "CLAUDE.template.md",
    ".env.example",
    ".editorconfig",
    ".claude",
    "docs",
}


def files_under(root, tops):
    for top in tops:
        p = root / top
        candidates = [p] if p.is_file() else (
            [f for f in p.rglob("*") if f.is_file()] if p.is_dir() else []
        )
        for f in candidates:
            if "__pycache__" not in f.parts:
                yield f


class CopyfolderParityTests(unittest.TestCase):
    def test_no_files_outside_the_manifest(self):
        for f in COPY.rglob("*"):
            if f.is_file() and "__pycache__" not in f.parts:
                rel = f.relative_to(COPY)
                self.assertIn(
                    rel.parts[0], INCLUDED_TOPS,
                    "unexpected file in copyfolder: %s" % rel,
                )

    def test_every_copy_file_matches_base_byte_for_byte(self):
        count = 0
        for f in files_under(COPY, INCLUDED_TOPS):
            rel = f.relative_to(COPY)
            twin = BASE / rel
            self.assertTrue(twin.is_file(), "no base twin for %s" % rel)
            self.assertEqual(
                f.read_bytes(), twin.read_bytes(), "drift: %s" % rel
            )
            count += 1
        self.assertGreater(count, 10, "copy set implausibly small")

    def test_every_base_file_under_the_manifest_is_mirrored(self):
        for f in files_under(BASE, INCLUDED_TOPS):
            rel = f.relative_to(BASE)
            self.assertTrue(
                (COPY / rel).is_file(),
                "missing in copyfolder (re-sync): %s" % rel,
            )


if __name__ == "__main__":
    unittest.main()
