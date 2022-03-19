from tkinter import *

window = Tk()
window.geometry("1000x600")
window.title("Ziegler–Nichols tuning method")

icon = PhotoImage(file='images/pid.png')
window.iconphoto(True, icon)

window.mainloop()