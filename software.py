from tkinter import *

window = Tk()
window.title("MacroRecorder")
window.geometry("500x200")
window.iconbitmap("assets/logo.ico")

my_menu = Menu(window)
window.config(menu=my_menu)

def cmd():
    print('command')

file_menu = Menu(my_menu,tearoff=0)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New...", command=cmd)
file_menu.add_command(label="Exit", command=window.quit)

window.mainloop()