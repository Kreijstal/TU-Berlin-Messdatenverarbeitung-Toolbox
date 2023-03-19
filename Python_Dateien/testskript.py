import numpy as np

# Ubung_01.root.mainloop()
i = 0


def test1():
    onesecond = 10000
    import Ubung_01 as ue1

    gui = ue1.GUI()

    def wait(ii):
        i = 0
        while i < onesecond * ii:
            i = i + 1
            gui.root.dooneevent(ue1.Tk._tkinter.ALL_EVENTS | ue1.Tk._tkinter.DONT_WAIT)

    wait(1)
    gui.var1.set(1)
    wait(1)
    gui.anzahlVonBins.set(30)
    gui.anzahlSamples.set(6000)
    wait(1)
    gui.freiheitgradVonStudenTverteilung.set(50)
    wait(1)
    gui.root.destroy()


def test2():
    onesecond = 3000
    import Ubung_01

    i = 0
    import Übung_02 as ue2

    app = ue2.RegressionApp()

    def show(ii):
        app.plotAktualizieren()
        app.res()
        i = 0
        while i < onesecond * ii:
            i = i + 1
            app.root.dooneevent(ue2.tk._tkinter.ALL_EVENTS | ue2.tk._tkinter.DONT_WAIT)

    while i < onesecond * 2:
        i = i + 1
        app.root.update_idletasks()
        app.root.update()
    app.dropDownVariable.set(app.liste_reg_and_interp[0])
    # ue2.text3.set("30")
    # ue2.number_array[10].insert(ue2.tk.END,"0")

    show(2)
    x = np.array([0, 20, 40, 60, 80])
    y = np.array([1.7, 1.1, 0.75, 0.5, 0.4])

    def insert(i, x):
        app.number_entries[i].delete(0, "end")
        app.number_entries[i].insert(ue2.tk.END, str(x))

    [insert(i, x) for i, x in enumerate(list(np.concatenate([x, y])))]
    show(4)
    app.dropDownVariable.set(app.liste_reg_and_interp[1])
    app.drop_down_change(app.liste_reg_and_interp[1])
    show(4)
    app.dropDownVariable.set(app.liste_reg_and_interp[2])
    app.drop_down_change(app.liste_reg_and_interp[2])
    app.plotAktualizieren()
    show(4)
    print("Ubung 2 läuft")
    app.root.destroy()
    # ue2.button.


def test3():
    onesecond = 30
    import Übung_03 as ue3

    ue3TKClass = ue3.TKWindow("Ubung 3 Wird jetzt getestet!")

    def wait(ii):
        i = 0
        while i < onesecond * ii:
            i = i + 1
            ue3TKClass.dooneevent(
                ue3.tk._tkinter.ALL_EVENTS | ue3.tk._tkinter.DONT_WAIT
            )

    def slider3test():
        a = ue3TKClass.widget_params["linearity_scale"]["from"]
        b = ue3TKClass.widget_params["linearity_scale"]["to"]
        i = a
        while i < b:
            ue3TKClass.scales["linearity"].set(i)
            i += (b - a) / 10
            wait(1)

    def slider2test():
        a = ue3TKClass.widget_params["amplification_scale"]["from"]
        b = ue3TKClass.widget_params["amplification_scale"]["to"]
        i = a
        while i < b:
            slider3test()
            ue3TKClass.scales["amplification"].set(i)
            i += (b - a) / 10
            wait(1)

    def slider1test():
        a = ue3TKClass.widget_params["offset_scale"]["from"]
        b = ue3TKClass.widget_params["offset_scale"]["to"]
        i = a
        while i < b:
            slider2test()
            ue3TKClass.scales["offset"].set(i)
            i += (b - a) / 10
            wait(1)

    def button1test():
        slider1test()
        ue3TKClass.widget_params["linearity_checkbox"]["variable"].set(True)
        wait(1)
        ue3TKClass.widget_params["linearity_checkbox"]["variable"].set(False)
        wait(1)

    def button2test():
        button1test()
        ue3TKClass.widget_params["amplification_checkbox"]["variable"].set(True)
        wait(1)
        button1test()
        ue3TKClass.widget_params["amplification_checkbox"]["variable"].set(False)
        wait(1)

    def button3test():
        button2test()
        ue3TKClass.widget_params["offset_checkbox"]["variable"].set(True)
        wait(1)
        button2test()
        ue3TKClass.widget_params["offset_checkbox"]["variable"].set(False)
        wait(1)

    button3test()
    wait(2)
    ue3TKClass.destroy()


