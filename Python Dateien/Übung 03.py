# ToDo
# Offsetfehler
# Verstärkungsfehler
# Linearitätsfehler

# Notes
# https://www.tutorialspoint.com/python/python_gui_programming.htm
# Checkbutton


import tkinter as tk
import numpy as np
import matplotlib as plt

plt.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

#test_data_x = np.linspace(0, 100, 100)
test_data_y = np.linspace(0, 100, 100)

window = tk.Tk()
window.title("Übung 03 - Statische Eigenschaften von Messystemen")

figure = Figure(figsize=(6, 4), dpi=100)
figure_canvas = FigureCanvasTkAgg(figure, window)

toolbar = NavigationToolbar2Tk(figure_canvas, window, pack_toolbar=False)

axes = figure.add_subplot()

axes.plot(test_data_y)
axes.set_title("Kennlinien Fehler Demo")

offset_toggle = 0
verstärkung_toggle = 0
linearität_toggle = 0

offset_value = 0
verstärkung_value = 0
linearität_value = 0

offset_checkbox = tk.Checkbutton(window, text="Offsetfehler", variable=offset_toggle, onvalue=1, offvalue=0)
verstärkung_checkbox = tk.Checkbutton(window, text="Verstärkungsfehler", variable=verstärkung_toggle, onvalue=1, offvalue=0)
linearität_checkbox = tk.Checkbutton(window, text="Linearitätsfehler", variable=linearität_toggle, onvalue=1, offvalue=0)

offset_scale = tk.Scale(window, showvalue=1, orient='horizontal', variable=offset_value, from_=-100.00, to=100.00)
verstärkung_scale = tk.Scale(window, showvalue=1, orient='horizontal', variable=verstärkung_value, from_=-100.00, to=100.00)
linearität_scale = tk.Scale(window, showvalue=1, orient='horizontal', variable=linearität_value, from_=-100.00, to=100.00)


figure_canvas.get_tk_widget().grid(row = 0,column = 1, columnspan = 3)
offset_checkbox.grid(row = 1,column = 0)
verstärkung_checkbox.grid(row = 2,column = 0)
linearität_checkbox.grid(row = 3,column = 0)
offset_scale.grid(row = 1,column = 1, columnspan = 2)
verstärkung_scale.grid(row = 2,column = 1, columnspan = 2)
linearität_scale.grid(row = 3,column = 1, columnspan = 2)


# def button_action():
#     anweisungs_label.config(text="Ich wurde geöndert")




# change_btn = tk.Button(window, text = "Ändern", command = button_action)
# exit_btn = tk.Button(window, text = "Exit", command = window.quit)

# anweisungs_label = tk.Label(window, text = "Ich bin eine Anweisung")
# info_label = tk.Label(window, text = "Ich bin ein Info Label:\nDer Beenden Button schließt das Fenster!")

# anweisungs_label.pack()
# change_btn.pack()
# info_label.pack()
# exit_btn.pack()

if __name__ == "__main__":
    window.mainloop()