import os
import pandas as pd
import Funkce

dtypes_nakladani = {
    'Navyseni_Ubytek': 'int'
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

def load_files_to_df(directory,extension,dtypes):
    files = [file for file in os.listdir(directory) if file.endswith(extension)]

    df = pd.DataFrame()

    for file in files:
        filepath = os.path.join(directory, file)
        data = pd.read_csv(filepath,delimiter=';', decimal=',', usecols = None, dtype=dtypes)

        filename = os.path.splitext(file)[0]
        data['Zdrojovy_soubor'] = filename
        df = df.append(data)
    return df

Zdrojovy = load_files_to_df('Data','.csv',dtypes_odpady)
print('________---sloucene soubory ----__________')
print(Zdrojovy)
Funkce.save_dataframe_to_csv(Zdrojovy,'Zdrojovy')

Zdrojovy.info()

Kody = load_csv_type_conversion('Kod_Nakladani.csv',dtypes_nakladani)

'Funkce pro spárování dvou DataFrame'
def merge_left(df1, df2, on_columns):
    merged_df = pd.merge(df1, df2, on=on_columns, how = 'left')
    return merged_df

Zdrojovy_Kody = merge_left(Zdrojovy,Kody,'Kod')
Funkce.save_dataframe_to_csv(Zdrojovy_Kody,'Zdrojovy_Kody')
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