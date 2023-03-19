# -*- coding: utf-8 -*-
"""
Created on 2022

Für eine Messreihe das vollständige Messergebnis unter der Normalverteilung bzw.
Student-t Verteilung für die Verschiedenen Vertrauensintervalle plotten. Dabei werden die entsprechenden Zwischenschritte (Mittelwert, Standardabweichung, usw.)
mit geplottet

@author: Juan
"""

import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as Tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Data:
    """
    A class for storing random data.

    Attributes:
        zuffaligeDatenMitNormaleVerteilung: A numpy array representing random data with a normal distribution.
        zuffaligeDatenMitTstudentverteilung: A numpy array representing random data with a Student's t-distribution.
    """

    def __init__(self):
        """
        Initializes the Data object with None for the random data attributes.
        """
        self.zuffaligeDatenMitNormaleVerteilung = None
        self.zuffaligeDatenMitTstudentverteilung = None


class Animator:
    """
    A class for animating histograms of random data.

    Args:
        anzahlVonBins: A tkinter Scale widget representing the number of bins in the histogram.
        anzahlSamples: A tkinter Scale widget representing the number of samples in the data.
        freiheitgradVonStudenTverteilung: A tkinter Scale widget representing the degrees of freedom for the Student's t-distribution.
        legend: A tkinter BooleanVar representing whether to show the legend on the plot.
        var1: A tkinter IntVar representing whether to refresh the data on each frame.
        var2: A tkinter IntVar representing whether to freeze the data.
        data: A Data object containing the random data.

    Methods:
        animate(i): Animates a frame of the histogram.

        Args:
            i (int): An integer representing the frame number. Ignored.

        Returns:
            A histogram generated from the random data.
    """

    def __init__(
        self,
        anzahlVonBins,
        anzahlSamples,
        freiheitgradVonStudenTverteilung,
        legend,
        var1,
        var2,
        data,
    ):
        """
        Initializes an Animator object with the given attributes.

        Args:
            anzahlVonBins: A tkinter Scale widget representing the number of bins in the histogram.
            anzahlSamples: A tkinter Scale widget representing the number of samples in the data.
            freiheitgradVonStudenTverteilung: A tkinter Scale widget representing the degrees of freedom for the Student's t-distribution.
            legend: A tkinter BooleanVar representing whether to show the legend on the plot.
            var1: A tkinter IntVar representing whether to refresh the data on each frame.
            var2: A tkinter IntVar representing whether to freeze the data.
            data: A Data object containing the random data.
        """
        self.fig = plt.Figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(2, 1, 1)
        self.ax2 = self.fig.add_subplot(2, 1, 2)
        self.oldscale1 = 0
        self.oldscale2 = 0
        self.oldscale3 = 0
        self.anzahlVonBins = anzahlVonBins
        self.anzahlSamples = anzahlSamples
        self.freiheitgradVonStudenTverteilung = freiheitgradVonStudenTverteilung
        self.legend = legend
        self.var1 = var1
        self.var2 = var2
        self.data = data

    def animate(self, i):
        """
        Animates a frame of the histogram.

        Args:
            i (int): An integer representing the frame number. Ignored.

        Returns:
            A histogram generated from the random data.
        """
        newscale1 = self.anzahlVonBins.get()
        newscale2 = self.anzahlSamples.get()
        newscale3 = self.freiheitgradVonStudenTverteilung.get()
        leg = self.legend.get()
        if (
            self.var1.get() == 0
            and self.oldscale1 == newscale1
            and self.oldscale2 == newscale2
            and self.oldscale3 == newscale3
        ):
            pass
        else:
            self.ax.cla()
            self.ax.set_title("Normal Verteilung")
            datemsatz1 = (
                np.random.normal(size=newscale2)
                if self.var2.get() == 0
                else self.data.zuffaligeDatenMitNormaleVerteilung[:newscale2]
            )
            # print
            hist = self.ax.hist(datemsatz1, bins=newscale1, label="Histogram")
            self.ax.set_ylabel("Häufigkeit")

            self.ax.axvspan(
                datemsatz1.mean() - datemsatz1.std(),
                datemsatz1.mean() + datemsatz1.std(),
                ymax=hist[0].max(),
                alpha=0.5,
                color="red",
                label="Vertrauensinterval 1$\sigma$, 68,3%",
            )
            # ax.fill_between()
            if leg:
                self.ax.legend(loc="upper right")
            else:
                legen = self.ax.get_legend()
                if legen:
                    legen.remove()
            self.ax2.cla()
            self.ax2.set_title("Student-t Verteilung")
            self.ax2.set_ylabel("Häufigkeit")
            self.ax2.set_xlabel("Zufallwerte")
            datemsatz2 = (
                np.random.standard_t(newscale3, size=newscale2)
                if self.var2.get() == 0
                else self.data.zuffaligeDatenMitTstudentverteilung[:newscale2]
            )
            hist = self.ax2.hist(datemsatz2, bins=newscale1)
            self.oldscale1 = newscale1
            self.oldscale2 = newscale2
            self.oldscale3 = newscale3
            return hist
        pass


