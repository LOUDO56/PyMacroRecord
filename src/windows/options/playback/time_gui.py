from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from windows.popup import Popup


class TimeGui(Popup):
    def __init__(self, parent, main_app, type):
        height = 280
        if type == "Scheduled":
            height = 310
        super().__init__(main_app.text_content["options_menu"]["playback_menu"][f"{type.lower()}_settings"]["title"], 300, height, parent)
        main_app.prevent_record = True
        self.settings = main_app.settings
        userSettings = main_app.settings.get_config()
        self.time_string = userSettings["Time_string"]
        self.time_format = userSettings["Time_format"]
        self.type = type
        if self.type == "Interval":
            value = userSettings["Playback"]["Repeat"]["Interval"]
        elif self.type == "For":
            value = userSettings["Playback"]["Repeat"]["For"]
        elif self.type == "Scheduled":
            value = userSettings["Playback"]["Repeat"]["Scheduled"]
        hourFrame = Frame(self)
        if self.type == "Scheduled":
            self.buttonTimeFormat = Button(hourFrame, text=self.time_format, command=self.changeTimeFormat)
            self.buttonTimeFormat.pack(pady=5)
        hourText = Label(hourFrame, text=main_app.text_content["options_menu"]["playback_menu"]["for_interval_settings"]["hours_text"], font=("Segoe UI", 9))
        hourText.pack(pady=10)
        hourInput = Spinbox(
            hourFrame,
            from_=0,
            to=24,
            width=10,
            validate="key",
            validatecommand=(main_app.validate_cmd, "%d", "%P"),
        )
        hourValue = str(value // 3600)
        if self.type == "Scheduled" and self.time_format == "12 hours"  and self.time_string == "PM" and int(hourValue) >= 12:
            hourInput.insert(0, int(hourValue) - 12)
        else:
            hourInput.insert(0, hourValue)

        hourInput.pack()

        self.buttonAmPm = Button(hourFrame, text=self.time_string, command=self.changeAmPm)
        if self.type == "Scheduled" and self.time_format == "12 hours":
            self.buttonAmPm.pack(pady=5)

        hourFrame.pack()

        minText = Label(self, text=main_app.text_content["options_menu"]["playback_menu"]["for_interval_settings"]["minutes_text"], font=("Segoe UI", 9))
        minText.pack(pady=10)
        minInput = Spinbox(
            self,
            from_=0,
            to=60,
            width=10,
            validate="key",
            validatecommand=(main_app.validate_cmd, "%d", "%P"),
        )
        minInput.insert(
            0, str((value % 3600) // 60)
        )
        minInput.pack()

        secText = Label(self, text=main_app.text_content["options_menu"]["playback_menu"]["for_interval_settings"]["seconds_text"], font=("Segoe UI", 9))
        secText.pack(pady=10)

        secInput = Spinbox(
            self,
            from_=0,
            to=60,
            width=10,
            validate="key",
            validatecommand=(main_app.validate_cmd, "%d", "%P"),
        )
        secInput.insert(0, str(value % 60))
        secInput.pack()

        buttonArea = Frame(self)
        Button(
            buttonArea,
            text=main_app.text_content["global"]["confirm_button"],
            command=lambda: self.setNewFixedHour(
                hourInput.get(), minInput.get(), secInput.get(), main_app
            ),
        ).pack(side=LEFT, padx=10)
        Button(buttonArea, text=main_app.text_content["global"]["cancel_button"], command=self.destroy).pack(side=LEFT, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        self.wait_window()
        main_app.prevent_record = False

    def changeAmPm(self):
        if self.time_string == "AM":
            self.time_string = "PM"
            self.buttonAmPm.configure(text="PM")
            self.settings.change_settings("Time_string", None, None, "PM")
        else:
            self.time_string = "AM"
            self.buttonAmPm.configure(text="AM")
            self.settings.change_settings("Time_string", None, None, "AM")


    def changeTimeFormat(self):
        if self.time_format == "12 hours":
            self.time_format = "24 hours"
            self.buttonTimeFormat.configure(text="24 hours")
            self.settings.change_settings("Time_format", None, None, "24 hours")
            self.buttonAmPm.pack_forget()

        else:
            self.time_format = "12 hours"
            self.buttonTimeFormat.configure(text="12 hours")
            self.settings.change_settings("Time_format", None, None, "12 hours")
            self.buttonAmPm.pack(pady=5)

    def setNewFixedHour(self, hour, min, sec, main_app):
        """Set interval value, 0 to disable"""
        hour = int(hour)
        min = int(min)
        sec = int(sec)
        hourCondition = (hour > 24 and self.time_format == "24 hours" or hour > 12 and self.time_format == "12 hours")
        if hourCondition or min > 60 or sec > 60:
            causes = []
            if hourCondition:
                causes.append(main_app.text_content["options_menu"]["playback_menu"]["for_interval_settings"]["hours_text"])
            if min > 60:
                causes.append(main_app.text_content["options_menu"]["playback_menu"]["for_interval_settings"]["minutes_text"])
            if sec > 60:
                causes.append(main_app.text_content["options_menu"]["playback_menu"]["for_interval_settings"]["seconds_text"])
            if len(causes) > 1:
                causeFinal = ""
                for i in range(len(causes)):
                    causeFinal += causes[i]
                    if i < len(causes) - 1:
                        causeFinal += ", "
                messagebox.showerror("Error", f'{causeFinal} {main_app.text_content["options_menu"]["playback_menu"]["for_interval_settings"]["error_new_value_multiple"]}')
            else:
                messagebox.showerror("Error", f'{causes[0]} {main_app.text_content["options_menu"]["playback_menu"]["for_interval_settings"]["error_new_value_single"]}')
            return
        if self.type != "Interval" and self.time_string == "PM" and self.time_format == "12 hours":
            hour += 12
        total_sec = hour * 3600 + min * 60 + sec
        if self.type == "Interval":
            self.settings.change_settings("Playback", "Repeat", "Interval", total_sec)
        elif self.type == "For":
            self.settings.change_settings("Playback", "Repeat", "For", total_sec)
        elif self.type == "Scheduled":
            self.settings.change_settings("Playback", "Repeat", "Scheduled", total_sec)
        self.destroy()
