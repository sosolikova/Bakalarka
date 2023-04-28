import json
import csv

# načtení dat z orp-simple.json
with open('orp-simple.json', mode='r', encoding='utf-8') as orp_file:
    orp_data = json.load(orp_file)

# načtení dat z LexikonObci.csv a vytvoření slovníku kódů ORP a jejich čísel
orp_cisla = {}
with open('LexikonObci.csv', mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=';')
    for row in csv_reader:
        kod = row['KOD']
        orp_cislo = row['ORP_Cislo']
        orp_cisla[kod] = orp_cislo

# přidání sloupce ORP_Cislo k jednotlivým záznamům v orp-simple.json
for feature in orp_data['features']:
    kod = feature['properties']['KOD']
    feature['properties']['ORP_Cislo'] = orp_cisla[kod] if kod in orp_cisla else None

# uložení upravených dat do souboru orp-simple-with-ORP_Cislo.json
with open('orp-simple-with-ORP_Cislo.json', mode='w', encoding='utf-8') as out_file:
    json.dump(orp_data, out_file)

