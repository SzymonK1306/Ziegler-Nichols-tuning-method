# 🦾 Tuning the PI Controller Using the Ziegler-Nichols Method

> ☣ **Warning:** This project was created during our studies for educational purposes only. It may contain non-optimal or outdated solutions.

### 📃 About
Our project allows you to **model** and **simulate** a given automatic control system (diagram in the pictures below). You can define all the parameters **_a, k_** and **_T_** in the menu. Then program **plots** the current output **y(t)** and error **e(t)** values of the system, checks **the stability** of the closed system and gives the result.

The project was implemented with *Python 3.9 (PyCharm 2021.3.2)* using the following libraries: **tkinter** and **PIL** (for GUI), **matplotlib** (for plots) and **NumPy** (for performing some mathematical functions).

### 📷 Screenshots
**Simulations with calculated Ziegler-Nichols parameters:**
- ```a = 4``` | Heaviside step function
<img src="/_readmeImg/1-step.png?raw=true 'Simulation I'" width="600">

- ```a = 4``` | Square wave
<img src="/_readmeImg/1-square.png?raw=true 'Simulation II'" width="600">

- ```a = 4``` | Sine function
<img src="/_readmeImg/1-sine.png?raw=true 'Simulation III'" width="600">

**Simulations with own parameters:**
- ```a = 4, k = 13, T = 4``` | Heaviside step function
<img src="/_readmeImg/2-step.png?raw=true 'Simulation I'" width="600">

- ```a = 4, k = 13, T = 4``` | Square wave
<img src="/_readmeImg/2-square.png?raw=true 'Simulation II'" width="600">

- ```a = 4, k = 13, T = 4``` | Sine function
<img src="/_readmeImg/2-sine.png?raw=true 'Simulation III'" width="600">


### 💪 Authors
- Szymon Kryzel
- Tomash Mikulevich
