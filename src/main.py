import os
from os import mkdir, remove, system, getlogin
from os import name as OsUser
from sys import platform
from threading import Thread
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
from webbrowser import open as OpenUrl
from PIL import Image
from pynput import keyboard
from pynput.keyboard import Key
from pystray import Icon
from pystray import MenuItem
from requests import get as getVer
from global_function import *
from macro import startRecord, stopRecord, playRec, stopPlayBackMacro
try:
    from win10toast import ToastNotifier
except:
    pass

version = "1.0.5"

# ------------------------------------------------------------------------------ #
#
#
#                               SETUP PART
#
#
# ------------------------------------------------------------------------------ #


if OsUser == "nt":
    windowPopupOption = "-toolwindow"
else:
    windowPopupOption = "-topmost"

special_keys = {
    "Key.esc": Key.esc, "Key.shift": Key.shift, "Key.tab": Key.tab, "Key.caps_lock": Key.caps_lock,
    "Key.ctrl": Key.ctrl, "Key.ctrl_l": Key.ctrl_l, "Key.ctrl_r": Key.ctrl_r, "Key.alt": Key.alt,
    "Key.alt_l": Key.alt_l, "Key.alt_r": Key.alt_r, "Key.cmd": Key.cmd, "Key.cmd_l": Key.cmd_l,
    "Key.cmd_r": Key.cmd_r, "Key.enter": Key.enter, "Key.backspace": Key.backspace, "Key.f19": Key.f19,
    "Key.f18": Key.f18, "Key.f17": Key.f17, "Key.f16": Key.f16, "Key.f15": Key.f15, "Key.f14": Key.f14,
    "Key.f13": Key.f13, "Key.f12": Key.f12, "Key.f11": Key.f11, "Key.f10": Key.f10,
    "Key.f9": Key.f9, "Key.f8": Key.f8, "Key.f7": Key.f7, "Key.f6": Key.f6, "Key.f5": Key.f5,
    "Key.f4": Key.f4, "Key.f3": Key.f3, "Key.f2": Key.f2, "Key.f1": Key.f1,
    "Key.media_volume_up": Key.media_volume_up, "Key.media_volume_down": Key.media_volume_down,
    "Key.media_volume_mute": Key.media_volume_mute, "Key.media_play_pause": Key.media_play_pause,
    "Key.insert": Key.insert, "Key.right": Key.right, "Key.down": Key.down, "Key.left": Key.left,
    "Key.up": Key.up, "Key.page_up": Key.page_up, "Key.page_down": Key.page_down, "Key.home": Key.home,
    "Key.end": Key.end, "Key.delete": Key.delete, "Key.space": Key.space,
    "Key.alt_gr": Key.alt_gr, "Key.menu": Key.menu, "Key.num_lock": Key.num_lock,
    "Key.pause": Key.pause, "Key.print_screen": Key.print_screen, "Key.scroll_lock": Key.scroll_lock,
    "Key.shift_l": Key.shift_l, "Key.shift_r": Key.shift_r
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
firstTime = False # KNow if the user start the file for the first time by checking if folder is creeated
hotkeyVisible = []  # For Gui visual
hotkeysDetection = []  # Detect Hotkeys
keyboardControl = keyboard.Controller()  # Keyboard controller to detect keypress

if(OsUser == "nt"):
    appdata_local = path.join(getenv("LOCALAPPDATA"), "PyMacroRecord")
else:
    appdata_local = path.join(path.expanduser("~"), "PyMacroRecord")
userSettingsPath = path.join(appdata_local, "userSettings.json")

# Prevents from playing last record not saved or saved when re-launching the software
if path.exists(path.join(appdata_local + "temprecord.json")):
    remove(path.join(appdata_local + "temprecord.json"))
# Setup of UserSettings if not exists
if path.isdir(appdata_local) == False:
    mkdir(appdata_local)
    firstTime = True
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
                "Key.f3"
            ],
        },

        "Minimization": {
            "When_Playing": False,
            "When_Recording": False,
        },

        "Run_On_StartUp": False,

        "After_Playback": {
            "Mode": "Idle"  # Quit, Lock Computer, Lof off computer, Turn off computer, Restart Computer, Standby, Hibernate
        },

        "Cant_rec": False,
        "StoppedRecManually": False,
        "NotDetectingKeyPressPlayBack": False
    }
    userSettings_json = dumps(userSettings, indent=4)
    settingFile = open(path.join(userSettingsPath), "w")
    settingFile.write(userSettings_json)
    settingFile.close()

