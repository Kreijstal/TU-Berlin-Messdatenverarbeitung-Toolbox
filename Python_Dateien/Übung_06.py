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
import scipy.signal

window_title = "Übung 06 - Leistungsimulation"

def clamp(minimum, x, maximum):
    return max(minimumself.impedanz, min(x, maximum))


class TKWindow(tk.Tk):
    """Das hier zeigt in tkinter ein Plot von Spannung und Strom """
    dictWidgets=dict()
    amplitude=1
    frequency=1
    spannung=[]
    power=[]
    spanningintegral=[]
    time=[]
    current=[]
    intU=0
    impedanz=1

    def createWidgets(self):
        self.figure = Figure(figsize=(10,7), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self).get_tk_widget()
        self.figure.tight_layout()

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
                self.spannung.pop(0)#self.intU=self.intU-self.spannung.pop(0)
                l=self.time.pop(0)
                self.current.pop(0)
                self.power.pop(0)
                #print(("left",l,"right",i))
                ax.set_xlim(left=l,right=i)
                self.axes[1].set_xlim(left=l,right=i)
                l=max(-min(self.spannung),max(self.spannung))*1.05
                ll=max(-min(self.current),max(self.current))*1.05
                ax.set_ylim(ymin=-l,ymax=l)
                self.axes[2].set_ylim(ymin=-ll,ymax=ll)
                self.axes[1].set_ylim(ymin=min(0,min(self.power)*1.01),ymax=max(0,max(self.power)*1.01))
            du=(u-(self.spannung[-1] if len(self.spannung)>0 else 0))/0.001
            #self.intU=u+self.intU
            self.spannung.append(u)
            self.intU=np.sum(self.spannung)
            #assert UU==self.intU,"U=%s,U=%s"%(UU,self.intU)
            self.time.append(i)
            I=self.getCurrent(i,u,du,self.intU)
            self.current.append(I)
            self.power.append(u*I)
            ax.plot(self.time,self.spannung,color="blue")
            ax=self.axes[2]
            ax.plot(self.time,self.current,color="orange")
            ax=self.axes[1]
            ax.plot(self.time,self.power,color="red")
        pass
    def createSlider(self,name,from_,to,orient=tk.HORIZONTAL,**kwargs):
            self.dictWidgets[name]=tk.Scale(self,orient=orient,length=100, from_=from_, to=to,**kwargs)
            return self.dictWidgets[name]

    def createDropdown(self,name,options,l):
        a=tk.StringVar()
        self.dictWidgets[name]=tk.OptionMenu(self,  a, *options,command=l)
        a.set("Funktion Auswahl")
        return self.dictWidgets[name]

    def getCurrent(self,time,u,du,U):
        try:
            impedanz=eval("lambda u,t,du,U:"+self.dictWidgets["Impedanz"].get())(u,time,du,U)
            assert(impedanz!=0 and float('-inf') < float(impedanz) < float('inf'))
            self.impedanz=float(impedanz)
            self.dictWidgets["Impedanz"].config(bg="white")
        except Exception as e:
            self.dictWidgets["Impedanz"].config(bg="red")
            #if self.impedanz
        #print(("Impedanz:",self.impedanz))
        return u/self.impedanz
        
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
            this.dictWidgets["tastGrad"].grid_remove()
        def sine(amplitude,frequency,time):
            return amplitude*np.sin(time*2*np.pi*frequency)
        def attachRechteck():
            this.dictWidgets["someFunction"]=rechteck
            this.dictWidgets["tastGrad"].grid(column=5,row=0,sticky="ns",rowspan=4)
        def rechteck(amplitude,frequency,time):
            return amplitude*scipy.signal.square(time*2*np.pi*frequency,duty=this.dictWidgets["tastGrad"].get())
        def attachsawtooth():
            this.dictWidgets["tastGrad"].grid(column=5,row=0,sticky="ns",rowspan=4)
            this.dictWidgets["someFunction"]=sawtooth
        def sawtooth(amplitude,frequency,time):
            return amplitude*scipy.signal.sawtooth(time*2*np.pi*frequency,width=this.dictWidgets["tastGrad"].get())
        case_1 = attachSine
        case_2 = attachRechteck
        case_3 = attachsawtooth
        case_4 = lambda : print("load swa")
        switch.add_case("sinus", case_1, True)
        switch.add_case("rechteck", case_2, True)
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
        self.createDropdown("dropdown",["sinus","sawtooth","rechteck"],self.onSelection).grid(column=3,row=1,columnspan=2,sticky="ew",ipadx=120)
        self.createSlider("amplitude",0,100).grid(column=1,row=2,sticky="ew",ipadx=120)
        tk.Label(self,text="Z =").grid(column=3, row=2,sticky="w")
        self.createTextInput("Impedanz","1").grid(column=4,row=2,sticky="w",ipadx=120)
        self.canvas.grid(column=0,row=3,columnspan = 5)
        self.createSlider("tastGrad",0,1,resolution=0.01,orient=tk.VERTICAL)
    def create_axes(self):
        #Creating axes
        self.axes=[self.figure.add_subplot(1,2,1),self.figure.add_subplot(1,2,2)]
        self.axes.append(self.axes[0].twinx())
        self.axes[0].set_xlabel('Zeit (s)')
        self.axes[1].set_xlabel('Zeit (s)')
        self.axes[0].set_ylabel('Spannung (V)')
        self.axes[1].set_ylabel('Leistung (W)')
        self.axes[1].yaxis.tick_right()
        self.axes[1].yaxis.set_label_position("right")
        self.axes[2].set_ylabel('Strom (A)')
        #10000*10*10 #self.resizable(False, False) #self.columnconfigure(0, weight=0) #self.columnconfigure(1, weight=10)
        
exercise_06 = TKWindow(window_title)
exercise_06.window_loop()
