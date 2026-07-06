# Root-Singleton Docs Guard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `tests/hooks/test_root_docs.py` so a silent truncation or content-loss in any of the four unguarded singleton docs (`README.md`, `TEMPLATE-CHANGELOG.md`, `harness-kit/ADOPTION.md`, `harness-kit/START-HERE.md`) turns the suite red — closing the gap that let the v2.5.0 README truncation ship.

**Architecture:** One data-driven unittest file. A pure helper `check_doc(text, anchors)` returns a list of problems (empty = healthy); in-memory fixture tests prove it *discriminates* (flags truncated text — the TDD red proof), real-doc tests assert the four live docs pass, plus a changelog entry floor. Spec: `docs/superpowers/specs/2026-07-06-root-docs-guard-design.md`.

**Tech Stack:** Python 3 stdlib `unittest` + `pathlib` only. Discovered by `py -m unittest discover -s tests` from the seed root.

## Global Constraints

- Tests only — do NOT touch `base/`, `harness-kit/` content, hooks, or templates (no `template-version:` stamp advances).
- No third-party dependencies, no network, no temp-file writes (fixtures are in-memory strings).
- Anchor strings must be ASCII-only (no em-dashes) — encoding must never affect matching.
- On this Windows machine use `py`, never `python` (Microsoft Store alias).
- Working branch: `v2.5.2-root-docs-guard` (already checked out; spec committed as `a6d71cc`).
- Suite baseline: 58 tests, 1 environment-gated skip. After this plan: 64 tests, same skip.

---

### Task 1: `check_doc` helper + discrimination fixtures (TDD red → green)

**Files:**
- Create: `tests/hooks/test_root_docs.py`
- Test: `tests/hooks/test_root_docs.py` (the file tests itself via fixtures)

**Interfaces:**
- Produces: `check_doc(text: str, anchors: list[str], min_bytes: int = MIN_BYTES) -> list[str]` — pure function, returns problem descriptions, empty list = healthy. Module constants `ROOT: Path`, `REQUIRED: dict[str, list[str]]`, `MIN_BYTES = 500`, `CHANGELOG_ENTRY_FLOOR = 15`. Task 2 consumes all of these.

- [ ] **Step 1: Write the failing discrimination tests**

Create `tests/hooks/test_root_docs.py` with the module docstring, constants, and ONLY the fixture test class (no `check_doc` implementation yet — that is the red state):

