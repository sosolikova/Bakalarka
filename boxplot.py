import matplotlib.pyplot as plt
import numpy as np

# Vytvoření náhodných dat pro druhý druh odpadu
np.random.seed(2)
data2 = np.random.normal(0, 1, size=100)

# Vytvoření náhodných dat pro první druh odpadu
np.random.seed(1)
data1 = np.random.normal(2, 1, size=100)

# Vytvoření boxplotu
fig, ax = plt.subplots()
ax.boxplot([data1, data2])

# Nastavení popisků os a názvu grafu
ax.set_xlabel('Druhy odpadů')
ax.set_ylabel('Hodnoty')
ax.set_title('Boxplot pro dva druhy odpadů')

# Nastavení popisků na ose x
ax.set_xticklabels(['Odpad 1', 'Odpad 2'])

# Zobrazení grafu
plt.show()


