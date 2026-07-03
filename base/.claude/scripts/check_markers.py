#!/usr/bin/env python3
"""Exit gate: fail if template markers survive setup.

Single home for the leftover-marker check — SETUP.md step 12 and the
wiki-lint skill both run this script instead of maintaining their own
grep incantations. Exit 0: clean; exit 1: leftovers listed on stdout, or
CLAUDE.md missing (wrong cwd / step-7 rename skipped — fail loud, never
false-green). Run from the app root. Stdlib only; Windows-safe.
"""
# template-version: 2026-07.6
import re
import sys
from pathlib import Path

SCAN_TOPS = ["CLAUDE.md", ".claude", "docs", ".github"]
MARKERS = ("{{", "ADAPT:")
# ADAPT: if the app's stack uses {{ legitimately (Handlebars, Jinja,
# Angular, Vue, Liquid), code samples in docs/ would turn this check —
# and wiki-lint step 5 — permanently red: narrow MARKERS or extend
# EXEMPT for those paths.
# Exempt: reusable templates that ship with placeholders forever (copy
# them, never fill them in place) and files that legitimately keep ADAPT:
# tailoring markers or quote the marker syntax (including this script).
EXEMPT = re.compile(
    r"docs[\\/]adr[\\/]0000-template\.md$"
    r"|docs[\\/]specs[\\/]SPEC\.template\.md$"
    r"|\.claude[\\/]hooks[\\/](protect_files|verify_on_stop)\.py$"
    r"|\.claude[\\/]scripts[\\/]check_markers\.py$"
)


def read_lines(f):
    # BOM-aware: PowerShell 5.1 redirection writes UTF-16 LE, where a
    # plain utf-8 decode keeps interleaved NULs and "{{" never matches.
    raw = f.read_bytes()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return raw.decode("utf-16", errors="ignore").splitlines()
    return raw.decode("utf-8-sig", errors="ignore").splitlines()


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
    if not (root / "CLAUDE.md").is_file():
        print(
            "check_markers: CLAUDE.md not found — run from the app root"
            " (SETUP step 7 renames CLAUDE.template.md)"
        )
        return 1
    hits = []
    for f in iter_files(root):
        rel = str(f.relative_to(root))
        if EXEMPT.search(rel):
            continue
        try:
            lines = read_lines(f)
        except OSError:
            continue
        for lineno, line in enumerate(lines, 1):
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
