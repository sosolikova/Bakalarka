import pandas as pd
import decimal
from decimal import Decimal, getcontext

getcontext().prec = 5     # nastavi presnost na 5 desetinna mista

def convert_to_float(n):
    try:
        return float(n.replace(",","."))
    except:
        return n
def convert_to_int(x):
    return int(float(x.replace(',', '.')) * 1000000)

Data_200110 = pd.read_csv('200110.csv', delimiter=';',dtype={'Evident':str,'Evident_A':str,'Evident_TypSubjektu':str,'Partner':str,'Partner_A':str,'Partner_TypSubjektu':str,'Druh_odpadu':str},converters={'Mnozstvi':convert_to_float})
Data_200111 = pd.read_csv('200111.csv',delimiter=';',converters={'Mnozstvi':convert_to_float})
Nakladani = pd.read_csv('Kod_nakladani.csv',delimiter=';',converters={'Navyseni_Ubytek':int})
Nakladani.to_csv('Nakladani',index=False, header=True)
print(Data_200110.head())
print(Data_200111.head())
print(Data_200110['Mnozstvi'])
print(Data_200111['Mnozstvi'])


Data_200110_zuctovani = pd.merge(Data_200110,Nakladani,on='Kod',how = 'left')
print(Data_200110_zuctovani.head())
Nesparovane_200110_zuctovani = Data_200110_zuctovani[Data_200110_zuctovani['Navyseni_Ubytek'].isnull()]
if Nesparovane_200110_zuctovani.empty:
    print('Jsou sparovany vsechny radky')
else:
    row_unmatched = Nesparovane_200110_zuctovani.shape[0] 
    print(f'K {row_unmatched} radkum nebyla dohledana hodnota Navyseni_Ubytek')
    print('__________nesparovane__________')
    print(Nesparovane_200110_zuctovani)

'Funkce pro spárování dvou DataFrame'
def merge_left(df1, df2, on_columns):
    merged_df = pd.merge(df1, df2, on=on_columns, how = 'left')
    return merged_df
Data_200111_merge = merge_left(Data_200111,Nakladani,'Kod')
print('_______merge data 200111__________')
print(Data_200111_merge)

def save_dataframe_to_csv(dataframe, filname):
    dataframe.to_csv(filname,index = False, header = True)
save_dataframe_to_csv(Data_200111_merge,'Data_200111_zuctovani')

Data_200110_zuctovani.to_csv('Data_200110_zuctovani',index=False, header=True)

Data_200110_zuctovani.insert(loc=0,column='Novy',value=(Data_200110_zuctovani['Mnozstvi'] * Data_200110_zuctovani['Navyseni_Ubytek']))

Data_200110_zuctovani.to_csv('Data_200110_zuctovani',index=False, header=True)

print('_______print groupby_______')
print(Data_200110_zuctovani.groupby(['Evident','Evident_TypSubjektu'])[['Novy']].sum().reset_index())
Grouping_200110_2 = Data_200110_zuctovani.groupby(['Evident','Evident_TypSubjektu'])['Novy'].sum().reset_index()
Grouping_200110_2.to_csv('Data_200110_grouping2',index = False, header = True)
Filtered = Grouping_200110_2[Grouping_200110_2['Novy'] != 0.0000]
print('______FILTERED_________')
print(Filtered)
Filtered.to_csv('Filtered',index = False, header = True)
data_types = Filtered.dtypes
print('________data types filtered________')
print(data_types)

data_types2 = Data_200110_zuctovani.dtypes
print('________data types zuctovani________')
print(data_types2)

data_types3 = Data_200110.dtypes
print('________data types 200110________')
print(data_types3)