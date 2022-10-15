# -*- coding: utf-8 -*-
"""
Created 2022

Für eine Messreihe wird jeweils die Regression, lineare Interpolation und spline
Interpolation geplottet und die geschätzten Werte für eine unbekannte Größe ausgegeben.

Beispielweise würde hier der Wiederstand in abhängigkeit er Temperatur approximiert und ausgerechnet 

@author: Datenschutz bitte.
"""
import tkinter as tk
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import interpolate  as ip

liste_reg_and_interp=["Methode der kleinsten Quadrate","Lineare Interpolation","Kubische Splines"]
N=5
a=None
b=None
root= tk.Tk()
def sortinputandoutput(x,y):
    """Sortiert die input und output damit wir linear interpolieren können

    Args:
        x (Array of int32): x Werte, Werte vom ersten array 
        y (Array of int32): y Werte, Werte vom zweiten array 

    Returns:
        list: beinhaltet die x und y Werte 
    """    ""
    l=list(zip(x,y))
    l.sort(key=lambda a:a[0])
    return list(zip(*l))

def makeline(x,y):
    """Erstellt eine lineare approximation zwischen zwei Punkten 

    Args:
        x (Array of int32): x Wert
        y (Array of int32): y Wert

    Returns:
        (float,float): Paramater für die Funktion y=ax+b
    """    ""
    N=len(x)
    a_numerator=N*np.sum(x*y)-(np.sum(y)*np.sum(x))
    a_denominator=N*np.sum(x**2)-(np.sum(x))**2
    a=a_numerator/a_denominator
    b_numerator=np.sum(y)*np.sum(x**2)-np.sum(y*x)*np.sum(x)
    b_denominator=N*np.sum(x**2)-(np.sum(x))**2
    b=b_numerator/b_denominator
    return a,b


def Regression(x,y):
    """Regression für eine beliegige Messreihe
    Args:
        x (Array of int32): _description_
        y (Array of int32): _description_
    """    ""
    a,b=makeline(x,y)
    a=float("{:.3f}".format(a))
    y_antwort_text.set(a)
    b=float("{:.3f}".format(b))
    x_antworten_antworten.set(b)
    xvl = np.linspace(min(x), max(x), 10000)
    yvl=a*xvl+b
    plot1.plot(xvl,yvl,color='blue')
    plot1.legend(['Messdaten','Lineare Regression'])
    plot1.set_title('Lineare Regression')
    plot1.grid()
    [x.grid() for x in [result_label,result_labela,result_labelb,resultb, result_labely, result_labelx,  resulta1, resultVonDerYvariable, resultVonDerXVariabeln]]
    
def remove():
    [x.grid_remove() for x in [result_label,result_labela,result_labelb,resultb, result_labely, result_labelx,  resulta1, resultVonDerYvariable, resultVonDerXVariabeln]]
    
def Lineare_interpolation(x,y):
    """Lineare Interpolation für eine beliegige Messreihe


    Args:
        x (Array of int32): x Werte 
        y (Array of int32): y Werte 
    """    ""
    remove()
    plot1.plot(x, y)
    plot1.legend(['Messdaten','Lineare Interpolation'])
    plot1.set_title('Lineare Interpolatione')
    plot1.grid()
    
def Spline(x,y):
    """Spline Interpolation für eine beliegige Messreihe

    Args:
        x (Array of int32): x Werte 
        y (Array of int32): y Werte
    """    ""
    remove()
    spl = ip.CubicSpline(x, y)
    x_sp = np.linspace(x.min(), x.max(), 10000)
    y_sp = spl(x_sp)
    plot1.plot(x_sp, y_sp)
    plot1.legend(['Messdaten','Spline Interpolation'])
    plot1.set_title('Spline Interpolatione')
    plot1.grid()
    
#def plot1():
figure3 = plt.Figure(figsize=(6,4), dpi=100) 
#scatter3 = FigureCanvasTkAgg(figure3, root) 
#scatter3.get_tk_widget().grid(row=6, column=3,columnspan = 100, rowspan = 24, padx = 0, pady = 0)
plot1 = figure3.add_subplot(111)
scatter3 = FigureCanvasTkAgg(figure3, root) 
scatter3.get_tk_widget().grid(row=6, column=3,columnspan = 100, rowspan = 24, padx = 0, pady = 0)
#ani=animation.FuncAnimation(plt.gcf(), lambda a:None, [1], interval=100,blit=False)
plot1.set_xlabel('x [z.B. Temperatur in °C]') 
plot1.set_ylabel('y [z.B. Widerstand in \u03A9]') 


def res():
    """Schätzung von Werten für eine unbekannte Größe
    """  
    #Wir lesen die Eingabe temperatur 
    try:    
        xvltemp=float(number_array[10].get())
        number_array[10].config(bg="white")
    except Exception as e:
        number_array[10].config(bg="red")
        return
    if s==liste_reg_and_interp[0]:
        '''
        Das ist Lineare regression für eine bestimmte Temperatur
        '''
        a,b=makeline(x,y)
        ergebnisse=a*xvltemp+b
        ergebnisse=float("{:.3f}".format(ergebnisse))
    elif s==liste_reg_and_interp[1]:
        '''
        Das ist linear interpolation für eine bestimmte Temperatur
        '''
        #x0=xvltemp
        ergebnisse=findValue(x,xvltemp,y)
    elif s==liste_reg_and_interp[2]:
        '''
        Das ist cubische regression für eine bestimmte Temperatur
        '''
        spl = ip.CubicSpline(x, y)
        x_sp = np.linspace(x.min(), x.max(), 1000)
        y_sp = spl(x_sp)
        ergebnisse=findValue(x_sp,xvltemp,y_sp)
    text3.set(ergebnisse)

