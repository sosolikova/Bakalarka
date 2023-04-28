from cgitb import text
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import tkinter
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import options
from ttkthemes import ThemedTk
from ttkthemes import ThemedStyle
import json
import geopandas as gpd
import matplotlib.pyplot as plt
import HromadneNacitani as hn
import Funkce as fc
import csv
import locale
locale.setlocale(locale.LC_ALL, '')

volby_indikator = []
volby_kod = []
volby_rok = []
volby_druhOdpadu = []
volby_funkce = []
volby_sloupce = []
volby_sloupce_univ = ['Evident_Kraj_Nazev','Evident_ORP_Nazev','Indikator','Kod','OdpadNaObyv_g','Odpad_vKg','Pocet_Obyvatel','Partner_Kraj_Nazev','Partner_ORP_Nazev','Druh_Odpadu','Rok']
volby_seskupeni = []
volby_seskupeni_univ = ['Druh_Odpadu','Indikator','Kod']

# Seznamy pro evidenta
volby_evident_kraj = []
volby_evident_ORP = []
volby_evident_nazev = []
volby_evident_typ = []

# Seznamy pro partnera
volby_partner_kraj = []
volby_partner_ORP = []
volby_partner_nazev = []
volby_partner_typ = []

# Definice funkcí
def handle_evident_kraj(selection):
    volby_evident_kraj.append(selection)
    text_widget.insert('1.0', f"Evident kraj: {selection}\n")

def handle_evident_ORP(selection):
    volby_evident_ORP.append(selection)
    text_widget.insert('1.0', f"Evident ORP: {selection}\n")

def handle_evident_nazev(selection):
    volby_evident_nazev.append(selection)
    text_widget.insert('1.0', f"Evident název: {selection}\n")

def handle_evident_typSubjektu(selection):
    volby_evident_typ.append(selection)
    text_widget.insert('1.0', f"Evident typ subjektu: {selection}\n")

def handle_partner_kraj(selection):
    volby_partner_kraj.append(selection)
    text_widget.insert('1.0', f"Partner kraj: {selection}\n")

def handle_partner_ORP(selection):
    volby_partner_ORP.append(selection)
    text_widget.insert('1.0', f"Partner ORP: {selection}\n")

def handle_partner_nazev(selection):
    volby_partner_nazev.append(selection)
    text_widget.insert('1.0', f"Partner název: {selection}\n")

def handle_partner_typSubjektu(selection):
    volby_partner_typ.append(selection)
    text_widget.insert('1.0', f"Partner typ subjektu: {selection}\n")

def handle_indikator(selection):
    volby_indikator.append(selection)
    text_widget.insert('1.0', f"Indikátor: {selection}\n")

def handle_kod(selection):
    volby_kod.append(selection)
    text_widget.insert('1.0', f"Kód nakládání: {selection}\n")

def handle_rok(selection):
    volby_rok.append(selection)
    text_widget.insert('1.0', f"Rok: {selection}\n")

def handle_druhOdpadu(selection):
    volby_druhOdpadu.append(selection)
    text_widget.insert('1.0', f"Druh odpadu: {selection}\n")

def handle_sloupce(selection):
    volby_sloupce.append(selection)
    text_widget.insert('1.0', f"Sloupec: {selection}\n")

def handle_seskupeni(selection):
    volby_seskupeni.append(selection)
    text_widget.insert('1.0', f"Sloupec: {selection}\n")

def handle_funkce(selection):
    volby_funkce.append(selection)
    text_widget.insert('1.0', f"Vybraný výpočet: {selection}\n")

def format_column(df):
    if 'Odpad_vKg' in df.columns:
        df['Odpad_vKg'] = df['Odpad_vKg'].apply(lambda x: locale.format_string("%d", x, grouping=True))
    if 'Pocet_Obyvatel' in df.columns:
        df['Pocet_Obyvatel'] = df['Pocet_Obyvatel'].apply(lambda x: locale.format_string("%d", x, grouping=True))
    if 'OdpadNaPocetObyv' in df.columns:
        df['OdpadNaPocetObyv'] = df['OdpadNaPocetObyv'].apply(lambda x: locale.format_string("%0.3f", x, grouping=True))

