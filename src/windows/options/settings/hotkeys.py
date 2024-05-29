from tkinter import *
from tkinter.ttk import *
from windows.popup import Popup

vk_nb = {"<96>": "0", "<97>": "1", "<98>": "2", "<99>": "3", "<100>": "4", "<101>": "5", "<102>": "6",
         "<103>": "7", "<104>": "8", "<105>": "9", "<65437>": "5", "<110>": "."}

class Hotkeys(Popup):
    def __init__(self, parent, main_app):
        super().__init__(main_app.text_content["options_menu"]["settings_menu"]["hotkeys_settings"]["title"], 300, 200, parent)
        main_app.prevent_record = True
        hotkeyLine = Frame(self)
        userSettings = main_app.settings.get_config()
        hotkeyStart = userSettings["Hotkeys"]["Record_Start"]
        hotkeyStop = userSettings["Hotkeys"]["Record_Stop"]
        hotkeyPlaybackStart = userSettings["Hotkeys"]["Playback_Start"]
        hotkeyPlaybackStop = userSettings["Hotkeys"]["Playback_Stop"]
        hotkeyVisible = [hotkeyStart, hotkeyStop, hotkeyPlaybackStart, hotkeyPlaybackStop]
        hotkeyManager = main_app.hotkeyManager

        for i in range(len(hotkeyVisible)):
            for j in range(len(hotkeyVisible[i])):
                key = hotkeyVisible[i][j].replace("Key.", "").replace("_l", "").replace("_r", "").replace("_gr", "")
                if "<" and ">" in key:
                    key = vk_nb[key]
                hotkeyVisible[i][j] = key.upper()

        Button(hotkeyLine, text=main_app.text_content["options_menu"]["settings_menu"]["hotkeys_settings"]["clear_text"],
               command=lambda: hotkeyManager.clearHotKey("Record_Start", self.startKey)).grid(row=0, column=2, padx=10)
        Button(hotkeyLine, text=main_app.text_content["options_menu"]["settings_menu"]["hotkeys_settings"]["clear_text"],
               command=lambda: hotkeyManager.clearHotKey("Record_Stop", self.stopKey)).grid(row=1, column=2, padx=10)
        Button(hotkeyLine, text=main_app.text_content["options_menu"]["settings_menu"]["hotkeys_settings"]["clear_text"],
               command=lambda: hotkeyManager.clearHotKey("Playback_Start", self.playbackStartKey)).grid(row=2, column=2,padx=10)


        Button(hotkeyLine, text=main_app.text_content["options_menu"]["settings_menu"]["hotkeys_settings"]["start_record_text"],
               command=lambda: hotkeyManager.enableHotKeyDetection("Record_Start", self.startKey, 0)).grid(row=0, column=0, padx=10)
        self.startKey = Label(hotkeyLine, text=hotkeyVisible[0], font=('Segoe UI', 12))
        self.startKey.grid(row=0, column=1, pady=5)

        Button(hotkeyLine, text=main_app.text_content["options_menu"]["settings_menu"]["hotkeys_settings"]["stop_record_text"],
               command=lambda: hotkeyManager.enableHotKeyDetection("Record_Stop", self.stopKey, 1)).grid(row=1, column=0, padx=10)
        self.stopKey = Label(hotkeyLine, text=hotkeyVisible[1], font=('Segoe UI', 12))
        self.stopKey.grid(row=1, column=1, pady=5)

        Button(hotkeyLine, text=main_app.text_content["options_menu"]["settings_menu"]["hotkeys_settings"]["start_playback_text"],
               command=lambda: hotkeyManager.enableHotKeyDetection("Playback_Start", self.playbackStartKey, 2)).grid(row=2, column=0,
                                                                                                  padx=10)
        self.playbackStartKey = Label(hotkeyLine, text=hotkeyVisible[2], font=('Segoe UI', 12))
        self.playbackStartKey.grid(row=2, column=1, pady=5)

        Button(hotkeyLine, text=main_app.text_content["options_menu"]["settings_menu"]["hotkeys_settings"]["stop_playback_text"],
               command=lambda: hotkeyManager.enableHotKeyDetection("Playback_Stop", self.playbackStopKey, 3)).grid(row=3, column=0,
                                                                                                padx=10)
        self.playbackStopKey = Label(hotkeyLine, text=hotkeyVisible[3], font=('Segoe UI', 12))
        self.playbackStopKey.grid(row=3, column=1, pady=5)

        hotkeyLine.pack()

        buttonArea = Frame(self)
        Button(buttonArea, text=main_app.text_content["global"]["close_button"], command=self.destroy).pack(side=LEFT, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        self.wait_window()
        main_app.prevent_record = False