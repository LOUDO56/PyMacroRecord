from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from windows.popup import Popup


class Speed(Popup):
    def __init__(self, parent, main_app):
        super().__init__("Speed Settings", 300, 150, parent)
        main_app.prevent_record = True
        self.settings = main_app.settings
        Label(self, text="Enter Speed Number between 0.1 and 10", font=('Segoe UI', 10)).pack(side=TOP, pady=10)
        userSettings = main_app.settings.get_config()
        setNewSpeedInput = Entry(self, width=10)
        setNewSpeedInput.insert(0, str(userSettings["Playback"]["Speed"]))
        setNewSpeedInput.pack(pady=20)
        buttonArea = Frame(self)
        Button(buttonArea, text="Confirm", command=lambda: self.setNewSpeedNumber(setNewSpeedInput.get())).pack(side=LEFT,
                                                                                                           padx=10)
        Button(buttonArea, text="Cancel", command=self.destroy).pack(side=LEFT, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        self.wait_window()
        main_app.prevent_record = False

    def setNewSpeedNumber(self, val):
        """Function to set the new Speed numbers and to check if the value is good"""
        try:
            if float(val) <= 0 or float(val) > 10:
                messagebox.showerror("Wrong Speed Number", "Your speed value must be between 0.1 and 10!")
            else:
                self.settings.change_settings("Playback", "Speed", None, float(val))
                self.destroy()
        except ValueError:
            messagebox.showerror("Wrong Speed Number", "Your input must be a number!")