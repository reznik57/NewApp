"""Tests for base/.claude/scripts/check_markers.py — run from the seed root:
python -m unittest discover -s tests -v
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "base" / ".claude" / "scripts" / "check_markers.py"


def run_check(app_root):
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=app_root, capture_output=True, text=True, timeout=30,
    )


class CheckMarkersTests(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)

    def write(self, rel, content):
        path = Path(self.root) / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_clean_app_passes(self):
        self.write("CLAUDE.md", "# CLAUDE.md\nAll filled.\n")
        self.write("docs/wiki/index.md", "# Index\n")
        result = run_check(self.root)
        self.assertEqual(result.returncode, 0)
        self.assertIn("marker check OK", result.stdout)

    def test_leftover_placeholder_fails_with_location(self):
        self.write("CLAUDE.md", "Stack: {{LANGUAGE}}\n")
        result = run_check(self.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("CLAUDE.md:1", result.stdout)

    def test_unrenamed_template_at_the_app_root_fails(self):
        # SETUP step 7 renames CLAUDE.template.md -> CLAUDE.md. The script
        # claims to fail loud when that rename was skipped -- but it detects
        # it only by CLAUDE.md's ABSENCE, and a scaffolder that generated its
        # own CLAUDE.md (SETUP step 1 anticipates exactly this) satisfies the
        # check while the kit's manual sits beside it, unrenamed and full of
        # slots. Measured: 21 live placeholders, "marker check OK", exit 0.
        self.write("CLAUDE.md", "# My App\nScaffold-generated, no markers.\n")
        self.write("CLAUDE.template.md", "Domain: {{DOMAIN}}\n")
        result = run_check(self.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("CLAUDE.template.md", result.stdout)

    def test_leftover_adapt_note_fails(self):
        self.write("CLAUDE.md", "clean\n")
        self.write("docs/notes.md", "ADAPT: fill this in\n")
        result = run_check(self.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("notes.md", result.stdout)

    def test_reusable_templates_are_exempt(self):
        self.write("CLAUDE.md", "clean\n")
        self.write("docs/adr/0000-template.md", "# {{Title}}\n")
        self.write("docs/specs/SPEC.template.md", "# Spec: {{Feature name}}\n")
        result = run_check(self.root)
        self.assertEqual(result.returncode, 0)

    def test_hooks_are_exempt(self):
        self.write("CLAUDE.md", "clean\n")
        self.write(".claude/hooks/protect_files.py", "# ADAPT: extend these per project.\n")
        result = run_check(self.root)
        self.assertEqual(result.returncode, 0)

    def test_missing_claude_md_fails_loud(self):
        # Wrong cwd or a skipped step-7 rename must never be a false green.
        self.write("docs/x.md", "clean\n")
        result = run_check(self.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("CLAUDE.md not found", result.stdout)

    def test_utf16_file_markers_detected(self):
        # PowerShell 5.1 redirection writes UTF-16 LE; the gate must still
        # see markers there (plain utf-8 decode keeps interleaved NULs).
        self.write("CLAUDE.md", "clean\n")
        path = Path(self.root) / "docs" / "note.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("Stack: {{LANGUAGE}}\n", encoding="utf-16")
        result = run_check(self.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("note.md", result.stdout)

    def test_missing_github_dir_is_fine(self):
        # Step 10 allows deleting .github entirely; the scan must not choke.
        self.write("CLAUDE.md", "clean\n")
        result = run_check(self.root)
        self.assertEqual(result.returncode, 0)

    def test_github_actions_expressions_are_not_markers(self):
        # ${{ ... }} is GitHub Actions syntax, not a template slot — and
        # .github/ is deliberately still scanned (see the next test), so
        # this must pass via marker logic, not a path exemption.
        self.write("CLAUDE.md", "clean\n")
        self.write(
            ".github/workflows/ci.yml",
            "key: nuget-${{ runner.os }}-${{ hashFiles('**/*.csproj') }}\n",
        )
        result = run_check(self.root)
        self.assertEqual(result.returncode, 0)

    def test_bare_slot_in_workflow_still_fails(self):
        # The reason .github/workflows/ gets no blanket exemption: an
        # unfilled kit slot in ci.yml must still fail the exit gate.
        self.write("CLAUDE.md", "clean\n")
        self.write(".github/workflows/ci.yml", "        run: {{CHECK CMD}}\n")
        result = run_check(self.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("ci.yml", result.stdout)

    def test_emoji_hit_survives_cp1252_stdout(self):
        # A gate must judge any input without crashing on it: Windows
        # consoles default to cp1252, which cannot encode an emoji in a
        # hit line — the report must print, not traceback (a crash exits
        # 1 too, indistinguishable from "markers found" minus the list).
        self.write("CLAUDE.md", "clean\n")
        self.write("docs/notes.md", "> \U0001f4dd ADAPT: fill this in\n")
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=self.root, capture_output=True, timeout=30,
            env=dict(os.environ, PYTHONIOENCODING="cp1252"),
        )
        stdout = result.stdout.decode("utf-8", errors="replace")
        self.assertEqual(result.returncode, 1)
        self.assertIn("notes.md", stdout)
        self.assertNotIn(b"Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
