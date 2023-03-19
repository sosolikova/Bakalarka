import pandas as pd
import geopandas as gpd
import json
import folium
import chardet
import HromadneNacitani as hn

#gdf = gpd.read_file('kraje-simple.json')
#gdf = gpd.read_file('kraje-simple.json', encoding='utf-8')
with open("kraje-simple.json", "r", encoding="utf-8") as f:
    gdf = json.load(f)

'''
with open('kraje-simple.json') as f:
    gdf = json.load(f)
gdf.head()
'''
# vytvoření prázdné mapy
m = folium.Map(location=[49.8, 15.6], zoom_start=7)

# přidání vrstvy pro zobrazení dat z dataframe
folium.Choropleth(
    geo_data='kraje-simple.json',
    name='choropleth',
    data=hn.Zdrojovy_kody_mnozstvi,
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