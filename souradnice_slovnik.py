import csv
import json

# otevření souboru s výstupem
with open('obce.csv', 'w', newline='', encoding='utf-8') as f:
    # vytvoření objektu pro zápis csv
    writer = csv.writer(f)

    # otevření souboru s daty
    with open('obce.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # vytvoření seznamu se slovníky obsahujícími 'obecKod' a 'souradnice'
    seznam = [{'obecKod': obec['adresaUradu']['obecKod'], 'souradnice': obec['souradnice']} for obec in data['municipalities']]

    # zápis hlavičky csv souboru
    writer.writerow(['obecKod', 'souradnice'])

    # zápis hodnot 'obecKod' a 'souradnice' do csv souboru
    for obec in seznam:
        writer.writerow([obec['obecKod'], obec['souradnice']])