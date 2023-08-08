import csv
import json

with open('/hier_speicher_adresse.csv', 'w', encoding='utf-8') as csv_schreib_datei:
    writer = csv.writer(csv__schreib_datei, delimiter=',')
    writer.writerow(kopfzeile)

    for eintrag in fly.values():
        zeile = []
        for spalte in kopfzeile:
            zeile.append(eintrag[spalte])
        writer.writerow(zeile)