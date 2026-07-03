#!/usr/bin/env python3
"""Exit gate: fail if template markers survive setup.

Single home for the leftover-marker check — SETUP.md step 12 and the
wiki-lint skill both run this script instead of maintaining their own
grep incantations. Exit 0: clean; exit 1: leftovers listed on stdout.
Run from the app root. Stdlib only; Windows-safe.
"""
# template-version: 2026-07.4
import re
import sys
from pathlib import Path

SCAN_TOPS = ["CLAUDE.md", ".claude", "docs", ".github"]
MARKERS = ("{{", "ADAPT:")
# Exempt: reusable templates that ship with placeholders forever (copy
# them, never fill them in place) and files that legitimately keep ADAPT:
# tailoring markers or quote the marker syntax (including this script).
EXEMPT = re.compile(
    r"docs[\\/]adr[\\/]0000-template\.md$"
    r"|docs[\\/]specs[\\/]SPEC\.template\.md$"
    r"|\.claude[\\/]hooks[\\/](protect_files|verify_on_stop)\.py$"
    r"|\.claude[\\/]scripts[\\/]check_markers\.py$"
)


def iter_files(root):
    for top in SCAN_TOPS:
        p = root / top
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in p.rglob("*"):
                if f.is_file():
                    yield f


def main():
    root = Path.cwd()
    hits = []
    for f in iter_files(root):
        rel = str(f.relative_to(root))
        if EXEMPT.search(rel):
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if any(marker in line for marker in MARKERS):
                hits.append("%s:%d: %s" % (rel, lineno, line.strip()[:80]))
    if hits:
        print("Leftover template markers found:")
        print("\n".join(hits))
        return 1
    print("marker check OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
