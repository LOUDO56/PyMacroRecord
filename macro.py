from threading import Thread
from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import Key
from json import load, dumps
from os import getenv, path
from time import sleep, time

appdata_local = getenv('LOCALAPPDATA') + "/PyMacroRecord" # Path where I store data
appdata_local = appdata_local.replace('\\', "/")
specialKeyPressed = False
macroEvents = {"events": []}  # The core of this script, it serves to store all data events, so it can be replayable or saved on a file
userSettings = load(open(path.join(appdata_local + "/userSettings.json")))

hotkeysDetection = []

mouseControl = mouse.Controller()
keyboardControl = keyboard.Controller()
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

record = False  # Know if record is active
playback = False  # Know if playback is active


# All events from mouse and keyboard when record is active
def on_move(x, y):
    global start_time
    macroEvents["events"].append({'type': 'cursorMove', 'x': x, 'y': y, 'timestamp': time() - start_time})
    start_time = time()


def on_click(x, y, button, pressed):
    global start_time
    if button == Button.left:
        macroEvents["events"].append(
            {'type': 'leftClickEvent', 'x': x, 'y': y, 'timestamp': time() - start_time, 'pressed': pressed})
    elif button == Button.right:
        macroEvents["events"].append(
            {'type': 'rightClickEvent', 'x': x, 'y': y, 'timestamp': time() - start_time, 'pressed': pressed})
    elif button == Button.middle:
        macroEvents["events"].append(
            {'type': 'middleClickEvent', 'x': x, 'y': y, 'timestamp': time() - start_time, 'pressed': pressed})
    start_time = time()


def on_scroll(x, y, dx, dy):
    global start_time
    macroEvents["events"].append({'type': 'scrollEvent', 'dx': dx, 'dy': dy, 'timestamp': time() - start_time})
    start_time = time()


def on_press(key):
    global start_time, playback, keyboard_listener, hotkeysDetection
    userSettings = load(open(path.join(appdata_local + "/userSettings.json")))
    if userSettings["Cant_rec"]:
        return
    if "Key." in str(key):
        keyPressed = str(key)
    else:
        keyPressed = str(keyboard_listener.canonical(key)).replace("'", "")
    if keyPressed not in hotkeysDetection:
        hotkeysDetection.append(keyPressed)
    if record == False and playback == False:
        if hotkeysDetection == userSettings["Hotkeys"]["Record_Start"]:
            startRecord()

        # Play Back
        if record == False and playback == False and path.exists(path.join(appdata_local + "/temprecord.json")):
            if hotkeysDetection == userSettings["Hotkeys"]["Playback_Start"]:
                hotkeysDetection = []
                Thread(target=playRec).start() # Thread to prevent hotkey not working

    if record == False and playback == True:
        if hotkeysDetection == userSettings["Hotkeys"]["Playback_Stop"]:
            hotkeysDetection = []
            playback = False

    if record == True and playback == False:
        # Stop Record
        if hotkeysDetection == userSettings["Hotkeys"]["Record_Stop"]:
            hotkeysDetection = []
            stopRecord()
        if userSettings["Recordings"]["Keyboard"]:
            try:
                macroEvents["events"].append(
                    {'type': 'keyboardEvent', 'key': key.char, 'timestamp': time() - start_time, 'pressed': True})
            except AttributeError:
                macroEvents["events"].append(
                    {'type': 'keyboardEvent', 'key': str(key), 'timestamp': time() - start_time, 'pressed': True})
            start_time = time()

def on_release(key):
    global start_time
    if len(hotkeysDetection) != 0:
        hotkeysDetection.pop()
    if record == True and playback == False:
        if userSettings["Recordings"]["Keyboard"]:
            try:
                macroEvents["events"].append(
                    {'type': 'keyboardEvent', 'key': key.char, 'timestamp': time() - start_time, 'pressed': False})
            except AttributeError:
                macroEvents["events"].append(
                    {'type': 'keyboardEvent', 'key': str(key), 'timestamp': time() - start_time, 'pressed': False})
            start_time = time()


