import threading
from json import load, dumps
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
from pynput import keyboard
from pynput.keyboard import Key
from subprocess import Popen
from os import path, mkdir, getenv, remove
from webbrowser import open as OpenUrl
from atexit import register
from time import sleep
import pystray
from PIL import Image
import os



special_keys = {
    "Key.esc": Key.esc, "Key.shift": Key.shift, "Key.tab": Key.tab, "Key.caps_lock": Key.caps_lock,
    "Key.ctrl": Key.ctrl, "Key.ctrl_l": Key.ctrl_l, "Key.ctrl_r": Key.ctrl_r, "Key.alt": Key.alt,
    "Key.alt_l": Key.alt_l, "Key.alt_r": Key.alt_r, "Key.cmd": Key.cmd, "Key.cmd_l": Key.cmd_l,
    "Key.cmd_r": Key.cmd_r, "Key.enter": Key.enter, "Key.backspace": Key.backspace, "Key.f19": Key.f19,
    "Key.f18": Key.f18, "Key.f17": Key.f17, "Key.f16": Key.f16, "Key.f15": Key.f15, "Key.f14": Key.f14,
    "Key.f13": Key.f13, "Key.media_volume_up": Key.media_volume_up, "Key.media_volume_down": Key.media_volume_down,
    "Key.media_volume_mute": Key.media_volume_mute, "Key.media_play_pause": Key.media_play_pause,
    "Key.f6": Key.f6, "Key.f5": Key.f5, "Key.f4": Key.f4, "Key.f3": Key.f3, "Key.f2": Key.f2, "Key.f1": Key.f1,
    "Key.insert": Key.insert, "Key.right": Key.right, "Key.down": Key.down, "Key.left": Key.left,
    "Key.up": Key.up, "Key.page_up": Key.page_up, "Key.page_down": Key.page_down, "Key.home": Key.home,
    "Key.end": Key.end, "Key.delete": Key.delete, "Key.space": Key.space,
    "Key.alt_gr": Key.alt_gr, "Key.menu": Key.menu, "Key.num_lock": Key.num_lock,
    "Key.pause": Key.pause, "Key.print_screen": Key.print_screen, "Key.scroll_lock": Key.scroll_lock,
    "Key.shift_l": Key.shift_l, "Key.shift_r": Key.shift_r,
}

playbackStatement = False  # Know if playback is active
recordStatement = False  # Know if record is active
recordSet = False  # Know if user set recorded so he can save it
fileAlreadySaved = False  # Know if user already save is macro once so not neet to save as
closeWindow = False # Know if user is about to close the window
changeKey = False # Know to change hotkey
cantRec = False # Prevents recording from settings speed and repeat setup
hotkeyVisible = []
hotkeysDetection = []
keyboardControl = keyboard.Controller()  # Keyboard controller to detect keypress

appdata_local = getenv('LOCALAPPDATA') + "/MacroPyRecorder"
appdata_local = appdata_local.replace('\\', "/")
if path.exists(path.join(appdata_local + "/temprecord.json")):
    remove(path.join(appdata_local + "/temprecord.json"))
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
            "Record_Start": [
                "o"
            ],
            "Record_Stop": [
                "Key.esc"
            ],
            "Playback_Start": [
                "p"
            ],
            "Playback_Stop": [
                "Key.esc"
            ],
        },

        "Minimization": {
            "When_Playing": False,
            "When_Recording": False,
        },

        "Run_On_StartUp": False,

        "After_Playback": {
            "Mode": "Idle" #Quit, Lock Computer, Lof off computer, Turn off computer, Standby, Hibernate
        },

        "Cant_rec": False

    }

    userSettings_json = dumps(userSettings, indent=4)
    open(path.join(appdata_local + "/userSettings.json"), "w").write(userSettings_json)


userSettings = load(open(path.join(appdata_local+"/userSettings.json")))


def changeSettings(category, option=None, option2=None, newValue=None):
    """Change settings of user"""
    global userSettings
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
        elif option2 != None:
            userSettings[category][option][option2] = newValue
        else:
            userSettings[category][option] = newValue
    userSettings_json = dumps(userSettings, indent=4)
    open(path.join(appdata_local + "/userSettings.json"), "w").write(userSettings_json)
    userSettings = load(open(path.join(appdata_local+"/userSettings.json")))


