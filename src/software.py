import threading
from threading import Thread
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
import pystray
from PIL import Image
import os
from requests import get as getVer
from win10toast import ToastNotifier

from global_function import *


version = "1.0.0"

# ------------------------------------------------------------------------------ #
#
#
#                               SETUP PART
#
#
# ------------------------------------------------------------------------------ #


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
# Special keys are for on press and on release event so when the playback is on, it can press special keys without errors

# Variable Setup

playbackStatement = False  # Know if playback is active
recordStatement = False  # Know if record is active
recordSet = False  # Know if user set recorded so he can save it
fileAlreadySaved = False  # Know if user already save is macro once so not neet to save as
closeWindow = False  # Know if user is about to close the window
changeKey = False  # Know to change hotkey
cantRec = False  # Prevents recording from settings speed and repeat setup
macroPath = None
hotkeyVisible = []  # For Gui visual
hotkeysDetection = []  # Detect Hotkeys
keyboardControl = keyboard.Controller()  # Keyboard controller to detect keypress

appdata_local = getenv('LOCALAPPDATA') + "/PyMacroRecord"
appdata_local = appdata_local.replace('\\', "/")
userSettingsPath = appdata_local + "/userSettings.json"

# Prevents from playing last record not saved or saved when re-launching the software
if path.exists(path.join(appdata_local + "/temprecord.json")):
    remove(path.join(appdata_local + "/temprecord.json"))

# Setup of UserSettings if not exists
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
            "Mode": "Idle"  # Quit, Lock Computer, Lof off computer, Turn off computer, Standby, Hibernate
        },

        "Cant_rec": False,
        "StoppedRecManually": False,
        "NotDetectingKeyPressPlayBack": False

    }

    userSettings_json = dumps(userSettings, indent=4)
    open(path.join(userSettingsPath), "w").write(userSettings_json)

userSettings = load(open(path.join(userSettingsPath)))

if "StoppedRecManually" not in userSettings or "NotDetectingKeyPressPlayBack" not in userSettings:
    userSettings["StoppedRecManually"] = False
    userSettings["NotDetectingKeyPressPlayBack"] = False
    userSettings_json = dumps(userSettings, indent=4)
    open(path.join(userSettingsPath), "w").write(userSettings_json)


if userSettings["StoppedRecManually"]:
    changeSettings("StoppedRecManually")

if userSettings["NotDetectingKeyPressPlayBack"]:
    changeSettings("NotDetectingKeyPressPlayBack")

# ------------------------------------------------------------------------------ #
#
#
#                            KEYBOARD INPUT DETECTION
#
#
# ------------------------------------------------------------------------------ #

def win32_event_filter(msg, data):
    userSettings = load(open(path.join(userSettingsPath)))
    if data.flags & 0x10:
        if playbackStatement == True and recordStatement == False:
            if userSettings["NotDetectingKeyPressPlayBack"]:
                return False
            else:
                return True
        else:
            return True

def on_press(key):
    """
    Detect key release to change buttons in the gui
    """
    global changeKey, recordStatement, playbackStatement, recordBtn, playBtn, recordSet, userSettings, specialKeyPressed, hotkeysDetection, entryToChange, hotkeyVisible
    if changeKey == True: # To print hotkeys of users in settings
        keyPressed = getKeyPressed(keyboardListener, key)
        if keyPressed not in hotkey:
            hotkey.append(keyPressed)
            keyPressed = keyPressed.replace("Key.", "").replace("_l", "").replace("_r", "").replace("_gr", "")
            hotkeyVisible.append(keyPressed.upper())
        entryToChange.configure(text=hotkeyVisible)
        if "ctrl" not in keyPressed and "alt" not in keyPressed and "shift" not in keyPressed: # If it's not a combination, then we stop
            changeSettings("Hotkeys", typeOfHotKey, None, hotkey)
            changeKey = False
            hotkeyVisible = []

    if changeKey == False and cantRec == False:
        keyPressed = getKeyPressed(keyboardListener, key)
        userSettings = load(open(path.join(userSettingsPath)))
        if keyPressed not in hotkeysDetection:
            hotkeysDetection.append(keyPressed)
        if hotkeysDetection == userSettings["Hotkeys"]["Record_Start"]:
            if recordStatement == False and playbackStatement == False:
                hotkeysDetection = []
                specialKeyPressed = False
                startRecordingAndChangeImg(False)

        if hotkeysDetection == userSettings["Hotkeys"]["Playback_Start"]:
            if recordStatement == False and playbackStatement == False and recordSet == True:
                hotkeysDetection = []
                specialKeyPressed = False
                startPlayback(False)

        if hotkeysDetection == userSettings["Hotkeys"]["Record_Stop"]:
            if recordStatement == True and playbackStatement == False:
                hotkeysDetection = []
                specialKeyPressed = False
                stopRecordingAndChangeImg(False)

        if hotkeysDetection == userSettings["Hotkeys"]["Playback_Stop"]:
            if recordStatement == False and playbackStatement == True:
                hotkeysDetection = []
                specialKeyPressed = False
                stopPlayback()


