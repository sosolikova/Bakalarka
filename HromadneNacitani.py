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