```python
"""Guard the unguarded root-singleton docs against silent truncation.

test_kit_parity.py pins base/ <-> harness-kit/ byte equality, but docs
that exist as a single copy with no twin -- README.md and
TEMPLATE-CHANGELOG.md at the seed root, ADOPTION.md and START-HERE.md
in the kit (KIT_ONLY) -- have nothing to compare against, so no test
reads their content at all. It bit once: v2.5.0 arrived with README.md
truncated (the whole "Upgrading seeded apps" section gone, trailing
newline lost) and the suite stayed green. This test pins load-bearing
anchors, a trailing newline, a size floor, and a changelog entry
floor. A red run after a deliberate doc restructure means: update
REQUIRED here, consciously, in the same commit.
Run from the seed root: python -m unittest discover -s tests
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# doc (relative to the seed root) -> load-bearing anchor strings.
# ASCII-only on purpose: encoding must never affect matching, so
# anchors stop BEFORE any em-dash in the real heading.
REQUIRED = {
    "README.md": [
        "## Philosophy",
        "## Map",
        "## Instantiation",
        "## When not to use this seed",
        "## Portability",
        "## Relationship to installed plugins",
        "## Upgrading seeded apps",
    ],
    "TEMPLATE-CHANGELOG.md": [
        "# Template Changelog",
        "Seed version history",
    ],
    "harness-kit/ADOPTION.md": [
        "# Existing App Adoption",
        "**STOP GUARD**",
        "**UPDATE MODE**",
    ],
    "harness-kit/START-HERE.md": [
        "# Harness Kit",
        "Pick the checklist",
        "SINGLE-USE",
    ],
}

MIN_BYTES = 500          # below this a doc is a wipe, not an edit
CHANGELOG_ENTRY_FLOOR = 15  # "## " entries; currently 19 -- fires on loss


class CheckDocDiscriminationTests(unittest.TestCase):
    """check_doc must flag exactly the v2.5.0 truncation signatures."""

    ANCHORS = ["## Alpha", "## Omega"]
    # 60 body lines keep the healthy fixture safely above MIN_BYTES.
    HEALTHY = (
        "# Doc\n\n## Alpha\n" + ("body line\n" * 60) + "## Omega\ntail\n"
    )

    def test_healthy_text_has_no_problems(self):
        self.assertEqual(check_doc(self.HEALTHY, self.ANCHORS), [])

    def test_dropped_section_is_flagged(self):
        # v2.5.0 signature 1: a whole anchored section vanished.
        truncated = self.HEALTHY.split("## Omega")[0]
        problems = check_doc(truncated, self.ANCHORS)
        self.assertTrue(
            any("## Omega" in p for p in problems),
            "dropped section not flagged: %s" % problems,
        )

    def test_missing_trailing_newline_is_flagged(self):
        # v2.5.0 signature 2: the file ended without a newline.
        problems = check_doc(self.HEALTHY.rstrip("\n"), self.ANCHORS)
        self.assertTrue(
            any("newline" in p for p in problems),
            "lost trailing newline not flagged: %s" % problems,
        )

    def test_wholesale_wipe_is_flagged(self):
        problems = check_doc("# Doc\n## Alpha\n## Omega\n", self.ANCHORS)
        self.assertTrue(
            any("small" in p for p in problems),
            "near-empty doc not flagged: %s" % problems,
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run to verify it fails (red)**

Run: `py -m unittest tests.hooks.test_root_docs -v`
Expected: 4 tests, each ERROR with `NameError: name 'check_doc' is not defined`.

- [ ] **Step 3: Implement `check_doc` (minimal)**

Insert between the `CHANGELOG_ENTRY_FLOOR` constant and the test class:

```python
def check_doc(text, anchors, min_bytes=MIN_BYTES):
    """Return a list of problems with a doc's text (empty = healthy)."""
    problems = []
    if len(text.encode("utf-8")) < min_bytes:
        problems.append("suspiciously small (< %d bytes)" % min_bytes)
    if not text.endswith("\n"):
        problems.append("missing trailing newline (truncation signature)")
    for anchor in anchors:
        if anchor not in text:
            problems.append("missing anchor: %r" % anchor)
    return problems
```

- [ ] **Step 4: Run to verify it passes (green)**

Run: `py -m unittest tests.hooks.test_root_docs -v`
Expected: `Ran 4 tests ... OK`.

- [ ] **Step 5: Commit**

```bash
git add tests/hooks/test_root_docs.py
git commit -m "test: check_doc helper flags doc-truncation signatures (red->green)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 2: Guard the four real docs + changelog entry floor

**Files:**
- Modify: `tests/hooks/test_root_docs.py` (append one class before the `__main__` block)

**Interfaces:**
- Consumes: `check_doc`, `ROOT`, `REQUIRED`, `CHANGELOG_ENTRY_FLOOR` from Task 1 (same module).
- Produces: suite-visible guard tests; nothing downstream consumes them.

- [ ] **Step 1: Append the real-doc guard tests**

Add after `CheckDocDiscriminationTests` (before `if __name__ == "__main__":`):

```python
class RootDocsGuardTests(unittest.TestCase):
    """The four live singleton docs must stay healthy."""

    def test_every_singleton_doc_is_healthy(self):
        for rel, anchors in REQUIRED.items():
            path = ROOT / rel
            self.assertTrue(path.is_file(), "missing doc: %s" % rel)
            problems = check_doc(path.read_text(encoding="utf-8"), anchors)
            self.assertEqual(problems, [], "%s: %s" % (rel, problems))

    def test_changelog_keeps_its_version_history(self):
        text = (ROOT / "TEMPLATE-CHANGELOG.md").read_text(encoding="utf-8")
        entries = [l for l in text.splitlines() if l.startswith("## ")]
        self.assertGreaterEqual(
            len(entries), CHANGELOG_ENTRY_FLOOR,
            "version history implausibly short: %d entries" % len(entries),
        )
```

Note: `read_text` uses universal newlines, so CRLF files arrive as `\n` and `text.endswith("\n")` works unchanged.

- [ ] **Step 2: Run the new file (expect green — the live docs ARE healthy)**

Run: `py -m unittest tests.hooks.test_root_docs -v`
Expected: `Ran 6 tests ... OK`.

- [ ] **Step 3: Manual red-proof against a live doc (no commit of this state)**

Temporarily damage a doc copy to prove end-to-end discrimination, then restore:

