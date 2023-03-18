import tkinter as tk

def process_selection():
    # získání výběru uživatele
    selected_indices = listbox.curselection()
    # získání hodnot z výběru
    selected_options = [options[index] for index in selected_indices]
    # vypsání výběru do konzole
    print("Vybrané možnosti: ", selected_options)

# vytvoření okna
root = tk.Tk()

# vytvoření seznamu možností
options = ["Možnost 1", "Možnost 2", "Možnost 3", "Možnost 4", "Možnost 5"]

# vytvoření seznamového widgetu s výběrem více možností
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=1)

# přidání možností do seznamu
for option in options:
    listbox.insert(tk.END, option)

# vytvoření tlačítka pro zpracování výběru
button = tk.Button(root, text="Zpracovat výběr", command=process_selection)

# vložení seznamového widgetu a tlačítka do okna
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
button.pack(side=tk.BOTTOM)

# spuštění hlavní smyčky
root.mainloop()


