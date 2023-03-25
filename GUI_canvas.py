import tkinter as tk
from tkinter import ttk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # První ComboBox pro výběr země
        self.country_label = tk.Label(self, text="Země:")
        self.country_label.grid(row=0, column=0)
        self.country_combo = ttk.Combobox(self, state="readonly")
        self.country_combo.grid(row=0, column=1)
        self.country_combo.bind("<<ComboboxSelected>>", self.on_country_select)

        # Druhý ComboBox pro výběr města
        self.city_label = tk.Label(self, text="Město:")
        self.city_label.grid(row=1, column=0)
        self.city_combo = ttk.Combobox(self, state="readonly")
        self.city_combo.grid(row=1, column=1)

        # Nastavení možností v prvním ComboBoxu
        self.country_combo["values"] = ("Česká republika", "Slovensko", "Polsko")

    def on_country_select(self, event):
        # Získání hodnoty vybrané v prvním ComboBoxu
        selected_country = self.country_combo.get()

        # Nastavení možností v druhém ComboBoxu podle vybrané hodnoty
        if selected_country == "Česká republika":
            self.city_combo["values"] = ("Praha", "Brno", "Ostrava")
        elif selected_country == "Slovensko":
            self.city_combo["values"] = ("Bratislava", "Košice", "Žilina")
        elif selected_country == "Polsko":
            self.city_combo["values"] = ("Varšava", "Krakov", "Poznaň")

# Vytvoření hlavního okna a spuštění aplikace
root = tk.Tk()
app = Application(master=root)
app.mainloop()