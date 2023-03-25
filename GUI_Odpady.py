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

# Definice funkcí

def handle_selection(selection):
    """Funkce se spustí při výběru položky v menu"""
    text_widget.insert('1.0', f"Vybráno: {selection}\n")

vybrany_evident_kraj = []
vybrany_evident_kraj2 = []
# Funkce pro zpracování výběru z listboxu
def handle_listbox_selection(event):
    selected_items = evident_kraj_listbox.curselection()
    text_widget.delete('1.0', tk.END)
    for item in selected_items:
        text_widget.insert(tk.END, f"{evident_kraj_listbox.get(item)}\n")
        '''vybrany_evident_kraj.append(selected_items)'''
def process_selection():
    global vybrany_evident_kraj
    #získání výběru uživatele
    selected_indices = evident_kraj_listbox.curselection()
    #získání hodnot z výběru
    selcted_options=[options_kraj[index] for index in selected_indices]
    #vypsání výběru
    print('Vybrané možnosti: ', selcted_options)
    text_widget.insert(tk.END, f"{selcted_options}")
    vybrany_evident_kraj.append(evident_kraj_listbox.get(selected_indices))

# Nastavení tlačítka pro výpis výběru
def vypis_vyberu():
    selected_items = evident_kraj_listbox.curselection()
    text_widget.delete('1.0', tk.END)
    for item in selected_items:
        selected_item = evident_kraj_listbox.get(item)
        text_widget.insert(tk.END, f"{selected_item}\n")
        vybrany_evident_kraj2.append(selected_item)


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

# Evident kraj listbox (více možností)
evident_kraj_label = tk.Label(evident_frame, text="Kraj")
evident_kraj_label.pack(side=tk.TOP)
options_kraj = hn.u_list_evident_kraj
evident_kraj_listbox=tk.Listbox(evident_frame, selectmode=tk.MULTIPLE, height=6)
evident_kraj_listbox.insert("end",*options_kraj)
evident_kraj_listbox.bind("<<ListboxSelect>>", handle_listbox_selection)
evident_kraj_listbox.pack(side=tk.TOP)

# vytvoření tlačítka pro zpracování výběru
evident_kraj_button = tk.Button(evident_frame, text="Zpracovat výběr", command=process_selection)
evident_kraj_button.pack(side=tk.TOP)
tlacitko = tk.Button(root, text="Vypsat výběr", command=vypis_vyberu)
tlacitko.pack(side=tk.TOP)

# Evident typ subjektu
evident_typSubjektu_label = tk.Label(evident_frame, text="Typ subjektu")
evident_typSubjektu_label.pack(side=tk.TOP)
options = hn.u_list_evident_typ
evident_typSubjektu_combo = ttk.Combobox(evident_frame, value=options)
evident_typSubjektu_combo.bind("<<ComboboxSelected>>", lambda event: handle_selection(evident_typSubjektu_combo.get()))
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

print(f"Tisk vybraneho hraje: {vybrany_evident_kraj2}\n")
root.mainloop()