def show_map():
    global vyber_dat_vysledek
    if vyber_dat_vysledek is not None:
        # Načtení souboru
        gdf_kraje = gpd.read_file('kraje-simple.json', encoding='utf-8')
        gdf_orp = gpd.read_file('orp-simple.json', encoding='utf-8')
        gdf_obce = gpd.read_file('obce-simple.json', encoding='utf-8')

        if subjekt_radiobut_value.get() == '1':
            subjekt = 'Evident'
        elif subjekt_radiobut_value.get() == '2':
            subjekt = 'Partner'

        if uzemi_radiobut_value.get() == '1':
            uzemi = 'Kraj_Cislo'
            mapa = gdf_kraje
            json_column = 'NUTS3_KOD'
        elif uzemi_radiobut_value.get() == '2':
            uzemi = 'ORP_Cislo'
            mapa = gdf_orp
            json_column = 'ORP_Cislo'
        elif uzemi_radiobut_value.get() == '3':
            uzemi = 'ZUJ_Cislo'
            json_column = 'KOD'
            mapa = gdf_obce

        if sloupecHodnoty_radiobut_value.get() == '1':
            hodnoty = 'OdpadNaObyv_g'
        elif sloupecHodnoty_radiobut_value.get() == '2':
            hodnoty = 'Odpad_vKg'
        print("stisk tlačítka: ")
        print(hodnoty)
        nazev_sloupce = f'{subjekt}_{uzemi}'
        nazev_sloupce_lexikon = uzemi
        '''    
        odpad_data = hn.seskupeni_dat_po_sloupcich(vyber_dat_vysledek,'Odpad_vKg',nazev_sloupce)
        odpad_data['Odpad_vKg'] = odpad_data['Odpad_vKg'].abs()
        print(odpad_data)
        pocetObyv_data = hn.seskupeni_dat_po_sloupcich(hn.LexikonObci,'Pocet_Obyvatel',nazev_sloupce)
        print(pocetObyv_data)
        # Sloučení df odpad_data a pocetObyv_data podle proměnné nazev_sloupce
        mapa_data = pocetObyv_data.merge(odpad_data,left_on=nazev_sloupce, right_on = nazev_sloupce,how='left')
        mapa_data['Odpad_vKg'] = mapa_data['Odpad_vKg'].fillna(value=0)
        print(mapa_data)
        # Výpočet odpad na obyvatele
        mapa_data = hn.vlozit_sloupec_prepocet_odpadNaPocetObyv(mapa_data)
        print(mapa_data)
        '''
        mapa_data = hn.odpadNaObyvatele_g(vyber_dat_vysledek,nazev_sloupce,hn.LexikonObci,nazev_sloupce_lexikon)
        print("výtisk po mé funkci")
        print(mapa_data)
        bezNul_data = mapa_data[mapa_data['Odpad_vKg'] > 0]
        print("data frame bez nul")
        print(bezNul_data)
        # zaokrouhlení sloupce hodnoty ('OdpadNaObyvatele') na celá čísla nahoru
        bezNul_data[hodnoty] = bezNul_data[hodnoty].apply(np.ceil).astype(int)
        print("data frame bez nul zaokr")
        print(bezNul_data)
        #Sloučení df kraje_produkce s geometrickým df podle názvu kraje
        gdf_merged = mapa.merge(mapa_data, left_on=json_column, right_on=nazev_sloupce,how='left')
        gdf_merged.to_csv('gdf_merged.csv', index=False) # pak vymazat
        print(gdf_merged)
        # nahrazení chybějících hodnot v datovém rámci gdf_merged
        gdf_merged[hodnoty] = gdf_merged[hodnoty].fillna(value=-1)
        # zaokrouhlení sloupce hodnoty ('OdpadNaObyvatele') na celá čísla nahoru
        gdf_merged[hodnoty] = gdf_merged[hodnoty].apply(np.ceil).astype(int)

        bezNul_data = bezNul_data.sort_values(by=hodnoty, ascending=True)

        gdf_merged.to_csv('gdf_merged.csv', index=False) # pak vymazat
        
        print("tisk gdf merged")
        print(gdf_merged)
        # určení kvantilů
        q1 = bezNul_data[hodnoty].quantile(0.15)
        q3 = bezNul_data[hodnoty].quantile(0.85)
        print(q1)
        print(q3)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr      
        print("lower bound: ")
        print(lower_bound)
        print("upper bound: ")
        print(upper_bound)
        outliers = bezNul_data[(bezNul_data[hodnoty] < lower_bound) | (bezNul_data[hodnoty] > upper_bound)]
        print("tisk outliers")
        print(outliers)
        pocet_odlehlych_hodnot = len(outliers)
        if pocet_odlehlych_hodnot > 0:
            upper_limit_scale = upper_bound = round(upper_bound,0)
        else:
            upper_limit_scale = bezNul_data[hodnoty].max()
        #upper_bound = 10
        print("upper limit scale")
        print(upper_limit_scale)
        cmap = plt.cm.get_cmap('viridis')
        cmap = cmap.reversed()
        cmap.set_over('black')
        cmap.set_under('white')

        # nastavení rozsahu hodnot pro barevnou mapu
        vmin = 0
        vmax = upper_limit_scale  # nastavíme max hodnotu v hodnotách jako vrchol legendy
        norm = plt.Normalize(vmin=vmin, vmax=vmax)

        fig, ax = plt.subplots()

        # použití metody plot() pro zobrazení mapy s barvami krajů podle hodnot ze sloupce dle uživatelské volby  v novém datovém rámci gdf_merged
        gdf_merged.plot(column = hodnoty,
                        cmap = cmap,
                        ax=ax,
                        norm=norm,
                        legend = True,
                        edgecolor='black',
                        linewidth=0.5,
                        alpha=0.8,
                        )
        if len(gdf_merged[gdf_merged[hodnoty] == 0]) > 0:
            text_bila_mista = 'Bílá místa znázorňují území, která neevidovala tento druh odpadu. '
        else: text_bila_mista = ''
        if pocet_odlehlych_hodnot > 0:
            text_odlehle_hodnoty = 'Černě jsou zvýrazněny\n odlehlé hodnoty nad {} kg'
        else: text_odlehle_hodnoty = ''
        # popisky názvů míst nezobrazovat na úrovni ZÚJ
        if uzemi_radiobut_value.get() != '3':
            for index, row in gdf_merged.iterrows():
              plt.annotate(text=row['NAZEV'], 
                      xy=row['geometry'].centroid.coords[0], 
                      horizontalalignment='center',
                      color='black',
                      fontsize=5)
              
        text_widget.delete("1.0","end")
        text_widget.insert(END, "Data pro vznik mapy:\n\n ")
        text_widget.insert(END, bezNul_data)
        # Přidání textu s hodnotou vmax
        formatted_upper_bound = '{:,.0f}'.format(upper_bound).replace(',', ' ')
        ax.annotate(f'{text_odlehle_hodnoty}\n{text_bila_mista}'.format(formatted_upper_bound), xy=(0.95, 0.1), xycoords='axes fraction', ha='right', va='center')
        
        def create_title_from_list(my_list):
            title = ""
            for item in my_list:
                title = title + str(item) + ", "
            title = title[:-2]  # odstranění posledních dvou znaků
            return title
        
        if sloupecHodnoty_radiobut_value.get() == '1':
            hodnoty_text = 'Mapa zobrazuje hodnoty: v g na obyvatele '
        elif sloupecHodnoty_radiobut_value.get() == '2':
            hodnoty_text = 'Mapa zobrazuje hodnoty: odpad v kg '
        if subjekt_radiobut_value.get() == '1':
            subjekt_text = 'Nakládání s odpady z pohledu: evidentů, '
        elif subjekt_radiobut_value.get() == '2':
            subjekt_text = 'Nakládání s odpady z pohledu: partnerů, '
        if uzemi_radiobut_value.get() == '1':
            uzemi_text = 'shrnutí na úrovni: krajů '
        elif uzemi_radiobut_value.get() == '2':
            uzemi_text = 'shrnutí na úrovni: ORP '
        elif uzemi_radiobut_value.get() == '3':
            uzemi_text = 'shrnutí na úrovni: ZÚJ '
        if volby_evident_kraj:
            text = create_title_from_list(volby_evident_kraj)
            evident_kraj = f' evident kraj: {text}, '
        else: evident_kraj= ''
        if volby_evident_ORP:
            text = create_title_from_list(volby_evident_ORP)
            evident_ORP = f' evident ORP: {text}, '
        else: evident_ORP= ''
        if volby_partner_kraj:
            text = create_title_from_list(volby_partner_kraj)
            partner_kraj = f' partner kraj: {text}, '
        else: partner_kraj= ''
        if volby_partner_ORP:
            text = create_title_from_list(volby_partner_ORP)
            partner_ORP = f' partner ORP: {text}, '
        else: partner_ORP= ''
        if volby_druhOdpadu:
            text = create_title_from_list(volby_druhOdpadu)
            odpad = f' Druh odpadu: {text}, '
        else: odpad= ''
        if volby_indikator:
            text = create_title_from_list(volby_indikator)
            identifikator = f' Indikátor: {text} '
        else: identifikator = ''
        if volby_kod:
            text = create_title_from_list(volby_kod)
            nakladani = f' Kód způsobu nakládání: {text} '
        else: nakladani = ''
        if volby_rok:
          text = create_title_from_list(volby_rok)
          obdobi = f' Období: {text} '
        else: obdobi = ''

        plt.title(f'{hodnoty_text}\n{subjekt_text}{uzemi_text}\n{evident_kraj}{evident_ORP}{partner_kraj}{partner_ORP}\n{odpad}{identifikator}{nakladani}{obdobi}')
        plt.show()
    else:
        messagebox.showwarning("Chyba", "Nebyla nalezena žádná data k zobrazení v mapě.")

