#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# =========================================================
# DATEN LADEN / SPEICHERN
# =========================================================
def lade_daten():
    try:
        with open("data.json", "r") as f:
            daten = json.load(f)
            print(f"{len(daten)} Transaktionen geladen.")
            return daten
    except FileNotFoundError:
        print("Keine vorherigen Daten gefunden. Neue Liste wird erstellt.")
        with open("data.json", "w") as f:
            json.dump([], f)
        return []

def speichere_daten():
    with open("data.json", "w") as f:
        json.dump(transaktionen, f, indent=4)
    print(f"{len(transaktionen)} Transaktionen gespeichert.")

# =========================================================
# BUDGET-FUNKTION
# =========================================================
def lade_budgets():
    try:
        with open("budgets.json", "r") as f:
            budgets = json.load(f)
            print(f"{len(budgets)} Budgets geladen.")
            return budgets
    except FileNotFoundError:
        print("Keine vorherigen Budgets gefunden. Neue Liste wird erstellt.")
        return {}

def speichere_budgets():
    with open("budgets.json", "w") as f:
        json.dump(budgets, f, indent=4)
    print("Budgets gespeichert.")

def setze_budget(kategorie, limit):
    budgets[kategorie] = limit
    print(f"Budget für '{kategorie}' auf {limit} € gesetzt.")
    speichere_budgets()

def pruefe_budget(betrag, kategorie):
    if kategorie in budgets and budgets[kategorie] >= 0:
        ausgegeben = sum(t["betrag"] for t in transaktionen if t["kategorie"].lower() == kategorie.lower() and t["betrag"] < 0)
        if abs(ausgegeben + betrag) > budgets[kategorie]:
            print(f"⚠️ Warnung: Budget für '{kategorie}' ({budgets[kategorie]} €) überschritten!")

# =========================================================
# TRANSAKTIONEN HINZUFÜGEN
# =========================================================
def transaktion_hinzufuegen(betrag, kategorie, beschreibung, geplant=False, datum=None, typ="Einnahme"):
    if typ == "Ausgabe":
        betrag = -abs(betrag)
        pruefe_budget(betrag, kategorie)
    elif typ == "Einnahme":
        betrag = abs(betrag)

    if datum:
        datum_obj = datetime.strptime(datum, "%Y-%m-%d").date()
    else:
        datum_obj = datetime.today().date()

    transaktion = {
        "betrag": betrag,
        "kategorie": kategorie,
        "beschreibung": beschreibung,
        "datum": datum_obj.strftime("%Y-%m-%d"),
        "geplant": geplant,
        "typ": typ
    }
    transaktionen.append(transaktion)
    print("Transaktion wurde hinzugefügt!")
def transaktionen_mit_index_anzeigen():
        print("\n--- TRANSAKTIONEN MIT INDEX ---")
        for i, t in enumerate(transaktionen):
            status = "geplant" if t["geplant"] else "ausgeführt"
            print(f"{i}: [{t['datum']}] | {t['betrag']:.2f} € | {t['kategorie']} | {t['beschreibung']} | ({status})")

def transaktion_bearbeiten():
    transaktionen_mit_index_anzeigen()
    try:
        index = int(input("Welche Transaktion bearbeiten? Index eingeben: "))
        if index < 0 or index >= len(transaktionen):
            print("Ungültiger Index!")
            return

        t = transaktionen[index]
        print("\nAlte Werte ENTER lassen, um nicht zu ändern.")

        neuer_betrag = input(f"Betrag [{t['betrag']}]: ")
        neue_kategorie = input(f"Kategorie [{t['kategorie']}]: ")
        neue_beschreibung = input(f"Beschreibung [{t['beschreibung']}]: ")
        neues_datum = input(f"Datum [{t['datum']}] (YYYY-MM-DD): ")
        
        if neuer_betrag != "":
            t["betrag"] = float(neuer_betrag)
        if neue_kategorie != "":
            t["kategorie"] = neue_kategorie
        if neue_beschreibung != "":
            t["beschreibung"] = neue_beschreibung
        if neues_datum != "":
            t["datum"] = neues_datum

        print("Transaktion aktualisiert!")
        speichere_daten()

    except ValueError:
        print("Ungültige Eingabe!")


def transaktion_loeschen():
    transaktionen_mit_index_anzeigen()
    try:
        index = int(input("Welche Transaktion löschen? Index eingeben: "))
        if index < 0 or index >= len(transaktionen):
            print("Ungültiger Index!")
            return
        geloescht = transaktionen.pop(index)
        print(f"Transaktion gelöscht: {geloescht}")
        speichere_daten()
    except ValueError:
        print("Ungültige Eingabe!")



