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
    figure_params = {
        "figsize": (8, 5),
        "title 1": "ADU Kennlinie",
        "xlabel 1": "Input",
        "ylabel 1": "Codes",
        "title 2": "Quantisierungsrauschen",
        "xlabel 2": "Input",
        "ylabel 2": "\delta Kennlinien",
        "bounds": 1000,
        "legend_position": "upper left",
    }

    graphs = {
        "x": np.linspace(0, figure_params["bounds"], figure_params["bounds"] + 1),
        "y_adu": {
            "curve": np.zeros(figure_params["bounds"] + 1),
            "label": "ADU Kennlinie",
            "color": "blue",
            "linestyle": "solid",
        },
        "y_ideal": {
            "curve": np.zeros(figure_params["bounds"] + 1),
            "label": "ideale Kennlinie",
            "color": "green",
            "linestyle": "dashed",
        },
        "y_delta": {
            "curve": np.zeros(figure_params["bounds"] + 1),
            "label": "Quantisierungsrauschen",
            "color": "red",
            "linestyle": "solid",
        },
    }

    bits_scale_params = {"variable": None, "from": 2, "to": 8}
    resolution_text = None

    def __init__(self, title="Test Window"):
        super().__init__()
        self.init_window(title)
        self.init_params()
        self.init_figure()
        self.init_axes()
        self.create_widgets()
        self.place_widgets()

    def init_window(self, title):
        self.title(title)
        self.resizable(False, False)
        # self.columnconfigure(0, weight=0)
        # self.columnconfigure(1, weight=10)

    def init_params(self):
        self.bits_scale_params["variable"] = tk.DoubleVar()
        self.resolution_text = tk.StringVar()

    def init_figure(self):
        self.figure = Figure(figsize=self.figure_params["figsize"], dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)

    def init_axes(self):
        self.axes1 = self.figure.add_subplot(1, 2, 1)  # Characteristics and ideal curve
        self.axes2 = self.figure.add_subplot(
            1, 2, 2
        )  # Delta between characteristic and ideal curve

    def create_widgets(self):
        self.bits_scale = tk.Scale(
            self,
            showvalue=1,
            orient="horizontal",
            variable=self.bits_scale_params["variable"],
            from_=self.bits_scale_params["from"],
            to=self.bits_scale_params["to"],
        )
        self.resolution = tk.Label(
            self, textvariable=self.resolution_text
        )  # , padx=5, pady=5)

    def place_widgets(self):
        self.figure_canvas.get_tk_widget().grid(row=0, column=0, columnspan=1)

        self.bits_scale.grid(row=1, column=0, sticky="ew", pady=10, padx=40)
        self.resolution.grid(row=2, column=0, sticky="ew", pady=10, padx=40)

    def window_loop(self):
        self.animation_object = animation.FuncAnimation(
            self.figure, self.animate, interval=200
        )
        self.mainloop()

    def animate(self, i):  # ToDo
        bits = self.bits_scale.get()

        new_resolution = self.calculate_resolution(bits)

        self.update_resolution_label(new_resolution)
        self.update_graphs(bits, new_resolution)

        self.axes1.clear()
        self.axes1.set_title(self.figure_params["title 1"])
        self.axes1.set_xlabel(self.figure_params["xlabel 1"])
        self.axes1.set_ylabel(self.figure_params["ylabel 1"])
        self.axes1.autoscale(False)
        self.axes1.grid()
        self.axes1.minorticks_on()
        self.axes1.set_xbound(lower=0, upper=self.figure_params["bounds"])
        self.axes1.set_ybound(lower=0, upper=bits**2 - 1)
        self.plot_axes(self.axes1, self.graphs["y_adu"])
        self.plot_axes(self.axes1, self.graphs["y_ideal"])
        self.axes1.legend(loc=self.figure_params["legend_position"])
        self.set_tick_labels(bits)

        self.axes2.clear()
        self.axes2.set_title(self.figure_params["title 2"])
        self.axes2.set_xlabel(self.figure_params["xlabel 2"])
        self.axes2.set_ylabel(self.figure_params["ylabel 2"])
        self.axes2.autoscale(False)
        self.axes2.grid()
        self.axes2.minorticks_on()
        self.axes2.set_xbound(lower=0, upper=self.figure_params["bounds"])
        self.axes2.set_ybound(lower=-0.5, upper=0.5)
        self.plot_axes(self.axes2, self.graphs["y_delta"])

    def calculate_resolution(self, bits):
        return self.figure_params["bounds"] / (bits**2 - 1)

    def update_resolution_label(self, resolution):
        self.resolution_text.set("Resolution: {:.2f}".format(resolution))

    def update_graphs(self, bits, resolution):
        for x in range(0, self.figure_params["bounds"] + 1):
            self.graphs["y_adu"]["curve"][x] = (x + resolution / 2) // resolution
            self.graphs["y_ideal"]["curve"][x] = (
                x * (bits**2 - 1)
            ) / self.figure_params["bounds"]
            self.graphs["y_delta"]["curve"][x] = (
                self.graphs["y_ideal"]["curve"][x] - self.graphs["y_adu"]["curve"][x]
            )

    def plot_axes(self, axes, graph):
        axes.plot(
            self.graphs["x"],
            graph["curve"],
            label=graph["label"],
            color=graph["color"],
            linestyle=graph["linestyle"],
        )

    def set_tick_labels(self, bits):
        ticks = []
        labels = []

        for i in range(0, bits**2):
            if bits < 6:
                ticks.append(i)
                labels.append(f"{i:b}".zfill(bits))
            elif i % 2:
                ticks.append(i)
                labels.append(f"{i:b}".zfill(bits))

        self.axes1.set_yticks(ticks, labels)


if __name__ == "__main__":
    exercise_03 = TKWindow(window_title)
    exercise_03.window_loop()
