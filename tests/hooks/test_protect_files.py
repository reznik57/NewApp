"""Tests for base/.claude/hooks/protect_files.py — run from the seed root:
python -m unittest discover -s tests -v
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / "base" / ".claude" / "hooks" / "protect_files.py"
SETTINGS = ROOT / "base" / ".claude" / "settings.template.json"


def run_hook(tool_input, tool_name="Edit"):
    payload = json.dumps({"tool_name": tool_name, "tool_input": tool_input})
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

    def test_blocks_binary_suffix_anywhere(self):
        # Suffix rule, not path list: a text Write into a binary is
        # always corruption, wherever the file lives.
        result = run_hook({"file_path": "C:/proj/content/img/chart.png"})
        self.assertEqual(result.returncode, 2)
        self.assertIn("binary", result.stderr)

    def test_blocks_binary_suffix_case_insensitive(self):
        result = run_hook({"file_path": "C:/proj/Screenshot.PNG"})
        self.assertEqual(result.returncode, 2)

    def test_allows_text_file_between_binaries(self):
        result = run_hook({"file_path": "C:/proj/content/pdf/notes.md"})
        self.assertEqual(result.returncode, 0)

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

    def test_allows_traversal_out_of_hooks_to_skill(self):
        # ".." is collapsed lexically before the harness check: this path
        # resolves to a skill, which stays agent-editable.
        result = run_hook({"file_path": ".claude/hooks/../skills/x/SKILL.md"})
        self.assertEqual(result.returncode, 0)

    def test_blocks_traversal_into_hooks(self):
        result = run_hook({"file_path": ".claude/skills/../hooks/verify_on_stop.py"})
        self.assertEqual(result.returncode, 2)

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

    def test_probe_blocked_path_exits_2(self):
        # --probe replaces hand-built stdin JSON at setup time, where a
        # payload typo hits the fail-open path and reads as "allowed".
        result = subprocess.run(
            [sys.executable, str(HOOK), "--probe", "C:/proj/.env"],
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("BLOCKED", result.stdout)

    def test_probe_allowed_path_exits_0(self):
        result = subprocess.run(
            [sys.executable, str(HOOK), "--probe", "src/app.py"],
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("allowed", result.stdout)

    def test_probe_without_path_fails_usage(self):
        result = subprocess.run(
            [sys.executable, str(HOOK), "--probe"],
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage", result.stderr)


class McpWriteToolTests(unittest.TestCase):
    """The bypass this hook was blind to (real incident, 2026-07-11).

    An MCP write tool escaped the guard TWICE over: its name missed the
    matcher, and its target sits under "path", not "file_path" — so even
    a matched call would have fallen through the empty-path fail-open.
    Both halves are pinned here; either one regressing re-opens the hole.
    """

    MCP_EDIT = "mcp__omnigent__sys_os_edit"

    def test_blocks_protected_file_named_under_path_key(self):
        result = run_hook({"path": "C:/proj/.env"}, tool_name=self.MCP_EDIT)
        self.assertEqual(result.returncode, 2)
        self.assertIn("secrets", result.stderr)

    def test_blocks_harness_edit_named_under_path_key(self):
        result = run_hook(
            {"path": ".claude/settings.json"}, tool_name=self.MCP_EDIT
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("harness", result.stderr)

    def test_allows_ordinary_file_named_under_path_key(self):
        result = run_hook({"path": "src/app.py"}, tool_name=self.MCP_EDIT)
        self.assertEqual(result.returncode, 0)

    def test_unreadable_schema_fails_open_deliberately(self):
        # Documented choice, not an oversight: a matched tool whose target
        # we cannot read is more likely a non-file write than a disguised
        # file edit. Locks the decision so a future change is deliberate.
        result = run_hook({"destination": ".env"}, tool_name=self.MCP_EDIT)
        self.assertEqual(result.returncode, 0)


class MatcherCoverageTests(unittest.TestCase):
    """Registration must cover what the hook defends against.

    The incident lived in the GAP between the hook and its settings.json
    registration — a hook that blocks correctly is worthless if the tool
    never reaches it. Nothing guarded that seam before; this does.
    """

    @classmethod
    def setUpClass(cls):
        settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
        entries = settings["hooks"]["PreToolUse"]
        cls.matcher = re.compile(entries[0]["matcher"])

    def test_matches_native_write_tools(self):
        for tool in ("Edit", "Write", "NotebookEdit"):
            self.assertTrue(self.matcher.search(tool), tool)

    def test_matches_mcp_write_tools(self):
        for tool in (
            "mcp__omnigent__sys_os_edit",
            "mcp__omnigent__sys_os_write",
            "mcp__filesystem__write_file",
            "mcp__whatever__create_file",
        ):
            self.assertTrue(self.matcher.search(tool), tool)

    def test_does_not_match_read_only_tools(self):
        # Over-matching is cheap (the hook allows any unprotected path),
        # under-matching loses the guard — but a matcher that fires on
        # every read would spawn a process per Read call.
        for tool in ("Read", "Grep", "Glob", "mcp__omnigent__sys_os_read"):
            self.assertIsNone(self.matcher.search(tool), tool)


if __name__ == "__main__":
    unittest.main()
