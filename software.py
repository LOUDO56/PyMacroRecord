import threading
from tkinter import *
from tkinter.ttk import *

from macro import startRecord, stopRecord, playRec

# Window Setup
window = Tk()
window.title("MacroRecorder")
window.geometry("350x200")
window.iconbitmap("assets/logo.ico")

my_menu = Menu(window)
window.config(menu=my_menu)


def startRecordingAndChangeImg():
    global stopBtn
    recordBtn.pack_forget()
    stopBtn = Button(window, image=stopImg, command=stopRecordingAndChangeImg)
    stopBtn.pack(side=RIGHT, padx=50)
    startRecord()
    window.wait_variable()

def stopRecordingAndChangeImg():
    global recordBtn
    stopBtn.pack_forget()
    recordBtn = Button(window, image=recordImg, command=startRecordingAndChangeImg)
    recordBtn.pack(side=RIGHT, padx=50)
    stopRecord()


# Menu Bar
file_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New")
file_menu.add_command(label="Save", command=window.quit, state=DISABLED)
file_menu.add_command(label="Save as", command=window.quit, state=DISABLED)
file_menu.add_separator()
file_menu.add_command(label="Settings", command=window.quit)

# Play Button
playImg = PhotoImage(file=r"assets/button/play.png")
playBtn = Button(window, image=playImg, command=playRec)
playBtn.pack(side=LEFT, padx=50)

# Record Button
recordImg = PhotoImage(file=r"assets/button/record.png")
recordBtn = Button(window, image=recordImg, command=startRecordingAndChangeImg)
recordBtn.pack(side=RIGHT, padx=50)

# Stop Button
stopImg = PhotoImage(file=r"assets/button/stop.png")

window.mainloop()