userSettings = loadRecord()

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
    """Detect if key is pressed by real keyboard or pynput"""
    userSettings = loadRecord()
    if data.flags == 0x10:
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
    global changeKey, recordStatement, playbackStatement, recordBtn, playBtn, recordSet, userSettings, hotkeysDetection, hotkeyVisible, cantRec, hotkey
    userSettings = loadRecord()
    if changeKey == True:  # To print hotkeys of users in settings
        keyPressed = getKeyPressed(keyboardListener, key)
        if keyPressed not in hotkey:
            if "<" and ">" in keyPressed:
                try:
                    keyPressed = vk_nb[keyPressed]
                except:
                    pass
            hotkey.append(keyPressed)
            keyPressed = keyPressed.replace("Key.", "").replace("_l", "").replace("_r", "").replace("_gr", "")
            hotkeyVisible.append(keyPressed.upper())
        entryToChange.configure(text=hotkeyVisible)
        i = 0
        for hotkeyUser in userSettings["Hotkeys"]:
            if userSettings["Hotkeys"][hotkeyUser] == hotkey and indexToChange != i:
                messagebox.showerror("Error", "You cannot have the same keyboard shortcut for another category.")
                entryToChange.configure(text="Please key")
                changeKey = True
                hotkey = []
                hotkeyVisible = []
                break
            else:
                if all(keyword not in keyPressed for keyword in ["ctrl", "alt", "shift"]):
                    changeSettings("Hotkeys", typeOfHotKey, None, hotkey)
                    changeKey = False
                    hotkeyVisible = []
                    userSettings = loadRecord()
            i += 1

    if changeKey == False and cantRec == False:
        keyPressed = getKeyPressed(keyboardListener, key)
        if "<" and ">" in keyPressed:
            try:
                keyPressed = vk_nb[keyPressed]
            except:
                pass
        for keys in userSettings["Hotkeys"]:
            if userSettings["Hotkeys"][keys] == []:
                userSettings["Hotkeys"][keys] = ""
        if keyPressed not in hotkeysDetection:
            hotkeysDetection.append(keyPressed)
        if hotkeysDetection == userSettings["Hotkeys"][
            "Record_Start"] and recordStatement == False and playbackStatement == False:
            startRecordingAndChangeImg(False)
            hotkeysDetection = []

        if hotkeysDetection == userSettings["Hotkeys"][
            "Record_Stop"] and recordStatement == True and playbackStatement == False:
            stopRecordingAndChangeImg(False)

        if hotkeysDetection == userSettings["Hotkeys"][
            "Playback_Start"] and recordStatement == False and playbackStatement == False and recordSet == True:
            startPlayback(False)


        elif hotkeysDetection == userSettings["Hotkeys"][
            "Playback_Stop"] and recordStatement == False and playbackStatement == True:
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


def preventRecord(state):
    """
    Prevents from recording when in settings or file explorer to save, load a record.
    """
    global cantRec
    if state:
        cantRec = True
    else:
        cantRec = False
    changeSettings("Cant_rec")

def startRecordingAndChangeImg(pressKey=True):
    """
    When this function is called, it presses for the user his keybind to start the recording if he pressed the button
    instead of his keyboard, it changes the button image
    """
    global stopBtn, recordStatement, playbackStatement, cantRec
    if pressKey:
        if recordSet == True:
            preventRecord(True)
            wantToSave = warningPopUpSave()
            if wantToSave:
                saveMacro()
                if macroPath == None:
                    return
            elif wantToSave == False:
                pass
            elif wantToSave == None:
                preventRecord(False)
                return
            preventRecord(False)
    userSettings = loadRecord()
    playBtn.configure(state=DISABLED)
    if playbackStatement == False:
        recordStatement = True
        file_menu.entryconfig('Load', state=DISABLED)
        recordBtn.configure(image=stopImg, command=stopRecordingAndChangeImg)
        file_menu.entryconfig('Save', state=DISABLED)
        file_menu.entryconfig('Save as', state=DISABLED)
        file_menu.entryconfig('New', state=DISABLED)
        file_menu.entryconfig('Load', state=DISABLED)
        if userSettings["Minimization"]["When_Recording"]:
            window.withdraw()
            Thread(target=showNotifWithdraw).start()
        startRecord()


