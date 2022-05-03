from tkinter import *                   # lib for GUI
from PIL import ImageTk, Image
from matplotlib import pyplot as plt    # lib for plots
import numpy as np                      # lib for mathematical functions


# multiply matrices
def multiply_matrices(mat1, mat2):
        if len(mat1[0])!=len(mat2):     # checking matrix dimensions
                print("Wrong matrices")
        else:
                result = [[0 for i in range(len(mat2[0]))] for j in range(len(mat1))]   # create empty matrix of result

                for i in range(len(mat1)):      # rows of matrix 1
                        for j in range(len(mat2[0])):   # columns of matrix 2
                                for k in range(len(mat2)):      # iteration through rows and columns
                                        result[i][j] += mat1[i][k] * mat2[k][j]
                return result


# GUI

# creation the window
window = Tk()
window.geometry("900x600")
window.title("Ziegler–Nichols tuning method")

# Frames
image_frame = Frame(window)  # frame for image
image_frame.pack()

signal_title_frame = Frame(window)  # frame for the text on the signal choice
signal_title_frame.pack()

signal_frame = Frame(window)    # frame for signals to choose
signal_frame.pack()

parameters_title_frame = Frame(window)  # frame for the text on the parameters choice
parameters_title_frame.pack()

parameters_frame = Frame(window)        # frame for parameters
parameters_frame.pack()

# window icon
icon = PhotoImage(file='images/pid.png')
window.iconphoto(True, icon)

# photos
schematic = ImageTk.PhotoImage(Image.open("images/schematic.png"))
schematic_label = Label(image_frame, image=schematic)
schematic_label.pack()

# radio buttons
Label(signal_title_frame, text="Choose input signal:", font=("Arial", 15)).pack()
var = IntVar()
Radiobutton(signal_frame, text="Square wave", variable=var, value=0,).grid(row=0, column=1)
Radiobutton(signal_frame, text="Heaviside step function", variable=var, value=1,).grid(row=0, column=2)
Radiobutton(signal_frame, text="Sine function", variable=var, value=2,).grid(row=0, column=3)

# input fields
Label(parameters_title_frame, text="Choose parameters:", font=("Arial", 15)).pack()
# Amplitude
Label(parameters_frame, text="Amplitude:").grid(row=1, column=1)
amplitude = Entry(parameters_frame, width=10)
amplitude.insert(END, "1")      # default value
amplitude.grid(row=2, column=1, padx=10)
# Frequency
Label(parameters_frame, text="Frequency:").grid(row=1, column=2)
frequency = Entry(parameters_frame, width=10)
frequency.insert(END, "1")      # default value
frequency.grid(row=2, column=2, padx=10)
# a parameter
Label(parameters_frame, text="'a' parameter:").grid(row=1, column=3)
a_parameter = Entry(parameters_frame, width=10)
a_parameter.insert(END, "1")    # default value
a_parameter.grid(row=2, column=3, padx=10)
# gain 'k'
Label(parameters_frame, text="gain 'k':").grid(row=1, column=4)
gain_k = Entry(parameters_frame, width=10)
gain_k.insert(END, "1")         # default value
gain_k.grid(row=2, column=4, padx=10)
# Integral time
Label(parameters_frame, text="Integral time 'T':").grid(row=1, column=5)
integral_time = Entry(parameters_frame, width=10)
integral_time.insert(END, "1")    # default value
integral_time.grid(row=2, column=5, padx=10)

# MATHEMATICAL MODEL
a = float(a_parameter.get())
k = float(gain_k.get())
T = float(integral_time.get())

k_max = 2*a*a*a
T_osc = 2*3.14/a

# Ziegler-Nichols PI parameters
k_ZN = 0.45*k_max
T_ZN = 0.85*T_osc

numerator_ZN = [0, 0, 0, k_ZN*T_ZN, k_ZN]
denominator_ZN = [1, 2*a, a*a, k_ZN, k_ZN/T_ZN]

A_ZN = [[0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [-k_ZN/T_ZN, -k_ZN, -a*a, -2*a]]
B_ZN = [[0],
        [0],
        [0],
        [1]]
C_ZN = [[k_ZN, k_ZN*T_ZN, 0, 0]]

m = multiply_matrices(C_ZN, B_ZN)
print(m)

window.mainloop()
