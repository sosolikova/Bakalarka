import locale
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd

dtypes_nakladani = {
    'Navyseni_Ubytek': 'int'
}
dtypes_unique_orp = {
    'Kraj_Cislo':     'string',
    'Kraj_Nazev':       'string',
    'ORP_Cislo':     'string',
    'ORP_Nazev':  'string',
    'Pocet_obyvatel':  'int',
}
dtypes_unique_kraj = {
    'Kraj_Cislo':     'string',
    'Kraj_Nazev':       'string',
    'Pocet_obyvatel':  'int',
}
dtypes_zuj = {
    'ZUJ_Kod': 'string',
    'ORP_Kod':  'string',
    'ZUJ_Nazev': 'string',
    'ORP_Nazev': 'string',
    'Kraj_Kod': 'string',
    'Kraj_Nazev': 'string'
}
dtypes_obyvatele = {
    'Kod_Okresu':     'string',
    'Kod_Obce':       'string',
    'Nazev_Obce':     'string',
    'Pocet_Obyvatel':  'int'
}
dtypes_lexikonObci ={
    'ZUJ_Cislo':    'string',
    'ZUJ_Nazev':    'string',
    'ORP_Cislo':  'string',
    'ORP_Nazev':  'string',
    'Kraj_Cislo': 'string',
    'Kraj_Nazev': 'string',
    'Pocet_Obyvatel':     'int'
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

'Funkce pro uložení DataFrame do csv'
def save_dataframe_to_csv(dataframe, filname):
    dataframe.to_csv(filname,index = False, header = True)

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

unique_kraj = load_csv_type_conversion('Unique_kraj.csv',dtypes_unique_kraj)
unique_orp = load_csv_type_conversion('Unique_ORP.csv', dtypes_unique_orp)

print(unique_kraj)
Zdrojovy = load_files_to_df('Data','.csv',dtypes_odpady,'Druh_Odpadu','Rok')
print('________---sloucene soubory ----__________')
print(Zdrojovy)
save_dataframe_to_csv(Zdrojovy,'Zdrojovy')
print('______----Zdrojovy----______')
Zdrojovy.info()

Pocet_obyvatel = load_csv_type_conversion('Pocet_obyvatel_2021.csv',dtypes_obyvatele)
#print('_______--pocet obyvatel--___________')
#print(Pocet_obyvatel)

LexikonObci = load_csv_type_conversion('LexikonObci.csv',dtypes_lexikonObci)
#print('_______--lexikon obci--___________')
#print(LexikonObci)

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

Kody_Nakladani = load_csv_type_conversion('Kod_Nakladani.csv',dtypes_nakladani)


'Funkce pro spárování dvou DataFrame'
def merge_left(df1, df2, column1, column2):
    merged_df = pd.merge(df1, df2, left_on=column1,right_on=column2, how = 'left')
    return merged_df
#Funkce pro spárování dvou DataFrame se suffixes'
def merge_left2(df1, df2, column1, column2,suffixes1,suffixes2):
    merged_df = pd.merge(df1, df2, left_on=column1,right_on=column2, how = 'left',suffixes=(suffixes1,suffixes2))
    return merged_df

Zdrojovy = merge_left(Zdrojovy,Pocet_obyvatel,'Evident_ZUJ_Cislo','Kod_Obce')

Zdrojovy_Kody = merge_left(Zdrojovy,Kody_Nakladani,'Kod','Kod')
save_dataframe_to_csv(Zdrojovy_Kody,'Zdrojovy_Kody')
print('______-------Zdrojovy_Kody----______')
Zdrojovy_Kody.info()
print('Je soucet nulovy Zdrojovy_kody')

ZUJ_ORP = load_csv_type_conversion('ZUJ_ORP.csv',dtypes_zuj)


'Kontrola sparovani radku'
def kontrola_sparovani (dataframe,column):
    Nesparovane_radky = dataframe[dataframe[column].isnull()]
    if Nesparovane_radky.empty:
        print(f'Ke vsem radkum leve tabulky byly dohledany hodnoty do sloupce {column}')
        return(True, None)
    else: 
        Nesparovane_radky_pocet = Nesparovane_radky.shape[0]
        print(f'K {Nesparovane_radky_pocet} radkum nebyla dohledana hodnota do sloupce {column}')
        print(Nesparovane_radky)
        return(False,Nesparovane_radky)

'APLIKACE kontrola sparovani'
kontrola_sparovani(Zdrojovy_Kody,'Navyseni_Ubytek')
    
'Vynásobení Množství * (-1 nebo +1) a převede na Kg vynásobením 1000'
def vlozit_sloupec_prepocet_mnozstvi(df):
    df.insert(loc=0,column='Odpad_vKg',value=(df['Mnozstvi'] * df['Navyseni_Ubytek']) * 1000)
    return df

def vlozit_sloupec_prepocet_odpadNaPocetObyv(df):
    df.insert(loc=0,column='OdpadNaObyv_g',value=(df['Odpad_vKg'] / df['Pocet_Obyvatel'])*1000)
    return df

'APLIKACE přidání sloupce Odpad_vKg'
Zdrojovy_Kody_Mnozstvi=vlozit_sloupec_prepocet_mnozstvi(Zdrojovy_Kody)
Zdrojovy_Kody_Mnozstvi=vlozit_sloupec_prepocet_odpadNaPocetObyv(Zdrojovy_Kody_Mnozstvi)

save_dataframe_to_csv(Zdrojovy_Kody_Mnozstvi,'Zdrojovy_kody_mnozstvi')
print('______-------Zdrojovy_Kody_mnozstvi----______')
Zdrojovy_Kody_Mnozstvi.info()

'Grouping DataFrame podle jednoho či více sloupců'
def seskupeni_dat_po_sloupcich(data, func_column, *group_columns ):
    grouped_data = data.groupby(list(group_columns))[func_column].sum().reset_index()
    sorted_data = grouped_data.sort_values(by=func_column,ascending=False)
    return sorted_data

'Grouping DataFrame podle listu s názvy sloupců'
def seskupeni_dat_seznam_sloupcu(data, func_column, group_column_list ):
    grouped_data = data.groupby(group_column_list)[func_column].sum().reset_index()
    return grouped_data


'APLIKACE slouceni podle sloupcu Evident, Evidnet_TypSubjektu, funkce bude na sloupci Odpad_vKg'
Zdrojovy_Kody_Mnozstvi_Seskup = seskupeni_dat_po_sloupcich(Zdrojovy_Kody_Mnozstvi,'Odpad_vKg','Druh_Odpadu','Evident_ZUJ_Cislo','Evident_TypSubjektu')
save_dataframe_to_csv(Zdrojovy_Kody_Mnozstvi_Seskup,'Zdrojovy_kody_mnozstvi_group')


'Funkce pro kontrolu, ze u kazde ZUJ vyjde bilance 0'
def filter_sum_after_grouping(grouped_data, column):
    filtered_data = grouped_data[grouped_data[column] !=0].reset_index()
    return filtered_data
'Funkce ktera vrátí počet řádků df, které se rovnají hodnotě a které se nerovnají'
def count_rows(data,column,value):
    equal_rows = (data[column] == value).sum()
    non_equal_rows = 0
    for val in data[column]:
        if val != value:
            non_equal_rows += 1
        else:
            continue
    return equal_rows, non_equal_rows

def print_non_equal_rows(data, column, value):
    non_equal_rows = data[data[column] != value]
    print("Rows that don't equal to", value, "in column", column, "are:")
    print(non_equal_rows)
    return non_equal_rows.index

'APLIKACE kontrola, zda ZUJ vyjde bilance 0'
Zdrojovy_kody_mnozstvi_group_nevyhov_0 = filter_sum_after_grouping(Zdrojovy_Kody_Mnozstvi_Seskup,'Odpad_vKg')
save_dataframe_to_csv(Zdrojovy_kody_mnozstvi_group_nevyhov_0,'Zdrojovy_kody_mnozstvi_group_nevyhov_0')

equal_rows, non_equal_rows = count_rows(Zdrojovy_Kody_Mnozstvi_Seskup, 'Odpad_vKg', 0)
print(f"Počet ZUJ, které mají roční zúčtování rovno nule: {equal_rows}")
print(f"Počet ZUJ, které roční zúčtování nemají vyrovnané: {non_equal_rows}")

print_non_equal_rows(Zdrojovy_Kody_Mnozstvi_Seskup,'Odpad_vKg', 0)



def summary_stat_parametr(df,parametr,volba,column_summary):
    sort = df[(df[parametr] == volba)]
    result = sort.groupby(parametr)[column_summary].agg([np.mean,np.median,np.min,np.max])
    result = result.applymap(lambda x: round(x))
    locale.setlocale(locale.LC_ALL, '')
    result = result.applymap(lambda x: locale.format_string('%d', x, grouping=True))
    print(result)
    return result


def summary_stat_parametr(df, parametr, seznam, column_summary):
    sort = df[df[parametr].isin(seznam)]
    result = sort.groupby(parametr)[column_summary].agg([np.mean, np.median, np.min, np.max])
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

def summary_stat_new(df):
    result = df.agg([np.mean, np.median, np.mod, np.min, np.max])
    return result



my_list=['Zlínský kraj','Jihomoravský kraj','Jihočeský kraj']
print('Zkouška sortování')
sortovani = Zdrojovy_Kody_Mnozstvi[Zdrojovy_Kody_Mnozstvi['Evident_Kraj_Nazev'].isin(my_list)]
result = summary_stat(sortovani,'Evident_Kraj_Nazev','Odpad_vKg')

summary_stat_parametr(Zdrojovy_Kody_Mnozstvi,'Evident_Kraj_Nazev',my_list,'Odpad_vKg')



# vytvořit seznam unikátních hodnot ze sloupce
def unique_list(df,column_name,start=None):
    u_list = list(df[column_name].unique())
    u_list = sorted(u_list) # seřazení seznamu podle abecedy
    if start == "-all-":
        u_list.insert(0,'-all-') # přidá novou položku "-all-" na pozici 0
    u_list.insert(0,'') # přidá novou položku "" na pozici 0
    return u_list

u_list_indikator = unique_list(Zdrojovy,'Indikator','-all-')
u_list_kod = unique_list(Zdrojovy,'Kod','ahoj')
u_list_druhOdpadu = unique_list(Zdrojovy, 'Druh_Odpadu','-all-')
u_list_rok = unique_list(Zdrojovy,'Rok','-all-')

u_list_evident_kraj = unique_list(Zdrojovy,'Evident_Kraj_Nazev','-all-')
u_list_evident_zuj_cislo = unique_list(Zdrojovy,'Evident_ZUJ_Cislo','')
u_list_evident_zuj_nazev = unique_list(Zdrojovy,'Evident_ZUJ_Nazev','')
u_list_evident_typ = unique_list(Zdrojovy,'Evident_TypSubjektu','-all-')
u_list_evident_orp = unique_list(Zdrojovy,'Evident_ORP_Nazev','')

u_list_partner_kraj = unique_list(Zdrojovy,'Partner_Kraj_Nazev','-all-')
u_list_partner_orp = unique_list(Zdrojovy,'Partner_ORP_Nazev','')
u_list_partner_zuj_nazev = unique_list(Zdrojovy,'Partner_ZUJ_Nazev','')
u_list_partner_typ = unique_list(Zdrojovy,'Partner_TypSubjektu','-all-')
u_list_partner_zuj_cislo = unique_list(Zdrojovy,'Partner_ZUJ_Cislo','')

u_list_column_names = list(Zdrojovy_Kody_Mnozstvi.columns)

def create_area_list(df,column_high,column_low):
    list = df.groupby(column_high)[column_low].unique()
    return list

list_kraj_orp = create_area_list(LexikonObci,'Kraj_Nazev','ORP_Nazev')
list_orp_zuj = create_area_list(LexikonObci,'ORP_Nazev','ZUJ_Nazev')


#Funguje
def vyber_subjektu(df, column1, volby1, column2, volby2, column3, volby3, column4, volby4) :
    if not (volby2 or volby3):
      if (volby1 == [] or volby1 == ['-all-']):
          volby1 = unique_list(Zdrojovy,column1,'-all-')
          del volby1[0:2]
      else: volby1   

    if (volby4 == [] or volby4 == ['-all-']):
        volby4 = unique_list(Zdrojovy,column4,'-all-')
        del volby4[0:2]
    else: volby4

    vysledek = df[((df[column1].isin(volby1)) | (df[column2].isin(volby2)) | (df[column3].isin(volby3)))&(df[column4].isin(volby4))]

    return vysledek

#Výběr kritérií - nový
def vyber_kriterii(df, column1, volby1, column2, volby2, column3, volby3, column4, volby4) :
    if not (volby2):
      if (volby1 == [] or volby1 == ['-all-']):
          volby1 = unique_list(Zdrojovy,column1,'-all-')
          del volby1[0:2]
      else: volby1   

    if (volby3 == [] or volby3 == ['-all-']):
        volby3 = unique_list(Zdrojovy,column3,'-all-')
        del volby3[0:2]
    else: volby3

    if (volby4 == [] or volby4 == ['-all-']):
        volby4 = unique_list(Zdrojovy,column4,'-all-')
        del volby4[0:2]
    else: volby4

    vysledek = df[((df[column1].isin(volby1)) | (df[column2].isin(volby2))) & (df[column3].isin(volby3)) & (df[column4].isin(volby4))]
        
    return vysledek

def odpadNaObyvatele_g(df_filtered,column_grouped,df_lexikon,column_lexikon):
    odpad = seskupeni_dat_po_sloupcich(df_filtered,'Odpad_vKg',column_grouped)
    odpad['Odpad_vKg'] = odpad['Odpad_vKg'].abs()
    obyvatele = seskupeni_dat_po_sloupcich(df_lexikon,'Pocet_Obyvatel',column_lexikon)
    odpad_obyvatele = obyvatele.merge(odpad,left_on=column_lexikon, right_on = column_grouped, how='left')
    odpad_obyvatele['Odpad_vKg'] = odpad_obyvatele['Odpad_vKg'].fillna(value=0)
    odpadNaObyv_g = vlozit_sloupec_prepocet_odpadNaPocetObyv(odpad_obyvatele)
    return odpadNaObyv_g

# ve funkci odstraněné how='left' pro výpočet Relativních četností
def odpadNaObyvatele_g2(df_filtered,column_grouped,df_lexikon,column_lexikon):
    odpad = seskupeni_dat_po_sloupcich(df_filtered,'Odpad_vKg',column_grouped)
    odpad['Odpad_vKg'] = odpad['Odpad_vKg'].abs()
    obyvatele = seskupeni_dat_po_sloupcich(df_lexikon,'Pocet_Obyvatel',column_lexikon)
    odpad_obyvatele = obyvatele.merge(odpad,left_on=column_lexikon, right_on = column_grouped)
    odpad_obyvatele['Odpad_vKg'] = odpad_obyvatele['Odpad_vKg'].fillna(value=0)
    odpadNaObyv_g = vlozit_sloupec_prepocet_odpadNaPocetObyv(odpad_obyvatele)
    return odpadNaObyv_g


def zjisteni_hranic(df, columns):
    # určení kvantilů
    q1 = df[columns].quantile(0.15)
    q3 = df[columns].quantile(0.85)
    iqr = q3 - q1
    spodni_hranice = q1 - 1.5 * iqr
    horni_hranice = q3 + 1.5 * iqr
    return spodni_hranice, horni_hranice

def zjisteni_hranic2(df, columns,q1,q3):
    # určení kvantilů
    q1 = df[columns].quantile(q1)
    q3 = df[columns].quantile(q3)
    iqr = q3 - q1
    spodni_hranice = q1 - 1.5 * iqr
    horni_hranice = q3 + 1.5 * iqr
    return spodni_hranice, horni_hranice