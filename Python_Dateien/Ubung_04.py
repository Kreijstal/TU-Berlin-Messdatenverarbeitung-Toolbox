import sys,getopt
import numpy as np
import control
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as Tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import svg.path
import control.matlab
import yaml

try:
   opts, args = getopt.getopt(sys.argv[1:],"r",["render"])
except getopt.GetoptError:
   print("Invalid param")
   sys.exit(2)
for opt, arg in opts:
      if opt == '-r':
         #!pip install svg.path
         #!pip install latextools
         #!pip install drawSvg
         import latextools
         latex_eq = latextools.render_snippet(r'''
\begin{minipage}[0pt]{180pt}
Sei $\omega_s$ die Eigenfrequenz und $\zeta$ die Dämpfungsgrad, eine 2te Ordnung LTI Übertragungsfunktion sieht so aus
$$H(s)=\frac{\omega_s^2}{s^2+s\zeta\omega_s+\omega_s^2}$$
mit $\cos(\phi)=\zeta$ für $-1<\zeta <1$ die Zeitfunktion kann man so schreiben:\\
\[H(t)=1-\frac{e^{-z\omega_s t}}{\sqrt{1-z^{2}}}\sin\left(\omega_s\sqrt{1-z^{2}}t+\phi\right)\]
%$t_r=\frac{\pi-\phi}{\omega_s\sin(\phi)}$
Und die Polen sind an der Stellen
\[s=-\zeta \omega_s\pm j\omega_s\sqrt{1-\zeta^2}\]
\end{minipage} 
'''.strip(),
    pad=1)
         latex_eq.as_svg().as_drawing().rasterize().savePng("eq1.png")
#fig = plt.Figure(figsize=(5,5))  
root = Tk.Tk()

##scale.pack()
Tk.Label(root,text="2te Ordnung LTI").grid(column=0, row=0)
canvas = Tk.Canvas(root)
#https://www.electrical4u.com/time-response-of-second-order-control-system/
photoimage = Tk.PhotoImage(master=canvas,file="eq1.png")
canvas.create_image(160, 130, image=photoimage)
canvas.grid(column=0,row=1, rowspan = 10)
#Tk.Label(root,text="Es ist möglich mit den Sliders zu Spielen").grid(column=0,row=1)
w_s=1
z=1
sys = control.tf([w_s^2], [1, w_s* z,w_s^2]) 
plt.figure("Bode",figsize=(6,5))
control.bode_plot(sys)
canvas2 = FigureCanvasTkAgg(plt.gcf(), master=root)
canvas2.get_tk_widget().grid(column=0,row=11,columnspan = 1, rowspan = 7, padx =0, pady = 0)

ani=animation.FuncAnimation(plt.gcf(), lambda a:None, [1], interval=100,blit=False)
def onVarChange():
    #print(([w_s^2], [1, w_s* z,w_s^2]))
    sys = control.tf([w_s^2], [1, w_s* z,w_s^2]) 
    #plt.close()
    plt.figure("Bode")
    plt.clf()
    control.bode_plot(sys)
    plt.figure("Bode")
    plt.title("Bode plot")
    plt.figure("pzmap")
    plt.clf()
    control.pzmap(sys)
    plt.figure("step_response")
    plt.cla()
    t,y=control.step_response(sys)
    plt.plot(t,y)
    plt.title("Sprungantwort")
    plt.grid()
    Tk.Label(root,text=yaml.dump({k: float(v) for k, v in control.matlab.stepinfo(sys).items()})).grid(column=2,row=0, rowspan = 7)
    #canvas2.get_tk_widget().grid_remove()
    #canvas2 = FigureCanvasTkAgg(plt.gcf(), master=root)
    #canvas2.get_tk_widget().grid(column=0,row=11,columnspan = 2, rowspan = 7, padx = 0, pady = 0)
def onZetaChange(_):
    global z
    z=float(_)
    onVarChange()

def onfrequenzChange(_):
    global w_s
    w_s=int(_)
    onVarChange()
Tk.Label(root,text="zeta").grid(column=1,row=0)
scale = Tk.Scale(root,orient=Tk.HORIZONTAL,length=300, from_=-5, to=5,resolution =   0.01,command= onZetaChange )
scale.grid(column=1,row=1)
Tk.Label(root,text="Eigenfrequenz").grid(column=1,row=2)
scale2 = Tk.Scale(root,orient=Tk.HORIZONTAL,length=300, from_=0, to=100,command= onfrequenzChange)
scale2.grid(column=1,row=3)
fig = plt.figure("pzmap",figsize=(6,5))
control.pzmap(sys)
canvas3 = FigureCanvasTkAgg(fig, master=root)
canvas3.get_tk_widget().grid(column=1,row=11,columnspan = 1, rowspan = 7, padx = 0, pady = 0)
ani2=animation.FuncAnimation(plt.gcf(), lambda a:None, [1], interval=100,blit=False)
fig2 = plt.figure("step_response",figsize=(5,5))
canvas4 = FigureCanvasTkAgg(fig2, master=root)
canvas4.get_tk_widget().grid(column=2,row=11,columnspan = 1, rowspan = 7, padx = 0, pady = 0)
ani3=animation.FuncAnimation(plt.gcf(), lambda a:None, [1], interval=100,blit=False)
t,y=control.step_response(sys)
plt.title("Sprungantwort")
plt.plot(t,y)
plt.grid()
#Tk.Label(root,text="#samples").grid(column=2,row=2)
#scale2.grid(column=2,row=3)
#Tk.Label(root,text="Freiheitsgrad von student T").grid(column=2,row=4)
#scale3 = Tk.Scale(root,orient=Tk.HORIZONTAL,length=300, from_=1, to=100)
#scale3.grid(column=2,row=5)
#var1=Tk.IntVar()
#var2=Tk.IntVar()
#c1=Tk.Checkbutton(root, text='refresh samples/frame',variable=var1, onvalue=1, offvalue=0)
#c1.grid(column=1,row=0)

#c2=Tk.Checkbutton(root, text='Freeze datensatz',variable=var2, onvalue=1, offvalue=0,command=generate_Datensatz)
#c2.grid(column=1,row=1)
#ax = fig.add_subplot(211)
#ax2 = fig.add_subplot(212)
#fig.tight_layout() 
#ani=animation.FuncAnimation(fig, animate, np.arange(1, 64), interval=100,
#        blit=False)
root.title("Übung 4 MT1")
root.mainloop()
plt.close()