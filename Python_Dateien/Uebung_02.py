# -*- coding: utf-8 -*-
"""
Created 2022

Für eine Messreihe wird jeweils die Regression, lineare Interpolation und spline
Interpolation geplottet und die geschätzten Werte für eine unbekannte Größe ausgegeben.

Beispielweise würde hier der Wiederstand in abhängigkeit er Temperatur approximiert und ausgerechnet 

@author: Boris
"""
import tkinter as tk
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import interpolate as ip
import sys, getopt
screenpam=1
try:
    opts, args = getopt.getopt(sys.argv[1:], "p", ["presentation"])
except getopt.GetoptError:
    print("Invalid param")
    sys.exit(2)
for opt, arg in opts:
    if opt == "-p":
        screenpam=2

def sortinputandoutput(x, y):
    """Sortiert die input und output damit wir linear interpolieren können

    Args:
        x (Array of int32): x Werte, Werte vom ersten array 
        y (Array of int32): y Werte, Werte vom zweiten array 

    Returns:
        list: beinhaltet die x und y Werte 
    """ ""
    l = list(zip(x, y))
    l.sort(key=lambda a: a[0])
    return list(zip(*l))


def create_label(root, text, row, column, textvariable=None):
    label = tk.Label(root, text=text, textvariable=textvariable)
    label.grid(row=row, column=column)
    return label


def create_option_menu(parent, options, command, row, column, width=30, font=None):
    variable = tk.StringVar(value=options[0])
    menu = tk.OptionMenu(parent, variable, *options, command=command)
    menu.config(width=width, font=font)
    menu.grid(row=row, column=column)
    return variable, menu


def create_button(parent, text, command, row, column):
    button = tk.Button(parent, text=text, command=command)
    button.grid(row=row, column=column)
    return button


def makeline(x, y):
    """Erstellt eine lineare approximation zwischen zwei Punkten 

    Args:
        x (Array of int32): x Wert
        y (Array of int32): y Wert

    Returns:
        (float,float): Paramater für die Funktion y=ax+b
    """ ""
    N = len(x)
    a_numerator = N * np.sum(x * y) - (np.sum(y) * np.sum(x))
    a_denominator = N * np.sum(x**2) - (np.sum(x)) ** 2
    a = a_numerator / a_denominator
    b_numerator = np.sum(y) * np.sum(x**2) - np.sum(y * x) * np.sum(x)
    b_denominator = N * np.sum(x**2) - (np.sum(x)) ** 2
    b = b_numerator / b_denominator
    return a, b


def findValue(x, x0, y):
    xmin = min(x)
    xmax = max(x)
    if x0 < xmin or x0 > xmax:
        y_for_temp = "Fail"
        # return "FAIL"
    else:
        # print(x0)
        x_variabel_fuer_anfang_Lin_interp = np.max(list(filter(lambda n: n < x0, x)))
        x_variabel_fuer_ende_Lin_interp = np.min(list(filter(lambda n: n >= x0, x)))
        x_und_y_gezippt = tuple(zip(x, list(y)))
        # print(list(x_und_y_gezippt))
        x_und_y_gedict = dict(list(x_und_y_gezippt))
        y_wert_1 = x_und_y_gedict[x_variabel_fuer_anfang_Lin_interp]
        y_wert_2 = x_und_y_gedict[x_variabel_fuer_ende_Lin_interp]

        x_wert_1 = x_variabel_fuer_anfang_Lin_interp
        x_wert_2 = x_variabel_fuer_ende_Lin_interp
        # print(x_wert_1,x_wert_2,y_wert_1,y_wert_2)
        a, b = makeline(np.array([x_wert_1, x_wert_2]), np.array([y_wert_1, y_wert_2]))
        y_for_temp = a * x0 + b
        y_for_temp = float("{:.3f}".format(y_for_temp))
        return y_for_temp


