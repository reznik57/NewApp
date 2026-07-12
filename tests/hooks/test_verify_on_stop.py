"""Tests for base/.claude/hooks/verify_on_stop.py — run from the seed root:
python -m unittest discover -s tests -v
"""
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[2] / "base" / ".claude" / "hooks" / "verify_on_stop.py"

# Executable path quoted: a Python under "C:\Program Files\..." must not
# make the suite (or the self-test) environment-dependent.
PASS_CMD = '"%s" -c "raise SystemExit(0)"' % sys.executable
FAIL_CMD = '"%s" -c "print(\'boom\'); raise SystemExit(1)"' % sys.executable


def run_hook(stdin_obj, check_cmd, extra_args=None, cwd=None, env_overrides=None):
    env = dict(os.environ, HARNESS_CHECK_CMD=check_cmd, **(env_overrides or {}))
    return subprocess.run(
        [sys.executable, str(HOOK)] + (extra_args or []),
        input=json.dumps(stdin_obj), capture_output=True, text=True,
        timeout=60, env=env, cwd=cwd,
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

    def test_diagnostic_tail_survives_utf8_output(self):
        # vitest prints UTF-8 marks; with text=True and no encoding the
        # hook decoded the pipe with the Windows locale (cp1252), the
        # reader thread died on bytes like 0x9d (e.g. ”) and the
        # diagnostic tail was lost — a blocked pipe could even flip the
        # exit code. The marker after the non-cp1252 char must reach
        # stderr.
        # The child writes RAW UTF-8 bytes via stdout.buffer — like node/
        # vitest, it must stay immune to the Python stdio env below. The
        # marker is concatenated so it exists contiguously ONLY in the
        # child's output — the hook echoes the command text in its
        # failure message, which must not satisfy the assertion.
        cmd = (
            '"%s" -c "import sys;'
            " sys.stdout.buffer.write(b'\\xe2\\x80\\x9d tail-' + b'proof');"
            ' sys.stdout.buffer.flush(); raise SystemExit(1)"'
            % sys.executable
        )
        # PYTHONUTF8=0 pins the hook to the legacy locale codec (the
        # real-world condition; bites only where that isn't UTF-8, e.g.
        # cp1252 Windows). ascii:replace keeps the hook's own stderr
        # safely decodable for THIS suite under any test-runner locale.
        result = run_hook(
            {"stop_hook_active": False}, cmd,
            env_overrides={"PYTHONUTF8": "0", "PYTHONIOENCODING": "ascii:replace"},
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("tail-proof", result.stderr)

    @unittest.skipUnless(sys.platform == "win32",
                         "drive-letter casing exists only on Windows")
    def test_check_runs_from_canonical_cwd(self):
        # The hook inherits the session cwd; opened as d:\... (lowercase)
        # Vitest keys module identities case-sensitively and every suite
        # dies at describe() before collecting a test. run_check chdirs
        # to the realpath first — the check command must observe the
        # canonical-case cwd.
        cwd = os.getcwd()
        lower = cwd[0].lower() + cwd[1:]
        cmd = (
            '"%s" -c "import os, sys;'
            ' sys.exit(0 if os.getcwd() == os.path.realpath(os.getcwd()) else 1)"'
            % sys.executable
        )
        result = run_hook({"stop_hook_active": False}, cmd, cwd=lower)
        self.assertEqual(result.returncode, 0)

    # `check` is a process TREE (cmd.exe -> npm -> node), and killing the
    # shell does not kill the tree. With CAPTURED PIPES, subprocess then
    # waited for the pipes to close -- which a surviving grandchild holds
    # open -- so the hook's own cap bounded nothing (measured: a 3s cap took
    # 20.2s). Past the hook runner's timeout (Claude Code cancels a command
    # hook at 600s) the hook is cancelled, and a cancelled hook does not
    # block: the gate would open SILENTLY. Both shapes are pinned below.
    LINGER = 15

    def _lingering_grandchild(self, then):
        return (
            '"%s" -c "import subprocess, sys;'
            " subprocess.Popen([sys.executable, '-c', 'import time;"
            " time.sleep(%d)']); %s\"" % (sys.executable, self.LINGER, then)
        )

    def test_a_lingering_grandchild_does_not_extend_the_hook(self):
        # The check itself finishes (red), but leaves a child holding the
        # output handle. The hook must report and return AT ONCE.
        cmd = self._lingering_grandchild("raise SystemExit(1)")
        start = time.monotonic()
        result = run_hook({"stop_hook_active": False}, cmd)
        elapsed = time.monotonic() - start
        self.assertEqual(result.returncode, 2)
        self.assertLess(
            elapsed, self.LINGER - 5,
            "a lingering grandchild held the hook for %.1fs" % elapsed,
        )

    def test_timeout_caps_a_hanging_check_whose_tree_survives(self):
        # The worst case: the check HANGS and its tree holds the output.
        # Only our own cap can end this -- and it must, well inside the
        # hook runner's.
        cmd = self._lingering_grandchild("time.sleep(%d)" % self.LINGER)
        cmd = cmd.replace("import subprocess, sys;", "import subprocess, sys, time;")
        start = time.monotonic()
        result = run_hook({"stop_hook_active": False}, cmd,
                          env_overrides={"HARNESS_CHECK_TIMEOUT": "2"})
        elapsed = time.monotonic() - start
        self.assertEqual(result.returncode, 2)
        self.assertIn("timed out", result.stderr)
        self.assertLess(
            elapsed, self.LINGER - 5,
            "the 2s cap did not bound wall time: %.1fs" % elapsed,
        )

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

    def test_self_test_accepts_quoted_tool_path(self):
        # Windows tools often live under paths with spaces; the quoted
        # form must not be split at the space (was a false FAIL).
        result = run_hook({}, '"%s" -V' % sys.executable, extra_args=["--self-test"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("self-test OK", result.stdout)

    def test_self_test_ignores_operators_inside_quotes(self):
        # A | inside a quoted argument is not a pipe (was a false FAIL).
        cmd = '"%s" -c "x = \'a|b\'"' % sys.executable
        result = run_hook({}, cmd, extra_args=["--self-test"])
        self.assertEqual(result.returncode, 0)

    def test_self_test_skips_shell_builtins(self):
        # cd resolves via the shell at run time, never via PATH lookup.
        cmd = 'cd . && "%s" -V' % sys.executable
        result = run_hook({}, cmd, extra_args=["--self-test"])
        self.assertEqual(result.returncode, 0)

    def test_self_test_checks_segments_after_npm_run(self):
        # A compound starting with npm run must still validate the rest.
        tmp = tempfile.mkdtemp()
        with open(os.path.join(tmp, "package.json"), "w", encoding="utf-8") as f:
            json.dump({"scripts": {"check": "true"}}, f)
        cmd = "npm run check && definitely-missing-tool-xyz"
        result = run_hook({}, cmd, extra_args=["--self-test"], cwd=tmp)
        self.assertEqual(result.returncode, 1)
        self.assertIn("not found", result.stdout)


if __name__ == "__main__":
    unittest.main()
