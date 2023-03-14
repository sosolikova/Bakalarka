import pandas as pd


dtypes_nakladani = {
    'Navyseni_Ubytek': 'int'
}
dtypes_odpady = {
    'Evident':              'string',
    'Evident_A':            'string',
    'Evident_TypSubjektu':  'string',
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

'APLIKACE'
nactena_200111 = load_csv_type_conversion('200111.csv',dtypes_odpady)
print(nactena_200111)
nakladani_fce = load_csv_type_conversion('Kod_Nakladani.csv',dtypes_nakladani)
print(nakladani_fce.info())


'Funkce pro spárování dvou DataFrame'
def merge_left(df1, df2, on_columns):
    merged_df = pd.merge(df1, df2, on=on_columns, how = 'left')
    return merged_df

'Funkce pro uložení DataFrame do csv'
def save_dataframe_to_csv(dataframe, filname):
    dataframe.to_csv(filname,index = False, header = True)

'APLIKACE_prirazeni -1/+1 podle Kodu'
sloucena = merge_left(nactena_200111,nakladani_fce,'Kod')
save_dataframe_to_csv(sloucena,'sloucena_200111')

'Kontrola sparovani radku'
def unmatched (dataframe,column):
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
unmatched(sloucena,'Navyseni_Ubytek')

'Vynásobení Množství * (-1 nebo +1) a převede na Kg vynásobením 1000'
def add_col_multipl(df):
    df.insert(loc=0,column='ZmenaMnozstvi',value=(df['Mnozstvi'] * df['Navyseni_Ubytek']) * 1000)
    return df

'APLIKACE přidání sloupce ZmenaMnozstvi'
Zuctovani_200111=add_col_multipl(sloucena)
save_dataframe_to_csv(Zuctovani_200111,'Zuctovani_200111')

'Grouping DataFrame podle jednoho či více sloupců'
def group_data_by_columns(data, func_column, *group_columns ):
    grouped_data = data.groupby(list(group_columns))[func_column].sum().reset_index()
    return grouped_data

'APLIKACE slouceni podle sloupcu Evident, Evidnet_TypSubjektu, funkce bude na sloupci ZmenaMnozstvi'
Grouping_200111 = group_data_by_columns(Zuctovani_200111,'ZmenaMnozstvi','Evident','Evident_TypSubjektu')
save_dataframe_to_csv(Grouping_200111,'Grouping_200111')

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
Nevyhovujici_0_200111 = filter_sum_after_grouping(Grouping_200111,'ZmenaMnozstvi')
save_dataframe_to_csv(Nevyhovujici_0_200111,'Nevyhovujici_0_200111')

equal_rows, non_equal_rows = count_rows(Grouping_200111, 'ZmenaMnozstvi', 0)
print(f"Počet ZUJ, které mají roční zúčtování rovno nule: {equal_rows}")
print(f"Počet ZUJ, které roční zúčtování nemají vyrovnané: {non_equal_rows}")

'Funkce pro kontrolu, ze u kazde ZUJ vyjde bilance <-1 nebo >1'
def filter_sum_after_grouping(grouped_data, column):
    filtered_data = grouped_data[grouped_data[column] > 1] | grouped_data[grouped_data[column] < -1].reset_index()
    return filtered_data
Nevyhovujici_1_200111 = filter_sum_after_grouping(Grouping_200111,'ZmenaMnozstvi')
save_dataframe_to_csv(Nevyhovujici_1_200111,'Nevyhovujici_1_200111')