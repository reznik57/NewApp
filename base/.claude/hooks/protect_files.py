#!/usr/bin/env python3
"""PreToolUse hook: block agent edits to protected files.

Reads the tool-call JSON from stdin. Exit 2 blocks the call and feeds the
stderr message back to the agent; exit 0 allows it. Stdlib only; Windows-safe.
Registered in .claude/settings.json under PreToolUse, matcher "Edit|Write|NotebookEdit".
"""
# template-version: 2026-07.4
import json
import os
import sys
from pathlib import PurePath

# ADAPT: extend these per project.
PROTECTED_BASENAMES = {
    "package-lock.json", "npm-shrinkwrap.json", "pnpm-lock.yaml",
    "yarn.lock", "bun.lock", "bun.lockb",
}
PROTECTED_SEGMENTS = {".git"}
ALLOWED_ENV_FILES = {".env.example"}


def check_path(file_path):
    """Return a human-readable reason if this path string is protected."""
    path = PurePath(file_path.replace("\\", "/"))
    name = path.name.lower()
    for segment in path.parts[:-1]:
        if segment.lower() in PROTECTED_SEGMENTS:
            return "%s/ internals must not be edited directly" % segment
    if name == ".git":
        return ".git is a git internal (worktree/submodule pointer); must not be edited directly"
    # The harness protects itself: hooks, scripts, and settings are edited
    # by the USER, never by the agent they bind. (SETUP step 4's
    # CHECK_COMMAND edit happens before settings activation in step 5, so
    # setup is unaffected; skills stay agent-editable by design.)
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
    try:
        # Read as bytes: json.loads() strips a leading UTF-8 BOM per spec,
        # but json.load() on a text stream does not (Windows PowerShell's
        # pipe to a native process prepends a BOM, which would otherwise
        # be misread as malformed input and fail this hook OPEN).
        payload = json.loads(sys.stdin.buffer.read())
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
        return 0  # malformed input: never block on our own bug
    tool_input = payload.get("tool_input") or {}
    file_path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if not file_path:
        return 0
    reason = is_protected(file_path)
    if reason:
        print("BLOCKED by protect_files hook: %s." % reason, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