def sumarizace():
    global vysledek_excel
    global vyber_dat_vysledek
    if vyber_dat_vysledek is not None:
        vysledek = vyber_dat_vysledek
        if volby_evident_kraj:
            vysledek=hn.summary_stat_parametr(vysledek,'Evident_ORP_Nazev',hn.list_kraj_orp[volby_evident_kraj],'Odpad_vKg')

            vysledek_excel = vysledek

            text_widget.delete("1.0","end")
            text_widget.insert("1.0",f"ZÁKLADNÍ STATISTICKÉ VELIČINY PRO ORP v kraji: {volby_evident_kraj}\n {vysledek}\n")
        elif volby_evident_ORP:
            vysledek=hn.summary_stat_parametr(vysledek,'Evident_ZUJ_Nazev',hn.list_orp_zuj[volby_evident_ORP],'Odpad_vKg')

            text_widget.delete("1.0","end")
            text_widget.insert("1.0",f"ZÁKLADNÍ STATISTICKÉ VELIČINY PRO ZUJ v ORP: {volby_evident_ORP}\n {vysledek}\n")
        else:
            text_widget.delete("1.0","end")
            text_widget.insert("1.0", "Výběr nesplnil žádný záznam.\n")  
    else:
        messagebox.showwarning("Chyba", "Nebyla nalezena žádná data k zobrazení.")

