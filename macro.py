import pyautogui
from keyboard import is_pressed
from pynput import mouse, keyboard
from pynput.mouse import Button
import time
import threading
import json
import os


macroName = input("Quelle nom tu veux donner a ton record: ")

macroEvents = {'events':[]}
mouseControl = mouse.Controller()
keyboardControl = keyboard.Controller()

def on_move(x, y):
    global start_time
    macroEvents["events"].append({'type': 'cursorMove', 'x': x, 'y': y, 'timestamp': time.time() - start_time})
    start_time = time.time()

def on_click(x, y, button, pressed):
    global start_time
    if button == Button.left:
        macroEvents["events"].append({'type': 'leftClickEvent', 'x': x, 'y': y, 'timestamp': time.time() - start_time, 'pressed': pressed})
    elif button == Button.right:
        macroEvents["events"].append({'type': 'rightClickEvent', 'x': x, 'y': y, 'timestamp': time.time() - start_time, 'pressed': pressed})
    elif button == Button.middle:
        macroEvents["events"].append({'type': 'middleClickEvent', 'x': x, 'y': y, 'timestamp': time.time() - start_time, 'pressed': pressed})
    start_time = time.time()

def on_scroll(x, y, dx, dy):
    global start_time
    macroEvents["events"].append({'type': 'scrollEvent', 'dx': dx, 'dy': dy, 'timestamp': time.time() - start_time})
    start_time = time.time()


def on_press(key):
    global start_time
    try:
        macroEvents["events"].append({'type': 'keyboardEvent', 'key': key.char, 'timestamp': time.time() - start_time, 'pressed': True})
    except AttributeError:
        macroEvents["events"].append({'type': 'keyboardEvent', 'key': str(key), 'timestamp': time.time() - start_time, 'pressed': True})
    start_time = time.time()

def on_release(key):
    global start_time
    try:
        macroEvents["events"].append({'type': 'keyboardEvent', 'key': key.char, 'timestamp': time.time() - start_time, 'pressed': False})
    except AttributeError:
        macroEvents["events"].append({'type': 'keyboardEvent', 'key': str(key), 'timestamp': time.time() - start_time, 'pressed': False})
    start_time = time.time()

def detectStop():
    global record
    while record:
        if is_pressed('s'):
            mouse_listener.stop()
            keyboard_listener.stop()
            record = False


time.sleep(1)
print('enrengistrement lancÃ©')
record = True
start_time = time.time()
mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

with mouse_listener, keyboard_listener:
    detectStop()
    mouse_listener.join()
    keyboard_listener.join()


print('record fini')
json_macroEvents = json.dumps(macroEvents, indent=4)

with open(os.path.join("C:/Users/Lucas/Desktop/rien/data", macroName+".json"),"w") as macroRecord:
    macroRecord.write(json_macroEvents)