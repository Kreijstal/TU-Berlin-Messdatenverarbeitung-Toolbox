# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 13:37:14 2022

@author: Boris
"""
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def test():
    N=5
    global a,b,x,y
    x=np.array([int(num1.get()),int(num2.get()),int(num3.get()),int(num4.get()),int(num5.get())])
    y=np.array([float(num6.get()),float(num7.get()),float(num8.get()),float(num9.get()),float(num10.get())])
    a_numerator=N*np.sum(x*y)-(np.sum(y)*np.sum(x))
    a_denominator=N*np.sum(x**2)-(np.sum(x))**2
    a=a_numerator/a_denominator
    a=float("{:.3f}".format(a))
    text1.set(a)
    b_numerator=np.sum(y)*np.sum(x**2)-np.sum(y*x)*np.sum(x)
    b_denominator=N*np.sum(x**2)-(np.sum(x))**2
    b=b_numerator/b_denominator
    b=float("{:.3f}".format(b))
    text2.set(b)

def plot():
   xvl = np.linspace(min(x), max(x), 100)
   yvl=a*xvl+b;
   figure3 = plt.Figure(figsize=(6,4))
   plot1 = figure3.add_subplot(111)
   plot1.scatter(x,y,color='red')
   plot1.plot(xvl,yvl,color='blue')
   scatter3 = FigureCanvasTkAgg(figure3, root) 
   scatter3.get_tk_widget().grid(row=6, column=3,columnspan = 100, rowspan = 24, padx = 0, pady = 0)
   plot1.legend(['Messdaten','Methode der kleinsten Quadrate'])
   plot1.set_xlabel('x [Temperatur in °C]') 
   plot1.set_ylabel('y [Widerstand in \u03A9]') 
   plot1.set_title('Methode der kleinsten Quadrate')

def res():
    xvltemp=int(num11.get())
    y_for_temp=a*xvltemp+b
    y_for_temp=float("{:.3f}".format(y_for_temp))
    text3.set(y_for_temp)
    
root= tk.Tk()
text1=tk.StringVar()
text2=tk.StringVar()
text3=tk.StringVar()

root.geometry("800x600")
root.title('Übung 2')  


values1 = tk.Label(root, text="Input values 1 (x) ").grid(row=0, column=0)
values2 = tk.Label(root, text="Input values 2 (y) ").grid(row=6, column=0)

result_label=tk.Label(root, text="Results : ").grid(row=1, column=2)
result_labela=tk.Label(root, text="a= ").grid(row=2, column=3)
resulta=tk.Label(root, text="", textvariable=text1).grid(row=2,column=4)

result_labelb=tk.Label(root, text="b= ").grid(row=3, column=3)
resultb=tk.Label(root, text="", textvariable=text2).grid(row=3,column=4)

result_labely=tk.Label(root, text="y= ").grid(row=4, column=3)
resulta=tk.Label(root, text="", textvariable=text1).grid(row=4,column=4)
result_labely=tk.Label(root, text="x + ").grid(row=4, column=5)
resulta=tk.Label(root, text="", textvariable=text2).grid(row=4,column=6)

num1 = tk.Entry(root,justify='center')
num1.grid(row=1, column=0,pady=4)  
num2 = tk.Entry(root,justify='center')
num2.grid(row=2, column=0,pady=4)  
num3 = tk.Entry(root,justify='center')
num3.grid(row=3, column=0,pady=4)  
num4 = tk.Entry(root,justify='center')
num4.grid(row=4, column=0,pady=4) 
num5 = tk.Entry(root,justify='center')
num5.grid(row=5, column=0,pady=4)  
num6 = tk.Entry(root,justify='center')
num6.grid(row=7, column=0)  
num7 = tk.Entry(root,justify='center')
num7.grid(row=8, column=0)  
num8 = tk.Entry(root,justify='center')
num8.grid(row=9, column=0)  
num9 = tk.Entry(root,justify='center')
num9.grid(row=10, column=0) 
num10 = tk.Entry(root,justify='center')
num10.grid(row=11, column=0)
#Leerer Plot
figure3 = plt.Figure(figsize=(6,4), dpi=100) 
scatter3 = FigureCanvasTkAgg(figure3, root) 
scatter3.get_tk_widget().grid(row=6, column=3,columnspan = 100, rowspan = 24, padx = 0, pady = 0)

button= tk.Button(root, text="Calculate", command=lambda:[test(),plot()])
button.grid(row=12, column=0)  


emp=tk.Label(root, text="Temperature in °C ").grid(row=13, column=0)

num11 = tk.Entry(root,justify='center')
num11.grid(row=14, column=0)

button2 = tk.Button(root,text="Calculate Resistance",command=res)
button2.grid(row=15, column=0)

result_labely=tk.Label(root, text="y= ").grid(row=16, column=0)
resulta=tk.Label(root, text="", textvariable=text3).grid(row=17,column=0)
result_labely2=tk.Label(root, text="\u03A9").grid(row=17, column=1)

root.mainloop()
