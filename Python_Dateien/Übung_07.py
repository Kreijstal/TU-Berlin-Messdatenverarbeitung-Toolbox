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

window_title = "Übung 07 - Messbrücke"

class TKWindow(tk.Tk):
    """Class to generate TKinter Window
    """        
    f = 50 # Frequency of the Base Signal u_0
    figure_params = {"figsize": (8,5),
                     "title 1": "Signal Verläufe",
                     "xlabel 1": "t in s",
                     "ylabel 1": "U in V",
                     "title 2": "XY-Betrieb",
                     "xlabel 2": "$U_B$ in V",
                     "ylabel 2": "$U_=$ in V",
                     "bounds": 100,
                     "legend_position": "upper right"}
    
    graphs = {"t": np.linspace(0, figure_params["bounds"], figure_params["bounds"]+1),
              "u_0": {"curve": np.zeros(figure_params["bounds"]+1), 
                      "label": "$u_0$", 
                      "color": "blue",
                      "linestyle": "solid"},
              "u_b": {"curve": np.zeros(figure_params["bounds"]+1),
                      "label": "$u_B$", 
                      "color": "red",
                      "linestyle": "solid"}}
    
    widgets = {"picture": {"self": "",
                           "side": tk.LEFT,
                           "image": "",
                           "path": __file__+"/../Messbruecke.png"},
               "label_u0": {"self": "",
                            "side": tk.LEFT,
                            "text": "û_0 in V:"},
               "label_z1": {"self": "",
                            "side": tk.LEFT,
                            "text": "Z_1 in Ω:"},
               "label_z2": {"self": "",
                            "side": tk.LEFT,
                            "text": "Z_2 in Ω:"},
               "label_z3": {"self": "",
                            "side": tk.LEFT,
                            "text": "Z_3 in Ω:"},
               "label_z4": {"self": "",
                            "side": tk.LEFT,
                            "text": "Z_4 in Ω:"},
               "entry_u0": {"self": "",
                            "side": tk.RIGHT,
                            "variable": "",
                            "old_value": ""},
               "entry_z1": {"self": "",
                            "side": tk.RIGHT,
                            "variable": "",
                            "old_value": ""},
               "entry_z2": {"self": "",
                            "side": tk.RIGHT,
                            "variable": "",
                            "old_value": ""},
               "entry_z3": {"self": "",
                            "side": tk.RIGHT,
                            "variable": "",
                            "old_value": ""},
               "entry_z4": {"self": "",
                            "side": tk.RIGHT,
                            "variable": "",
                            "old_value": ""}}
    
    measurement_bridge_values = {"u_0": 0.0+0.0j,
                                 "z_1": 0.0+0.0j,
                                 "z_2": 0.0+0.0j,
                                 "z_3": 0.0+0.0j,
                                 "z_4": 0.0+0.0j,
                                 "i_12": 0.0+0.0j,
                                 "i_34": 0.0+0.0j,
                                 "u_1": 0.0+0.0j,
                                 "u_2": 0.0+0.0j,
                                 "u_3": 0.0+0.0j,
                                 "u_4": 0.0+0.0j,
                                 "u_b": 0.0+0.0j}

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
        self.frame_left = tk.Frame(self.frame)
        self.frame_left.pack(side=tk.LEFT)
        self.frame_row_1 = tk.Frame(self.frame_left)
        self.frame_row_1.pack()
        self.frame_row_2 = tk.Frame(self.frame_left)
        self.frame_row_2.pack()
        self.frame_row_3 = tk.Frame(self.frame_left)
        self.frame_row_3.pack()
        self.frame_row_4 = tk.Frame(self.frame_left)
        self.frame_row_4.pack()
        self.frame_row_5 = tk.Frame(self.frame_left)
        self.frame_row_5.pack()
        self.frame_row_6 = tk.Frame(self.frame_left)
        self.frame_row_6.pack()
    
    def init_params(self):
        """Initialize widget variables befor widget creation.
        """      
        self.widgets["picture"]["image"] = tk.PhotoImage(file=self.widgets["picture"]["path"])
        
        self.widgets["entry_u0"]["variable"] = tk.StringVar()
        self.widgets["entry_z1"]["variable"] = tk.StringVar()
        self.widgets["entry_z2"]["variable"] = tk.StringVar()
        self.widgets["entry_z3"]["variable"] = tk.StringVar()
        self.widgets["entry_z4"]["variable"] = tk.StringVar()
    
    def create_widgets(self):
        """Creates all widgets for the window.
        """        
        self.widgets["picture"]["self"] = tk.Canvas(self.frame, width=600)
        
        self.label_info1 = tk.Label(self.frame_row_2, text="Darstellung von komplexen Zahlen:", padx=30).pack(side=tk.TOP)
        self.label_info1 = tk.Label(self.frame_row_2, text="Trennzeichen ist ein Punkt \".\"", padx=30).pack(side=tk.TOP)
        self.label_info1 = tk.Label(self.frame_row_2, text="Zeichen für komplexen Anteil ist \"j\"", padx=30).pack(side=tk.TOP)
        self.label_info1 = tk.Label(self.frame_row_2, text="Beispiel: -5.5+10j", padx=30).pack(side=tk.TOP)
        
        self.widgets["label_u0"]["self"] = tk.Label(self.frame_row_1, text=self.widgets["label_u0"]["text"], padx=30, pady=10)
        self.widgets["label_z1"]["self"] = tk.Label(self.frame_row_3, text=self.widgets["label_z1"]["text"], padx=30, pady=10)
        self.widgets["label_z2"]["self"] = tk.Label(self.frame_row_4, text=self.widgets["label_z2"]["text"], padx=30, pady=10)
        self.widgets["label_z3"]["self"] = tk.Label(self.frame_row_5, text=self.widgets["label_z3"]["text"], padx=30, pady=10)
        self.widgets["label_z4"]["self"] = tk.Label(self.frame_row_6, text=self.widgets["label_z4"]["text"], padx=30, pady=10)
        
        self.widgets["entry_u0"]["self"] = tk.Entry(self.frame_row_1, textvariable=self.widgets["entry_u0"]["variable"])
        self.widgets["entry_z1"]["self"] = tk.Entry(self.frame_row_3, textvariable=self.widgets["entry_z1"]["variable"])
        self.widgets["entry_z2"]["self"] = tk.Entry(self.frame_row_4, textvariable=self.widgets["entry_z2"]["variable"])
        self.widgets["entry_z3"]["self"] = tk.Entry(self.frame_row_5, textvariable=self.widgets["entry_z3"]["variable"])
        self.widgets["entry_z4"]["self"] = tk.Entry(self.frame_row_6, textvariable=self.widgets["entry_z4"]["variable"])
    
    def init_widgets(self):
        """Initialize widget variables after widget creation.
        """        
        self.widgets["picture"]["self"].create_image(300, 160, image=self.widgets["picture"]["image"])
    
    def init_figure(self):
        """Initialize matplotlib figure and corresponding widget.
        """        
        self.figure = Figure(figsize=self.figure_params["figsize"], dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self.frame_bottom)
    
    def init_axes(self):
        """Initialize figure axes.
        """        
        self.axes1 = self.figure.add_subplot(1, 2, 1)   # plot of u_o and u_b over time
        self.axes2 = self.figure.add_subplot(1, 2, 2)   # plot of u_0 over u_b
        
        self.axes1.clear()
        self.axes1.set_title(self.figure_params["title 1"])
        self.axes1.set_xlabel(self.figure_params["xlabel 1"])
        self.axes1.set_ylabel(self.figure_params["ylabel 1"])
        self.axes1.grid()
        self.axes1.minorticks_on()
        self.plot_axes(self.axes1, self.graphs["u_0"])
        self.plot_axes(self.axes1, self.graphs["u_b"])
        self.axes1.legend(loc=self.figure_params["legend_position"])
        
        self.axes2.clear()
        self.axes2.set_title(self.figure_params["title 2"])
        self.axes2.set_xlabel(self.figure_params["xlabel 2"])
        self.axes2.set_ylabel(self.figure_params["ylabel 2"])
        self.axes2.autoscale(False)
        self.axes2.grid()
        self.axes2.minorticks_on()
        self.axes2.set_xbound(lower = 0, upper = self.figure_params["bounds"])
        self.axes2.set_ybound(lower = -0.5, upper = 0.5)
        self.figure.tight_layout()
        self.plot_axes(self.axes2, self.graphs["u_0"], self.graphs["u_b"])
    
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
        if self.check_for_changed_entry():
            self.update_measurement_bridge_values()
            self.update_graphs()
            
            self.axes1.clear()
            self.axes1.set_title(self.figure_params["title 1"])
            self.axes1.set_xlabel(self.figure_params["xlabel 1"])
            self.axes1.set_ylabel(self.figure_params["ylabel 1"])
            self.axes1.grid()
            self.axes1.minorticks_on()
            self.plot_axes(self.axes1, self.graphs["u_0"])
            self.plot_axes(self.axes1, self.graphs["u_b"])
            self.axes1.legend(loc=self.figure_params["legend_position"])
            
            self.axes2.clear()
            self.axes2.set_title(self.figure_params["title 2"])
            self.axes2.set_xlabel(self.figure_params["xlabel 2"])
            self.axes2.set_ylabel(self.figure_params["ylabel 2"])
            self.axes2.autoscale(False)
            self.axes2.grid()
            self.axes2.minorticks_on()
            self.axes2.set_xbound(lower = -np.absolute(self.measurement_bridge_values["u_0"]), upper = np.absolute(self.measurement_bridge_values["u_0"]))
            self.axes2.set_ybound(lower = -np.absolute(self.measurement_bridge_values["u_0"]), upper = np.absolute(self.measurement_bridge_values["u_0"]))
            self.figure.tight_layout()
            self.plot_axes(self.axes2, self.graphs["u_0"], self.graphs["u_b"])
    
    def check_for_changed_entry(self):
        """Method to check all input variables for updates/changes

        Returns:
            bool: Result of check for changed variables
        """        
        for entry in self.widgets:
            if "entry" in entry:
                if self.entry_changed(entry):
                    new_value = self.widgets[entry]["variable"].get()
                    try:
                        complex(new_value)
                    except ValueError:
                        self.widgets[entry]["self"].config(fg="red")
                    else:
                        self.widgets[entry]["self"].config(fg="black")
                        self.widgets[entry]["old_value"] = new_value
                        return True
        return False
    
    def entry_changed(self, entry):
        """Compares current value of given variable with old value

        Args:
            entry (dict): Dictionary containing all variables of corresponding widget.

        Returns:
            bool: Result of comparison
        """        
        return self.widgets[entry]["variable"].get() != self.widgets[entry]["old_value"]
    
    def update_measurement_bridge_values(self):
        """Writes the complex number from entry widget into corresponding variable.
        """        
        self.measurement_bridge_values["u_0"]= complex(self.widgets["entry_u0"]["variable"].get()) if self.widgets["entry_u0"]["variable"].get() != "" else 0.0+0.0j
        self.measurement_bridge_values["z_1"]= complex(self.widgets["entry_z1"]["variable"].get()) if self.widgets["entry_z1"]["variable"].get() != "" else 0.0+0.0j
        self.measurement_bridge_values["z_2"]= complex(self.widgets["entry_z2"]["variable"].get()) if self.widgets["entry_z2"]["variable"].get() != "" else 0.0+0.0j
        self.measurement_bridge_values["z_3"]= complex(self.widgets["entry_z3"]["variable"].get()) if self.widgets["entry_z3"]["variable"].get() != "" else 0.0+0.0j
        self.measurement_bridge_values["z_4"]= complex(self.widgets["entry_z4"]["variable"].get()) if self.widgets["entry_z4"]["variable"].get() != "" else 0.0+0.0j
        
        z_12 = self.measurement_bridge_values["z_1"]+self.measurement_bridge_values["z_2"]
        z_34 = self.measurement_bridge_values["z_3"]+self.measurement_bridge_values["z_4"]

        self.measurement_bridge_values["i_12"]= self.measurement_bridge_values["u_0"]/z_12 if z_12 != 0.0+0.0j else 0.0+0.0j
        self.measurement_bridge_values["i_34"]= self.measurement_bridge_values["u_0"]/z_34 if z_34 != 0.0+0.0j else 0.0+0.0j
        
        self.measurement_bridge_values["u_1"]= self.measurement_bridge_values["u_0"]-self.measurement_bridge_values["z_2"]*self.measurement_bridge_values["i_12"]
        self.measurement_bridge_values["u_2"]= self.measurement_bridge_values["u_0"]-self.measurement_bridge_values["z_1"]*self.measurement_bridge_values["i_12"]
        self.measurement_bridge_values["u_3"]= self.measurement_bridge_values["u_0"]-self.measurement_bridge_values["z_4"]*self.measurement_bridge_values["i_34"]
        self.measurement_bridge_values["u_4"]= self.measurement_bridge_values["u_0"]-self.measurement_bridge_values["z_3"]*self.measurement_bridge_values["i_34"]
        
        self.measurement_bridge_values["u_b"]= self.measurement_bridge_values["u_3"]-self.measurement_bridge_values["u_1"]
    
    def update_graphs(self):
        """Update graph values.
        """        
        for t in self.graphs["t"]:
            print(np.angle(self.measurement_bridge_values["u_0"]))
            self.graphs["u_0"]["curve"][int(t)] = np.absolute(self.measurement_bridge_values["u_0"])*np.sin(2*np.pi*self.f*t/1000+np.angle(self.measurement_bridge_values["u_0"]))
            self.graphs["u_b"]["curve"][int(t)] = np.absolute(self.measurement_bridge_values["u_b"])*np.sin(2*np.pi*self.f*t/1000+np.angle(self.measurement_bridge_values["u_b"]))
    
    def plot_axes(self, axes, graph, x=None):
        """Plots given graph in given axes object.

        Args:
            axes (matplotlib axes object): Ploting in this axes object
            graph (dict): Graph to plot
            x (dict, optional): values for x-axis. Defaults to None, in this case a linear series is used.
        """    
        axes.plot(self.graphs["t"] if x is None else x["curve"], 
                  graph["curve"], 
                  label = graph["label"], 
                  color = graph["color"], 
                  linestyle = graph["linestyle"])

if __name__ == "__main__":
    exercise_07 = TKWindow(window_title)
    exercise_07.window_loop()