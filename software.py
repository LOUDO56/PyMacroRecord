from json import load, dumps
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
from pynput import keyboard
from subprocess import Popen
from os import path, mkdir, getenv, remove
from webbrowser import open as OpenUrl
from atexit import register
from time import sleep

playbackStatement = False  # Know if playback is active
recordStatement = False  # Know if record is active
recordSet = False  # Know if user set recorded so he can save it
fileAlreadySaved = False  # Know if user already save is macro once so not neet to save as
closeWindow = False # Know if user is about to close the window
keyboardControl = keyboard.Controller()  # Keyboard controller to detect keypress

appdata_local = getenv('LOCALAPPDATA') + "/MacroRecorder"
appdata_local = appdata_local.replace('\\', "/")
if path.isdir(appdata_local) == False:
    mkdir(appdata_local)  # Temp record to interact with macro.py
    userSettings = {
        "Playback": {
            "Speed": 1,
            "Repeat": {
                "Mode": "OneTime",
                "Times": 1,
                "For": 0,
                "Interval": 0

            }
        },

        "Recordings": {
            "Mouse_Move": True,
            "Mouse_Click": True,
            "Keyboard": True,
        },

        "Hotkeys": {
            "Record_Start": "o",
            "Record_Stop": str(keyboard.Key.esc),
            "Playback_Start": "p",
            "Playback_Stop": str(keyboard.Key.esc),
        },

        "Minimization": {
            "When_Playing": False,
            "When_Recording": False,
        },

        "Run_On_StartUp": False,

        "After_Recording": "Idle" #Quit, Lock Computer, Lof off computer, Turn off computer, Standby, Hibernate

    }

    userSettings_json = dumps(userSettings, indent=4)
    open(path.join(appdata_local + "/userSettings.json"), "w").write(userSettings_json)


userSettings = load(open(path.join(appdata_local+"/userSettings.json")))


def changeSettings(category, option=None, newValue=None):
    """Change settings of user"""
    if newValue is None:
        if option is None:
            if userSettings[category]:
                userSettings[category] = False
            else:
                userSettings[category] = True
        else:
            if userSettings[category][option]:
                userSettings[category][option] = False
            else:
                userSettings[category][option] = True

    if option is not None and newValue is not None:
        if option == None:
            userSettings[category] = newValue
        else:
            userSettings[category][option] = newValue
    userSettings_json = dumps(userSettings, indent=4)
    open(path.join(appdata_local + "/userSettings.json"), "w").write(userSettings_json)


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
                sleep(0.1)
                recordBtn.configure(state=NORMAL)
                playBtn.configure(image=playImg)
                file_menu.entryconfig('New', state=NORMAL)
                file_menu.entryconfig('Load', state=NORMAL)
                file_menu.entryconfig('Save', state=NORMAL)
                file_menu.entryconfig('Save as', state=NORMAL)


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
    print('playback')
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
        if closeWindow:
            window.destroy()


def loadMacro(e=None):
    """
        Load a script that the user did, to play it or overwrite it (if he saved his new record of course)
    """
    global macroPath, recordSet, fileAlreadySaved
    if recordStatement == False and playbackStatement == False:
        if recordSet == True:
            wantToSave = warningPopUpSave()
            if wantToSave == None:
                return
            elif wantToSave:
                saveMacro()
        macroFile = filedialog.askopenfile(filetypes=[('Json Files', '*.json')], defaultextension='.json')
        if macroFile is not None:
            macroContent = open(macroFile.name)
            macroPath = macroFile.name
            macroEvents = load(macroContent)
            json_macroEvents = dumps(macroEvents, indent=4)
            open(path.join(appdata_local + "/temprecord.json"), "w").write(json_macroEvents)
            playBtn.configure(state=NORMAL)
            file_menu.entryconfig('Save', state=NORMAL, command=saveMacro)
            file_menu.entryconfig('Save as', state=NORMAL, command=saveMacroAs)
            file_menu.entryconfig('New', state=NORMAL, command=newMacro)
            macroFile.close()
            print("loaded")
            fileAlreadySaved = True


def newMacro(e=None):
    """
        Load a script that the user did, to play it or overwrite it (if he saved his new record of course)
    """
    global recordSet, fileAlreadySaved
    if recordStatement == False and playbackStatement == False and recordSet == True:
        wantToSave = warningPopUpSave()
        if wantToSave == None:
            return
        elif wantToSave:
            saveMacro()
        recordBtn.configure(image=recordImg, command=startRecordingAndChangeImg)
        file_menu.entryconfig('Save', state=DISABLED)
        file_menu.entryconfig('Save as', state=DISABLED)
        file_menu.entryconfig('New', state=DISABLED)
        playBtn.configure(state=DISABLED)
        recordSet = False
        fileAlreadySaved = False

