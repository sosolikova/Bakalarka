import json
import geopandas as gpd
import matplotlib.pyplot as plt
import HromadneNacitani as hn

# ziskani df s vyfiltrovanými údaji pro Indikator 'Produkce' a použita funkce sum za jednotlivé kraje
indikator_map_orp = hn.Zdrojovy_kody_mnozstvi[(hn.Zdrojovy_kody_mnozstvi['Indikator'] == 'Produkce') & (hn.Zdrojovy_kody_mnozstvi['Druh_Odpadu'] == '200110')]
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


# Vypsání načtených dat
print('_________nactene data__________-')
print(gdf_merged)
'''
leg_kwds={'title': 'ZmenaMnozstvi', 
          'loc': 'upper left',
          'bbox_to_anchor': (1,1.03),
          'ncol':1}
          '''
# Použití metody plot() pro zobrazení mapy s barvami krajů podle hodnot ze sloupce 'ZmenaMnozstvi' v novém datovém rámci gdf_merged.
gdf_merged.plot(column = 'ZmenaMnozstvi',
               cmap = 'Accent',
               legend = True)
               #legend_kwds = leg_kwds)
plt.title('Odpad dle ORP')
#gdf_orp.plot(column = 'NAZEV',legend = False)
#gdf_obce.plot(column = 'NAZEV',legend = False)
plt.show()

