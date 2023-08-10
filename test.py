from tkinter import *

root = Tk()
root.geometry("300x300")

changing = False

def hotkeyChange ():
    global changing
    changing = True
    changeBtn.configure(text = "press a key", state = DISABLED)

changeBtn = Button(root, text = "change Hotkey", command = hotkeyChange)
changeBtn.pack()

lbl = Label(root, text = "No Hotkey")
lbl.pack()

hotkey = None


def changeHotkey(event):
    global hotkey
    global changing
    if changing:
        hotkey = event.keysym
        lbl.configure(text = str(hotkey))
        changeBtn.configure(state = NORMAL, text = "change Hotkey")
        changing = False
    elif event.keysym == hotkey:
        print("Hotkey was pressed")
root.bind_all("<Key>", changeHotkey)
root.mainloop()