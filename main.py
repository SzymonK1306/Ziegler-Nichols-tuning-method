from tkinter import *  # lib for GUI
from PIL import ImageTk, Image
from tkinter import messagebox
from matplotlib import pyplot as plt  # lib for plots
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import numpy as np  # lib for mathematical functions


# ----- Functions -----

# Matrix multiplication
def multiply_matrices(mat1, mat2):
    if len(mat1[0]) != len(mat2):  # checking matrix dimensions
        print("Wrong matrices")
    else:
        result = [[0 for i in range(len(mat2[0]))] for j in range(len(mat1))]  # create empty matrix of result

        for i in range(len(mat1)):  # rows of matrix 1
            for j in range(len(mat2[0])):  # columns of matrix 2
                for k in range(len(mat2)):  # iteration through rows and columns
                    result[i][j] += mat1[i][k] * mat2[k][j]

        return result


# Matrix sum
def sum_matrices(mat1, mat2):
    if len(mat1[0]) != len(mat2[0]) or len(mat1) != len(mat2):  # checking matrix dimensions
        print("Wrong matrices")
    else:
        result = [[0 for i in range(len(mat1[0]))] for j in range(len(mat1))]  # create empty matrix of result

        for i in range(len(mat1)):  # rows
            for j in range(len(mat1[0])):  # columns
                result[i][j] = mat1[i][j] + mat2[i][j]

        return result


# Matrix and scalar multiplication
def multiply_matrix_scalar(mat, x):
    result = [[0 for i in range(len(mat[0]))] for j in range(len(mat))]  # create empty matrix of result

    for i in range(len(mat)):  # rows
        for j in range(len(mat[0])):  # columns
            result[i][j] = mat[i][j] * x

    return result


# Choosing signal using radio buttons
def choose_signal(value):
    global signal

    if value == 0:
        signal = "Square"
    elif value == 1:
        signal = "Heaviside"
    elif value == 2:
        signal = "Sine"


# Plots function
def plotting(x, y, z, time):
    figure_1 = Figure(figsize=(4, 3), dpi=100)
    plot_1 = figure_1.add_subplot(111)
    plot_1.plot(time, x, color='C0')
    plot_1.plot(time, y, color='C1')

    chart = FigureCanvasTkAgg(figure_1, master=plots_frame)
    chart.get_tk_widget().grid(pady=6, row=0, column=0)

    figure_2 = Figure(figsize=(4, 3), dpi=100)
    plot_2 = figure_2.add_subplot(111)
    plot_2.plot(time, z, color='C2')

    chart = FigureCanvasTkAgg(figure_2, master=plots_frame)
    chart.get_tk_widget().grid(pady=6, row=0, column=1)

    # toolbar = NavigationToolbar2Tk(chart, plots_frame)
    # toolbar.get_tk_widget().pack()
    # toolbar.update()


# Simulation function
def simulation(zn_method):
    # Simulation parameters
    t_stop = float(simulation_time.get())
    t_sample = float(integration_step.get())
    t = np.arange(0, t_stop, t_sample, dtype=np.float64)
    stability = True

    N = int(np.ceil(t_stop / t_sample))

    # Model parameters
    a = float(a_parameter.get())
    k = float(gain_k.get())
    T = float(integral_time.get())

    # PD parameters using Z-N method
    if zn_method:
        k_max = 2 * (a ** 3)
        T_osc = 2 * np.pi / a
        k = 0.45 * k_max
        T = 0.85 * T_osc
    elif (2 * a ** 3) < k or (2 * k * a ** 3 - k ** 2 - (2 * a * k)/T) < 0:    # stability test
        stability = False

    # Input signals parameters
    amp = float(amplitude.get())
    freq = float(frequency.get())
    duty = 0.5  # ! Need to add to GUI

    # State-space model
    numerator = [0, 0, 0, k, k / T]
    denominator = [1, 2 * a, a ** 2, k, k / T]

    A = [[0, 1, 0, 0],
         [0, 0, 1, 0],
         [0, 0, 0, 1],
         [-k / T, -k, -(a ** 2), -2 * a]]

    B = [[0],
         [0],
         [0],
         [1]]

    C = [[k / T, k, 0, 0]]

    # Input signals
    u = [0 for i in range(N)]  # Input signal initialization

    if signal == "Heaviside":
        u = [amp for i in range(N)]
    elif signal == "Square":
        u = [amp * np.sign(np.sin(2 * np.pi * freq * i * t_sample)) for i in range(N)]  # ! Need to edit
    elif signal == "Sine":
        u = [amp * np.sin(2 * np.pi * freq * i * t_sample) for i in range(N)]

    # Simulation
    if stability:
        y = [0 for i in range(N)]  # Output signal initialization
        e = [0 for i in range(N)]  # Error signal initialization

        xi_1 = [[0],  # Zero initial conditions
            [0],
            [0],
            [0]]

        for i in range(N):
            Ax = multiply_matrices(A, xi_1)
            Bu = multiply_matrix_scalar(B, u[i])
            Cx = multiply_matrices(C, xi_1)

            xi_1 = sum_matrices(xi_1, multiply_matrix_scalar(sum_matrices(Ax, Bu), t_sample))

            y[i] = Cx[0][0]
            e[i] = u[i] - y[i]

        # ----- Plotting -----

        plotting(u, y, e, t)

    else:
        messagebox.showinfo("Stability", "The control system is unstable, change parameters of PI regulator")


