from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from windows.popup import Popup


class Speed(Popup):
    def __init__(self, parent, main_app):
        super().__init__(main_app.text_content["options_menu"]["playback_menu"]["speed_settings"]["title"], 300, 150, parent)
        main_app.prevent_record = True
        self.settings = main_app.settings
        Label(self, text=main_app.text_content["options_menu"]["playback_menu"]["speed_settings"]["sub_text"], font=('Segoe UI', 10)).pack(side=TOP, pady=10)
        userSettings = main_app.settings.get_config()
        setNewSpeedInput = Spinbox(self, from_=0.1, to=10, width=7, validate="key",
                              validatecommand=(main_app.validate_cmd, "%d", "%P"))
        setNewSpeedInput.insert(0, str(userSettings["Playback"]["Speed"]))
        setNewSpeedInput.pack(pady=20)
        buttonArea = Frame(self)
        Button(buttonArea, text=main_app.text_content["global"]["confirm_button"], command=lambda: self.setNewSpeedNumber(setNewSpeedInput.get(), main_app)).pack(side=LEFT,
                                                                                                           padx=10)
        Button(buttonArea, text=main_app.text_content["global"]["cancel_button"], command=self.destroy).pack(side=LEFT, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        self.wait_window()
        main_app.prevent_record = False

    def setNewSpeedNumber(self, val, main_app):
        """Function to set the new Speed numbers and to check if the value is good"""
        if float(val) <= 0 or float(val) > 10:
            messagebox.showerror(main_app.text_content["global"]["error"], main_app.text_content["options_menu"]["playback_menu"]["speed_settings"]["error_new_value"])
        else:
            self.settings.change_settings("Playback", "Speed", None, float(val))
            self.destroy()