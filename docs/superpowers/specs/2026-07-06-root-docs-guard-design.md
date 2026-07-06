# Design: Guard for unguarded root-singleton docs

- Date: 2026-07-06
- Status: Draft (awaiting user review)
- Scope: test-suite hardening only; no product/template change

## 1. Problem & motivation

This session shipped v2.5.0 with a silent truncation of `README.md`: an
externally-authored update dropped the entire `## Upgrading seeded apps`
section (and a paragraph tail), leaving a dangling cross-reference from
`SETUP.md` and `TEMPLATE-CHANGELOG.md`. The parity net did not catch it.

Root cause: `tests/hooks/test_kit_parity.py` guards `base/` <-> `harness-kit/`
by **byte-equality of mirror pairs**. Docs that exist as a single copy with no
twin — `README.md`, `TEMPLATE-CHANGELOG.md` (seed-root only), and the KIT_ONLY
files `harness-kit/ADOPTION.md`, `harness-kit/START-HERE.md` — have nothing to
compare against, so no test reads their content at all. A singleton can be
truncated to nonsense and the suite stays green.

A key constraint learned while diagnosing: the README truncation ended at
`claude-md-management).` — on sentence-ending punctuation. So a naive
"file must not end mid-sentence" heuristic would **not** have caught it. What
catches it is a **content-presence** check (an expected section vanished) or a
**cross-reference-integrity** check (a citation dangles). This rules out
end-of-file heuristics as the primary mechanism.

## 2. Goals / Non-goals

Goals:
- A truncation or wholesale content-loss in any unguarded root-singleton doc
  fails the test suite (turns red), the same way kit divergence already does.
- Robust, low-maintenance, non-fragile — no false positives on legitimate
  edits; matches the existing `tests/hooks/` unittest style.

Non-goals:
- Not a spellchecker, linter, or prose-quality gate.
- Not a general cross-reference-integrity engine (see Rejected alternatives).
- No change to `base/`, `harness-kit/` content, hooks, or shipped templates —
  tests only, so no `template-version:` stamp advances.

## 3. Scope

The four **unguarded singleton** docs (no byte-twin in the parity manifest):

| Doc | Home | Why unguarded |
|-----|------|---------------|
| `README.md` | seed root | not mirrored to the kit |
| `TEMPLATE-CHANGELOG.md` | seed root | not mirrored to the kit |
| `harness-kit/ADOPTION.md` | kit | KIT_ONLY, no source twin |
| `harness-kit/START-HERE.md` | kit | KIT_ONLY, no source twin |

Out of scope: `SETUP.md` — it IS a mirror pair (root <-> kit), already
byte-guarded by `test_kit_parity`. (The residual "both copies truncated
identically" case is left to that test's owner; it is not a singleton.)

## 4. Design

### 4.1 Location & style

New file `tests/hooks/test_root_docs.py`, `unittest.TestCase`, discovered by
`python -m unittest discover -s tests`. Data-driven: one table drives all four
docs, so adding a doc or anchor is a one-line change.

### 4.2 Required anchors (load-bearing, stable, ASCII-only)

Anchors are chosen ASCII-only (no em-dashes) to avoid UTF-8 match fragility.

```
REQUIRED = {
  "README.md": [
    "## Philosophy", "## Map", "## Instantiation",
    "## When not to use this seed", "## Portability",
    "## Relationship to installed plugins", "## Upgrading seeded apps",
  ],
  "TEMPLATE-CHANGELOG.md": ["# Template Changelog", "Seed version history"],
  "harness-kit/ADOPTION.md": [
    "# Existing App Adoption", "**STOP GUARD**", "**UPDATE MODE**",
  ],
  "harness-kit/START-HERE.md": [
    "# Harness Kit", "Pick the checklist", "SINGLE-USE",
  ],
}
```

### 4.3 Checks (per doc unless noted)

1. **exists & non-trivial** — file present, size >= 500 bytes (a wholesale
   wipe fails).
2. **ends with a newline** — catches the truncation signature this session had
   (README lost its trailing newline). Cheap, high-signal; a legitimate file
   always ends with `\n`.
3. **all anchors present** — every string in the doc's list occurs in the
   file. A dropped section (the exact v2.5.0 failure: `## Upgrading seeded
   apps` vanished) fails here.
4. **changelog entry floor** (`TEMPLATE-CHANGELOG.md` only) — at least 15
   lines starting `## ` (version entries; currently 19). Catches losing a
   chunk of version history.

### 4.4 Why these checks catch the incident

The v2.5.0 truncation had two signatures — a vanished section AND a missing
trailing newline. Check 3 catches the first, check 2 the second; either alone
would have turned the suite red. Defense in depth across cheap checks.

## 5. Validation strategy (TDD red -> green)

The test is the deliverable, so it is validated by proving it discriminates:

1. **Red on a truncated fixture** — in a temp dir, copy a real doc, truncate it
   (drop an anchored section / strip the trailing newline), point the check at
   the copy, assert it FAILS. This proves the guard would have caught v2.5.0.
2. **Green on the real docs** — the suite run asserts the four real docs PASS.

Both live in the same test file: a `_check_doc(text, anchors)` helper returns a
list of problems; the real-doc tests assert it is empty, the fixture tests
assert it is non-empty for each mutation.

## 6. Error handling & maintenance

- A legitimately renamed/removed section makes the test red until the anchor
  list is updated. This friction is intentional — a structural change to a
  load-bearing doc should be a conscious, reviewed edit, not silent.
- Anchors are few and stable (section headers, guard labels). Expected update
  cadence: rare.
- The changelog floor (15) sits well below the current count (19) so normal
  growth never trips it; it only fires on real loss.

## 7. Testing

- Framework: `unittest`, no third-party deps, no network — matches the suite.
- Reads files as UTF-8; anchors ASCII so encoding never affects matching.
- Adds ~6-8 test methods; suite grows from 58 to ~64-66, still fast.

## 8. Rejected alternatives (do not relitigate)

- **End-of-file "not mid-sentence" heuristic.** Would not have caught v2.5.0
  (it ended on a period). Fragile and insufficient — rejected as primary.
- **Approach B: cross-reference-integrity engine.** Scan docs for cited section
  names / file paths and assert they resolve. More general, near-zero
  maintenance, but more code, and it only guards content that happens to be
  referenced — an unreferenced section that vanishes slips through. Higher
  complexity for no extra coverage of THIS bug class. The one concrete cited
  section ("Upgrading seeded apps") is already a README anchor, so approach A
  subsumes the incident.
- **Approach C: hybrid (A + B).** Best theoretical coverage, most code. YAGNI:
  A alone turns the incident red. Revisit only if dangling-reference bugs recur.

## 9. Out of scope / future

- Guarding `SETUP.md`'s "both copies truncated identically" edge (belongs to
  `test_kit_parity`).
- A generic cross-reference checker (approach B) if that bug class recurs.
