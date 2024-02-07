from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from windows.popup import Popup


class Repeat(Popup):
    def __init__(self, parent, main_app):
        super().__init__("Repeat Settings", 300, 150, parent)
        main_app.prevent_record = True
        self.settings = main_app.settings
        Label(self, text="Enter Repeat Number ", font=('Segoe UI', 10)).pack(side=TOP, pady=10)
        userSettings = main_app.settings.get_config()
        repeatTimes = Spinbox(self, from_=1, to=100000000, width=7, validate="key",
                              validatecommand=(main_app.validate_cmd, "%d", "%P"))
        repeatTimes.insert(0, userSettings["Playback"]["Repeat"]["Times"])
        repeatTimes.pack(pady=20)
        buttonArea = Frame(self)
        Button(buttonArea, text="Confirm",
               command=lambda: self.setNewRepeat(int(repeatTimes.get()))).pack(side=LEFT, padx=10)
        Button(buttonArea, text="Cancel", command=self.destroy).pack(side=LEFT, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        self.wait_window()
        main_app.prevent_record = False

    def setNewRepeat(self, newValue):
        if newValue <= 0:
            messagebox.showerror("Error", "You cannot have less than 1 repetition.")
        else:
            self.settings.change_settings("Playback", "Repeat", "Times", newValue)
            self.destroy()


