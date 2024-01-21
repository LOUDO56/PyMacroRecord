from time import sleep
from json import load, dumps, decoder
from os import path, getenv
from os import name as OsUser
import sys

if(OsUser == "nt"):
    appdata_local = path.join(getenv("LOCALAPPDATA"), "PyMacroRecord")
else:
    appdata_local = path.join(path.expanduser("~"), "PyMacroRecord")
userSettingsPath = path.join(appdata_local, "userSettings.json")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")
    return path.join(base_path, relative_path)

def simulateKeyPress(keyArray, special_keys, keyboardControl):
    """Simulate keypress"""
    for keys in keyArray:
        keyToPress = keys if 'Key.' not in keys else special_keys[keys]
        keyboardControl.press(keyToPress)
    for keys in keyArray:
        keyToPress = keys if 'Key.' not in keys else special_keys[keys]
        keyboardControl.release(keyToPress)

def getKeyPressed(keyboardListener, key):
    """Return right key. canonical() prevents from weird characters to show up with ctrl active. Like ctrl + d,
    pynput will not print Key.ctrl and d, it will print Key.ctrl and a weird character"""
    if "Key." in str(key):
        keyPressed = str(key)
    else:
        keyPressed = str(keyboardListener.canonical(key)).replace("'", "")
    return keyPressed



def changeSettings(category, option=None, option2=None, newValue=None):
    """Change settings of user"""
    userSettings = load(open(path.join(userSettingsPath)))
    if not category in userSettings:
        userSettings[category] = ""
    if newValue is None:
        if option is None:
            userSettings[category] = not userSettings[category]
        elif option2 is not None:
            userSettings[category][option][option2] = not userSettings[category][option][option2]
        else:
            userSettings[category][option] = not userSettings[category][option]

    elif option is not None and newValue is not None:
        if option2 is not None:
            userSettings[category][option][option2] = newValue
        else:
            userSettings[category][option] = newValue
    userSettings_json = dumps(userSettings, indent=4)
    open(path.join(userSettingsPath), "w").write(userSettings_json)

def loadRecord():
    try:
        return load(open(path.join(userSettingsPath)))
    except decoder.JSONDecodeError as e:
        sleep(0.2)
        return load(open(path.join(userSettingsPath)))