# Test odlehlé hodnoty
def odlehle_hodnoty():
    global vysledek_excel
    global vyber_dat_vysledek
    if vyber_dat_vysledek is not None:
        vysledek = vyber_dat_vysledek
    
        pocet_hodnot = len(vysledek['Odpad_vKg'])
        # Výpočet IQR metody
        q1, q3 = np.percentile(vysledek['Odpad_vKg'], [25, 75])
        iqr = q3 - q1

        # Určení odlehlých hodnot
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = vysledek[(vysledek['Odpad_vKg'] < lower_bound) | (vysledek['Odpad_vKg'] > upper_bound)]
        pocet_odlehlych_hodnot_lower=len(vysledek[(vysledek['Odpad_vKg'] < lower_bound)])
        pocet_odlehlych_hodnot_upper=len(vysledek[(vysledek['Odpad_vKg'] > upper_bound)])
        pocet_odlehlych_hodnot = len(outliers)

        vysledek_excel = outliers

        if not volby_sloupce:
            outliers = outliers.loc[:,volby_sloupce_univ]
        else: outliers = outliers.loc[:,volby_sloupce]
        if not outliers.empty:
            format_column(outliers) 

        # Výsledky testu
        if len(outliers) > 0:
            vysledek_testu_text = f"V datovém vzorku o {pocet_hodnot} hodnotách existuje {pocet_odlehlych_hodnot} odlehlých hodnot ({pocet_odlehlych_hodnot_lower}, {pocet_odlehlych_hodnot_upper}):\n\n{outliers.to_string(index=False, justify='right')}"
            print(outliers)

        else:
            vysledek_testu_text = f"Odlehlé hodnoty v datovém vzorku o {pocet_hodnot} hodnotách nejsou zjištěny."
        
        text_widget.delete("1.0","end")
        text_widget.insert(END, "DIXONŮV TEST PRO ODHALENÍ ODLEHLÝCH HODNOT:\n\n ")
        text_widget.insert(END, vysledek_testu_text)
    else:
        messagebox.showwarning("Chyba", "Nebyla nalezena žádná data k zobrazení.")

# Sloučení podmínek výběru dle kritérií, výběr evidenta, výběr partnera
#Platný
def vyber_evident_partner_kriteria():
    global vysledek_excel
    global vyber_dat_vysledek
    vysledek_evident = hn.vyber_subjektu(hn.Zdrojovy_Kody_Mnozstvi,'Evident_Kraj_Nazev',volby_evident_kraj,'Evident_ORP_Nazev',volby_evident_ORP,'Evident_ZUJ_Nazev',volby_evident_nazev,'Evident_TypSubjektu',volby_evident_typ)

    vysledek_evidentApartner = hn.vyber_subjektu(vysledek_evident,'Partner_Kraj_Nazev',volby_partner_kraj,'Partner_ORP_Nazev',volby_partner_ORP,'Partner_ZUJ_Nazev',volby_partner_nazev,'Partner_TypSubjektu',volby_partner_typ)

    vysledek = hn.vyber_kriterii(vysledek_evidentApartner,'Indikator',volby_indikator,'Kod',volby_kod,'Druh_Odpadu',volby_druhOdpadu,'Rok',volby_rok)

    vysledek_excel = vysledek
    vyber_dat_vysledek = vysledek
    if not volby_sloupce:
        vysledek = vysledek.loc[:,volby_sloupce_univ]
    else: vysledek = vysledek.loc[:,volby_sloupce]
    if not vysledek.empty:
        format_column(vysledek)

        pocet_polozek = len(vysledek.index)
        text_widget.delete("1.0","end")
        text_widget.insert("1.0",f"VÝPIS FILTROVANÝCH DAT DLE VÝBĚRU EVIDENTA, PARTNERA A KRITÉRIÍ ({pocet_polozek} položek):\n\n {vysledek.to_string(index=False, justify='right')}\n")
    else:
        text_widget.delete("1.0","end")
        text_widget.insert("1.0", "Výběr nesplnil žádný záznam.\n")        

