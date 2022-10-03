from tkinter import *
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

window = ttk.Window()
window.title("基于K-Means++的股票预测系统")
window.geometry(f"{int(window.winfo_screenwidth()/2)}x{int(window.winfo_screenheight()/2)}")

lbl = Label(window, text="股票原始数据：")
lbl.grid(column=0, row=0, padx=10, pady=10)
window.update()

txt = Entry(window, width=50)
print(window.winfo_width())
txt.grid(column=1, row=0, padx=10, pady=10)


def clicked():
    files = filedialog.askopenfiles(filetypes=(("Text file", "csv"),))
    txt.insert(0, ",".join([file.name for file in files]))


btn = Button(window, text="点击选择", command=clicked)
btn.grid(column=2, row=0, padx=10, pady=10)

window.mainloop()

