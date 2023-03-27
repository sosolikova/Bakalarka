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

volby_identifikator = []
volby_kod = []
volby_rok = []
volby_druhOdpadu = []
volby_funkce = []

# Seznamy pro evidenta
volby_evident_kraj = []
volby_evident_ORP = []
volby_evident_nazev = []
volby_evident_typ = []

# Seznamy pro partnera
volby_partner_kraj = []
volby_partner_ORP = []
volby_partner_nazev = []
volby_partner_typ = []

# Definice funkcí
def handle_evident_kraj(selection):
    volby_evident_kraj.append(selection)
    text_widget.insert('1.0', f"Evident kraj: {selection}\n")

def handle_evident_ORP(selection):
    volby_evident_ORP.append(selection)
    text_widget.insert('1.0', f"Evident ORP: {selection}\n")

def handle_evident_nazev(selection):
    volby_evident_nazev.append(selection)
    text_widget.insert('1.0', f"Evident název: {selection}\n")

def handle_evident_typSubjektu(selection):
    volby_evident_typ.append(selection)
    text_widget.insert('1.0', f"Evident typ subjektu: {selection}\n")

def handle_partner_kraj(selection):
    volby_partner_kraj.append(selection)
    text_widget.insert('1.0', f"Partner kraj: {selection}\n")

def handle_partner_ORP(selection):
    volby_partner_ORP.append(selection)
    text_widget.insert('1.0', f"Partner ORP: {selection}\n")

def handle_partner_nazev(selection):
    volby_partner_nazev.append(selection)
    text_widget.insert('1.0', f"Partner název: {selection}\n")

def handle_partner_typSubjektu(selection):
    volby_partner_typ.append(selection)
    text_widget.insert('1.0', f"Partner typ subjektu: {selection}\n")

def handle_identifikator(selection):
    volby_identifikator.append(selection)
    text_widget.insert('1.0', f"Identifikátor: {selection}\n")

def handle_kod(selection):
    volby_kod.append(selection)
    text_widget.insert('1.0', f"Kód nakládání: {selection}\n")

def handle_rok(selection):
    volby_rok.append(selection)
    text_widget.insert('1.0', f"Rok: {selection}\n")

def handle_druhOdpadu(selection):
    volby_druhOdpadu.append(selection)
    text_widget.insert('1.0', f"Druh odpadu: {selection}\n")

def handle_funkce(selection):
    volby_funkce.append(selection)
    text_widget.delete('1.0','end')
    text_widget.insert('1.0', f"Vybraný výpočet: {selection}\n")
def funkce1():
    text_widget.insert(tk.END, "Funkce1\n")
def funkce2():
    text_widget.insert(tk.END, "Funkce2\n")
def funkce3():
    text_widget.insert(tk.END, "Funkce3\n")

# Slovník, kde klíče jsou názvy funkcí a hodnoty jsou samotné funkce
funkce_dict = {
    "Percentily": funkce1,
    "Kontingenční tabulka": funkce2,
    "Summarizace": funkce3
}

def perform_action():
    selected_func=funkce_combo.get()
    text_widget.delete('1.0','end')
    text_widget.insert("end",f"Vybrána funkce: {selected_func.upper()}\n")
    # tady umístit kód pro spuštění vybrané funkce
        # kontrolujeme, zda klíč existuje ve slovníku a voláme příslušnou funkci
    if selected_func in funkce_dict:
        funkce_dict[selected_func]()
    else:
        text_widget.insert("end","Chybná volba funkce")

