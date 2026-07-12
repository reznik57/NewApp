# Random Dev Port 9000–9999 — Implementation Plan (Seed-Runde v2.7.7)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Jeder aus dem Seed gebaute Server bindet einen einmal gewürfelten Port aus 9000–9999 statt des Framework-Defaults — mechanisch bewacht vom Exit-Gate.

**Architecture:** Das `typescript-next`-Profil liefert `dev`/`start` mit einem `{{DEV_PORT}}`-Platzhalter; SETUP würfelt ihn beim Aufsetzen einmal und trägt ihn fest ein. `check_markers.py` bekommt `package.json` in `SCAN_TOPS`, wodurch ein vergessener Port das Exit-Gate rot macht statt still auf 3000 zu landen. Für Stacks ohne Profil trägt SETUP Schritt 4 die Regel als Prosa; eine Zeile in `CLAUDE.template.md` bindet auch Agenten, die der App später einen zweiten Server hinzufügen.

**Tech Stack:** Python 3 (stdlib only, Windows-safe), `unittest`, JSON/Markdown-Templates. Ausführung: `py -m pytest tests -q` vom Seed-Root.

Spec: [docs/superpowers/specs/2026-07-12-random-dev-port-design.md](../specs/2026-07-12-random-dev-port-design.md)
Branch: `v2.7.7-random-dev-port` (existiert bereits, Spec ist als `7abec26` committed)

## Global Constraints

- **Port-Bereich: 9000–9999**, exakt diese Grenzen; Würfeln mit `py -c "import random;print(random.randint(9000,9999))"`. Einmal gewürfelt, dann fest verdrahtet — NIE pro Start neu.
- **Runden-ID dieser Änderung: `2026-07.32`, Version `v2.7.7`.** Jede berührte Datei mit `template-version:`-Stamp wird auf `2026-07.32` re-gestempelt (Root-CLAUDE.md → Template discipline). `.json` trägt keinen Stamp.
- **`base/` ist die Quelle, `harness-kit/` der Byte-Mirror.** Nach jeder Änderung an `base/*` oder `SETUP.md` MUSS gespiegelt werden, sonst schlägt `test_kit_parity.py` fehl. Kein Edit nur auf der Kit-Seite.
- **Die Suite muss vor JEDEM Commit grün sein:** `py -m pytest tests -q` vom Seed-Root. Baseline vor dieser Runde: **108 passed, 1 skipped** (der Symlink-Skip auf Windows ist normal).
- **Auf dieser Maschine `py`, nicht `python`** (Microsoft-Store-Alias).
- **Kein `git add -A`.** Nur die in der Task genannten Pfade stagen — `.claude/` im Seed-Root ist ungetrackter Fremd-State und bleibt unangetastet.

---

### Task 1: Changelog-Runde v2.7.7 anlegen

