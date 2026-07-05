#!/usr/bin/env python3
"""Exit gate: fail if template markers survive setup.

Single home for the leftover-marker check — SETUP.md step 12 and the
wiki-lint skill both run this script instead of maintaining their own
grep incantations. Exit 0: clean; exit 1: leftovers listed on stdout, or
CLAUDE.md missing (wrong cwd / step-7 rename skipped — fail loud, never
false-green). Run from the app root. Stdlib only; Windows-safe.
"""
# template-version: 2026-07.11
import re
import sys
from pathlib import Path

SCAN_TOPS = ["CLAUDE.md", ".claude", "docs", ".github"]
MARKERS = ("{{", "ADAPT:")
# A "{{" directly preceded by "$" is NOT a marker: GitHub Actions
# expressions (${{ matrix.os }}) live in the scanned .github/, and kit
# slots are never spelled ${{...}}. Deliberately handled here instead
# of exempting the path — an unfilled {{SLOT}} in ci.yml must still
# fail the gate.
# ADAPT: if the app's stack uses bare {{ legitimately (Handlebars,
# Jinja, Angular, Vue, Liquid), code samples in docs/ would turn this
# check — and wiki-lint step 5 — permanently red: narrow MARKERS or
# extend EXEMPT for those paths.
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


def has_marker(line):
    for marker in MARKERS:
        i = line.find(marker)
        while i != -1:
            if marker != "{{" or i == 0 or line[i - 1] != "$":
                return True
            i = line.find(marker, i + 1)
    return False


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
    # A gate must be able to judge any input without crashing on it:
    # Windows consoles default to cp1252, which cannot print an emoji
    # in a hit line — the report would abort mid-print with exit 1,
    # indistinguishable from "markers found" but without the list.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
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
            if has_marker(line):
                hits.append("%s:%d: %s" % (rel, lineno, line.strip()[:80]))
    if hits:
        print("Leftover template markers found:")
        print("\n".join(hits))
        return 1
    print("marker check OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
