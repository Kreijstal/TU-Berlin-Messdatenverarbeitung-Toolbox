# -*- coding: utf-8 -*-
"""
Created on 2022

Für eine Messreihe das vollständige Messergebnis unter der Normalverteilung bzw.
Student-t Verteilung für die Verschiedenen Vertrauensintervalle plotten. Dabei werden die entsprechenden Zwischenschritte (Mittelwert, Standardabweichung, usw.)
mit geplottet

@author: Datenschutz bitte.
"""


#Mit '#' am anfangs der Zeile können wir kommentieren
#Willkommen zur MT1! Here we see the most commonly used commands for python that you can use for the protocols.
print("mit den print Funktion können wir text in den Terminal ausgeben.")
#Wir importieren modulen mit import
import sys

print("Die Python version ist %d.%d.%d"%(sys.version_info.major,sys.version_info.minor,sys.version_info.micro))

#man kann immer die Funktion help anwenden um herauszufinden, wie eine Funktion dokumentiert ist z.B
#help(print)

##Messunsicherheit und Statistik
#Es ist sehr wichtig das wir auch numpy installiert haben, man könnte es installieren mit !pip install numpy, aber normalerweiser es ist immer mit python gebü
# ndelt
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as Tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


fig = plt.Figure(figsize=(5,5))  
oldscale1=0
oldscale2=0
oldscale3=0
def animate(i):
    """
    Diese funktiion animiert jede Frame

    Args:
        i (int): ein Zahl, wird ignoriert.

    Returns:
        Histogramm, die zufälligt erzeugt würde.
    """    
    global oldscale1
    global oldscale2
    global oldscale3
    newscale1=anzahlVonBins.get()
    newscale2=anzahlSamples.get()
    newscale3=freiheitgradVonStudenTverteilung.get()
    if var1.get()==0 and oldscale1==newscale1 and oldscale2==newscale2 and oldscale3==newscale3:
        pass
    else:
        ax.cla()
        ax.set_title("Normal Verteilung")
        datemsatz1=np.random.normal(size=newscale2) if var2.get()==0 else zuffaligeDatenMitNormaleVerteilung[:newscale2]
        #print
        hist=ax.hist(datemsatz1,bins=newscale1,label="Histogram")

        ax.axvspan(datemsatz1.mean()-datemsatz1.std(),datemsatz1.mean()+datemsatz1.std(), ymax=hist[0].max() ,alpha=0.5, color='red',label="Vertrauensinterval 1$\sigma$, 68,3%")
        #ax.fill_between()
        ax.legend(loc="upper right")
        ax2.cla()
        ax2.set_title("Student T Verteilung")
        datemsatz2=np.random.standard_t(newscale3,size=newscale2) if var2.get()==0 else zuffaligeDatenMitTstudentverteilung[:newscale2]
        hist=ax2.hist(datemsatz2,bins=newscale1)
        oldscale1=newscale1
        oldscale2=newscale2
        oldscale3=newscale3
        return hist
    pass

zuffaligeDatenMitNormaleVerteilung=None
zuffaligeDatenMitTstudentverteilung=None
def generate_Datensatz():
    """
    Es generiert zufällige Daten
    """    
    global zuffaligeDatenMitNormaleVerteilung
    global zuffaligeDatenMitTstudentverteilung
    if var2.get()==1: 
        zuffaligeDatenMitNormaleVerteilung=np.random.normal(size=10000)
        zuffaligeDatenMitTstudentverteilung=np.random.standard_t(freiheitgradVonStudenTverteilung.get(),size=10000)
        freiheitgradVonStudenTverteilung.configure(state="disable")
        freiheitgradVonStudenTverteilung.grid_remove()
        IstRefreshSamplesGecheckht.configure(state="disable")
        var1.set(0)
    else:
        freiheitgradVonStudenTverteilung.grid(column=2,row=5)
        freiheitgradVonStudenTverteilung.configure(state="normal")
        IstRefreshSamplesGecheckht.configure(state="normal")

root = Tk.Tk()
anzahlVonBins = Tk.Scale(root,orient=Tk.HORIZONTAL,length=300, from_=2, to=100)
anzahlSamples = Tk.Scale(root,orient=Tk.HORIZONTAL,length=300, from_=2, to=10000)
#scale.pack()
label = Tk.Label(root,text="Normal und Student Verteilung").grid(column=0, row=0)
Tk.Label(root,text="Es ist möglich mit den Sliders zu Spielen").grid(column=0,row=1)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0,row=2,columnspan = 2, rowspan = 7, padx = 0, pady = 0)
Tk.Label(root,text="#bins").grid(column=2,row=0)
anzahlVonBins.grid(column=2,row=1)
Tk.Label(root,text="#samples").grid(column=2,row=2)
anzahlSamples.grid(column=2,row=3)
Tk.Label(root,text="Freiheitsgrad von student T").grid(column=2,row=4)
freiheitgradVonStudenTverteilung = Tk.Scale(root,orient=Tk.HORIZONTAL,length=300, from_=1, to=100)
freiheitgradVonStudenTverteilung.grid(column=2,row=5)
var1=Tk.IntVar()
var2=Tk.IntVar()
IstRefreshSamplesGecheckht=Tk.Checkbutton(root, text='refresh samples/frame',variable=var1, onvalue=1, offvalue=0)
IstRefreshSamplesGecheckht.grid(column=1,row=0)
istGefroren=Tk.Checkbutton(root, text='Freeze datensatz',variable=var2, onvalue=1, offvalue=0,command=generate_Datensatz)
istGefroren.grid(column=1,row=1)
ax = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
fig.tight_layout() 
ani=animation.FuncAnimation(fig, animate, np.arange(1, 64), interval=100,
        blit=False)
root.title("Übung 1 MT1")
root.mainloop()
