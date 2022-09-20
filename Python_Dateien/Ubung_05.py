# Notes
# https://www.tutorialspoint.com/python/python_gui_programming.htm

# ToDo
# ADU Kennlinie
# Auflösung (Ausrechnen)
# Veränderbare Bit Zahl
# Quantisierungsrauschen


import tkinter as tk
import numpy as np
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

window_title = "Übung 05 - Digitale Messdatenerfassung mittels ADU"

class TKWindow(tk.Tk):
    figure_params = {"figsize": (8,5),
                     "title 1": "ADU Kennlinie",
                     "xlabel 1": "Input",
                     "ylabel 1": "Codes",
                     "title 2": "Kennlinien Delta",
                     "xlabel 2": "Input",
                     "ylabel 2": "\delta Codes",
                     "bounds": 100,
                     "legend_position": "upper left"}
    # ToDo
    graphs = {"x": np.linspace(0, figure_params["bounds"], figure_params["bounds"]+1),
              "y": {"curve": np.zeros(figure_params["bounds"]+1), 
                    "label": "reale Kennlinie", 
                    "color": "blue",
                    "linestyle": "solid"},
              "y_ideal": {"curve": np.linspace(0, figure_params["bounds"], figure_params["bounds"]+1), 
                          "label": "ideale Kennlinie", 
                          "color": "red",
                          "linestyle": "dashed"},
              "y_offset_error": {"curve": np.linspace(0, figure_params["bounds"], figure_params["bounds"]+1), 
                                 "label": "Kennlinie mit Offset-Fehler", 
                                 "color": "green",
                                 "linestyle": "dashdot"},
              "y_amplification_error": {"curve": np.linspace(0, figure_params["bounds"], figure_params["bounds"]+1), 
                                        "label": "Kennlinie mit Verstärkungs-Fehler", 
                                        "color": "yellowgreen",
                                        "linestyle": "dashdot"},
              "y_linearity_error": {"curve": np.linspace(0, figure_params["bounds"], figure_params["bounds"]+1),
                                    "label": "Kennlinie mit Linearitäts-Fehler", 
                                    "color": "darkgreen",
                                    "linestyle": "dashdot"}}
    
    bits_scale_params = {"variable": None,
                         "from": 0,
                         "to": 128}
    resolution_text = "Resolution: "

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
        # self.columnconfigure(0, weight=0)
        # self.columnconfigure(1, weight=10)
    
    def init_params(self):
        self.widget_params["adu_bits"]["variable"] = tk.DoubleVar()
    
    def init_figure(self):
        self.figure = Figure(figsize=self.figure_params["figsize"], dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)
    
    def init_axes(self):
        self.axes1 = self.figure.add_subplot(1, 2, 1)   # Characteristics and ideal curve
        self.axes2 = self.figure.add_subplot(1, 2, 2)   # Delta between characteristic and ideal curve
        # self.axes3 = self.figure.add_subplot(2, 2, 4)
    
    def create_widgets(self):
        self.bits_scale = tk.Scale(self, 
                                   showvalue=1, 
                                   orient='horizontal', 
                                   variable=self.widget_params["adu_bits"]["variable"], 
                                   from_=self.widget_params["adu_bits"]["from"], 
                                   to=self.widget_params["adu_bits"]["to"])
        self.resolution = tk.Text(self)#, padx=5, pady=5)

    def place_widgets(self):
        self.figure_canvas.get_tk_widget().grid(row = 0, column = 0, columnspan = 1)
        
        self.bits_scale.grid(row = 1, column = 1, sticky = 'ew', pady = 10, padx = 40)
        self.resolution.grid(row = 2, column = 1, sticky = 'ew', pady = 10, padx = 40)
    
    def init_widgets(self):
        self.resolution.insert(0, self.resolution_text)
    
    def window_loop(self):
        self.animation_object = animation.FuncAnimation(self.figure, self.animate, interval = 100)
        self.mainloop()
    
    def animate(self, i):  # ToDo
        self.update_graphs()
        self.axes1.clear()
        self.axes1.set_title(self.figure_params["title 1"])
        self.axes1.set_xlabel(self.figure_params["xlabel 1"])
        self.axes1.set_ylabel(self.figure_params["ylabel 1"])
        self.axes1.autoscale(False)
        self.axes1.grid()
        self.axes1.minorticks_on()
        self.axes1.set_xbound(lower = 0, upper = self.figure_params["bounds"])
        self.axes1.set_ybound(lower = 0, upper = self.figure_params["bounds"])
        self.plot_axes(self.graphs["y"])
        self.plot_axes(self.graphs["y_ideal"])
        self.plot_axes(self.graphs["y_offset_error"]) if self.widget_params['offset_checkbox']["variable"].get() else None
        self.plot_axes(self.graphs["y_amplification_error"]) if self.widget_params['amplification_checkbox']["variable"].get() else None
        self.plot_axes(self.graphs["y_linearity_error"]) if self.widget_params['linearity_checkbox']["variable"].get() else None
        self.axes1.legend(loc=self.figure_params["legend_position"])
        
        self.axes2.clear()
        self.axes2.set_title(self.figure_params["title 2"])
        self.axes2.set_xlabel(self.figure_params["xlabel 2"])
        self.axes2.set_ylabel(self.figure_params["ylabel 2"])
        self.axes2.autoscale(False)
        self.axes2.grid()
        self.axes2.minorticks_on()
        self.axes2.set_xbound(lower = 0, upper = self.figure_params["bounds"])
        self.axes2.set_ybound(lower = 0, upper = self.figure_params["bounds"])
    
    def update_graphs(self): # ToDo
        a = self.widget_params["offset_scale"]["variable"].get() if self.widget_params['offset_checkbox']["variable"].get() else 0
        b = 1 + self.widget_params["amplification_scale"]["variable"].get()/(100 if self.widget_params["amplification_scale"]["variable"].get() < 0 else 10) \
        if self.widget_params['amplification_checkbox']["variable"].get() else 1
        c = self.widget_params["linearity_scale"]["variable"].get() if self.widget_params['linearity_checkbox']["variable"].get() else 0
        d = self.figure_params["bounds"]/2
        
        for x in range(0, self.figure_params["bounds"]+1):
            self.graphs["y"]["curve"][x] = a + b*x - c*((x/d - 1)**2 - 1)
            self.graphs["y_offset_error"]["curve"][x] = a + x
            self.graphs["y_amplification_error"]["curve"][x] = b*x
            self.graphs["y_linearity_error"]["curve"][x] = x - c*((x/d - 1)**2 - 1)
    
    def plot_axes(self, graph): # ToDo
        self.axes.plot(self.graphs["x"], 
                       graph["curve"], 
                       label = graph["label"], 
                       color = graph["color"], 
                       linestyle = graph["linestyle"])

if __name__ == "__main__":
    exercise_03 = TKWindow(window_title)
    exercise_03.window_loop()