import threading
from tkinter import *
from tkinter.ttk import *
from pynput import keyboard
import subprocess
import atexit
import time

keyboardControl = keyboard.Controller()

def cleanup():
    if 'macro_process' in globals():
        macro_process.terminate()

atexit.register(cleanup)

macro_process = subprocess.Popen(['python', 'macro.py'])

# Window Setup
window = Tk()
window.title("MacroRecorder")
window.geometry("350x200")
window.iconbitmap("assets/logo.ico")
window.resizable(False,False)

my_menu = Menu(window)
window.config(menu=my_menu)


def startRecordingAndChangeImg():
    global stopBtn
    global lenghtOfRecord
    keyboardControl.press('1')
    keyboardControl.release('1')
    lenghtOfRecord = time.time()
    recordBtn.configure(image=stopImg, command=stopRecordingAndChangeImg)


def stopRecordingAndChangeImg():
    global recordBtn
    global lenghtOfRecord
    keyboardControl.press('2')
    keyboardControl.release('2')
    lenghtOfRecord = (time.time() - lenghtOfRecord) + 1
    recordBtn.configure(image=recordImg, command=startRecordingAndChangeImg)
    playBtn.configure(state=NORMAL)

def replay():
    recordBtn.configure(state=DISABLED)
    keyboardControl.press('3')
    keyboardControl.release('3')
    threading.Thread(target=buttonDisabledToEnable).start()

def buttonDisabledToEnable():
    time.sleep(lenghtOfRecord)
    recordBtn.configure(state=NORMAL)


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
playBtn = Button(window, image=playImg, command=replay, state=DISABLED)
playBtn.pack(side=LEFT, padx=50)

# Record Button
recordImg = PhotoImage(file=r"assets/button/record.png")
recordBtn = Button(window, image=recordImg, command=startRecordingAndChangeImg)
recordBtn.pack(side=RIGHT, padx=50)

# Stop Button
stopImg = PhotoImage(file=r"assets/button/stop.png")



window.mainloop()
