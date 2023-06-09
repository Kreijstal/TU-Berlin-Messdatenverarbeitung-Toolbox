import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as Tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

"""
Das folgende ist eine Sigma delta Umsetzer
"""
fig = plt.Figure(figsize=(9, 9))
x = []
m = 1
xint = 0
xintlist = []
hm = []
hmm = 0
err = 0
errlist = []
errcum = 0
errcumlist = []


def animate(i):
    global xint
    global err
    global errcum
    global err
    global hmm
    currvalue = scale.get()
    x.append(currvalue)
    errlist.append(err)
    errcumlist.append(errcum)
    xintlist.append(xint)
    err = hmm * 20 - 10 - currvalue
    errcum += err
    if errcum > 0:
        hmm = 0
    else:
        hmm = 1
    hm.append(hmm)

    if len(x) > 25:
        hm.pop(0)
        x.pop(0)
        errcumlist.pop(0)
        errlist.pop(0)
    # ax.legend(loc="upper right")
    ax.cla()
    ax2.set_title("Student T Verteilung")
    ax.plot(x, label="eingabe signal")
    # ax.plot(xintlist)
    ax.plot(errlist, label="Fehler")
    ax.plot(errcumlist, label="kumulativer Fehler")
    ax.legend()
    ax2.cla()
    ax2.step(np.arange(0, len(hm)), hm)


root = Tk.Tk()
scale = Tk.Scale(
    root, orient=Tk.HORIZONTAL, length=300, from_=-10.0, to=10.0, resolution=0.05
)
# scale2 = Tk.Scale(root,orient=Tk.HORIZONTAL,length=300, from_=2, to=10000)
# scale.pack()
label = Tk.Label(root, text="Normal und Student Verteilung").grid(column=0, row=0)
Tk.Label(root, text="Es ist möglich mit den Sliders zu Spielen").grid(column=0, row=1)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0, row=2, columnspan=2, rowspan=7, padx=0, pady=0)
Tk.Label(root, text="#bins").grid(column=2, row=0)
scale.grid(column=2, row=1)
# Tk.Label(root,text="#samples").grid(column=2,row=2)
# scale2.grid(column=2,row=3)
# Tk.Label(root,text="Freiheitsgrad von student T").grid(column=2,row=4)
# scale3 = Tk.Scale(root,orient=Tk.HORIZONTAL,length=300, from_=1, to=100)
# scale3.grid(column=2,row=5)
# var1=Tk.IntVar()
# var2=Tk.IntVar()
# c1=Tk.Checkbutton(root, text='refresh samples/frame',variable=var1, onvalue=1, offvalue=0)
# c1.grid(column=1,row=0)
# c2=Tk.Checkbutton(root, text='Freeze datensatz',variable=var2, onvalue=1, offvalue=0,command=generate_Datensatz)
# c2.grid(column=1,row=1)
ax = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
fig.tight_layout()
ani = animation.FuncAnimation(fig, animate, np.arange(1, 64), interval=100, blit=False)
root.title("Sigma Delta Umsetzer")
root.mainloop()