def seskupeni_dat():
    global vysledek_excel
    global vyber_dat_vysledek
    if vyber_dat_vysledek is not None:
        vysledek = vyber_dat_vysledek
        list_seskupeni = volby_seskupeni

        if not volby_sloupce:
            vysledek = vysledek.loc[:,volby_sloupce_univ]
        else: vysledek = vysledek.loc[:,volby_sloupce]
        if not list_seskupeni:
            list_seskupeni = volby_seskupeni_univ
        else: list_seskupeni = volby_seskupeni
        if not vysledek.empty:
            if 'Odpad_vKg' in vysledek.columns:
                #grouping
                vysledek = hn.seskupeni_dat_seznam_sloupcu(vysledek,['Odpad_vKg','Pocet_Obyvatel'],list_seskupeni)
                vysledek_excel = vysledek
                format_column(vysledek)
                pocet_polozek = len(vysledek.index)
                text_widget.delete("1.0","end")
                text_widget.insert("1.0",f"SESKUPENÍ DAT DLE 'Odpad_vKg' ({pocet_polozek} položek):\n\n {vysledek.to_string(index=False, justify='right')}\n")
        else:
            text_widget.delete("1.0","end")
            text_widget.insert("1.0","Výběr nesplnil žádný záznam. \n")
    else:
        messagebox.showwarning("Chyba", "Nebyla nalezena žádná data k zobrazení.")

def graf_xyBodovy():
    global vyber_dat_vysledek
    if vyber_dat_vysledek is not None:
        vysledek = vyber_dat_vysledek
        fig,ax = plt.subplots()  
        colors = ['red', 'blue', 'green', 'orange'] #seznam barev pro scatter grafy
        for i,odpad in enumerate(volby_druhOdpadu):
            data = vysledek[vysledek['Druh_Odpadu'] == odpad]
            ax.scatter(data['Odpad_vKg'],data['Pocet_Obyvatel'],color=colors[i],label=odpad)
        ax.legend()
        ax.set_xlabel("Množství odpadu v kg")
        ax.set_ylabel("Počet obyvatel")
        plt.show()
    else:
        messagebox.showwarning("Chyba", "Nebyla nalezena žádná data k zobrazení.")

def vykonat_funkci():
    vybrana_funkce=funkce_combo.get()
    text_widget.delete('1.0','end')
    text_widget.insert("end",f"Vybrána funkce: {vybrana_funkce.upper()}\n")

    if vybrana_funkce in funkce_dict:
        funkce_dict[vybrana_funkce]()
    else:
        text_widget.insert("end","Nejprve vyberte data a poté vyberte funkci ze seznamu.")

def aktivovat_vyber():
    global vyber_dat_stisknuto
    vyber_dat_stisknuto = True
    funkce_combo.configure(state='readonly')
    saveXlsx_button.configure(state='normal')
    mapa_button.configure(state='normal')
    funkce_button.configure(state='normal')
    
def vyber_dat():
    aktivovat_vyber()
    vyber_evident_partner_kriteria()

def vytisknout_volby():
    """Tato funkce se spustí po stisknutí tlačítka Uložit volby"""
    text_widget.delete('1.0','end')
    text_widget.insert("end",'ZADANÉ VOLBY: \n\n')
    text_widget.insert("end",f"Vybraný výpočet: {volby_funkce}\n\n")

    text_widget.insert("end",f"Sloupce na výstup: {volby_sloupce}\n\n")
    text_widget.insert("end",f"Seskupení podle sloupců: {volby_seskupeni}\n\n")

    text_widget.insert("end",f"Indikátor: {volby_indikator}\n")
    text_widget.insert("end",f"Kód nakládání: {volby_kod}\n")
    text_widget.insert("end",f"Druh odpadu: {volby_druhOdpadu}\n")
    text_widget.insert("end",f"Rok: {volby_rok}\n\n")

    text_widget.insert("end",f"Evident kraj: {volby_evident_kraj}\n")
    text_widget.insert("end",f"Evident ORP: {volby_evident_ORP}\n")
    text_widget.insert("end",f"Evident ZÚJ: {volby_evident_nazev}\n")
    text_widget.insert("end",f"Evident typ subjektu: {volby_evident_typ}\n\n")

    text_widget.insert("end",f"Partner kraj: {volby_partner_kraj}\n")
    text_widget.insert("end",f"Partner ORP: {volby_partner_ORP}\n")
    text_widget.insert("end",f"Partner ZÚJ: {volby_partner_nazev}\n")
    text_widget.insert("end",f"Partner typ subjektu: {volby_partner_typ}\n\n")
"""Tato funkce se spustí po stisknutí tlačítka Vymazat volby"""
def vymazat_volby():
    text_widget.delete('1.0','end')
    volby_evident_kraj.clear()
    volby_evident_ORP.clear()
    volby_evident_nazev.clear()
    volby_evident_typ.clear()
    evident_kraj_combo.current(0)
    evident_ORP_combo.current(0)
    evident_nazev_combo.current(0)
    evident_typSubjektu_combo.current(0)

    volby_partner_kraj.clear()
    volby_partner_ORP.clear()
    volby_partner_nazev.clear()
    volby_partner_typ.clear()
    partner_kraj_combo.current(0)
    partner_ORP_combo.current(0)
    partner_nazev_combo.current(0)
    partner_typSubjektu_combo.current(0)

    volby_seskupeni.clear()
    volby_sloupce.clear()
    volby_funkce.clear()
    volby_indikator.clear()
    volby_kod.clear()
    volby_druhOdpadu.clear()
    volby_rok.clear()
    seskupit_combo.current(0)
    sloupce_combo.current(0)
    funkce_combo.current(0)
    indikator_combo.current(0)
    kod_combo.current(0)
    druhOdpadu_combo.current(0)
    rok_combo.current(0)

    funkce_combo.configure(state="disabled")
    saveXlsx_button.configure(state='disabled')
    mapa_button.configure(state='disabled')
    funkce_button.configure(state='disabled')



# Funkce pro uložení obsahu textového widgetu do xlsx souboru
def save_to_xlsx():
    global vysledek_excel
    if vysledek_excel is not None:
        file_name = filedialog.asksaveasfilename(defaultextension='.xlsx')
        if file_name:
            vysledek_excel.to_excel(file_name, index=True, header=True)
            messagebox.showinfo("Uloženo", "Data byla uložena do Excelu.")
    else:
        messagebox.showwarning("Chyba", "Nebyla nalezena žádná data k uložení.")


# Slovník, kde klíče jsou názvy funkcí a hodnoty jsou samotné funkce
funkce_dict = {
    "Sumarizace": sumarizace,
    "Zjištění odlehlých hodnot": odlehle_hodnoty,
    "Seskupení dat": seskupeni_dat,
    "XY Bodový graf": graf_xyBodovy,
    
}       

root = Tk()
root.title('Data o odpadech')
root.geometry("1000x750")
style = ThemedStyle(root)
# style.set_theme('elegance')
bg = PhotoImage(file="green_forest.png")
bg_label = Label(root,image=bg)
bg_label.place (x=0, y=0, relwidth=1, relheight=1)

# Vytvoření frame

left_frame = Frame(root)
left_frame.pack(side=LEFT,padx=20, pady=20)

right_frame = Frame(root)
right_frame.pack(side=TOP, padx=20, pady=20)


# Vytvoření frame pro Evident a Partner
funkcni_frame = tk.LabelFrame(left_frame, padx=10, pady=10)
funkcni_frame.configure(borderwidth=0, highlightthickness=0)
funkcni_frame.pack(side=tk.TOP, pady=(20, 0))

evident_frame = tk.LabelFrame(left_frame, text="Evident", padx=10, pady=10)
evident_frame.pack(side=tk.TOP, pady=(20, 0))

partner_frame = tk.LabelFrame(left_frame, text = "Partner", padx=10, pady=10)
partner_frame.pack(side=tk.TOP, pady=(20, 0))


# Tlačítko uložit volby
ulozit_button = tk.Button(funkcni_frame, text="Zobrazit volby",command=vytisknout_volby)
ulozit_button.pack(side=tk.TOP, pady=(20,0))

# Tlačítko vymazat volby
vymazat_button = tk.Button(funkcni_frame, text="Smazat volby",command=vymazat_volby)
vymazat_button.pack(side=tk.TOP, pady = (20,0))

# EVIDENT frame
# Evident kraj combobox
evident_kraj_label = tk.Label(evident_frame, text="Kraj")
evident_kraj_label.pack(side=tk.TOP)
options = hn.u_list_evident_kraj
evident_kraj_combo=ttk.Combobox(evident_frame, value=options)
evident_kraj_combo.bind("<<ComboboxSelected>>", lambda event: handle_evident_kraj(evident_kraj_combo.get()))
evident_kraj_combo.current(0)
evident_kraj_combo.pack(side=tk.TOP)

# Evident ORP
evident_ORP_label = tk.Label(evident_frame, text="ORP")
evident_ORP_label.pack(side=tk.TOP)
options = hn.u_list_evident_orp
evident_ORP_combo = ttk.Combobox(evident_frame, value=options)
evident_ORP_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_evident_ORP(evident_ORP_combo.get()))
evident_ORP_combo.current(0)
evident_ORP_combo.pack()

# Evident název (ZÚJ)
evident_nazev_label = tk.Label(evident_frame, text="ZÚJ")
evident_nazev_label.pack(side=tk.TOP)
options = hn.u_list_evident_zuj_nazev
evident_nazev_combo = ttk.Combobox(evident_frame, value=options)
evident_nazev_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_evident_nazev(evident_nazev_combo.get()))
evident_nazev_combo.current(0)
evident_nazev_combo.pack()

# Evident typ subjektu
evident_typSubjektu_label = tk.Label(evident_frame, text="Typ subjektu")
evident_typSubjektu_label.pack(side=tk.TOP)
options = hn.u_list_evident_typ
evident_typSubjektu_combo = ttk.Combobox(evident_frame, value=options)
evident_typSubjektu_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_evident_typSubjektu(evident_typSubjektu_combo.get()))
evident_typSubjektu_combo.current(0)
evident_typSubjektu_combo.pack()


# PARTNER frame

# Partner kraj combobox (více možností)
partner_kraj_label = tk.Label(partner_frame, text="Kraj")
partner_kraj_label.pack(side=tk.TOP)
options = hn.u_list_partner_kraj
partner_kraj_combo=ttk.Combobox(partner_frame, value=options)
partner_kraj_combo.bind("<<ComboboxSelected>>", lambda event: handle_partner_kraj(partner_kraj_combo.get()))
partner_kraj_combo.current(0)
partner_kraj_combo.pack()

# Partner ORP
partner_ORP_label = tk.Label(partner_frame, text="ORP")
partner_ORP_label.pack(side=tk.TOP)
options = hn.u_list_partner_orp
partner_ORP_combo = ttk.Combobox(partner_frame, value=options)
partner_ORP_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_partner_ORP(partner_ORP_combo.get()))
partner_ORP_combo.current(0)
partner_ORP_combo.pack()

# Partner název (ZÚJ)
partner_nazev_label = tk.Label(partner_frame, text="ZÚJ")
partner_nazev_label.pack(side=tk.TOP)
options = hn.u_list_partner_zuj_nazev
partner_nazev_combo = ttk.Combobox(partner_frame, value=options)
partner_nazev_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_partner_nazev(partner_nazev_combo.get()))
partner_nazev_combo.current(0)
partner_nazev_combo.pack()

# Partner typ subjektu
partner_typSubjektu_label = tk.Label(partner_frame, text="Typ subjektu")
partner_typSubjektu_label.pack(side=tk.TOP)
options = hn.u_list_partner_typ
partner_typSubjektu_combo = ttk.Combobox(partner_frame, value=options)
partner_typSubjektu_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_partner_typSubjektu(partner_typSubjektu_combo.get()))
partner_typSubjektu_combo.current(0)
partner_typSubjektu_combo.pack()



# RIGHT frame (parametry)

# Indikátor
indikator_label = tk.Label(right_frame, text="Indikátor")
indikator_label.grid(row=0, column=0)
options = hn.u_list_indikator
indikator_combo = ttk.Combobox(right_frame, value=options)
indikator_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_indikator(indikator_combo.get()))
indikator_combo.current(0)
indikator_combo.grid(row=1, column=0,padx=20, pady=0)
# Kód nakládání
kod_label = tk.Label(right_frame, text="Kód nakládání")
kod_label.grid(row=2, column=0)
options = hn.u_list_kod
kod_combo = ttk.Combobox(right_frame, value=options)
kod_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_kod(kod_combo.get()))
kod_combo.current(0)
kod_combo.grid(row=3, column=0,padx=20, pady=0)
# Druh odpadu
druhOdpadu_label= tk.Label(right_frame, text="Druh odpadu")
druhOdpadu_label.grid(row=0, column=1)
options = hn.u_list_druhOdpadu
druhOdpadu_combo = ttk.Combobox(right_frame, value=options)
druhOdpadu_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_druhOdpadu(druhOdpadu_combo.get()))
druhOdpadu_combo.current(0)
druhOdpadu_combo.grid(row=1, column=1,padx=20, pady=0)
# Rok
rok_label= tk.Label(right_frame, text="Rok")
rok_label.grid(row=2, column=1)
options = hn.u_list_rok
rok_combo = ttk.Combobox(right_frame, value=options)
rok_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_rok(rok_combo.get()))
rok_combo.current(0)
rok_combo.grid(row=3, column=1,padx=20, pady=0)


# Volba sloupečků pro zobrazení ve výstupu
sloupce_label= tk.Label(right_frame, text="Volba sloupců na výstup")
sloupce_label.grid(row=0, column=2, padx=20, pady=0)
options = hn.u_list_column_names
sloupce_combo = ttk.Combobox(right_frame, value=options, width = 25)
sloupce_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_sloupce(sloupce_combo.get()))
sloupce_combo.current(0)
sloupce_combo.grid(row=1, column=2,padx=20, pady=0)

# Volba sloupečků podle kterých seskupovat
seskupit_label= tk.Label(right_frame, text="Sloupce k seskupení")
seskupit_label.grid(row=2, column=2, padx=20, pady=0)
options = hn.u_list_column_names
seskupit_combo = ttk.Combobox(right_frame, value=options, width = 25)
seskupit_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_seskupeni(seskupit_combo.get()))
seskupit_combo.current(0)
seskupit_combo.grid(row=3, column=2,padx=20, pady=0)

# Talčítko pro výběr dat. Zavolá se funkce evident_partner_kriteria
vyber_dat_stisknuto = False
vyber_dat_button=tk.Button(right_frame, text="Výběr dat",command=vyber_dat, width=25, bg="#CCFFCC")
vyber_dat_button.grid(row=1, column=3, padx=20,pady=0)

# Seznam funkcí
funkce_label= tk.Label(right_frame, text="Funkce")
funkce_label.grid(row=2, column=3, padx=20, pady=0)
options = ['','Sumarizace','Zjištění odlehlých hodnot', 'Seskupení dat','XY Bodový graf']
funkce_combo = ttk.Combobox(right_frame, value=options, state="disabled", width=25)
funkce_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_funkce(funkce_combo.get()))
funkce_combo.current(0)
funkce_combo.grid(row=3, column=3,padx=20, pady=0)

# Talčítko pro spuštění funkce
funkce_button=tk.Button(right_frame, text="Spuštění funkce", state="disabled", command=vykonat_funkci, width=15)
funkce_button.grid(row=3, column=4, padx=20,pady=0)

# Funkce
saveXlsx_button = tk.Button(right_frame,text="Uložit do xlsx",state="disabled", command=save_to_xlsx, width=15)
saveXlsx_button.grid(row=1, column=4, padx=20, pady=0)
# Funkce
mapa_button = tk.Button(right_frame,text="Zobrazit mapu", state="disabled",command=show_map)
mapa_button.grid(row=1, column=6, padx=20, pady=0)

# Proměnné pro radiobutton
subjekt_radiobut_value = tkinter.StringVar()
subjekt_radiobut_value.set('1')

uzemi_radiobut_value = tkinter.StringVar()
uzemi_radiobut_value.set('1')

sloupecHodnoty_radiobut_value = tkinter.StringVar()
sloupecHodnoty_radiobut_value.set('1')

# Vytvoření radiobuttons
evident_radiobut = tkinter.Radiobutton(right_frame, text="Mapa evidentů", variable=subjekt_radiobut_value, value="1")
evident_radiobut.grid(row=0, column=7, padx=20, pady=0, sticky="W")
partner_radiobut = tkinter.Radiobutton(right_frame, text="Mapa partnerů", variable=subjekt_radiobut_value, value="2")
partner_radiobut.grid(row=1, column=7, padx=20, pady=0, sticky="W")

kraj_radiobut = tkinter.Radiobutton(right_frame, text="Úroveň krajů", variable=uzemi_radiobut_value, value="1")
kraj_radiobut.grid(row=3, column=7, padx=20, pady=0, sticky="W")
ORP_radiobut = tkinter.Radiobutton(right_frame, text="Úroveň ORP", variable=uzemi_radiobut_value, value="2")
ORP_radiobut.grid(row=4, column=7, padx=20, pady=0, sticky="W")
ZUJ_radiobut = tkinter.Radiobutton(right_frame, text="Úroveň ZÚJ", variable=uzemi_radiobut_value, value="3")
ZUJ_radiobut.grid(row=5, column=7, padx=20, pady=0, sticky="W")

NaPocObyv_radiobut = tkinter.Radiobutton(right_frame, text="Kg na obyvatele", variable=sloupecHodnoty_radiobut_value, value="1")
NaPocObyv_radiobut.grid(row=3, column=6, padx=20, pady=0, sticky="W")
MnozstviKg_radiobut = tkinter.Radiobutton(right_frame, text="Odpad_vKg", variable=sloupecHodnoty_radiobut_value, value="2")
MnozstviKg_radiobut.grid(row=4, column=6, padx=20, pady=0, sticky="W")


# Vytvoření Text Widget a Scroollbar
text_widget = tk.Text(root)
y_scrollbar = tk.Scrollbar(root, command=text_widget.yview)
x_scrollbar = tk.Scrollbar(root, command=text_widget.xview,orient=tk.HORIZONTAL)

# Připojení Scrollbar k Text Widget
text_widget.config(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

root.mainloop()