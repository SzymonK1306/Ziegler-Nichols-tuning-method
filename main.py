from tkinter import *                   # lib for GUI
from matplotlib import pyplot as plt    # lib for plots
import numpy as np                      # lib for mathematical functions

# creation the window
window = Tk()
window.geometry("1000x600")
window.title("Ziegler–Nichols tuning method")

# window icon
icon = PhotoImage(file='images/pid.png')
window.iconphoto(True, icon)

# radio buttons
var = IntVar()
Radiobutton(window, text="Square wave", variable=var, value=0,).grid(row=0, column=0)
Radiobutton(window, text="Heaviside step function", variable=var, value=1,).grid(row=0, column=1)
Radiobutton(window, text="Sine function", variable=var, value=2,).grid(row=0, column=2)

# input fields
Label(window, text="Amplitude:").grid(row=1, column=0)
amplitude = Entry(window, width=10).grid(row=1, column=1)
Label(window, text="Frequency:").grid(row=2, column=0)
frequency = Entry(window, width=10).grid(row=2, column=1)

window.mainloop()
