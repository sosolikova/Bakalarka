from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from pandas import options
import HromadneNacitani as hn


root = Tk()
root.title('Data o odpadech')
'root.iconbitmap(c:/gui/codemy.ico)'
root.geometry("400x400")

def comboclick(event):
    #myLabel = Label(root, text=myCombo.get()).pack()
    if myCombo.get() == 'Friday':
        myLabel = Label(root, text="Yay Its patek").pack()
    else:
        myLabel = Label(root, text=myCombo.get()).pack()

options = hn.u_list_indikator          
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

myCombo = ttk.Combobox(root, value=options)
myCombo.current(0)
myCombo.bind("<<ComboboxSelected>>", comboclick)
myCombo.pack()
#myButton = Button(root, text="select from list",command=selected)
#myButton.pack()
root.mainloop()