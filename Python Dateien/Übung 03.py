# Notes
# https://www.tutorialspoint.com/python/python_gui_programming.htm

# Improved Checkboxes and parameter dictionarys
# Made checkboxes checked at start and added dictionarys for all 
# parameters of window, widgets and plots

import tkinter as tk
import numpy as np
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

window_title = "Übung 03 - Statische Eigenschaften von Messystemen"

class TKWindow(tk.Tk):
    axes_params = {"bounds": 100,
                   "title": "Kennlinien Fehler",
                   "xlabel": "Output",
                   "ylabel": "Input",
                   "plot1": {"label": "reale Kennlinie",
                             "color": "blue",
                             "linestyle": "-"},
                   "plot2": {"label": "ideale Kennlinie",
                             "color": "red",
                             "linestyle": "--"},
                   "legend_position": "upper left"}
    
    graphs = {"x": np.linspace(0, axes_params["bounds"], axes_params["bounds"]+1), 
             "y": np.zeros(axes_params["bounds"]+1),
             "y_ideal": np.linspace(0, axes_params["bounds"], axes_params["bounds"]+1)}
    
    widget_params = {"offset_checkbox": {"name": "offset",
                                          "text": "Offsetfehler",
                                          "variable": None},
                     "amplification_checkbox": {"name": "amplification",
                                                "text": "Verstärkungsfehler",
                                                "variable": None},
                     "linearity_checkbox": {"name": "linearity",
                                            "text": "Linearitätsfehler",
                                            "variable": None},
                     "offset_scale": {"name": "offset", 
                                      "variable": None,
                                      "from": -100,
                                      "to": 100},
                     "amplification_scale": {"name": "amplification", 
                                             "variable": None,
                                             "from": -100,
                                             "to": 100},
                     "linearity_scale": {"name": "linearity", 
                                         "variable": None,
                                         "from": -25,
                                         "to": 25}}    
    
    def __init__(self, title = "Test Window"):
        super().__init__()
        self.init_window(title)
        self.init_params()
        self.init_figure()
        self.init_axes()
        self.create_widgets()
        self.place_widgets()
        self.init_widgets()
    
    def init_window(self, title):
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
        self.figure = Figure(figsize=(6, 4), dpi=100)
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
        self.update_graph()
        self.axes.clear()
        self.axes.set_title(self.axes_params["title"])
        self.axes.set_xlabel(self.axes_params["xlabel"])
        self.axes.set_ylabel(self.axes_params["ylabel"])
        self.axes.autoscale(False)
        self.axes.grid()
        self.axes.minorticks_on()
        self.axes.set_xbound(lower = 0, upper = self.axes_params["bounds"])
        self.axes.set_ybound(lower = 0, upper = self.axes_params["bounds"])
        self.axes.plot(self.graphs["x"], 
                       self.graphs["y"], 
                       label = self.axes_params["plot1"]["label"], 
                       color = self.axes_params["plot1"]["color"], 
                       linestyle = self.axes_params["plot1"]["linestyle"])
        self.axes.plot(self.graphs["x"], 
                       self.graphs["y_ideal"], 
                       label = self.axes_params["plot2"]["label"], 
                       color = self.axes_params["plot2"]["color"], 
                       linestyle = self.axes_params["plot2"]["linestyle"])
        self.axes.legend(loc=self.axes_params["legend_position"])
    
    def update_graph(self):
        a = self.widget_params["offset_scale"]["variable"].get() if self.widget_params['offset_checkbox']["variable"].get() else 0
        b = 1 + self.widget_params["amplification_scale"]["variable"].get()/(100 if self.widget_params["amplification_scale"]["variable"].get() < 0 else 10) \
        if self.widget_params['amplification_checkbox']["variable"].get() else 1
        c = self.widget_params["linearity_scale"]["variable"].get() if self.widget_params['linearity_checkbox']["variable"].get() else 0
        d = self.axes_params["bounds"]/2
        
        for x in range(0, self.axes_params["bounds"]+1):
            self.graphs["y"][x] = a + b*x - c*((x/d - 1)**2 - 1)

if __name__ == "__main__":
    exercise_03 = TKWindow(window_title)
    exercise_03.window_loop()