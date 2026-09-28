# Hypothesis Revision Cycle · 1.0.0

Ein kleiner ausführbarer Forschungszyklus: Ideen erhalten, Gegenmodelle
vergleichen und den nächsten fehlenden Arbeitsschritt konkret benennen.
Die Implementierung ist eine eigenständige Ergänzung zu HALVETH Core 3.5.1.
Sie benötigt Node.js 22 oder neuer und keine zusätzlichen Pakete.

## Die sechs Schritte

1. **Hypothese festhalten:** Aussage, Quelle und bekannte Ereigniszeit binden.
2. **Modelle unterscheiden:** Mindestens ein Hypothesenmodell und ein Gegenmodell
   ausdrücklich beschreiben. Zwei Namen mit derselben Erklärung reichen nicht.
3. **Beobachtung planen:** Eine gemeinsame Frage, Methode und einen Scope mit
   unterschiedlichen beobachtbaren Vorhersagen für die Modelle formulieren.
4. **Minimum-Evidenz vorab binden:** Vor Beobachtung und Ergebnis die benötigten
   Quellen oder Messungen, Kriterien und Mindestmengen festlegen. Den Plan-Digest
   zusammen mit dem unveränderten Plan aufbewahren.
5. **Änderungsbedingung nennen:** Für jedes Modell beantworten: Welcher konkrete
   Befund würde meine Einschätzung ändern? Die Bedingung referenziert Kriterien.
6. **Ergebnis einordnen:** Beobachtungen, Begründung, eingegrenztes Ergebnis,
   offenen Rest und eine konkrete Wiederaufnahmebedingung dokumentieren.

`OPEN` und `INCONCLUSIVE` sind reguläre Ergebnisse. Der Prüfer hält fehlende
Arbeitsschritte sichtbar; er bestätigt keine Hypothese automatisch und führt
keine Testidee aus.

## Sofort lokal verwenden

Im Verzeichnis dieser README:

```powershell
node review.mjs --template
node review.mjs example.synthetic.json
```

Die CLI liest höchstens 1 MB UTF-8-JSON und schreibt das Ergebnis auf
Standardausgabe. Sie verändert keine Eingabedatei. Das Beispiel ist vollständig
synthetisch: Schriftgröße und Kontrast stehen als konkurrierende Erklärungen
einer Lesbarkeitsfrage gegenüber. Es enthält einen Plan, aber keine gemessenen
Beobachtungen und kein Ergebnis. Erwartet werden `NEEDS_WORK`, `RESULT_OPEN`
und `hypothesisConfirmed: false`.

Eigene Anwendung:

```js
import {
  createRevisionCycle,
  reviewHypothesisRevisionCycle,
  revisionPlanDigest
} from './hypothesis-revision-cycle.mjs';

const cycle = createRevisionCycle(
  'IDEA-1',
  'Die neue Menüschrift verbessert die Lesbarkeit.',
  'SYNTHETIC:DESIGN-QUESTION',
  new Date().toISOString()
);
const review = reviewHypothesisRevisionCycle(cycle);
console.log(review.nextStep, review.missing);
// Erst nach ausgefülltem Plan zur späteren Ergebnisbindung aufbewahren:
// const planDigest = revisionPlanDigest(cycle);
```

## Zeit und Änderungen

| Feld | Bedeutung |
| --- | --- |
| `hypothesis.eventTime` | Zeitpunkt des beschriebenen Ereignisses, soweit bekannt |
| `observation.eventTime` | Zeitpunkt des beobachteten oder aus Quellen rekonstruierten Ereignisses |
| `observation.observedAt` | Zeitpunkt der Beobachtung beziehungsweise Quellenprüfung |
| `recordedAt` | Zeitpunkt der jeweiligen Aufzeichnung |
| `plan.boundAt` | Deklarierter Zeitpunkt der Planbindung |
| `prediction.targetTime` | Geplanter künftiger Zeitpunkt; keine Beobachtung |

Unbekannte Ereignis- und Zielzeiten bleiben `null`. Ein früheres Ereignis kann
heute anhand einer Quelle beobachtet werden, ohne sein Ereignisdatum zu ändern.
Eine Zukunftsvorhersage wird nicht zu einer gegenwärtigen Messung.

Der Plan-Digest bindet Hypothese, Modelle und gesamten Plan. Änderungen daran
erzeugen einen anderen Digest. Das Ergebnis muss seinen zugehörigen Plan
referenzieren. Zeitwerte bleiben Angaben des Aufrufers: Ihre formale Reihenfolge
und ein Digest beweisen keine unabhängige Präregistrierung. Dafür ist ein
separater nachweisbarer Archiv- oder Zeitbeleg nötig. Nachträglich gewählte
Kriterien bleiben explorativ; ein neuer vorab gebundener Durchlauf bekommt eine
neue Zyklus-ID. Historische Dateien werden nicht überschrieben.

## Ergebnis richtig lesen

- `NEEDS_WORK`: `missing` und `nextStep` benennen offene Arbeitsschritte.
- `DECLARED_CYCLE_STRUCTURALLY_BOUND`: Felder, Referenzen, deklarierte Zeiten,
  Mindestmengen und Digest passen im vorgelegten Datensatz zusammen.
- `declaredResult`: eingetragene Bewertung des Aufrufers; kein Validatorurteil.
- `evidenceCounts`: referenzierte Quellen-/Inhaltspaare pro Kriterium. Mehrere
  IDs mit derselben Quelle und demselben Inhalt zählen einmal.

Der Textvergleich erkennt bestimmte doppelte Erklärungen, prüft aber nicht
deren fachliche Verschiedenheit. Quelleninhalte werden nicht geladen, ihre
Richtigkeit und Unabhängigkeit nicht beglaubigt. Der Prüfer beweist weder eine
Ursache noch die Vollständigkeit der Modellmenge. `SELECTED`, `TRUE` und
`EXECUTED` sind keine erlaubten Ergebniswerte. Auswahl, Wahrheit, Bewertung und
Ausführung bleiben getrennt. Die Claim-Grenze lautet
`LOCAL_STRUCTURE_AND_NEXT_STEP_ONLY`.

## Optionaler HTTP-Adapter

`hypothesis-revision-http.mjs` exportiert `handleHypothesisRevisionRequest`.
Er erhält vom einbettenden Server drei Funktionen: `requireLocalAgentRequest`,
`readJsonBody` und `jsonResponse`. Der Request-Gate wird vor der Bodyverarbeitung
ausgeführt. Der Host muss ihn selbst implementieren und durchsetzen sowie
Bodygröße, Fehlerantworten und Betriebskonfiguration festlegen. Das Modul startet
keinen Server, öffnet keinen Port und autorisiert keinen Aufruf selbst.

Formal gültige, unvollständige Zyklen geben HTTP 200 mit `NEEDS_WORK` zurück.
Strukturelle Eingabefehler werden mit `statusCode = 400` an den Host geworfen.
Gate-Fehler bleiben Fehler des Hosts. Der Adapter führt keine externe Prüfung
aus und hat keine Abhängigkeit von einer lokalen Projektkonfiguration.

## Lizenz und Umfang

Die [MIT-Lizenz](LICENSE) gilt ausschließlich für die Dateien in diesem
Methodenverzeichnis. Sie trifft keine Aussage über die Lizenz anderer
Repository-Inhalte, fremder Quellen oder referenzierter Daten.
Copyright 2026 HALVETH VERACHEL Studios.
