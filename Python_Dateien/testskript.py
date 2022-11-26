import numpy as np
onesecond=30000
#Ubung_01.root.mainloop()
i=0
def test1():
    import Ubung_01
    i=0
    while i<onesecond:
        i=i+1
        Ubung_01.root.update_idletasks()
        Ubung_01.root.update()

    Ubung_01.anzahlVonBins.set(30)
    i=0
    while i<onesecond*3:
        i=i+1
        Ubung_01.root.update_idletasks()
        Ubung_01.root.update()
    Ubung_01.var1.set(1)
    i=0
    while i<onesecond*2:
        i=i+1
        Ubung_01.root.update_idletasks()
        Ubung_01.root.update()
    Ubung_01.anzahlSamples.set(6000)
    Ubung_01.freiheitgradVonStudenTverteilung.set(50)
    i=0
    while i<onesecond*10:
        i=i+1
        Ubung_01.root.update_idletasks()
        Ubung_01.root.update()
    print("Ubung 1 läuft")
    Ubung_01.root.destroy()
#test1()
def test2():
    i=0
    import Übung_02 as ue2
    def show(ii):
        ue2.plotAktualizieren()
        ue2.res()
        i=0
        while i<onesecond*ii:
            i=i+1
            ue2.root.update_idletasks()
            ue2.root.update()
    while i<onesecond*2:
        i=i+1
        ue2.root.update_idletasks()
        ue2.root.update()
    ue2.dropDownVariable.set(ue2.liste_reg_and_interp[0])
    #ue2.text3.set("30")
    #ue2.number_array[10].insert(ue2.tk.END,"0")
    
    show(2)
    x=np.array([0, 20, 40, 60, 80])
    y=np.array([1.7, 1.1, 0.75, 0.5, 0.4])
    def insert(i,x):
        ue2.number_array[i].delete(0, 'end')
        ue2.number_array[i].insert(ue2.tk.END,str(x))

    [insert(i,x) for i,x in enumerate(list(np.concatenate([x,y])))]
    show(4)
    ue2.dropDownVariable.set(ue2.liste_reg_and_interp[1])
    ue2.drop_down_change(ue2.liste_reg_and_interp[1])
    show(4)
    ue2.dropDownVariable.set(ue2.liste_reg_and_interp[2])
    ue2.drop_down_change(ue2.liste_reg_and_interp[2])
    ue2.plotAktualizieren()
    show(4)
    print("Ubung 2 läuft")
    ue2.root.destroy()
    #ue2.button.
#test2()
def test3():
    onesecond=30000
    import Übung_03 as ue3
    fuckyou=ue3.TKWindow("Ubung 3 Wird jetzt getestet!")
    def wait(ii):
        i=0
        while i<onesecond*ii:
            i=i+1
            fuckyou.update_idletasks()
            fuckyou.update()
    def button1test():
        fuckyou.widget_params["linearity_checkbox"]["variable"].set(True)
        wait(1)
        fuckyou.widget_params["linearity_checkbox"]["variable"].set(False)
        wait(1)
    def button2test():
        button1test()
        fuckyou.widget_params["amplification_checkbox"]["variable"].set(True)
        wait(1)
        button1test()
        fuckyou.widget_params["amplification_checkbox"]["variable"].set(False)
        wait(1)
    def button3test():
        button2test()
        fuckyou.widget_params["offset_checkbox"]["variable"].set(True)
        wait(1)
        button2test()
        fuckyou.widget_params["offset_checkbox"]["variable"].set(False)
        wait(1)
    button3test()
    wait(2)

test3()
import Ubung_04
import Ubung_05
import Übung_06
import Übung_07