# -*- coding: utf-8 -*-
"""
Skript zur Uebung 2 - Regression und Interpolation
Grundlagen der elektronischen Messtechnik

FG Mess- und Diagnosetechnik
TU Berlin

@author: dthomane
"""
import numpy as np
from scipy import stats as st
from scipy import interpolate  as ip
from matplotlib import pyplot as plt


# Modes
# 1: Messdaten
# 2: Lineare Regression
# 3: Lineare Interpolation
# 4: Kubische spline Interpolation
Mode = [1, 2, 3, 4]


# Messdaten
x = np.array([0, 20, 40, 60, 80])
y = np.array([1.7, 1.1, 0.75, 0.5, 0.4])


# PLOTS

# Messdaten plotten
if 1 in Mode:
    plt.plot(x, y, 'bo', label='Messdaten')

# Lineare Regression plotten
if 2 in Mode:
    lr = st.linregress(x, y)
    
    x_lr = np.array([x.min(), x.max()])
    y_lr = lr.slope*x_lr + lr.intercept
    
    plt.plot(x_lr, y_lr, '-', label='Lineare Regression')

# Lineare Interpolation plotten
if 3 in Mode:
    plt.plot(x, y, '-', label='Lineare Interpolation')

# Kubische Spline Interpolation plotten
if 4 in Mode:
    spl = ip.CubicSpline(x, y)
    
    x_sp = np.linspace(x.min(), x.max(), 1000)
    y_sp = spl(x_sp)
    
    plt.plot(x_sp, y_sp, '-', label='Kubische spline Interpolierende')


plt.legend()
plt.show()