def on_press(key):
    """
    Detect key release to change buttons in the gui
    """
    global changeKey, recordStatement, playbackStatement, recordBtn, playBtn, recordSet, userSettings, specialKeyPressed, hotkeysDetection, entryToChange, hotkeyVisible
    if changeKey == True:
        if "Key." in str(key):
            keyPressed = str(key)
        else:
            keyPressed = str(keyboardListener.canonical(key)).replace("'", "")
        if keyPressed not in hotkey:
            hotkey.append(keyPressed)
            keyPressed = keyPressed.replace("Key.", "").replace("_l", "").replace("_r", "").replace("_gr", "")
            hotkeyVisible.append(keyPressed.upper())
        entryToChange.configure(text=hotkeyVisible)
        if "ctrl" not in keyPressed and "alt" not in keyPressed and "shift" not in keyPressed:
            changeSettings("Hotkeys", typeOfHotKey, None, hotkey)
            changeKey = False
            hotkeyVisible = []
    if changeKey == False and cantRec == False:
        if "Key." in str(key):
            keyPressed = str(key)
        else:
            keyPressed = str(keyboardListener.canonical(key)).replace("'", "")
        if keyPressed not in hotkeysDetection:
            hotkeysDetection.append(keyPressed)
        if hotkeysDetection == userSettings["Hotkeys"]["Record_Start"]:
            if (recordStatement == False and playbackStatement == False):
                hotkeysDetection = []
                specialKeyPressed = False
                startRecordingAndChangeImg(False)
        if hotkeysDetection == userSettings["Hotkeys"]["Playback_Start"]:
            if (recordStatement == False and playbackStatement == False and recordSet == True):
                hotkeysDetection = []
                specialKeyPressed = False
                replay(False)
        if hotkeysDetection == userSettings["Hotkeys"]["Record_Stop"]:
            if (recordStatement == True and playbackStatement == False):
                hotkeysDetection = []
                specialKeyPressed = False
                stopRecordingAndChangeImg(False)
        if hotkeysDetection == userSettings["Hotkeys"]["Playback_Stop"]:
            if (recordStatement == False and playbackStatement == True):
                hotkeysDetection = []
                specialKeyPressed = False
                playbackStatement = False
                sleep(0.1)
                recordBtn.configure(state=NORMAL)
                playBtn.configure(image=playImg, command=replay)
                file_menu.entryconfig('New', state=NORMAL)
                file_menu.entryconfig('Load', state=NORMAL)
                file_menu.entryconfig('Save', state=NORMAL)
                file_menu.entryconfig('Save as', state=NORMAL)
                userSettings = load(open(path.join(appdata_local + "/userSettings.json")))
                if userSettings["After_Playback"]["Mode"] != "Idle":
                    cleanup()
                    window.quit()
                    if userSettings["After_Playback"]["Mode"] == "Standy":
                        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                    if userSettings["After_Playback"]["Mode"] == "Log off Computer":
                        os.system("shutdown /l")
                    if userSettings["After_Playback"]["Mode"] == "Turn off Computer":
                        os.system("shutdown /s")
                    if userSettings["After_Playback"]["Mode"] == "Hibernate (If activated)":
                        os.system("shutdown -h")
                if userSettings["Minimization"]["When_Playing"]:
                    window.deiconify()

def on_release(key):
    global hotkeysDetection
    if len(hotkeysDetection) != 0:
        hotkeysDetection.pop()

    
