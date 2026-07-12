#!/usr/bin/env python3
"""PreToolUse hook: block agent edits to protected files.

Reads the tool-call JSON from stdin. Exit 2 blocks the call and feeds the
stderr message back to the agent; exit 0 allows it. Stdlib only; Windows-safe.
Registered in .claude/settings.json under PreToolUse (that file owns the
matcher — it must cover every write tool, native AND MCP; the seam is
pinned by tests/hooks/test_protect_files.py).

Bash is deliberately NOT matched: this guard is friction plus forced user
involvement, not a security boundary. When it rightly blocks a needed
harness edit, the sanctioned path is the user applying the change or
explicitly delegating it (e.g. a scripted patch) — never a silent bypass.

--probe <path> checks one path against the block/allow logic with the
hook's exit contract (2 blocked, 0 allowed) — a setup-time seam that
avoids hand-built stdin JSON (where a typo makes the fail-open path
look like "allowed"). It does NOT verify the settings.json
registration; the live .env-edit probe in a fresh session does.
"""
# template-version: 2026-07.29
import json
import os
import posixpath
import sys
from pathlib import PurePath

# Where a tool names its target, in priority order. "file_path" /
# "notebook_path" are Claude Code's native Edit/Write/NotebookEdit;
# "path" is what MCP write tools use (observed live: omnigent's
# mcp__omnigent__sys_os_edit wrote a protected file straight through
# this hook, because it matched no key here AND no matcher entry — the
# registration in settings.json must stay in step, which
# test_protect_files pins).
PATH_KEYS = ("file_path", "notebook_path", "path")

# ADAPT: extend these per project.
PROTECTED_BASENAMES = {
    "package-lock.json", "npm-shrinkwrap.json", "pnpm-lock.yaml",
    "yarn.lock", "bun.lock", "bun.lockb",
}
PROTECTED_SEGMENTS = {".git"}
ALLOWED_ENV_FILES = {".env.example"}
# A text Edit/Write into a binary file is ALWAYS corruption, wherever
# the file lives — suffix rule, not path list. ADAPT: extend with the
# app's own binary crown jewels (e.g. .xlsm masters).
BINARY_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico",
    ".pdf", ".xlsx", ".xls", ".docx",
    ".zip", ".gz", ".7z",
    ".db", ".sqlite", ".sqlite3",
    ".woff", ".woff2", ".ttf", ".otf",
}


def check_path(file_path):
    """Return a human-readable reason if this path string is protected."""
    # Collapse ".." lexically first: ".claude/hooks/../skills/x" is a
    # skill (agent-editable), ".claude/skills/../hooks/x" is a hook.
    path = PurePath(posixpath.normpath(file_path.replace("\\", "/")))
    name = path.name.lower()
    for segment in path.parts[:-1]:
        if segment.lower() in PROTECTED_SEGMENTS:
            return "%s/ internals must not be edited directly" % segment
    if name == ".git":
        return ".git is a git internal (worktree/submodule pointer); must not be edited directly"
    # The harness protects itself: hooks, scripts, and settings are edited
    # by the USER, never by the agent they bind. Harness edits therefore
    # belong BEFORE activation — SETUP step 4, i.e. ahead of step 5, or
    # ahead of step 2 when a stack profile copies settings.json in; after
    # activation they are the ask-the-user case. (Skills stay
    # agent-editable by design.)
    parts_lower = [s.lower() for s in path.parts]
    for i in range(len(parts_lower) - 2):
        if parts_lower[i] == ".claude" and parts_lower[i + 1] in ("hooks", "scripts"):
            return "the harness must not be edited by the agent it binds; ask the user"
    if name in ("settings.json", "settings.local.json") \
            and len(parts_lower) >= 2 and parts_lower[-2] == ".claude":
        return "the harness must not be edited by the agent it binds; ask the user"
    if name in ALLOWED_ENV_FILES:
        return None
    if name == ".env" or name.startswith(".env."):
        return "%s may contain secrets; the user edits it manually" % path.name
    if name in PROTECTED_BASENAMES:
        return "%s is a lockfile; change deps via the package manager" % path.name
    if PurePath(name).suffix in BINARY_SUFFIXES:
        return ("%s is a binary file; a text edit corrupts it — "
                "use a proper tool or ask the user" % path.name)
    return None


def is_protected(file_path):
    """Check the raw path, then its symlink-resolved target."""
    reason = check_path(file_path)
    if reason:
        return reason
    real = os.path.realpath(file_path)
    if real and real != file_path:
        return check_path(real)
    return None


def main():
    if "--probe" in sys.argv:
        args = sys.argv[sys.argv.index("--probe") + 1:]
        if not args:
            print("usage: protect_files.py --probe <path>", file=sys.stderr)
            return 2
        reason = is_protected(args[0])
        if reason:
            print("BLOCKED: %s." % reason)
            return 2
        print("allowed: %s" % args[0])
        return 0
    try:
        # Read as bytes: json.loads() strips a leading UTF-8 BOM per spec,
        # but json.load() on a text stream does not (Windows PowerShell's
        # pipe to a native process prepends a BOM, which would otherwise
        # be misread as malformed input and fail this hook OPEN).
        payload = json.loads(sys.stdin.buffer.read())
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
        return 0  # malformed input: never block on our own bug
    tool_input = payload.get("tool_input") or {}
    file_path = next(
        (tool_input[k] for k in PATH_KEYS if tool_input.get(k)), ""
    )
    if not file_path:
        # Unknown schema: fail OPEN, deliberately. A matched tool whose
        # target we cannot read is more likely a non-file write (an MCP
        # server creating a page/issue) than a disguised file edit, and
        # blocking every unreadable payload would break those. The cost
        # of this choice is bounded by PATH_KEYS staying current — add a
        # key the moment a real MCP write tool names its target
        # differently.
        return 0
    reason = is_protected(file_path)
    if reason:
        print("BLOCKED by protect_files hook: %s." % reason, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
