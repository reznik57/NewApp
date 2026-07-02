#!/usr/bin/env python3
"""PreToolUse hook: block agent edits to protected files.

Reads the tool-call JSON from stdin. Exit 2 blocks the call and feeds the
stderr message back to the agent; exit 0 allows it. Stdlib only; Windows-safe.
Registered in .claude/settings.json under PreToolUse, matcher "Edit|Write".
"""
import json
import sys
from pathlib import PurePath

# ADAPT: extend these per project.
PROTECTED_BASENAMES = {
    "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb",
}
PROTECTED_SEGMENTS = {".git"}
ALLOWED_ENV_FILES = {".env.example"}


def is_protected(file_path):
    """Return a human-readable reason if the path is protected, else None."""
    path = PurePath(file_path.replace("\\", "/"))
    name = path.name.lower()
    if name in ALLOWED_ENV_FILES:
        return None
    if name == ".env" or name.startswith(".env."):
        return "%s may contain secrets; the user edits it manually" % path.name
    if name in PROTECTED_BASENAMES:
        return "%s is a lockfile; change deps via the package manager" % path.name
    for segment in path.parts[:-1]:
        if segment.lower() in PROTECTED_SEGMENTS:
            return "%s/ internals must not be edited directly" % segment
    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
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
