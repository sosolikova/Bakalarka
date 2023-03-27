import locale
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import Funkce
import geopandas as gpd

dtypes_nakladani = {
    'Navyseni_Ubytek': 'int'
}
dtypes_zuj = {
    'ZUJ_Kod': 'string',
    'ORP_Kod':  'string',
    'ZUJ_Nazev': 'string',
    'ORP_Nazev': 'string',
    'Kraj_Kod': 'string',
    'Kraj_Nazev': 'string'
}
dtypes_odpady= {
    'Evident_ZUJ_Cislo':    'string',
    'Evident_ZUJ_Nazev':    'string',
    'Evident_ZUJ_Cislo_A':  'string',
    'Evident_ZUJ_Nazev_A':  'string',
    'Evident_ORP_Cislo':    'string',
    'Evident_ORP_Nazev':    'string',
    'Evident_Kraj_Cislo':   'string',
    'Evident_Kraj_Nazev':   'string',
    'Evident_TypSubjektu':  'string',

    'Partner_ZUJ_Cislo':    'string',
    'Partner_ZUJ_Nazev':    'string',
    'Partner_ZUJ_Cislo_A':  'string',
    'Partner_ZUJ_Nazev_A':  'string',
    'Partner_ORP_Cislo':    'string',
    'Partner_ORP_Nazev':    'string',
    'Partner_Kraj_Cislo':   'string',
    'Partner_Kraj_Nazev':   'string',
    'Partner_TypSubjektu':  'string',

    'Kod':                  'string',
    'Indikator':            'string',
    'Mnozstvi':             'float'
}

'Funkce pro načtení dat z CSV do DataFrame'
def load_csv_type_conversion(filename, dtypes):
    df = pd.read_csv(filename, delimiter=';', decimal=',',dtype = dtypes)
    return df

def load_files_to_df(directory,extension,dtypes,column_name,column_year):
    files = [file for file in os.listdir(directory) if file.endswith(extension)]

    df = pd.DataFrame()

    for file in files:
        filepath = os.path.join(directory, file)
        data = pd.read_csv(filepath,delimiter=';', decimal=',', usecols = None, dtype=dtypes)

        filename = os.path.splitext(file)[0]
        data[column_name] = filename.split("_")[0]
        data[column_year] = filename.split("_")[1]

        df = df.append(data)
        df[column_name] = df[column_name].astype(str)
        df[column_year] = df[column_year].astype(str)

    return df

Zdrojovy = load_files_to_df('Data','.csv',dtypes_odpady,'Druh_Odpadu','Rok')
print('________---sloucene soubory ----__________')
print(Zdrojovy)
Funkce.save_dataframe_to_csv(Zdrojovy,'Zdrojovy')
print('______----Zdrojovy----______')
Zdrojovy.info()

def checknull(df):
  check = df.isnull().sum()
  print('_________checknull__________')
  print(check)
  return 

checknull(Zdrojovy)

def je_soucet_nulovy(df):
    check_sum = df.isnull().sum().sum()  # součet všech NaN hodnot v DataFrame
    if check_sum == 0:
        print('Nechybi zadna hodnota')
        return True
    else:
        missing_rows = df[df.isnull().any(axis=1)].index.tolist()  # seznam řádků s chybějícími hodnotami
        print("Indexy radku s chybejicimi hodnotami: ", missing_rows)
        return False

je_soucet_nulovy(Zdrojovy)

Kody = load_csv_type_conversion('Kod_Nakladani.csv',dtypes_nakladani)

'Funkce pro spárování dvou DataFrame'
def merge_left(df1, df2, column1, column2):
    merged_df = pd.merge(df1, df2, left_on=column1,right_on=column2, how = 'left')
    return merged_df
#Funkce pro spárování dvou DataFrame se suffixes'
def merge_left2(df1, df2, column1, column2,suffixes1,suffixes2):
    merged_df = pd.merge(df1, df2, left_on=column1,right_on=column2, how = 'left',suffixes=(suffixes1,suffixes2))
    return merged_df

Zdrojovy_Kody = merge_left(Zdrojovy,Kody,'Kod','Kod')
Funkce.save_dataframe_to_csv(Zdrojovy_Kody,'Zdrojovy_Kody')
print('______-------Zdrojovy_Kody----______')
Zdrojovy_Kody.info()

