import os
import pandas as pd
import Funkce

dtypes_odpady2= {
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
    df = pd.read_csv(filename, delimiter=';', decimal=',')

    for column, dtype in dtypes.items():
        if column in df.columns:
          df[column].astype(dtype)
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

Zdrojovy2 = load_files_to_df('Data','.csv',dtypes_odpady2)
print('________---sloucene soubory ----__________')
print(Zdrojovy2)
Funkce.save_dataframe_to_csv(Zdrojovy2,'Zdrojovy2')

Zdrojovy2.info()