def stopRecordingAndChangeImg(pressKey=True):
    """
    When this function is called, it presses for the user his keybind to stop the recording if he pressed the button
    instead of his keyboard, it changes the button image
    """
    global recordBtn, recordStatement, recordSet
    userSettings = loadRecord()
    recordStatement = False
    recordSet = True
    recordBtn.configure(image=recordImg, command=startRecordingAndChangeImg)
    playBtn.configure(state=NORMAL)
    file_menu.entryconfig('Save', state=NORMAL, command=saveMacro)
    file_menu.entryconfig('Save as', state=NORMAL, command=saveMacroAs)
    file_menu.entryconfig('New', state=NORMAL, command=newMacro)
    file_menu.entryconfig('Load', state=NORMAL)
    if userSettings["Minimization"]["When_Recording"]:
        window.deiconify()
    stopRecord()

def playInterval():
    playRec()
    sleep(userSettings["Playback"]["Repeat"]["Interval"])

def startPlayback(pressKey=True):
    global playback, recBeingPlayed
    """
        Playback the last recorded macro or the loaded one
    """
    global playbackStatement, recordBtn, recordSet
    userSettings = loadRecord()
    if userSettings["StoppedRecManually"]:
        changeSettings("StoppedRecManually")
    playBtn.configure(image=stopImg, command=stopPlayback)
    playbackStatement = True
    file_menu.entryconfig('Save', state=DISABLED)
    file_menu.entryconfig('Save as', state=DISABLED)
    file_menu.entryconfig('New', state=DISABLED)
    file_menu.entryconfig('Load', state=DISABLED)
    recordBtn.configure(state=DISABLED)
    if userSettings["Minimization"]["When_Playing"]:
        window.withdraw()
        Thread(target=showNotifWithdraw).start()

    Thread(target=playRec).start()

def stopPlayback():
    global playbackStatement, userSettings
    stopPlayBackMacro()
    userSettings = loadRecord()
    playbackStatement = False
    recordBtn.configure(state=NORMAL)
    playBtn.configure(image=playImg, command=startPlayback)
    file_menu.entryconfig('New', state=NORMAL)
    file_menu.entryconfig('Load', state=NORMAL)
    file_menu.entryconfig('Save', state=NORMAL)
    file_menu.entryconfig('Save as', state=NORMAL)
    if userSettings["NotDetectingKeyPressPlayBack"]:
        changeSettings("NotDetectingKeyPressPlayBack")
    if not userSettings["StoppedRecManually"]:
        if userSettings["After_Playback"]["Mode"] != "Idle":
            icon.stop()
            if userSettings["After_Playback"]["Mode"] == "Standy":
                if OsUser == "nt":
                    system("rundll32.exe powrprof.dll, SetSuspendState 0,1,0")
                elif platform == "Linux" or "linux":
                    system("systemctl suspend")
                elif platform == "darwin" or platform == "Darwin":
                    system("pmset sleepnow")
            elif userSettings["After_Playback"]["Mode"] == "Log off Computer":
                if OsUser == "nt":
                    system("shutdown /l")
                else:
                    system("pkill -KILL -u " + getlogin())
            elif userSettings["After_Playback"]["Mode"] == "Turn off Computer":
                if OsUser == "nt":
                    system("shutdown /s /t 0")
                else:
                    system("shutdown -h now")
            elif userSettings["After_Playback"]["Mode"] == "Restart Computer":
                if OsUser == "nt":
                    system("shutdown /r /t 0")
                else:
                    system("shutdown -r now")
            elif userSettings["After_Playback"]["Mode"] == "Hibernate (If activated)":
                if OsUser == "nt":
                    system("shutdown -h")
                elif platform == "Linux" or "linux":
                    system("systemctl hibernate")
                elif platform == "darwin" or platform == "Darwin":
                    system("pmset sleepnow")
            window.quit()
            window.destroy()
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
    global macroPath, fileAlreadySaved, cantRec
    if recordStatement == False and playbackStatement == False and recordSet == True:
        if cantRec == False:
            preventRecord(True)
        macroSaved = filedialog.asksaveasfile(filetypes=[('Json Files', '*.json')], defaultextension='.json')
        if macroSaved is not None:
            macroContent = open(path.join(appdata_local + "/temprecord.json"), "r")
            macroEvents = load(macroContent)
            json_macroEvents = dumps(macroEvents, indent=4)
            fileToSave = open(macroSaved.name, "w")
            fileToSave.write(json_macroEvents)
            fileToSave.close()
            macroPath = macroSaved.name
            # macroPath serve to know where his last saved macro is, so the user can
            # overwrite it if he did a new record
            macroSaved.close()
            fileAlreadySaved = True
        preventRecord(False)


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
            macroSaved.close()
        else:
            saveMacroAs()
        if closeWindow:
            icon.stop()
            window.quit()
            window.destroy()


