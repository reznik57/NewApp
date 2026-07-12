"""The app's server port is rolled once from 9000-9999 -- and the seed says so
in the places that can enforce it.

Framework defaults (Next 3000, Vite 5173, http.server 8000) collide as soon as
two apps run in parallel; the expensive failure is the silent one -- talking to
yesterday's server. v2.7.7 gives every seeded server a port rolled once from
9000-9999 and wires the rule to the exit gate via a {{DEV_PORT}} slot.

One fact, several homes that must agree: the profile SHIPS the slot, the profile
README and SETUP NAME the range, and check_markers.py SCANS package.json so an
unfilled slot cannot reach a green gate. Drop any one of them and the rule
degrades to prose without anyone noticing -- this test is what notices.
Run from the seed root: python -m unittest discover -s tests
"""
# template-version: 2026-07.32
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROFILE = ROOT / "profiles" / "typescript-next"
SCRIPTS = PROFILE / "package-scripts.json"
PROFILE_README = PROFILE / "README.md"
GATE = ROOT / "base" / ".claude" / "scripts" / "check_markers.py"
SLOT = "{{DEV_PORT}}"
BOUNDS = ("9000", "9999")


class DevPortSlotTests(unittest.TestCase):
    def test_dev_and_start_bind_the_rolled_port(self):
        scripts = json.loads(SCRIPTS.read_text(encoding="utf-8"))["scripts"]
        for name in ("dev", "start"):
            self.assertIn(
                "-p %s" % SLOT, scripts.get(name, ""),
                "profile script %r must bind the rolled port, not the"
                " framework default" % name,
            )

    def test_the_gate_scans_package_json(self):
        # Without this line the slot is decoration: an unfilled {{DEV_PORT}}
        # would survive the exit gate and the app would serve on 3000.
        self.assertIn('"package.json"', GATE.read_text(encoding="utf-8"))


class PortRangeTests(unittest.TestCase):
    def assert_names_the_range(self, path):
        text = path.read_text(encoding="utf-8")
        for bound in BOUNDS:
            self.assertIn(
                bound, text,
                "%s no longer names the port range -- the roll instruction and"
                " the slot must not drift apart" % path.name,
            )

    def test_profile_readme_names_the_range(self):
        self.assert_names_the_range(PROFILE_README)


if __name__ == "__main__":
    unittest.main()