def findValue(x,x0,y):
    xmin=min(x)
    xmax=max(x)
    if x0<xmin or x0>xmax:
        y_for_temp='Fail'
        #return "FAIL"
    else:
        #print(x0)
        x_variabel_fuer_anfang_Lin_interp=np.max(list(filter(lambda n:n<x0, x)))
        x_variabel_fuer_ende_Lin_interp=np.min(list(filter(lambda n:n>=x0, x)))
        x_und_y_gezippt=tuple(zip(x,list(y)))
        #print(list(x_und_y_gezippt))
        x_und_y_gedict=dict(list(x_und_y_gezippt))
        y_wert_1=x_und_y_gedict[x_variabel_fuer_anfang_Lin_interp]
        y_wert_2=x_und_y_gedict[x_variabel_fuer_ende_Lin_interp]

        x_wert_1=x_variabel_fuer_anfang_Lin_interp
        x_wert_2=x_variabel_fuer_ende_Lin_interp    
        #print(x_wert_1,x_wert_2,y_wert_1,y_wert_2)
        a,b=makeline(np.array([x_wert_1,x_wert_2]), np.array([y_wert_1,y_wert_2]))
        y_for_temp=a*x0+b
        y_for_temp=float("{:.3f}".format(y_for_temp))    
        return y_for_temp


s=liste_reg_and_interp[0]   
def drop_down_change(dp):
    global s
    s=dp
    plotAktualizieren()
 
def plotAktualizieren():
    """Der plot im Fenster wird aktualisiert
    """    
    plot1.clear()
    global x,y,N
    values=[]
    for i in range(10):
        try:
            values.append(float(number_array[i].get()))
            number_array[i].config(bg="white")
        except Exception as e:
            number_array[i].config(bg="red")
            return

    
    x=np.array(values[0:5])
    y=np.array(values[5:10])
   
    plot1.scatter(x,y,color='red')
    plot1.set_xlabel('x [z.B. Temperatur in °C]') 
    plot1.set_ylabel('y [z.B. Widerstand in \u03A9]') 
    x,y=[np.array(t) for t in sortinputandoutput(x,y)]
    if s==liste_reg_and_interp[0]:
        Regression(x,y)
    elif s==liste_reg_and_interp[1]:
        Lineare_interpolation(x,y)
    elif s==liste_reg_and_interp[2]:
        Spline(x,y)
    figure3.canvas.draw()
    figure3.canvas.flush_events()
  
widgetObjects = {"result_label":{"name":"result_label",
                                 "text":"Results : ",
                                "variable":None}}
y_antwort_text=tk.StringVar()
x_antworten_antworten=tk.StringVar()
text3=tk.StringVar()
#dropdown_menu=tk.StringVar(root)
#dropdown_menu.set(liste_reg_and_interp[0])

root.geometry("800x600")
root.title('Übung 2')  
Corona_rules=tk.StringVar()
Corona_rules.set(liste_reg_and_interp[0])
menu= tk.OptionMenu(root, Corona_rules, *liste_reg_and_interp,command=drop_down_change)
menu.config(width=30, font=('Times New Roman', 9))
menu.grid(row=0, column=10)


    
result_label=tk.Label(root, text="Results : ")
result_label.grid(row=1, column=11)
result_labela=tk.Label(root, text="a= ")
result_labela.grid(row=2, column=12)
resulta1=tk.Label(root, text="", textvariable=y_antwort_text)
resulta1.grid(row=2,column=13)
result_labelb=tk.Label(root, text="b= ")
result_labelb.grid(row=3, column=12)
resultb=tk.Label(root, text="", textvariable=x_antworten_antworten)
resultb.grid(row=3,column=13)
result_labely=tk.Label(root, text="y= ")
result_labely.grid(row=4, column=12)
resultVonDerYvariable=tk.Label(root, text="", textvariable=y_antwort_text)
resultVonDerYvariable.grid(row=4,column=13)
result_labelx=tk.Label(root, text="x + ")
result_labelx.grid(row=4, column=14)
resultVonDerXVariabeln=tk.Label(root, text="", textvariable=x_antworten_antworten)
resultVonDerXVariabeln.grid(row=4,column=15)
inputValuesTkx = tk.Label(root, text="Input values 1 (x) ")
inputValuesTkx.grid(row=0, column=0)
inputValuesTky = tk.Label(root, text="Input values 2 (y) ")
inputValuesTky.grid(row=6, column=0)

number_array=[]
for i in range(5):
    num= tk.Entry(root,justify='center')
    num.grid(row=i+1, column=0,pady=4) 
    num.insert(tk.END, str(i)) 
    number_array.append(num)
for i in range(5,10):
    number_array.append(tk.Entry(root,justify='center'))
    number_array[i].grid(row=i+2, column=0)  
    number_array[i].insert(tk.END, str(random.randrange(0, (i-4)*10))) 


button= tk.Button(root, text="Calculate", command=lambda:[plotAktualizieren()])
button.grid(row=12, column=0)  


emp=tk.Label(root, text="Unbekannte Größe ").grid(row=13, column=0)

number_array.append(tk.Entry(root,justify='center'))
number_array[10].grid(row=14, column=0)
number_array[10].insert(tk.END, '3') 
button2 = tk.Button(root,text="Calculate 2",command=res)
button2.grid(row=15, column=0)

result_labely2=tk.Label(root, text="y= ")
result_labely2.grid(row=16, column=0)
resulta2a=tk.Label(root, text="", textvariable=text3)
resulta2a.grid(row=17,column=0)
result_labely3=tk.Label(root, text="\u03A9")
result_labely3.grid(row=17, column=1)
  
root.mainloop()
