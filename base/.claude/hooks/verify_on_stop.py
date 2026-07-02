#!/usr/bin/env python3
"""Stop hook: run the fast verification gate before the agent stops.

Exit 0 lets the agent stop; exit 2 blocks the stop and feeds stderr back so
the agent fixes the failure first. Stdlib only; Windows-safe.
Registered in .claude/settings.json under Stop.

--self-test verifies the wiring (used by SETUP.md step 4).
"""
import json
import os
import subprocess
import sys

# ADAPT: the single configuration point. Must match CLAUDE.md's Verification
# Gate and CI. HARNESS_CHECK_CMD env override exists as a test seam.
CHECK_COMMAND = os.environ.get("HARNESS_CHECK_CMD", "npm run check")
TIMEOUT_SECONDS = 300
OUTPUT_TAIL_CHARS = 3000


def run_check():
    try:
        result = subprocess.run(
            CHECK_COMMAND, shell=True, capture_output=True, text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        print(
            "verify_on_stop: '%s' timed out after %ss."
            % (CHECK_COMMAND, TIMEOUT_SECONDS),
            file=sys.stderr,
        )
        return 2
    if result.returncode == 0:
        return 0
    output = (result.stdout or "") + (result.stderr or "")
    print(
        "verify_on_stop: '%s' failed (exit %s). Fix before stopping.\n%s"
        % (CHECK_COMMAND, result.returncode, output[-OUTPUT_TAIL_CHARS:]),
        file=sys.stderr,
    )
    return 2


def self_test():
    if CHECK_COMMAND.startswith("npm run "):
        script = CHECK_COMMAND[len("npm run "):].split()[0]
        try:
            with open("package.json", encoding="utf-8") as f:
                scripts = json.load(f).get("scripts", {})
        except (OSError, ValueError) as exc:
            print("self-test FAIL: cannot read package.json (%s)" % exc)
            return 1
        if script not in scripts:
            print("self-test FAIL: package.json has no '%s' script" % script)
            return 1
    print("self-test OK: check command is '%s'" % CHECK_COMMAND)
    return 0


def main():
    if "--self-test" in sys.argv:
        return self_test()
    try:
        # Read as bytes: json.loads() strips a leading UTF-8 BOM per spec,
        # but json.load() on a text stream does not (Windows PowerShell's
        # pipe to a native process prepends a BOM, which would otherwise be
        # misread as malformed input and silently drop stop_hook_active).
        payload = json.loads(sys.stdin.buffer.read())
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
        payload = {}
    if payload.get("stop_hook_active"):
        return 0  # this stop was already triggered by us once; let it through
    return run_check()


if __name__ == "__main__":
    sys.exit(main())
