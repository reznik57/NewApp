"""Tests for base/.claude/hooks/protect_files.py — run from the seed root:
python -m unittest discover -s tests -v
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[2] / "base" / ".claude" / "hooks" / "protect_files.py"


def run_hook(tool_input):
    payload = json.dumps({"tool_name": "Edit", "tool_input": tool_input})
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=payload, capture_output=True, text=True, timeout=30,
    )


class ProtectFilesTests(unittest.TestCase):
    def test_blocks_env_file(self):
        result = run_hook({"file_path": "C:/proj/.env"})
        self.assertEqual(result.returncode, 2)
        self.assertIn("secrets", result.stderr)

    def test_blocks_env_variant(self):
        result = run_hook({"file_path": "/home/u/proj/.env.production"})
        self.assertEqual(result.returncode, 2)

    def test_allows_env_example(self):
        result = run_hook({"file_path": "C:/proj/.env.example"})
        self.assertEqual(result.returncode, 0)

    def test_blocks_lockfile(self):
        result = run_hook({"file_path": "C:/proj/package-lock.json"})
        self.assertEqual(result.returncode, 2)
        self.assertIn("lockfile", result.stderr)

    def test_blocks_git_internals(self):
        result = run_hook({"file_path": "C:/proj/.git/config"})
        self.assertEqual(result.returncode, 2)

    def test_blocks_file_named_git(self):
        # In worktrees/submodules .git is a FILE (gitdir pointer), not a dir;
        # it must be protected even with no .git parent segment.
        result = run_hook({"file_path": "C:/proj/wt/.git"})
        self.assertEqual(result.returncode, 2)

    def test_blocks_modern_bun_lockfile(self):
        # bun.lock (text) is Bun's default lockfile since 1.2; bun.lockb is legacy.
        result = run_hook({"file_path": "C:/proj/bun.lock"})
        self.assertEqual(result.returncode, 2)
        self.assertIn("lockfile", result.stderr)

    def test_blocks_harness_hook_edit(self):
        result = run_hook({"file_path": "C:/proj/.claude/hooks/verify_on_stop.py"})
        self.assertEqual(result.returncode, 2)
        self.assertIn("harness", result.stderr)

    def test_blocks_harness_script_edit(self):
        result = run_hook({"file_path": ".claude/scripts/check_markers.py"})
        self.assertEqual(result.returncode, 2)

    def test_blocks_harness_settings_edit(self):
        result = run_hook({"file_path": "C:/proj/.claude/settings.json"})
        self.assertEqual(result.returncode, 2)
        result = run_hook({"file_path": "C:/proj/.claude/settings.local.json"})
        self.assertEqual(result.returncode, 2)

    def test_allows_skill_edit(self):
        # Skills stay agent-editable by design (ultrathink: "update this file").
        result = run_hook({"file_path": "C:/proj/.claude/skills/ultrathink/SKILL.md"})
        self.assertEqual(result.returncode, 0)

    def test_blocks_env_example_inside_git_dir(self):
        result = run_hook({"file_path": "C:/proj/.git/.env.example"})
        self.assertEqual(result.returncode, 2)

    def test_blocks_symlink_to_env(self):
        tmp = tempfile.mkdtemp()
        target = os.path.join(tmp, ".env")
        link = os.path.join(tmp, "harmless.txt")
        with open(target, "w", encoding="utf-8") as f:
            f.write("SECRET=1")
        try:
            os.symlink(target, link)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable on this system")
        result = run_hook({"file_path": link})
        self.assertEqual(result.returncode, 2)

    def test_blocks_protected_notebook_path(self):
        # NotebookEdit sends notebook_path, not file_path (matcher covers it).
        result = run_hook({"notebook_path": "C:/proj/.git/notes.ipynb"})
        self.assertEqual(result.returncode, 2)

    def test_allows_normal_source_file(self):
        result = run_hook({"file_path": "C:/proj/src/app.ts"})
        self.assertEqual(result.returncode, 0)

    def test_allows_on_malformed_input(self):
        result = subprocess.run(
            [sys.executable, str(HOOK)],
            input="not json", capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0)

    def test_blocks_env_file_with_utf8_bom(self):
        # Windows PowerShell's `|` pipe to a native process prepends a UTF-8
        # BOM. json.load() on a text stream does not strip it, which used to
        # make this hook mistake the payload for malformed input and fail
        # OPEN (allow the edit) instead of blocking it. Regression guard.
        payload = json.dumps({"tool_name": "Edit", "tool_input": {"file_path": "C:/proj/.env"}})
        result = subprocess.run(
            [sys.executable, str(HOOK)],
            input=b"\xef\xbb\xbf" + payload.encode("utf-8"),
            capture_output=True, timeout=30,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"secrets", result.stderr)

    def test_allows_on_missing_file_path(self):
        result = run_hook({})
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
