import tkinter as tk
import HromadneNacitani as hn

def handle_selection(selection):
    """Funkce, která bude spuštěna při výběru položky v menu"""
   # print(f"Vybráno: {selection}")
    text_widget.insert("end",f"Vybráno: {selection}\n")

# Vytvoření okna
root = tk.Tk()

# Vytvoření menu
menu = tk.Menu(root)
root.config(menu=menu)

# Vytvoření položek v menu
file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=lambda: handle_selection(hn.Zdrojovy_kody_mnozstvi_group_nevyhov_0))
file_menu.add_command(label="Open", command=lambda: handle_selection("Open"))
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

edit_menu = tk.Menu(menu)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=lambda: handle_selection("Cut"))
edit_menu.add_command(label="Copy", command=lambda: handle_selection("Copy"))
edit_menu.add_command(label="Paste", command=lambda: handle_selection("Paste"))

# Vytvoření Text widget
text_widget = tk.Text(root)
text_widget.pack()

# Spuštění hlavní smyčky
root.mainloop()