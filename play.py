from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import Key
import time
import os
import json

appdata_local = os.getenv('LOCALAPPDATA')+"/MacroRecorder"
appdata_local = appdata_local.replace('\\', "/")


with open(os.path.join(appdata_local+"/temprecord.json")) as f:
    macroEvents = json.load(f)

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

keyboardControl.press('p')
keyboardControl.release('p')
for i in range(len(macroEvents["events"])):
    time.sleep(macroEvents["events"][i]["timestamp"])
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
        keyToPress = macroEvents["events"][i]["key"] if 'Key.' not in macroEvents["events"][i]["key"] else \
        special_keys[macroEvents["events"][i]["key"]]
        if macroEvents["events"][i]["pressed"] == True:
            keyboardControl.press(keyToPress)
        else:
            keyboardControl.release(keyToPress)


keyboardControl.press(Key.esc)
keyboardControl.release(Key.esc)