def on_release(key):
    global hotkeysDetection
    if len(hotkeysDetection) != 0:
        hotkeysDetection.pop()


# ------------------------------------------------------------------------------ #
#
#
#                               RECORD MANAGEMENTS
#
#
# ------------------------------------------------------------------------------ #


def startRecordingAndChangeImg(pressKey=True):
    """
    When this function is called, it presses for the user his keybind to start the recording if he pressed the button
    instead of his keyboard, it changes the button image
    """
    global stopBtn, recordStatement, playbackStatement
    if recordSet == True and fileAlreadySaved == False:
        wantToSave = warningPopUpSave()
        if wantToSave:
            saveMacro()
            if macroPath == None:
                return
        elif wantToSave == False:
            pass
        elif wantToSave == None:
            return
    userSettings = load(open(path.join(userSettingsPath)))
    playBtn.configure(state=DISABLED)
    if playbackStatement == False:
        recordStatement = True
        file_menu.entryconfig('Load', state=DISABLED)
        if pressKey:
            simulateKeyPress(userSettings["Hotkeys"]["Record_Start"], special_keys, keyboardControl)
        recordBtn.configure(image=stopImg, command=stopRecordingAndChangeImg)
        file_menu.entryconfig('Save', state=DISABLED)
        file_menu.entryconfig('Save as', state=DISABLED)
        file_menu.entryconfig('New', state=DISABLED)
        file_menu.entryconfig('Load', state=DISABLED)
        if userSettings["Minimization"]["When_Recording"]:
            window.withdraw()
            threading.Thread(target=showNotifWithdraw).start()


def stopRecordingAndChangeImg(pressKey=True):
    """
    When this function is called, it presses for the user his keybind to stop the recording if he pressed the button
    instead of his keyboard, it changes the button image
    """
    global recordBtn, recordStatement, recordSet
    userSettings = load(open(path.join(userSettingsPath)))
    recordStatement = False
    recordSet = True
    if pressKey:
        simulateKeyPress(userSettings["Hotkeys"]["Record_Stop"], special_keys, keyboardControl)
    recordBtn.configure(image=recordImg, command=startRecordingAndChangeImg)
    playBtn.configure(state=NORMAL)
    file_menu.entryconfig('Save', state=NORMAL, command=saveMacro)
    file_menu.entryconfig('Save as', state=NORMAL, command=saveMacroAs)
    file_menu.entryconfig('New', state=NORMAL, command=newMacro)
    file_menu.entryconfig('Load', state=NORMAL)
    if userSettings["Minimization"]["When_Recording"]:
        window.deiconify()


def startPlayback(pressKey=True):
    """
        Playback the last recorded macro or the loaded one
    """
    global playbackStatement, recordBtn, recordSet
    userSettings = load(open(path.join(userSettingsPath)))
    if userSettings["StoppedRecManually"]:
        changeSettings("StoppedRecManually")
    playBtn.configure(image=stopImg, command=stopPlayback)
    playbackStatement = True
    file_menu.entryconfig('Save', state=DISABLED)
    file_menu.entryconfig('Save as', state=DISABLED)
    file_menu.entryconfig('New', state=DISABLED)
    file_menu.entryconfig('Load', state=DISABLED)
    if pressKey:
        simulateKeyPress(userSettings["Hotkeys"]["Playback_Start"], special_keys, keyboardControl)
    recordBtn.configure(state=DISABLED)
    if userSettings["Minimization"]["When_Playing"]:
        window.withdraw()
        threading.Thread(target=showNotifWithdraw).start()

