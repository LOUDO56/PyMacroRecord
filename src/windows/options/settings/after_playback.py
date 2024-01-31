from tkinter import *
from tkinter.ttk import *
from windows.popup import Popup


class AfterPlayBack(Popup):
    def __init__(self, parent, main_app):
        super().__init__("After Playback", 250, 150, parent)
        main_app.prevent_record = True
        self.settings = main_app.settings
        options = [
            'Idle',
            'Quit Software',
            'Standy',
            'Log off Computer',
            'Turn off Computer',
            'Restart Computer',
            'Hibernate (If enabled)'
        ]

        menuOptions = LabelFrame(self, text="On playback complete")
        AfterPlaybackOption = StringVar()
        userSettings = main_app.settings.get_config()
        OptionMenu(menuOptions, AfterPlaybackOption, userSettings["After_Playback"]["Mode"], *options).pack(fill="both",
                                                                                                            padx=10,
                                                                                                            pady=10)
        menuOptions.pack(fill="both", padx=5, pady=10)
        buttonArea = Frame(self)
        Button(buttonArea, text="Confirm",
               command=lambda: [self.settings.change_settings("After_Playback", "Mode", None, AfterPlaybackOption.get()),
                                self.destroy()]).pack(side=LEFT, padx=10)
        Button(buttonArea, text="Cancel", command=self.destroy).pack(side=LEFT, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        self.wait_window()
        main_app.prevent_record = False