def startRecord():
    """
        Start record
    """
    global start_time, mouse_listener, keyboard_listener, macroEvents, record, recordLenght, userSettings
    userSettings = load(open(path.join(appdata_local + "/userSettings.json")))
    record = True
    macroEvents = {'events': []}
    start_time = time()
    if userSettings["Recordings"]["Mouse_Move"] and userSettings["Recordings"]["Mouse_Click"]:
        mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    elif userSettings["Recordings"]["Mouse_Move"] and not userSettings["Recordings"]["Mouse_Click"]:
        mouse_listener = mouse.Listener(on_move=on_move, on_scroll=on_scroll)
    else:
        mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
    mouse_listener.start()


def stopRecord():
    """
        Stop record
    """
    global macroEvents, record
    record = False
    mouse_listener.stop()
    macroEvents["events"].remove(macroEvents["events"][-1])
    macroEvents["events"].remove(macroEvents["events"][-1])
    macroEvents["events"].remove(macroEvents["events"][0])
    json_macroEvents = dumps(macroEvents, indent=4)
    open(path.join(appdata_local + "/temprecord.json"), "w").write(json_macroEvents)


def playRec():
    """
        Playback function
        I retrieve data from temprecord to prevents conflict, like the user loaded a new record.
        Then I loop all the events, and for each event, he sleeps some time and then trigger is specific events.

        To detect the stop of playback, I don't use the detection on the While loop because it won't work,
        and if I put the for loop in a thread, the playback is incredibly slow.
    """
    global playback, keyboard_listener
    userSettings = load(open(path.join(appdata_local + "/userSettings.json")))
    playback = True
    macroEvents = load(open(path.join(appdata_local + "/temprecord.json"), "r"))
    for repeat in range(userSettings["Playback"]["Repeat"]["Times"]):
        for events in range(len(macroEvents["events"])):
            if playback == False:
                return
            sleep(macroEvents["events"][events]["timestamp"] * (1 / userSettings["Playback"]["Speed"]))
            if macroEvents["events"][events]["type"] == "cursorMove":
                mouseControl.position = (macroEvents["events"][events]["x"], macroEvents["events"][events]["y"])
            elif macroEvents["events"][events]["type"] == "leftClickEvent":
                mouseControl.position = (macroEvents["events"][events]["x"], macroEvents["events"][events]["y"])
                if macroEvents["events"][events]["pressed"] == True:
                    mouseControl.press(Button.left)
                else:
                    mouseControl.release(Button.left)
            elif macroEvents["events"][events]["type"] == "rightClickEvent":
                mouseControl.position = (macroEvents["events"][events]["x"], macroEvents["events"][events]["y"])
                if macroEvents["events"][events]["pressed"] == True:
                    mouseControl.press(Button.right)
                else:
                    mouseControl.release(Button.right)
            elif macroEvents["events"][events]["type"] == "middleClickEvent":
                mouseControl.position = (macroEvents["events"][events]["x"], macroEvents["events"][events]["y"])
                if macroEvents["events"][events]["pressed"] == True:
                    mouseControl.press(Button.middle)
                else:
                    mouseControl.release(Button.middle)
            elif macroEvents["events"][events]["type"] == "scrollEvent":
                mouseControl.scroll(macroEvents["events"][events]["dx"], macroEvents["events"][events]["dy"])
            elif macroEvents["events"][events]["type"] == "keyboardEvent":
                if macroEvents["events"][events]["key"] != None:
                    keyToPress = macroEvents["events"][events]["key"] if 'Key.' not in macroEvents["events"][events]["key"] else \
                    special_keys[macroEvents["events"][events]["key"]]
                    if macroEvents["events"][events]["pressed"] == True:
                        keyboardControl.press(keyToPress)
                    else:
                        keyboardControl.release(keyToPress)
    for keys in userSettings["Hotkeys"]["Playback_Stop"]:
        keyToPress = keys if 'Key.' not in keys else special_keys[keys]
        keyboardControl.press(keyToPress)
    for keys in userSettings["Hotkeys"]["Playback_Stop"]:
        keyToPress = keys if 'Key.' not in keys else special_keys[keys]
        keyboardControl.release(keyToPress)
    playback = False



with keyboard.Listener(on_press=on_press, on_release=on_release) as keyboard_listener:
    keyboard_listener.join()