def stopPlayback():
    global playbackStatement, userSettings
    simulateKeyPress(userSettings["Hotkeys"]["Playback_Stop"], special_keys, keyboardControl)
    playbackStatement = False
    recordBtn.configure(state=NORMAL)
    playBtn.configure(image=playImg, command=startPlayback)
    file_menu.entryconfig('New', state=NORMAL)
    file_menu.entryconfig('Load', state=NORMAL)
    file_menu.entryconfig('Save', state=NORMAL)
    file_menu.entryconfig('Save as', state=NORMAL)
    userSettings = load(open(path.join(userSettingsPath)))
    if userSettings["NotDetectingKeyPressPlayBack"]:
        changeSettings("NotDetectingKeyPressPlayBack")
    if not userSettings["StoppedRecManually"]:
        if userSettings["After_Playback"]["Mode"] != "Idle":
            cleanup()
            window.quit()
            if userSettings["After_Playback"]["Mode"] == "Standy":
                os.system("rundll32.exe powrprof.dll, SetSuspendState Sleep")
            if userSettings["After_Playback"]["Mode"] == "Log off Computer":
                os.system("shutdown /l")
            if userSettings["After_Playback"]["Mode"] == "Turn off Computer":
                os.system("shutdown /s")
            if userSettings["After_Playback"]["Mode"] == "Hibernate (If activated)":
                os.system("shutdown -h")
    else:
        changeSettings("StoppedRecManually")
    if userSettings["Minimization"]["When_Playing"]:
        window.deiconify()


# ------------------------------------------------------------------------------ #
#
#
#                             RECORD FILE MANAGEMENTS
#
#
# ------------------------------------------------------------------------------ #

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


# ------------------------------------------------------------------------------ #
#
#
#                            USER SETTINGS MANAGEMENTS
#
#
# ------------------------------------------------------------------------------ #


def showNotifWithdraw():
    toast = ToastNotifier()
    toast.show_toast(
        title="PyMacroRecord minimized",
        msg="PyMacroRecord as been minimized",
        duration=1,
        icon_path="assets/logo.ico"
    )


def warningPopUpSave():
    """Just popup a window to say 'Do you want to save your record?'
    So the user don't lost his last record accidentally"""
    return messagebox.askyesnocancel("Info", "Do you want to save your record?")