ZUJ_ORP = load_csv_type_conversion('ZUJ_ORP.csv',dtypes_zuj)
''' Po přejmenování sloupců zdrojových souborů raději zakomentuji 
Zdrojovy_Kody_ORP_Evident = merge_left2(Zdrojovy,ZUJ_ORP,'Evident','ZUJ_Kod','Zdroj','Evident')
Funkce.save_dataframe_to_csv(Zdrojovy_Kody_ORP_Evident,'Zdrojovy_Kody_ORP_Evident')
print('_____--zdrojovy-ZUJ-ORP-Evident_________-')
Zdrojovy_Kody_ORP_Evident.info()

Zdrojovy_Kody_ORP_Partner = merge_left2(Zdrojovy_Kody_ORP_Evident,ZUJ_ORP,'Partner','ZUJ_Kod','_Evident','_Partner')
Funkce.save_dataframe_to_csv(Zdrojovy_Kody_ORP_Partner,'Zdrojovy_Kody_ORP_Partner')
print('_____--zdrojovy-ZUJ-ORP-Partner_________-')
Zdrojovy_Kody_ORP_Partner.info()
'''

'Kontrola sparovani radku'
def check_match (dataframe,column):
    unmatched_row = dataframe[dataframe[column].isnull()]
    if unmatched_row.empty:
        print(f'Ke vsem radkum leve tabulky byly dohledany hodnoty do sloupce {column}')
        return(True, None)
    else: 
        unmatched_row_count = unmatched_row.shape[0]
        print(f'K {unmatched_row_count} radkum nebyla dohledana hodnota do sloupce {column}')
        print(unmatched_row)
        return(False,unmatched_row)

'APLIKACE kontrola sparovani'
check_match(Zdrojovy_Kody,'Navyseni_Ubytek')
    
'Vynásobení Množství * (-1 nebo +1) a převede na Kg vynásobením 1000'
def add_col_multipl(df):
    df.insert(loc=0,column='ZmenaMnozstvi',value=(df['Mnozstvi'] * df['Navyseni_Ubytek']) * 1000)
    return df

'APLIKACE přidání sloupce ZmenaMnozstvi'
Zdrojovy_kody_mnozstvi=add_col_multipl(Zdrojovy_Kody)
Funkce.save_dataframe_to_csv(Zdrojovy_kody_mnozstvi,'Zdrojovy_kody_mnozstvi')
print('______-------Zdrojovy_Kody_mnozstvi----______')
Zdrojovy_kody_mnozstvi.info()

'Grouping DataFrame podle jednoho či více sloupců'
def group_data_by_columns(data, func_column, *group_columns ):
    grouped_data = data.groupby(list(group_columns))[func_column].sum().reset_index()
    return grouped_data

'APLIKACE slouceni podle sloupcu Evident, Evidnet_TypSubjektu, funkce bude na sloupci ZmenaMnozstvi'
Zdrojovy_kody_mnozstvi_group = group_data_by_columns(Zdrojovy_kody_mnozstvi,'ZmenaMnozstvi','Druh_Odpadu','Evident_ZUJ_Cislo','Evident_TypSubjektu')
Funkce.save_dataframe_to_csv(Zdrojovy_kody_mnozstvi_group,'Zdrojovy_kody_mnozstvi_group')

'Funkce pro kontrolu, ze u kazde ZUJ vyjde bilance 0'
def filter_sum_after_grouping(grouped_data, column):
    filtered_data = grouped_data[grouped_data[column] !=0].reset_index()
    return filtered_data
'Funkce ktera vrátí počet řádků df, které se rovnají hodnotě a které se nerovnají'
def count_rows(data,column,value):
    equal_rows = (data[column] == value).sum()
    non_equal_rows = (data[column] != value). sum()
    return equal_rows, non_equal_rows

'APLIKACE kontrola, zda ZUJ vyjde bilance 0'
Zdrojovy_kody_mnozstvi_group_nevyhov_0 = filter_sum_after_grouping(Zdrojovy_kody_mnozstvi_group,'ZmenaMnozstvi')
Funkce.save_dataframe_to_csv(Zdrojovy_kody_mnozstvi_group_nevyhov_0,'Zdrojovy_kody_mnozstvi_group_nevyhov_0')

equal_rows, non_equal_rows = count_rows(Zdrojovy_kody_mnozstvi_group, 'ZmenaMnozstvi', 0)
print(f"Počet ZUJ, které mají roční zúčtování rovno nule: {equal_rows}")
print(f"Počet ZUJ, které roční zúčtování nemají vyrovnané: {non_equal_rows}")



'_____________________'
'Pripojeni tabulky ZUJ_ORP'
"""
'Nacteni tabulky ZUJ_ORP'
ZUJ_ORP = load_csv_type_conversion('ZUJ_ORP.csv',dtypes_zuj)

Zdrojovy_Kody_Mnozstvi_Zuj = merge_left(Zdrojovy_kody_mnozstvi, ZUJ_ORP, 'ZUJ_Kod')

"""
'_________GRAFY____________'
Produkce_and_Prevzeti = Zdrojovy_kody_mnozstvi[(Zdrojovy_kody_mnozstvi['Indikator'] == "Produkce") | (Zdrojovy_kody_mnozstvi['Indikator'] == "Převzetí")]
print('____produkce a prevzeti_______')
print(Produkce_and_Prevzeti.groupby('Indikator')['ZmenaMnozstvi'].agg([np.mean,np.median])) 