def loadMacro(e=None):
    """
        Load a script that the user did, to play it or overwrite it (if he saved his new record of course)
    """
    global macroPath, recordSet, fileAlreadySaved, cantRec
    preventRecord(True)
    if recordStatement == False and playbackStatement == False:
        if recordSet == True and fileAlreadySaved == False:
            wantToSave = warningPopUpSave()
            if wantToSave == None:
                preventRecord(False)
                return
            elif wantToSave:
                saveMacro()
        macroFile = filedialog.askopenfile(filetypes=[('Json Files', '*.json')], defaultextension='.json')
        if macroFile is not None:
            macroContent = open(macroFile.name)
            macroPath = macroFile.name
            macroEvents = load(macroContent)
            json_macroEvents = dumps(macroEvents, indent=4)
            temprecord = open(path.join(appdata_local + "/temprecord.json"), "w")
            temprecord.write(json_macroEvents)
            temprecord.close()
            playBtn.configure(state=NORMAL)
            file_menu.entryconfig('Save', state=NORMAL, command=saveMacro)
            file_menu.entryconfig('Save as', state=NORMAL, command=saveMacroAs)
            file_menu.entryconfig('New', state=NORMAL, command=newMacro)
            macroFile.close()
            fileAlreadySaved = True
            recordSet = False
    preventRecord(False)


def newMacro(e=None):
    """
        Load a script that the user did, to play it or overwrite it (if he saved his new record of course)
    """
    global recordSet, fileAlreadySaved
    if recordStatement == False and playbackStatement == False:
        if recordSet == True and fileAlreadySaved == False:
            preventRecord(True)
            wantToSave = warningPopUpSave()
            if wantToSave == None:
                preventRecord(True)
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
    if OsUser == "nt":
        toast = ToastNotifier()
        toast.show_toast(
            title="PyMacroRecord minimized",
            msg="PyMacroRecord has been minimized",
            duration=5,
            icon_path=resource_path(path.join("assets", "logo.ico"))
        )
    elif platform == "Linux" or platform == "linux":
        system("""notify-send -u normal "PyMacroRecord" "PyMacroRecord has been minimized" """)
    elif platform == "Darwin" or platform == "darwin":
        system("""
        osascript -e 'display notification "PyMacroRecord" with title "PyMacroRecord has been minimized" 
        """)
    else:
        pass


def warningPopUpSave():
    """Just popup a window to say 'Do you want to save your record?'
    So the user don't lost his last record accidentally"""
    return messagebox.askyesnocancel("Confirm", "Do you want to save your record?")