# =========================================================
# KONTOSTAND BERECHNEN
# =========================================================
def kontostand_berechnen(inkl_planung=False):
    heute = datetime.today().date()
    saldo = 0.0
    for t in transaktionen:
        t_datum = datetime.strptime(t["datum"], "%Y-%m-%d").date()
        if inkl_planung:
            saldo += t["betrag"]
        else:
            if (not t["geplant"]) or (t["geplant"] and t_datum <= heute):
                saldo += t["betrag"]

    if not inkl_planung and saldo < 0:
        print(f"Aktueller Kontostand: {saldo:.2f} € -> Houston we have a problem")
    elif inkl_planung:
        print(f"Voraussichtliches Saldo (inkl. geplanter Transaktionen): {saldo:.2f} €")
    else:
        print(f"Aktueller Kontostand: {saldo:.2f} €")
    return saldo

# =========================================================
# TRANSAKTIONEN ANZEIGEN
# =========================================================
def alle_transaktionen_anzeigen():
    print("\n--- ALLE TRANSAKTIONEN ---")
    for t in transaktionen:
        status = "geplant" if t["geplant"] else "ausgeführt"
        print(f"{t['datum']} | {t['betrag']:.2f} € | {t['kategorie']} | {t['beschreibung']} | {status}")
    print("--------------------------")

def nach_kategorie_filtern(kategorie):
    print(f"\n--- TRANSAKTIONEN IN KATEGORIE '{kategorie}' ---")
    for t in transaktionen:
        if t["kategorie"].lower() == kategorie.lower():
            status = "geplant" if t["geplant"] else "ausgeführt"
            print(f"{t['datum']} | {t['betrag']:.2f} € | {t['beschreibung']} | {status}")
    print("--------------------------")

def transaktionen_suchen():
    suchbegriff = input("Suchbegriff: ").lower()
    print(f"\n--- SUCHERGEBNIS ---")
    for t in transaktionen:
        if (suchbegriff in t["beschreibung"].lower()) or (suchbegriff in t["kategorie"].lower()):
            status = "geplant" if t["geplant"] else "ausgeführt"
            print(f"{t['datum']} | {t['betrag']:.2f} € | {t['kategorie']} | {t['beschreibung']} | {status}")
    print("--------------------------")

# =========================================================
# SALDO DIAGRAMM
# =========================================================
def diagramm_saldo():
    if not transaktionen:
        print("Keine Transaktionen vorhanden.")
        return

    daten_sortiert = sorted(transaktionen, key=lambda x: datetime.strptime(x["datum"], "%Y-%m-%d"))
    start_datum = datetime.strptime(daten_sortiert[0]["datum"], "%Y-%m-%d").date()
    ende_datum = max(datetime.today().date(), max(datetime.strptime(t["datum"], "%Y-%m-%d").date() for t in daten_sortiert))

    datum_liste = []
    saldo_liste = []
    aktueller_saldo = 0.0
    datum = start_datum
    while datum <= ende_datum + timedelta(days=30):
        tages_transaktionen = [t for t in transaktionen if datetime.strptime(t["datum"], "%Y-%m-%d").date() == datum]
        for t in tages_transaktionen:
            aktueller_saldo += t["betrag"]
        datum_liste.append(datum)
        saldo_liste.append(aktueller_saldo)
        datum += timedelta(days=1)

    plt.figure(figsize=(12,6))
    plt.plot(datum_liste, saldo_liste, marker='o', linestyle='-')
    plt.title("Kontostand Verlauf (inkl. geplanter Transaktionen)")
    plt.xlabel("Datum")
    plt.ylabel("Saldo (€)")
    plt.grid(True)
    plt.axhline(0, color='red', linestyle='--')
    plt.fill_between(datum_liste, saldo_liste, 0, where=[s<0 for s in saldo_liste], color='red', alpha=0.2)
    plt.show()