def summary_stat_parametr(df,parametr,volba,column_summary):
    sort = df[(df[parametr] == volba)]
    result = sort.groupby(parametr)[column_summary].agg([np.mean,np.median,np.min,np.max])
    result = result.applymap(lambda x: round(x))
    locale.setlocale(locale.LC_ALL, '')
    result = result.applymap(lambda x: locale.format_string('%d', x, grouping=True))
    print(result)
    return result

def summary_stat_parametr(df,parametr,seznam,column_summary):
    if seznam == ["-all-"]:
        sort = df
    else:
      sort = df[(df[parametr].isin(seznam))]
    result = sort.groupby(parametr)[column_summary].agg([np.mean,np.median,np.min,np.max])
    result = result.applymap(lambda x: round(x))
    locale.setlocale(locale.LC_ALL, '')
    result = result.applymap(lambda x: locale.format_string('%d', x, grouping=True))
    print('Výsledek funkce summary_stat_parametr:')
    print(result)
    return result

def summary_stat(df,parametr,column_summary):
    result = df.groupby(parametr)[column_summary].agg([np.mean,np.median,np.min,np.max])
    result = result.applymap(lambda x: round(x))
    locale.setlocale(locale.LC_ALL, '')
    result = result.applymap(lambda x: locale.format_string('%d', x, grouping=True))
    print(result)
    return result

my_list=['Zlínský kraj','Jihomoravský kraj','Jihočeský kraj']
print('Zkouška sortování')
sortovani = Zdrojovy_kody_mnozstvi[Zdrojovy_kody_mnozstvi['Evident_Kraj_Nazev'].isin(my_list)]
result = summary_stat(sortovani,'Evident_Kraj_Nazev','ZmenaMnozstvi')

summary_stat_parametr(Zdrojovy_kody_mnozstvi,'Evident_Kraj_Nazev',my_list,'ZmenaMnozstvi')

# vytvořit seznam unikátních hodnot ze sloupce
def unique_list(df,column_name):
    u_list = list(df[column_name].unique())
    u_list.insert(0,'-all-') # přidá novou položku "-all-" na pozici 0
    u_list.insert(0,'') # přidá novou položku "" na pozici 0
    u_list = sorted(u_list) # seřazení seznamu podle abecedy
    print(f'_________unikatni hodnoty{column_name}___________')
    #print(u_list)
    return u_list


u_list_indikator = unique_list(Zdrojovy,'Indikator')
u_list_kod = unique_list(Zdrojovy,'Kod')
u_list_druhOdpadu = unique_list(Zdrojovy, 'Druh_Odpadu')
u_list_rok = unique_list(Zdrojovy,'Rok')

u_list_evident_kraj = unique_list(Zdrojovy,'Evident_Kraj_Nazev')
u_list_evident_zuj_cislo = unique_list(Zdrojovy,'Evident_ZUJ_Cislo')
u_list_evident_zuj_nazev = unique_list(Zdrojovy,'Evident_ZUJ_Nazev')
u_list_evident_typ = unique_list(Zdrojovy,'Evident_TypSubjektu')
u_list_evident_orp = unique_list(Zdrojovy,'Evident_ORP_Nazev')

u_list_partner_kraj = unique_list(Zdrojovy,'Partner_Kraj_Nazev')
u_list_partner_orp = unique_list(Zdrojovy,'Partner_ORP_Nazev')
u_list_partner_zuj_nazev = unique_list(Zdrojovy,'Partner_ZUJ_Nazev')
u_list_partner_typ = unique_list(Zdrojovy,'Partner_TypSubjektu')
u_list_partner_zuj_cislo = unique_list(Zdrojovy,'Partner_ZUJ_Cislo')





'''
unikatni_indikator = list(Zdrojovy['Indikator'].unique())
print('_________unikatni hodnoty___________')
print(unikatni_indikator)
'''
indikator_select = Zdrojovy_kody_mnozstvi[Zdrojovy_kody_mnozstvi['Kod'] == 'XD1']
print('_____indikator select __________')
print(indikator_select)
indikator_select['ZmenaMnozstvi'].hist(bins=30)
plt.show()

def vyber_subjektu(df,column1,volby1,column2,volby2,column3,volby3):
    vysledek=df[(df[column1].isin(volby1)) | (df[column2].isin(volby2)) | (df[column3].isin(volby3))]
    return vysledek

def vyber_kriterii(df,column1,volby1,column2,volby2,column3,volby3):
    vysledek=df[(df[column1].isin(volby1)) & (df[column2].isin(volby2)) & (df[column3].isin(volby3))]
    return vysledek