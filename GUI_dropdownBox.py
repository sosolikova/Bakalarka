from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from pandas import options
import HromadneNacitani as hn


root = Tk()
root.title('Data o odpadech')
'root.iconbitmap(c:/gui/codemy.ico)'
root.geometry("400x400")

def selected(event):
    if clicked.get() == 'Friday':
        myLabel = Label(root, text="Yay Its Friday").pack()
    else:
        myLabel = Label(root, text=clicked.get()).pack()

def comboclick(event):
    #myLabel = Label(root, text=myCombo.get()).pack()
    if myCombo.get() == 'Friday':
        myLabel = Label(root, text="Yay Its patek").pack()
    else:
        myLabel = Label(root, text=myCombo.get()).pack()

options = hn.unikatni_indikator          
options2 = [
    "Monday",
    "Tueseday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
clicked = StringVar()
clicked.set(options[0])

drop = OptionMenu(root, clicked, *options, command=selected)
drop.pack(pady=20)

myCombo = ttk.Combobox(root, value=options)
myCombo.current(0)
myCombo.bind("<<ComboboxSelected>>", comboclick)
myCombo.pack()
#myButton = Button(root, text="select from list",command=selected)
#myButton.pack()
root.mainloop()