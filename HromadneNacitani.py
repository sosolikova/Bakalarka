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
    'ORP_Kod':  'string'
}
dtypes_odpady= {
    'Evident':              'string',
    'Evident_A':            'string',
    'Evident_TypSubjektu':  'string',
    'Evident_Nazev':        'string',
    'Evident_Nazev_A':      'string',
    'Evident_Kraj':         'string',
    'Partner':              'string',
    'Partner_A':            'string',
    'Partner_TypSubjektu':  'string',
    'Partner_Nazev':        'string',
    'Partner_Nazev_A':      'string',
    'Partner_Kraj':         'string',
    'Kod':                  'string',
    'Indikator':            'string',
    'Mnozstvi':             'float'
}

'Funkce pro načtení dat z CSV do DataFrame'
def load_csv_type_conversion(filename, dtypes):
    df = pd.read_csv(filename, delimiter=';', decimal=',',dtype = dtypes)
    return df

def load_files_to_df(directory,extension,dtypes,column_name):
    files = [file for file in os.listdir(directory) if file.endswith(extension)]

    df = pd.DataFrame()

    for file in files:
        filepath = os.path.join(directory, file)
        data = pd.read_csv(filepath,delimiter=';', decimal=',', usecols = None, dtype=dtypes)

        filename = os.path.splitext(file)[0]
        data[column_name] = filename
        df = df.append(data)
    return df

Zdrojovy = load_files_to_df('Data','.csv',dtypes_odpady,'Druh_Odpadu')
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
def merge_left(df1, df2, on_columns):
    merged_df = pd.merge(df1, df2, on=on_columns, how = 'left')
    return merged_df

Zdrojovy_Kody = merge_left(Zdrojovy,Kody,'Kod')
Funkce.save_dataframe_to_csv(Zdrojovy_Kody,'Zdrojovy_Kody')
print('______-------Zdrojovy_Kody----______')
Zdrojovy_Kody.info()

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
Zdrojovy_kody_mnozstvi_group = group_data_by_columns(Zdrojovy_kody_mnozstvi,'ZmenaMnozstvi','Druh_Odpadu','Evident','Evident_TypSubjektu')
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

'Funkce pro kontrolu, ze u kazde ZUJ vyjde bilance <-1 nebo >1'
def filter_sum_after_grouping(grouped_data, column):
    filtered_data = grouped_data[grouped_data[column] > 1] | grouped_data[grouped_data[column] < -1].reset_index()
    return filtered_data
Zdrojovy_kody_mnozstvi_group_nevyhov_1 = filter_sum_after_grouping(Zdrojovy_kody_mnozstvi_group,'ZmenaMnozstvi')
Funkce.save_dataframe_to_csv(Zdrojovy_kody_mnozstvi_group_nevyhov_1,'Zdrojovy_kody_mnozstvi_group_nevyhov_1')

if not Zdrojovy_kody_mnozstvi_group_nevyhov_1.empty:
    print(f"Pocet ZUJ, které mají rocni zuctovani > 1 Kg nebo < -1 Kg: {Zdrojovy_kody_mnozstvi_group_nevyhov_1.shape[0]}")
    print(Zdrojovy_kody_mnozstvi_group_nevyhov_1)
else: 
    print('Zadna ZUJ nema bilanci rocniho zuctovani v odchylce vetsi nez +/- 1 Kg.')

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
    #print(f'Průměr a medián pro parametr {parametr} = {volba}')
    #print(sort.groupby(parametr)[column_summary].agg([np.mean,np.median]))
    return sort.groupby(parametr)[column_summary].agg([np.mean,np.median])

summary = summary_stat_parametr(Zdrojovy_kody_mnozstvi,'Indikator','Převzetí','ZmenaMnozstvi')

# vytvořit seznam unikátních hodnot ze sloupce
def unique_list(df,column_name):
    u_list = list(df[column_name].unique())
    u_list.insert(0,'-all-') # přidá novou položku "-all-" na pozici 0
    print(f'_________unikatni hodnoty{column_name}___________')
    #print(u_list)
    return u_list

u_list_partner_kraj = unique_list(Zdrojovy,'Partner_Kraj')
u_list_indikator = unique_list(Zdrojovy,'Indikator')
u_list_evident = unique_list(Zdrojovy,'Evident')
u_list_evident_typ = unique_list(Zdrojovy,'Evident_TypSubjektu')
'''
unikatni_indikator = list(Zdrojovy['Indikator'].unique())
print('_________unikatni hodnoty___________')
print(unikatni_indikator)
'''
