# ToDo
# Offsetfehler
# Verstärkungsfehler
# Linearitätsfehler

# Notes
# https://www.tutorialspoint.com/python/python_gui_programming.htm
# Checkbutton


import tkinter as tk
import numpy as np
import matplotlib as mpl
import matplotlib.animation as animation

mpl.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

window = tk.Tk()
window.title("Übung 03 - Statische Eigenschaften von Messystemen")

figure = Figure(figsize=(6, 4), dpi=100)
figure_canvas = FigureCanvasTkAgg(figure, window)

toolbar = NavigationToolbar2Tk(figure_canvas, window, pack_toolbar=False)

axes = figure.add_subplot()

graph = np.linspace(0, 100, 100)

axes.plot(graph)
axes.set_title("Kennlinien Fehler Demo")

offset_toggle = tk.DoubleVar
verstärkung_toggle = tk.DoubleVar
linearität_toggle = tk.DoubleVar

offset_value = tk.DoubleVar
verstärkung_value = tk.DoubleVar
linearität_value = tk.DoubleVar

offset_checkbox = tk.Checkbutton(window, text="Offsetfehler", variable=offset_toggle, onvalue=1, offvalue=0)
verstärkung_checkbox = tk.Checkbutton(window, text="Verstärkungsfehler", variable=verstärkung_toggle, onvalue=1, offvalue=0)
linearität_checkbox = tk.Checkbutton(window, text="Linearitätsfehler", variable=linearität_toggle, onvalue=1, offvalue=0)

offset_scale = tk.Scale(window, showvalue=1, orient='horizontal', variable=offset_value, from_=-100.00, to=100.00)
verstärkung_scale = tk.Scale(window, showvalue=1, orient='horizontal', variable=verstärkung_value, from_=-100.00, to=100.00)
linearität_scale = tk.Scale(window, showvalue=1, orient='horizontal', variable=linearität_value, from_=-100.00, to=100.00)

window.columnconfigure(0, weight=0)
window.columnconfigure(1, weight=10)
figure_canvas.get_tk_widget().grid(row = 0, column = 0, columnspan = 2)
offset_checkbox.grid(row = 1, column = 0, sticky = 'w', pady = 10, padx = 40)
verstärkung_checkbox.grid(row = 2, column = 0, sticky = 'w', pady = 10, padx = 40)
linearität_checkbox.grid(row = 3, column = 0, sticky = 'w', pady = 10, padx = 40)
offset_scale.grid(row = 1, column = 1, sticky = 'ew', pady = 10, padx = 40)
verstärkung_scale.grid(row = 2, column = 1, sticky = 'ew', pady = 10, padx = 40)
linearität_scale.grid(row = 3, column = 1, sticky = 'ew', pady = 10, padx = 40)

def animate(i):
    global offset_scale, axes
    graph = np.linspace(0, offset_scale.get(), 100)
    axes.clear()
    axes.plot(graph)

if __name__ == "__main__":
    ani = animation.FuncAnimation(figure, animate, interval = 100)
    window.mainloop()