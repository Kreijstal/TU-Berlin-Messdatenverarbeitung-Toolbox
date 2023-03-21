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
    Eine Klasse zum Animieren von Histogrammen mit Zufallsdaten.

    Argumente:
        anzahlVonBins: Ein tkinter Scale-Widget, das die Anzahl der Bins im Histogramm darstellt.
        anzahlSamples: Ein tkinter Scale-Widget, das die Anzahl der Stichproben in den Daten darstellt.
        freiheitsgradVonStudenTverteilung: Ein tkinter Scale-Widget, das die Freiheitsgrade der Student's t-Verteilung darstellt.
        legende: Eine tkinter BooleanVar, die angibt, ob die Legende im Diagramm angezeigt werden soll.
        var1: Eine tkinter IntVar, die angibt, ob die Daten bei jedem Frame erneuert werden sollen.
        var2: Eine tkinter IntVar, die angibt, ob die Daten eingefroren werden sollen.
        daten: Ein Datenobjekt, das die Zufallsdaten enthält.
    
    Methoden:
        animieren(i): Animiert ein Frame des Histogramms.
    
        Argumente:
            i (int): Eine Ganzzahl, die die Frame-Nummer darstellt. Wird ignoriert.
    
        Rückgabewert:
            Ein Histogramm, das aus den Zufallsdaten generiert wurde.
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
        Initialisiert ein Animator-Objekt mit den gegebenen Attributen.

        Argumente:
            anzahlVonBins: Ein tkinter-Scale-Widget, das die Anzahl der Bins im Histogramm repräsentiert.
            anzahlSamples: Ein tkinter-Scale-Widget, das die Anzahl der Stichproben in den Daten repräsentiert.
            freiheitgradVonStudenTverteilung: Ein tkinter-Scale-Widget, das die Freiheitsgrade der Student'schen t-Verteilung repräsentiert.
            legende: Eine tkinter BooleanVar, die angibt, ob die Legende im Diagramm angezeigt werden soll.
            var1: Eine tkinter IntVar, die angibt, ob die Daten bei jedem Frame aktualisiert werden sollen.
            var2: Eine tkinter IntVar, die angibt, ob die Daten eingefroren werden sollen.
            daten: Ein Data-Objekt, das die Zufallsdaten enthält.
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
        Animiert eine Einzelbild des Histogramms.
        
        Args:
            i (int): Eine Ganzzahl, die die Rahmennummer darstellt. Wird ignoriert.
        
        Returns:
            Ein Histogramm, das aus den Zufallsdaten generiert wurde
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
            self.ax.set_title("Normalverteilung")
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
    Diese Klasse definiert die grafische Benutzeroberfläche (GUI) für die Anwendung. Sie ermöglicht es dem Benutzer, verschiedene
    Parameter und Einstellungen zu manipulieren und die resultierenden Diagramme anzusehen.

    Argumente:
        Keine

    Attribute:
        data (Data): Eine Instanz der Data-Klasse, die generierte Zufallsdaten enthält
        root (Tkinter.Tk): Das Hauptfenster von Tkinter für die GUI
        anzahlVonBins (Tkinter.Scale): Ein Schieberegler zur Anpassung der Anzahl der Bins in den Histogrammen
        anzahlSamples (Tkinter.Scale): Ein Schieberegler zur Anpassung der Anzahl der Stichproben in den Histogrammen
        freiheitgradVonStudenTverteilung (Tkinter.Scale): Ein Schieberegler zur Anpassung der Freiheitsgrade in der Student-t-Verteilung
        legende (Tkinter.BooleanVar): Eine boolesche Variable zur Steuerung der Anzeige der Legende im Diagramm
        var1 (Tkinter.IntVar): Eine Ganzzahlvariable zur Steuerung, ob die Stichproben bei jedem Frame erneuert werden
        var2 (Tkinter.IntVar): Eine Ganzzahlvariable zur Steuerung, ob die Daten eingefroren oder zufällig generiert werden
        IstRefreshSamplesGecheckht (Tkinter.Checkbutton): Eine Checkbox zur Steuerung, ob die Stichproben bei jedem Frame erneuert werden
        istGefroren (Tkinter.Checkbutton): Eine Checkbox zur Steuerung, ob die Daten eingefroren oder zufällig generiert werden
        men (Tkinter.Menu): Ein Popup-Menü, das angezeigt wird, wenn der Benutzer mit der rechten Maustaste auf das Diagramm klickt
        animator (Animator): Eine Instanz der Animator-Klasse zur Steuerung der Animation des Diagramms
        canvas (matplotlib.backends.backend_tkagg.FigureCanvasTkAgg): Eine Leinwand zur Anzeige des Diagramms in der GUI
        ani (matplotlib.animation.FuncAnimation): Ein Animationsobjekt zur Animation des Diagramms

    Methoden:
        generate_Datensatz(self): Generiert Zufallsdaten für die Normal- und Student-t-Verteilungen und aktiviert/deaktiviert das Student-t-Schieberegler-Widget
        do_popup(self, menu): Zeigt ein Popup-Menü an, wenn der Benutzer mit der rechten Maustaste auf die Leinwand klickt
        run(self): Startet die Tkinter-Hauptschleife
    """

    def __init__(self):
        """
        Initialisiert die GUI und erstellt alle notwendigen Widgets und Objekte

        Argumente:
            Keine

        Rückgabewerte:
            Keine
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
