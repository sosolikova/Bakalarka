import pandas as pd
import geopandas as gpd
import json
import folium
import chardet
import webbrowser
import HromadneNacitani as hn
import Funkce
import plotly.express as px

# ziskani df s vyfiltrovanými údaji pro Indikator 'Produkce' a použita funkce sum za jednotlivé kraje
indikator_map_kraje = hn.Zdrojovy_kody_mnozstvi[(hn.Zdrojovy_kody_mnozstvi['Indikator'] == 'Produkce') & (hn.Zdrojovy_kody_mnozstvi['Druh_Odpadu'] == '200111')]
kraje_produkce = hn.group_data_by_columns(indikator_map_kraje,'ZmenaMnozstvi','Evident_Kraj_Nazev','Indikator')
print('___----indikator-map - kraje_produkce ___________')
print(kraje_produkce.head)

# ORP
'''
indikator_map_orp = hn.Zdrojovy_Kody_ORP_Partner[(hn.Zdrojovy_Kody_ORP_Partner['Indikator'] == 'Produkce') & (hn.Zdrojovy_Kody_ORP_Partner['Druh_Odpadu'] == '200111')]
orp_produkce = hn.group_data_by_columns(indikator_map_orp,'Mnozstvi','Evident_ORP_Nazev','Indikator')
print('___----indikator-map - orp_produkce ___________')
Funkce.save_dataframe_to_csv(orp_produkce,'orp_produkce.csv')
print(orp_produkce.head)
'''

# obce
indikator_map_obce = hn.Zdrojovy_kody_mnozstvi[(hn.Zdrojovy_kody_mnozstvi['Indikator'] == 'Produkce') & (hn.Zdrojovy_kody_mnozstvi['Druh_Odpadu'] == '200110')]
obce_produkce = hn.group_data_by_columns(indikator_map_obce,'ZmenaMnozstvi','Evident_ZUJ_Nazev','Indikator')
print('___----indikator-map - obce_produkce ___________')
print(obce_produkce.head)

# načtení json souborů
gdf_kraje = gpd.read_file('kraje-simple.json', encoding='utf-8')
gdf_orp = gpd.read_file('orp-simple.json', encoding='utf-8')
gdf_obce = gpd.read_file('obce-simple.json', encoding='utf-8')

# vytvoření prázdné mapy
m = folium.Map(location=[49.8, 15.6], zoom_start=7)

# přidání vrstvy pro zobrazení dat z dataframe
folium.Choropleth(
    geo_data=gdf_kraje,
    name='choropleth',
    data=kraje_produkce,
    columns=['Evident_Kraj_Nazev', 'ZmenaMnozstvi'],
    key_on='feature.properties.NAZEV',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Množství odpadu Kraj',
    fill_missing= 0,
    highlight=True,
    tooltip = folium.GeoJsonTooltip(
        fields=['Evident_Kraj_Nazev', 'ZmenaMnozstvi'],
        aliases=['Kraj:', 'Množství odpadu:'],
        localize=True
    )
).add_to(m)

# přidání ovládací vrstvy pro vrstvu s daty
folium.LayerControl().add_to(m)

# uložení mapy do html souboru
m.save('mapa.html')
webbrowser.open('mapa.html')
'''
fig = px.choropleth(indikator_map_kraje,
                        locations='Evident_Kraj_Nazev',
                        geojson=gdf_kraje,
                        color='ZmenaMnozstvi',
                        hover_name = 'Evident_Kraj_Nazev',
                        hover_data = ['ZmenaMnozstvi'])
fig.update_geos(fitbounds="locations",visible=False)
fig.show()
'''