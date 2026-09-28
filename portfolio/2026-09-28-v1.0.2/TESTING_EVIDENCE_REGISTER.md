# Test- und Ausführungsbelege

| Beleg | Tatsächlich gebundener Stand | Aussageumfang |
| --- | --- | --- |
| E-MW-NATIVE | Nativer OpenMW-Lauf, passed=true, exitCode=0 | Ray-Auswahl, Konsolenweg, getrennte Instanzen, Cooldown, Save/Reload, Zustandsfortschritt und Effekt-Lebenszyklus |
| E-MW-INSTALL | Sechs Patchdateien; neun geschützte Dateien unverändert | Gebundener lokaler Installationszustand; veränderliche Inbox ausdrücklich getrennt |
| E-MW-CI | Zwei Source-checks-Läufe, completed/success, gleicher Feature-Commit | GitHub-gemeldete Quellprüfungen |
| E-OPEN-CI / E-TRESOR-CI | Aktueller Default-HEAD: CI erfolgreich gemeldet | Workflow-Ergebnisse; keine umfassende Produktzertifizierung |
| E-SCARLET-CI / E-PORTAL-CI | Pages-Deployment erfolgreich gemeldet | Veröffentlichungspfad; kein Ersatz für funktionale Tests |
| E-T0 | Bestehender Ergebnisbeleg und zwei gelesene Skripte | Fünf Modelle, ein Shader und endliche mathematische Beispiele |

Das Portfolio selbst erhält eine getrennte Struktur-, Hash-, Link- und Exportprüfung. Ihre Ergebnisse stehen in machine/validation.json. Diese Prüfung verifiziert die Portfolio-Dateien; sie führt keine historischen Sicherheitsversuche erneut aus.
