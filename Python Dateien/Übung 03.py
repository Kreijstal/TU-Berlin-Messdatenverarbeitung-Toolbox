# Notes
# https://www.tutorialspoint.com/python/python_gui_programming.htm

import tkinter as tk
import numpy as np
import matplotlib as mpl
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

mpl.use('TkAgg')

title = "Übung 03 - Statische Eigenschaften von Messystemen"

class TKWindow(tk.Tk):
    #figure = Figure(figsize=(6, 4), dpi=100)
    graph = np.zeros(100)
    
    def __init__(self, title):
        super().__init__()
        self.init_window()
        self.init_params()
        self.init_figure()
        self.init_axes()
        self.create_widgets()
        self.place_widgets()
    
    def init_window(self):
        self.title(title)
        self.resizable(False, False)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=10)
    
    def init_params(self):
        self.params = {'offset': [tk.BooleanVar(), tk.DoubleVar()], 
                       'amplification': [tk.BooleanVar(), tk.DoubleVar()], 
                       'linearity': [tk.BooleanVar(), tk.DoubleVar()]}
    
    def init_figure(self):
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)
    
    def init_axes(self):
        self.axes = self.figure.add_subplot()
        self.axes.set_title("Kennlinien Fehler Demo")                       #dynamisch
    
    def create_widgets(self):
        self.checkboxes = {'offset': tk.Checkbutton(self, text="Offsetfehler", variable=self.params['offset'][0], onvalue=True, offvalue=False),
                           'amplification': tk.Checkbutton(self, text="Verstärkungsfehler", variable=self.params['amplification'][0], onvalue=True, offvalue=False),
                           'linearity': tk.Checkbutton(self, text="Linearitätsfehler", variable=self.params['linearity'][0], onvalue=True, offvalue=False)}
        self.scales = {'offset': tk.Scale(self, showvalue=1, orient='horizontal', variable=self.params['offset'][1], from_=-100.00, to=100.00),
                       'amplification': tk.Scale(self, showvalue=1, orient='horizontal', variable=self.params['amplification'][1], from_=-1.00, to=1.00),
                       'linearity': tk.Scale(self, showvalue=1, orient='horizontal', variable=self.params['linearity'][1], from_=-1.00, to=1.00)}
    
    def place_widgets(self):
        self.figure_canvas.get_tk_widget().grid(row = 0, column = 0, columnspan = 2)
        
        self.checkboxes['offset'].grid(row = 1, column = 0, sticky = 'w', pady = 10, padx = 40)
        self.checkboxes['amplification'].grid(row = 2, column = 0, sticky = 'w', pady = 10, padx = 40)
        self.checkboxes['linearity'].grid(row = 3, column = 0, sticky = 'w', pady = 10, padx = 40)
        
        self.scales['offset'].grid(row = 1, column = 1, sticky = 'ew', pady = 10, padx = 40)
        self.scales['amplification'].grid(row = 2, column = 1, sticky = 'ew', pady = 10, padx = 40)
        self.scales['linearity'].grid(row = 3, column = 1, sticky = 'ew', pady = 10, padx = 40)
    
    def window_loop(self):
        self.animation_object = animation.FuncAnimation(self.figure, self.animate, interval = 100)
        self.mainloop()
    
    def animate(self, i):
        self.update_graph()
        self.axes.clear()
        self.axes.plot(self.graph)
    
    def update_graph(self):
        a = self.params['linearity'][1].get() if self.params['linearity'][0].get() else 0
        b = 1 + self.params['amplification'][1].get() if self.params['amplification'][0].get() else 1
        c = self.params['offset'][1].get() if self.params['offset'][0].get() else 0
        
        for x in range(0, self.graph.size):
            self.graph[x] = a*x**2 + b*x + c

# toolbar = NavigationToolbar2Tk(figure_canvas, window, pack_toolbar=False)

if __name__ == "__main__":
    exercise_03 = TKWindow(title)
    exercise_03.window_loop()