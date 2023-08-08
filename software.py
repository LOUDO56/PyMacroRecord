from json import load, dumps
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from pynput import keyboard
from subprocess import Popen
from atexit import register
from os import path, mkdir, getenv

playbackStatement = False  # Know if playback is active
recordStatement = False  # Know if record is active
recordSet = False  # Know if user set recorded so he can save it
fileAlreadySaved = False  # Know if user already save is macro once so not neet to save as
keyboardControl = keyboard.Controller()  # Keyboard controller to detect keypress

appdata_local = getenv('LOCALAPPDATA') + "/MacroRecorder"
appdata_local = appdata_local.replace('\\', "/")
if path.isdir(appdata_local) == False:
    mkdir(appdata_local)  # Temp record to interact with macro.py


def on_release(key):
    """
    Detect key release to change buttons in the gui
    """
    global recordStatement, playbackStatement, recordBtn, playBtn, recordSet
    try:
        if key.char == 'o':
            if (recordStatement == False and playbackStatement == False):
                startRecordingAndChangeImg(False)
        if key.char == 'p':
            if (recordStatement == False and playbackStatement == False and recordSet == True):
                replay(False)
                recordBtn.configure(state=DISABLED)
    except AttributeError:
        if key == keyboard.Key.esc:
            if (recordStatement == True and playbackStatement == False):
                stopRecordingAndChangeImg(False)
            if (recordStatement == False and playbackStatement == True):
                playbackStatement = False
                recordBtn.configure(state=NORMAL)
                playBtn.configure(image=playImg)
                file_menu.entryconfig('Load', state=NORMAL)


def startRecordingAndChangeImg(pressKey=True):
    """
    When this function is called, it presses for the user his keybind to start the recording if he pressed the button
    instead of his keyboard, it changes the button image
    """
    global stopBtn, recordStatement, playbackStatement
    playBtn.configure(state=DISABLED)
    if playbackStatement == False:
        recordStatement = True
        file_menu.entryconfig('Load', state=DISABLED)
        if pressKey:
            keyboardControl.press('o')
            keyboardControl.release('o')
        recordBtn.configure(image=stopImg, command=stopRecordingAndChangeImg)
        file_menu.entryconfig('Save', state=DISABLED)
        file_menu.entryconfig('Save as', state=DISABLED)
        file_menu.entryconfig('New', state=DISABLED)
        file_menu.entryconfig('Load', state=DISABLED)


def stopRecordingAndChangeImg(pressKey=True):
    """
    When this function is called, it presses for the user his keybind to stop the recording if he pressed the button
    instead of his keyboard, it changes the button image
    """
    global recordBtn, recordStatement, recordSet
    recordStatement = False
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
    """
        Replay the last recorded macro or the loaded one
    """
    global playbackStatement, recordBtn, recordSet
    playBtn.configure(image=stopImg)
    if recordSet == True:
        playbackStatement = True
        file_menu.entryconfig('Save', state=DISABLED)
        file_menu.entryconfig('Save as', state=DISABLED)
        file_menu.entryconfig('New', state=DISABLED)
        file_menu.entryconfig('Load', state=DISABLED)
        if pressKey:
            keyboardControl.press('p')
            keyboardControl.release('p')
        recordBtn.configure(state=DISABLED)


def saveMacroAs(e=None):
    """
        Save the macro as a file name, I use temprecord.json to retrieve the last record and then save it on his file
    """
    global macroPath, fileAlreadySaved
    if recordStatement == False and playbackStatement == False and recordSet == True:
        macroSaved = filedialog.asksaveasfile(filetypes=[('Json Files', '*.json')], defaultextension='.json')
        if macroSaved is not None:
            macroContent = open(path.join(appdata_local + "/temprecord.json"), "r")
            macroEvents = load(macroContent)
            json_macroEvents = dumps(macroEvents, indent=4)
            open(macroSaved.name, "w").write(json_macroEvents)
            macroPath = macroSaved.name
            # macroPath serve to know where his last saved macro is, so the user can
            # overwrite it if he did a new record
            macroSaved.close()
            fileAlreadySaved = True


def saveMacro(e=None):
    """
        Save the last macro saved or loaded, I use temprecord.json to retrieve the last record and then save it on his file
    """
    if recordStatement == False and playbackStatement == False and recordSet == True:
        if fileAlreadySaved == True:
            macroContent = open(path.join(appdata_local + "/temprecord.json"), "r")
            macroSaved = open(path.join(macroPath), "w")
            macroEvents = load(macroContent)
            json_macroEvents = dumps(macroEvents, indent=4)
            macroSaved.write(json_macroEvents)
            print('saved')
        else:
            saveMacroAs()


def loadMacro(e=None):
    """
        Load a script that the user did, to play it or overwrite it (if he saved his new record of course)
    """
    global macroPath, recordSet
    if recordStatement == False and playbackStatement == False:
        macroFile = filedialog.askopenfile(filetypes=[('Json Files', '*.json')], defaultextension='.json')
        macroContent = open(macroFile.name)
        macroPath = macroFile.name
        macroEvents = load(macroContent)
        json_macroEvents = dumps(macroEvents, indent=4)
        open(path.join(appdata_local + "/temprecord.json"), "w").write(json_macroEvents)
        playBtn.configure(state=NORMAL)
        file_menu.entryconfig('Save', state=NORMAL, command=saveMacro)
        file_menu.entryconfig('Save as', state=NORMAL, command=saveMacroAs)
        file_menu.entryconfig('New', state=NORMAL, command=newMacro)
        recordSet = True
        macroFile.close()


def newMacro(e=None):
    """
        Load a script that the user did, to play it or overwrite it (if he saved his new record of course)
    """
    global recordSet, fileAlreadySaved
    if recordStatement == False and playbackStatement == False and recordSet == True:
        recordBtn.configure(image=recordImg, command=startRecordingAndChangeImg)
        file_menu.entryconfig('Save', state=DISABLED)
        file_menu.entryconfig('Save as', state=DISABLED)
        file_menu.entryconfig('New', state=DISABLED)
        playBtn.configure(state=DISABLED)
        recordSet = False
        fileAlreadySaved = False


def cleanup():
    """
        When the users want to stop the software, the macro.py in the background is terminated
    """
    if 'macro_process' in globals():
        macro_process.terminate()


register(cleanup)

macro_process = Popen(['python',
                       'macro.py'])  # it serves to run macro.py in the background because thread make the recording slower for some reasons

# Window Setup
window = Tk()
window.title("MacroRecorder")
window.geometry("350x200")
window.iconbitmap("assets/logo.ico")
window.resizable(False, False)

# Menu Setup
my_menu = Menu(window)
window.config(menu=my_menu)

# File Section
file_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", state=DISABLED)
file_menu.add_command(label="Load", command=loadMacro)
file_menu.add_command(label="Save", state=DISABLED)
file_menu.add_command(label="Save as", state=DISABLED)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)

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
window.bind('<Control-n>', newMacro)

keyboardListener = keyboard.Listener(on_release=on_release)
keyboardListener.start()

window.mainloop()
