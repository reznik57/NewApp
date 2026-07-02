#!/usr/bin/env python3
"""PreToolUse hook: block agent edits to protected files.

Reads the tool-call JSON from stdin. Exit 2 blocks the call and feeds the
stderr message back to the agent; exit 0 allows it. Stdlib only; Windows-safe.
Registered in .claude/settings.json under PreToolUse, matcher "Edit|Write|NotebookEdit".
"""
import json
import os
import sys
from pathlib import PurePath

# ADAPT: extend these per project.
PROTECTED_BASENAMES = {
    "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb",
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
    file_path = (payload.get("tool_input") or {}).get("file_path", "")
    if not file_path:
        return 0
    reason = is_protected(file_path)
    if reason:
        print("BLOCKED by protect_files hook: %s." % reason, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
