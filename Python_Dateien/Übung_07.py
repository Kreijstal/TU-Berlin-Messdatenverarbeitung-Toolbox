# -*- coding: utf-8 -*-
"""
Messbrücken
Anzeige der Brückenspannung und der Oszilloskopanzeigen für eine vorgebbare
Messbrücke

"""


import tkinter as tk
import numpy as np
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

window_title = "Übung 07 - Anzeige der Brückenspannung und der Oszilloskopanzeigen für eine vorgebbare Messbrücke"

class TKWindow(tk.Tk):
    figure_params = {"figsize": (8,5),
                     "title": "Messbr:ucken",
                     "xlabel": "Output",
                     "ylabel": "Input",
                     "bounds": 100,
                     "legend_position": "upper left"}
    
    graphs = {"x": np.linspace(0, figure_params["bounds"], figure_params["bounds"]+1),
              "y": {"curve": np.zeros(figure_params["bounds"]+1), 
                    "label": "reale Kennlinie", 
                    "color": "blue",
                    "linestyle": "solid"}}
    
    widget_params = {"offset_checkbox": {"name": "offset",
                                          "text": "Offsetfehler",
                                          "variable": None}}    

    def __init__(self, title = "Test Window"):
        """initialization der Klasse

        Args:
            title (str, optional): Fenstertitle. Defaults to "Test Window".
        """        ""
        super().__init__()
        self.init_window(title)
        self.init_params()
        self.init_figure()
        self.init_axes()
        self.create_widgets()
        self.place_widgets()
        self.init_widgets()
    
    def init_window(self, title):
        """_summary_

        Args:
            title (_type_): _description_
        """        
        self.title(title)
        self.resizable(False, False)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=10)
    
    def init_params(self):
        self.widget_params["offset_checkbox"]["variable"] = tk.BooleanVar()
        self.widget_params["amplification_checkbox"]["variable"] = tk.BooleanVar()
        self.widget_params["linearity_checkbox"]["variable"] = tk.BooleanVar()
        self.widget_params["offset_scale"]["variable"] = tk.DoubleVar()
        self.widget_params["amplification_scale"]["variable"] = tk.DoubleVar()
        self.widget_params["linearity_scale"]["variable"] = tk.DoubleVar()
    
    def init_figure(self):
        self.figure = Figure(figsize=self.figure_params["figsize"], dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)
    
    def init_axes(self):
        self.axes = self.figure.add_subplot()
    
    def create_widgets(self):
        self.scales = {self.widget_params["offset_scale"]["name"]: tk.Scale(self, 
                                                                            showvalue=1, 
                                                                            orient='horizontal', 
                                                                            variable=self.widget_params["offset_scale"]["variable"], 
                                                                            from_=self.widget_params["offset_scale"]["from"], 
                                                                            to=self.widget_params["offset_scale"]["to"]),
                       self.widget_params["amplification_scale"]["name"]: tk.Scale(self, 
                                                                                   showvalue=1, 
                                                                                   orient='horizontal', 
                                                                                   variable=self.widget_params["amplification_scale"]["variable"], 
                                                                                   from_=self.widget_params["amplification_scale"]["from"], 
                                                                                   to=self.widget_params["amplification_scale"]["to"]),
                       self.widget_params["linearity_scale"]["name"]: tk.Scale(self, 
                                                                               showvalue=1, 
                                                                               orient='horizontal', 
                                                                               variable=self.widget_params["linearity_scale"]["variable"], 
                                                                               from_=self.widget_params["linearity_scale"]["from"], 
                                                                               to=self.widget_params["linearity_scale"]["to"])}
        self.checkboxes = {self.widget_params["offset_checkbox"]["name"]: tk.Checkbutton(self, 
                                                                                         text=self.widget_params["offset_checkbox"]["text"], 
                                                                                         variable=self.widget_params["offset_checkbox"]["variable"], 
                                                                                         command=lambda: self.checkbox_clicked(self.scales[self.widget_params["offset_scale"]["name"]]),
                                                                                         onvalue=True, 
                                                                                         offvalue=False),
                           self.widget_params["amplification_checkbox"]["name"]: tk.Checkbutton(self, 
                                                                                                text=self.widget_params["amplification_checkbox"]["text"], 
                                                                                                variable=self.widget_params["amplification_checkbox"]["variable"], 
                                                                                                command=lambda: self.checkbox_clicked(self.scales[self.widget_params["amplification_scale"]["name"]]),
                                                                                                onvalue=True, 
                                                                                                offvalue=False),
                           self.widget_params["linearity_checkbox"]["name"]: tk.Checkbutton(self, 
                                                                                            text=self.widget_params["linearity_checkbox"]["text"], 
                                                                                            variable=self.widget_params["linearity_checkbox"]["variable"], 
                                                                                            command=lambda: self.checkbox_clicked(self.scales[self.widget_params["linearity_scale"]["name"]]),
                                                                                            onvalue=True, 
                                                                                            offvalue=False)}
    
    def checkbox_clicked(self, scale):
        """_summary_

        Args:
            scale (_type_): _description_
        """        ""
        scale.set(0)
    
    def place_widgets(self):
        self.figure_canvas.get_tk_widget().grid(row = 0, column = 0, columnspan = 2)
        
        self.checkboxes['offset'].grid(row = 1, column = 0, sticky = 'w', pady = 10, padx = 40)
        self.checkboxes['amplification'].grid(row = 2, column = 0, sticky = 'w', pady = 10, padx = 40)
        self.checkboxes['linearity'].grid(row = 3, column = 0, sticky = 'w', pady = 10, padx = 40)
        
        self.scales['offset'].grid(row = 1, column = 1, sticky = 'ew', pady = 10, padx = 40)
        self.scales['amplification'].grid(row = 2, column = 1, sticky = 'ew', pady = 10, padx = 40)
        self.scales['linearity'].grid(row = 3, column = 1, sticky = 'ew', pady = 10, padx = 40)
    
    def init_widgets(self):
        [self.checkboxes[checkbox].select() for checkbox in self.checkboxes]
    
    def window_loop(self):
        self.animation_object = animation.FuncAnimation(self.figure, self.animate, interval = 100)
        self.mainloop()
    
    def animate(self, i):
        pass
        
    def update_graphs(self):
        pass

    
    def plot_axes(self, plot):
        pass

if __name__ == "__main__":
    exercise_07 = TKWindow(window_title)
    exercise_07.window_loop()