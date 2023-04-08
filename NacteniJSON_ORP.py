import json
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import HromadneNacitani as hn
import mplcursors

# ziskani df s vyfiltrovanými údaji pro Indikator 'Produkce' a použita funkce sum za jednotlivé kraje
indikator_map_orp = hn.Zdrojovy_kody_mnozstvi[(hn.Zdrojovy_kody_mnozstvi['Indikator'] == 'Produkce') & (hn.Zdrojovy_kody_mnozstvi['Druh_Odpadu'] == '200111')]
orp_produkce = hn.group_data_by_columns(indikator_map_orp,'ZmenaMnozstvi','Evident_ORP_Nazev','Indikator')
print('___----indikator-map - orp_produkce ___________')
print(orp_produkce.head)

# Načtení souboru
gdf_kraje = gpd.read_file('kraje-simple.json', encoding='utf-8')
gdf_orp = gpd.read_file('orp-simple.json', encoding='utf-8')
gdf_obce = gpd.read_file('obce-simple.json', encoding='utf-8')

#Sloučení df kraje_produkce s geometrickým df podle názvu kraje
gdf_merged = gdf_orp.merge(orp_produkce, left_on='NAZEV', right_on='Evident_ORP_Nazev',how='left')

# nahrazení chybějících hodnot v datovém rámci gdf_merged
gdf_merged['ZmenaMnozstvi'] = gdf_merged['ZmenaMnozstvi'].fillna(value=0)

# určení kvantilů
q1 = gdf_merged['ZmenaMnozstvi'].quantile(0.15)
q3 = gdf_merged['ZmenaMnozstvi'].quantile(0.85)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
upper_bound = round(upper_bound,-3)

# Vypsání načtených dat
print('_________nactene data__________-')
print(gdf_merged)

cmap = plt.cm.get_cmap('GnBu')
cmap.set_over('black')
cmap.set_under('white')
fig, ax = plt.subplots()


# použití metody plot() pro zobrazení mapy s barvami krajů podle hodnot ze sloupce 'ZmenaMnozstvi' v novém datovém rámci gdf_merged
gdf_merged.plot(column = 'ZmenaMnozstvi',
                cmap = cmap,
                ax=ax,
                legend = True,
                edgecolor='black',
                linewidth=0.5,
                alpha=0.8,
                norm=plt.Normalize(1, vmax=upper_bound))

formatted_upper_bound = '{:,.0f}'.format(upper_bound).replace(',', ' ')
# Přidání textu s hodnotou vmax
ax.annotate('Černě jsou zvýrazněny\n odlehlé hodnoty nad {} kg'.format(formatted_upper_bound), xy=(0.95, 0.1), xycoords='axes fraction', ha='right', va='center')


plt.title('Odpad dle ORP')
plt.show()