import sys, getopt
import numpy as np
import control
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as Tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# import svg.path
import control.matlab
import yaml


try:
    opts, args = getopt.getopt(sys.argv[1:], "r", ["render"])
except getopt.GetoptError:
    print("Invalid param")
    sys.exit(2)
for opt, arg in opts:
    if opt == "-r":
        #!pip install svg.path
        #!pip install latextools
        #!pip install drawSvg
        import latextools

        latex_eq = latextools.render_snippet(
            r"""
\begin{minipage}[0pt]{180pt}
Sei $\omega_s$ die Eigenfrequenz und $\zeta$ die Dämpfungsgrad, eine 2te Ordnung LTI Übertragungsfunktion sieht so aus
$$H(s)=\frac{\omega_s^2}{s^2+s\zeta\omega_s+\omega_s^2}$$
mit $\cos(\phi)=\zeta$ für $-1<\zeta <1$ die Zeitfunktion kann man so schreiben:\\
\[H(t)=1-\frac{e^{-z\omega_s t}}{\sqrt{1-z^{2}}}\sin\left(\omega_s\sqrt{1-z^{2}}t+\phi\right)\]
%$t_r=\frac{\pi-\phi}{\omega_s\sin(\phi)}$
Und die Polen sind an der Stellen
\[s=-\zeta \omega_s\pm j\omega_s\sqrt{1-\zeta^2}\]
\end{minipage} 
""".strip(),
            pad=1,
        )
        latex_eq.as_svg().as_drawing().rasterize().savePng("eq1.png")
# https://www.desmos.com/calculator/jp1ejacymw

class LTIApp:
    def __init__(self):
        self.root = Tk.Tk()
        self.setup_ui()
        self.root.title("Übung 4 MT1")

    def setup_ui(self):
        plt.ioff()
        plt.close()

        # Create UI elements
        self.create_labels()
        self.create_bode_plot()
        self.create_pzmap()
        self.create_step_response()
        self.create_scales()
        self.create_step_info()
        self.create_image()

    def create_labels(self):
        Tk.Label(self.root, text="2te Ordnung LTI").grid(column=0, row=0)
        Tk.Label(self.root, text="zeta").grid(column=1, row=0)
        Tk.Label(self.root, text="Eigenfrequenz").grid(column=1, row=2)

    def create_image(self):
        canvas = Tk.Canvas(self.root)
        # https://www.electrical4u.com/time-response-of-second-order-control-system/
        self.photoimage = Tk.PhotoImage(master=canvas, file=__file__ + "/../eq1.png")
        canvas.create_image(160, 130, image=self.photoimage)
        canvas.grid(column=0, row=1, rowspan=10)


    def create_bode_plot(self):
        self.w_s = 1
        self.z = 1
        self.sys = control.tf([self.w_s ** 2], [1, self.w_s * self.z, self.w_s ** 2])

        plt.figure("Bode", figsize=(6, 5))
        control.bode_plot(self.sys)
        self.canvas2 = FigureCanvasTkAgg(plt.gcf(), master=self.root)
        self.canvas2.get_tk_widget().grid(column=0, row=11, columnspan=1, rowspan=7, padx=0, pady=0)

        self.ani = animation.FuncAnimation(plt.gcf(), lambda a: None, [1], interval=100, blit=False)

    def create_pzmap(self):
        fig = plt.figure("pzmap", figsize=(6, 5))
        control.pzmap(self.sys)
        self.canvas3 = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas3.get_tk_widget().grid(column=1, row=11, columnspan=1, rowspan=7, padx=0, pady=0)

        self.ani2 = animation.FuncAnimation(plt.gcf(), lambda a: None, [1], interval=100, blit=False)

    def create_step_response(self):
        fig2 = plt.figure("step_response", figsize=(5, 5))
        self.canvas4 = FigureCanvasTkAgg(fig2, master=self.root)
        self.canvas4.get_tk_widget().grid(column=2, row=11, columnspan=1, rowspan=7, padx=0, pady=0)

        self.ani3 = animation.FuncAnimation(plt.gcf(), lambda a: None, [1], interval=100, blit=False)

        t, y = control.step_response(self.sys)
        plt.title("Sprungantwort")
        plt.plot(t, y)
        plt.grid()

    def create_scales(self):
        self.scale = Tk.Scale(
            self.root,
            orient=Tk.HORIZONTAL,
            length=300,
            from_=-5,
            to=5,
            resolution=0.01,
            command=self.on_zeta_change,
        )
        self.scale.grid(column=1, row=1, sticky="ew")
        self.scale2 = Tk.Scale(
            self.root,
            orient=Tk.HORIZONTAL,
            length=300,
            from_=0,
            to=100,
            command=self.on_frequenz_change,
        )
        self.scale2.grid(column=1, row=3, sticky="ew")

    def create_step_info(self):
        self.textlab = Tk.Label(
            self.root,
            text=yaml.dump({k: float(v) for k, v in control.matlab.stepinfo(self.sys).items()})
        )
        self.textlab.grid(column=2, row=0, rowspan=7)

    def on_zeta_change(self, value):
        self.z = float(value)
        self.on_var_change()

    def on_frequenz_change(self, value):
        self.w_s = int(value)
        self.on_var_change()

    def on_var_change(self):
        self.sys = control.tf([self.w_s ** 2], [1, self.w_s * self.z, self.w_s ** 2])

        # Update Bode plot
        plt.figure("Bode")
        plt.clf()
        control.bode_plot(self.sys)

        # Update pzmap
        plt.figure("pzmap")
        plt.clf()
        control.pzmap(self.sys)

        # Update step response
        plt.figure("step_response")
        plt.cla()
        t, y = control.step_response(self.sys, T=np.linspace(0, 10, num=1000))
        plt.plot(t, y)
        plt.title("Sprungantwort")
        plt.grid()

        try:
            step_info = control.matlab.stepinfo(self.sys)
            step_info_text = yaml.dump({k: float(v) for k, v in step_info.items()})
        except IndexError:
            step_info_text = "Error calculating step info."

        self.textlab.config(text=step_info_text)

    def run(self):
        self.root.mainloop()
        plt.close("all")


if __name__ == "__main__":
    app = LTIApp()
    app.run()
