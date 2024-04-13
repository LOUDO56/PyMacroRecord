from sys import platform

def getKeyPressed(keyboardListener, key):
    """Return right key. canonical() prevents from weird characters to show up with ctrl active. Like ctrl + d,
    pynput will not print Key.ctrl and d, it will print Key.ctrl and a weird character"""
    if "Key." in str(key):
        keyPressed = str(key)
    else:
        if platform.lower() == "win32":
            keyPressed_list = list(str(keyboardListener.canonical(key)))
        else:
            keyPressed_list = list(str(key))
        if keyPressed_list[0] != "<":
            keyPressed_list[0] = ""
            keyPressed_list[-1] = ""
        keyPressed = "".join(keyPressed_list)
        if platform.lower() == "darwin":
            if keyPressed == "\\x03":
                keyPressed = "Key.enter"
            if keyPressed == "\\x1b":
                keyPressed = None
        elif platform.lower() == "linux":
            if keyPressed == "'^'":
                keyPressed = "^"
    return keyPressed
