from tkinter import *
from sys import platform

class Popup(Toplevel):
    def __init__(self, name, w, h, parent):
        super().__init__(parent)
        self.title(name)
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.resizable(False, False)
        if platform == "win32":
            self.attributes("-toolwindow", 1)
        else:
            self.attributes("-topmost", 1)
        self.grab_set()

