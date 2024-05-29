from pynput import keyboard
from utils.get_key_pressed import getKeyPressed
from tkinter import messagebox
from utils.keys import vk_nb


class HotkeysManager:
    def __init__(self, main_app):
        self.keyboard_listener = keyboard.Listener(
            on_press=self.__on_press,
            on_release=self.__on_release,
            win32_event_filter=self.__win32_event_filter,
        )
        self.main_app = main_app
        self.settings = main_app.settings
        self.hotkeys = []
        self.hotkey_visible = []
        self.hotkey_detection = []
        self.macro = main_app.macro
        self.hotkey_button = None
        self.type_of_hotkey = None
        self.entry_to_change = None
        self.changeKey = False
        self.index_to_change = 0
        self.keyboard_listener.start()

    def enableHotKeyDetection(self, type_of_hotkey, entry_to_change, index):
        self.hotkey_button = entry_to_change
        self.type_of_hotkey = type_of_hotkey
        self.index_to_change = index
        self.changeKey = True
        self.entry_to_change = entry_to_change
        self.entry_to_change.configure(text=self.main_app.text_content["options_menu"]["settings_menu"]["hotkeys_settings"]["please_key_text"])

    def clearHotKey(self, type, entry_to_change):
        self.settings.change_settings("Hotkeys", type, None, [])
        entry_to_change.configure(text="")

    def __win32_event_filter(self, msg, data):
        """Detect if key is pressed by real keyboard or pynput"""
        if data.flags == 0x10:
            if self.macro.playback == True and self.macro.record == False:
                return False
            else:
                return True

    def __on_press(self, key):
        userSettings = self.settings.get_config()
        if self.changeKey == True:
            keyPressed = getKeyPressed(self.keyboard_listener, key)
            if keyPressed not in self.hotkeys:
                if ">" in keyPressed:
                    try:
                        keyPressed = vk_nb[keyPressed]
                    except:
                        pass
                self.hotkeys.append(keyPressed)
                keyPressed = (
                    keyPressed.replace("Key.", "")
                    .replace("_l", "")
                    .replace("_r", "")
                    .replace("_gr", "")
                )
                self.hotkey_visible.append(keyPressed.upper())
            self.hotkey_button.configure(text=self.hotkey_visible)

            if all(keyword not in keyPressed for keyword in ["ctrl", "alt", "shift", 'cmd']):
                if (
                    self.type_of_hotkey == "Record_Start"
                    and userSettings["Hotkeys"]["Playback_Start"] == self.hotkeys
                    or self.type_of_hotkey == "Playback_Start"
                    and userSettings["Hotkeys"]["Record_Start"] == self.hotkeys
                ):
                    messagebox.showerror(
                        self.main_app.text_content["global"]["error"],
                        self.main_app.text_content["options_menu"]["settings_menu"]["hotkeys_settings"]["error_hotkeys"],
                    )
                    self.entry_to_change.configure(text=self.main_app.text_content["options_menu"]["settings_menu"]["hotkeys_settings"]["please_key_text"])
                    self.hotkeys = []
                    self.hotkey_visible = []
                    return
                self.settings.change_settings(
                    "Hotkeys", self.type_of_hotkey, None, self.hotkeys
                )
                self.changeKey = False
                self.hotkeys = []
                self.hotkey_visible = []

        if self.changeKey == False and self.main_app.prevent_record == False:
            keyPressed = getKeyPressed(self.keyboard_listener, key)
            if ">" in keyPressed:
                try:
                    keyPressed = vk_nb[keyPressed]
                except:
                    pass
            for keys in userSettings["Hotkeys"]:
                if userSettings["Hotkeys"][keys] == []:
                    userSettings["Hotkeys"][keys] = ""
            if keyPressed not in self.hotkey_detection:
                self.hotkey_detection.append(keyPressed)
            by_hotkey = True
            if (
                self.hotkey_detection == userSettings["Hotkeys"]["Record_Start"]
                and self.macro.record == False
                and self.macro.playback == False
            ):
                self.macro.start_record(by_hotkey)

            elif (
                self.hotkey_detection == userSettings["Hotkeys"]["Record_Stop"]
                and self.macro.record == True
                and self.macro.playback == False
            ):
                self.macro.stop_record()

            elif (
                self.hotkey_detection == userSettings["Hotkeys"]["Playback_Start"]
                and self.macro.record == False
                and self.macro.playback == False
                and self.main_app.macro_recorded == True
            ):
                self.macro.start_playback()

            elif (
                self.hotkey_detection == userSettings["Hotkeys"]["Playback_Stop"]
                and self.macro.record == False
                and self.macro.playback == True
            ):
                self.macro.stop_playback(by_hotkey)

    def __on_release(self, key):
        if len(self.hotkey_detection) != 0:
            self.hotkey_detection.pop()
