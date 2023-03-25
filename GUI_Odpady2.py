from cgitb import text
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from pandas import options
from ttkthemes import ThemedTk
from ttkthemes import ThemedStyle
import HromadneNacitani as hn
import Funkce as fc



volby_evident_kraj = []
volby_evident_ORP = []
volby_evident_typ = []
evident_orp_options = ['Zlínský kraj']
# Definice funkcí

def handle_evident_kraj(selection):
    """Funkce bude přidávat volby do seznamu"""
    volby_evident_kraj.append(selection)
    """Funkce se spustí při výběru položky v menu"""
    text_widget.insert('1.0', f"Evident kraj: {selection}\n")

def handle_evident_ORP(selection):
    volby_evident_ORP.append(selection)
    text_widget.insert('1.0', f"Evident ORP: {selection}\n")

def handle_evident_typSubjektu(selection):
    volby_evident_typ.append(selection)
    text_widget.insert('1.0', f"Evident typ subjektu: {selection}\n")

def vytisknout_volby():
    """Tato funkce se spustí po stisknutí tlačítka Uložit volby"""
    print("Zadané volby: ")
    print("Evident kraj: ", volby_evident_kraj)
    print("Evident typ subjektu: ", volby_evident_ORP)
    print("Evident typ subjektu: ", volby_evident_typ)
   
def vybrat_orp():
    if volby_evident_kraj == '-all-':
        evident_orp_options = hn.u_list_evident_orp
    else:
        vyber = hn.Zdrojovy[hn.Zdrojovy['Evident_Kraj'].isin(volby_evident_kraj)]
        evident_orp_options = hn.unique_list(vyber,'Evident_Nazev')

root = Tk()
root.title('Data o odpadech')
root.geometry("1000x750")
style = ThemedStyle(root)
# style.set_theme('elegance')

# Vvytvoření frame
left_frame = Frame(root)
left_frame.pack(side=LEFT,padx=20, pady=20)

right_frame = Frame(root)
right_frame.pack(side=RIGHT, padx=20, pady=20)

# Vytvoření frame pro Evident a Partner
evident_frame = tk.LabelFrame(left_frame, text="Evident")
evident_frame.pack(side=tk.TOP)

partner_frame = tk.LabelFrame(left_frame, text = "Partner")
partner_frame.pack(side=tk.TOP)

# Vytvoření prvků pro výběr parametrů

# Evident kraj combobox (více možností)
evident_kraj_label = tk.Label(evident_frame, text="Kraj")
evident_kraj_label.pack(side=tk.TOP)
options = hn.u_list_evident_kraj
evident_kraj_combo=ttk.Combobox(evident_frame, value=options)
evident_kraj_combo.bind("<<ComboboxSelected>>", lambda event: handle_evident_kraj(evident_kraj_combo.get()))
evident_kraj_combo.current(0)
evident_kraj_combo.pack(side=tk.TOP)

# Tlačítko uložit volby kraj
evident_kraj_button = tk.Button(evident_frame, text="Uložit volby",command= vybrat_orp)
evident_kraj_button.pack(side=tk.TOP)

# Evident typ ORP
evident_ORP_label = tk.Label(evident_frame, text="ORP")
evident_ORP_label.pack(side=tk.TOP)
options = evident_orp_options
evident_ORP_combo = ttk.Combobox(evident_frame, value=options)
evident_ORP_combo.bind('<FocusOut>',lambda event: print('change vyber'))
evident_ORP_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_evident_ORP(evident_ORP_combo.get()))
evident_ORP_combo.current(0)
evident_ORP_combo.pack()


# Tlačítko uložit volby
ulozit_button = tk.Button(evident_frame, text="Uložit volby",command=vytisknout_volby)
ulozit_button.pack(side=tk.TOP)

# Evident typ subjektu
evident_typSubjektu_label = tk.Label(evident_frame, text="Typ subjektu")
evident_typSubjektu_label.pack(side=tk.TOP)
options = hn.u_list_evident_typ
evident_typSubjektu_combo = ttk.Combobox(evident_frame, value=options)
evident_typSubjektu_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_evident_typSubjektu(evident_typSubjektu_combo.get()))
evident_typSubjektu_combo.current(0)
evident_typSubjektu_combo.pack()


# Vytvoření Text Widget a Scroollbar
text_widget = tk.Text(root)
y_scrollbar = tk.Scrollbar(root, command=text_widget.yview)
x_scrollbar = tk.Scrollbar(root, command=text_widget.xview,orient=tk.HORIZONTAL)

# Připojení Scrollbar k Text Widget
text_widget.config(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

root.mainloop()