from tkinter import *
from tkinter.ttk import *
from windows.popup import Popup
from webbrowser import open as OpenUrl
from utils.user_settings import UserSettings
from time import time
from sys import platform


class NewVerAvailable(Popup):
    def __init__(self, main_app, version):
        width = 330
        if platform.lower() == "darwin":
            width += 110
        super().__init__(main_app.text_content["new_version"]["title"], width, 130, main_app)
        self.main_app = main_app
        self.main_app.prevent_record = True
        Label(self, text=f'{main_app.text_content["new_version"]["sub_text_1"]} {version} {main_app.text_content["new_version"]["sub_text_2"]}').pack(side=TOP)
        Label(self, text=main_app.text_content["new_version"]["sub_text_3"]).pack(side=TOP)
        buttonArea = Frame(self)
        Button(buttonArea, text=main_app.text_content["new_version"]["ignore_button"], command=self.ignore_new_ver).pack(side=LEFT, padx=5)
        Button(buttonArea, text=main_app.text_content["new_version"]["remind_later_button"], command=self.remind_later).pack(side=LEFT, padx=5)
        Button(buttonArea, text=main_app.text_content["new_version"]["download_button"],
               command=lambda: OpenUrl(f"https://github.com/LOUDO56/PyMacroRecord/releases/tag/v{version}")).pack(
            side=LEFT, padx=5)
        buttonArea.pack(side=BOTTOM, pady=10)
        self.wait_window()
        self.main_app.prevent_record = False

    def remind_later(self):
        user_settings = UserSettings(self.main_app)
        user_settings.change_settings("Others", "Remind_new_ver_at", None, time() + 432000)  # Add 5 days
        self.destroy()

    def ignore_new_ver(self):
        user_settings = UserSettings(self.main_app)
        user_settings.change_settings("Others", "Remind_new_ver_at", None, time() + 5259600)  # Add 2 months
        self.destroy()
