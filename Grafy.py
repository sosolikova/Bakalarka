import os
import pandas as pd
import matplotlib.pyplot as plt
import Funkce
import HromadneNacitani

Kraje = HromadneNacitani.seskupeni_dat_po_sloupcich(HromadneNacitani.Zdrojovy_Kody_Mnozstvi,'ZmenaMnozstvi','Druh_Odpadu','Indikator','Evident_Kraj')
Funkce.save_dataframe_to_csv(Kraje,'Kraje_Produkce')
""" 
Kraje[Kraje['Druh_Odpadu'] == '200110']['ZmenaMnozstvi'].hist()
plt.show()
"""
Kraje.head()