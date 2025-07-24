from json import dumps, load
from os import path, getenv, mkdir
from sys import platform
from tkinter import messagebox
from tkinter.constants import BOTTOM, X


class UserSettings:
    """Class to interact with userSettings.json"""
    def __init__(self, main_app):
        self.first_time = False
        self.main_app = main_app

        if platform == "win32":
            self.path_setting = path.join(getenv("LOCALAPPDATA"), "PyMacroRecord")
        elif "linux" in platform.lower():
            self.path_setting = path.join(path.expanduser("~"), ".config", "PyMacroRecord")
        elif "darwin" in platform.lower():
            self.path_setting = path.join(path.expanduser("~"), "Library", "Application Support", "PyMacroRecord")

        self.user_setting = path.join(self.path_setting, "userSettings.json")

        if not path.isdir(self.path_setting) or not path.isfile(self.user_setting):
            self.first_time = True
            self.init_settings()

        self.settings_dict = self.__get_config()
        self.check_new_options()

    def init_settings(self):
        """
        Init the settings in Appdata file in windows or user directory
        in Linux and macOS if it doesn't exist.
        """
        if not path.isdir(self.path_setting):
            mkdir(self.path_setting)

        userSettings = {
            "Playback": {
                "Speed": 1,
                "Repeat": {
                    "Times": 1,
                    "For": 0,
                    "Interval": 0,
                    "Delay": 0,
                    "Scheduled": 0,
                    "Infinite": False,
                }
            },

            "Recordings": {
                "Mouse_Move": True,
                "Mouse_Click": True,
                "Keyboard": True,
                "Show_Events_On_Status_Bar": False,
            },

            "Saving": {
                "Compact_json": True
            },
            "Loading": {
                "Always_import_macro_settings": False
            },

            "Hotkeys": {
                "Record_Start": [],
                "Record_Stop": [],
                "Playback_Start": [],
                "Playback_Stop": [
                    "Key.f3"
                ],
            },

            "Minimization": {
                "When_Playing": False,
                "When_Recording": False,
            },

            "Run_On_StartUp": False,

            "After_Playback": {
                "Mode": "Idle"
                # Quit, Lock Computer, Lof off computer, Turn off computer, Restart Computer, Standby, Hibernate
            },

            "Language": "en",
            "Time_string": "PM",
            "Time_format": "12 hours",

            "Others": {
                "Check_update": True,
                "Fixed_timestamp": 0,
                "Remind_new_ver_at": 0,
            }
        }

        userSettings_json = dumps(userSettings, indent=4)
        with open(self.user_setting, "w") as settingFile:
            settingFile.write(userSettings_json)

    def __get_config(self):
        """Get settings of users"""
        with open(self.user_setting, "r") as settingFile:
            settingFile_json = load(settingFile)
        return settingFile_json

    def update_settings(self):
        with open(self.user_setting, "w") as settingFile:
            settingFile.write(dumps(self.settings_dict, indent=4))

    def reset_settings(self):
        if messagebox.askyesno(self.main_app.text_content["global"]["confirm"], self.main_app.text_content["options_menu"]["others_menu"]["reset_settings_confirmation"]):
            self.init_settings()

    def get_path(self):
        return self.path_setting

    def change_settings(self, category, option=None, option2=None, newValue=None):
        """Change settings of user"""
        if option == "Show_Events_On_Status_Bar":
            if self.settings_dict[category][option]:
                self.main_app.status_text.pack_forget()
            else:
                self.main_app.status_text.pack(side=BOTTOM, fill=X)
        if not category in self.settings_dict:
            self.settings_dict[category] = ""
        if newValue is None:
            if option is None:
                self.settings_dict[category] = not self.settings_dict[category]
            elif option2 is not None:
                self.settings_dict[category][option][option2] = not self.settings_dict[category][option][option2]
            else:
                self.settings_dict[category][option] = not self.settings_dict[category][option]

        elif option is not None and newValue is not None:
            if option2 is not None:
                self.settings_dict[category][option][option2] = newValue
            else:
                self.settings_dict[category][option] = newValue
        elif option is None and option2 is None:
            self.settings_dict[category] = newValue
        self.update_settings()

    def check_new_options(self):
        userSettings = self.settings_dict
        if "Others" not in userSettings:
            userSettings["Others"] = {"Check_update": True}
        if "Fixed_timestamp" not in userSettings["Others"]:
            userSettings["Others"]["Fixed_timestamp"] = 0
        if "Delay" not in userSettings["Playback"]["Repeat"]:
            userSettings["Playback"]["Repeat"]["Delay"] = 0
        if "Remind_new_ver_at" not in userSettings["Others"]:
            userSettings["Others"]["Remind_new_ver_at"] = 0
        if "Language" not in userSettings:
            userSettings["Language"] = "en"
        if "Saving" not in userSettings:
            userSettings["Saving"] = {"Compact_json": True}
        if "Scheduled" not in userSettings["Playback"]["Repeat"]:
            userSettings["Playback"]["Repeat"]["Scheduled"] = 0
        if "Time_string" not in userSettings:
            userSettings["Time_string"] = "12 hours"
        if "Time_format" not in userSettings:
            userSettings["Time_format"] = "PM"
        if "Infinite" not in userSettings["Playback"]["Repeat"]:
            userSettings["Playback"]["Repeat"]["Infinite"] = False
        if "Show_Events_On_Status_Bar" not in userSettings["Recordings"]:
            userSettings["Recordings"]["Show_Events_On_Status_Bar"] = False
        if "Loading" not in userSettings:
            userSettings["Loading"] = {}
            if "Always_import_macro_settings" not in userSettings["Loading"]:
                userSettings["Loading"]["Always_import_macro_settings"] = False
        self.update_settings()
