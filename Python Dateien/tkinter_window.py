# https://www.tutorialspoint.com/python/python_gui_programming.htm

import tkinter as tk
import numpy as np
import matplotlib as mpl
#import matplotlib.animation as animation
#from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

window_title = "Übung 03 - Statische Eigenschaften von Messystemen"

class _graph:
    values = []
    subplot: int
    label: str
    color: str
    linestyle: str

    def __init__(self, values, 
                       subplot=111,
                       label="label",
                       color="blue",
                       linestyle="-"):
        self.values = values
        self.subplot = subplot
        self.label = label
        self.color = color
        self.linestyle = linestyle

class _radiobutton:
    name: str
    variable: tk.IntVar
    widget: tk.Radiobutton
    
    def __init__(self, parent, name=""):
        

class _checkbox:
    name: str
    variable: tk.BooleanVar
    widget: tk.Checkbutton
    toggled: bool
    
    def __init__(self, parent, name="checkbox"):
        self.name = name
        self.variable = tk.BooleanVar()
        self.widget = tk.Checkbutton(parent,
                                     text=self.name,
                                     variable=self.variable, 
                                     command=self._onClick,
                                     onvalue=True, 
                                     offvalue=False)
        self.toggled = False
    
    def _onClick(self):
        self.toggled = True
    
    def getValue(self):
        return self.widget.get()
    
    def isToggled(self):
        toggled = self.toggled
        self.toggled = False
        return toggled

class _scale:
    name: str
    variable: tk.DoubleVar
    widget: tk.Scale
    
    def __init__(self, parent, name="scale", from_=100, to=100):
        self.name = name
        self.variable = tk.DoubleVar()
        self.widget = tk.Scale(parent,
                               showvalue=1,
                               orient='horizontal', 
                               variable=self.variable, 
                               from_=from_, 
                               to=to)
    
    def getValue(self):
        return self.widget.get()
    
    def resetValue(self):
        self.widget.set(0)

class TKWindow(tk.Tk):
    frame: tk.Frame
    figure: mpl.figure.Figure
    figure_canvas: FigureCanvasTkAgg
    radiobuttons: [tk.Radiobutton]
    checkbuttons: [tk.Checkbutton]
    scales: [tk.Scales]
    control_elemts_frames: [tk.Frame]
    
    def __init__(self, figure, axis = None, title = "Test Window", **kwargs):
        super().__init__()
        self.init_window(title)
        self.init_figure(figure)
        self.init_axes()
        self.init_widgets(**kwargs)
    
    def init_window(self, title):
        self.title(title)
        self.resizable(False, False)
        self.frame = tk.Frame(self).pack()
        #self.columnconfigure(0, weight=0)
        #self.columnconfigure(1, weight=10)
    
    # def init_figure(self):
    #     self.figure = Figure(figsize=self.figure_params["figsize"], dpi=100)
    #     self.figure_canvas = FigureCanvasTkAgg(self.figure, self.frame)
    
    # def init_axes(self):
    #     self.axes = self.figure.add_subplot()
    
    def init_widgets(self, **kwargs):
        self.figure_canvas.get_tk_widget().pack(side="left")
        self.control_elemts_frames[0] = tk.Frame(self.frame).pack(side="right", fill="X")
        for key, value in kwargs.items():
            if key == "radiobuttons":
                self.control_elemts_frames.append(tk.Frame(self.control_elemts_frames[0]))
                for radiobutton in value:
                    self.radiobuttons.append()
                    
                    self.control_elemts_frames[-1]
        if hasattr(self, "")
    
    def place_widgets(self):
        
        self.checkboxes['offset'].grid(row = 1, column = 0, sticky = 'w', pady = 10, padx = 40)
        self.checkboxes['amplification'].grid(row = 2, column = 0, sticky = 'w', pady = 10, padx = 40)
        self.checkboxes['linearity'].grid(row = 3, column = 0, sticky = 'w', pady = 10, padx = 40)
        
        self.scales['offset'].grid(row = 1, column = 1, sticky = 'ew', pady = 10, padx = 40)
        self.scales['amplification'].grid(row = 2, column = 1, sticky = 'ew', pady = 10, padx = 40)
        self.scales['linearity'].grid(row = 3, column = 1, sticky = 'ew', pady = 10, padx = 40)
    
    def old_init_widgets(self):
        [self.checkboxes[checkbox].select() for checkbox in self.checkboxes]
    
    def window_loop(self):
        self.animation_object = animation.FuncAnimation(self.figure, self.animate, interval = 100)
        self.mainloop()
    
    def animate(self, i):
        self.update_graphs()
        self.axes.clear()
        self.axes.set_title(self.figure_params["title"])
        self.axes.set_xlabel(self.figure_params["xlabel"])
        self.axes.set_ylabel(self.figure_params["ylabel"])
        self.axes.autoscale(False)
        self.axes.grid()
        self.axes.minorticks_on()
        self.axes.set_xbound(lower = 0, upper = self.figure_params["bounds"])
        self.axes.set_ybound(lower = 0, upper = self.figure_params["bounds"])
        self.plot_axes(self.graphs["y"])
        self.plot_axes(self.graphs["y_ideal"])
        self.plot_axes(self.graphs["y_offset_error"]) if self.widget_params['offset_checkbox']["variable"].get() else None
        self.plot_axes(self.graphs["y_amplification_error"]) if self.widget_params['amplification_checkbox']["variable"].get() else None
        self.plot_axes(self.graphs["y_linearity_error"]) if self.widget_params['linearity_checkbox']["variable"].get() else None
        self.axes.legend(loc=self.figure_params["legend_position"])
    
    def update_graphs(self):
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
    
    def plot_axes(self, plot):
        self.axes.plot(self.graphs["x"], 
                       plot["curve"], 
                       label = plot["label"], 
                       color = plot["color"], 
                       linestyle = plot["linestyle"])

if __name__ == "__main__":
    exercise_03 = TKWindow(window_title)
    exercise_03.window_loop()