def test4():
    onesecond = 5
    import Ubung_04 as ue4

    def wait(ii):
        i = 0
        while i < onesecond * ii:
            i = i + 1
            ue4.root.dooneevent(ue4.Tk._tkinter.ALL_EVENTS | ue4.Tk._tkinter.DONT_WAIT)

    def slider2test():
        a = 0
        b = 100
        i2 = a
        while i2 <= b:
            ue4.scale2.set(i2)
            ue4.onfrequenzChange(i2)
            i2 += (b - a) / 10
            wait(1)

    def slider1test():
        a = -5
        b = 5
        i3 = a
        while i3 <= b:
            slider2test()
            ue4.scale.set(i3)
            ue4.onZetaChange(i3)
            i3 += (b - a) / 10
            wait(1)

    slider1test()
    wait(1)
    ue4.root.destroy()


def test5():
    import Ubung_05 as ue5

    onesecond = 30000

    def wait(ii):
        i = 0
        while i < onesecond * ii:
            i = i + 1
            ue5TKClass.update_idletasks()
            ue5TKClass.update()

    ue5TKClass = ue5.TKWindow("Ubung 5 Wird jetzt getestet!")

    def slider1test():
        for i in range(2, 9):
            ue5TKClass.bits_scale.set(i)
            ue5TKClass.animate(i)
            ue5TKClass.figure_canvas.draw()

            wait(1)

    slider1test()
    wait(1)
    ue5TKClass.destroy()


def test6():
    import Übung_06 as ue6

    onesecond = 100

    def wait(ii):
        i = 0
        while i < onesecond * ii:
            i = i + 1
            ue6TKClass.update_idletasks()
            ue6TKClass.update()
            ue6TKClass.animate(i * ue6TKClass.tx)
            ue6TKClass.figure_canvas.draw()

    ue6TKClass = ue6.TKWindow("Ubung 6 Wird jetzt getestet!")
    ue6TKClass.dictWidgets["frequency"].set(137)
    ue6TKClass.dictWidgets["amplitude"].set(13)
    # ue6TKClass.dictWidgets["dropdown"].set("sinus")
    ue6TKClass.onSelection("sinus")
    ue6TKClass.create_axes(4)
    wait(1)
    ue6TKClass.destroy()


def test7():
    import Übung_07 as ue7

    onesecond = 20

    def wait(ii):
        i = 0
        while i < onesecond * ii:
            i = i + 1
            ue7TKClass.update_idletasks()
            ue7TKClass.update()
            ue7TKClass.animate(i)
            ue7TKClass.figure_canvas.draw()

    ue7TKClass = ue7.TKWindow("Ubung 7 Wird jetzt getestet!")
    wait(1)
    ue7TKClass.widgets["entry_u0"]["self"].delete(0, ue7.tk.END)
    ue7TKClass.widgets["entry_u0"]["self"].insert(ue7.tk.END, "5")
    ue7TKClass.widgets["entry_z1"]["self"].delete(0, ue7.tk.END)
    ue7TKClass.widgets["entry_z1"]["self"].insert(ue7.tk.END, "4+j")
    ue7TKClass.widgets["entry_z2"]["self"].delete(0, ue7.tk.END)
    ue7TKClass.widgets["entry_z2"]["self"].insert(ue7.tk.END, "3+2j")
    ue7TKClass.widgets["entry_z3"]["self"].delete(0, ue7.tk.END)
    ue7TKClass.widgets["entry_z3"]["self"].insert(ue7.tk.END, "-4-5j")
    ue7TKClass.widgets["entry_z4"]["self"].delete(0, ue7.tk.END)
    ue7TKClass.widgets["entry_z4"]["self"].insert(ue7.tk.END, "-3")
    wait(1)


# test1()
test2()
# test3()
# test4()
# test5()
# test6()
# test7()


# mingw -c "./venv/bin/python Python_Dateien/testskript.py"
