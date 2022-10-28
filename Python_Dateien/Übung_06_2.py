# -*- coding: utf-8 -*-
"""
Leistungsmessung
Anzeige der Leistungskurven für einen einstellbaren Verbraucher, linear oder nichtlinear mit Oberwellen.

von Erik Tröndle

"""


import tkinter as tk
import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

window_title = "Übung 06 - Leistungsmessung"

class TKWindow(tk.Tk):
    """Class to generate TKinter Window
    """
    font_size = 16
    
    figure_params = {"figsize": (12,7),
                     "title": "Signal Verläufe",
                     "xlabel": "t in s",
                     "ylabel 1": "U in V",
                     "ylabel 2": "I in A",
                     "ylabel 3": "P in W, S in VA, Q in VAr",
                     "bounds": 100,
                     "legend_position": "upper right"}
    
    graphs = {"t": np.linspace(0, figure_params["bounds"], figure_params["bounds"]+1),
              "u": {"curve": np.zeros(figure_params["bounds"]+1), 
                      "label": "Spannung", 
                      "color": "blue",
                      "linestyle": "solid"},
              "i": {"curve": np.zeros(figure_params["bounds"]+1),
                      "label": "$Strom$", 
                      "color": "red",
                      "linestyle": "solid"},
              "p": {"curve": np.zeros(figure_params["bounds"]+1), 
                      "label": "$Wirkleistung$", 
                      "color": "orange",
                      "linestyle": "solid"},
              "s": {"curve": np.zeros(figure_params["bounds"]+1), 
                      "label": "$Scheinleistung$", 
                      "color": "green",
                      "linestyle": "solid"},
              "q": {"curve": np.zeros(figure_params["bounds"]+1), 
                      "label": "$Blindleistung$", 
                      "color": "purple",
                      "linestyle": "solid"}}
    
    widgets = {"label_f": {"self": "",
                           "side": tk.LEFT,
                           "text": "Frequenz f in Hz:"},
               "label_a": {"self": "",
                           "side": tk.LEFT,
                           "text": "Amplitude in V:"},
               "label_z": {"self": "",
                           "side": tk.LEFT,
                           "text": "Widerstand Z in Ω:"},
               "label_theta": {"self": "",
                               "side": tk.LEFT,
                               "text": "Phasenanschnittwinkel ϑ in °:"},
               "entry_f": {"self": "",
                           "side": tk.LEFT,
                           "variable": "",
                           "old_value": "0"},
               "entry_a": {"self": "",
                           "side": tk.LEFT,
                           "variable": "",
                           "old_value": "0"},
               "entry_z": {"self": "",
                           "side": tk.LEFT,
                           "variable": "",
                           "old_value": "0"},
               "scale_theta": {"self": "",
                               "side": tk.LEFT,
                               "variable": "",
                               "old_value": 0,
                               "from": -180,
                               "to": 180}}

    def __init__(self, title = "Test Window"):
        """Override for standard initialization method

        Args:
            title (str, optional): Setzt den Titel des Fensters. Defaults to "Test Window".
        """        
        super().__init__()
        self.init_window(title)
        self.init_frames()
        self.init_params()
        self.create_widgets()
        self.init_widgets()
        self.init_figure()
        self.init_axes()
        self.place_widgets()
    
    def init_window(self, title):
        """Set´s parameters for the window.

        Args:
            title (str): Setzt den Titel des Fensters.
        """          
        self.title(title)
        self.resizable(False, False)
    
    def init_frames(self):
        """Initialize Frames for Window Layout
        """        
        self.frame = tk.Frame(self)
        self.frame.pack()
        self.frame_bottom = tk.Frame(self.frame)
        self.frame_bottom.pack(side=tk.BOTTOM)
        self.frame_right = tk.Frame(self.frame)
        self.frame_right.pack(side=tk.RIGHT)
        self.frame_left_row_1 = tk.Frame(self.frame)
        self.frame_left_row_1.pack(fill=tk.X, expand=True)
        self.frame_left_row_2 = tk.Frame(self.frame)
        self.frame_left_row_2.pack(fill=tk.X, expand=True)
        self.frame_left_row_3 = tk.Frame(self.frame)
        self.frame_left_row_3.pack(fill=tk.X, expand=True)
        self.frame_left_row_4 = tk.Frame(self.frame)
        self.frame_left_row_4.pack(fill=tk.X, expand=True)
        self.frame_right_row_1 = tk.Frame(self.frame_right)
        self.frame_right_row_1.pack()
        self.frame_right_row_2 = tk.Frame(self.frame_right)
        self.frame_right_row_2.pack()
        self.frame_right_row_3 = tk.Frame(self.frame_right)
        self.frame_right_row_3.pack()
        self.frame_right_row_4 = tk.Frame(self.frame_right)
        self.frame_right_row_4.pack()
    
    def init_params(self):
        """Initialize widget variables befor widget creation.
        """
        self.widgets["entry_f"]["variable"] = tk.StringVar()
        self.widgets["entry_a"]["variable"] = tk.StringVar()
        self.widgets["entry_z"]["variable"] = tk.StringVar()
        self.widgets["scale_theta"]["variable"] = tk.DoubleVar()
    
    def create_widgets(self):
        """Creates all widgets for the window.
        """
        self.label_info1 = tk.Label(self.frame_right_row_1, text="Darstellung von komplexen Zahlen:", font=("Arial", self.font_size), padx=30).pack(side=tk.LEFT)
        self.label_info2 = tk.Label(self.frame_right_row_2, text="Trennzeichen ist ein Punkt \".\"", font=("Arial", self.font_size), padx=30).pack(side=tk.LEFT)
        self.label_info3 = tk.Label(self.frame_right_row_3, text="Zeichen für komplexen Anteil ist \"j\"", font=("Arial", self.font_size), padx=30).pack(side=tk.LEFT)
        self.label_info4 = tk.Label(self.frame_right_row_4, text="Beispiel: -5.5+10j", font=("Arial", self.font_size), padx=30).pack(side=tk.LEFT)
        
        self.widgets["label_f"]["self"] = tk.Label(self.frame_left_row_1, text=self.widgets["label_f"]["text"], font=("Arial", self.font_size), padx=30, pady=10)
        self.widgets["label_a"]["self"] = tk.Label(self.frame_left_row_2, text=self.widgets["label_a"]["text"], font=("Arial", self.font_size), padx=30, pady=10)
        self.widgets["label_z"]["self"] = tk.Label(self.frame_left_row_3, text=self.widgets["label_z"]["text"], font=("Arial", self.font_size), padx=30, pady=10)
        self.widgets["label_theta"]["self"] = tk.Label(self.frame_left_row_4, text=self.widgets["label_theta"]["text"], font=("Arial", self.font_size), padx=30, pady=10)
        
        self.widgets["entry_f"]["self"] = tk.Entry(self.frame_left_row_1, textvariable=self.widgets["entry_f"]["variable"], font=("Arial", self.font_size))
        self.widgets["entry_a"]["self"] = tk.Entry(self.frame_left_row_2, textvariable=self.widgets["entry_a"]["variable"], font=("Arial", self.font_size))
        self.widgets["entry_z"]["self"] = tk.Entry(self.frame_left_row_3, textvariable=self.widgets["entry_z"]["variable"], font=("Arial", self.font_size))
        self.widgets["scale_theta"]["self"] = tk.Scale(self.frame_left_row_4,  
                                                       showvalue=1, 
                                                       orient='horizontal', 
                                                       length= 400,
                                                       variable=self.widgets["scale_theta"]["variable"], 
                                                       from_=self.widgets["scale_theta"]["from"], 
                                                       to=self.widgets["scale_theta"]["to"],
                                                       font=("Arial", self.font_size))
    
    def init_widgets(self):
        """Initialize widget variables after widget creation.
        """
        self.widgets["entry_f"]["self"].insert(0, "50")
        self.widgets["entry_a"]["self"].insert(0, "1")
        self.widgets["entry_z"]["self"].insert(0, "1000")
    
    def init_figure(self):
        """Initialize matplotlib figure and corresponding widget.
        """        
        self.figure = plt.figure(figsize=self.figure_params["figsize"], dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self.frame_bottom)
    
    def init_axes(self):
        """Initialize figure axes.
        """        
        self.axes = self.figure.add_subplot()
        self.figure.subplots_adjust(right=0.75)
        
        self.twin1 = self.axes.twinx()
        self.twin2 = self.axes.twinx()
        
        # Offset the right spine of twin2.  The ticks and label have already been
        # placed on the right by twinx above.
        self.twin2.spines.right.set_position(("axes", 1.2))
        
        self.axes.clear()
        self.axes.set_title(self.figure_params["title"])
        self.axes.set_xlabel(self.figure_params["xlabel"])
        self.axes.set_ylabel(self.figure_params["ylabel 1"])
        self.axes.grid()
        self.axes.minorticks_on()
        self.axes.yaxis.label.set_color(self.graphs["u"]["color"])
        self.axes.tick_params(axis="y", colors=self.graphs["u"]["color"])
        self.plot_axes(self.axes, self.graphs["u"])
        
        self.twin1.clear()
        self.twin1.set_ylabel(self.figure_params["ylabel 2"])
        # self.twin1.grid()
        # self.twin1.minorticks_on()
        self.axes.yaxis.label.set_color(self.graphs["i"]["color"])
        self.axes.tick_params(axis="y", colors=self.graphs["i"]["color"])
        self.plot_axes(self.twin1, self.graphs["i"])
        
        self.twin2.clear()
        self.twin2.set_ylabel(self.figure_params["ylabel 3"])
        # self.twin2.grid()
        # self.twin2.minorticks_on()
        self.plot_axes(self.twin2, self.graphs["p"])
        self.plot_axes(self.twin2, self.graphs["q"])
        self.plot_axes(self.twin2, self.graphs["s"])
    
    def place_widgets(self):
        """Place TKinter widgets.
        """        
        self.figure_canvas.get_tk_widget().pack()
        
        [self.widgets[widget]["self"].pack(side=self.widgets[widget]["side"]) for widget in self.widgets]
    
    def window_loop(self):
        """Startin animation and window loop.
        """        
        self.animation_object = animation.FuncAnimation(self.figure, self.animate, interval = 100)
        self.mainloop()
    
    def animate(self, i):
        """Method respnsible for animation. Updates axes objects and calls all necessary methods to draw graphs.

        Args:
            i (int): needed for animation
        """        
        if self.check_for_changed_input_values():
            self.update_graphs()
            
            self.figure.subplots_adjust(right=0.75)
            # Offset the right spine of twin2.  The ticks and label have already been
            # placed on the right by twinx above.
            self.twin2.spines.right.set_position(("axes", 1.2))
            
            self.axes.clear()
            self.axes.set_title(self.figure_params["title"])
            self.axes.set_xlabel(self.figure_params["xlabel"])
            self.axes.set_ylabel(self.figure_params["ylabel 1"])
            self.axes.grid()
            self.axes.minorticks_on()
            self.axes.yaxis.label.set_color(self.graphs["u"]["color"])
            self.axes.tick_params(axis="y", colors=self.graphs["u"]["color"])
            p_u = self.plot_axes(self.axes, self.graphs["u"])
            
            self.twin1.clear()
            self.twin1.set_ylabel(self.figure_params["ylabel 2"])
            # self.twin1.grid()
            # self.twin1.minorticks_on()
            self.axes.yaxis.label.set_color(self.graphs["i"]["color"])
            self.axes.tick_params(axis="y", colors=self.graphs["i"]["color"])
            p_i = self.plot_axes(self.twin1, self.graphs["i"])
            
            self.twin2.clear()
            self.twin2.set_ylabel(self.figure_params["ylabel 3"])
            # self.twin2.grid()
            # self.twin2.minorticks_on()
            p_p = self.plot_axes(self.twin2, self.graphs["p"])
            p_q = self.plot_axes(self.twin2, self.graphs["q"])
            p_s = self.plot_axes(self.twin2, self.graphs["s"])

            self.axes.legend(handles=[p_u, p_i, p_p, p_q, p_s], loc=self.figure_params["legend_position"])
    
    def check_for_changed_input_values(self):
        """Method to check all input variables for updates/changes

        Returns:
            bool: Result of check for changed variables
        """        
        for widget in self.widgets:
            if "entry" in widget or "scale" in widget:
                if self.value_changed(widget):
                    new_value = self.widgets[widget]["variable"].get()
                    try:
                        float(new_value) if "f" in widget else complex(new_value)
                    except ValueError:
                        self.widgets[widget]["self"].config(fg="red")
                    else:
                        self.widgets[widget]["self"].config(fg="black")
                        self.widgets[widget]["old_value"] = new_value
                        return True
        return False
    
    def value_changed(self, widget):
        """Compares current value of given variable with old value

        Args:
            widget (dict): Dictionary containing all variables of corresponding widget.

        Returns:
            bool: Result of comparison
        """        
        return self.widgets[widget]["variable"].get() != self.widgets[widget]["old_value"]
    
    def update_graphs(self):
        """Update graph values.
        """        
        for t in self.graphs["t"]:
            f = float(self.widgets["entry_f"]["variable"].get())
            u = complex(self.widgets["entry_a"]["variable"].get())
            z = complex(self.widgets["entry_z"]["variable"].get())
            theta = self.widgets["scale_theta"]["variable"].get()
            
            i = u/z
            a_u = np.absolute(u)
            phi_u = np.angle(u)
            a_i = np.absolute(u/z)
            phi_i = np.angle(u) - np.angle(z)
            phi_i2 = np.angle(i)                #test
            s = u*np.conjugate(i)
            a_s = np.absolute(s)
            phi_s = np.angle(s)
            p = np.real(s)
            a_p = np.absolute(p)
            phi_p = np.angle(p)
            q = np.imag(s)
            a_q = np.absolute(q)
            phi_q = np.angle(q)
            
            self.graphs["u"]["curve"][int(t)] = a_u*np.sin(2*np.pi*f*t/1000+phi_u)
            self.graphs["i"]["curve"][int(t)] = a_i*np.sin(2*np.pi*f*t/1000+phi_i)
            self.graphs["p"]["curve"][int(t)] = a_p*np.sin(2*np.pi*f*t/1000+phi_p)
            self.graphs["s"]["curve"][int(t)] = a_s*np.sin(2*np.pi*f*t/1000+phi_i)
            self.graphs["q"]["curve"][int(t)] = a_q*np.sin(2*np.pi*f*t/1000+phi_i)
    
    def plot_axes(self, axes, graph, x=None):
        """Plots given graph in given axes object.

        Args:
            axes (matplotlib.axes._subplots.AxesSubplot): Ploting in this axes object
            graph (dict): Graph to plot
            x (dict, optional): values for x-axis. Defaults to None, in this case a linear series is used.

        Returns:
            matplotlib.lines.Line2D: Plot object for further use.
        """        
        ax, = axes.plot(self.graphs["t"] if x is None else x["curve"], 
                        graph["curve"], 
                        label = graph["label"], 
                        color = graph["color"], 
                        linestyle = graph["linestyle"])
        return ax

if __name__ == "__main__":
    exercise_07 = TKWindow(window_title)
    exercise_07.window_loop()