# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 13:37:14 2022

@author: Boris
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
    l=list(zip(x,y))
    l.sort(key=lambda a:a[0])
    return list(zip(*l))

def makeline(x,y):
    """returns a,b"""
    N=len(x)
    a_numerator=N*np.sum(x*y)-(np.sum(y)*np.sum(x))
    a_denominator=N*np.sum(x**2)-(np.sum(x))**2
    a=a_numerator/a_denominator
    b_numerator=np.sum(y)*np.sum(x**2)-np.sum(y*x)*np.sum(x)
    b_denominator=N*np.sum(x**2)-(np.sum(x))**2
    b=b_numerator/b_denominator
    return a,b


def Regression(x,y):
    a,b=makeline(x,y)
    a=float("{:.3f}".format(a))
    text1.set(a)
    b=float("{:.3f}".format(b))
    text2.set(b)
    xvl = np.linspace(min(x), max(x), 100)
    yvl=a*xvl+b
    plot1.plot(xvl,yvl,color='blue')
    plot1.legend(['Messdaten','Lineare Regression'])
    plot1.set_title('Lineare Regression')
    [x.grid() for x in [result_label,result_labela,result_labelb,resultb, result_labely, result_labelx,  resulta1, resulta2, resulta3]]
    
def remove():
    [x.grid_remove() for x in [result_label,result_labela,result_labelb,resultb, result_labely, result_labelx,  resulta1, resulta2, resulta3]]
    
def Lineare_interpolation(x,y):
    remove()
    plot1.plot(x, y)
    plot1.legend(['Messdaten','Lineare Interpolation'])
    plot1.set_title('Lineare Interpolatione')
    
def Spline(x,y):
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
plot1.set_xlabel('x [Temperatur in °C]') 
plot1.set_ylabel('y [Widerstand in \u03A9]') 


def res():
    ''' Funktion wird aufgerufen um den Widerstand für bestimtte Temperatur ausgerchent
    

    '''
    #Wir lesen die Eingabe temperatur 
    xvltemp=float(num11.get())
    if s==liste_reg_and_interp[0]:
        '''
        Das ist Lineare regression für eine bestimmte Temperatur
        '''
        a,b=makeline(x,y)
        y_for_temp=a*xvltemp+b
        y_for_temp=float("{:.3f}".format(y_for_temp))
    elif s==liste_reg_and_interp[1]:
        '''
        Das ist linear interpolation für eine bestimmte Temperatur
        '''
        x0=xvltemp
        xmin=min(x)
        xmax=max(x)
        if x0<xmin or x0>xmax:
            y_for_temp='Fail'
            #return "FAIL"
        else:
            print(x0)
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
            y_for_temp=a*xvltemp+b
            y_for_temp=float("{:.3f}".format(y_for_temp))
    elif s==liste_reg_and_interp[2]:
        '''
        Das ist cubische regression für eine bestimmte Temperatur
        '''
        x0=xvltemp
        spl = ip.CubicSpline(x, y)
        x_sp = np.linspace(x.min(), x.max(), 1000)
        y_sp = spl(x_sp)
        xmin=min(x_sp)
        xmax=max(x_sp)
        if x0<xmin or x0>xmax:
            y_for_temp='Fail'
            #return "FAIL"
        else:
            print(x0)
            x_variabel_fuer_anfang_Lin_interp=np.max(list(filter(lambda n:n<x0, x_sp)))
            x_variabel_fuer_ende_Lin_interp=np.min(list(filter(lambda n:n>=x0, x_sp)))
            x_und_y_gezippt=tuple(zip(x_sp,list(y_sp)))
            #print(list(x_und_y_gezippt))
            x_und_y_gedict=dict(list(x_und_y_gezippt))
            y_wert_1=x_und_y_gedict[x_variabel_fuer_anfang_Lin_interp]
            y_wert_2=x_und_y_gedict[x_variabel_fuer_ende_Lin_interp]

            x_wert_1=x_variabel_fuer_anfang_Lin_interp
            x_wert_2=x_variabel_fuer_ende_Lin_interp    
            #print(x_wert_1,x_wert_2,y_wert_1,y_wert_2)
            a,b=makeline(np.array([x_wert_1,x_wert_2]), np.array([y_wert_1,y_wert_2]))
            y_for_temp=a*xvltemp+b
            y_for_temp=float("{:.3f}".format(y_for_temp))
    text3.set(y_for_temp)
        
          
s=liste_reg_and_interp[0]   
def drop_down_change(dp):
    global s
    s=dp
    click()
 
