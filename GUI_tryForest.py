import tkinter as tk
from tkinter import ttk
import tkinter

root = tk.Tk()
root.geometry("1000x750")

# Import the tcl file
root.tk.call('source', 'forest-light.tcl')

# Set the theme with the theme_use method
ttk.Style().theme_use('forest-light')

frame = ttk.Frame(root)
frame.pack()

# Vyber dat frame
sort_options_frame = ttk.LabelFrame(frame, text = "Volba parametrů")
sort_options_frame.grid(row=0, column=0, padx=20, pady=10)

# evident frame
evident_frame = ttk.LabelFrame(sort_options_frame, text = "Evident")
evident_frame.grid(row=0, column=0, padx=20, pady=10)

# Evident kraj
evident_kraj_options=["Zlínský kraj", "Pardubický kraj", "Olomoucký kraj"]
evident_kraj_label = ttk.Label(evident_frame, text = "Kraj")
evident_kraj_combo = ttk.Combobox(evident_frame, state=["readonly"],value=evident_kraj_options)
evident_kraj_label.grid(row=0, column=0)
evident_kraj_combo.grid(row=1, column=0)

evident_kraj_options_c=["CZ0712", "CZ0714", "CZ0804"]
evident_kraj_label_c = ttk.Label(evident_frame, text = "Číslo kraje")
evident_kraj_combo_c = ttk.Combobox(evident_frame, state=["readonly"],value=evident_kraj_options_c)
evident_kraj_label_c.grid(row=0, column=1)
evident_kraj_combo_c.grid(row=1, column=1)

# Evident ORP
evident_orp_options=["Zlín", "Pardubice", "Kroměříž", "Hulín"]
evident_orp_label = ttk.Label(evident_frame, text = "ORP")
evident_orp_combo = ttk.Combobox(evident_frame, state=["readonly"],value=evident_orp_options)
evident_orp_label.grid(row=2, column=0)
evident_orp_combo.grid(row=3, column=0)

evident_orp_options_s=["orp", "orp", "orp", "orp"]
evident_orp_label_s = ttk.Label(evident_frame, text = "Číslo ORP")
evident_orp_combo_s = ttk.Combobox(evident_frame, state=["readonly"],value=evident_orp_options_s)
evident_orp_label_s.grid(row=2, column=1)
evident_orp_combo_s.grid(row=3, column=1)

#Evident ZUJ
evident_zuj_options=["Kvítkovice", "Prštné", "Malenovice", "Smiřice"]
evident_zuj_label = ttk.Label(evident_frame, text = "ZUJ")
evident_zuj_combo = ttk.Combobox(evident_frame, state=["readonly"],value=evident_zuj_options)
evident_zuj_label.grid(row=4, column=0)
evident_zuj_combo.grid(row=5, column=0)

evident_zuj_options_c=["502405", "500496", "500135", "503410"]
evident_zuj_label_c = ttk.Label(evident_frame, text = "číslo ZUJ")
evident_zuj_combo_c = ttk.Combobox(evident_frame, state=["readonly"],value=evident_zuj_options_c)
evident_zuj_label_c.grid(row=4, column=1)
evident_zuj_combo_c.grid(row=5, column=1)


# partner frame
partner_frame = ttk.LabelFrame(sort_options_frame, text = "Partner")
partner_frame.grid(row=1, column=0, padx=20, pady=10)

# partner kraj
partner_kraj_options=["Zlínský kraj", "Pardubický kraj", "Olomoucký kraj"]
partner_kraj_label = ttk.Label(partner_frame, text = "Kraj")
partner_kraj_combo = ttk.Combobox(partner_frame, state=["readonly"],value=partner_kraj_options)
partner_kraj_label.grid(row=0, column=0)
partner_kraj_combo.grid(row=1, column=0)

partner_kraj_options_c=["CZ0712", "CZ0714", "CZ0804"]
partner_kraj_label_c = ttk.Label(partner_frame, text = "Číslo kraje")
partner_kraj_combo_c = ttk.Combobox(partner_frame, state=["readonly"],value=partner_kraj_options_c)
partner_kraj_label_c.grid(row=0, column=1)
partner_kraj_combo_c.grid(row=1, column=1)

# partner ORP
partner_orp_options=["Zlín", "Pardubice", "Kroměříž", "Hulín"]
partner_orp_label = ttk.Label(partner_frame, text = "ORP")
partner_orp_combo = ttk.Combobox(partner_frame, state=["readonly"],value=partner_orp_options)
partner_orp_label.grid(row=2, column=0)
partner_orp_combo.grid(row=3, column=0)

partner_orp_options_s=["orp", "orp", "orp", "orp"]
partner_orp_label_s = ttk.Label(partner_frame, text = "Číslo ORP")
partner_orp_combo_s = ttk.Combobox(partner_frame, state=["readonly"],value=partner_orp_options_s)
partner_orp_label_s.grid(row=2, column=1)
partner_orp_combo_s.grid(row=3, column=1)

#partner ZUJ
partner_zuj_options=["Kvítkovice", "Prštné", "Malenovice", "Smiřice"]
partner_zuj_label = ttk.Label(partner_frame, text = "ZUJ")
partner_zuj_combo = ttk.Combobox(partner_frame, state=["readonly"],value=partner_zuj_options)
partner_zuj_label.grid(row=4, column=0)
partner_zuj_combo.grid(row=5, column=0)

partner_zuj_options_c=["502405", "500496", "500135", "503410"]
partner_zuj_label_c = ttk.Label(partner_frame, text = "číslo ZUJ")
partner_zuj_combo_c = ttk.Combobox(partner_frame, state=["readonly"],value=partner_zuj_options_c)
partner_zuj_label_c.grid(row=4, column=1)
partner_zuj_combo_c.grid(row=5, column=1)

for widget in sort_options_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)


# Frame nastavení kritérií
sort_kriteria_frame = ttk.LabelFrame(frame, text = "Kritéria výběru")
sort_kriteria_frame.grid(row=0, column=1, padx=20, pady=10)



#Identifikátor
identifikator_options=["Převzetí","Produkce","Vyskladnění"]
identifikator_label = ttk.Label(sort_kriteria_frame, text = "Identifikátor")
identifikator_combo = ttk.Combobox(sort_kriteria_frame, state=["readonly"],value=identifikator_options)
identifikator_label.grid(row=0, column=0)
identifikator_combo.grid(row=1, column=0)

#Kód odpadu
kod_odpadu_options=["A00", "Předání", "Převzetí", "Produkce"]
kod_odpadu_label = ttk.Label(sort_kriteria_frame, text = "Kód odpadu")
kod_odpadu_listbox = tkinter.Listbox(sort_kriteria_frame, selectmode=tk.MULTIPLE, height=1)
kod_odpadu_listbox.insert("end",*kod_odpadu_options)
kod_odpadu_label.grid(row=2, column=0)
kod_odpadu_listbox.grid(row=3, column=0)

fruits = ["Apple", "Banana", "Orange", "Pear", "Grape", "Watermelon", "Pineapple", "Cherry", "Kiwi", "Mango"]

listbox = tk.Listbox(sort_kriteria_frame, selectmode="multiple", height=5)
listbox.grid(row=4, column=0, padx=(0,5), sticky="ns")

scrollbar = ttk.Scrollbar(sort_kriteria_frame, orient="vertical", command=listbox.yview)
scrollbar.grid(row=4, column=0, padx=(5,0),sticky="ns")

listbox.config(yscrollcommand=scrollbar.set)
listbox.insert("end", *fruits)
root.mainloop()