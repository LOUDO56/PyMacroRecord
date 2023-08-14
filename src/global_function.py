from json import load, dumps
from os import path, getenv

appdata_local = getenv('LOCALAPPDATA') + "/PyMacroRecord"
appdata_local = appdata_local.replace('\\', "/")
userSettingsPath = appdata_local + "/userSettings.json"

def getKeyPressed(keyboardListener, key):
    """Return right key. canonical() prevents from weird characters to show up with ctrl active. Like ctrl + d,
    pynput will not print Key.ctrl and d, it will print Key.ctrl and a weird character"""
    if "Key." in str(key):
        keyPressed = str(key)
    else:
        keyPressed = str(keyboardListener.canonical(key)).replace("'", "")
    return keyPressed


def simulateKeyPress(keyArray, special_keys, keyboardControl):
    """Simulate keypress"""
    for keys in keyArray:
        keyToPress = keys if 'Key.' not in keys else special_keys[keys]
        keyboardControl.press(keyToPress)
    for keys in keyArray:
        keyToPress = keys if 'Key.' not in keys else special_keys[keys]
        keyboardControl.release(keyToPress)


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
    userSettings = load(open(path.join(userSettingsPath)))