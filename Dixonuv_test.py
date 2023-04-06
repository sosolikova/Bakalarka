import numpy as np
from scipy.stats import t

# Data vzorku
data = [2.3, 3.4, 4.5, 6.7, 5.6, 7.8, 8.9, 10.1, 9.0, 40.3, 11.2, 13.4, 15.6, 14.5, 16.7, 17.8, 18.9, 19.0, 20.1, 21.2]

# Výpočet IQR metody
q1, q3 = np.percentile(data, [25, 75])
iqr = q3 - q1

# Určení odlehlých hodnot
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
outliers = [x for x in data if x < lower_bound or x > upper_bound]

# Výsledky testu
if len(outliers) > 0:
    print("Existuje odlehlá hodnota v datovém vzorku.")
else:
    print("Odlehlá hodnota v datovém vzorku není zjištěna.")




# vytvoření umělého datového vzorku s odlehlou hodnotou
data2 = np.array([5.5, 6.1, 6.3, 6.6, 6.8, 7.1, 7.5, 8.0, 12.3])

# definice hladiny významnosti
alpha = 0.05

# výpočet testovací statistiky a kritické hodnoty
n = len(data2)
mean = np.mean(data2)
std = np.std(data2, ddof=1)
t_value = (n - 2) * (np.max(data) - mean) / std
critical_value = t.ppf(1 - alpha / (2 * n), n - 2) * (n - 1) / np.sqrt(n) * np.sqrt(n - 2 + np.power(t.ppf(1 - alpha / (2 * n), n - 2), 2))

print("t_value: ")
print(t_value)
print("\n critical_value")
print(critical_value)
# porovnání testovací statistiky s kritickou hodnotou
if t_value > critical_value:
    print("Odlehlá hodnota byla nalezena.")
else:
    print("Odlehlá hodnota nebyla nalezena.")