def vytisknout_volby():
    """Tato funkce se spustí po stisknutí tlačítka Uložit volby"""
    text_widget.delete('1.0','end')
    text_widget.insert("end",'Zadané volby: \n')
    text_widget.insert("end",f"Identifikátor: {volby_identifikator}\n")
    text_widget.insert("end",f"Kód nakládání: {volby_kod}\n")
    text_widget.insert("end",f"Druh odpadu: {volby_druhOdpadu}\n")
    text_widget.insert("end",f"Rok: {volby_rok}\n\n")

    text_widget.insert("end",f"Evident kraj: {volby_evident_kraj}\n")
    text_widget.insert("end",f"Evident ORP: {volby_evident_ORP}\n")
    text_widget.insert("end",f"Evident ZÚJ: {volby_evident_nazev}\n")
    text_widget.insert("end",f"Evident typ subjektu: {volby_evident_typ}\n\n")

    text_widget.insert("end",f"Partner kraj: {volby_partner_kraj}\n")
    text_widget.insert("end",f"Partner ORP: {volby_partner_ORP}\n")
    text_widget.insert("end",f"Partner ZÚJ: {volby_partner_nazev}\n")
    text_widget.insert("end",f"Partner typ subjektu: {volby_partner_typ}\n\n")

def vymazat_volby():
    """Tato funkce se spustí po stisknutí tlačítka Vymazat volby"""
    text_widget.delete('1.0','end')
    volby_evident_kraj.clear()
    volby_evident_ORP.clear()
    volby_evident_nazev.clear()
    volby_evident_typ.clear()
    evident_kraj_combo.current(0)
    evident_ORP_combo.current(0)
    evident_nazev_combo.current(0)
    evident_typSubjektu_combo.current(0)

    volby_partner_kraj.clear()
    volby_partner_ORP.clear()
    volby_partner_nazev.clear()
    volby_partner_typ.clear()
    partner_kraj_combo.current(0)
    partner_ORP_combo.current(0)
    partner_nazev_combo.current(0)
    partner_typSubjektu_combo.current(0)

    volby_identifikator.clear()
    volby_kod.clear()
    volby_druhOdpadu.clear()
    volby_rok.clear()
    identifikator_combo.current(0)
    kod_combo.current(0)
    druhOdpadu_combo.current(0)
    rok_combo.current(0)


def on_button_click():
    vysledek=hn.summary_stat_parametr(hn.Zdrojovy_kody_mnozstvi,'Evident_Kraj_Nazev',volby_evident_kraj,'ZmenaMnozstvi')
    text_widget.delete("1.0","end")
    text_widget.insert("1.0",vysledek)

def on_checkbox_click():
    if check_var.get():
        # Zobrazení comboboxu
        partner_frame.pack(side=tk.TOP)
        partner_kraj_label.pack(side=tk.TOP)
        partner_kraj_combo.pack(side=tk.TOP)
        partner_ORP_label.pack(side=tk.TOP)
        partner_ORP_combo.pack(side=tk.TOP)
        partner_nazev_label.pack(side=tk.TOP)
        partner_nazev_combo.pack(side=tk.TOP)
        partner_typSubjektu_label.pack(side=tk.TOP)
        partner_typSubjektu_combo.pack(side=tk.TOP)
    else:
        # Skrytí comboboxu
        partner_frame.pack_forget()
        partner_kraj_label.pack_forget()
        partner_kraj_combo.pack_forget()
        partner_ORP_label.pack_forget()
        partner_ORP_combo.pack_forget()
        partner_nazev_label.pack_forget()
        partner_nazev_combo.pack_forget()
        partner_typSubjektu_label.pack_forget()
        partner_typSubjektu_combo.pack_forget()   

root = Tk()
root.title('Data o odpadech')
root.geometry("1000x750")
style = ThemedStyle(root)
# style.set_theme('elegance')
bg = PhotoImage(file="green_forest.png")
bg_label = Label(root,image=bg)
bg_label.place (x=0, y=0, relwidth=1, relheight=1)

# Vvytvoření frame
left_frame = Frame(root)
left_frame.pack(side=LEFT,padx=20, pady=20)

right_frame = Frame(root)
right_frame.pack(side=TOP, padx=20, pady=20)