# =========================================================
# MONATSÜBERSICHT / STATISTIKEN
# =========================================================
def monats_auswertung(jahr=None, monat=None):
    if not jahr: jahr = datetime.today().year
    if not monat: monat = datetime.today().month

    ausgaben = [t for t in transaktionen if t["betrag"] < 0 and 
                datetime.strptime(t["datum"], "%Y-%m-%d").year == jahr and
                datetime.strptime(t["datum"], "%Y-%m-%d").month == monat]

    einnahmen = [t for t in transaktionen if t["betrag"] > 0 and 
                datetime.strptime(t["datum"], "%Y-%m-%d").year == jahr and
                datetime.strptime(t["datum"], "%Y-%m-%d").month == monat]

    gesamt_ausgaben = sum(t["betrag"] for t in ausgaben)
    gesamt_einnahmen = sum(t["betrag"] for t in einnahmen)

    top_kategorien = {}
    for t in ausgaben:
        top_kategorien[t["kategorie"]] = top_kategorien.get(t["kategorie"], 0) + abs(t["betrag"])
    top_3 = sorted(top_kategorien.items(), key=lambda x: x[1], reverse=True)[:3]

    tage_im_monat = (datetime(jahr, monat % 12 + 1, 1) - timedelta(days=1)).day
    durchschnitt_taeglich = abs(gesamt_ausgaben) / tage_im_monat
    sparquote = (gesamt_einnahmen + gesamt_ausgaben) / gesamt_einnahmen * 100 if gesamt_einnahmen else 0

    print(f"\n--- Monatsauswertung {jahr}-{monat:02d} ---")
    print(f"Gesamtausgaben: {gesamt_ausgaben:.2f} €")
    print(f"Gesamteinnahmen: {gesamt_einnahmen:.2f} €")
    print(f"Top 3 Kategorien: {top_3}")
    print(f"Durchschnittliche tägliche Ausgabe: {durchschnitt_taeglich:.2f} €")
    print(f"Sparquote: {sparquote:.2f}%")
    print("----------------------------------------")

# =========================================================
# MENÜ
# =========================================================
def menu():
    print("""
====================================
          CASH FLOW TRACKER
====================================
Benutzeranleitung:
1. Einnahmen sofort = positive Werte (Saldo wird aktualisiert)
2. Ausgaben sofort = negative Werte (Saldo wird aktualisiert)
3. Geplante Einnahmen/Ausgaben = werden noch nicht im Saldo berücksichtigt
4. Datum im Format YYYY-MM-DD
5. Daten werden automatisch in 'data.json' gespeichert
====================================
""")
    while True:
        print("\nWähle eine Option:")
        print("1. Einnahme sofort")
        print("2. Ausgabe sofort")
        print("3. Geplante Einnahme")
        print("4. Geplante Ausgabe")
        print("5. Alle Transaktionen anzeigen")
        print("6. Nach Kategorie filtern")
        print("7. Kontostand anzeigen")
        print("8. Voraussichtliches Saldo anzeigen")
        print("9. Transaktionen suchen")
        print("10. CSV exportieren")
        print("11. Saldo Diagramm anzeigen")
        print("12. Speichern & Beenden")
        print("13. Budget setzen")
        print("14. Monatsauswertung anzeigen")
        print("15. Transaktion bearbeiten")
        print("16. Transaktion löschen")

        auswahl = input("Deine Auswahl: ")

        if auswahl in ["1","2","3","4"]:
            betrag = float(input("Betrag: "))
            kategorie = input("Kategorie: ")
            beschreibung = input("Beschreibung: ")
            datum_eingabe = input("Datum (YYYY-MM-DD) oder Enter für heute: ")
            geplant = auswahl in ["3","4"]
            typ = "Ausgabe" if auswahl in ["2","4"] else "Einnahme"
            transaktion_hinzufuegen(betrag, kategorie, beschreibung, geplant, datum_eingabe if datum_eingabe else None, typ)

        elif auswahl == "5":
            alle_transaktionen_anzeigen()
        elif auswahl == "6":
            kategorie = input("Kategorie zum Filtern: ")
            nach_kategorie_filtern(kategorie)
        elif auswahl == "7":
            kontostand_berechnen()
        elif auswahl == "8":
            kontostand_berechnen(inkl_planung=True)
        elif auswahl == "9":
            transaktionen_suchen()
        elif auswahl == "10":
            import csv
            with open("transaktionen.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Datum","Betrag (€)","Kategorie","Beschreibung","Geplant","Typ"])
                for t in transaktionen:
                    writer.writerow([t["datum"], t["betrag"], t["kategorie"], t["beschreibung"], t["geplant"], t["typ"]])
            print("CSV-Datei 'transaktionen.csv' erstellt.")
        elif auswahl == "11":
            diagramm_saldo()
        elif auswahl == "12":
            speichere_daten()
            speichere_budgets()
            print("Programm beendet. Auf Wiedersehen!")
            break
        elif auswahl == "13":
            kategorie = input("Kategorie: ")
            limit = float(input("Budgetlimit (€): "))
            setze_budget(kategorie, limit)
        elif auswahl == "14":
            jahr = input("Jahr (Enter für aktuelles Jahr): ")
            monat = input("Monat (Enter für aktuellen Monat): ")
            jahr = int(jahr) if jahr else None
            monat = int(monat) if monat else None
            monats_auswertung(jahr, monat)
        elif auswahl == "15":
            transaktion_bearbeiten()
        elif auswahl == "16":
            transaktion_loeschen()
        else:
            print("Ungültige Eingabe. Bitte erneut wählen.")

# =========================================================
# START DES PROGRAMMS
# =========================================================
transaktionen = lade_daten()
budgets = lade_budgets()
menu()


# In[ ]:




