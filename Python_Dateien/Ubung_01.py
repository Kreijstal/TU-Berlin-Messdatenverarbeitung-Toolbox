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
    global oldscale1
    global oldscale2
    global oldscale3
    newscale1=scale.get()
    newscale2=scale2.get()
    newscale3=scale3.get()
    if var1.get()==0 and oldscale1==newscale1 and oldscale2==newscale2 and oldscale3==newscale3:
        pass
    else:
        ax.cla()
        ax.set_title("Normal Verteilung")
        datemsatz1=np.random.normal(size=newscale2) if var2.get()==0 else rand1[:newscale2]
        #print
        hist=ax.hist(datemsatz1,bins=newscale1,label="Histogram")

        ax.axvspan(datemsatz1.mean()-datemsatz1.std(),datemsatz1.mean()+datemsatz1.std(), ymax=hist[0].max() ,alpha=0.5, color='red',label="Vertrauensinterval")
        #ax.fill_between()
        ax.legend(loc="upper right")
        ax2.cla()
        ax2.set_title("Student T Verteilung")
        datemsatz2=np.random.standard_t(newscale3,size=newscale2) if var2.get()==0 else rand2[:newscale2]
        hist=ax2.hist(datemsatz2,bins=newscale1)
        oldscale1=newscale1
        oldscale2=newscale2
        oldscale3=newscale3
        return hist
    pass

rand1=None
rand2=None
def generate_Datensatz():
    global rand1
    global rand2
    if var2.get()==1: 
        rand1=np.random.normal(size=10000)
        rand2=np.random.standard_t(scale3.get(),size=10000)
        scale3.configure(state="disable")
        scale3.grid_remove()
        c1.configure(state="disable")
        var1.set(0)
    else:
        scale3.grid(column=2,row=5)
        scale3.configure(state="normal")
        c1.configure(state="normal")

root = Tk.Tk()
scale = Tk.Scale(root,orient=Tk.HORIZONTAL,length=300, from_=2, to=100)
scale2 = Tk.Scale(root,orient=Tk.HORIZONTAL,length=300, from_=2, to=10000)
#scale.pack()
label = Tk.Label(root,text="Normal und Student Verteilung").grid(column=0, row=0)
Tk.Label(root,text="Es ist möglich mit den Sliders zu Spielen").grid(column=0,row=1)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0,row=2,columnspan = 2, rowspan = 7, padx = 0, pady = 0)
Tk.Label(root,text="#bins").grid(column=2,row=0)
scale.grid(column=2,row=1)
Tk.Label(root,text="#samples").grid(column=2,row=2)
scale2.grid(column=2,row=3)
Tk.Label(root,text="Freiheitsgrad von student T").grid(column=2,row=4)
scale3 = Tk.Scale(root,orient=Tk.HORIZONTAL,length=300, from_=1, to=100)
scale3.grid(column=2,row=5)
var1=Tk.IntVar()
var2=Tk.IntVar()
c1=Tk.Checkbutton(root, text='refresh samples/frame',variable=var1, onvalue=1, offvalue=0)
c1.grid(column=1,row=0)
c2=Tk.Checkbutton(root, text='Freeze datensatz',variable=var2, onvalue=1, offvalue=0,command=generate_Datensatz)
c2.grid(column=1,row=1)
ax = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
fig.tight_layout() 
ani=animation.FuncAnimation(fig, animate, np.arange(1, 64), interval=100,
        blit=False)
root.title("Übung 1 MT1")
root.mainloop()
