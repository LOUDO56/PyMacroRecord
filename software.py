import threading
from tkinter import *
from tkinter.ttk import *
from pynput import keyboard
from keyboard import is_pressed
import subprocess
import atexit
import time
import os


playback2 = False
record2 = False
<<<<<<< HEAD
recordSet = False
keyboardControl = keyboard.Controller()


appdata_local = os.getenv('LOCALAPPDATA')+"/MacroRecorder"
appdata_local = appdata_local.replace('\\', "/")
if os.path.isdir(appdata_local) == False:
    os.mkdir(appdata_local)


def on_release(key):
    global record2, playback2, recordBtn, playBtn, recordSet
    try:
        if key.char == 'o':
            if (record2 == False and playback2 == False):
               startRecordingAndChangeImg(False)
        if key.char == 'p':
            if (record2 == False and playback2 == False and recordSet == True):
                replay(False)
                recordBtn.configure(state=DISABLED)
    except AttributeError:
        if key == keyboard.Key.esc:
            if (record2 == True and playback2 == False):
                stopRecordingAndChangeImg(False)
            if (record2 == False and playback2 == True):
                playback2 = False
                recordBtn.configure(state=NORMAL)
                playBtn.configure(image=playImg)
                file_menu.entryconfig('Load', state=NORMAL)
        if key == keyboard.Key.f12:
            playBtn.configure(state=NORMAL)
            file_menu.entryconfig('Save', state=NORMAL, command=saveMacro)
            file_menu.entryconfig('Save as', state=NORMAL, command=saveMacroAs)
            file_menu.entryconfig('New', state=NORMAL, command=newMacro)
            recordSet = True

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
>>>>>>> 7043313f60759a798761a735a23a23dd99d0135b


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
<<<<<<< HEAD
    global stopBtn, record2, playback2
    playBtn.configure(state=DISABLED)
    if playback2 == False:
        record2 = True
        file_menu.entryconfig('Load', state=DISABLED)
        if pressKey:
            keyboardControl.press('o')
            keyboardControl.release('o')
        recordBtn.configure(image=stopImg, command=stopRecordingAndChangeImg)


def stopRecordingAndChangeImg(pressKey=True):
    global recordBtn, record2, recordSet
    record2 = False
    recordSet = True
    if pressKey:
        keyboardControl.press(keyboard.Key.esc)
        keyboardControl.release(keyboard.Key.esc)
    recordBtn.configure(image=recordImg, command=startRecordingAndChangeImg)
    playBtn.configure(state=NORMAL)
    file_menu.entryconfig('Save', state=NORMAL, command=saveMacro)
    file_menu.entryconfig('Save as', state=NORMAL, command=saveMacroAs)
    file_menu.entryconfig('New', state=NORMAL, command=newMacro)
    file_menu.entryconfig('Load', state=NORMAL)

def replay(pressKey=True):
    global playback2, recordBtn, recordSet
    playBtn.configure(image=stopImg)
    if recordSet == True:
        playback2 = True
        file_menu.entryconfig('Load', state=DISABLED)
        if pressKey:
            keyboardControl.press('p')
            keyboardControl.release('p')
        recordBtn.configure(state=DISABLED)

=======
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


>>>>>>> 7043313f60759a798761a735a23a23dd99d0135b


def saveMacro():
    keyboardControl.press(keyboard.Key.ctrl_l)
    keyboardControl.press('s')
    keyboardControl.release(keyboard.Key.ctrl_l)
    keyboardControl.release('s')

def saveMacroAs():
    keyboardControl.press(keyboard.Key.ctrl_l)
    keyboardControl.press(keyboard.Key.alt)
    keyboardControl.press('s')



def newMacro():
    global recordSet
    keyboardControl.press(keyboard.Key.ctrl)
    keyboardControl.press('n')
    keyboardControl.release(keyboard.Key.ctrl)
    keyboardControl.release('n')
    recordBtn.configure(image=recordImg, command=startRecordingAndChangeImg)
    file_menu.entryconfig('Save', state=DISABLED)
    file_menu.entryconfig('Save as', state=DISABLED)
    playBtn.configure(state=DISABLED)
    recordSet = False

def loadMacro():
    if (playback2 == False and record2 == False):
        keyboardControl.press(keyboard.Key.ctrl)
        keyboardControl.press('l')

# Menu Bar
file_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", state=DISABLED)
file_menu.add_command(label="Load", command=loadMacro)
file_menu.add_command(label="Save", state=DISABLED)
file_menu.add_command(label="Save as", state=DISABLED)

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