class GUI:
    """
    This class defines the Graphical User Interface (GUI) for the application. It allows the user to manipulate different
    parameters and settings, and view the resulting plots.

    Args:
        None

    Attributes:
        data (Data): An instance of the Data class to hold generated random data
        root (Tkinter.Tk): The main Tkinter window for the GUI
        anzahlVonBins (Tkinter.Scale): A scale widget to adjust the number of bins in the histograms
        anzahlSamples (Tkinter.Scale): A scale widget to adjust the number of samples in the histograms
        freiheitgradVonStudenTverteilung (Tkinter.Scale): A scale widget to adjust the degrees of freedom in the Student-t distribution
        legend (Tkinter.BooleanVar): A boolean variable to control whether the legend is shown on the plot
        var1 (Tkinter.IntVar): An integer variable to control whether the samples are refreshed every frame
        var2 (Tkinter.IntVar): An integer variable to control whether the data is frozen or generated randomly
        IstRefreshSamplesGecheckht (Tkinter.Checkbutton): A checkbox to control whether the samples are refreshed every frame
        istGefroren (Tkinter.Checkbutton): A checkbox to control whether the data is frozen or generated randomly
        men (Tkinter.Menu): A popup menu to show when the user right-clicks on the plot
        animator (Animator): An instance of the Animator class to handle the animation of the plot
        canvas (matplotlib.backends.backend_tkagg.FigureCanvasTkAgg): A canvas to display the plot in the GUI
        ani (matplotlib.animation.FuncAnimation): An animation object to animate the plot

    Methods:
        generate_Datensatz(self): Generates random data for the normal and Student-t distributions, and enables/disables the Student-t scale widget
        do_popup(self, menu): Shows a popup menu when the user right-clicks on the canvas
        run(self): Runs the Tkinter mainloop
    """

    def __init__(self):
        """
        Initializes the GUI and creates all the necessary widgets and objects

        Args:
            None

        Returns:
            None
        """

        self.data = Data()

        # Create the main Tkinter window
        self.root = Tk.Tk()

        # Create and place the scale widgets
        self.anzahlVonBins = Tk.Scale(
            self.root, orient=Tk.HORIZONTAL, length=300, from_=2, to=100
        )
        self.anzahlSamples = Tk.Scale(
            self.root, orient=Tk.HORIZONTAL, length=300, from_=2, to=10000
        )
        self.anzahlVonBins.grid(column=2, row=1)
        self.anzahlSamples.grid(column=2, row=3)

        # Create and place labels
        Tk.Label(self.root, text="Normal und Student Verteilung").grid(column=0, row=0)
        Tk.Label(self.root, text="Es ist möglich mit den Sliders zu Spielen").grid(
            column=0, row=1
        )
        Tk.Label(self.root, text="#Bins").grid(column=2, row=0)
        Tk.Label(self.root, text="#Samples").grid(column=2, row=2)
        Tk.Label(self.root, text="Freiheitsgrad von Student-t").grid(column=2, row=4)

        # Create and place the freeze and refresh checkboxes
        self.var1 = Tk.IntVar()
        self.var2 = Tk.IntVar()
        self.IstRefreshSamplesGecheckht = Tk.Checkbutton(
            self.root,
            text="Samples/Frame aktualisieren",
            variable=self.var1,
            onvalue=1,
            offvalue=0,
        )
        self.istGefroren = Tk.Checkbutton(
            self.root,
            text="Datensatz fest machen",
            variable=self.var2,
            onvalue=1,
            offvalue=0,
            command=self.generate_Datensatz,
        )
        self.IstRefreshSamplesGecheckht.grid(column=1, row=0)
        self.istGefroren.grid(column=1, row=1)

        # Create and place the student T scale widget, initially shown
        self.freiheitgradVonStudenTverteilung = Tk.Scale(
            self.root, orient=Tk.HORIZONTAL, length=300, from_=1, to=100
        )
        self.freiheitgradVonStudenTverteilung.grid(column=2, row=5)
        # self.freiheitgradVonStudenTverteilung.grid_remove()

        # Create a boolean variable for the legend checkbox, and add it to a popup menu
        self.legend = Tk.BooleanVar()
        self.legend.set(True)
        self.men = Tk.Menu(self.root)
        self.men.add_checkbutton(
            label="Zeige Legende", onvalue=1, offvalue=0, variable=self.legend
        )

        # Create an instance of the Animator class
        self.animator = Animator(
            self.anzahlVonBins,
            self.anzahlSamples,
            self.freiheitgradVonStudenTverteilung,
            self.legend,
            self.var1,
            self.var2,
            self.data,
        )

        # Create the FigureCanvasTkAgg object and place it in the window
        self.canvas = FigureCanvasTkAgg(self.animator.fig, master=self.root)
        self.canvas.get_tk_widget().grid(
            column=0, row=2, columnspan=2, rowspan=7, padx=0, pady=0
        )
        # Bind the popup menu to right-click events on the canvas
        self.canvas.get_tk_widget().bind("<Button-3>", self.do_popup(self.men))

        # Call tight_layout to ensure that the plots fit well in the window
        self.animator.fig.tight_layout()

        # Create an animation object that calls the Animator.animate method
        self.ani = animation.FuncAnimation(
            self.animator.fig,
            self.animator.animate,
            np.arange(1, 64),
            interval=100,
            blit=False,
        )

        self.root.title("Übung 1 MT1")

    def generate_Datensatz(self):
        """
        Es generiert zufällige Daten
        """
        # Declare the global variables for the random data

        # Generate random data for a normal distribution and a student T distribution
        if self.var2.get() == 1:
            self.data.zuffaligeDatenMitNormaleVerteilung = np.random.normal(size=10000)
            self.data.zuffaligeDatenMitTstudentverteilung = np.random.standard_t(
                self.freiheitgradVonStudenTverteilung.get(), size=10000
            )

            # Disable and remove the student T scale widget
            self.freiheitgradVonStudenTverteilung.configure(state="disable")
            self.freiheitgradVonStudenTverteilung.grid_remove()
            self.IstRefreshSamplesGecheckht.configure(state="disable")
            self.var1.set(0)
        else:
            # Enable and show the student T scale widget
            self.freiheitgradVonStudenTverteilung.grid(column=2, row=5)
            self.freiheitgradVonStudenTverteilung.configure(state="normal")
            self.IstRefreshSamplesGecheckht.configure(state="normal")

    def do_popup(self, menu):
        """
        A helper function to show a popup menu when the user right-clicks on the canvas

        Args:
            menu: A Tkinter Menu object

        Returns:
            A function that shows the popup menu when called with an event
        """

        def do_popup(event):
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

        return do_popup

    def run(self):
        """
        Runs the Tkinter mainloop
        """
        self.root.mainloop()


if __name__ == "__main__":
    GUI().run()