def click():
    plot1.clear()
    global x,y,N
    x=np.array([int(num1.get()),int(num2.get()),int(num3.get()),int(num4.get()),int(num5.get())])
    y=np.array([float(num6.get()),float(num7.get()),float(num8.get()),float(num9.get()),float(num10.get())])
    plot1.scatter(x,y,color='red')
    plot1.set_xlabel('x [Temperatur in °C]') 
    plot1.set_ylabel('y [Widerstand in \u03A9]') 
    x,y=[np.array(t) for t in sortinputandoutput(x,y)]
    if s==liste_reg_and_interp[0]:
        Regression(x,y)
    elif s==liste_reg_and_interp[1]:
        Lineare_interpolation(x,y)
    elif s==liste_reg_and_interp[2]:
        Spline(x,y)
    figure3.canvas.draw()
    figure3.canvas.flush_events()
  

text1=tk.StringVar()
text2=tk.StringVar()
text3=tk.StringVar()
#dropdown_menu=tk.StringVar(root)
#dropdown_menu.set(liste_reg_and_interp[0])

root.geometry("800x600")
root.title('Übung 2')  
Corona=tk.StringVar()
Corona.set(liste_reg_and_interp[0])
menu= tk.OptionMenu(root, Corona, *liste_reg_and_interp,command=drop_down_change)
menu.config(width=30, font=('Times New Roman', 9))
menu.grid(row=0, column=10)


    
result_label=tk.Label(root, text="Results : ")
result_label.grid(row=1, column=11)
result_labela=tk.Label(root, text="a= ")
result_labela.grid(row=2, column=12)
resulta1=tk.Label(root, text="", textvariable=text1)
resulta1.grid(row=2,column=13)
result_labelb=tk.Label(root, text="b= ")
result_labelb.grid(row=3, column=12)
resultb=tk.Label(root, text="", textvariable=text2)
resultb.grid(row=3,column=13)
result_labely=tk.Label(root, text="y= ")
result_labely.grid(row=4, column=12)
resulta2=tk.Label(root, text="", textvariable=text1)
resulta2.grid(row=4,column=13)
result_labelx=tk.Label(root, text="x + ")
result_labelx.grid(row=4, column=14)
resulta3=tk.Label(root, text="", textvariable=text2)
resulta3.grid(row=4,column=15)
inputValuesTkx = tk.Label(root, text="Input values 1 (x) ")
inputValuesTkx.grid(row=0, column=0)
inputValuesTky = tk.Label(root, text="Input values 2 (y) ")
inputValuesTky.grid(row=6, column=0)

num1 = tk.Entry(root,justify='center')
num1.grid(row=1, column=0,pady=4) 
num1.insert(tk.END, '1') 
num2 = tk.Entry(root,justify='center')
num2.grid(row=2, column=0,pady=4)
num2.insert(tk.END, '2')   
num3 = tk.Entry(root,justify='center')
num3.grid(row=3, column=0,pady=4)  
num3.insert(tk.END, '3') 
num4 = tk.Entry(root,justify='center')
num4.grid(row=4, column=0,pady=4) 
num4.insert(tk.END, '4') 
num5 = tk.Entry(root,justify='center')
num5.grid(row=5, column=0,pady=4)  
num5.insert(tk.END, '5') 
num6 = tk.Entry(root,justify='center')
num6.grid(row=7, column=0)  
num6.insert(tk.END, str(random.randrange(0, 20))) 
num7 = tk.Entry(root,justify='center')
num7.grid(row=8, column=0)  
num7.insert(tk.END, str(random.randrange(0, 20))) 
num8 = tk.Entry(root,justify='center')
num8.grid(row=9, column=0)  
num8.insert(tk.END, str(random.randrange(0, 20))) 
num9 = tk.Entry(root,justify='center')
num9.grid(row=10, column=0) 
num9.insert(tk.END, str(random.randrange(0, 20))) 
num10 = tk.Entry(root,justify='center')
num10.grid(row=11, column=0)
num10.insert(tk.END, str(random.randrange(0, 100))) 

button= tk.Button(root, text="Calculate", command=lambda:[click()])
button.grid(row=12, column=0)  


emp=tk.Label(root, text="Temperature in °C ").grid(row=13, column=0)

num11 = tk.Entry(root,justify='center')
num11.grid(row=14, column=0)
num11.insert(tk.END, '17') 
button2 = tk.Button(root,text="Calculate Resistance",command=res)
button2.grid(row=15, column=0)

result_labely2=tk.Label(root, text="y= ")
result_labely2.grid(row=16, column=0)
resulta2a=tk.Label(root, text="", textvariable=text3)
resulta2a.grid(row=17,column=0)
result_labely3=tk.Label(root, text="\u03A9")
result_labely3.grid(row=17, column=1)
  
root.mainloop()
