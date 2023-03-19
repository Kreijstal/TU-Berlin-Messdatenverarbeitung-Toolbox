# -*- coding: utf-8 -*-
"""
Statische Eigenschaften von Messsystemen
Anzeige einer realen- und idealen Systemkennlinie mit allen Fehlern

von Erik Tröndle

"""


import tkinter as tk
import numpy as np
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys, getopt
window_title = "Übung 03 - Statische Eigenschaften von Messystemen"
screenpam=1
try:
    opts, args = getopt.getopt(sys.argv[1:], "p", ["presentation"])
except getopt.GetoptError:
    print("Invalid param")
    sys.exit(2)
for opt, arg in opts:
    if opt == "-p":
        screenpam=2

class TKWindow(tk.Tk):
    """Class to generate TKinter Window"""

    figure_params = {
        "figsize": (8*screenpam, 5*screenpam),
        "title": "Kennlinien Fehler",
        "xlabel": "Output",
        "ylabel": "Input",
        "bounds": 100,
        "legend_position": "upper left",
    }

    graphs = {
        "x": np.linspace(0, figure_params["bounds"], figure_params["bounds"] + 1),
        "y": {
            "curve": np.zeros(figure_params["bounds"] + 1),
            "label": "reale Kennlinie",
            "color": "blue",
            "linestyle": "solid",
        },
        "y_ideal": {
            "curve": np.linspace(
                0, figure_params["bounds"], figure_params["bounds"] + 1
            ),
            "label": "ideale Kennlinie",
            "color": "red",
            "linestyle": "dashed",
        },
        "y_offset_error": {
            "curve": np.linspace(
                0, figure_params["bounds"], figure_params["bounds"] + 1
            ),
            "label": "Kennlinie mit Offset-Fehler",
            "color": "green",
            "linestyle": "dashdot",
        },
        "y_amplification_error": {
            "curve": np.linspace(
                0, figure_params["bounds"], figure_params["bounds"] + 1
            ),
            "label": "Kennlinie mit Verstärkungs-Fehler",
            "color": "yellowgreen",
            "linestyle": "dashdot",
        },
        "y_linearity_error": {
            "curve": np.linspace(
                0, figure_params["bounds"], figure_params["bounds"] + 1
            ),
            "label": "Kennlinie mit Linearitäts-Fehler",
            "color": "darkgreen",
            "linestyle": "dashdot",
        },
    }

    widget_params = {
        "offset_checkbox": {"name": "offset", "text": "Offsetfehler", "variable": None},
        "amplification_checkbox": {
            "name": "amplification",
            "text": "Verstärkungsfehler",
            "variable": None,
        },
        "linearity_checkbox": {
            "name": "linearity",
            "text": "Linearitätsfehler",
            "variable": None,
        },
        "offset_scale": {"name": "offset", "variable": None, "from": -100, "to": 100},
        "amplification_scale": {
            "name": "amplification",
            "variable": None,
            "from": -100,
            "to": 100,
        },
        "linearity_scale": {
            "name": "linearity",
            "variable": None,
            "from": -25,
            "to": 25,
        },
    }

    def __init__(self, title="Test Window"):
        """Override for standard initialization method

        Args:
            title (str, optional): Setzt den Titel des Fensters. Defaults to "Test Window".
        """
        super().__init__()
        self.offsetold=None
        self.ampold=None
        self.wimp=None
        self.changed=True
        self.init_window(title)
        self.init_params()
        self.create_widgets()
        self.init_widgets()
        self.init_figure()
        self.init_axes()
        self.place_widgets()
        self.animation_object = animation.FuncAnimation(
            self.figure, self.animate, interval=100
        )
        
    def init_window(self, title):
        """Set´s parameters for the window.

        Args:
            title (str): Setzt den Titel des Fensters.
        """
        self.title(title)
        self.resizable(False, False)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=10)

    def init_params(self):
        """Initialize widget variables befor widget creation."""
        self.widget_params["offset_checkbox"]["variable"] = tk.BooleanVar()
        self.widget_params["amplification_checkbox"]["variable"] = tk.BooleanVar()
        self.widget_params["linearity_checkbox"]["variable"] = tk.BooleanVar()
        self.widget_params["offset_scale"]["variable"] = tk.DoubleVar()
        self.widget_params["amplification_scale"]["variable"] = tk.DoubleVar()
        self.widget_params["linearity_scale"]["variable"] = tk.DoubleVar()

    def create_widgets(self):
        """Creates all widgets for the window."""
        self.scales = {
            self.widget_params["offset_scale"]["name"]: tk.Scale(
                self,
                showvalue=1,
                orient="horizontal",
                variable=self.widget_params["offset_scale"]["variable"],
                from_=self.widget_params["offset_scale"]["from"],
                to=self.widget_params["offset_scale"]["to"],
            ),
            self.widget_params["amplification_scale"]["name"]: tk.Scale(
                self,
                showvalue=1,
                orient="horizontal",
                variable=self.widget_params["amplification_scale"]["variable"],
                from_=self.widget_params["amplification_scale"]["from"],
                to=self.widget_params["amplification_scale"]["to"],
            ),
            self.widget_params["linearity_scale"]["name"]: tk.Scale(
                self,
                showvalue=1,
                orient="horizontal",
                variable=self.widget_params["linearity_scale"]["variable"],
                from_=self.widget_params["linearity_scale"]["from"],
                to=self.widget_params["linearity_scale"]["to"],
            ),
        }
        self.checkboxes = {
            self.widget_params["offset_checkbox"]["name"]: tk.Checkbutton(
                self,
                text=self.widget_params["offset_checkbox"]["text"],
                variable=self.widget_params["offset_checkbox"]["variable"],
                command=lambda: self.checkbox_clicked(
                    self.scales[self.widget_params["offset_scale"]["name"]]
                ),
                onvalue=True,
                offvalue=False,
            ),
            self.widget_params["amplification_checkbox"]["name"]: tk.Checkbutton(
                self,
                text=self.widget_params["amplification_checkbox"]["text"],
                variable=self.widget_params["amplification_checkbox"]["variable"],
                command=lambda: self.checkbox_clicked(
                    self.scales[self.widget_params["amplification_scale"]["name"]]
                ),
                onvalue=True,
                offvalue=False,
            ),
            self.widget_params["linearity_checkbox"]["name"]: tk.Checkbutton(
                self,
                text=self.widget_params["linearity_checkbox"]["text"],
                variable=self.widget_params["linearity_checkbox"]["variable"],
                command=lambda: self.checkbox_clicked(
                    self.scales[self.widget_params["linearity_scale"]["name"]]
                ),
                onvalue=True,
                offvalue=False,
            ),
        }

    def checkbox_clicked(self, scale):
        """Callback for a clicked checkbox

        Args:
            scale (dict): Scale whose value has to be set to zero
        """
        self.changed=True
        scale.set(0)
    def set_old(self):
        self.offsetold=self.widget_params["offset_scale"]["variable"].get()
        self.ampold=self.widget_params["amplification_scale"]["variable"].get()
        self.wimp=self.widget_params["linearity_scale"]["variable"].get()
        
    def check_old(self):
        return self.offsetold==self.widget_params["offset_scale"]["variable"].get() and self.ampold==self.widget_params["amplification_scale"]["variable"].get() and self.wimp==self.widget_params["linearity_scale"]["variable"].get()
        
    def init_widgets(self):
        """Initialize widget variables after widget creation."""
        [self.checkboxes[checkbox].select() for checkbox in self.checkboxes]

    def init_figure(self):
        """Initialize matplotlib figure and corresponding widget."""
        self.figure = Figure(figsize=self.figure_params["figsize"], dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)

    def init_axes(self):
        """Initialize figure axes."""
        self.axes = self.figure.add_subplot()

    def place_widgets(self):
        """Place TKinter widgets."""
        self.figure_canvas.get_tk_widget().grid(row=0, column=0, columnspan=2)

        self.checkboxes["offset"].grid(row=1, column=0, sticky="w", pady=10, padx=40)
        self.checkboxes["amplification"].grid(
            row=2, column=0, sticky="w", pady=10, padx=40
        )
        self.checkboxes["linearity"].grid(row=3, column=0, sticky="w", pady=10, padx=40)

        self.scales["offset"].grid(row=1, column=1, sticky="ew", pady=10, padx=40)
        self.scales["amplification"].grid(
            row=2, column=1, sticky="ew", pady=10, padx=40
        )
        self.scales["linearity"].grid(row=3, column=1, sticky="ew", pady=10, padx=40)

    def window_loop(self):
        """Startin animation and window loop."""

        self.mainloop()

    def animate(self, i):
        """Method respnsible for animation. Updates axes objects and calls all necessary methods to draw graphs.

        Args:
            i (int): needed for animation
        """
        if not self.changed and self.check_old():
           return
        
        self.update_graphs()
        self.axes.clear()
        self.axes.set_title(self.figure_params["title"])
        self.axes.set_xlabel(self.figure_params["xlabel"])
        self.axes.set_ylabel(self.figure_params["ylabel"])
        self.axes.autoscale(False)
        self.axes.grid()
        self.axes.minorticks_on()
        self.axes.set_xbound(lower=0, upper=self.figure_params["bounds"])
        self.axes.set_ybound(lower=0, upper=self.figure_params["bounds"])
        self.plot_axes(self.graphs["y"])
        self.plot_axes(self.graphs["y_ideal"])
        self.plot_axes(self.graphs["y_offset_error"]) if self.widget_params[
            "offset_checkbox"
        ]["variable"].get() else None
        self.plot_axes(self.graphs["y_amplification_error"]) if self.widget_params[
            "amplification_checkbox"
        ]["variable"].get() else None
        self.plot_axes(self.graphs["y_linearity_error"]) if self.widget_params[
            "linearity_checkbox"
        ]["variable"].get() else None
        self.axes.legend(loc=self.figure_params["legend_position"])
        self.set_old()
        self.changed=False

    def update_graphs(self):
        """Update graph values."""
        a = (
            self.widget_params["offset_scale"]["variable"].get()
            if self.widget_params["offset_checkbox"]["variable"].get()
            else 0
        )
        b = (
            1
            + self.widget_params["amplification_scale"]["variable"].get()
            / (
                100
                if self.widget_params["amplification_scale"]["variable"].get() < 0
                else 10
            )
            if self.widget_params["amplification_checkbox"]["variable"].get()
            else 1
        )
        c = (
            self.widget_params["linearity_scale"]["variable"].get()
            if self.widget_params["linearity_checkbox"]["variable"].get()
            else 0
        )
        d = self.figure_params["bounds"] / 2

        for x in range(0, self.figure_params["bounds"] + 1):
            self.graphs["y"]["curve"][x] = a + b * x - c * ((x / d - 1) ** 2 - 1)
            self.graphs["y_offset_error"]["curve"][x] = a + x
            self.graphs["y_amplification_error"]["curve"][x] = b * x
            self.graphs["y_linearity_error"]["curve"][x] = x - c * (
                (x / d - 1) ** 2 - 1
            )

    def plot_axes(self, plot):
        """Plots given graph in axes object.

        Args:
            plot (dict): Graph to plot
        """
        self.axes.plot(
            self.graphs["x"],
            plot["curve"],
            label=plot["label"],
            color=plot["color"],
            linestyle=plot["linestyle"],
        )


if __name__ == "__main__":
    exercise_03 = TKWindow(window_title)
    exercise_03.window_loop()