# Vytvoření prvků pro výběr parametrů
'''
parametry_frame = tk.LabelFrame(right_frame, text= "Výběr parametrů")
parametry_frame.pack(side=tk.TOP, expand=True)
'''

# Vytvoření frame pro Evident a Partner
funkcni_frame = tk.LabelFrame(left_frame, padx=40, pady=30)
funkcni_frame.configure(borderwidth=0, highlightthickness=0)
funkcni_frame.pack(side=tk.TOP, expand=True)

evident_frame = tk.LabelFrame(left_frame, text="Evident", padx=10, pady=10)
evident_frame.pack(side=tk.TOP)

partner_frame = tk.LabelFrame(left_frame, text = "Partner", padx=10, pady=10)
#partner_frame.pack(side=tk.TOP)
partner_frame.pack_forget()

# Tlačítko uložit volby
ulozit_button = tk.Button(funkcni_frame, text="Uložit volby",command=vytisknout_volby)
ulozit_button.pack(side=tk.TOP)

# Tlačítko vymazat volby
vymazat_button = tk.Button(funkcni_frame, text="Vymazat volby",command=vymazat_volby)
vymazat_button.pack(side=tk.TOP)

# EVIDENT frame
# Evident kraj combobox
evident_kraj_label = tk.Label(evident_frame, text="Kraj")
evident_kraj_label.pack(side=tk.TOP)
options = hn.u_list_evident_kraj
evident_kraj_combo=ttk.Combobox(evident_frame, value=options)
evident_kraj_combo.bind("<<ComboboxSelected>>", lambda event: handle_evident_kraj(evident_kraj_combo.get()))
evident_kraj_combo.current(0)
evident_kraj_combo.pack(side=tk.TOP)

# Evident ORP
evident_ORP_label = tk.Label(evident_frame, text="ORP")
evident_ORP_label.pack(side=tk.TOP)
options = hn.u_list_evident_orp
evident_ORP_combo = ttk.Combobox(evident_frame, value=options)
evident_ORP_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_evident_ORP(evident_ORP_combo.get()))
evident_ORP_combo.current(0)
evident_ORP_combo.pack()

# Evident název
evident_nazev_label = tk.Label(evident_frame, text="Název")
evident_nazev_label.pack(side=tk.TOP)
options = hn.u_list_evident_orp
evident_nazev_combo = ttk.Combobox(evident_frame, value=options)
evident_nazev_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_evident_nazev(evident_nazev_combo.get()))
evident_nazev_combo.current(0)
evident_nazev_combo.pack()

# Evident typ subjektu
evident_typSubjektu_label = tk.Label(evident_frame, text="Typ subjektu")
evident_typSubjektu_label.pack(side=tk.TOP)
options = hn.u_list_evident_typ
evident_typSubjektu_combo = ttk.Combobox(evident_frame, value=options)
evident_typSubjektu_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_evident_typSubjektu(evident_typSubjektu_combo.get()))
evident_typSubjektu_combo.current(0)
evident_typSubjektu_combo.pack()


# PARTNER frame
# Vytvoření checkboxu
check_var = tk.BooleanVar()
checkbox = tk.Checkbutton(left_frame, text="Zobrazit partnera", variable=check_var, command=on_checkbox_click)
checkbox.pack(side=tk.TOP)

# Partner kraj combobox (více možností)
partner_kraj_label = tk.Label(partner_frame, text="Kraj")
#partner_kraj_label.pack(side=tk.TOP)
options = hn.u_list_partner_kraj
partner_kraj_combo=ttk.Combobox(partner_frame, value=options)
partner_kraj_combo.bind("<<ComboboxSelected>>", lambda event: handle_partner_kraj(partner_kraj_combo.get()))
partner_kraj_combo.current(0)
partner_kraj_combo.pack_forget()

