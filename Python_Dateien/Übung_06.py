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

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


import tkinter as tk
import numpy as np
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import itertools
import scipy.signal
from functools import reduce
#
window_title = "Übung 06 - Leistungsimulation"

#def clamp(minimum, x, maximum):
#    return max(minimum, min(x, maximum))


class TKWindow(tk.Tk):
    """Das hier zeigt in tkinter ein Plot von Spannung und Strom """
    dictWidgets=dict()
    amplitude=0
    frequency=0
    spannung=[]
    ueff=[]
    ueffv=0
    ieff=[]
    ieffv=0
    power=[]
    time=[]
    current=[]
    peff=[]
    intU=0
    impedanz=1
    tx=0.001
    phi=0
    showeff=None

    def createWidgets(self):
        self.figure = Figure(figsize=(10,7), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self).get_tk_widget()
        self.figure.tight_layout()
        self.m = tk.Menu(self, tearoff=0)
        self.canvm = tk.Menu(self, tearoff=0)
        self.viewm = tk.Menu(self, tearoff=0)
                #self.m.add_separator()
        #self.m.add_command(label="Rename")
        #Adding Labels
        tk.Label(self,text="Plot von der Spannung und Strom").grid(column=0, row=0,columnspan=5)
        tk.Label(self,text="Frequenz =").grid(column=0, row=1,sticky="w")
        tk.Label(self,text="Amplitude =").grid(column=0, row=2,sticky="w")

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
        self.animation_object = animation.FuncAnimation(self.figure, self.animate,init_func=lambda:self.create_axes(1), interval=1,frames=itertools.count(step=self.tx))
        self.mainloop()
    
    def animate(self, i):
        #self.frequency=self.dictWidgets["frequency"].get()
        self.amplitude=self.dictWidgets["amplitude"].get()
        show=self.showeff.get()
        symmetrisch=self.sym.get()
        for ax in self.axes:
            for artist in ax.lines + ax.collections:
                artist.remove()
        if "someFunction" in self.dictWidgets:
            ax=self.axes[0]
            t=np.linspace(i-self.tx+self.tx/10,i,10)
            u=self.dictWidgets["someFunction"](self.amplitude,self.frequency,t)
            leg=self.showlegend.get()
            for (Z,V) in zip(t,u):
                self.intU=self.intU+V*self.tx/10
                du=(V-(self.spannung[-1] if len(self.spannung)>0 else 0))/(self.tx/10)
                I=self.getCurrent(Z,V,du,self.intU)
                self.spannung.append(V)
                self.time.append(Z)
                self.current.append(I)
                self.power.append(V*I)
                self.ueffv=self.ueffv+V**2*self.tx/10
                self.ieffv=self.ieffv+I**2*self.tx/10
                ueff=np.sqrt(self.ueffv/Z)
                ieff=np.sqrt(self.ieffv/Z)
                self.ueff.append(ueff)
                self.ieff.append(ieff)
                self.peff.append(ieff*ueff)
            if len(self.spannung)>1000:
                lasttime=self.time[0]
                self.time=self.time[10:]
                self.spannung=self.spannung[10:]
                self.current=self.current[10:]
                self.power=self.power[10:]
                self.ueff=self.ueff[10:]
                self.ieff=self.ieff[10:]
                self.peff=self.peff[10:]
                #print(("left",l,"right",i))
                ax.set_xlim(left=lasttime,right=i)
                self.axes[1].set_xlim(left=lasttime,right=i)
                self.axes[2].set_xlim(left=lasttime,right=i)
                for (meas,ax,eff) in zip((self.spannung,self.current),(self.axes[0],self.axes[2]),(self.ueff,self.ieff)):
                    topmax=max(meas)
                    botmin=min(meas)
                    if show:
                        topmax=max((topmax,max(eff)))
                        botmin=min((botmin,min(eff)))
                    if symmetrisch:
                        topmax=max(topmax,-botmin)
                        botmin=-topmax
                    dx=(topmax-botmin)*0.05
                    topmax=topmax+dx
                    botmin=botmin-dx
                    ax.set_ylim(ymin=botmin,ymax=topmax)
                maxpow=max(self.power)
                if show:
                    maxpow=max(maxpow,max(self.peff))
                self.axes[1].set_ylim(ymin=min(0,min(self.power)*1.01),ymax=max(0,maxpow*1.01))
            lnsa=[]
            for (i,c,l,val,valeff) in  zip((0,2,1),("blue","orange","red"),("u","i","p"),(self.spannung,self.current,self.power),(self.ueff,self.ieff,self.peff)):
                ax=self.axes[i]
                if show:
                    lnsa.append(ax.plot(self.time,valeff,color=c,linestyle="--",label="$%s_{eff}$"%l.upper()))
                lnsa.append(ax.plot(self.time,val,color=c,label="$%s(t)$"%l))
            ax=self.axes[0]
            lns=reduce(lambda a,b:a+b,lnsa)
            if leg:
                ax.legend(lns,[l.get_label() for l in lns],bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=3)
            else:
                legend=ax.get_legend()
                if legend:
                    legend.remove()
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
            impedanz=eval("lambda u,t,du,U,f,a:"+self.dictWidgets["Impedanz"].get())(u,time,du,U,self.frequency,self.amplitude)
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
        switch = Switch()
        this=self
        def attachSine():
            this.dictWidgets["someFunction"]=sine
            this.dictWidgets["tastGrad"].grid_remove()
        def sine(amplitude,frequency,time):
            return amplitude*np.sin(time*2*np.pi*frequency+self.phi)
        def attachRechteck():
            this.dictWidgets["someFunction"]=rechteck
            this.dictWidgets["tastGrad"].grid(column=5,row=0,sticky="ns",rowspan=4)
        def rechteck(amplitude,frequency,time):
            return amplitude*scipy.signal.square(time*2*np.pi*frequency+self.phi,duty=this.dictWidgets["tastGrad"].get())
        def attachsawtooth():
            this.dictWidgets["tastGrad"].grid(column=5,row=0,sticky="ns",rowspan=4)
            this.dictWidgets["someFunction"]=sawtooth
        def sawtooth(amplitude,frequency,time):
            return amplitude*scipy.signal.sawtooth(time*2*np.pi*frequency+self.phi,width=this.dictWidgets["tastGrad"].get())
        case_1 = attachSine
        case_2 = attachRechteck
        case_3 = attachsawtooth
        case_4 = lambda : print("load swa")
        switch.add_case("sinus", case_1, True)
        switch.add_case("rechteck", case_2, True)
        switch.add_case("sawtooth", case_3, True)
        switch.add_case("rechteck", case_3, True)
        switch.case(a)
    def change_frequency(self,freq):
        oldfrequency=self.frequency
        self.frequency=float(freq)
        oldphase=self.phi
        tau=2*np.pi
        t=self.time[-1]+0.0001 if len(self.time)>0 else 0
        self.phi=(tau*(oldfrequency-self.frequency)*t+oldphase)%tau
        #print(("old",oldfrequency,"new",freq,"time",t,"oldphi",oldphase,"phi",self.phi,"1",(t*tau*oldfrequency+oldphase)%tau,"2",(t*tau*self.frequency+self.phi)%tau))

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
        #Adding Sliders and widgets
        self.createSlider("frequency",0,200,command=self.change_frequency).grid(column=1,row=1,sticky="ew",ipadx=120)
        self.createDropdown("dropdown",["sinus","sawtooth","rechteck"],self.onSelection).grid(column=3,row=1,columnspan=2,sticky="ew",ipadx=120)
        self.createSlider("amplitude",0,100).grid(column=1,row=2,sticky="ew",ipadx=120)
        tk.Label(self,text="Z =").grid(column=3, row=2,sticky="w")
        self.createTextInput("Impedanz","1").grid(column=4,row=2,sticky="w",ipadx=120)
        def do_popup(menu):
            def do_popup(event):
                try:
                    menu.tk_popup(event.x_root, event.y_root)
                finally:
                    menu.grab_release()
            return do_popup
        def change_text_in_input(text):
            w=self.dictWidgets["Impedanz"]
            w.delete(0,tk.END)
            w.insert(tk.END,text)
        self.m.add_command(label="Kondensator",command=lambda:change_text_in_input("2*np.pi*f*u/du"))
        self.m.add_command(label="Kondensator + Widerstand",command=lambda:change_text_in_input("u/(du+u*99)*2*np.pi*f*2"))
        self.m.add_command(label="Spule",command=lambda:change_text_in_input("u/(2*np.pi*f*U)"))
        self.m.add_command(label="Diode",command=lambda:change_text_in_input("9999999 if u<0 else 1"))
        self.m.add_command(label="Dimmer",command=lambda:change_text_in_input("99999999 if (du>0 and 9/10*a>u>0)or(du<0 and -9/10*a<u<0) else 1"))

        self.dictWidgets["Impedanz"].bind("<Button-3>",do_popup(self.m))
        CreateToolTip(self.dictWidgets["Impedanz"],"""Impedanz als Funktion abhängig von Spannung und Zeit
Ein Python Ausdruck
Rechtsklick um Beispielmenu zu Zeigen
Variabeln
----------
u= Spannung
du = Ableitung der Spannung
U= Integral der Spannung 
t= Zeit in (s)
a= Amplitude
f= Frequenz""")
        def reset():
            self.spannung=[]
            self.power=[]
            self.time=[]
            self.current=[]
            self.ueff=[]
            self.ueffv=0
            self.ieff=[]
            self.ieffv=0
            self.peff=[]
            self.animation_object.frame_seq = self.animation_object.new_frame_seq()
            self.intU=0
            for ax in self.axes:
                for artist in ax.lines + ax.collections:
                    artist.remove()
                ax.relim()
                ax.autoscale()
        self.canvm.add_command(label="Reset",command=reset)
        self.showeff=tk.BooleanVar()
        self.sym=tk.BooleanVar()
        self.showlegend=tk.BooleanVar()
        self.sym.set(True)
        self.showlegend.set(True)
        self.canvm.add_checkbutton(label="Effektive Werte zeigen",onvalue=1,offvalue=0,variable=self.showeff)
        self.canvm.add_checkbutton(label="Y Achse symmetrisch",onvalue=1,offvalue=0,variable=self.sym)
        self.canvm.add_checkbutton(label="Zeige Legende",onvalue=1,offvalue=0,variable=self.showlegend)
        self.canvm.add_cascade(label="View",menu=self.viewm)
        self.viewm.add_command(label="View 1",command=lambda:self.create_axes(1))
        self.viewm.add_command(label="View 2",command=lambda:self.create_axes(2))
        self.viewm.add_command(label="View 3",command=lambda:self.create_axes(3))
        self.viewm.add_command(label="View 4",command=lambda:self.create_axes(4))
        self.canvas.bind("<Button-3>",do_popup(self.canvm))
        self.canvas.grid(column=0,row=3,columnspan = 5)
        self.createSlider("tastGrad",0,1,resolution=0.01,orient=tk.VERTICAL)
    def create_axes(self,view):
        #Creating axes
        self.figure.clear()
        if view==1:
            self.figure.subplots_adjust(right=0.75)
            self.axes=[self.figure.add_subplot(1,1,1)]
            self.axes.append(self.axes[0].twinx())
            self.axes.append(self.axes[0].twinx())
            self.axes[1].spines.right.set_position(("axes",1.2))
        elif view==2:
            self.figure.subplots_adjust(right=0.9)
            self.axes=[self.figure.add_subplot(1,2,1),self.figure.add_subplot(1,2,2)]
            self.axes.append(self.axes[0].twinx())
        elif view==3:
            self.figure.subplots_adjust(right=0.9)
            self.axes=[self.figure.add_subplot(2,1,1),self.figure.add_subplot(2,1,2)]
            self.axes.append(self.axes[0].twinx())
        elif view==4:
            self.figure.subplots_adjust(right=0.9)
            self.axes=[self.figure.add_subplot(3,1,1),self.figure.add_subplot(3,1,3),self.figure.add_subplot(3,1,2)]
        self.axes[0].set_xlabel('Zeit (s)')
        self.axes[1].set_xlabel('Zeit (s)')
        for i,(l,c) in enumerate([('Spannung (V)',"Blue"),('Leistung (W)',"red"),('Strom (A)',"orange")]):
            self.axes[i].set_ylabel(l)
            self.axes[i].yaxis.label.set_color(c)
        self.axes[1].yaxis.tick_right()
        self.axes[1].yaxis.set_label_position("right")
        #10000*10*10 #self.resizable(False, False) #self.columnconfigure(0, weight=0) #self.columnconfigure(1, weight=10)
        
exercise_06 = TKWindow(window_title)
exercise_06.window_loop()
