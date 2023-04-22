import json
import pandas as pd
import plotly.express as px
import HromadneNacitani as hn

# nahrání dat
indikator_map_kraje = hn.Zdrojovy_Kody_Mnozstvi[(hn.Zdrojovy_Kody_Mnozstvi['Indikator'] == 'Produkce') & (hn.Zdrojovy_Kody_Mnozstvi['Druh_Odpadu'] == '200111')]
kraje_produkce = hn.seskupeni_dat_po_sloupcich(indikator_map_kraje,'ZmenaMnozstvi','Evident_Kraj_Nazev','Indikator')

# načtení geometrie pro kraje
kraje_geojson = json.load(open('kraje-simple.json', 'r', encoding='utf-8'))

fig = px.choropleth_mapbox(kraje_produkce,
                           geojson=kraje_geojson,
                           locations='Evident_Kraj_Nazev',
                           featureidkey="properties.NAZEV",
                           color='ZmenaMnozstvi',
                           color_continuous_scale='YlGn',
                           mapbox_style='carto-positron',
                           center={"lat": 49.8, "lon": 15.6},
                           zoom=7,
                           opacity=0.7,
                           labels={'ZmenaMnozstvi':'Množství odpadu Kraj'},
                           hover_data={'Evident_Kraj_Nazev':True, 'ZmenaMnozstvi':':.2f'}
                          )
fig.show()
