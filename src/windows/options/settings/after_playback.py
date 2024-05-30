from tkinter import *
from tkinter.ttk import *
from windows.popup import Popup


class AfterPlayBack(Popup):
    def __init__(self, parent, main_app):
        super().__init__(main_app.text_content["options_menu"]["settings_menu"]["after_playback_settings"]["title"], 250, 150, parent)
        main_app.prevent_record = True
        self.settings = main_app.settings
        options = {
            main_app.text_content["options_menu"]["settings_menu"]["after_playback_settings"]["idle"]: "Idle",
            main_app.text_content["options_menu"]["settings_menu"]["after_playback_settings"]["quit software"]: "Quit software",
            main_app.text_content["options_menu"]["settings_menu"]["after_playback_settings"]["standby"]: "Standby",
            main_app.text_content["options_menu"]["settings_menu"]["after_playback_settings"]["log off computer"]: "Log off computer",
            main_app.text_content["options_menu"]["settings_menu"]["after_playback_settings"]["turn off computer"]: "Turn off computer",
            main_app.text_content["options_menu"]["settings_menu"]["after_playback_settings"]["restart computer"]: "Restart computer",
            main_app.text_content["options_menu"]["settings_menu"]["after_playback_settings"]["hibernate (if enabled)"]: "Hibernate (if enabled)"
        }

        menuOptions = LabelFrame(self, text=main_app.text_content["options_menu"]["settings_menu"]["after_playback_settings"]["when_playback_complete_text"])
        AfterPlaybackOption = StringVar()
        userSettings = main_app.settings.get_config()
        (OptionMenu(menuOptions,
                   AfterPlaybackOption,
                   main_app.text_content["options_menu"]["settings_menu"]["after_playback_settings"][userSettings["After_Playback"]["Mode"].lower()],
                   *options.keys())
        .pack(fill="both", padx=10,pady=10))

        menuOptions.pack(fill="both", padx=5, pady=10)
        buttonArea = Frame(self)
        Button(buttonArea, text=main_app.text_content["global"]["confirm_button"],
               command=lambda: [self.settings.change_settings("After_Playback", "Mode", None, options[AfterPlaybackOption.get()]),
                                self.destroy()]).pack(side=LEFT, padx=10)
        Button(buttonArea, text=main_app.text_content["global"]["cancel_button"], command=self.destroy).pack(side=LEFT, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        self.wait_window()
        main_app.prevent_record = False