def stopProgram():
    """
         When the users want to stop the software, it checks if the users did a record but did not save it
     """
    global closeWindow, cantRec
    if recordSet == True and fileAlreadySaved == False:
        preventRecord(True)
        closeWindow = True
        wantToSave = warningPopUpSave()
        if wantToSave:
            saveMacro()
        elif wantToSave == False:
            icon.stop()
            window.quit()
            window.destroy()
        preventRecord(False)
    else:
        icon.stop()
        window.quit()
        window.destroy()


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
    preventRecord(True)
    speedWin = Toplevel(window)
    w = 300
    h = 150
    speedWin.geometry('%dx%d+%d+%d' % (w, h, x, y))
    speedWin.title("Change Speed")
    speedWin.grab_set()
    speedWin.resizable(False, False)
    speedWin.attributes(windowPopupOption, 1)
    Label(speedWin, text="Enter Speed Number between 0.1 and 10", font=('Segoe UI', 10)).pack(side=TOP, pady=10)
    userSettings = loadRecord()
    setNewSpeedInput = Entry(speedWin, width=10)
    setNewSpeedInput.insert(0, str(userSettings["Playback"]["Speed"]))
    setNewSpeedInput.pack(pady=20)
    buttonArea = Frame(speedWin)
    Button(buttonArea, text="Confirm", command=lambda: setNewSpeedNumber(setNewSpeedInput.get())).pack(side=LEFT,
                                                                                                       padx=10)
    Button(buttonArea, text="Cancel", command=speedWin.destroy).pack(side=LEFT, padx=10)
    buttonArea.pack(side=BOTTOM, pady=10)
    window.wait_window(speedWin)
    preventRecord(False)


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
    preventRecord(True)
    repeatGui = Toplevel(window)
    w = 300
    h = 150
    repeatGui.geometry('%dx%d+%d+%d' % (w, h, x, y))
    repeatGui.title("Change Repeat")
    repeatGui.grab_set()
    repeatGui.resizable(False, False)
    repeatGui.attributes(windowPopupOption, 1)
    Label(repeatGui, text="Enter Repeat Number ", font=('Segoe UI', 10)).pack(side=TOP, pady=10)
    userSettings = loadRecord()
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
    preventRecord(False)


def afterPlaybackGui():
    """Gui to set mode after playback, like shutting down computer, stuff like that"""
    global cantRec
    preventRecord(True)
    playBackGui = Toplevel(window)
    w = 250
    h = 150
    playBackGui.geometry('%dx%d+%d+%d' % (w, h, x, y))
    playBackGui.title("After Playback")
    playBackGui.grab_set()
    playBackGui.resizable(False, False)
    playBackGui.attributes(windowPopupOption, 1)

    options = [
        'Idle',
        'Quit Software',
        'Standy',
        'Log off Computer',
        'Turn off Computer',
        'Restart Computer',
        'Hibernate (If activated)'

    ]
    menuOptions = LabelFrame(playBackGui, text="On playback complete")
    AfterPlaybackOption = StringVar()
    userSettings = loadRecord()
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
    preventRecord(False)

def clearHotKey(type, entryToChange):
    changeSettings("Hotkeys", type, None, [])
    entryToChange.configure(text="")

