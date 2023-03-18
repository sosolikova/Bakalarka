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

# funkce pro výpočet grafu
def calculate_graph(indikator, partner_kraj):
    # zde by byl kód pro výpočet grafu na základě zadaných parametrů
    # v tomto případě pouze vypíše hodnoty na konzoli
    print(f"Výpočet grafu pro indikátor: {indikator}, kraj partnera: {partner_kraj}")
    # vracíme náhodná data pro účely ukázky
    return [1, 2, 3], [4, 5, 6]

# funkce pro zobrazení grafu
def show_graph(indikator, partner_kraj):
    # vypočítáme data pro graf
    x, y = calculate_graph(indikator, partner_kraj)
    # vykreslíme graf
    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Graf")
    plt.show()

root = Tk()
root.title('Data o odpadech')
root.geometry("800x500")
style = ThemedStyle(root)
style.set_theme('elegance')

# vytvoříme dvě hlavní části okna
left_frame = Frame(root)
left_frame.pack(side=LEFT, padx=20, pady=20)

right_frame = Frame(root)
right_frame.pack(side=RIGHT, padx=20, pady=20)

# vytvoříme Comboboxy pro výběr parametrů
indikator_label = Label(left_frame, text="Evident:")
indikator_label.pack()
options = hn.u_list_evident          
indikator_combo = ttk.Combobox(left_frame, value=options)
indikator_combo.current(0)
indikator_combo.pack()

indikator_label = Label(left_frame, text="Evident typ subjektu:")
indikator_label.pack()
options = hn.u_list_evident_typ          
indikator_combo = ttk.Combobox(left_frame, value=options)
indikator_combo.current(0)
indikator_combo.pack()

indikator_label = Label(left_frame, text="Indikátor:")
indikator_label.pack()
options = hn.u_list_indikator          
indikator_combo = ttk.Combobox(left_frame, value=options)
indikator_combo.current(0)
indikator_combo.pack()

partner_kraj_label = Label(left_frame, text="Kraj partnera:")
partner_kraj_label.pack()
options = hn.u_list_partner_kraj
partner_kraj_combo = ttk.Combobox(left_frame, value=options)
partner_kraj_combo.current(0)
partner_kraj_combo.pack()

# funkce pro výpočet a zobrazení grafu na základě zadaných parametrů
def calculate_and_show_graph():
    indikator = indikator_combo.get()
    partner_kraj = partner_kraj_combo.get()
    show_graph(indikator, partner_kraj)

# vytvoříme tlačítko pro spuštění výpočtu grafu
#calculate_button = Button(left_frame, text="Spočítej", command=calculate_and_show_graph)
calculate_button = Button(left_frame, text="Spočítej", command=hn.Zdrojovy_kody_mnozstvi_group_nevyhov_0)
calculate_button.pack()

# vytvoření proměnných pro každý checkbox
var1 = tk.IntVar()
var2 = tk.IntVar()
var3 = tk.IntVar()

# vytvoření checkboxů a nastavení proměnných
c1 = tk.Checkbutton(root, text="Možnost 1", variable=var1)
c2 = tk.Checkbutton(root, text="Možnost 2", variable=var2)
c3 = tk.Checkbutton(root, text="Možnost 3", variable=var3)

# umístění checkboxů na okno
c1.pack()
c2.pack()
c3.pack()

# získání hodnot z proměnných
def get_checkbox_values():
    values = []
    if var1.get() == 1:
        values.append("Možnost 1")
    if var2.get() == 1:
        values.append("Možnost 2")
    if var3.get() == 1:
        values.append("Možnost 3")
    print(values)
    
# Výběr složky pro načtení dat
def browse_folder():
    folder_path = filedialog.askdirectory()
    print("Vybraná složka: ", folder_path)

browse_button = tk.Button(text="Vybrat složku", command=browse_folder)
browse_button.pack()

def on_button_click():
    volba = indikator_combo.get()
    if volba == "-all-":
        funkce3()
    else:
        funkce1()

def funkce1():
    vysledek = hn.summary_stat_parametr(hn.Zdrojovy_kody_mnozstvi,'Indikator',indikator_combo.get(),'ZmenaMnozstvi')
    text_widget.delete("1.0","end")
    text_widget.insert("1.0", vysledek)
  
def funkce2():
    vysledek = hn.Zdrojovy_kody_mnozstvi_group_nevyhov_0
    text_widget.delete("1.0","end")
    text_widget.insert("1.0", vysledek)
    
def funkce3():
    vysledek = hn.summary_stat(hn.Zdrojovy_kody_mnozstvi,'Indikator','ZmenaMnozstvi')
    text_widget.delete("1.0","end")
    text_widget.insert("1.0", vysledek)

def graph():
    indikator_select = hn.Zdrojovy_kody_mnozstvi[hn.Zdrojovy_kody_mnozstvi['Indikator'] == indikator_combo.get()]
    indikator_select['ZmenaMnozstvi'].hist(bins=30)
    plt.show()

def save_to_csv():
    fc.save_dataframe_to_csv(hn.Zdrojovy_kody_mnozstvi_group_nevyhov_0,'Novy')

my_button = Button(root,text="Graph It!",command=graph)
my_button.pack()

# tlačítko pro získání hodnot z checkboxů
button1 = tk.Button(root, text="Tlačítko 1", command=on_button_click)
button2 = tk.Button(root, text="Tlačítko 2", command=funkce2)
button3 = tk.Button(root, text="Uložit CSV", command=save_to_csv)
button1.pack()
button2.pack()
button3.pack()

# Vytvoření Text widget
text_widget = tk.Text(root)
text_widget.pack(side=tk.BOTTOM)

root.mainloop()