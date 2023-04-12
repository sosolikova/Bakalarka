import json
import numpy as np
from scipy.spatial.distance import pdist, squareform
import HromadneNacitani as hn

# ziskani df s vyfiltrovanými údaji pro Indikator 'Produkce' a použita funkce sum za jednotlivé kraje
indikator_map_zuj = hn.Zdrojovy_kody_mnozstvi[(hn.Zdrojovy_kody_mnozstvi['Indikator'] == 'Produkce') & (hn.Zdrojovy_kody_mnozstvi['Druh_Odpadu'] == '200111')]
zuj_produkce = hn.group_data_by_columns(indikator_map_zuj,'ZmenaMnozstvi','Evident_ZUJ_Cislo','Indikator')

print('nacteni odpadu')
# otevření souboru s geografickými daty o obcích
with open('obce.json', encoding='utf-8') as f:
    data = json.load(f)

# vytvoření seznamu se slovníky obsahujícími 'obecKod' a 'souradnice'
seznam = [{'obecKod': obec['adresaUradu']['obecKod'], 'souradnice': obec['souradnice']} for obec in data['municipalities']]
print('vytvoreni slovniku')
# vytvoření pole souřadnic a seznamu identifikátorů obcí
coords = []
obecKody = []
for obec in seznam:
    obecKod = obec['obecKod']
    souradnice = obec['souradnice']
    if souradnice is None:
        continue
    lat, lon = map(float, souradnice.split(','))
    coords.append([lat, lon])
    obecKody.append(obecKod)
print('vytvoreni pole')
# vytvoření pole produkce odpadů
produced_waste = zuj_produkce['ZmenaMnozstvi'].values

# výpočet euklidovské vzdálenosti mezi obcemi
distances = squareform(pdist(coords))
print('vypocet vzdalenosti')
# normalizace dat
produced_waste = (produced_waste - produced_waste.mean()) / produced_waste.std()
print('vypocet morana')
# výpočet Moranova I
N = len(produced_waste)
W = 1 / distances
W = W / np.sum(W, axis=1)[:, None]
I = (N / np.sum(W)) * np.sum(W * (produced_waste - np.mean(produced_waste)) * (np.sum(W, axis=1) - 1 - N * (np.sum(W, axis=1) / np.sum(W)) ** 2))

# vypsání výsledků
print("Moran's I:", I)