class RegressionApp:
    def __init__(self):
        self.WINDOW_WIDTH = 800*screenpam
        self.WINDOW_HEIGHT = 600*screenpam
        self.FONT = ("Times New Roman", 9*screenpam)
        self.liste_reg_and_interp = [
            "Methode der kleinsten Quadrate",
            "Lineare Interpolation",
            "Kubische Splines",
        ]
        self.N = 5
        self.root = tk.Tk()
        self.initialize_gui()
        self.x = []
        self.y = []

    def Lineare_interpolation(self, x, y):
        """Lineare Interpolation für eine beliegige Messreihe
        
        
        Args:
            x (Array of int32): x Werte 
            y (Array of int32): y Werte 
        """ ""
        self.remove()
        self.plot1.plot(x, y)
        self.plot1.legend(["Messdaten", "Lineare Interpolation"])
        self.plot1.set_title("Lineare Interpolatione")
        self.plot1.grid()

    def Spline(self, x, y):
        """Spline Interpolation für eine beliegige Messreihe
    
        Args:
            x (Array of int32): x Werte 
            y (Array of int32): y Werte
        """ ""
        self.remove()
        spl = ip.CubicSpline(x, y)
        x_sp = np.linspace(x.min(), x.max(), 10000)
        y_sp = spl(x_sp)
        self.plot1.plot(x_sp, y_sp)
        self.plot1.legend(["Messdaten", "Spline Interpolation"])
        self.plot1.set_title("Spline Interpolatione")
        self.plot1.grid()

    def res(self):
        """Schätzung von Werten für eine unbekannte Größe"""
        # Wir lesen die Eingabe temperatur
        x, y = self.x, self.y
        try:
            xvltemp = float(self.number_entries[10].get())
            self.number_entries[10].config(bg="white")
        except Exception as e:
            self.number_entries[10].config(bg="red")
            return

        if self.drop_down_state == self.liste_reg_and_interp[0]:
            """
            Das ist Lineare regression für eine bestimmte Temperatur
            """
            a, b = makeline(x, y)
            ergebnisse = a * xvltemp + b
            ergebnisse = float("{:.3f}".format(ergebnisse))

        elif self.drop_down_state == self.liste_reg_and_interp[1]:
            """
            Das ist linear interpolation für eine bestimmte Temperatur
            """
            # x0=xvltemp
            ergebnisse = findValue(x, xvltemp, y)

        elif self.drop_down_state == self.liste_reg_and_interp[2]:
            """
            Das ist cubische regression für eine bestimmte Temperatur
            """
            spl = ip.CubicSpline(x, y)
            x_sp = np.linspace(x.min(), x.max(), 1000)
            y_sp = spl(x_sp)
            ergebnisse = findValue(x_sp, xvltemp, y_sp)

        self.numeric_result.set(ergebnisse)

    def Regression(self, x, y):
        """Regression für eine beliebige Messreihe
        Args:
            x (Array of int32): _description_
            y (Array of int32): _description_
        """
        a, b = makeline(x, y)
        a = float("{:.3f}".format(a))
        self.y_antwort_text.set(a)
        b = float("{:.3f}".format(b))
        self.x_antworten_antworten.set(b)
        xvl = np.linspace(min(x), max(x), 10000)
        yvl = a * xvl + b
        self.plot1.plot(xvl, yvl, color="blue")
        self.plot1.legend(["Messdaten", "Lineare Regression"])
        self.plot1.set_title("Lineare Regression")
        self.plot1.grid()
        [
            x.grid()
            for x in [
                self.result_label,
                self.result_a_label,
                self.result_b_label,
                self.result_b_value,
                self.result_y_label,
                self.result_x_label,
                self.result_a1_label,
                self.result_y_value,
                self.result_x_value,
            ]
        ]

    def remove(self):
        [
            x.grid_remove()
            for x in [
                self.result_label,
                self.result_a_label,
                self.result_b_label,
                self.result_b_value,
                self.result_y_label,
                self.result_x_label,
                self.result_a1_label,
                self.result_y_value,
                self.result_x_value,
            ]
        ]

    def drop_down_change(self, dp):
        self.drop_down_state = dp
        self.plotAktualizieren()

    def plotAktualizieren(self):
        """
        Updates the plot in the GUI based on the input values and selected regression method.

        This method reads the input values, validates them, and creates a scatter plot of the data points.
        It then calls the appropriate regression method based on the user's selection, updates the plot,
        and refreshes the canvas.
        """
        self.plot1.clear()
        values = []
        for i in range(10):
            try:
                values.append(float(self.number_entries[i].get()))
                self.number_entries[i].config(bg="white")
            except Exception as e:
                self.number_entries[i].config(bg="red")
                return

        x = np.array(values[0:5])
        y = np.array(values[5:10])

        self.plot1.scatter(x, y, color="red")
        self.plot1.set_xlabel("x [z.B. Temperatur in °C]")
        self.plot1.set_ylabel("y [z.B. Widerstand in \u03A9]")
        x, y = [np.array(t) for t in sortinputandoutput(x, y)]
        if self.drop_down_state == self.liste_reg_and_interp[0]:
            self.Regression(x, y)
        elif self.drop_down_state == self.liste_reg_and_interp[1]:
            self.Lineare_interpolation(x, y)
        elif self.drop_down_state == self.liste_reg_and_interp[2]:
            self.Spline(x, y)
        self.x, self.y = x, y
        self.plt_figure.canvas.draw()
        self.plt_figure.canvas.flush_events()

    def initialize_gui(self):
        """
        Initializes the graphical user interface (GUI) for the regression application.

        This method sets up the plot, labels, input fields, and buttons for the application.
        It also configures the appearance and layout of the various widgets.
        """
        self.plt_figure = plt.Figure(figsize=(6*screenpam, 4*screenpam), dpi=100)
        self.plot1 = self.plt_figure.add_subplot(111)
        self.tk_canvas = FigureCanvasTkAgg(self.plt_figure, self.root)
        self.tk_canvas.get_tk_widget().grid(
            row=6, column=3, columnspan=100, rowspan=24, padx=0, pady=0
        )
        self.plot1.set_xlabel("x [z.B. Temperatur in °C]")
        self.plot1.set_ylabel("y [z.B. Widerstand in \u03A9]")

        self.drop_down_state = self.liste_reg_and_interp[0]
        self.y_antwort_text = tk.StringVar()
        self.x_antworten_antworten = tk.StringVar()
        self.numeric_result = tk.StringVar()
        self.number_entries = []

        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.root.title("Übung 2")

        # Create the OptionMenu
        dropDownVariable, menu = create_option_menu(
            self.root,
            self.liste_reg_and_interp,
            self.drop_down_change,
            row=0,
            column=10,
            width=30,
            font=self.FONT,
        )
        self.dropDownVariable = dropDownVariable

        # Set up result labels
        self.result_label = create_label(self.root, "Results : ", 1, 11)
        self.result_a_label = create_label(self.root, "a= ", 2, 12)
        self.result_a1_label = create_label(self.root, "", 2, 13, self.y_antwort_text)
        self.result_b_label = create_label(self.root, "b= ", 3, 12)
        self.result_b_value = create_label(
            self.root, "", 3, 13, self.x_antworten_antworten
        )
        self.result_y_label = create_label(self.root, "y= ", 4, 12)
        self.result_y_value = create_label(self.root, "", 4, 13, self.y_antwort_text)
        self.result_x_label = create_label(self.root, "x + ", 4, 14)
        self.result_x_value = create_label(
            self.root, "", 4, 15, self.x_antworten_antworten
        )

        # Set up input value labels
        create_label(self.root, "Eingabewerte (x)", 0, 0)
        create_label(self.root, "Eingabewerte 2 (y)", 6, 0)
        # Set up input entry fields
        for i in range(5):
            num = tk.Entry(self.root, justify="center")
            num.grid(row=i + 1, column=0, pady=4)
            num.insert(tk.END, str(i))
            self.number_entries.append(num)

        for i in range(5, 10):
            num = tk.Entry(self.root, justify="center")
            num.grid(row=i + 2, column=0)
            num.insert(tk.END, str(random.randrange(0, (i - 4) * 10)))
            self.number_entries.append(num)

        # Set up calculate buttons
        create_button(
            self.root,
            text="Diagramm zeichnen",
            command=lambda: [self.plotAktualizieren()],
            row=12,
            column=0,
        )
        create_button(self.root, text="Das y Wert berechnen", command=self.res, row=15, column=0)

        create_label(self.root, "Unbekannte Größe", 13, 0)

        self.number_entries.append(tk.Entry(self.root, justify="center"))
        self.number_entries[10].grid(row=14, column=0)
        self.number_entries[10].insert(tk.END, "30")
        create_label(self.root, "y= ", 16, 0)
        create_label(self.root, "", 17, 0, self.numeric_result)
        create_label(self.root, "\u03A9", 17, 1)


if __name__ == "__main__":
    app = RegressionApp()
    app.root.mainloop()
