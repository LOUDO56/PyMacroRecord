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
        extra_width = 0
        extra_height = 0
        if platform.lower() == "win32":
            import ctypes
            user32 = ctypes.windll.user32
            screensize = user32.GetSystemMetrics(0)
            if screensize > 2450:
                extra_width = 110
                extra_height = 50
            if screensize > 3000:
                extra_width = 200
                extra_height = 100
            if screensize > 3500:
                extra_width = 200
                extra_height = 150
        self.geometry('%dx%d+%d+%d' % (w + extra_width, h + extra_height, x, y))
        self.resizable(False, False)
        if platform == "win32":
            self.attributes("-toolwindow", 1)
        else:
            self.attributes("-topmost", 1)
        self.grab_set()

