import threading
from tkinter import *
from tkinter.ttk import *
from pynput import keyboard
from keyboard import is_pressed
import subprocess
import atexit
import time


playback2 = False
record2 = False
keyboardControl = keyboard.Controller()



def on_release(key):
    global record2, playback2, recordBtn, lengthOfRecord
    try:
        if key.char == 'è':
            if record2 == False:
                startRecordingAndChangeImg(False)
        if key.char == 'à':
            if (record2 == False and playback2 == False):
                replay(False)
    except AttributeError:
        if key == keyboard.Key.esc:
            if record2 == True:
                stopRecordingAndChangeImg(False)


# def key_released(e):
#     global record2, playback2
#
#     if e.keysym == 'Escape':
#         if record2 == True:
#             stopRecordingAndChangeImg(False)
#
#     if e.char == 'è':
#         if (record2 == False and playback2 == False):
#             startRecordingAndChangeImg(False)
#     #
#     if e.char == 'à':
#         if (record2 == False and playback2 == False):
#             replay(False)


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


def startRecordingAndChangeImg(pressKey=True):
    global stopBtn, lengthOfRecord, record2, playback2
    if playback2 == False:
        if pressKey:
            keyboardControl.press('è')
            keyboardControl.release('è')
        lengthOfRecord = time.time()
        recordBtn.configure(image=stopImg, command=stopRecordingAndChangeImg)
        record2 = True
        print('function start callled')


def stopRecordingAndChangeImg(pressKey=True):
    global recordBtn, lengthOfRecord, record2
    if pressKey:
        keyboardControl.press(keyboard.Key.esc)
        keyboardControl.release(keyboard.Key.esc)
    print(time.time() - lengthOfRecord)
    lengthOfRecord = (time.time() - lengthOfRecord) + 2
    recordBtn.configure(image=recordImg, command=startRecordingAndChangeImg)
    playBtn.configure(state=NORMAL)
    print('record stoppé')
    record2 = False

def replay(pressKey=True):
    global playback2, recordBtn
    playback2 = True
    if pressKey:
        keyboardControl.press('à')
        keyboardControl.release('à')
    recordBtn.configure(state=DISABLED)
    threading.Thread(target=buttonDisabledToEnable).start()

def buttonDisabledToEnable():
    global playback2, lengthOfRecord
    time.sleep(lengthOfRecord)
    recordBtn.configure(state=NORMAL)
    playback2 = False




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

# window.bind('<KeyRelease>',key_released )

keyboardListener = keyboard.Listener(on_release=on_release)
keyboardListener.start()

window.mainloop()