"""Tests for base/.claude/hooks/protect_files.py — run from the seed root:
python -m unittest discover -s tests -v
"""
import json
import subprocess
import sys
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

    def test_blocks_env_example_inside_git_dir(self):
        result = run_hook({"file_path": "C:/proj/.git/.env.example"})
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

    def test_allows_on_missing_file_path(self):
        result = run_hook({})
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