def warningPopUpSave():
    return messagebox.askyesnocancel("Info", "Do you want to save your record?")

def stopProgram():
    global closeWindow, macro_process
    """
        When the users want to stop the software, the macro.py in the background is terminated
    """
    if recordSet == True:
        closeWindow = True
        wantToSave = warningPopUpSave()
        if wantToSave:
            saveMacro()
            remove_temprecord()
        elif wantToSave == False:
            remove_temprecord()
            macro_process.terminate()
            window.destroy()
    else:
        remove_temprecord()
        macro_process.terminate()
        window.destroy()

def remove_temprecord():
    try:
        remove(path.join(appdata_local + "/temprecord.json"))
    except FileNotFoundError:
        pass


def changeSpeed():
    global speedWin, horizontal_line, speedTestVal
    speedWin = Toplevel(window)
    speedWin.geometry("300x150")
    speedWin.title("Change Speed")
    speedWin.grab_set()
    speedWin.resizable(False, False)
    speedWin.attributes("-toolwindow", 1)
    speedTestVal = Label(speedWin, text="Speed 0")
    speedTestVal.pack()
    speedTestVal.pack(side=TOP)
    horizontal_line = Scale(speedWin, from_=0.1, to=10, command=getSpeedNumber)
    horizontal_line.set('1')
    horizontal_line.pack(side=BOTTOM, pady=30)

def getSpeedNumber(val=0):
    val = round(float(val))
    speedTestVal.config(text = f"Speed {val}")

def cleanup():
    """
        When the users want to stop the software, the macro.py in the background is terminated
    """
    if 'macro_process' in globals():
        macro_process.terminate()


register(cleanup)

macro_process = Popen(['pythonw',
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
file_menu.add_command(label="New", state=DISABLED, accelerator="Ctrl+N")
file_menu.add_command(label="Load", command=loadMacro, accelerator="Ctrl+L")
file_menu.add_command(label="Save", state=DISABLED, accelerator="Ctrl+S")
file_menu.add_command(label="Save as", state=DISABLED, accelerator="Ctrl+Shift+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)

# Options Section
options_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Options", menu=options_menu)

# Playback Sub
playback_sub = Menu(options_menu, tearoff=0)
options_menu.add_cascade(label="Playback", menu=playback_sub)
playback_sub.add_command(label="Speed", command=changeSpeed)
playback_sub.add_command(label="Repeat")

# Recordings Sub
mouseMove = BooleanVar()
mouseClick = BooleanVar()
keyboardInput = BooleanVar()
mouseMove.set(userSettings["Recordings"]["Mouse_Move"])
mouseClick.set(userSettings["Recordings"]["Mouse_Click"])
keyboardInput.set(userSettings["Recordings"]["Keyboard"])
recordings_sub = Menu(options_menu, tearoff=0)
options_menu.add_cascade(label="Recordings", menu=recordings_sub)
recordings_sub.add_checkbutton(label="Mouse movement", variable=mouseMove, command=lambda: changeSettings("Recordings", "Mouse_Move"))
recordings_sub.add_checkbutton(label="Mouse click", variable=mouseClick, command=lambda: changeSettings("Recordings", "Mouse_Click"))
recordings_sub.add_checkbutton(label="Keyboard", variable=keyboardInput, command=lambda: changeSettings("Recordings", "Keyboard"))

# Options Sub
options_sub = Menu(options_menu, tearoff=0)
options_menu.add_cascade(label="Options", menu=options_sub)
options_sub.add_command(label="Hotkeys")

minimization_sub = Menu(options_sub, tearoff=0)
options_sub.add_cascade(label="Minimization", menu=minimization_sub)
minimization_playing = BooleanVar().set(userSettings["Minimization"]["When_Playing"])
minimization_record = BooleanVar().set(userSettings["Minimization"]["When_Recording"])
minimization_sub.add_checkbutton(label="Minimized when playing", variable=minimization_playing, command=lambda: changeSettings("Minimization", "When_Playing"))
minimization_sub.add_checkbutton(label="Minimized when recording", variable=minimization_record, command=lambda: changeSettings("Minimization", "When_Recording"))

runStartUp = BooleanVar().set(userSettings["Run_On_StartUp"])
options_sub.add_checkbutton(label="Run on startup", variable=runStartUp, command=lambda: changeSettings("Run_On_StartUp"))
options_sub.add_command(label="After recording")

help_section = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Help", menu=help_section)
help_section.add_command(label="Github Page", command=lambda: OpenUrl("https://github.com/LOUDO56/macro-recorder/tree/main#readme"))
help_section.add_command(label="About")

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

window.protocol("WM_DELETE_WINDOW", stopProgram)

window.mainloop()