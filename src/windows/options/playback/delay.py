from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from windows.popup import Popup


class Delay(Popup):
    def __init__(self, parent, main_app):
        super().__init__("Delay Settings", 300, 150, parent)
        main_app.prevent_record = True
        self.settings = main_app.settings
        Label(self, text="Enter delay between repeat", font=('Segoe UI', 10)).pack(side=TOP, pady=10)
        userSettings = main_app.settings.get_config()
        setNewDelayInput = Entry(self, width=10)
        setNewDelayInput.insert(0, str(userSettings["Playback"]["Repeat"]["Delay"]))
        setNewDelayInput.pack(pady=20)
        buttonArea = Frame(self)
        Button(buttonArea, text="Confirm", command=lambda: self.setNewDelayNumber(setNewDelayInput.get())).pack(side=LEFT,
                                                                                                           padx=10)
        Button(buttonArea, text="Cancel", command=self.destroy).pack(side=LEFT, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        self.wait_window()
        main_app.prevent_record = False

    def setNewDelayNumber(self, val):
        """Function to set the new Delay numbers and to check if the value is good"""
        try:
            self.settings.change_settings("Playback", "Repeat", "Delay", float(val))
            self.destroy()
        except ValueError:
            messagebox.showerror("Wrong Speed Number", "Your input must be a number!")