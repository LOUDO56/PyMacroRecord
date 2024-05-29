from tkinter import *
from tkinter.ttk import *
from windows.popup import Popup


class Timestamp(Popup):
    def __init__(self, parent, main_app):
        super().__init__(main_app.text_content["options_menu"]["others_menu"]["fixed_timestamp_settings"]["title"], 300, 150, parent)
        main_app.prevent_record = True
        self.settings = main_app.settings
        Label(self, text=main_app.text_content["options_menu"]["others_menu"]["fixed_timestamp_settings"]["sub_text"], font=('Segoe UI', 10)).pack(side=TOP, pady=10)
        userSettings = main_app.settings.get_config()
        fixed_timetamp = Spinbox(self, from_=0, to=100000000, width=7, validate="key",
                              validatecommand=(main_app.validate_cmd, "%d", "%P"))
        fixed_timetamp.insert(0, userSettings["Others"]["Fixed_timestamp"])
        fixed_timetamp.pack(pady=20)
        buttonArea = Frame(self)
        Button(buttonArea, text=main_app.text_content["global"]["confirm_button"],
               command=lambda: [self.settings.change_settings("Others", "Fixed_timestamp", None, float(fixed_timetamp.get())),
                                self.destroy()]).pack(side=LEFT, padx=10)
        Button(buttonArea, text=main_app.text_content["global"]["cancel_button"], command=self.destroy).pack(side=LEFT, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        self.wait_window()
        main_app.prevent_record = False

