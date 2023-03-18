import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Vytvoření grafu
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
ax.plot([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])

# Vykreslení grafu v Canvas
canvas_widget = FigureCanvasTkAgg(fig, master=canvas)
canvas_widget.draw()
canvas_widget.get_tk_widget().pack()

root.mainloop()