from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from windows.popup import Popup


class Interval(Popup):
    def __init__(self, parent, main_app):
        super().__init__("Interval Settings", 300, 240, parent)
        main_app.prevent_record = True
        self.settings = main_app.settings
        userSettings = main_app.settings.get_config()
        hourText = Label(self, text="Hours", font=('Segoe UI', 9))
        hourText.pack(pady=10)
        hourInput = Spinbox(self, from_=0, to=24, width=10, validate="key",
                            validatecommand=(main_app.validate_cmd, "%d", "%P"))
        hourInput.insert(0, str(userSettings["Playback"]["Repeat"]["Interval"] // 3600))
        hourInput.pack()

        minText = Label(self, text="Minutes", font=('Segoe UI', 9))
        minText.pack(pady=10)
        minInput = Spinbox(self, from_=0, to=60, width=10, validate="key",
                           validatecommand=(main_app.validate_cmd, "%d", "%P"))
        minInput.insert(0, str((userSettings["Playback"]["Repeat"]["Interval"] % 3600) // 60))
        minInput.pack()

        secText = Label(self, text="Seconds", font=('Segoe UI', 9))
        secText.pack(pady=10)

        secInput = Spinbox(self, from_=0, to=60, width=10, validate="key",
                           validatecommand=(main_app.validate_cmd, "%d", "%P"))
        secInput.insert(0, str(userSettings["Playback"]["Repeat"]["Interval"] % 60))
        secInput.pack()

        buttonArea = Frame(self)
        Button(buttonArea, text="Confirm",
               command=lambda: self.setNewInterval(hourInput.get(), minInput.get(), secInput.get())).pack(side=LEFT, padx=10)
        Button(buttonArea, text="Cancel", command=self.destroy).pack(side=LEFT, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        self.wait_window()
        main_app.prevent_record = False

    def setNewInterval(self, hour, min, sec):
        """Set interval value, 0 to disable"""
        try:
            hour = int(hour)
            min = int(min)
            sec = int(sec)
        except:
            messagebox.showerror("Error", "You need to put numbers.")
            return
        if hour > 24 or min > 60 or sec > 60:
            causes = []
            if hour > 24:
                causes.append("Hour")
            if min > 24:
                causes.append("Minutes")
            if sec > 60:
                causes.append("Seconds")
            if len(causes) > 1:
                causeFinal = ""
                for i in range(len(causes)):
                    causeFinal += causes[i]
                    if i < len(causes) - 1:
                        causeFinal += ", "
                messagebox.showerror("Error", causeFinal + " input are incorrect.")
            else:
                messagebox.showerror("Error", causes[0] + " input is incorrect.")
            return

        interval = (int(hour) * 3600) + (int(min) * 60) + int(sec)
        self.settings.change_settings("Playback", "Repeat", "Interval", interval)
        self.destroy()
