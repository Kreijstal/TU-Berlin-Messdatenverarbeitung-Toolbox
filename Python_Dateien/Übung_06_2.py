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
                     "xlabel": "t in ms",
                     "ylabel 1": "U in V",
                     "ylabel 2": "I in A",
                     "ylabel 3": "P in W, S in VA, Q in VAr",
                     "bounds": 100,
                     "legend_position": "lower right"}
    
    graphs = {"t": np.linspace(0, figure_params["bounds"], figure_params["bounds"]+1),
              "u": {"curve": np.zeros(figure_params["bounds"]+1), 
                      "label": "Spannung - U", 
                      "color": "blue",
                      "linestyle": "solid",
                      "linewidth": 3},
              "i": {"curve": np.zeros(figure_params["bounds"]+1),
                      "label": "$Strom - I$", 
                      "color": "red",
                      "linestyle": "solid",
                      "linewidth": 2},
              "p": {"curve": np.zeros(figure_params["bounds"]+1), 
                      "label": "$Augenblicksleistung - p(t)$", 
                      "color": "orange",
                      "linestyle": "solid",
                      "linewidth": 1.5},
              "S": {"curve": np.zeros(figure_params["bounds"]+1), 
                      "label": "$Scheinleistung - S$", 
                      "color": "cyan",
                      "linestyle": "dashed",
                      "linewidth": 3},
              "P": {"curve": np.zeros(figure_params["bounds"]+1), 
                      "label": "$Wirkleistung - P$", 
                      "color": "lightgreen",
                      "linestyle": "dashed",
                      "linewidth": 2},
              "Q": {"curve": np.zeros(figure_params["bounds"]+1), 
                      "label": "$Blindleistung - Q$", 
                      "color": "darkgreen",
                      "linestyle": "dashed",
                      "linewidth": 1.5}}
    
    widgets = {"label_f": {"self": "",
                           "side": tk.LEFT,
                           "text": "Frequenz f in Hz (mindestens 10 Hz):"},
               "label_a": {"self": "",
                           "side": tk.LEFT,
                           "text": "Spannungs Vector U in V:"},
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
        self.widgets["entry_f"]["self"].insert(0, "10")
        self.widgets["entry_a"]["self"].insert(0, "5")
        self.widgets["entry_z"]["self"].insert(0, "j")
    
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
        
        self.axes.set_title(self.figure_params["title"])
        self.axes.set_xlabel(self.figure_params["xlabel"])
        self.axes.set_ylabel(self.figure_params["ylabel 1"])
        self.axes.grid()
        self.axes.minorticks_on()
        self.axes.yaxis.label.set_color(self.graphs["u"]["color"])
        self.axes.tick_params(axis="y", colors=self.graphs["u"]["color"])
        self.plot_axes(self.axes, self.graphs["u"])
        
        self.twin1.set_ylabel(self.figure_params["ylabel 2"])
        self.twin1.grid()
        self.twin1.minorticks_on()
        self.twin1.yaxis.label.set_color(self.graphs["i"]["color"])
        self.twin1.tick_params(axis="y", colors=self.graphs["i"]["color"])
        self.plot_axes(self.twin1, self.graphs["i"])
        
        self.twin2.spines.right.set_position(("axes", 1.2)) # Offset the right spine of twin2
        self.twin2.set_ylabel(self.figure_params["ylabel 3"])
        self.twin2.grid()
        self.twin2.minorticks_on()
        self.plot_axes(self.twin2, self.graphs["p"])
        self.plot_axes(self.twin2, self.graphs["S"])
        self.plot_axes(self.twin2, self.graphs["P"])
        self.plot_axes(self.twin2, self.graphs["Q"])
    
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
            
            self.axes.clear()
            self.axes.set_title(self.figure_params["title"])
            self.axes.set_xlabel(self.figure_params["xlabel"])
            self.axes.set_ylabel(self.figure_params["ylabel 1"])
            self.axes.set_ylim(-np.absolute(complex(self.widgets["entry_a"]["variable"].get()))*1.1, np.absolute(complex(self.widgets["entry_a"]["variable"].get()))*1.1)
            self.axes.grid()
            self.axes.minorticks_on()
            self.axes.yaxis.label.set_color(self.graphs["u"]["color"])
            self.axes.tick_params(axis="y", colors=self.graphs["u"]["color"])
            plot_u = self.plot_axes(self.axes, self.graphs["u"])
            
            self.twin1.clear()
            self.twin1.set_ylabel(self.figure_params["ylabel 2"])
            self.twin1.set_ylim(-np.absolute(complex(self.widgets["entry_a"]["variable"].get())/complex(self.widgets["entry_z"]["variable"].get()))*1.1, np.absolute(complex(self.widgets["entry_a"]["variable"].get())/complex(self.widgets["entry_z"]["variable"].get()))*1.1)
            self.twin1.minorticks_on()
            self.twin1.yaxis.label.set_color(self.graphs["i"]["color"])
            self.twin1.tick_params(axis="y", colors=self.graphs["i"]["color"])
            plot_i = self.plot_axes(self.twin1, self.graphs["i"])
            
            self.twin2.clear()
            self.twin2.spines.right.set_position(("axes", 1.2))
            self.twin2.set_ylabel(self.figure_params["ylabel 3"])
            max_power_value = np.max([np.max(self.graphs["p"]["curve"]), 
                                      self.graphs["S"]["curve"][1], 
                                      self.graphs["P"]["curve"][1], 
                                      self.graphs["Q"]["curve"][1]])
            self.twin2.set_ylim(-max_power_value*1.1, max_power_value*1.1)
            self.twin2.minorticks_on()
            plot_p = self.plot_axes(self.twin2, self.graphs["p"])
            plot_S = self.plot_axes(self.twin2, self.graphs["S"])
            plot_P = self.plot_axes(self.twin2, self.graphs["P"])
            plot_Q = self.plot_axes(self.twin2, self.graphs["Q"])

            self.twin2.legend(handles=[plot_u, plot_i, plot_p, plot_S, plot_P, plot_Q], loc=self.figure_params["legend_position"], framealpha=1)
    
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
                        if "entry_f" in widget and float(new_value) < 10.0: raise ValueError("f should be grater or equal to 10 Hz")
                        if "entry_z" in widget and type(new_value) != type(1.0): self.widgets["scale_theta"]["variable"].set(0.0)
                        if "scale_theta" in widget and new_value != 0.0 and np.imag(complex(self.widgets["entry_z"]["variable"].get())) != 0.0: 
                            old_z = complex(self.widgets["entry_z"]["variable"].get())
                            self.widgets["entry_z"]["self"].delete(0,100)
                            self.widgets["entry_z"]["self"].insert(0,[f"{np.real(old_z)}" if np.real(old_z) != 0.0 else 1.0])
                    except ValueError:
                        self.widgets[widget]["self"].config(fg="red")
                        self.widgets[widget]["old_value"] = ""
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
        frequency = float(self.widgets["entry_f"]["variable"].get())
        u_vector = complex(self.widgets["entry_a"]["variable"].get())
        z_vector = complex(self.widgets["entry_z"]["variable"].get())
        theta = self.widgets["scale_theta"]["variable"].get()
        
        û = np.absolute(u_vector)
        U_eff = û/2**0.5
        phi_u = np.angle(u_vector)
        
        i_vector = u_vector / z_vector
        î = np.absolute(i_vector)
        I_eff = î/2**0.5
        phi_i = np.angle(i_vector)
        
        U_complex = U_eff * (np.cos(phi_u) + 1j * np.sin(phi_u))
        I_complex = I_eff * (np.cos(phi_i) + 1j * np.sin(phi_i))
        S_complex = U_complex * np.conjugate(I_complex)
        
        P = û*î/2/np.pi*(np.pi*(1-np.absolute(theta)/180)-np.sin(2*np.pi*np.absolute(theta)/180)/2)
        S = û*î/2*(1/np.pi*(np.pi*(1-np.absolute(theta)/180)-np.sin(2*np.pi*np.absolute(theta)/180)/2))**0.5
        Q = (S**2-P**2)**0.5
        
        for t in self.graphs["t"]:
            amplitude_is_zero = self.phase_control(t, frequency, u_vector, theta)
            
            wt = 2*np.pi*frequency*t/1000 # angular frequency * time
            u_complex = û * (np.cos(wt+phi_u) + 1j * np.sin(wt+phi_u)) * amplitude_is_zero
            i_complex = î * (np.cos(wt+phi_i) + 1j * np.sin(wt+phi_i)) * amplitude_is_zero
            
            p = np.real(u_complex)*np.real(i_complex)
            
            self.graphs["u"]["curve"][int(t)] = np.real(u_complex)
            self.graphs["i"]["curve"][int(t)] = np.real(i_complex)
            self.graphs["p"]["curve"][int(t)] = p
            self.graphs["S"]["curve"][int(t)] = S if theta != 0.0 else np.absolute(S_complex) # = û*î/2
            self.graphs["P"]["curve"][int(t)] = P if theta != 0.0 else np.real(S_complex)
            self.graphs["Q"]["curve"][int(t)] = Q if theta != 0.0 else np.imag(S_complex)
    
    def phase_control(self, t, frequency, u_vector, theta):
        """Returns 0 when the signal should be zero due to theta

        Args:
            t (float): The given time step
            frequency (float): Frequency of the signal
            u_vector (complex): Phasor of the signal
            theta (float): Phase control angle

        Returns:
            flaot: 0.0 or 1.0 depending on the result of the calculations
        """        
        T = 1/frequency
        halbe_perioden_in_zeitfenster = int(0.2/T)
        totzeit = T*theta/360 # T/2 * theta/180
        versatz_durch_phasenverschiebung = T*np.angle(u_vector*1j)/2/np.pi#+T/4
        for k in range(-1,halbe_perioden_in_zeitfenster+2):
            ns = T*k/2-versatz_durch_phasenverschiebung
            if theta >= 0 and t/1000 >= ns and t/1000 < ns+totzeit:
                return 0.0
            elif theta < 0 and t/1000 <= ns and t/1000 > ns+totzeit:
                return 0.0
        return 1.0
    
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
                        linestyle = graph["linestyle"],
                        linewidth = graph["linewidth"])
        return ax

if __name__ == "__main__":
    exercise_07 = TKWindow(window_title)
    exercise_07.window_loop()