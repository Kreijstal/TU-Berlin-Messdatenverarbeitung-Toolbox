# -*- coding: utf-8 -*-
"""
Created on 2022

6. Leistungsmessung
• Anzeige der Leistungskurven für einen einstellbaren Verbraucher, linear oder nichtlinear mit Oberwellen.

@author: Datenschutz bitte.
"""
class Switch(object):
    #Quelle : https://codegree.de/python-switch-case/
    def __init__(self):
        # Alle möglichen Fälle werden hier festgehalten
        self.cases = []
        # speichert, ob ein Fall eingetreten ist
        self.case_matched = False
    def add_case(self, value, callback, breaks=True):
        # Fügt Fall an das Ende der internen Liste self.cases
        self.cases.append({
            "value": value,
            "callback": callback,
            "breaks": breaks
        })
    
    def case(self, value):
        # Speichert die Zwischenergebnisse        
        results = []
        for case in self.cases:
            # überprüft ob bereits ein voriger Fall eingetroffen ist
            # oder der aktuelle Fall eintrifft
            if self.case_matched == True or value == case["value"]:
                self.case_matched = True
                # Ergebnis des Callbacks für den aktuellen Fall wird
                # gespeichert
                results.append(case["callback"]())
                # falls breaks für den aktuellen Fall auf True
                # gesetzt wurde, endet die Schleife
                if case["breaks"]:
                    break
        self.case_matched = False
        return results


import tkinter as tk
import numpy as np
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import itertools

window_title = "Übung 06 - Leistungsimulation"




class TKWindow(tk.Tk):
    """Das hier zeigt in tkinter ein Plot von Spannung und Strom


    """
    dictWidgets=dict()
    amplitude=1
    frequency=1
    spannung=[]
    time=[]
    current=[]
    impedanz=1

    def createWidgets(self):
        self.figure = Figure(figsize=(8,5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self).get_tk_widget()

    def __init__(self, title = "Test Window"):
        """initialization der Klasse

        Args:
            title (str, optional): Fenstertitle. Defaults to "Test Window".
        """        ""
        super().__init__()
        self.createWidgets()
        self.init_window(title)
        #self.create_axes()
        
        #self.init_params()
        #self.init_figure()
        #self.init_axes()
        #self.create_widgets()
        #self.place_widgets()
        #self.init_widgets()
        
    def window_loop(self):
        self.animation_object = animation.FuncAnimation(self.figure, self.animate,init_func=self.create_axes, interval=1,frames=itertools.count(step=0.001))
        self.mainloop()
    
    def animate(self, i):
        for ax in self.axes:
            for artist in ax.lines + ax.collections:
                artist.remove()
        if "someFunction" in self.dictWidgets:
            ax=self.axes[0]
            u=self.dictWidgets["someFunction"](self.dictWidgets["amplitude"].get(),self.dictWidgets["frequency"].get(),i)
            if len(self.spannung)>100:
                self.spannung.pop(0)
                l=self.time.pop(0)
                self.current.pop(0)
                print(("left",l,"right",i))
                ax.set_xlim(left= l,right=i)
            self.spannung.append(u)
            self.time.append(i)
            self.current.append(self.getCurrent(i,u))
            ax.plot(self.time,self.spannung,color="blue")
            ax.plot(self.time,self.current,color="orange")
        pass
    def createSlider(self,name,from_,to):
        self.dictWidgets[name]=tk.Scale(self,orient=tk.HORIZONTAL,length=100, from_=from_, to=to)
        return self.dictWidgets[name]


    def createDropdown(self,name,options,l):
        a=tk.StringVar()
        self.dictWidgets[name]=tk.OptionMenu(self,  a, *options,command=l)
        a.set("Funktion Auswahl")
        return self.dictWidgets[name]

    def getCurrent(self,time,u):
        try:
            self.impedanz=eval("lambda u,t:"+self.dictWidgets["Impedanz"].get())(u,time)
            self.dictWidgets["Impedanz"].config(bg="white")
        except Exception as e:
            self.dictWidgets["Impedanz"].config(bg="red")
            if(self.impedanz)
        return self.currrent



        
    def createTextInput(self,name,default):
        self.dictWidgets[name]=tk.Entry(self,justify="center")
        self.dictWidgets[name].insert(tk.END,"1")
        return self.dictWidgets[name]

    def onSelection(self,a):
        print(a)
        print("something was selected")
        switch = Switch()
        this=self
        def attachSine():
            this.dictWidgets["someFunction"]=sine
        def sine(amplitude,frequency,time):
            return amplitude*np.sin(time*2*np.pi*frequency)
        case_1 = attachSine
        case_2 = lambda : print("boris")
        case_3 = lambda : print("load immediate")
        case_4 = lambda : print("load swa")
        switch.add_case("sine", case_1, True)
        switch.add_case("triangle", case_2, True)
        switch.add_case("sawtooth", case_3, True)
        switch.add_case("rechteck", case_3, True)
        switch.case(a)


    def init_window(self, title):
        """
        Initializierung funktion für den Fenster

        Args:
            title (str): den Titel von den Fenster

So hoffentlich sieht de fenster so aus:
            ------------------------------------------------------------
            |         _____________               _____________         |
            |   f  =  |_____________|             |dropdown____|        |
            |   A  =  |_____________|        z=   |_____________|       |
            |    ____________________           ____________________    |
            |   |                    |         |                    |   |
            |   |        U I         |         |      P             |   |
            |   |____________________|         |____________________|   |
            |                                                           |
             ------------------------------------------------------------
        """        
        self.title(title)
        #Adding Labels
        tk.Label(self,text="Plot von der Spannung und Strom").grid(column=0, row=0,columnspan=5)
        tk.Label(self,text="Frequenz =").grid(column=0, row=1,sticky="w")
        tk.Label(self,text="Amplitude =").grid(column=0, row=2,sticky="w")
        #Adding Sliders and widgets
        self.createSlider("frequency",0,200).grid(column=1,row=1,sticky="ew",ipadx=120)
        self.createDropdown("dropdown",["sine","sawtooth","triangle"],self.onSelection).grid(column=3,row=1,columnspan=2,sticky="ew",ipadx=120)
        self.createSlider("amplitude",0,100).grid(column=1,row=2,sticky="ew",ipadx=120)
        tk.Label(self,text="Z =").grid(column=3, row=2,sticky="w")
        self.createTextInput("Impedanz","1").grid(column=4,row=2,sticky="w",ipadx=120)
        self.canvas.grid(column=0,row=3,columnspan = 5)

    def create_axes(self):
        #Creating axes
        self.axes=(self.figure.add_subplot(1,2,1),self.figure.add_subplot(1,2,2))

        #10000*10*10
        #self.resizable(False, False)
        #self.columnconfigure(0, weight=0)
        #self.columnconfigure(1, weight=10)
        


exercise_06 = TKWindow(window_title)
exercise_06.window_loop()