def startRecordingAndChangeImg(pressKey=True):
    """
    When this function is called, it presses for the user his keybind to start the recording if he pressed the button
    instead of his keyboard, it changes the button image
    """
    global stopBtn, recordStatement, playbackStatement
    userSettings = load(open(path.join(appdata_local + "/userSettings.json")))
    playBtn.configure(state=DISABLED)
    if playbackStatement == False:
        recordStatement = True
        file_menu.entryconfig('Load', state=DISABLED)
        if pressKey:
            for keys in userSettings["Hotkeys"]["Record_Start"]:
                keyToPress = keys if 'Key.' not in keys else special_keys[keys]
                keyboardControl.press(keyToPress)
            for keys in userSettings["Hotkeys"]["Record_Start"]:
                keyToPress = keys if 'Key.' not in keys else special_keys[keys]
                keyboardControl.release(keyToPress)
        recordBtn.configure(image=stopImg, command=stopRecordingAndChangeImg)
        file_menu.entryconfig('Save', state=DISABLED)
        file_menu.entryconfig('Save as', state=DISABLED)
        file_menu.entryconfig('New', state=DISABLED)
        file_menu.entryconfig('Load', state=DISABLED)
        if userSettings["Minimization"]["When_Recording"]:
           window.withdraw()


def stopRecordingAndChangeImg(pressKey=True):
    """
    When this function is called, it presses for the user his keybind to stop the recording if he pressed the button
    instead of his keyboard, it changes the button image
    """
    global recordBtn, recordStatement, recordSet
    userSettings = load(open(path.join(appdata_local + "/userSettings.json")))
    recordStatement = False
    recordSet = True
    if pressKey:
        for keys in userSettings["Hotkeys"]["Record_Stop"]:
            keyToPress = keys if 'Key.' not in keys else special_keys[keys]
            keyboardControl.press(keyToPress)
        for keys in userSettings["Hotkeys"]["Record_Stop"]:
            keyToPress = keys if 'Key.' not in keys else special_keys[keys]
            keyboardControl.release(keyToPress)
    recordBtn.configure(image=recordImg, command=startRecordingAndChangeImg)
    playBtn.configure(state=NORMAL)
    file_menu.entryconfig('Save', state=NORMAL, command=saveMacro)
    file_menu.entryconfig('Save as', state=NORMAL, command=saveMacroAs)
    file_menu.entryconfig('New', state=NORMAL, command=newMacro)
    file_menu.entryconfig('Load', state=NORMAL)
    if userSettings["Minimization"]["When_Recording"]:
        window.deiconify()


def replay(pressKey=True):
    """
        Replay the last recorded macro or the loaded one
    """
    global playbackStatement, recordBtn, recordSet
    userSettings = load(open(path.join(appdata_local + "/userSettings.json")))
    playBtn.configure(image=stopImg, command=stopReplay)
    playbackStatement = True
    file_menu.entryconfig('Save', state=DISABLED)
    file_menu.entryconfig('Save as', state=DISABLED)
    file_menu.entryconfig('New', state=DISABLED)
    file_menu.entryconfig('Load', state=DISABLED)
    if pressKey:
        for keys in userSettings["Hotkeys"]["Playback_Start"]:
            keyToPress = keys if 'Key.' not in keys else special_keys[keys]
            keyboardControl.press(keyToPress)
        for keys in userSettings["Hotkeys"]["Playback_Start"]:
            keyToPress = keys if 'Key.' not in keys else special_keys[keys]
            keyboardControl.release(keyToPress)
    recordBtn.configure(state=DISABLED)
    if userSettings["Minimization"]["When_Playing"]:
        window.withdraw()

def stopReplay():
    for keys in userSettings["Hotkeys"]["Playback_Stop"]:
        keyToPress = keys if 'Key.' not in keys else special_keys[keys]
        keyboardControl.press(keyToPress)
    for keys in userSettings["Hotkeys"]["Playback_Stop"]:
        keyToPress = keys if 'Key.' not in keys else special_keys[keys]
        keyboardControl.release(keyToPress)

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
            fileAlreadySaved = True


def newMacro(e=None):
    """
        Load a script that the user did, to play it or overwrite it (if he saved his new record of course)
    """
    global recordSet, fileAlreadySaved
    if recordStatement == False and playbackStatement == False:
        if recordSet == True:
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
    if recordSet == True and fileAlreadySaved == False:
        closeWindow = True
        wantToSave = warningPopUpSave()
        if wantToSave:
            saveMacro()
        elif wantToSave == False:
            macro_process.terminate()
            window.destroy()
            icon.stop()
    else:
        macro_process.terminate()
        window.destroy()
        icon.stop()

