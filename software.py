import json
import threading
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from pynput import keyboard
import subprocess
import atexit
import time
import os


playback2 = False
record2 = False
recordSet = False
saveFile = False
fileAlreadySaved = False
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



def saveMacroAs(e=None):
    global macroPath, fileAlreadySaved
    if (record2 == False and playback2 == False and recordSet == True):
        macroSaved = filedialog.asksaveasfile(filetypes=[('Json Files', '*.json')], defaultextension='.json')
        if macroSaved is not None:
            macroContent = open(os.path.join(appdata_local + "/temprecord.json"), "r")
            macroEvents = json.load(macroContent)
            json_macroEvents = json.dumps(macroEvents, indent=4)
            open(macroSaved.name, "w").write(json_macroEvents)
            macroPath = macroSaved.name
            macroSaved.close()
            fileAlreadySaved = True



def saveMacro(e=None):
    if(record2 == False and playback2 == False and recordSet == True):
        if fileAlreadySaved == True:
            macroContent = open(os.path.join(appdata_local + "/temprecord.json"), "r")
            macroSaved = open(os.path.join(macroPath), "w")
            macroEvents = json.load(macroContent)
            json_macroEvents = json.dumps(macroEvents, indent=4)
            macroSaved.write(json_macroEvents)
            print('saved')
        else:
            saveMacroAs()

def loadMacro(e=None):
    global macroPath, recordSet
    if (record2 == False and playback2 == False):
        macroFile = filedialog.askopenfile(filetypes=[('Json Files', '*.json')], defaultextension='.json')
        macroContent = open(macroFile.name)
        macroPath = macroFile.name
        macroEvents = json.load(macroContent)
        json_macroEvents = json.dumps(macroEvents, indent=4)
        open(os.path.join(appdata_local + "/temprecord.json"), "w").write(json_macroEvents)
        playBtn.configure(state=NORMAL)
        file_menu.entryconfig('Save', state=NORMAL, command=saveMacro)
        file_menu.entryconfig('Save as', state=NORMAL, command=saveMacroAs)
        file_menu.entryconfig('New', state=NORMAL, command=newMacro)
        recordSet = True
        macroFile.close()


def newMacro():
    global recordSet
    keyboardControl.press(keyboard.Key.ctrl)
    keyboardControl.press('n')
    keyboardControl.release(keyboard.Key.ctrl)
    keyboardControl.release('n')
    recordBtn.configure(image=recordImg, command=startRecordingAndChangeImg)
    file_menu.entryconfig('Save', state=DISABLED)
    file_menu.entryconfig('Save as', state=DISABLED)
    file_menu.entryconfig('New', state=DISABLED)
    playBtn.configure(state=DISABLED)
    recordSet = False


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

window.bind('<Control-Shift-S>', saveMacroAs)
window.bind('<Control-s>', saveMacro)
window.bind('<Control-l>', loadMacro)

keyboardListener = keyboard.Listener(on_release=on_release)
keyboardListener.start()

window.mainloop()