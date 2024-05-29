from tkinter import *
from tkinter.ttk import *
from windows.popup import Popup


class About(Popup):
    def __init__(self, parent, main_app, version, updated):
        super().__init__(main_app.text_content["help_menu"]["about_settings"]["title"], 300, 150, parent)
        Label(self, text=f"{main_app.text_content['help_menu']['about_settings']['publisher_text']}: LOUDO").pack(
            side=TOP, pady=3)
        Label(self,
              text=f"{main_app.text_content['help_menu']['about_settings']['version_text']}: {version} ({updated})").pack(
            side=TOP, pady=3)
        Label(self,
              text=f"{main_app.text_content['help_menu']['about_settings']['license_text']}: General Public License v3.0").pack(
            side=TOP, pady=3)
        buttonArea = Frame(self)
        Button(buttonArea, text="Close", command=self.destroy).pack(side=LEFT, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        main_app.prevent_record = True
        self.wait_window()
        main_app.prevent_record = False

