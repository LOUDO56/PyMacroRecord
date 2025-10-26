from tkinter import BOTTOM, TOP
from tkinter.ttk import Button, Frame, Label

from windows.popup import Popup


class NotWindows(Popup):
    def __init__(self, parent):
        super().__init__("Warning", 440, 170, parent)
        parent.prevent_record = True
        Label(
            self,
            text=parent.text_content["global"]["mac_linux_run"],
            font=("Segoe UI", 10),
        ).pack(side=TOP, pady=2)
        Label(
            self,
            text=parent.text_content["global"]["hotkeys_warning"],
            font=("Segoe UI", 10),
        ).pack(side=TOP, pady=2)
        Label(
            self,
            text=parent.text_content["global"]["not_fix_mac_linux"],
            font=("Segoe UI", 10),
        ).pack(side=TOP, pady=2)
        Label(
            self,
            text=parent.text_content["global"]["choose_safe_hotkeys"],
            font=("Segoe UI", 10),
        ).pack(side=TOP, pady=2)
        buttonArea = Frame(self)
        Button(buttonArea, text="OK", command=self.destroy).pack(side=BOTTOM, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        self.wait_window()
        parent.prevent_record = False
