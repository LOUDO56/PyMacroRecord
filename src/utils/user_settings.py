from sys import platform
from os import path, getenv, mkdir
from json import dumps, load
from utils.version import Version


class UserSettings:
    """Class to interact with userSettings.json"""
    def __init__(self):
        self.first_time = False

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
                    "Delay": 0
                }
            },

            "Recordings": {
                "Mouse_Move": True,
                "Mouse_Click": True,
                "Keyboard": True,
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

            "Others": {
                "Check_update": True,
                "Fixed_timestamp": 0
            }
        }

        userSettings_json = dumps(userSettings, indent=4)
        with open(self.user_setting, "w") as settingFile:
            settingFile.write(userSettings_json)

    def get_config(self):
        """Get settings of users"""
        with open(self.user_setting, "r") as settingFile:
            settingFile_json = load(settingFile)
        return settingFile_json

    def update_settings(self, updatedValues):
        with open(self.user_setting, "w") as settingFile:
            settingFile.write(updatedValues)

    def get_path(self):
        return self.path_setting

    def change_settings(self, category, option=None, option2=None, newValue=None):
        """Change settings of user"""
        userSettings = self.get_config()
        if not category in userSettings:
            userSettings[category] = ""
        if newValue is None:
            if option is None:
                userSettings[category] = not userSettings[category]
            elif option2 is not None:
                userSettings[category][option][option2] = not userSettings[category][option][option2]
            else:
                userSettings[category][option] = not userSettings[category][option]

        elif option is not None and newValue is not None:
            if option2 is not None:
                userSettings[category][option][option2] = newValue
            else:
                userSettings[category][option] = newValue
        self.update_settings(dumps(userSettings, indent=4))

    def check_new_options(self):
        userSettings = self.get_config()
        if "Others" not in userSettings:
            userSettings["Others"] = {"Check_update": True}
            self.update_settings(dumps(userSettings, indent=4))
        if "Fixed_timestamp" not in userSettings["Others"]:
            userSettings["Others"]["Fixed_timestamp"] = 0
            self.update_settings(dumps(userSettings, indent=4))
        if "Delay" not in userSettings["Playback"]["Repeat"]:
            userSettings["Playback"]["Repeat"]["Delay"] = 0
            self.update_settings(dumps(userSettings, indent=4))
