import pandas as pd

def convert_to_float(n):
    try:
        return float(n.replace(",","."))
    except:
        return n

data_200110 = pd.read_csv('200110.csv',delimiter=';',converters={'Mnozstvi':convert_to_float})
data_200111 = pd.read_csv('200111.csv',delimiter=';',converters={'Mnozstvi':convert_to_float})


print(data_200110.shape)
print(data_200110.info())
print(data_200110.head())
print(data_200110.dtypes)
print(data_200110.Mnozstvi.describe())

print

suspect = data_200110['Druh_odpadu']
print('__________ druh odpadu _________')
print(suspect)
checknull = data_200110.isnull().sum()
print('_________checknull__________')
print(checknull)
Kody_nakladani = pd.read_csv('KodovaniZpusobuNakladani.csv',delimiter=';')
print(Kody_nakladani.shape)
print(Kody_nakladani.info())
print(Kody_nakladani.head())

"""
sloucene = data_200110.merge(Kody_nakladani, on='Kod')
"""
data_200110_kody = pd.merge(data_200110, Kody_nakladani, on='Kod')
print(data_200110_kody.shape)
print(data_200110_kody.info())


data_200110_kody.insert(loc=0,column='Novy',value= data_200110_kody['Mnozstvi'] * data_200110_kody['Navyseni_Ubytek'])
data_200110_kody['Novy']=data_200110_kody['Novy']
print(data_200110_kody['Novy'],['Mnozstvi'],['Navyseni_Ubytek'])
data_200110_kody.to_csv('data_200110_kody',index=False, header=0)
print('ahoj')
print(data_200110_kody.info())
"""
Vypocet sumarizace """
grouping_200110 = data_200110_kody.groupby(['Evident','Evident_TypSubjektu'])['Novy'].sum()
grouping_200110.to_csv('grouping_200110',index=False, header=0)
print(grouping_200110.tail())