def validate_input(action, value_if_allowed):
    if action == "1":  # Insert
        try:
            float(value_if_allowed)
            return True
        except ValueError:
            return False
    return True


def changeSpeed():
    global speedWin, horizontal_line, speedTestVal, cantRec
    cantRec = True
    changeSettings("Cant_rec")
    speedWin = Toplevel(window)
    w = 300
    h = 150
    speedWin.geometry('%dx%d+%d+%d' % (w, h, x, y))
    speedWin.title("Change Speed")
    speedWin.grab_set()
    speedWin.resizable(False, False)
    speedWin.attributes("-toolwindow", 1)
    Label(speedWin, text="Enter Speed Number between 0.1 and 10", font = ('Segoe UI', 10)).pack(side=TOP, pady=10)
    userSettings = load(open(path.join(appdata_local + "/userSettings.json")))
    setNewSpeedInput = Entry(speedWin, width=10)
    setNewSpeedInput.insert(0, str(userSettings["Playback"]["Speed"]))
    setNewSpeedInput.pack(pady=20)
    buttonArea = Frame(speedWin)
    Button(buttonArea, text="Confirm", command=lambda: setNewSpeedNumber(setNewSpeedInput.get())).pack(side=LEFT, padx=10)
    Button(buttonArea, text="Cancel", command=speedWin.destroy).pack(side=LEFT, padx=10)
    buttonArea.pack(side=BOTTOM, pady=10)
    window.wait_window(speedWin)
    cantRec = False
    changeSettings("Cant_rec")

def setNewSpeedNumber(val):
    try:
        if float(val) <= 0 or float(val) > 10:
            messagebox.showerror("Wrong Speed Number", "Your speed value must be between 0.1 and 10!")
        else:
            changeSettings("Playback", "Speed", None, float(val))
            speedWin.destroy()
    except ValueError:
        messagebox.showerror("Wrong Speed Number", "Your input must be a number!")


def repeatGuiSettings():
    global cantRec
    cantRec = True
    repeatGui = Toplevel(window)
    changeSettings("Cant_rec")
    w = 300
    h = 150
    repeatGui.geometry('%dx%d+%d+%d' % (w, h, x, y))
    repeatGui.title("Change Speed")
    repeatGui.grab_set()
    repeatGui.resizable(False, False)
    repeatGui.attributes("-toolwindow", 1)
    Label(repeatGui, text="Enter Repeat Number ", font=('Segoe UI', 10)).pack(side=TOP, pady=10)
    userSettings = load(open(path.join(appdata_local + "/userSettings.json")))
    repeatTimes = Spinbox(repeatGui, from_=1, to=100000000, width=7, validate="key", validatecommand=(validate_cmd, "%d", "%P"))
    repeatTimes.insert(0, userSettings["Playback"]["Repeat"]["Times"])
    repeatTimes.pack(pady=20)
    buttonArea = Frame(repeatGui)
    Button(buttonArea, text="Confirm", command=lambda: [changeSettings("Playback", "Repeat", "Times", int(repeatTimes.get())), repeatGui.destroy()]).pack(side=LEFT,padx=10)
    Button(buttonArea, text="Cancel", command=repeatGui.destroy).pack(side=LEFT, padx=10)
    buttonArea.pack(side=BOTTOM, pady=10)
    window.wait_window(repeatGui)
    cantRec = False
    changeSettings("Cant_rec")


def afterPlaybackGui():
    global cantRec
    cantRec = True
    playBackGui = Toplevel(window)
    changeSettings("Cant_rec")
    w = 250
    h = 150
    playBackGui.geometry('%dx%d+%d+%d' % (w, h, x, y))
    playBackGui.title("After Playback")
    playBackGui.grab_set()
    playBackGui.resizable(False, False)
    playBackGui.attributes("-toolwindow", 1)

    options = [
        'Idle',
        'Quit Software',
        'Standy',
        'Log off Computer',
        'Turn off Computer',
        'Hibernate (If activated)'

    ]
    menuOptions = LabelFrame(playBackGui, text="On playback complete")
    AfterPlaybackOption = StringVar()
    userSettings = load(open(path.join(appdata_local + "/userSettings.json")))
    OptionMenu(menuOptions, AfterPlaybackOption, userSettings["After_Playback"]["Mode"], *options).pack(fill="both", padx=10, pady=10)
    menuOptions.pack(fill="both", padx=5, pady=10)
    buttonArea = Frame(playBackGui)
    Button(buttonArea, text="Confirm", command=lambda: [changeSettings("After_Playback", "Mode", None, AfterPlaybackOption.get()), playBackGui.destroy()]).pack(side=LEFT, padx=10)
    Button(buttonArea, text="Cancel", command=playBackGui.destroy).pack(side=LEFT, padx=10)
    buttonArea.pack(side=BOTTOM, pady=10)
    window.wait_window(playBackGui)
    cantRec = False
    changeSettings("Cant_rec")


