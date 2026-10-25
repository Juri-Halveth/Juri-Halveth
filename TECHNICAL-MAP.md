[Deutsch](TECHNICAL-MAP.md) · [English](TECHNICAL-MAP.en.md) · [Русский](TECHNICAL-MAP.ru.md)

# Technische Schnittstellen. Konkrete Arbeitsproben.

**Ich entwickle und untersuche die Schnittstellen zwischen Systemen.**

Wähle ein technisches Gebiet und öffne direkt die zugehörige Funktion, Gegenprobe oder Builddefinition. Die Beispiele verbinden 6 ausgewählte öffentliche Repositories durch nachvollziehbare Arbeitsschritte.

Quellprüfung: 2026-10-20 · 6 / 12

- [Oberflächen & lokale Schnittstellen](#interfaces)
- [Entscheidungen & Zustände](#state)
- [Security-Logik & Gegenproben](#security)
- [Quellen & Datenintegrität](#data)
- [Grafik & numerische Modelle](#models)
- [Builds & Veröffentlichung](#delivery)

<a id="cross-references"></a>
## Wiederkehrende Arbeitsweisen

**Eingaben vor ihrer Übernahme prüfen**

[Eine Kennung von einer Berechtigung unterscheiden](#reference-authority) · [Dieselben Quellenpakete in Node und Browser lesen](#node-browser-packet)

**Offene Ergebnisse sichtbar erhalten**

[Entscheidungen mit offenen Ergebnissen modellieren](#decision-model) · [Regelkonflikte berechnen und Ergebnisse wiederholen](#python-replay) · [Sicherheitsberichte auf offene Belegkanten prüfen](#security-report-model)

**Quellen, Build und Ergebnis nachvollziehen**

[Quellstand und veröffentlichte Dateien getrennt binden](#artifact-provenance) · [Generierten Stand vor dem Deploy prüfen](#pages-delivery)

**Zeit und Beobachtungsgrenzen im Modell führen**

[Animation an Sichtbarkeit und Nutzerwunsch binden](#browser-motion) · [Bildänderungen innerhalb eines Prüfbereichs messen](#pixel-comparison) · [Ein Grafikmodell mit Grenzfall prüfen](#optics-counterexample)

<a id="interfaces"></a>
## Oberflächen & lokale Schnittstellen

<a id="browser-motion"></a>
### Animation an Sichtbarkeit und Nutzerwunsch binden

**Darstellung, Animationszeit und Browserereignisse**

JavaScript · Canvas 2D · Browser lifecycle

Die Portfolio-Grafik pausiert außerhalb des sichtbaren Bereichs und berücksichtigt reduzierte Bewegung. Tests simulieren Sichtbarkeitswechsel und lange Unterbrechungen.

**Prüfumfang:** Browseradapter mit simuliertem Canvas und Ereignissen; eigene Bewegungsberechnung separat prüfbar.

**Quellcode und Gegenprobe**

- Implementierung — [Juri-Halveth/Juri-Halveth.github.io/landing-motion.js:1](https://github.com/Juri-Halveth/Juri-Halveth.github.io/blob/945eef06bf0a03822e7db589d31ef3dbb902cc69/landing-motion.js#L1-L47) · `945eef0`
- Gegenprobe — [Juri-Halveth/Juri-Halveth.github.io/tests/landing-motion.test.cjs:23](https://github.com/Juri-Halveth/Juri-Halveth.github.io/blob/945eef06bf0a03822e7db589d31ef3dbb902cc69/tests/landing-motion.test.cjs#L23-L35) · `945eef0`

<a id="desktop-backup"></a>
### Vom Desktopdialog zur lokalen Sicherung

**Weboberfläche, Python-API und Dateisystem**

Python · pywebview · Windows

Tresor exportiert die verschlüsselte Tresordatei an einen gewählten Ort. Die Regression prüft einen abgewiesenen Dateifilter, den Ersatzdialog und Abbruch durch den Nutzer.

**Prüfumfang:** Native Dialoge sind im Test ersetzt. Die Arbeitsprobe zeigt die UI/Python-Grenze; die Kryptografie besitzt einen eigenen Prüfbedarf.

**Quellcode und Gegenprobe**

- Implementierung — [Juri-Halveth/halveth-tresor/src/tresor/app.py:223](https://github.com/Juri-Halveth/halveth-tresor/blob/66da64abfc58cd8cce05f935197aa51e31e232f2/src/tresor/app.py#L223-L256) · `66da64a`
- Gegenprobe — [Juri-Halveth/halveth-tresor/tests/test_app_backup.py:61](https://github.com/Juri-Halveth/halveth-tresor/blob/66da64abfc58cd8cce05f935197aa51e31e232f2/tests/test_app_backup.py#L61-L80) · `66da64a`

<a id="state"></a>
## Entscheidungen & Zustände

<a id="decision-model"></a>
### Entscheidungen mit offenen Ergebnissen modellieren

**Eingegebene Optionen, Gewichtung und Ergebnisansicht**

JavaScript · Web Crypto · Deterministic ranking

Das Entscheidungsmodell vergleicht vollständig eingegebene Optionen. Fehlende Werte bleiben offen; gleiche Stimmen erzeugen einen Gleichstand. Tests prüfen beide Fälle.

**Prüfumfang:** Ein gemeinsamer lokaler Algorithmus mit deklarierten Profilgewichten.

**Quellcode und Gegenprobe**

- Implementierung — [Juri-Halveth/fortuna/docs/collective.mjs:52](https://github.com/Juri-Halveth/fortuna/blob/438f6ba7557924aa011cc0d4f26d4acb4bc4d77d/docs/collective.mjs#L52-L71) · `438f6ba`
- Gegenprobe — [Juri-Halveth/fortuna/docs/collective.test.mjs:29](https://github.com/Juri-Halveth/fortuna/blob/438f6ba7557924aa011cc0d4f26d4acb4bc4d77d/docs/collective.test.mjs#L29-L39) · `438f6ba`

<a id="python-replay"></a>
### Regelkonflikte berechnen und Ergebnisse wiederholen

**Deklarierte Regeln, Auswertung und Replay-Receipt**

Python · JSON · Three-valued logic

Das Regelmodell erhält unbekannte Werte und widersprüchliche Regeln. Ein Receipt bindet Eingabe, Modellquelle und Ergebnis; Replay erkennt veränderte Ergebnisse.

**Prüfumfang:** Deterministisches Offline-Modell für deklarierte Eingaben und Prioritäten.

**Quellcode und Gegenprobe**

- Implementierung — [Juri-Halveth/halveth-forschungslabor/branches/normenwerk-rule-universe/normenkern.py:125](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/normenwerk-rule-universe/normenkern.py#L125-L168) · `c6008ab`
- Gegenprobe — [Juri-Halveth/halveth-forschungslabor/branches/normenwerk-rule-universe/test_normenkern.py:57](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/normenwerk-rule-universe/test_normenkern.py#L57-L62) · `c6008ab`

<a id="security"></a>
## Security-Logik & Gegenproben

<a id="reference-authority"></a>
### Eine Kennung von einer Berechtigung unterscheiden

**Requestdaten und separat gebundener Authentisierungskontext**

JavaScript · Canonical JSON · Authorization model

Der lokale Referenzprüfer vergleicht Principal, Register-Digest und aktuellen Referenzzustand. Ein im Request eingetragener Principal genügt nicht. Fehlerantworten geben denselben begrenzten Status zurück.

**Prüfumfang:** Synthetischer Sicherheitsvertrag. Der vertrauenswürdige Authentisierungsadapter ist eine externe Voraussetzung.

**Quellcode und Gegenprobe**

- Implementierung — [Juri-Halveth/halveth-forschungslabor/branches/document-issue-reference-verifier/src/reference-verifier.mjs:179](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/document-issue-reference-verifier/src/reference-verifier.mjs#L179-L206) · `c6008ab`
- Gegenprobe — [Juri-Halveth/halveth-forschungslabor/branches/document-issue-reference-verifier/test/reference-verifier.test.mjs:83](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/document-issue-reference-verifier/test/reference-verifier.test.mjs#L83-L89) · `c6008ab`

<a id="security-report-model"></a>
### Sicherheitsberichte auf offene Belegkanten prüfen

**Deklarierte Beobachtung, Auswirkung und Berichtsstruktur**

JavaScript · Closed input schema · Negative controls

Das Lehrmodell erkennt Platzhalter, fehlende Akteur-/Produktbindungen und eine vorgeschlagene Schwere oberhalb des deklarierten Belegstands. Gegenproben prüfen diese Übergänge.

**Prüfumfang:** Strukturprüfung synthetischer Berichte; reale Befunde bleiben beim jeweiligen Fall und dessen Belegen.

**Quellcode und Gegenprobe**

- Implementierung — [Juri-Halveth/halveth-forschungslabor/branches/security-impact-learning/submission-review.mjs:1](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/security-impact-learning/submission-review.mjs#L1-L17) · `c6008ab`
- Gegenprobe — [Juri-Halveth/halveth-forschungslabor/branches/security-impact-learning/submission-review.test.mjs:1](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/security-impact-learning/submission-review.test.mjs#L1-L11) · `c6008ab`

<a id="data"></a>
## Quellen & Datenintegrität

<a id="node-browser-packet"></a>
### Dieselben Quellenpakete in Node und Browser lesen

**Quellbytes, Transportpaket und zwei Datenverbraucher**

Node.js · Browser Web Crypto · SHA-256 · Base64

Ein Paket bindet Quellrevision, Bytezahl und SHA-256. Der Vergleichstest prüft gleiche Auswertung durch Node und Browser sowie Ablehnung veränderter Grenzen und Bytes.

**Prüfumfang:** Datenintegrität und gebundene Interpretation im implementierten Paketformat.

**Quellcode und Gegenprobe**

- Implementierung — [Juri-Halveth/halveth-forschungslabor/scripts/packet.mjs:1](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/scripts/packet.mjs#L1-L25) · `c6008ab`
- Gegenprobe — [Juri-Halveth/halveth-forschungslabor/scripts/source-packet-browser.test.mjs:1](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/scripts/source-packet-browser.test.mjs#L1-L20) · `c6008ab`

<a id="artifact-provenance"></a>
### Quellstand und veröffentlichte Dateien getrennt binden

**Git-Arbeitsbaum, Website-Build und Artefaktbytes**

Node.js · Git · SHA-256 · Filesystem

Die Buildprüfung bildet einen Digest über sortierte Dateipfade und exakte Buildbytes. Der Test erkennt veränderte und zusätzlich eingeschleuste Ausgabedateien sowie einen schmutzigen Quellbaum.

**Prüfumfang:** Integritätsprüfung des gebundenen Website-Artefakts und seines Quellstands.

**Quellcode und Gegenprobe**

- Implementierung — [Juri-Halveth/halveth-scarlet/tools/artifact_tree.mjs:1](https://github.com/Juri-Halveth/halveth-scarlet/blob/b768ca093d9bd68b1453a8ccc5b6d02ecaa1eb07/tools/artifact_tree.mjs#L1-L33) · `b768ca0`
- Gegenprobe — [Juri-Halveth/halveth-scarlet/tests/source-state.test.mjs:11](https://github.com/Juri-Halveth/halveth-scarlet/blob/b768ca093d9bd68b1453a8ccc5b6d02ecaa1eb07/tests/source-state.test.mjs#L11-L55) · `b768ca0`

<a id="models"></a>
## Grafik & numerische Modelle

<a id="optics-counterexample"></a>
### Ein Grafikmodell mit Grenzfall prüfen

**Geometrisches Modell, numerische Vorhersage und Vergleich**

JavaScript · Ray geometry · Numerical tests

Das Optiklabor berechnet gebrochene Strahlen und Fokus. Ein eigener Test zeigt: Extrapolation hilft bei gerader Bewegung, kann nach einer ungesehenen Richtungsänderung aber schlechter abschneiden.

**Prüfumfang:** Geometrisches Lehrmodell mit synthetischen Strahlen und Bewegungsverläufen.

**Quellcode und Gegenprobe**

- Implementierung — [Juri-Halveth/halveth-forschungslabor/branches/eye-optics-and-prediction/model.mjs:1](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/eye-optics-and-prediction/model.mjs#L1-L33) · `c6008ab`
- Gegenprobe — [Juri-Halveth/halveth-forschungslabor/branches/eye-optics-and-prediction/model.test.mjs:24](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/eye-optics-and-prediction/model.test.mjs#L24-L31) · `c6008ab`

<a id="pixel-comparison"></a>
### Bildänderungen innerhalb eines Prüfbereichs messen

**Gelieferte RGBA-Frames und begrenzte Änderungserkennung**

JavaScript · RGBA arrays · Sampling

Der Vergleicher zählt Pixeländerungen innerhalb einer Region und Schwelle. Er gibt die Lücken zwischen den gelieferten Zeitpunkten ausdrücklich mit aus.

**Prüfumfang:** Reiner Offline-Vergleich synthetischer Arrays; Aufnahme und Erfassung sind eigene Schnittstellen.

**Quellcode und Gegenprobe**

- Implementierung — [Juri-Halveth/halveth-forschungslabor/branches/pixel-region-change-observer/src/observer.js:130](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/pixel-region-change-observer/src/observer.js#L130-L192) · `c6008ab`
- Gegenprobe — [Juri-Halveth/halveth-forschungslabor/branches/pixel-region-change-observer/test/observer.test.js:44](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/pixel-region-change-observer/test/observer.test.js#L44-L54) · `c6008ab`

<a id="delivery"></a>
## Builds & Veröffentlichung

<a id="pages-delivery"></a>
### Generierten Stand vor dem Deploy prüfen

**Projektkatalog, statischer Build, CI und Pages**

GitHub Actions · Node.js · GitHub Pages

Die Portfolio-Pipeline baut aus dem Katalog, verlangt identische eingecheckte Ausgaben, führt die Tests aus und veröffentlicht den main-Stand über einen getrennten Deployjob.

**Prüfumfang:** Konkreter statischer Veröffentlichungsweg; CI und Deployment führen eigene Ergebnisse.

**Quellcode und Gegenprobe**

- Pipeline — [Juri-Halveth/Juri-Halveth.github.io/.github/workflows/pages.yml:17](https://github.com/Juri-Halveth/Juri-Halveth.github.io/blob/945eef06bf0a03822e7db589d31ef3dbb902cc69/.github/workflows/pages.yml#L17-L54) · `945eef0`
- Implementierung — [Juri-Halveth/Juri-Halveth.github.io/tools/build-portfolio.cjs:13](https://github.com/Juri-Halveth/Juri-Halveth.github.io/blob/945eef06bf0a03822e7db589d31ef3dbb902cc69/tools/build-portfolio.cjs#L13-L33) · `945eef0`
- Gegenprobe — [Juri-Halveth/Juri-Halveth.github.io/tests/portfolio.test.cjs:9](https://github.com/Juri-Halveth/Juri-Halveth.github.io/blob/945eef06bf0a03822e7db589d31ef3dbb902cc69/tests/portfolio.test.cjs#L9-L24) · `945eef0`

<a id="gradle-windows"></a>
### Windows-Werkzeuge im Java-Build verifizieren

**java-tron-Fork, Gradle-Metadaten und Compiler-Artefakte**

Java ecosystem · Gradle · Protobuf · gRPC

Der eigene Commit ergänzt SHA-256-Werte für die Windows-Versionen von protoc und protoc-gen-grpc-java. Der verlinkte Diff zeigt den exakten Umfang.

**Prüfumfang:** Eigener Build-Metadatenbeitrag im geerbten java-tron-Codebestand. Die Blockchain-Implementierung bleibt dem Upstream zugeordnet.

**Quellcode und Gegenprobe**

- Implementierung — [Juri-Halveth/halveth-tron-security-lab/gradle/verification-metadata.xml:856](https://github.com/Juri-Halveth/halveth-tron-security-lab/blob/d25e104e6b887bc4d782185a96ecf3c4eb782d8c/gradle/verification-metadata.xml#L856-L858) · `d25e104`
- Implementierung — [Juri-Halveth/halveth-tron-security-lab/gradle/verification-metadata.xml:1253](https://github.com/Juri-Halveth/halveth-tron-security-lab/blob/d25e104e6b887bc4d782185a96ecf3c4eb782d8c/gradle/verification-metadata.xml#L1253-L1255) · `d25e104`
- [Eigener Commit](https://github.com/Juri-Halveth/halveth-tron-security-lab/commit/0472a5b9551ac838a2feecee2de1b1fac3f3fba9)

---

Die Karte ordnet veröffentlichte Arbeitsproben nach Schnittstellen. Sie beschreibt den sichtbaren Implementierungsumfang und keine formale Qualifikation. Verbindungen sind fachliche Querverweise; eine gemeinsame Produktruntime wird daraus nicht abgeleitet.

Projektleitung und Zusammenstellung: Juri / HALVETH. Entwicklung mit KI-Unterstützung. Verlinkte Quellen behalten ihre Attribution und Lizenzen. Der Stand jedes Beispiels ist an eine konkrete Revision gebunden.

[Zum Projektüberblick](https://juri-halveth.github.io/) · [JSON](data/technical-map.json)