Muss zuerst laufen: [tests/hooks/test_stamps.py:82](../../../tests/hooks/test_stamps.py#L82) verlangt, dass jeder Stamp eine real existierende Changelog-Runde benennt. Ohne den Header `## 2026-07.32` macht der erste Re-Stamp in Task 2 die Suite rot.

**Files:**
- Modify: `TEMPLATE-CHANGELOG.md` (neuer Eintrag direkt vor `## 2026-07.31 — v2.7.6`)

**Interfaces:**
- Consumes: nichts.
- Produces: die Runden-ID `2026-07.32`, die alle folgenden Tasks als Stamp verwenden.

- [ ] **Step 1: Eintrag einfügen**

Direkt über der Zeile `## 2026-07.31 — v2.7.6` einfügen:

```markdown
## 2026-07.32 — v2.7.7

Servers built from this seed inherited the framework's default port — Next
3000, Vite 5173, `http.server` 8000. Two apps in parallel is the normal case on
a dev box, and the cheap failure there is the loud one (port in use). The
expensive one is silent: you open `localhost:3000` and talk to yesterday's
server without noticing.

Shipped:

- **Every server binds a port ROLLED ONCE from 9000–9999.** The TS/Next profile
  now ships `"dev": "next dev -p {{DEV_PORT}}"` and — new — its own
  `"start": "next start -p {{DEV_PORT}}"` (the scaffold's portless `start` used
  to survive); SETUP rolls the port and fills both slots. Rolled once and wired
  hard, so `baseUrl`, CORS origins and OAuth callbacks stay stable. An app with
  two servers takes two ports from the range.
- **The exit gate guards it.** `check_markers.py` scans `package.json` — an
  unfilled `{{DEV_PORT}}` now fails SETUP step 12 instead of quietly falling
  back to 3000. Non-existent paths are skipped, so a stack-less app pays
  nothing for it.
- **The stack-less path is covered in prose.** SETUP step 4 states the rule for
  ANY locally running server (`uvicorn --port`, `npx serve -l`), not just npm
  ones.
- **The rule outlives setup.** `CLAUDE.template.md` → Commands names the range,
  so an agent adding a second server to the app months later does not reach for
  8000.

Rejected, with reasons — do not relitigate:

- **Re-rolling the port on every start.** Collision-free, but a moving URL
  breaks Playwright `baseUrl`, CORS origins, OAuth redirect URIs and bookmarks.
  The 1-in-1000 collision it buys is not worth a permanently unstable address.
- **`PORT` via `.env` instead of a hard `-p` flag.** npm scripts do not expand
  `$PORT` on Windows, and whether a framework reads `.env` for the SERVER port
  is version-dependent — both fall back to the default SILENTLY, which is
  exactly the failure this round closes. A `-p` flag is visible, diffable and
  cross-platform.
- **Collision-checking the roll** (probe bound ports, re-roll on a hit): with
  1000 ports and a handful of apps the probability is negligible; the check
  would put platform-dependent socket code into the SETUP path.

Deliberately open, with trigger:

- The gate covers the npm path only. A Python or static server has no
  `package.json`; its port lives in the dev command in CLAUDE.md, where the rule
  is prose, not mechanism. **Trigger:** the first real app with a non-npm
  server — then decide whether the gate learns to read the dev command.
```

- [ ] **Step 2: Suite laufen lassen (muss unverändert grün sein)**

Run: `py -m pytest tests -q`
Expected: `108 passed, 1 skipped` — der Changelog-Eintrag allein ändert keine Testzahl, aber `test_root_docs.py` bewacht TEMPLATE-CHANGELOG.md gegen Trunkierung, und `test_stamps.py` parst jetzt die neue Runde.

- [ ] **Step 3: Commit**

```bash
git add TEMPLATE-CHANGELOG.md
git commit -m "docs(changelog): open round v2.7.7 (2026-07.32) — rolled server port 9000-9999"
```

---

### Task 2: Das Gate — `check_markers.py` scannt `package.json`

**Files:**
- Modify: `tests/hooks/test_check_markers.py` (zwei neue Tests am Ende der `CheckMarkersTests`-Klasse, vor `if __name__`)
- Modify: `base/.claude/scripts/check_markers.py:10` (Stamp) und `:22` (SCAN_TOPS + Begründungskommentar)
- Modify: `harness-kit/.claude/scripts/check_markers.py` (Byte-Mirror — kopiert, nicht editiert)

**Interfaces:**
- Consumes: Runden-ID `2026-07.32` aus Task 1.
- Produces: die Garantie, auf die Task 3's Platzhalter sich verlässt — `{{DEV_PORT}}` in `package.json` ⇒ Exit-Gate rot.

- [ ] **Step 1: Die failing tests schreiben**

In `tests/hooks/test_check_markers.py`, direkt vor `if __name__ == "__main__":` (nach `test_emoji_hit_survives_cp1252_stdout`) einfügen — Einrückung: Methoden der `CheckMarkersTests`-Klasse:

```python
    def test_unfilled_dev_port_in_package_json_fails(self):
        # The app's server port is a template slot like any other: left
        # unfilled, the app falls back to the framework default (3000) and
        # collides — silently — with every other app on the box. package.json
        # is in SCAN_TOPS so that cannot reach a green gate.
        self.write("CLAUDE.md", "clean\n")
        self.write(
            "package.json",
            '{"scripts": {"dev": "next dev -p {{DEV_PORT}}"}}\n',
        )
        result = run_check(self.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("package.json", result.stdout)

    def test_filled_package_json_passes(self):
        # The rolled port is an ordinary number — nothing left to fill.
        self.write("CLAUDE.md", "clean\n")
        self.write(
            "package.json",
            '{"scripts": {"dev": "next dev -p 9427"}}\n',
        )
        result = run_check(self.root)
        self.assertEqual(result.returncode, 0)
        self.assertIn("marker check OK", result.stdout)
```

- [ ] **Step 2: Tests laufen lassen — sie MÜSSEN fehlschlagen**

Run: `py -m pytest tests/hooks/test_check_markers.py -q`
Expected: FAIL — `test_unfilled_dev_port_in_package_json_fails` scheitert an `1 != 0`: `package.json` wird heute nicht gescannt, das Gate meldet fälschlich `marker check OK`. (`test_filled_package_json_passes` ist schon grün — er ist der Gegenbeweis, dass die Erweiterung nichts kaputtmacht, nicht der Treiber.)

- [ ] **Step 3: `SCAN_TOPS` erweitern**

In `base/.claude/scripts/check_markers.py` den Block ab Zeile 15 ersetzen. Alt:

```python
# CLAUDE.template.md is scanned even though a correct run has RENAMED it
# away (SETUP step 7): the absence of CLAUDE.md used to be the only signal
# that the rename was skipped, and a scaffolder that generated its own
# CLAUDE.md — which SETUP step 1 explicitly anticipates — satisfies that
# check while the kit's manual sits beside it, unrenamed. Measured: 21 live
# placeholders and a green gate. A path that does not exist is skipped, so
# this costs a correct run nothing.
SCAN_TOPS = ["CLAUDE.md", "CLAUDE.template.md", ".claude", "docs", ".github"]
```

Neu:

```python
# CLAUDE.template.md is scanned even though a correct run has RENAMED it
# away (SETUP step 7): the absence of CLAUDE.md used to be the only signal
# that the rename was skipped, and a scaffolder that generated its own
# CLAUDE.md — which SETUP step 1 explicitly anticipates — satisfies that
# check while the kit's manual sits beside it, unrenamed. Measured: 21 live
# placeholders and a green gate. A path that does not exist is skipped, so
# this costs a correct run nothing.
# package.json is scanned for the app's SERVER PORT: the TS/Next profile
# ships "next dev -p {{DEV_PORT}}", rolled once from 9000-9999 at setup
# (SETUP step 4). An unfilled slot there would leave the app on the
# framework default 3000 — where a second app quietly answers for it.
SCAN_TOPS = [
    "CLAUDE.md",
    "CLAUDE.template.md",
    ".claude",
    "docs",
    ".github",
    "package.json",
]
```

Und den Stamp in Zeile 10 auf die neue Runde setzen: `# template-version: 2026-07.32`

- [ ] **Step 4: Tests laufen lassen — sie müssen jetzt bestehen**

Run: `py -m pytest tests/hooks/test_check_markers.py -q`
Expected: PASS (alle Tests der Datei, inkl. der zwei neuen).

- [ ] **Step 5: In den Kit spiegeln**

```bash
cp base/.claude/scripts/check_markers.py harness-kit/.claude/scripts/check_markers.py
```

- [ ] **Step 6: Volle Suite**

Run: `py -m pytest tests -q`
Expected: `110 passed, 1 skipped` — `test_kit_parity.py` ist grün, weil Step 5 gespiegelt hat; ohne Step 5 stünde hier ein Byte-Diff.

- [ ] **Step 7: Commit**

```bash
git add base/.claude/scripts/check_markers.py harness-kit/.claude/scripts/check_markers.py tests/hooks/test_check_markers.py
git commit -m "fix(gate): scan package.json so an unfilled {{DEV_PORT}} cannot pass the exit gate"
```

---

### Task 3: Das Profil — `{{DEV_PORT}}`-Platzhalter und der Würfelwurf

**Files:**
- Create: `tests/hooks/test_dev_port.py`
- Modify: `profiles/typescript-next/package-scripts.json` (`dev` + neues `start`)
- Modify: `profiles/typescript-next/README.md:1` (Stamp) und Schritt 1

**Interfaces:**
- Consumes: das Gate aus Task 2 (`package.json` in `SCAN_TOPS`) — der Drift-Guard prüft, dass es da ist.
- Produces: `tests/hooks/test_dev_port.py` mit den Klassen `DevPortSlotTests` und `PortRangeTests`; Task 4 erweitert `PortRangeTests` um zwei Methoden.

- [ ] **Step 1: Den Drift-Guard schreiben (failing)**

Create `tests/hooks/test_dev_port.py`:

```python
"""The app's server port is rolled once from 9000-9999 -- and the seed says so
in the places that can enforce it.

Framework defaults (Next 3000, Vite 5173, http.server 8000) collide as soon as
two apps run in parallel; the expensive failure is the silent one -- talking to
yesterday's server. v2.7.7 gives every seeded server a port rolled once from
9000-9999 and wires the rule to the exit gate via a {{DEV_PORT}} slot.

One fact, several homes that must agree: the profile SHIPS the slot, the profile
README and SETUP NAME the range, and check_markers.py SCANS package.json so an
unfilled slot cannot reach a green gate. Drop any one of them and the rule
degrades to prose without anyone noticing -- this test is what notices.
Run from the seed root: python -m unittest discover -s tests
"""
# template-version: 2026-07.32
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROFILE = ROOT / "profiles" / "typescript-next"
SCRIPTS = PROFILE / "package-scripts.json"
PROFILE_README = PROFILE / "README.md"
GATE = ROOT / "base" / ".claude" / "scripts" / "check_markers.py"
SLOT = "{{DEV_PORT}}"
BOUNDS = ("9000", "9999")


class DevPortSlotTests(unittest.TestCase):
    def test_dev_and_start_bind_the_rolled_port(self):
        scripts = json.loads(SCRIPTS.read_text(encoding="utf-8"))["scripts"]
        for name in ("dev", "start"):
            self.assertIn(
                "-p %s" % SLOT, scripts.get(name, ""),
                "profile script %r must bind the rolled port, not the"
                " framework default" % name,
            )

    def test_the_gate_scans_package_json(self):
        # Without this line the slot is decoration: an unfilled {{DEV_PORT}}
        # would survive the exit gate and the app would serve on 3000.
        self.assertIn('"package.json"', GATE.read_text(encoding="utf-8"))


class PortRangeTests(unittest.TestCase):
    def assert_names_the_range(self, path):
        text = path.read_text(encoding="utf-8")
        for bound in BOUNDS:
            self.assertIn(
                bound, text,
                "%s no longer names the port range -- the roll instruction and"
                " the slot must not drift apart" % path.name,
            )

    def test_profile_readme_names_the_range(self):
        self.assert_names_the_range(PROFILE_README)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Test laufen lassen — er MUSS fehlschlagen**

Run: `py -m pytest tests/hooks/test_dev_port.py -q`
Expected: 2 FAIL — `test_dev_and_start_bind_the_rolled_port` (das Profil hat kein `start` und `dev` ist portlos) und `test_profile_readme_names_the_range` (der README nennt 9000/9999 nirgends). `test_the_gate_scans_package_json` ist grün — Task 2 hat es geliefert.

- [ ] **Step 3: `package-scripts.json` füllen**

Ersetze `profiles/typescript-next/package-scripts.json` vollständig:

```json
{
  "scripts": {
    "check": "prettier --check . && eslint . --max-warnings 0 && tsc --noEmit && vitest run",
    "test": "vitest run",
    "test:one": "vitest run -t",
    "fix": "prettier --write . && eslint . --fix",
    "dev": "next dev -p {{DEV_PORT}}",
    "build": "next build",
    "start": "next start -p {{DEV_PORT}}"
  }
}
```

(`start` ist neu im Profil. Bisher überlebte das portlose `start` von `create-next-app`; da `next start` ebenfalls ein Server ist, muss es denselben Port binden — sonst wechselt der Preview die Adresse.)

- [ ] **Step 4: Profil-README — Schritt 1 um den Würfelwurf erweitern**

In `profiles/typescript-next/README.md` Schritt 1 ersetzen. Alt:

```markdown
1. Merge `package-scripts.json` → the `"scripts"` block of the app's
   `package.json` (created by `create-next-app` or `npm init`). On a name
   collision the profile's entry WINS. Scaffold leftovers: delete `lint`
   (it lives in `check`/`fix` — a second, laxer lint entry drifts);
   keeping `start` is fine (`next start` serves deployments).
```

Neu:

```markdown
1. Merge `package-scripts.json` → the `"scripts"` block of the app's
   `package.json` (created by `create-next-app` or `npm init`). On a name
   collision the profile's entry WINS — including `start`, which the profile
   now ships itself so the preview server binds the app's port too. Scaffold
   leftovers: delete `lint` (it lives in `check`/`fix` — a second, laxer lint
   entry drifts).
   Then ROLL THE APP'S PORT and fill BOTH `{{DEV_PORT}}` slots with it:
   `py -c "import random;print(random.randint(9000,9999))"` → e.g. 9427, so
   `"dev": "next dev -p 9427"` and `"start": "next start -p 9427"`. Rolling
   from 9000–9999 keeps parallel apps off each other's ports and off the
   framework default 3000, where the failure is silent — you reach a server,
   just yesterday's. Rolled ONCE and wired hard, never per start: a moving port
   breaks Playwright `baseUrl`s, CORS origins and OAuth callbacks. Leave a slot
   unfilled and the exit gate (SETUP step 12) turns red — `check_markers.py`
   scans `package.json`.
```

Und den Stamp in Zeile 1 auf `<!-- template-version: 2026-07.32 -->` setzen.

- [ ] **Step 5: Test laufen lassen — er muss jetzt bestehen**

Run: `py -m pytest tests/hooks/test_dev_port.py -q`
Expected: `3 passed`.

- [ ] **Step 6: Volle Suite**

Run: `py -m pytest tests -q`
Expected: `113 passed, 1 skipped`. Bricht hier `test_stamps.py`, dann benennt der Stamp keine reale Runde — Task 1 prüfen.

- [ ] **Step 7: Commit**

```bash
git add tests/hooks/test_dev_port.py profiles/typescript-next/package-scripts.json profiles/typescript-next/README.md
git commit -m "feat(profile): dev and start bind a port rolled once from 9000-9999"
```

---

### Task 4: SETUP + CLAUDE.template — die Regel für alles außerhalb des Profils

**Files:**
- Modify: `tests/hooks/test_dev_port.py` (zwei Methoden in `PortRangeTests`)
- Modify: `SETUP.md` (Schritt 4)
- Modify: `base/CLAUDE.template.md:1` (Stamp) und `:118-121` (Commands-Sektion)
- Modify: `harness-kit/SETUP.md`, `harness-kit/CLAUDE.template.md` (Byte-Mirrors — kopiert, nicht editiert)

**Interfaces:**
- Consumes: `PortRangeTests.assert_names_the_range(path)` aus Task 3.
- Produces: nichts, worauf spätere Tasks bauen — dies ist die letzte inhaltliche Task.

- [ ] **Step 1: Die failing tests schreiben**

In `tests/hooks/test_dev_port.py` die Konstanten ergänzen (nach der `GATE`-Zeile):

```python
SETUP = ROOT / "SETUP.md"
CLAUDE_TEMPLATE = ROOT / "base" / "CLAUDE.template.md"
```

und in `PortRangeTests` nach `test_profile_readme_names_the_range` einfügen:

```python
    def test_setup_names_the_range(self):
        # The stack-less path: an app with no profile (python -m http.server,
        # npx serve) reaches the rule only here.
        self.assert_names_the_range(SETUP)

    def test_claude_template_names_the_range(self):
        # The rule has to outlive setup: an agent adding a SECOND server to
        # the app months later reads CLAUDE.md, not SETUP.md.
        self.assert_names_the_range(CLAUDE_TEMPLATE)
```

- [ ] **Step 2: Tests laufen lassen — sie MÜSSEN fehlschlagen**

Run: `py -m pytest tests/hooks/test_dev_port.py -q`
Expected: 2 FAIL — weder `SETUP.md` noch `base/CLAUDE.template.md` nennen heute 9000/9999.

- [ ] **Step 3: SETUP.md Schritt 4 erweitern**

In `SETUP.md` Schritt 4 ersetzen. Alt:

```markdown
- [ ] 4. **Fill the six-script contract** in `package.json`: `check`,
      `test`, `test:one`, `fix`, `dev`, `build` (the profile's
      `package-scripts.json` provides them). Non-npm stack: act on the
      ADAPT note in CLAUDE.md → Commands now — including its
      `CHECK_COMMAND` update, which step 6's self-test verifies.
```

Neu (der Rest des Schritts — „**Every harness edit belongs in this step**…" bis zum Ende — bleibt unverändert stehen):

```markdown
- [ ] 4. **Fill the six-script contract** in `package.json`: `check`,
      `test`, `test:one`, `fix`, `dev`, `build` (the profile's
      `package-scripts.json` provides them). **Every server this app runs
      locally binds a port ROLLED ONCE from 9000–9999** —
      `py -c "import random;print(random.randint(9000,9999))"` — wired hard
      into the command that starts it (`next dev -p 9427`,
      `uvicorn app:api --port 9427`, `npx serve -l 9427`), never the framework
      default: 3000/5173/8000 collide the moment a second app runs, and the
      expensive failure is the silent one — you reach a server, just
      yesterday's. Rolled ONCE, not per start: a moving port breaks Playwright
      `baseUrl`s, CORS origins and OAuth callbacks. Two servers (frontend +
      backend) take two ports from the range. On the profile path the roll
      fills `{{DEV_PORT}}` in `dev` and `start`, and step 12's gate catches a
      forgotten one; a non-npm server has no such slot — there the rule is on
      you. Non-npm stack: act on the ADAPT note in CLAUDE.md → Commands now —
      including its `CHECK_COMMAND` update, which step 6's self-test verifies.
```

`test_root_docs.py` verlangt, dass die Zeichenfolge `4. **Fill the six-script contract**` erhalten bleibt — sie steht unverändert am Anfang.

- [ ] **Step 4: CLAUDE.template.md Commands-Sektion erweitern**

In `base/CLAUDE.template.md` die Zeilen 120–121 ersetzen. Alt:

```markdown
The six-script contract lives in `package.json` (single source of truth):
`check` (THE gate), `test`, `test:one`, `fix`, `dev`, `build`.
```

Neu:

```markdown
The six-script contract lives in `package.json` (single source of truth):
`check` (THE gate), `test`, `test:one`, `fix`, `dev`, `build`.
Local servers bind a port from 9000–9999 (this app's live in the `dev`/`start`
commands) — never a framework default; that is what keeps apps running in
parallel off each other's ports. A NEW server gets its own port from the range.
```

Und den Stamp in Zeile 1 auf `<!-- template-version: 2026-07.32 -->` setzen.

- [ ] **Step 5: In den Kit spiegeln**

```bash
cp SETUP.md harness-kit/SETUP.md
cp base/CLAUDE.template.md harness-kit/CLAUDE.template.md
```

- [ ] **Step 6: Das CLAUDE.md-Budget nachmessen**

Run: `py -c "print(sum(1 for _ in open('base/CLAUDE.template.md', encoding='utf-8')))"`
Expected: eine Zahl deutlich unter dem ~190er-Ceiling (die Sektion wuchs um 3 Zeilen). Liegt sie darüber, NICHT die neue Regel opfern, sondern nach der wiki-lint-Doktrin messen, welcher Block überläuft, und den nach `docs/wiki/` migrieren.

- [ ] **Step 7: Volle Suite**

Run: `py -m pytest tests -q`
Expected: `115 passed, 1 skipped`. `test_kit_parity.py` ist grün, weil Step 5 gespiegelt hat.

- [ ] **Step 8: Commit**

```bash
git add SETUP.md base/CLAUDE.template.md harness-kit/SETUP.md harness-kit/CLAUDE.template.md tests/hooks/test_dev_port.py
git commit -m "feat(setup): state the 9000-9999 port rule for every server, profile or not"
```

---

### Task 5: Release — Merge, Tag, Push

**Files:** keine Änderungen; reine Release-Disziplin (Root-CLAUDE.md → Release discipline).

- [ ] **Step 1: Suite ein letztes Mal, vom sauberen Baum**

Run: `git status --short && py -m pytest tests -q`
Expected: nur `?? .claude/` (Fremd-State, bleibt ungetrackt); `115 passed, 1 skipped`.

- [ ] **Step 2: Merge nach master**

```bash
git checkout master
git merge --no-ff v2.7.7-random-dev-port -m "Merge v2.7.7-random-dev-port: every seeded server binds a port rolled once from 9000-9999, guarded by the exit gate"
```

- [ ] **Step 3: Annotierten Tag auf den Merge-Commit setzen**

```bash
git tag -a v2.7.7 -m "v2.7.7 — rolled server port 9000-9999, mechanized by check_markers scanning package.json"
```

- [ ] **Step 4: Remote-Identität prüfen — VOR dem Push**

Run: `git remote -v`
Expected: das TEMPLATE-Remote, nie ein App-Remote (Root-CLAUDE.md → Repo identity). Ist der pre-push-Guard in diesem Klon aktiv (`git config core.hooksPath` = `.githooks`), erledigt er das zusätzlich; ist er es nicht, ist diese Sichtprüfung die einzige Absicherung.

- [ ] **Step 5: master und Tag zusammen pushen**

```bash
git push origin master v2.7.7
```

---

## Self-Review

**Spec-Abdeckung:** Änderung 1 (package-scripts) → Task 3; Änderung 2 (Profil-README) → Task 3; Änderung 3 (SETUP + Mirror) → Task 4; Änderung 4 (check_markers + Mirror) → Task 2; Änderung 5 (CLAUDE.template + Mirror) → Task 4; Tests 1–3 der Spec → Tasks 2, 3, 4 (Kit-Parität ist durch die `cp`-Schritte abgedeckt); Release-Disziplin → Task 5; verworfene Alternativen + bewusst offener Rest → Task 1 (Changelog). Keine Lücke.

**Platzhalter-Scan:** Jeder Code-Schritt zeigt vollständigen Inhalt; `{{DEV_PORT}}` ist Nutzlast, kein Plan-TBD. Keine „TODO"/„TBD"/„analog zu Task N".

**Typ-/Namenskonsistenz:** `SLOT = "{{DEV_PORT}}"`, `BOUNDS`, `assert_names_the_range(path)` und die Klassennamen `DevPortSlotTests` / `PortRangeTests` sind in Task 3 definiert und werden in Task 4 exakt so weiterverwendet. Die Runden-ID `2026-07.32` ist in Tasks 1–4 identisch.