def hotkeySettingsGui():
    global typeOfHotKey, startKey, stopKey, playbackStartKey, playbackStopKey, cantRec
    cantRec = True
    changeSettings("Cant_rec")
    hotkeyGui = Toplevel(window)
    w = 300
    h = 200
    hotkeyGui.geometry('%dx%d+%d+%d' % (w, h, x, y))
    hotkeyGui.title("Hotkey settings")
    hotkeyGui.grab_set()
    hotkeyGui.resizable(False, False)
    hotkeyGui.attributes("-toolwindow", 1)
    hotkeyLine = Frame(hotkeyGui)
    hotkeyStart = userSettings["Hotkeys"]["Record_Start"]
    hotkeyStop = userSettings["Hotkeys"]["Record_Stop"]
    hotkeyPlaybackStart = userSettings["Hotkeys"]["Playback_Start"]
    hotkeyPlaybackStop = userSettings["Hotkeys"]["Playback_Stop"]
    hotkeyVisible = [hotkeyStart, hotkeyStop, hotkeyPlaybackStart, hotkeyPlaybackStop]
    cleanedHotkeys = []
    for key in hotkeyVisible:
        if isinstance(key, list):
            cleanedSublist = [
                subkey.replace("Key.", "").replace("_l", "").replace("_r", "").replace("_gr", "").upper() if isinstance(
                    subkey, str) else subkey for subkey in key]
            cleanedHotkeys.append(cleanedSublist)
        else:
            cleanedKey = key.replace("Key.", "").replace("_l", "").replace("_r", "").replace("_gr", "").upper()
            cleanedHotkeys.append(cleanedKey)
    hotkeyVisible = cleanedHotkeys
    Button(hotkeyLine, text="Start Record", command=lambda: enableHotKeyDetection("Record_Start", startKey)).grid(row=0, column=0, padx=10)
    startKey = Label(hotkeyLine, text=hotkeyVisible[0], font=('Segoe UI', 12))
    startKey.grid(row=0, column=1, pady=5)

    Button(hotkeyLine, text="Stop Record", command=lambda: enableHotKeyDetection("Record_Stop", stopKey)).grid(row=1, column=0, padx=10)
    stopKey = Label(hotkeyLine, text=hotkeyVisible[1], font=('Segoe UI', 12))
    stopKey.grid(row=1, column=1, pady=5)

    Button(hotkeyLine, text="Playback Start", command=lambda: enableHotKeyDetection("Playback_Start", playbackStartKey)).grid(row=2, column=0, padx=10)
    playbackStartKey = Label(hotkeyLine, text=hotkeyVisible[2], font=('Segoe UI', 12))
    playbackStartKey.grid(row=2, column=1, pady=5)

    Button(hotkeyLine, text="Playback Stop", command=lambda: enableHotKeyDetection("Playback_Stop", playbackStopKey)).grid(row=3, column=0, padx=10)
    playbackStopKey = Label(hotkeyLine, text=hotkeyVisible[3], font=('Segoe UI', 12))
    playbackStopKey.grid(row=3, column=1, pady=5)

    hotkeyLine.pack()

    buttonArea = Frame(hotkeyGui)
    Button(buttonArea, text="Close", command=hotkeyGui.destroy).pack(side=LEFT, padx=10)
    buttonArea.pack(side=BOTTOM, pady=10)
    window.wait_window(hotkeyGui)
    cantRec = False
    changeSettings("Cant_rec")



