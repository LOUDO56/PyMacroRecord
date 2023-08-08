from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import Key
from keyboard import is_pressed
from json import load, dumps
from os import getenv, path
from time import sleep, time


appdata_local = getenv('LOCALAPPDATA')+"/MacroRecorder"
appdata_local = appdata_local.replace('\\', "/")

macroEvents = {"events": []} # The core of this script, it serves to store all data events, so it can be replayable or saved on a file

mouseControl = mouse.Controller()
keyboardControl = keyboard.Controller()
special_keys = {"Key.esc": Key.esc, "Key.shift": Key.shift, "Key.tab": Key.tab, "Key.caps_lock": Key.caps_lock,
                "Key.ctrl": Key.ctrl, "Key.ctrl_l": Key.ctrl_l, "Key.alt": Key.alt, "Key.cmd": Key.cmd,
                "Key.cmd_r": Key.cmd_r, "Key.alt_r": Key.alt_r, "Key.ctrl_r": Key.ctrl_r, "Key.shift_r": Key.shift_r,
                "Key.enter": Key.enter, "Key.backspace": Key.backspace, "Key.f19": Key.f19, "Key.f18": Key.f18,
                "Key.f17": Key.f17, "Key.f16": Key.f16, "Key.f15": Key.f15, "Key.f14": Key.f14, "Key.f13": Key.f13,
                "Key.media_volume_up": Key.media_volume_up, "Key.media_volume_down": Key.media_volume_down,
                "Key.media_volume_mute": Key.media_volume_mute, "Key.media_play_pause": Key.media_play_pause,
                "Key.f6": Key.f6, "Key.f5": Key.f5, "Key.right": Key.right, "Key.down": Key.down, "Key.left": Key.left,
                "Key.up": Key.up, "Key.page_up": Key.page_up, "Key.page_down": Key.page_down, "Key.home": Key.home,
                "Key.end": Key.end, "Key.delete": Key.delete, "Key.space": Key.space}
# Special keys are for on press and on release event so when the playback is on, it can press special keys without errors

record = False # Know if record is active
playback = False # Know if playback is active

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
    global start_time, playback, keyboard_listener
    if (record == False and playback == True):
        if is_pressed('escape'):
            keyboardControl.release(keyboard.Key.esc)
            playback = False
            keyboard_listener.stop()
    else:
        try:
            macroEvents["events"].append(
                {'type': 'keyboardEvent', 'key': key.char, 'timestamp': time() - start_time, 'pressed': True})
        except AttributeError:
            macroEvents["events"].append(
                {'type': 'keyboardEvent', 'key': str(key), 'timestamp': time() - start_time, 'pressed': True})
        start_time = time()


def on_release(key):
    global start_time
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
    global start_time, mouse_listener, keyboard_listener, macroEvents, record, recordLenght
    record = True
    macroEvents = {'events': []}
    start_time = time()
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    mouse_listener.start()
    keyboard_listener.start()
    print('record started')


def stopRecord():
    """
        Stop record
    """
    global macroEvents, record
    record = False
    mouse_listener.stop()
    keyboard_listener.stop()
    json_macroEvents = dumps(macroEvents, indent=4)
    open(path.join(appdata_local+"/temprecord.json"), "w").write(json_macroEvents)
    print('record stopped')


def playRec():
    """
        Playback function
        I retrieve data from temprecord to prevents conflict, like the user loaded a new record.
        Then I loop all the events, and for each event, he sleeps some time and then trigger is specific events.

        To detect the stop of playback, I don't use the detection on the While loop because it won't work,
        and if I put the for loop in a thread, the playback is incredibly slow.
    """
    global playback, keyboard_listener
    playback = True
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()
    macroEvents = load(open(path.join(appdata_local + "/temprecord.json"), "r"))
    for i in range(len(macroEvents["events"])):
        if playback == False:
            return
        sleep(macroEvents["events"][i]["timestamp"])
        if macroEvents["events"][i]["type"] == "cursorMove":
            mouseControl.position = (macroEvents["events"][i]["x"], macroEvents["events"][i]["y"])
        elif macroEvents["events"][i]["type"] == "leftClickEvent":
            if macroEvents["events"][i]["pressed"] == True:
                mouseControl.press(Button.left)
            else:
                mouseControl.release(Button.left)
        elif macroEvents["events"][i]["type"] == "rightClickEvent":
            if macroEvents["events"][i]["pressed"] == True:
                mouseControl.press(Button.right)
            else:
                mouseControl.release(Button.right)
        elif macroEvents["events"][i]["type"] == "middleClickEvent":
            if macroEvents["events"][i]["pressed"] == True:
                mouseControl.press(Button.middle)
            else:
                mouseControl.release(Button.middle)
        elif macroEvents["events"][i]["type"] == "scrollEvent":
            mouseControl.scroll(macroEvents["events"][i]["dx"], macroEvents["events"][i]["dy"])
        elif macroEvents["events"][i]["type"] == "keyboardEvent":
            keyToPress = macroEvents["events"][i]["key"] if 'Key.' not in macroEvents["events"][i]["key"] else special_keys[macroEvents["events"][i]["key"]]
            if macroEvents["events"][i]["pressed"] == True:
                keyboardControl.press(keyToPress)
            else:
                keyboardControl.release(keyToPress)
    playback = False


                
            
# While loop to detect keybind of user
while True:
    # Start Record
    if record == False and playback == False:
        if is_pressed('o'):
            keyboardControl.release('o') # I release here because for some reason sometimes startRecord is called and then right after stopRecord is called
            startRecord()
    # Play Back
    if record == False and playback == False and len(macroEvents["events"]) != 0:
        if is_pressed('p'):
            keyboardControl.release('p')
            playRec()

    # Stop Record
    if record == True and playback == False:
        if is_pressed('escape'):
            keyboardControl.release(Key.esc)
            stopRecord()

