import datetime
from astral import sun, moon
from astral import planetary_position

# Funktion zum Berechnen der Positionen und Geschwindigkeiten der Planeten
def berechne_planeten_positionen_und_geschwindigkeiten(datum):
    # Liste der Planeten, die du berechnen möchtest
    planeten = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

    # Ergebnisliste für Positionen und Geschwindigkeiten
    ergebnisse = []

    # Berechnung der Positionen und Geschwindigkeiten für jeden Planeten
    for planet in planeten:
        # Berechnung der Position und Geschwindigkeit des Planeten
        position = planetary_position(datum, planet)
        geschwindigkeit = planetary_position(datum + datetime.timedelta(days=1), planet) - position

        # Hinzufügen der Position und Geschwindigkeit zur Ergebnisliste
        ergebnisse.append({'Planet': planet, 'Position': position, 'Geschwindigkeit': geschwindigkeit})

    return ergebnisse

# Aktuelles Datum
aktuelles_datum = datetime.date.today()

# Berechnung der Positionen und Geschwindigkeiten der Planeten
ergebnisse = berechne_planeten_positionen_und_geschwindigkeiten(aktuelles_datum)

# Ausgabe der Ergebnisse
for ergebnis in ergebnisse:
    print(ergebnis['Planet'])
    print('Position:', ergebnis['Position'])
    print('Geschwindigkeit:', ergebnis['Geschwindigkeit'])
    print('---')