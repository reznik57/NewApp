"""Guard docs whose content no other test reads, against silent gutting.

test_kit_parity.py pins base/ <-> harness-kit/ byte equality, but that
catches nothing on its own for two classes of doc: those with no twin at
all (the root-level singletons, the KIT_ONLY checklists), and those whose
twin is a COPY of them -- SETUP.md and the base/ instruction pair, where
the sanctioned re-sync writes source->mirror, so a gutted source is
mirrored faithfully and the suite stays green.

It bit twice. v2.5.0 arrived with README.md truncated (the whole
"Upgrading seeded apps" section gone, trailing newline lost) and the suite
stayed green. v2.8.0 moved the canon to AGENTS.md, and the two tests that
had read base/CLAUDE.template.md's content followed it there -- correctly,
leaving the bridge with no reader; deleting its @AGENTS.md import left
every test green.

This test pins load-bearing anchors, a trailing newline, a size floor, and
a changelog entry floor. A red run after a deliberate doc restructure
means: update REQUIRED here, consciously, in the same commit.
Run from the seed root: python -m unittest discover -s tests
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# doc (relative to the seed root) -> load-bearing anchor strings.
# ASCII-only on purpose: encoding must never affect matching, so
# anchors stop BEFORE any em-dash in the real heading. Anchors match as
# SUBSTRINGS anywhere in the doc: when restructuring, make sure a
# removed section's anchor does not accidentally survive in prose (a
# mention like "the ## Map section" would false-pass the check).
REQUIRED = {
    "CLAUDE.md": [
        "# CLAUDE.md",
        "## Source-of-truth map",
        "## Verification gate",
        "## Release discipline",
    ],
    "README.md": [
        "## Philosophy",
        "## Map",
        "## Instantiation",
        "## When not to use this seed",
        "## Portability",
        "## Relationship to installed plugins",
        "## Upgrading seeded apps",
    ],
    "TEMPLATE-CHANGELOG.md": [
        "# Template Changelog",
        "Seed version history",
    ],
    # The fresh-app spine. Its only other protection is byte-equality with
    # its own kit mirror -- and the sanctioned re-sync copies root->kit, so
    # a truncated source would be faithfully mirrored and the suite would
    # stay green. Anchor the load-bearing steps, not every one.
    "SETUP.md": [
        "# New App Setup",
        "**STOP GUARD**",
        "0. **Discovery",
        "4. **Fill the six-script contract**",
        "5. **Activate settings**",
        "11. **First commit at green**",
        "12. **EXIT GATE**",
    ],
    # The instruction pair, here for SETUP.md's exact reason: base->kit is a
    # copy, so byte-equality mirrors a gutted source faithfully and stays
    # green. v2.8.0 made that bite. The canon's content was pinned by two
    # tests through base/CLAUDE.template.md (test_dev_port's port range,
    # test_ultrathink_triggers' sole home); both correctly followed the
    # content to AGENTS.template.md, and the bridge was left with NO test
    # reading it at all. Measured: deleting its @AGENTS.md line left all
    # tests green -- a seeded app that loads zero instructions under Claude
    # Code, silently. Anchor the canon's load-bearing frame and the bridge's
    # one load-bearing line.
    "base/AGENTS.template.md": [
        "# AGENTS.md",
        "### 3. Source of Truth (anti-rot)",
        "### 4. Cite Symbols, Not Counts or Line Numbers",
        "## Everyday Task Discipline",
        "## Standing Rules",
        "## Docs & Knowledge Schema",
        "## Deep-Analysis Protocol",
    ],
    # Newlines on purpose: the import must survive as its own LINE. A bare
    # "@AGENTS.md" anchor would also match the file's own prose about the
    # import (backticked), false-passing the exact gutting this catches.
    "base/CLAUDE.template.md": [
        "# CLAUDE.md",
        "\n@AGENTS.md\n",
    ],
    "harness-kit/ADOPTION.md": [
        "# Existing App Adoption",
        "**STOP GUARD**",
        "**UPDATE MODE**",
    ],
    "harness-kit/START-HERE.md": [
        "# Harness Kit",
        "Pick the checklist",
        "SINGLE-USE",
    ],
}

MIN_BYTES = 500          # below this a doc is a wipe, not an edit
CHANGELOG_ENTRY_FLOOR = 15  # "## " entries; fires on loss, not growth


def check_doc(text, anchors, min_bytes=MIN_BYTES):
    """Return a list of problems with a doc's text (empty = healthy)."""
    problems = []
    if len(text.encode("utf-8")) < min_bytes:
        problems.append("suspiciously small (< %d bytes)" % min_bytes)
    if not text.endswith("\n"):
        problems.append("missing trailing newline (truncation signature)")
    for anchor in anchors:
        if anchor not in text:
            problems.append("missing anchor: %r" % anchor)
    return problems


class CheckDocDiscriminationTests(unittest.TestCase):
    """check_doc must flag exactly the v2.5.0 truncation signatures."""

    ANCHORS = ["## Alpha", "## Omega"]
    # 60 body lines keep the healthy fixture safely above MIN_BYTES.
    HEALTHY = (
        "# Doc\n\n## Alpha\n" + ("body line\n" * 60) + "## Omega\ntail\n"
    )

    def test_healthy_text_has_no_problems(self):
        self.assertEqual(check_doc(self.HEALTHY, self.ANCHORS), [])

    def test_dropped_section_is_flagged(self):
        # v2.5.0 signature 1: a whole anchored section vanished.
        truncated = self.HEALTHY.split("## Omega")[0]
        problems = check_doc(truncated, self.ANCHORS)
        self.assertTrue(
            any("## Omega" in p for p in problems),
            "dropped section not flagged: %s" % problems,
        )

    def test_missing_trailing_newline_is_flagged(self):
        # v2.5.0 signature 2: the file ended without a newline.
        problems = check_doc(self.HEALTHY.rstrip("\n"), self.ANCHORS)
        self.assertTrue(
            any("newline" in p for p in problems),
            "lost trailing newline not flagged: %s" % problems,
        )

    def test_wholesale_wipe_is_flagged(self):
        problems = check_doc("# Doc\n## Alpha\n## Omega\n", self.ANCHORS)
        self.assertTrue(
            any("small" in p for p in problems),
            "near-empty doc not flagged: %s" % problems,
        )


class RootDocsGuardTests(unittest.TestCase):
    """The live singleton docs pinned in REQUIRED must stay healthy."""

    def test_every_singleton_doc_is_healthy(self):
        for rel, anchors in REQUIRED.items():
            path = ROOT / rel
            self.assertTrue(path.is_file(), "missing doc: %s" % rel)
            problems = check_doc(path.read_text(encoding="utf-8"), anchors)
            self.assertEqual(problems, [], "%s: %s" % (rel, problems))

    def test_changelog_keeps_its_version_history(self):
        text = (ROOT / "TEMPLATE-CHANGELOG.md").read_text(encoding="utf-8")
        entries = [l for l in text.splitlines() if l.startswith("## ")]
        self.assertGreaterEqual(
            len(entries), CHANGELOG_ENTRY_FLOOR,
            "version history implausibly short: %d entries" % len(entries),
        )


if __name__ == "__main__":
    unittest.main()