```bash
cp README.md README.md.bak
py -c "s=open('README.md',encoding='utf-8').read(); i=s.find('## Upgrading seeded apps'); open('README.md','w',encoding='utf-8',newline='').write(s[:i])"
py -m unittest tests.hooks.test_root_docs 2>&1 | tail -3
mv -f README.md.bak README.md
git status --short   # must show a clean README.md again
```

Expected middle output: `FAILED (failures=1)` mentioning `missing anchor: '## Upgrading seeded apps'`. After restore: `git status` shows no README change.

- [ ] **Step 4: Run the FULL suite**

Run: `py -m unittest discover -s tests`
Expected: `Ran 64 tests ... OK (skipped=1)`.

- [ ] **Step 5: Commit**

```bash
git add tests/hooks/test_root_docs.py
git commit -m "test: guard the four root-singleton docs + changelog entry floor

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 3: Changelog entry (v2.5.2) + final verification

**Files:**
- Modify: `TEMPLATE-CHANGELOG.md` (insert new entry above `## 2026-07.17 — v2.5.1`)

**Interfaces:**
- Consumes: nothing from prior tasks (prose only).
- Produces: the release-notes entry the merge/tag step cites.

- [ ] **Step 1: Insert the v2.5.2 entry**

`TEMPLATE-CHANGELOG.md` is CRLF; use a deterministic splice (same pattern as v2.5.1), NOT a hand-edit. Script (run from seed root with `py`):

```python
import sys
PATH = "TEMPLATE-CHANGELOG.md"
ANCHOR = "## 2026-07.17"  # v2.5.1 header line start

BLOCK = """## 2026-07.18 — v2.5.2

Test-suite hardening only — no template content changes, so no stamp
advances. Closes the guard gap the v2.5.0 round exposed: root-singleton
docs (README.md, TEMPLATE-CHANGELOG.md, and the KIT_ONLY
harness-kit/ADOPTION.md + START-HERE.md) had no byte-twin in the kit
parity manifest, so no test read their content — README.md shipped
truncated (whole "Upgrading seeded apps" section gone) with a green
suite.

- New tests/hooks/test_root_docs.py: per-doc load-bearing anchors
  (ASCII-only), trailing-newline check, 500-byte size floor, and a
  15-entry changelog floor. In-memory fixture tests prove the checker
  flags both v2.5.0 truncation signatures (dropped section, lost
  trailing newline); live-doc tests pin the four real docs. Suite:
  58 -> 64 tests.
- Deliberate friction: restructuring a guarded doc now requires
  updating REQUIRED in the same commit.

Rejected, with reason (don't relitigate): end-of-file "mid-sentence"
heuristic (v2.5.0 truncation ended on a period — it would not have
fired); a general cross-reference-integrity engine (more code, only
guards referenced content; the one cited section is already an anchor).
Design: docs/superpowers/specs/2026-07-06-root-docs-guard-design.md.

"""

with open(PATH, "r", encoding="utf-8", newline="") as f:
    raw = f.read()
nl = "\r\n" if "\r\n" in raw else "\n"
lf = raw.replace("\r\n", "\n")
if lf.count(ANCHOR) != 1:
    sys.exit("expected exactly 1 anchor, found %d" % lf.count(ANCHOR))
lf = lf.replace(ANCHOR, BLOCK + ANCHOR, 1)
out = lf.replace("\n", nl) if nl == "\r\n" else lf
with open(PATH, "w", encoding="utf-8", newline="") as f:
    f.write(out)
print("OK: inserted v2.5.2 entry")
```

- [ ] **Step 2: Verify changelog integrity + full suite**

```bash
file TEMPLATE-CHANGELOG.md      # expect: CRLF line terminators, UTF-8
py -m unittest discover -s tests
```

Expected: `Ran 64 tests ... OK (skipped=1)` — note the new entry raises the `## ` count to 20, comfortably above the floor of 15.

- [ ] **Step 3: Commit**

```bash
git add TEMPLATE-CHANGELOG.md
git commit -m "docs: v2.5.2 changelog - root-singleton docs guard

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## After the plan (outside its scope — user-gated)

Merge/tag/push follow the session's established release flow and are an
outward action: `--no-ff` merge of `v2.5.2-root-docs-guard` into `master`,
annotated tag `v2.5.2`, push to `origin` (verify `origin` is
`reznik57/NewApp` immediately before pushing). Ask the user before executing.
