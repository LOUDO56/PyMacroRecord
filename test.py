from pynput import keyboard
from pynput.keyboard import Key

keyinput= []

def on_press(key):
    if "Key." in str(key):
        keypress = str(key)
    else:
        keypress = keyboardLis.canonical(key)

    if keypress not in keyinput:
        keyinput.append(keypress)
    print(keyinput)


with keyboard.Listener(on_press=on_press) as keyboardLis:
    keyboardLis.join()