# ----- Global Variables -----
signal = "Square"


# ----- GUI -----

# Creating a window
window = Tk()
window.geometry("900x650")
window.title("Ziegler–Nichols tuning method")

# Creating frames
image_frame = Frame(window)  # frame for image
image_frame.pack()

signal_title_frame = Frame(window)  # frame for text when selecting a signal
signal_title_frame.pack()

signal_frame = Frame(window)  # frame for signals to choose
signal_frame.pack()

parameters_title_frame = Frame(window)  # frame for text when selecting parameters
parameters_title_frame.pack()

parameters_frame = Frame(window)  # frame for parameters
parameters_frame.pack()

buttons_frame = Frame(window)  # frame for buttons
buttons_frame.pack()

plots_frame = Frame(window)  # frame for plots
plots_frame.pack()

# Window icon
icon = PhotoImage(file='images/pid.png')
window.iconphoto(True, icon)

# Images
schematic = ImageTk.PhotoImage(Image.open("images/schematic.png"))
schematic_label = Label(image_frame, image=schematic)
schematic_label.pack()

# Radio buttons
var = IntVar()
Label(signal_title_frame, text="Choose input signal:", font=("Arial", 15)).pack()
Radiobutton(signal_frame, text="Square wave", variable=var, value=0, command=lambda: choose_signal(0)).grid(row=0,
                                                                                                            column=1)
Radiobutton(signal_frame, text="Heaviside step function", variable=var, value=1, command=lambda: choose_signal(1)).grid(
    row=0, column=2)
Radiobutton(signal_frame, text="Sine function", variable=var, value=2, command=lambda: choose_signal(2)).grid(row=0,
                                                                                                              column=3)

# Input fields
Label(parameters_title_frame, text="Choose parameters:", font=("Arial", 15)).pack()

# amplitude
Label(parameters_frame, text="Amplitude:").grid(row=1, column=1)
amplitude = Entry(parameters_frame, width=10)
amplitude.insert(END, "1")  # default value
amplitude.grid(row=2, column=1, padx=10)

# frequency
Label(parameters_frame, text="Frequency:").grid(row=1, column=2)
frequency = Entry(parameters_frame, width=10)
frequency.insert(END, "1")  # default value
frequency.grid(row=2, column=2, padx=10)

# 'a' parameter
Label(parameters_frame, text="'a' parameter:").grid(row=1, column=3)
a_parameter = Entry(parameters_frame, width=10)
a_parameter.insert(END, "1")  # default value
a_parameter.grid(row=2, column=3, padx=10)

# gain 'k'
Label(parameters_frame, text="gain 'k':").grid(row=1, column=4)
gain_k = Entry(parameters_frame, width=10)
gain_k.insert(END, "1")  # default value
gain_k.grid(row=2, column=4, padx=10)

# integral time 'T'
Label(parameters_frame, text="Integral time 'T':").grid(row=1, column=5)
integral_time = Entry(parameters_frame, width=10)
integral_time.insert(END, "1")  # default value
integral_time.grid(row=2, column=5, padx=10)

# integration step
Label(parameters_frame, text="Integration step:").grid(row=1, column=6)
integration_step = Entry(parameters_frame, width=10)
integration_step.insert(END, "0.01")  # default value
integration_step.grid(row=2, column=6, padx=10)

# simulation time
Label(parameters_frame, text="Simulation time:").grid(row=1, column=7)
simulation_time = Entry(parameters_frame, width=10)
simulation_time.insert(END, "100")  # default value
simulation_time.grid(row=2, column=7, padx=10)

# start simulation

Button(buttons_frame, text="Simulation with your parameters", pady=5, padx=10, width=50,
       command=lambda: simulation(False)).grid(row=0, column=0)
Label(buttons_frame, text="      ").grid(row=0, column=1)
Button(buttons_frame, text="Simulation with Ziegler-Nichols parameters", pady=5, padx=10, width=50,
       command=lambda: simulation(True)).grid(row=0, column=2)

window.mainloop()
