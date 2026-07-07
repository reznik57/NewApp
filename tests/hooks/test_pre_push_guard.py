"""Tests for .githooks/pre_push_guard.py -- run from the seed root:
python -m unittest discover -s tests -v

The guard mechanizes CLAUDE.md -> Repo identity (the v2.4.7
push-onto-template incident): pushes from a working copy with the guard
active must target the template repo, and the tip of every pushed ref
must look like the seed (carry TEMPLATE-CHANGELOG.md; deliberately
tip-only -- see the guard's docstring).
"""
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GUARD_DIR = ROOT / ".githooks"
GUARD = GUARD_DIR / "pre_push_guard.py"
SHIM = GUARD_DIR / "pre-push"
TEMPLATE_URL = "https://github.com/reznik57/NewApp.git"
NORMALIZED = "github.com/reznik57/newapp"
ZERO = "0" * 40

sys.path.insert(0, str(GUARD_DIR))
import pre_push_guard  # noqa: E402


def run_git(cwd, *args):
    return subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.com",
         "-c", "commit.gpgsign=false"] + list(args),
        cwd=str(cwd), capture_output=True, text=True, timeout=60,
    )


def rmtree_force(path):
    """Windows: .git objects are read-only; clear the bit, then delete."""
    def onerror(func, p, _exc):
        os.chmod(p, stat.S_IWRITE)
        func(p)
    shutil.rmtree(path, onerror=onerror)


def make_repo(tmp, with_marker):
    """Init a repo with one commit; return its HEAD sha."""
    run_git(tmp, "init", "-q")
    if with_marker:
        (tmp / "TEMPLATE-CHANGELOG.md").write_text(
            "# Template Changelog\n", encoding="utf-8")
    (tmp / "somefile.txt").write_text("content\n", encoding="utf-8")
    run_git(tmp, "add", "-A")
    run_git(tmp, "commit", "-q", "-m", "c1")
    return run_git(tmp, "rev-parse", "HEAD").stdout.strip()


def run_guard(cwd, url, stdin_text, *extra):
    return subprocess.run(
        [sys.executable, str(GUARD)] + list(extra) + ["origin", url],
        input=stdin_text, cwd=str(cwd), capture_output=True, text=True,
        timeout=60,
    )


class NormalizeTests(unittest.TestCase):
    def test_accepts_all_remote_url_forms_of_the_template(self):
        for url in (
            "https://github.com/reznik57/NewApp.git",
            "https://github.com/reznik57/NewApp",
            "https://github.com/Reznik57/newapp/",
            "git@github.com:reznik57/NewApp.git",
            "ssh://git@github.com/reznik57/NewApp.git",
        ):
            self.assertEqual(pre_push_guard.normalize(url), NORMALIZED, url)

    def test_other_repos_do_not_normalize_to_the_template(self):
        for url in (
            "https://github.com/reznik57/fisi-learning.git",
            "https://gitlab.com/reznik57/NewApp.git",
            "git@github.com:someone/NewApp.git",
            "D:/somewhere/bare",
            "",
        ):
            self.assertNotEqual(pre_push_guard.normalize(url), NORMALIZED, url)

    def test_garbage_normalizes_to_none(self):
        self.assertIsNone(pre_push_guard.normalize("notaurl"))


class GuardBehaviorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="prepush-"))
        self.addCleanup(rmtree_force, self.tmp)

    def seed_repo(self, with_marker=True):
        return make_repo(self.tmp, with_marker)

    def test_wrong_remote_url_blocks(self):
        sha = self.seed_repo()
        line = "refs/heads/x %s refs/heads/x %s\n" % (sha, ZERO)
        r = run_guard(self.tmp, "https://github.com/reznik57/some-app.git", line)
        self.assertEqual(r.returncode, 1)
        self.assertIn("not the template repo", r.stderr)

    def test_seed_content_to_template_url_passes(self):
        sha = self.seed_repo()
        line = "refs/heads/x %s refs/heads/x %s\n" % (sha, ZERO)
        r = run_guard(self.tmp, TEMPLATE_URL, line)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_app_content_to_template_url_blocks(self):
        # The v2.4.7 incident class: a history without the seed marker
        # heading for the template remote.
        sha = self.seed_repo(with_marker=False)
        line = "refs/heads/x %s refs/heads/x %s\n" % (sha, ZERO)
        r = run_guard(self.tmp, TEMPLATE_URL, line)
        self.assertEqual(r.returncode, 1)
        self.assertIn("TEMPLATE-CHANGELOG.md", r.stderr)

    def test_annotated_tag_push_passes(self):
        self.seed_repo()
        run_git(self.tmp, "tag", "-a", "v0", "-m", "tag")
        tag_sha = run_git(self.tmp, "rev-parse", "v0").stdout.strip()
        line = "refs/tags/v0 %s refs/tags/v0 %s\n" % (tag_sha, ZERO)
        r = run_guard(self.tmp, TEMPLATE_URL, line)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_ref_deletion_passes_without_content_check(self):
        self.seed_repo(with_marker=False)  # even app-shaped: nothing local
        line = "(delete) %s refs/heads/gone %s\n" % (ZERO, "a" * 40)
        r = run_guard(self.tmp, TEMPLATE_URL, line)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_empty_stdin_passes(self):
        self.seed_repo()
        r = run_guard(self.tmp, TEMPLATE_URL, "")
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_malformed_input_line_fails_closed(self):
        self.seed_repo()
        r = run_guard(self.tmp, TEMPLATE_URL, "garbage line\n")
        self.assertEqual(r.returncode, 1)
        self.assertIn("unexpected pre-push input", r.stderr)

    def test_missing_args_fail_closed(self):
        r = subprocess.run(
            [sys.executable, str(GUARD)], input="", cwd=str(self.tmp),
            capture_output=True, text=True, timeout=60,
        )
        self.assertEqual(r.returncode, 1)


class SelfTestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="prepush-st-"))
        self.addCleanup(rmtree_force, self.tmp)
        make_repo(self.tmp, with_marker=True)

    def install_hook_file(self):
        hooks = self.tmp / ".githooks"
        hooks.mkdir(exist_ok=True)
        shutil.copy(SHIM, hooks / "pre-push")

    def run_self_test(self):
        return subprocess.run(
            [sys.executable, str(GUARD), "--self-test"], cwd=str(self.tmp),
            capture_output=True, text=True, timeout=60,
        )

    def test_healthy_wiring_passes(self):
        run_git(self.tmp, "remote", "add", "origin", TEMPLATE_URL)
        self.install_hook_file()
        run_git(self.tmp, "config", "core.hooksPath", ".githooks")
        r = self.run_self_test()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("guard active", r.stdout)

    def test_equivalent_hookspath_spellings_pass(self):
        # An absolute path or a trailing slash is functionally active;
        # the self-test must not false-negative on those spellings.
        run_git(self.tmp, "remote", "add", "origin", TEMPLATE_URL)
        self.install_hook_file()
        for value in (str(self.tmp / ".githooks"), ".githooks/"):
            run_git(self.tmp, "config", "core.hooksPath", value)
            r = self.run_self_test()
            self.assertEqual(r.returncode, 0, "%s: %s" % (value, r.stderr))

    def test_missing_hook_file_fails(self):
        # hooksPath set but no .githooks/pre-push in the tree (old-tag
        # or sparse checkout): git silently skips absent hooks, so the
        # self-test must report the third no-fire path.
        run_git(self.tmp, "remote", "add", "origin", TEMPLATE_URL)
        run_git(self.tmp, "config", "core.hooksPath", ".githooks")
        r = self.run_self_test()
        self.assertEqual(r.returncode, 1)
        self.assertIn("missing", r.stderr)

    def test_wrong_origin_fails(self):
        run_git(self.tmp, "remote", "add", "origin",
                "https://github.com/reznik57/some-app.git")
        self.install_hook_file()
        run_git(self.tmp, "config", "core.hooksPath", ".githooks")
        r = self.run_self_test()
        self.assertEqual(r.returncode, 1)
        self.assertIn("expected", r.stderr)

    def test_inactive_hookspath_fails(self):
        run_git(self.tmp, "remote", "add", "origin", TEMPLATE_URL)
        r = self.run_self_test()
        self.assertEqual(r.returncode, 1)
        self.assertIn("hooksPath", r.stderr)


class CommittedGuardTests(unittest.TestCase):
    """Pin the committed shim's index mode and line endings: a 100644
    or CRLF regression (easy on Windows, where new files stage as 644
    and the working tree hides both) is a silent fail-open on every
    Linux clone -- git skips non-executable hooksPath hooks with a mere
    hint, and sh chokes on \\r."""

    def test_shim_is_executable_in_the_index(self):
        r = run_git(ROOT, "ls-files", "-s", ".githooks/pre-push")
        self.assertTrue(r.stdout.startswith("100755 "), r.stdout)

    def test_shim_is_lf_in_the_index(self):
        r = run_git(ROOT, "ls-files", "--eol", ".githooks/pre-push")
        self.assertIn("i/lf", r.stdout)


class EndToEndWiringTests(unittest.TestCase):
    """A real `git push` must reach the guard through the sh shim."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="prepush-e2e-"))
        self.addCleanup(rmtree_force, self.tmp)

    def test_push_to_non_template_remote_is_blocked(self):
        repo = self.tmp / "repo"
        repo.mkdir()
        make_repo(repo, with_marker=True)
        hooks = repo / ".githooks"
        hooks.mkdir()
        shutil.copy(GUARD, hooks / "pre_push_guard.py")
        shutil.copy(SHIM, hooks / "pre-push")
        os.chmod(hooks / "pre-push", 0o755)  # Linux git skips non-exec hooks
        run_git(repo, "config", "core.hooksPath", ".githooks")
        bare = self.tmp / "bare.git"
        run_git(self.tmp, "init", "-q", "--bare", str(bare))
        run_git(repo, "remote", "add", "origin", str(bare))
        r = run_git(repo, "push", "origin", "HEAD:refs/heads/main")
        self.assertNotEqual(r.returncode, 0)
        # Must be check_push()'s own message: the shim's fail-closed
        # fallback also says "pre-push guard", which would green this
        # test without the guard ever running.
        self.assertIn("not the template repo", r.stderr)


if __name__ == "__main__":
    unittest.main()
