"""Tests for base/.claude/hooks/verify_on_stop.py — run from the seed root:
python -m unittest discover -s tests -v
"""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[2] / "base" / ".claude" / "hooks" / "verify_on_stop.py"

PASS_CMD = '%s -c "raise SystemExit(0)"' % sys.executable
FAIL_CMD = '%s -c "print(\'boom\'); raise SystemExit(1)"' % sys.executable


def run_hook(stdin_obj, check_cmd, extra_args=None):
    env = dict(os.environ, HARNESS_CHECK_CMD=check_cmd)
    return subprocess.run(
        [sys.executable, str(HOOK)] + (extra_args or []),
        input=json.dumps(stdin_obj), capture_output=True, text=True,
        timeout=60, env=env,
    )


class VerifyOnStopTests(unittest.TestCase):
    def test_allows_stop_when_check_passes(self):
        result = run_hook({"stop_hook_active": False}, PASS_CMD)
        self.assertEqual(result.returncode, 0)

    def test_blocks_stop_when_check_fails(self):
        result = run_hook({"stop_hook_active": False}, FAIL_CMD)
        self.assertEqual(result.returncode, 2)
        self.assertIn("failed", result.stderr)
        self.assertIn("boom", result.stderr)

    def test_skips_check_when_already_looping(self):
        # stop_hook_active=True must exit 0 WITHOUT running the (failing) command
        result = run_hook({"stop_hook_active": True}, FAIL_CMD)
        self.assertEqual(result.returncode, 0)

    def test_tolerates_malformed_stdin(self):
        env = dict(os.environ, HARNESS_CHECK_CMD=PASS_CMD)
        result = subprocess.run(
            [sys.executable, str(HOOK)], input="not json",
            capture_output=True, text=True, timeout=60, env=env,
        )
        self.assertEqual(result.returncode, 0)

    def test_skips_check_when_already_looping_with_utf8_bom(self):
        # Windows PowerShell's `|` pipe to a native process prepends a UTF-8
        # BOM. json.load() on a text stream does not strip it, which used to
        # make this hook mistake stop_hook_active=True for malformed input
        # (payload => {}) and re-run the (failing) check instead of exiting
        # 0. Regression guard.
        env = dict(os.environ, HARNESS_CHECK_CMD=FAIL_CMD)
        payload = json.dumps({"stop_hook_active": True})
        result = subprocess.run(
            [sys.executable, str(HOOK)],
            input=b"\xef\xbb\xbf" + payload.encode("utf-8"),
            capture_output=True, timeout=60, env=env,
        )
        self.assertEqual(result.returncode, 0)

    def test_self_test_passes_for_non_npm_command(self):
        result = run_hook({}, PASS_CMD, extra_args=["--self-test"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("self-test OK", result.stdout)

    def test_self_test_fails_when_npm_script_missing(self):
        # Runs in the seed root, which has no package.json — npm-run commands must fail self-test
        result = run_hook({}, "npm run check", extra_args=["--self-test"])
        self.assertEqual(result.returncode, 1)
        self.assertIn("self-test FAIL", result.stdout)

    def test_self_test_fails_for_missing_tool(self):
        # A typo'd non-npm binary must fail at setup, not block every stop.
        result = run_hook({}, "definitely-missing-tool-xyz --check", extra_args=["--self-test"])
        self.assertEqual(result.returncode, 1)
        self.assertIn("not found", result.stdout)

    def test_self_test_checks_every_compound_segment(self):
        cmd = PASS_CMD + " && definitely-missing-tool-xyz"
        result = run_hook({}, cmd, extra_args=["--self-test"])
        self.assertEqual(result.returncode, 1)
        self.assertIn("not found", result.stdout)


if __name__ == "__main__":
    unittest.main()
