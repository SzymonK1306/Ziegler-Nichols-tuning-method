from tkinter import *  # lib for GUI
from PIL import ImageTk, Image
from tkinter import messagebox
from matplotlib import pyplot as plt  # lib for plots
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
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
    Label(plots_frame, text="Input, output and error signals", font=("Arial", 13)).grid(row=0, column=0)
    fig = Figure()
    fig, axes = plt.subplots(2)

    axes[0].plot(time, x, 'r', label="u(t)")
    axes[0].plot(time, y, 'g', label="y(t)")
    axes[1].plot(time, z, color='b', label="e(t)")

    axes[0].grid(visible=True)
    axes[0].legend(loc='upper right')
    axes[1].grid(visible=True)
    axes[1].legend(loc='upper right')
    axes[1].set_xlabel('Time')

    fig.tight_layout()

    chart = FigureCanvasTkAgg(fig, master=plots_frame)
    chart.get_tk_widget().grid(row=1, column=0)

    toolbar = NavigationToolbar2Tk(chart, plots_toolbar_frame)
    toolbar.update()


# Simulation function
def simulation(zn_method):
    # Simulation parameters
    t_stop = float(simulation_time.get())
    t_sample = float(integration_step.get())
    t = np.arange(0, t_stop, t_sample, dtype=np.float64)

    N = int(np.ceil(t_stop / t_sample))
    stability = True

    # System parameters
    a = float(a_parameter.get())
    k = float(gain_k.get())
    T = float(integral_time.get())

    # PI parameters using Z-N method
    if zn_method:
        k_max = 2 * (a ** 3)
        T_osc = 2 * np.pi / a
        k = 0.45 * k_max
        T = 0.85 * T_osc
    elif (2 * a ** 3) < k or (2 * k * a ** 3 - k ** 2 - (2 * a * k) / T) < 0:  # stability test
        stability = False

    # Input signals parameters
    amp = float(amplitude.get())
    freq = float(frequency.get())

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

            xi = sum_matrices(Ax, Bu)
            xi = multiply_matrix_scalar(xi, t_sample)
            xi = sum_matrices(xi_1, xi)
            xi_1 = xi

            y[i] = Cx[0][0]
            e[i] = u[i] - y[i]

        # ----- Plotting -----
        for widget in plots_toolbar_frame.winfo_children():
            widget.destroy()

        # for widget in plots_frame.winfo_children():
        #     widget.destroy()

        plotting(u, y, e, t)

    else:
        messagebox.showinfo("Stability", "The control system is unstable, change parameters of PI regulator")


# ----- GUI -----

# Creating a window
window = Tk()
window.geometry("1100x550")
window.title("Ziegler–Nichols tuning method")

# Creating frames
left_frame = Frame(window)  # left side frame
left_frame.pack(side=LEFT, fill=BOTH, expand=True)

right_frame = Frame(window)  # right side frame
right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

plots_frame = Frame(right_frame)  # frame for plots
plots_frame.pack()

plots_toolbar_frame = Frame(right_frame)  # frame for toolbar (plots)
plots_toolbar_frame.pack()

img_frame = Frame(left_frame)  # frame for image
img_frame.pack()

sim_param_frame = Frame(left_frame)  # frame for simulation parameters
sim_param_frame.pack()

syst_param_frame = Frame(left_frame)  # frame for system parameters
syst_param_frame.pack()

input_signal_frame = Frame(left_frame)  # frame for input signals
input_signal_frame.pack()

input_param_frame = Frame(left_frame)  # frame for input signal parameters
input_param_frame.pack()

start_sim_buttons_frame = Frame(left_frame)  # frame for start simulation buttons
start_sim_buttons_frame.pack()

# Window icon
icon = PhotoImage(file='images/pid.png')
window.iconphoto(True, icon)

# Images
schematic = ImageTk.PhotoImage(Image.open("images/schematic.png").resize((350, 82)))
Label(img_frame, image=schematic).grid(row=0, column=0, columnspan=2)

# Simulation parameters
Label(sim_param_frame, text="Enter simulation parameters", font=("Arial", 13)).grid(row=1, column=0, columnspan=2)

# simulation time
Label(sim_param_frame, text="Simulation time: ").grid(row=2, column=0)
simulation_time = Entry(sim_param_frame, width=10)
simulation_time.insert(END, "100")  # default value
simulation_time.grid(row=2, column=1, sticky=W)

# integration step
Label(sim_param_frame, text="Integration step: ").grid(row=3, column=0)
integration_step = Entry(sim_param_frame, width=10)
integration_step.insert(END, "0.01")  # default value
integration_step.grid(row=3, column=1, sticky=W)

# System parameters
Label(syst_param_frame, text="Enter system parameters", font=("Arial", 13)).grid(row=4, column=0, columnspan=2)

# parameter 'a'
Label(syst_param_frame, text="Parameter 'a': ").grid(row=5, column=0, sticky=W)
a_parameter = Entry(syst_param_frame, width=10)
a_parameter.insert(END, "2")  # default value
a_parameter.grid(row=5, column=1, sticky=W)

# gain 'k'
Label(syst_param_frame, text="Gain 'k': ").grid(row=6, column=0, sticky=W)
gain_k = Entry(syst_param_frame, width=10)
gain_k.insert(END, "10")  # default value
gain_k.grid(row=6, column=1, sticky=W)

# integral time 'T'
Label(syst_param_frame, text="Integral time 'T': ").grid(row=7, column=0, sticky=W)
integral_time = Entry(syst_param_frame, width=10)
integral_time.insert(END, "4")  # default value
integral_time.grid(row=7, column=1, sticky=W)

# Input signals
var = IntVar()
signal = "Square"  # default value
Label(input_signal_frame, text="Choose input signal", font=("Arial", 13)).grid(row=8, column=0)
Radiobutton(input_signal_frame, text="Square wave", variable=var, value=0,
            command=lambda: choose_signal(0)).grid(row=9, column=0, sticky=W)
Radiobutton(input_signal_frame, text="Heaviside step function", variable=var, value=1,
            command=lambda: choose_signal(1)).grid(row=10, column=0, sticky=W)
Radiobutton(input_signal_frame, text="Sine function", variable=var, value=2,
            command=lambda: choose_signal(2)).grid(row=11, column=0, sticky=W)

# Input signal parameters
Label(input_param_frame, text="Enter input parameters", font=("Arial", 13)).grid(row=12, column=0, columnspan=2)

# amplitude
Label(input_param_frame, text="Amplitude: ").grid(row=13, column=0, sticky=W)
amplitude = Entry(input_param_frame, width=10)
amplitude.insert(END, "1")  # default value
amplitude.grid(row=13, column=1, sticky=W)

# frequency
Label(input_param_frame, text="Frequency: ").grid(row=14, column=0, sticky=W)
frequency = Entry(input_param_frame, width=10)
frequency.insert(END, "0.1")  # default value
frequency.grid(row=14, column=1, sticky=W)

# Start simulation
Label(input_param_frame, text="Simulate with", font=("Arial", 13)).grid(row=15, column=0, columnspan=2)
Button(start_sim_buttons_frame, text="Your parameters", pady=4, width=20,
       command=lambda: simulation(False)).grid(row=16, column=0, sticky=W)
Button(start_sim_buttons_frame, text="Ziegler-Nichols parameters", pady=4, width=20,
       command=lambda: simulation(True)).grid(row=16, column=1, sticky=E)


window.mainloop()
