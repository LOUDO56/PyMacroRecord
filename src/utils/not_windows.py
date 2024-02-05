from tkinter import *
from tkinter.ttk import *
from windows.popup import Popup


class NotWindows(Popup):
    def __init__(self, parent):
        super().__init__("Warning", 440, 170, parent)
        parent.prevent_record = True
        Label(
            self,
            text="You are currently running on Linux or MacOS",
            font=("Segoe UI", 10),
        ).pack(side=TOP, pady=2)
        Label(
            self,
            text="Be careful with hotkeys, conflits can happen when doing playback",
            font=("Segoe UI", 10),
        ).pack(side=TOP, pady=2)
        Label(
            self, text="It cannot be fixed on MacOS and Linux", font=("Segoe UI", 10)
        ).pack(side=TOP, pady=2)
        Label(
            self,
            text="So, choose safe Hotkeys but not one only letter.",
            font=("Segoe UI", 10),
        ).pack(side=TOP, pady=2)
        buttonArea = Frame(self)
        Button(buttonArea, text="OK", command=self.destroy).pack(side=BOTTOM, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        self.wait_window()
        parent.prevent_record = False
