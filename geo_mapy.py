import pandas as pd
import geopandas as gpd
import json
import folium
import chardet
import HromadneNacitani as hn

# ziskani df s vyfiltrovanými údaji pro Indikator 'Produkce' a použita funkce sum za jednotlivé kraje
indikator_map = hn.Zdrojovy_kody_mnozstvi[(hn.Zdrojovy_kody_mnozstvi['Indikator'] == 'Produkce') & (hn.Zdrojovy_kody_mnozstvi['Druh_Odpadu'] == '200111')]
kraje_produkce = hn.group_data_by_columns(indikator_map,'ZmenaMnozstvi','Evident_Kraj','Indikator')
print('___----indikator-map - kraje_produkce ___________')
print(kraje_produkce.head)


gdf_kraje = gpd.read_file('kraje-simple.json', encoding='utf-8')

# vytvoření prázdné mapy
m = folium.Map(location=[49.8, 15.6], zoom_start=7)

# přidání vrstvy pro zobrazení dat z dataframe
folium.Choropleth(
    geo_data=gdf_kraje,
    name='choropleth',
    data=kraje_produkce,
    columns=['Evident_Kraj', 'ZmenaMnozstvi'],
    key_on='feature.properties.NAZEV',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Množství odpadu'
).add_to(m)

# přidání ovládací vrstvy pro vrstvu s daty
folium.LayerControl().add_to(m)

# uložení mapy do html souboru
m.save('mapa.html')