def enableHotKeyDetection(mode, entry):
    global changeKey, typeOfHotKey, hotkey, entryToChange
    changeKey = True
    typeOfHotKey = mode
    hotkey = []
    entry.configure(text="Please key")
    entryToChange = entry



def destroyWindow(win):
    global cantRec
    win.destroy()
    changeSettings("Cant_rec")
    cantRec = False

def systemTray():
    global icon
    image = Image.open("assets/logo.ico")
    menu = (
        pystray.MenuItem('Show', action=window.deiconify,default=True),
    )
    icon = pystray.Icon("name", image, "MacroPyRecorder", menu)
    icon.run()


def cleanup():
    """
        When the users want to stop the software, the macro.py in the background is terminated
    """
    if 'macro_process' in globals():
        macro_process.terminate()
    icon.stop()


register(cleanup)

macro_process = Popen(['pythonw',
                       'macro.py'])  # it serves to run macro.py in the background because thread make the recording slower for some reasons

# Window Setup
window = Tk()
window.title("MacroPyRecorder")
w = 350
h = 200
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
window.geometry('%dx%d+%d+%d' % (w, h, x, y))

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
file_menu.add_separator()
file_menu.add_command(label="Save", state=DISABLED, accelerator="Ctrl+S")
file_menu.add_command(label="Save as", state=DISABLED, accelerator="Ctrl+Shift+S")

# Options Section
options_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Options", menu=options_menu)

# Playback Sub
playback_sub = Menu(options_menu, tearoff=0)
options_menu.add_cascade(label="Playback", menu=playback_sub)
playback_sub.add_command(label="Speed", command=changeSpeed)
playback_sub.add_command(label="Repeat", command=repeatGuiSettings)

# Recordings Sub
mouseMove = BooleanVar(value=userSettings["Recordings"]["Mouse_Move"])
mouseClick = BooleanVar(value=userSettings["Recordings"]["Mouse_Click"])
keyboardInput = BooleanVar(value=userSettings["Recordings"]["Mouse_Move"])
recordings_sub = Menu(options_menu, tearoff=0)
options_menu.add_cascade(label="Recordings", menu=recordings_sub)
recordings_sub.add_checkbutton(label="Mouse movement", variable=mouseMove, command=lambda: changeSettings("Recordings", "Mouse_Move"))
recordings_sub.add_checkbutton(label="Mouse click", variable=mouseClick, command=lambda: changeSettings("Recordings", "Mouse_Click"))
recordings_sub.add_checkbutton(label="Keyboard", variable=keyboardInput, command=lambda: changeSettings("Recordings", "Keyboard"))

# Options Sub
options_sub = Menu(options_menu, tearoff=0)
options_menu.add_cascade(label="Options", menu=options_sub)
options_sub.add_command(label="Hotkeys", command=hotkeySettingsGui)

minimization_sub = Menu(options_sub, tearoff=0)
options_sub.add_cascade(label="Minimization", menu=minimization_sub)
minimization_playing = BooleanVar(value=userSettings["Minimization"]["When_Playing"])
minimization_record = BooleanVar(value=userSettings["Minimization"]["When_Recording"])
minimization_sub.add_checkbutton(label="Minimized when playing", variable=minimization_playing, command=lambda: changeSettings("Minimization", "When_Playing"))
minimization_sub.add_checkbutton(label="Minimized when recording", variable=minimization_record, command=lambda: changeSettings("Minimization", "When_Recording"))

runStartUp = BooleanVar().set(userSettings["Run_On_StartUp"])
# options_sub.add_checkbutton(label="Run on startup", variable=runStartUp, command=lambda: changeSettings("Run_On_StartUp"))
options_sub.add_command(label="After playback...", command=afterPlaybackGui)

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

keyboardListener = keyboard.Listener(on_press=on_press, on_release=on_release)
keyboardListener.start()

validate_cmd = window.register(validate_input)

window.protocol("WM_DELETE_WINDOW", stopProgram)

threading.Thread(target=systemTray).start()

if userSettings["Cant_rec"]:
    changeSettings("Cant_rec")

window.mainloop()