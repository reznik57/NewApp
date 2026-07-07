"""harness-kit/ must stay a byte-identical mirror of its sources.

harness-kit/ is the self-contained kit and the SINGLE user-facing
entry point: copied as a FOLDER into any app — new or existing —
where START-HERE.md routes to SETUP or ADOPTION; no further seed
access needed (except optional profiles). Its files are COPIES
(base/ for the harness set, the seed root for SETUP.md); this test
pins the manifest and byte equality, so a source edit fails here
until mirrored. Re-sync with:
  robocopy base harness-kit /E /XD __pycache__ .github /XF .gitignore .gitattributes
  copy /Y SETUP.md harness-kit
Run from the seed root: python -m unittest discover -s tests
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "base"
COPY = ROOT / "harness-kit"

# harness-kit top-level entry -> the source root it mirrors.
# Deliberately absent: .gitignore (merge-only, ADOPTION step 3) and
# .github/ (CI is a merge step, ADOPTION step 8).
MANIFEST = {
    "CLAUDE.template.md": BASE,
    ".env.example": BASE,
    ".editorconfig": BASE,
    ".claude": BASE,
    "docs": BASE,
    "SETUP.md": ROOT,  # root-homed; travels as the kit's fresh-repo
                       # checklist (START-HERE routes to it)
}
# Authored directly in the kit, no source twin: the kickoff prompt's
# single home (START-HERE) and the adoption checklist itself — its
# home IS the kit; the seed root carries no second copy.
KIT_ONLY = {"START-HERE.md", "ADOPTION.md"}

# Merge sources shipped under an INERT name: the original name would
# either overwrite an app file on copy (.gitignore) or be parsed by
# GitHub as a broken workflow (ci.template.yml under .github/).
# Re-sync: copy the source over the kit file listed here.
RENAMED = {
    "gitignore.template": BASE / ".gitignore",
    "gitattributes.template": BASE / ".gitattributes",
    "ci.template.yml": BASE / ".github" / "workflows" / "ci.template.yml",
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


class KitParityTests(unittest.TestCase):
    def test_no_files_outside_the_manifest(self):
        for f in COPY.rglob("*"):
            if f.is_file() and "__pycache__" not in f.parts:
                rel = f.relative_to(COPY)
                self.assertTrue(
                    rel.parts[0] in MANIFEST
                    or rel.parts[0] in KIT_ONLY
                    or rel.parts[0] in RENAMED,
                    "unexpected file in harness-kit: %s" % rel,
                )

    def test_every_copy_file_matches_its_source_byte_for_byte(self):
        count = 0
        for f in files_under(COPY, MANIFEST):
            rel = f.relative_to(COPY)
            twin = MANIFEST[rel.parts[0]] / rel
            self.assertTrue(twin.is_file(), "no source twin for %s" % rel)
            self.assertEqual(
                f.read_bytes(), twin.read_bytes(), "drift: %s" % rel
            )
            count += 1
        self.assertGreater(count, 12, "copy set implausibly small")

    def test_every_source_file_in_the_manifest_is_mirrored(self):
        for top, source_root in MANIFEST.items():
            for f in files_under(source_root, [top]):
                rel = f.relative_to(source_root)
                self.assertTrue(
                    (COPY / rel).is_file(),
                    "missing in harness-kit (re-sync): %s" % rel,
                )

    def test_renamed_merge_sources_match_byte_for_byte(self):
        for kit_name, source in RENAMED.items():
            kit_file = COPY / kit_name
            self.assertTrue(kit_file.is_file(), "missing: %s" % kit_name)
            self.assertTrue(source.is_file(), "source gone: %s" % source)
            self.assertEqual(
                kit_file.read_bytes(), source.read_bytes(),
                "drift: %s" % kit_name,
            )


if __name__ == "__main__":
    unittest.main()
