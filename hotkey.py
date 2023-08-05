from pynput import keyboard
from macro import startRecord, stopRecord, playRec
keyboardControl = keyboard.Controller()



def on_press(key):
    if key.char == "2":
        key
    if key.char == "3":
        playRec()


keyboard_listener = keyboard.Listener(on_release=on_release)

with keyboard_listener:
    keyboard_listener.join()



