import json
import geopandas as gpd
import matplotlib.pyplot as plt

# Načtení souboru

gdf = gpd.read_file('kraje-simple.json', encoding='utf-8')

# Vypsání načtených dat
print('_________nactene data__________-')
print(gdf)
gdf.plot()
plt.show()