def stopProgram():
    global closeWindow, macro_process
    """
        When the users want to stop the software, the macro.py in the background is terminated
        And it checks if the users did a record but did not save it
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
    """Prevents from adding letters on an Entry label"""
    if action == "1":  # Insert
        try:
            float(value_if_allowed)
            return True
        except ValueError:
            return False
    return True


def changeSpeed():
    """Gui to change the speeds record"""
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
    Label(speedWin, text="Enter Speed Number between 0.1 and 10", font=('Segoe UI', 10)).pack(side=TOP, pady=10)
    userSettings = load(open(path.join(userSettingsPath)))
    setNewSpeedInput = Entry(speedWin, width=10)
    setNewSpeedInput.insert(0, str(userSettings["Playback"]["Speed"]))
    setNewSpeedInput.pack(pady=20)
    buttonArea = Frame(speedWin)
    Button(buttonArea, text="Confirm", command=lambda: setNewSpeedNumber(setNewSpeedInput.get())).pack(side=LEFT,
                                                                                                       padx=10)
    Button(buttonArea, text="Cancel", command=speedWin.destroy).pack(side=LEFT, padx=10)
    buttonArea.pack(side=BOTTOM, pady=10)
    window.wait_window(speedWin)
    cantRec = False
    changeSettings("Cant_rec")


def setNewSpeedNumber(val):
    """Function to set the new Speed numbers and to check if the value is good"""
    try:
        if float(val) <= 0 or float(val) > 10:
            messagebox.showerror("Wrong Speed Number", "Your speed value must be between 0.1 and 10!")
        else:
            changeSettings("Playback", "Speed", None, float(val))
            speedWin.destroy()
    except ValueError:
        messagebox.showerror("Wrong Speed Number", "Your input must be a number!")


def repeatGuiSettings():
    """Gui to set amount of repeat"""
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
    userSettings = load(open(path.join(userSettingsPath)))
    repeatTimes = Spinbox(repeatGui, from_=1, to=100000000, width=7, validate="key",
                          validatecommand=(validate_cmd, "%d", "%P"))
    repeatTimes.insert(0, userSettings["Playback"]["Repeat"]["Times"])
    repeatTimes.pack(pady=20)
    buttonArea = Frame(repeatGui)
    Button(buttonArea, text="Confirm",
           command=lambda: [changeSettings("Playback", "Repeat", "Times", int(repeatTimes.get())),
                            repeatGui.destroy()]).pack(side=LEFT, padx=10)
    Button(buttonArea, text="Cancel", command=repeatGui.destroy).pack(side=LEFT, padx=10)
    buttonArea.pack(side=BOTTOM, pady=10)
    window.wait_window(repeatGui)
    cantRec = False
    changeSettings("Cant_rec")


def afterPlaybackGui():
    """Gui to set mode after playback, like shutting down computer, stuff like that"""
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
    userSettings = load(open(path.join(userSettingsPath)))
    OptionMenu(menuOptions, AfterPlaybackOption, userSettings["After_Playback"]["Mode"], *options).pack(fill="both",
                                                                                                        padx=10,
                                                                                                        pady=10)
    menuOptions.pack(fill="both", padx=5, pady=10)
    buttonArea = Frame(playBackGui)
    Button(buttonArea, text="Confirm",
           command=lambda: [changeSettings("After_Playback", "Mode", None, AfterPlaybackOption.get()),
                            playBackGui.destroy()]).pack(side=LEFT, padx=10)
    Button(buttonArea, text="Cancel", command=playBackGui.destroy).pack(side=LEFT, padx=10)
    buttonArea.pack(side=BOTTOM, pady=10)
    window.wait_window(playBackGui)
    cantRec = False
    changeSettings("Cant_rec")


def hotkeySettingsGui():
    """Gui to set up new Hotkeys"""
    global typeOfHotKey, startKey, stopKey, playbackStartKey, playbackStopKey, cantRec
    userSettings = load(open(path.join(userSettingsPath)))
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
    Button(hotkeyLine, text="Start Record", command=lambda: enableHotKeyDetection("Record_Start", startKey)).grid(row=0,
                                                                                                                  column=0,
                                                                                                                  padx=10)
    startKey = Label(hotkeyLine, text=hotkeyVisible[0], font=('Segoe UI', 12))
    startKey.grid(row=0, column=1, pady=5)

    Button(hotkeyLine, text="Stop Record", command=lambda: enableHotKeyDetection("Record_Stop", stopKey)).grid(row=1,
                                                                                                               column=0,
                                                                                                               padx=10)
    stopKey = Label(hotkeyLine, text=hotkeyVisible[1], font=('Segoe UI', 12))
    stopKey.grid(row=1, column=1, pady=5)

    Button(hotkeyLine, text="Playback Start",
           command=lambda: enableHotKeyDetection("Playback_Start", playbackStartKey)).grid(row=2, column=0, padx=10)
    playbackStartKey = Label(hotkeyLine, text=hotkeyVisible[2], font=('Segoe UI', 12))
    playbackStartKey.grid(row=2, column=1, pady=5)

    Button(hotkeyLine, text="Playback Stop",
           command=lambda: enableHotKeyDetection("Playback_Stop", playbackStopKey)).grid(row=3, column=0, padx=10)
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
    """Just enable Hotkeys detection to change them"""
    global changeKey, typeOfHotKey, hotkey, entryToChange
    changeKey = True
    typeOfHotKey = mode
    hotkey = []
    entry.configure(text="Please key")
    entryToChange = entry


# ------------------------------------------------------------------------------ #
#
#
#                             GUI (VISUAL) MANAGEMENTS
#
#
# ------------------------------------------------------------------------------ #


def aboutMeGui():
    global cantRec
    cantRec = True
    changeSettings("Cant_rec")
    aboutGui = Toplevel(window)
    w = 300
    h = 200
    aboutGui.geometry('%dx%d+%d+%d' % (w, h, x, y))
    aboutGui.title("About")
    aboutGui.grab_set()
    aboutGui.resizable(False, False)
    aboutGui.attributes("-toolwindow", 1)
    Label(aboutGui, text="Publisher: LOUDO").pack(side=TOP, pady=3)
    Label(aboutGui, text=f"Version: {version} ({versionUpToDate})").pack(side=TOP, pady=3)
    Label(aboutGui, text="Under License: Attribution-NonCommercial").pack(side=TOP, pady=3)
    Label(aboutGui, text="ShareAlike 4.0 International").pack(side=TOP, pady=3)
    Label(aboutGui, text="And... I like cats and dogs, wbu?").pack(side=TOP, pady=15)
    buttonArea = Frame(aboutGui)
    Button(buttonArea, text="Close", command=aboutGui.destroy).pack(side=LEFT, padx=10)
    buttonArea.pack(side=BOTTOM, pady=10)
    window.wait_window(aboutGui)
    cantRec = False
    changeSettings("Cant_rec")

def newVerAvailable(ver):
    global cantRec
    cantRec = True
    changeSettings("Cant_rec")
    newVerGui = Toplevel(window)
    w = 300
    h = 130
    newVerGui.geometry('%dx%d+%d+%d' % (w, h, x, y))
    newVerGui.title("New Version Available!")
    newVerGui.grab_set()
    newVerGui.resizable(False, False)
    newVerGui.attributes("-toolwindow", 1)
    Label(newVerGui, text=f"New Version {ver} available!").pack(side=TOP)
    Label(newVerGui, text="Click the button to open releases page on GitHub").pack(side=TOP)
    buttonArea = Frame(newVerGui)
    Button(buttonArea, text="Click here to view", command=lambda: OpenUrl("https://github.com/LOUDO56/macro-recorder/releases")).pack(side=LEFT, pady=10)
    Button(buttonArea, text="Close", command=newVerGui.destroy).pack(side=LEFT, padx=10)
    buttonArea.pack(side=BOTTOM, pady=10)
    window.wait_window(newVerGui)
    cantRec = False
    changeSettings("Cant_rec")

def systemTray():
    """Just to show little icon on system tray"""
    global icon
    image = Image.open("assets/logo.ico")
    menu = (
        pystray.MenuItem('Show', action=window.deiconify, default=True),
    )
    icon = pystray.Icon("name", image, "PyMacroRecord", menu)
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
window.title("PyMacroRecord")
w = 350
h = 200
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)
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
keyboardInput = BooleanVar(value=userSettings["Recordings"]["Keyboard"])
recordings_sub = Menu(options_menu, tearoff=0)
options_menu.add_cascade(label="Recordings", menu=recordings_sub)
recordings_sub.add_checkbutton(label="Mouse movement", variable=mouseMove,
                               command=lambda: changeSettings("Recordings", "Mouse_Move"))
recordings_sub.add_checkbutton(label="Mouse click", variable=mouseClick,
                               command=lambda: changeSettings("Recordings", "Mouse_Click"))
recordings_sub.add_checkbutton(label="Keyboard", variable=keyboardInput,
                               command=lambda: changeSettings("Recordings", "Keyboard"))

# Options Sub
options_sub = Menu(options_menu, tearoff=0)
options_menu.add_cascade(label="Options", menu=options_sub)
options_sub.add_command(label="Hotkeys", command=hotkeySettingsGui)

minimization_sub = Menu(options_sub, tearoff=0)
options_sub.add_cascade(label="Minimization", menu=minimization_sub)
minimization_playing = BooleanVar(value=userSettings["Minimization"]["When_Playing"])
minimization_record = BooleanVar(value=userSettings["Minimization"]["When_Recording"])
minimization_sub.add_checkbutton(label="Minimized when playing", variable=minimization_playing,
                                 command=lambda: changeSettings("Minimization", "When_Playing"))
minimization_sub.add_checkbutton(label="Minimized when recording", variable=minimization_record,
                                 command=lambda: changeSettings("Minimization", "When_Recording"))

runStartUp = BooleanVar().set(userSettings["Run_On_StartUp"])
# options_sub.add_checkbutton(label="Run on startup", variable=runStartUp, command=lambda: changeSettings("Run_On_StartUp"))
options_sub.add_command(label="After playback...", command=afterPlaybackGui)

# Help section
help_section = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Help", menu=help_section)
help_section.add_command(label="Github Page",
                         command=lambda: OpenUrl("https://github.com/LOUDO56/macro-recorder/tree/main#readme"))
help_section.add_command(label="About", command=aboutMeGui)

# Play Button
playImg = PhotoImage(file=r"assets/button/play.png")
playBtn = Button(window, image=playImg, command=startPlayback, state=DISABLED)
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

keyboardListener = keyboard.Listener(on_press=on_press, on_release=on_release, win32_event_filter=win32_event_filter)
keyboardListener.start()

validate_cmd = window.register(validate_input)

window.protocol("WM_DELETE_WINDOW", stopProgram)

Thread(target=systemTray).start()

if userSettings["Cant_rec"]:
    changeSettings("Cant_rec") # Prevents from conflicts

# Check updates
newVersion = getVer("https://pastebin.com/raw/8YAjs4Pc").text
if newVersion != version:
    versionUpToDate = "Outdated"
    newVerAvailable(newVersion)
else:
    versionUpToDate = "Up to Date"


window.mainloop()
