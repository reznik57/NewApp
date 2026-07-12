# Design: gewürfelter Server-Port 9000–9999 (Seed-Runde v2.7.7)

Datum: 2026-07-12
Status: freigegeben (User), bereit für den Implementierungsplan

## Problem

Der Seed legt heute keinen Server-Port fest. Der einzige Ort, an dem ein Port
überhaupt entsteht, ist `profiles/typescript-next/package-scripts.json`
(`"dev": "next dev"`), und der erbt stillschweigend den Framework-Default 3000.
Dasselbe gilt für jede stack-lose App (`python -m http.server` → 8000, Vite →
5173).

Laufen zwei aus dem Seed gebaute Apps parallel — der Normalfall auf dieser
Maschine —, kollidieren sie auf demselben Default-Port. Der teurere Fehlermodus
ist nicht die Kollision (die ist laut), sondern die Verwechslung: Man ruft
`localhost:3000` auf und redet mit dem Dev-Server eines anderen Projekts, ohne
es zu merken.

## Entscheidung

Jeder lokal laufende Server einer App bindet einen Port aus **9000–9999**, der
**einmal beim Aufsetzen gewürfelt** und dann **fest** eingetragen wird. Hat eine
App mehrere Server (Frontend + Backend), bekommt jeder seinen eigenen Port aus
dem Bereich. `dev` und `start` (Produktions-Preview) einer App teilen sich
denselben Port.

Würfeln: `py -c "import random;print(random.randint(9000,9999))"`

Verworfene Alternativen (Begründung gehört in den Changelog-Eintrag, damit sie
nicht relitigiert werden):

- **Bei jedem Start neu würfeln.** Kollisionsfrei, aber die URL ändert sich
  ständig: Playwright-`baseUrl`, CORS-Origins, OAuth-Redirect-URIs und Bookmarks
  brechen. Der Nutzen (Kollision statt 1:1000 nie) rechtfertigt den Bruch nicht.
- **Port über `.env`/`PORT` statt hart im Script.** npm-Scripts expandieren
  `$PORT` auf Windows nicht, und ob das Framework `.env` für den *Server*-Port
  liest, ist versionsabhängig — beides fällt still auf den Default zurück, also
  genau in den Fehlermodus, den diese Runde schließt. Ein `-p`-Flag im Script ist
  sichtbar, cross-platform und diffbar.
- **Kollisionsprüfung beim Würfeln** (belegte Ports abfragen und neu würfeln).
  Bei 1000 Ports und einer Handvoll Apps ist die Kollisionswahrscheinlichkeit
  vernachlässigbar; die Prüfung wäre plattformabhängiger Code im SETUP-Pfad.

## Änderungen

### 1. `profiles/typescript-next/package-scripts.json`

```json
"dev":   "next dev -p {{DEV_PORT}}",
"start": "next start -p {{DEV_PORT}}"
```

Der Platzhalter ist bewusst dieselbe `{{...}}`-Syntax wie im Rest des Kits — das
ist es, was ihn ans Exit-Gate anschließt (Änderung 4).

### 2. `profiles/typescript-next/README.md`

Der Schritt, der `package-scripts.json` in die `package.json` mergt (heute
Schritt 1), bekommt den Würfelwurf: Port aus 9000–9999 ziehen, beide
`{{DEV_PORT}}` damit ersetzen. Begründung (Kollisionsfreiheit) gehört EINMAL
hierhin, nicht in jede berührte Datei.

### 3. `SETUP.md` (+ Kit-Mirror `harness-kit/SETUP.md`)

Schritt 4 („Fill the six-script contract") bekommt die **stack-agnostische**
Regel: Hat die App einen lokal laufenden Server — egal ob npm, Python oder
`npx serve` —, bekommt er einen einmal gewürfelten Port aus 9000–9999, nie den
Framework-Default. Das ist der Pfad für Stacks ohne Profil, den Änderung 1 nicht
erreicht.

### 4. `base/.claude/scripts/check_markers.py` (+ Kit-Mirror)

```python
SCAN_TOPS = ["CLAUDE.md", "CLAUDE.template.md", ".claude", "docs", ".github", "package.json"]
```

Damit macht ein vergessener `{{DEV_PORT}}` das Exit-Gate (SETUP Schritt 12) ROT,
statt dass die App still auf 3000 läuft. Nicht existierende Pfade werden von
`iter_files` übersprungen — eine stack-lose App zahlt dafür nichts. Der Kommentar
über `SCAN_TOPS` erklärt (wie schon für `CLAUDE.template.md`), WARUM
`package.json` mitgescannt wird.

### 5. `base/CLAUDE.template.md` (+ Kit-Mirror), Commands-Sektion

Eine Zeile, damit die Regel auch nach dem Aufsetzen bindet — wenn ein Agent der
App später einen zweiten Server hinzufügt:

> Lokale Server binden Ports aus 9000–9999 (die dieser App stehen im
> dev-Command) — nie den Framework-Default; das hält parallel laufende Apps
> kollisionsfrei.

Kostet ~1 Zeile am ~190er-CLAUDE.md-Budget (Ceiling: wiki-lint-Skill).

## Bewusst offen (gehört ehrlich in den Changelog)

Das Gate deckt nur den npm-Pfad ab: Ein Python- oder Static-Server hat keine
`package.json`, sein Port steht im dev-Command in CLAUDE.md, und dort ist die
Regel Prosa — nicht mechanisiert. Trigger, das zu schließen: die erste reale App
mit Nicht-npm-Server.

## Tests (die Suite IS das Gate des Seeds)

1. `tests/hooks/test_check_markers.py`: eine Fixture-App mit
   `package.json`, die `{{DEV_PORT}}` enthält → Exit 1 und der Treffer wird
   gelistet; dieselbe App mit gefülltem Port → `marker check OK`.
2. Neue Datei `tests/hooks/test_dev_port.py` als Drift-Guard: `package-scripts.json`
   enthält `-p {{DEV_PORT}}` in `dev` UND `start`; der Bereich `9000` … `9999` wird
   in `SETUP.md` und in `profiles/typescript-next/README.md` genannt;
   `package.json` steht in `SCAN_TOPS` von `check_markers.py`. Bricht, sobald eine
   dieser Stellen von den anderen abdriftet.
3. `test_kit_parity.py` deckt die Mirrors von `check_markers.py`,
   `CLAUDE.template.md` und `SETUP.md` bereits ab — es muss nur mitgespiegelt
   werden.

## Release-Disziplin (aus der Seed-CLAUDE.md)

- Branch `v2.7.7-random-dev-port`, Merge `--no-ff` in master, annotierter Tag
  `v2.7.7` auf dem Merge-Commit, Remote prüfen, dann master + Tag pushen.
- Jede berührte gestempelte Datei bekommt den neuen `template-version:`-Stamp des
  Changelog-Headers dieser Runde. `package-scripts.json` trägt keinen Stamp
  (JSON) — der Changelog-Header ist dort die einzige Spur.
- Changelog-Eintrag v2.7.7 inklusive der drei oben verworfenen Alternativen und
  des bewusst offenen Rests.
- `py -m pytest tests -q` grün vor jedem Commit.