def hotkeySettingsGui():
    """Gui to set up new Hotkeys"""
    global typeOfHotKey, startKey, stopKey, playbackStartKey, playbackStopKey, cantRec, changeKey
    userSettings = loadRecord()
    preventRecord(True)
    hotkeyGui = Toplevel(window)
    w = 300
    h = 200
    hotkeyGui.geometry('%dx%d+%d+%d' % (w, h, x, y))
    hotkeyGui.title("Hotkey settings")
    hotkeyGui.grab_set()
    hotkeyGui.resizable(False, False)
    hotkeyGui.attributes(windowPopupOption, 1)
    hotkeyLine = Frame(hotkeyGui)
    hotkeyStart = userSettings["Hotkeys"]["Record_Start"]
    hotkeyStop = userSettings["Hotkeys"]["Record_Stop"]
    hotkeyPlaybackStart = userSettings["Hotkeys"]["Playback_Start"]
    hotkeyPlaybackStop = userSettings["Hotkeys"]["Playback_Stop"]
    hotkeyVisible = [hotkeyStart, hotkeyStop, hotkeyPlaybackStart, hotkeyPlaybackStop]

    for i in range(len(hotkeyVisible)):
        for j in range(len(hotkeyVisible[i])):
            key = hotkeyVisible[i][j].replace("Key.", "").replace("_l", "").replace("_r", "").replace("_gr", "")
            if "<" and ">" in key:
                key = vk_nb[key]
            hotkeyVisible[i][j] = key.upper()

    Button(hotkeyLine, text="Clear", command=lambda: clearHotKey("Record_Start", startKey)).grid(row=0, column=2, padx=10)
    Button(hotkeyLine, text="Clear", command=lambda: clearHotKey("Record_Stop", stopKey)).grid(row=1, column=2, padx=10)
    Button(hotkeyLine, text="Clear", command=lambda: clearHotKey("Playback_Start", playbackStartKey)).grid(row=2, column=2, padx=10)

    Button(hotkeyLine, text="Start Record", command=lambda: enableHotKeyDetection("Record_Start", startKey, 0)).grid(row=0,
                                                                                                                  column=0,
                                                                                                                  padx=10)
    startKey = Label(hotkeyLine, text=hotkeyVisible[0], font=('Segoe UI', 12))
    startKey.grid(row=0, column=1, pady=5)

    Button(hotkeyLine, text="Stop Record", command=lambda: enableHotKeyDetection("Record_Stop", stopKey, 1)).grid(row=1,
                                                                                                               column=0,
                                                                                                               padx=10)
    stopKey = Label(hotkeyLine, text=hotkeyVisible[1], font=('Segoe UI', 12))
    stopKey.grid(row=1, column=1, pady=5)

    Button(hotkeyLine, text="Playback Start",
           command=lambda: enableHotKeyDetection("Playback_Start", playbackStartKey, 2)).grid(row=2, column=0, padx=10)
    playbackStartKey = Label(hotkeyLine, text=hotkeyVisible[2], font=('Segoe UI', 12))
    playbackStartKey.grid(row=2, column=1, pady=5)

    Button(hotkeyLine, text="Playback Stop",
           command=lambda: enableHotKeyDetection("Playback_Stop", playbackStopKey, 3)).grid(row=3, column=0, padx=10)
    playbackStopKey = Label(hotkeyLine, text=hotkeyVisible[3], font=('Segoe UI', 12))
    playbackStopKey.grid(row=3, column=1, pady=5)

    hotkeyLine.pack()

    buttonArea = Frame(hotkeyGui)
    Button(buttonArea, text="Close", command=hotkeyGui.destroy).pack(side=LEFT, padx=10)
    buttonArea.pack(side=BOTTOM, pady=10)
    window.wait_window(hotkeyGui)
    changeKey = False
    preventRecord(False)

