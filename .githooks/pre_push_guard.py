#!/usr/bin/env python3
"""Seed-side pre-push repo-identity guard (CLAUDE.md -> Repo identity).

This working copy is the TEMPLATE seed. The rule it mechanizes existed
as prose since the v2.4.7 push-onto-template incident (an app working
copy pushed onto the template remote); this guard makes the seed side
of that rule mechanical. Two checks, both fail closed:

  1. Wrong remote: the URL being pushed to must be the template repo.
     TEMPLATE_REPO below is the docs' single home of the exact URL --
     the docs link here instead of restating it; the tests pin it as
     deliberate friction.
  2. Wrong content: the TIP of every pushed ref must contain
     TEMPLATE-CHANGELOG.md -- a tip without it does not look like the
     seed, so an app history may be about to land on the template
     remote (the v2.4.7 incident class). Deliberately tip-only:
     foreign history merged under a marker-carrying tip passes (a
     range walk would false-block the seed's own three pre-changelog
     root commits).

Like protect_files.py this is an ACCIDENT GUARD, not a security
boundary: `git push --no-verify` skips it -- do that only deliberately,
with the user. A working tree without .githooks/ (old-tag or sparse
checkout) silently suspends the guard even with core.hooksPath set --
git neither runs nor warns about absent hooks; the self-test reports
the missing hook file. If the template repo really moves, update
TEMPLATE_REPO here AND the pinned expectations in
tests/hooks/test_pre_push_guard.py in the same commit (deliberate
friction, the test_root_docs REQUIRED pattern).

Activate once per clone (git config is not cloned):
    git config core.hooksPath .githooks
    py .githooks/pre_push_guard.py --self-test

Invoked by .githooks/pre-push with the pre-push protocol: argv is
<remote name> <remote url>; stdin carries one line per ref:
<local ref> SP <local sha> SP <remote ref> SP <remote sha>.
Tests: tests/hooks/test_pre_push_guard.py (run from the seed root).
"""
import os
import re
import subprocess
import sys

TEMPLATE_REPO = "github.com/reznik57/newapp"  # normalized: host/owner/repo
ZERO_SHA = "0" * 40
GIT_TIMEOUT = 30  # seconds per git call; a hang must not stall a push forever


def normalize(url):
    """Reduce a git remote URL to lowercase host/path, or None.

    Handles https://, ssh://, git://, and scp-like (git@host:path) forms;
    strips a trailing .git and slashes. GitHub treats owner/repo as
    case-insensitive, so everything is lowercased before comparing.
    """
    u = (url or "").strip().lower().rstrip("/")
    u = re.sub(r"\.git$", "", u)
    m = re.match(r"^(?:https?://|ssh://|git://)?(?:[^@/]+@)?([^:/]+)[:/](.+)$", u)
    if not m:
        return None
    return m.group(1) + "/" + m.group(2).strip("/")


def git(*args):
    """Run a git command; return (returncode, output). Fails closed on error."""
    try:
        proc = subprocess.run(
            ("git",) + args, capture_output=True, text=True, timeout=GIT_TIMEOUT
        )
        return proc.returncode, (proc.stdout or "").strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("pre-push guard: git call failed (%s) - failing closed" % exc,
              file=sys.stderr)
        sys.exit(1)


def commit_has_seed_marker(sha):
    code, _ = git("cat-file", "-e", "%s:TEMPLATE-CHANGELOG.md" % sha)
    return code == 0


def check_push(remote_name, remote_url, ref_lines):
    """Return a list of problems (empty = push may proceed)."""
    problems = []
    if normalize(remote_url) != TEMPLATE_REPO:
        problems.append(
            "remote '%s' (%s) is not the template repo (%s).\n"
            "This working copy is the TEMPLATE seed and pushes nowhere else\n"
            "(CLAUDE.md -> Repo identity). If the template repo really moved,\n"
            "update TEMPLATE_REPO in .githooks/pre_push_guard.py."
            % (remote_name, remote_url, TEMPLATE_REPO)
        )
        return problems  # wrong remote: content checks add nothing
    for line in ref_lines:
        parts = line.split()
        if not parts:
            continue
        if len(parts) != 4:
            problems.append("unexpected pre-push input line: %r" % line)
            continue
        local_ref, local_sha = parts[0], parts[1]
        if local_sha == ZERO_SHA:  # ref deletion: nothing local to inspect
            continue
        if not commit_has_seed_marker(local_sha):
            problems.append(
                "ref '%s' (%s) has no TEMPLATE-CHANGELOG.md - this does not\n"
                "look like the seed. An app may be pushing onto the template\n"
                "remote (the v2.4.7 incident class). See CLAUDE.md -> Repo\n"
                "identity." % (local_ref, local_sha[:12])
            )
    return problems


def self_test():
    """Verify the guard's own wiring in this clone. Exit 0 iff healthy."""
    failures = []
    code, url = git("remote", "get-url", "origin")
    if code != 0:
        failures.append("no 'origin' remote configured")
    elif normalize(url) != TEMPLATE_REPO:
        failures.append("origin is %s, expected %s" % (url, TEMPLATE_REPO))
    else:
        print("ok: origin -> %s" % url)
    code, _ = git("cat-file", "-e", "HEAD:TEMPLATE-CHANGELOG.md")
    if code != 0:
        failures.append("HEAD carries no TEMPLATE-CHANGELOG.md - not the seed?")
    else:
        print("ok: HEAD looks like the seed")
    code, hooks_path = git("config", "core.hooksPath")
    tcode, toplevel = git("rev-parse", "--show-toplevel")
    active = False
    if code == 0 and tcode == 0:
        # Equivalent spellings (absolute path, trailing slash, drive or
        # case variants on Windows) are functionally active: resolve
        # both sides before comparing.
        expected = os.path.normcase(
            os.path.realpath(os.path.join(toplevel, ".githooks")))
        actual = os.path.normcase(
            os.path.realpath(os.path.join(toplevel, hooks_path)))
        active = actual == expected
    if not active:
        failures.append(
            "core.hooksPath is %r - the guard is NOT active; run:\n"
            "  git config core.hooksPath .githooks"
            % (hooks_path if code == 0 else None)
        )
    elif not os.path.isfile(os.path.join(toplevel, ".githooks", "pre-push")):
        failures.append(
            ".githooks/pre-push is missing from this working tree (old-tag\n"
            "or sparse checkout?) - git silently skips absent hooks")
    else:
        print("ok: core.hooksPath -> .githooks and the hook file exists"
              " (guard active)")
    for f in failures:
        print("pre-push guard self-test: %s" % f, file=sys.stderr)
    return 1 if failures else 0


def main(argv):
    if "--self-test" in argv:
        return self_test()
    if len(argv) < 2:
        print("pre-push guard: expected <remote name> <remote url> from git -"
              " failing closed", file=sys.stderr)
        return 1
    problems = check_push(argv[0], argv[1], sys.stdin.read().splitlines())
    for p in problems:
        print("pre-push guard: refusing to push - %s" % p, file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
