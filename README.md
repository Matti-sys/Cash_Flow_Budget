Cash_Flow_Budget

Cash_Flow_Budget ist ein einfaches, aber erweitertes Python-Programm zur Verwaltung von täglichen Einnahmen und Ausgaben. Das Projekt demonstriert grundlegende und fortgeschrittene Python-Kenntnisse wie Listen, Dictionaries, Funktionen, Schleifen, Fehlerbehandlung, Dateiverarbeitung und Datenvisualisierung.

Funktionen

Hinzufügen von Einnahmen und Ausgaben (sofort oder geplant)

Alle Transaktionen anzeigen und nach Kategorien filtern

Transaktionen nach Beschreibung oder Kategorie suchen

Berechnung des aktuellen und voraussichtlichen Kontostands

Export von Transaktionen in eine CSV-Datei

Visualisierung des Kontostands als Liniendiagramm

Budget pro Kategorie – Limits setzen und Warnungen bei Überschreitung

Monatliche Auswertungen und Statistiken – Gesamtausgaben/-einnahmen, Top 3 Kategorien, durchschnittliche tägliche Ausgaben, Sparquote

Automatisches Speichern und Laden der Daten in JSON-Dateien (data.json und budgets.json)

## Installation

Python 3.x installieren

## Erforderliche Pakete installieren:

pip install matplotlib


## Programm starten:

python Cash_Flow_Budget.py

Projektstruktur
Cash_Flow_Budget/
├── Cash_Flow_Budget.py       # Hauptskript
├── data.json                 # Gespeicherte Transaktionen
├── budgets.json              # Gespeicherte Budgetlimits
├── README.md                 # Projektdokumentation

## Benutzeranleitung

Einnahmen oder Ausgaben eingeben, Betrag, Kategorie, Beschreibung und optionales Datum (YYYY-MM-DD) angeben

Menü verwenden, um Transaktionen anzuzeigen, zu filtern, Budgets zu setzen oder monatliche Statistiken abzurufen

Programm speichert Daten automatisch beim Beenden und lädt sie beim Start

Beispielanwendung
Wähle eine Option:
1. Einnahme sofort hinzufügen
2. Ausgabe sofort hinzufügen
5. Alle Transaktionen anzeigen
13. Budget für eine Kategorie setzen
14. Monatsauswertung anzeigen

