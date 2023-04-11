import json

# otevření souboru
with open('obce.json', encoding='utf-8') as f:
    data = json.load(f)

# vytvoření seznamu se slovníky obsahujícími 'obecKod' a 'souradnice'
seznam = [{'obecKod': obec['adresaUradu']['obecKod'], 'souradnice': obec['souradnice']} for obec in data['municipalities']]

# vypsání hodnot 'obecKod' a 'souradnice'
for obec in seznam:
    print(obec['obecKod'], obec['souradnice'])