from tkinter import *
from tkinter.ttk import *
from windows.popup import Popup


class About(Popup):
    def __init__(self, parent, main_app, version, updated):
        super().__init__("About", 300, 200, parent)
        Label(self, text="Publisher: LOUDO").pack(side=TOP, pady=3)
        Label(self, text=f"Version: {version} ({updated})").pack(side=TOP, pady=3)
        Label(self, text="Under License: General Public License v3.0").pack(side=TOP, pady=3)
        Label(self, text="And... That's pretty much it!").pack(side=TOP, pady=15)
        buttonArea = Frame(self)
        Button(buttonArea, text="Close", command=self.destroy).pack(side=LEFT, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        main_app.prevent_record = True
        self.wait_window()
        main_app.prevent_record = False
