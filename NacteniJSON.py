import json
import geopandas as gpd
import matplotlib.pyplot as plt

# Načtení souboru

gdf_kraje = gpd.read_file('kraje-simple.json', encoding='utf-8')
gdf_orp = gpd.read_file('orp-simple.json', encoding='utf-8')
gdf_obce = gpd.read_file('obce-simple.json', encoding='utf-8')

# Vypsání načtených dat
print('_________nactene data__________-')
#print(gdf)
leg_kwds={'title': 'NAZEV', 
          'loc': 'upper left',
          'bbox_to_anchor': (1,1.03),
          'ncol':1}
gdf_kraje.plot(column = 'NAZEV',
               cmap = 'Accent',
               legend = True,
               legend_kwds = leg_kwds)
plt.title('Odpad dle krajů')
#gdf_orp.plot(column = 'NAZEV',legend = False)
#gdf_obce.plot(column = 'NAZEV',legend = False)
plt.show()

