from tkinter import *
from tkinter.ttk import *
from windows.popup import Popup
from webbrowser import open as OpenUrl
from utils.user_settings import UserSettings
from time import time
from sys import platform


class NewVerAvailable(Popup):
    def __init__(self, parent, version):
        width = 330
        if platform.lower() == "darwin":
            width += 110
        super().__init__("Software Update", width, 130, parent)
        parent.prevent_record = True
        Label(self, text=f"New Version {version} available!").pack(side=TOP)
        Label(self, text="Do you want to download it now?").pack(side=TOP)
        buttonArea = Frame(self)
        Button(buttonArea, text="Ignore", command=self.ignore_new_ver).pack(side=LEFT, padx=5)
        Button(buttonArea, text="Remind me later", command=self.remind_later).pack(side=LEFT, padx=5)
        Button(buttonArea, text="Download update",
               command=lambda: OpenUrl(f"https://github.com/LOUDO56/PyMacroRecord/releases/tag/v{version}")).pack(
            side=LEFT, padx=5)
        buttonArea.pack(side=BOTTOM, pady=10)
        self.wait_window()
        parent.prevent_record = False

    def remind_later(self):
        user_settings = UserSettings()
        user_settings.change_settings("Others", "Remind_new_ver_at", None, time() + 432000)  # Add 5 days
        self.destroy()

    def ignore_new_ver(self):
        user_settings = UserSettings()
        user_settings.change_settings("Others", "Remind_new_ver_at", None, time() + 5259600)  # Add 2 months
        self.destroy()