def intervalSettingsGui():
    """
        Gui to adjust settings of interval
    """
    global intervalGui
    userSettings = loadRecord()
    preventRecord(True)
    intervalGui = Toplevel(window)
    w = 300
    h = 240
    intervalGui.geometry('%dx%d+%d+%d' % (w, h, x, y))
    intervalGui.title("Interval settings")
    intervalGui.grab_set()
    intervalGui.resizable(False, False)
    intervalGui.attributes(windowPopupOption, 1)

    hourText = Label(intervalGui, text="Hours", font=('Segoe UI', 9))
    hourText.pack(pady=10)
    hourInput = Spinbox(intervalGui, from_=0, to=24, width=10, validate="key",
                          validatecommand=(validate_cmd, "%d", "%P"))
    hourInput.insert(0, str(userSettings["Playback"]["Repeat"]["Interval"] // 3600))
    hourInput.pack()

    minText = Label(intervalGui, text="Minutes", font=('Segoe UI', 9))
    minText.pack(pady=10)
    minInput = Spinbox(intervalGui, from_=0, to=60, width=10, validate="key",
                          validatecommand=(validate_cmd, "%d", "%P"))
    minInput.insert(0, str((userSettings["Playback"]["Repeat"]["Interval"] % 3600) // 60))
    minInput.pack()

    secText = Label(intervalGui, text="Seconds", font=('Segoe UI', 9))
    secText.pack(pady=10)

    secInput = Spinbox(intervalGui, from_=0, to=60, width=10, validate="key",
                          validatecommand=(validate_cmd, "%d", "%P"))
    secInput.insert(0, str(userSettings["Playback"]["Repeat"]["Interval"] % 60))
    secInput.pack()


    buttonArea = Frame(intervalGui)
    Button(buttonArea, text="Confirm", command=lambda: setNewInterval(hourInput.get(), minInput.get(), secInput.get())).pack(side=LEFT,padx=10)
    Button(buttonArea, text="Cancel", command=intervalGui.destroy).pack(side=LEFT, padx=10)
    buttonArea.pack(side=BOTTOM, pady=10)
    window.wait_window(intervalGui)
    preventRecord(False)

def setNewInterval(hour, min, sec):
    """Set interval value, 0 to disable"""
    try:
        hour = int(hour)
        min = int(min)
        sec = int(sec)
    except:
        messagebox.showerror("Error", "You need to put numbers.")
        return
    if hour > 24 or min > 60 or sec > 60:
        causes = []
        if hour > 24:
            causes.append("Hour")
        if min > 24:
            causes.append("Minutes")
        if sec > 60:
            causes.append("Seconds")
        if len(causes) > 1:
            causeFinal = ""
            for i in range(len(causes)):
                causeFinal += causes[i]
                if i < len(causes) - 1:
                    causeFinal += ", "
            messagebox.showerror("Error", causeFinal + " input are incorrect.")
        else:
            messagebox.showerror("Error", causes[0] + " input is incorrect.")
        return

    interval = (int(hour) * 3600) + (int(min) * 60) + int(sec)
    changeSettings("Playback", "Repeat", "Interval", interval)
    intervalGui.destroy()



def enableHotKeyDetection(mode, entry, index):
    """Just enable Hotkeys detection to change them"""
    global changeKey, typeOfHotKey, hotkey, entryToChange, indexToChange
    if changeKey == False:
        changeKey = True
        typeOfHotKey = mode
        indexToChange = index
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
    preventRecord(True)
    aboutGui = Toplevel(window)
    w = 300
    h = 200
    aboutGui.geometry('%dx%d+%d+%d' % (w, h, x, y))
    aboutGui.title("About")
    aboutGui.grab_set()
    aboutGui.resizable(False, False)
    aboutGui.attributes(windowPopupOption, 1)
    Label(aboutGui, text="Publisher: LOUDO").pack(side=TOP, pady=3)
    Label(aboutGui, text=f"Version: {version} ({versionUpToDate})").pack(side=TOP, pady=3)
    Label(aboutGui, text="Under License: General Public License v3.0").pack(side=TOP, pady=3)
    Label(aboutGui, text="And... That's pretty much it!").pack(side=TOP, pady=15)
    buttonArea = Frame(aboutGui)
    Button(buttonArea, text="Close", command=aboutGui.destroy).pack(side=LEFT, padx=10)
    buttonArea.pack(side=BOTTOM, pady=10)
    window.wait_window(aboutGui)
    preventRecord(False)


def newVerAvailable(ver):
    global cantRec
    preventRecord(True)
    newVerGui = Toplevel(window)
    w = 300
    h = 130
    newVerGui.geometry('%dx%d+%d+%d' % (w, h, x, y))
    newVerGui.title("New Version Available!")
    newVerGui.grab_set()
    newVerGui.resizable(False, False)
    newVerGui.attributes(windowPopupOption, 1)
    Label(newVerGui, text=f"New Version {ver} available!").pack(side=TOP)
    Label(newVerGui, text="Click the button to open releases page on GitHub").pack(side=TOP)
    buttonArea = Frame(newVerGui)
    Button(buttonArea, text="Click here to view",
           command=lambda: OpenUrl("https://github.com/LOUDO56/macro-recorder/releases")).pack(side=LEFT, pady=10)
    Button(buttonArea, text="Close", command=newVerGui.destroy).pack(side=LEFT, padx=10)
    buttonArea.pack(side=BOTTOM, pady=10)
    window.wait_window(newVerGui)
    preventRecord(False)


def systemTray():
    """Just to show little icon on system tray"""
    global icon
    image = Image.open(resource_path(path.join("assets", "logo.ico")))
    menu = (
        MenuItem('Show', action=window.deiconify, default=True),
    )
    icon = Icon("name", image, "PyMacroRecord", menu)
    icon.run()


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

if OsUser == "nt":
    window.iconbitmap(resource_path(path.join("assets", "logo.ico")))
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
playback_sub.add_command(label="Interval", command=intervalSettingsGui)

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
options_menu.add_cascade(label="Settings", menu=options_sub)
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
help_section.add_command(label="Tutorial",
                         command=lambda: OpenUrl("https://github.com/LOUDO56/PyMacroRecord/blob/main/TUTORIAL.md"))
help_section.add_command(label="About", command=aboutMeGui)

# Play Button
playImg = PhotoImage(file=resource_path(path.join("assets", "button", "play.png")))
playBtn = Button(window, image=playImg, command=startPlayback, state=DISABLED)
playBtn.pack(side=LEFT, padx=50)

# Record Button
recordImg = PhotoImage(file=resource_path(path.join("assets", "button", "record.png")))
recordBtn = Button(window, image=recordImg, command=startRecordingAndChangeImg)
recordBtn.pack(side=RIGHT, padx=50)

# Stop Button
stopImg = PhotoImage(file=resource_path(path.join("assets", "button", "stop.png")))

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
    changeSettings("Cant_rec")  # Prevents from conflicts

def getNewVersion():
    global versionUpToDate
    try:
        newVersion = getVer("https://gist.githubusercontent.com/LOUDO56/c4a9d886031baa5d680dfd79b450f907/raw/ee2b8b31b6d8e6ba22e15d5f3bfc72b689b9aa45/gistfile1.txt", timeout=2).text
        if newVersion != version:
            versionUpToDate = "Outdated"
            newVerAvailable(newVersion)
        else:
            versionUpToDate = "Up to Date"
    except:
        versionUpToDate = "Cannot fetch if new update"

# Check updates
getNewVersion()

if firstTime:
    if OsUser != "nt":
        changeSettings("Hotkeys", "Record_Start", None, ['Key.f1'])
        changeSettings("Hotkeys", "Record_Stop", None, ['Key.f2'])
        changeSettings("Hotkeys", "Playback_Start", None, ['Key.f3'])
        changeSettings("Hotkeys", "Playback_Stop", None, ['Key.f4'])
        preventRecord(True)
        warningNotWindowsGui = Toplevel(window)
        w = 440
        h = 170
        warningNotWindowsGui.geometry('%dx%d+%d+%d' % (w, h, x, y))
        warningNotWindowsGui.title("Warning")
        warningNotWindowsGui.grab_set()
        warningNotWindowsGui.resizable(False, False)
        warningNotWindowsGui.attributes(windowPopupOption, 1)
        Label(warningNotWindowsGui, text="You are currently running on Linux or MacOS", font=('Segoe UI', 10)).pack(
            side=TOP, pady=2)
        Label(warningNotWindowsGui, text="Be careful with hotkeys, conflits can happen when doing playback",
              font=('Segoe UI', 10)).pack(side=TOP, pady=2)
        Label(warningNotWindowsGui, text="It cannot be fixed on MacOS and Linux", font=('Segoe UI', 10)).pack(side=TOP,
                                                                                                              pady=2)
        Label(warningNotWindowsGui, text="So, choose safe Hotkeys but not one only letter.", font=('Segoe UI', 10)).pack(
            side=TOP, pady=2)
        Label(warningNotWindowsGui, text="Default Hotkeys from windows have been changed to safer ones.",
              font=('Segoe UI', 10)).pack(side=TOP, pady=2)
        buttonArea = Frame(warningNotWindowsGui)
        Button(buttonArea, text="OK", command=warningNotWindowsGui.destroy).pack(side=BOTTOM, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        window.wait_window(warningNotWindowsGui)
        preventRecord(False)
window.mainloop()
