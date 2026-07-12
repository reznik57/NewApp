"""Parity guard: base settings.template.json vs the profile's settings.json.

The profile file is a COPY of the base template plus one documented
delta. That relationship drifted once for real (v2.2.1:
Read(.env.staging.local) missing on one side), so this test pins it:
editing one file now fails loudly until mirrored in the other — or
until the intended delta below is updated deliberately.
Run from the seed root: python -m unittest discover -s tests
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "base" / ".claude" / "settings.template.json"
PROFILE = ROOT / "profiles" / "typescript-next" / "settings.json"

# The one intended delta: the profile pre-approves the npx forms of its
# four toolchain commands and drops the generic npx ask entry (unlisted
# commands fall back to asking anyway).
PROFILE_EXTRA_ALLOW = {
    "Bash(npx tsc:*)",
    "Bash(npx vitest run:*)",
    "Bash(npx eslint:*)",
    "Bash(npx prettier:*)",
}
BASE_ONLY_ASK = {"Bash(npx:*)"}


class SettingsParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = json.loads(BASE.read_text(encoding="utf-8"))
        cls.profile = json.loads(PROFILE.read_text(encoding="utf-8"))

    def test_top_level_and_permission_key_sets_identical(self):
        # The list-shaped tests below only compare keys that BOTH files
        # already have. A block added to one side only (an "env" key, a
        # "statusLine", a permissions "defaultMode") drifts past them --
        # and since a TS/Next app copies the PROFILE file and deletes the
        # base template, the drift would land on the path most apps take.
        self.assertEqual(set(self.base), set(self.profile))
        self.assertEqual(
            set(self.base["permissions"]), set(self.profile["permissions"])
        )

    def test_deny_lists_identical(self):
        # Order-sensitive on purpose: a same-set reorder is still a diff
        # a human has to reconcile when porting future entries.
        self.assertEqual(
            self.base["permissions"]["deny"],
            self.profile["permissions"]["deny"],
        )

    def test_hook_registrations_identical(self):
        self.assertEqual(self.base["hooks"], self.profile["hooks"])

    def test_allow_delta_is_exactly_the_npx_quartet(self):
        base_allow = set(self.base["permissions"]["allow"])
        profile_allow = set(self.profile["permissions"]["allow"])
        self.assertEqual(profile_allow - base_allow, PROFILE_EXTRA_ALLOW)
        self.assertEqual(base_allow - profile_allow, set())

    def test_ask_delta_is_exactly_the_generic_npx_entry(self):
        base_ask = set(self.base["permissions"]["ask"])
        profile_ask = set(self.profile["permissions"]["ask"])
        self.assertEqual(base_ask - profile_ask, BASE_ONLY_ASK)
        self.assertEqual(profile_ask - base_ask, set())


if __name__ == "__main__":
    unittest.main()