# Partner ORP
partner_ORP_label = tk.Label(partner_frame, text="ORP")
#partner_ORP_label.pack(side=tk.TOP)
options = hn.u_list_partner_orp
partner_ORP_combo = ttk.Combobox(partner_frame, value=options)
partner_ORP_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_partner_ORP(partner_ORP_combo.get()))
partner_ORP_combo.current(0)
partner_ORP_combo.pack_forget()

# Partner název
partner_nazev_label = tk.Label(partner_frame, text="Název")
#partner_nazev_label.pack(side=tk.TOP)
options = hn.u_list_partner_orp
partner_nazev_combo = ttk.Combobox(partner_frame, value=options)
partner_nazev_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_partner_nazev(partner_nazev_combo.get()))
partner_nazev_combo.current(0)
partner_nazev_combo.pack_forget()

# Partner typ subjektu
partner_typSubjektu_label = tk.Label(partner_frame, text="Typ subjektu")
#partner_typSubjektu_label.pack(side=tk.TOP)
options = hn.u_list_partner_typ
partner_typSubjektu_combo = ttk.Combobox(partner_frame, value=options)
partner_typSubjektu_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_partner_typSubjektu(partner_typSubjektu_combo.get()))
partner_typSubjektu_combo.current(0)
partner_typSubjektu_combo.pack()
partner_typSubjektu_combo.pack_forget()









# RIGHT frame (parametry)
# Identifikátor
identifikator_label = tk.Label(right_frame, text="Identifikátor")
identifikator_label.grid(row=0, column=0)
options = hn.u_list_indikator
identifikator_combo = ttk.Combobox(right_frame, value=options)
identifikator_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_identifikator(identifikator_combo.get()))
identifikator_combo.current(0)
identifikator_combo.grid(row=1, column=0)
# Kód nakládání
kod_label = tk.Label(right_frame, text="Kód nakládání")
kod_label.grid(row=2, column=0)
options = hn.u_list_kod
kod_combo = ttk.Combobox(right_frame, value=options)
kod_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_kod(kod_combo.get()))
kod_combo.current(0)
kod_combo.grid(row=3, column=0)
# Druh odpadu
druhOdpadu_label= tk.Label(right_frame, text="Druh odpadu")
druhOdpadu_label.grid(row=4, column=0)
options = hn.u_list_druhOdpadu
druhOdpadu_combo = ttk.Combobox(right_frame, value=options)
druhOdpadu_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_druhOdpadu(druhOdpadu_combo.get()))
druhOdpadu_combo.current(0)
druhOdpadu_combo.grid(row=5, column=0)
# Rok
rok_label= tk.Label(right_frame, text="Rok")
rok_label.grid(row=6, column=0)
options = hn.u_list_rok
rok_combo = ttk.Combobox(right_frame, value=options)
rok_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_rok(rok_combo.get()))
rok_combo.current(0)
rok_combo.grid(row=7, column=0)




# Funkce
button1 = tk.Button(right_frame,text="Tlačítko1", command=on_button_click)
button1.grid(row=0, column=2, padx=20, pady=0)
# Funkce
button2 = tk.Button(right_frame,text="Tlačítko2", command=on_button_click)
button2.grid(row=0, column=3, padx=20, pady=0)
# Seznam funkcí
funkce_label= tk.Label(right_frame, text="Funkce")
funkce_label.grid(row=2, column=1, padx=20, pady=0)
options = ['','Sumarizace', 'Kontingenční tabulka', 'Percentily']
funkce_combo = ttk.Combobox(right_frame, value=options)
funkce_combo.bind("<<ComboboxSelected>>" ,lambda event: handle_funkce(funkce_combo.get()))
funkce_combo.current(0)
funkce_combo.grid(row=3, column=1,padx=20, pady=0)

# Talčítko pro spuštění funkce
funkce_button=tk.Button(right_frame, text="Spuštění funkce", command=perform_action)
funkce_button.grid(row=5, column=1, padx=20,pady=0)


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