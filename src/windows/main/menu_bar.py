from windows.help.about import *
from windows.others.donors import *
from windows.others.translators import *
from windows.options.playback import *
from windows.options.settings import *
from windows.others.timestamp import Timestamp
from utils.record_file_management import RecordFileManagement
from webbrowser import open as OpenUrl
from sys import argv

class MenuBar(Menu):
    def __init__(self, parent):
        super().__init__(parent)

        settings = parent.settings
        userSettings = settings.get_config()
        self.text_config = parent.text_content


        # Menu Setup
        my_menu = Menu(parent)
        parent.config(menu=my_menu)
        self.file_menu = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label=self.text_config["file_menu"]["file_text"], menu=self.file_menu)
        record_file_management = RecordFileManagement(parent, self)
        if len(argv) > 1:
            self.file_menu.add_command(label=self.text_config["file_menu"]["new_text"], accelerator="Ctrl+N", command=record_file_management.new_macro)
        else:
            self.file_menu.add_command(label=self.text_config["file_menu"]["new_text"], state=DISABLED, accelerator="Ctrl+N")
        self.file_menu.add_command(label=self.text_config["file_menu"]["load_text"], accelerator="Ctrl+L", command=record_file_management.load_macro)
        self.file_menu.add_separator()
        if len(argv) > 1:
            self.file_menu.add_command(label=self.text_config["file_menu"]["save_text"], accelerator="Ctrl+S", command=record_file_management.save_macro)
            self.file_menu.add_command(label=self.text_config["file_menu"]["save_as_text"], accelerator="Ctrl+Shift+S", command=record_file_management.save_macro_as)
        else:
            self.file_menu.add_command(label=self.text_config["file_menu"]["save_text"], accelerator="Ctrl+S", state=DISABLED)
            self.file_menu.add_command(label=self.text_config["file_menu"]["save_as_text"], accelerator="Ctrl+Shift+S", state=DISABLED)

        # Options Section
        self.options_menu = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label=self.text_config["options_menu"]["options_text"], menu=self.options_menu)

        # Playback Sub
        playback_sub = Menu(self.options_menu, tearoff=0)
        self.options_menu.add_cascade(label=self.text_config["options_menu"]["playback_menu"]["playback_text"], menu=playback_sub)
        playback_sub.add_command(label=self.text_config["options_menu"]["playback_menu"]["speed_text"], command=lambda: Speed(self, parent))
        playback_sub.add_command(label=self.text_config["options_menu"]["playback_menu"]["repeat_text"], command=lambda: Repeat(self, parent))
        playback_sub.add_command(label=self.text_config["options_menu"]["playback_menu"]["interval_text"], command=lambda: TimeGui(self, parent, "Interval"))
        playback_sub.add_command(label=self.text_config["options_menu"]["playback_menu"]["for_text"], command=lambda: TimeGui(self, parent, "For"))
        playback_sub.add_command(label=self.text_config["options_menu"]["playback_menu"]["scheduled_text"], command=lambda: TimeGui(self, parent, "Scheduled"))
        playback_sub.add_command(label=self.text_config["options_menu"]["playback_menu"]["delay_text"], command=lambda: Delay(self, parent))

        # Recordings Sub
        self.mouseMove = BooleanVar(value=userSettings["Recordings"]["Mouse_Move"])
        self.mouseClick = BooleanVar(value=userSettings["Recordings"]["Mouse_Click"])
        self.keyboardInput = BooleanVar(value=userSettings["Recordings"]["Keyboard"])
        recordings_sub = Menu(self.options_menu, tearoff=0)
        self.options_menu.add_cascade(label=self.text_config["options_menu"]["recordings_menu"]["recordings_text"], menu=recordings_sub)
        recordings_sub.add_checkbutton(label=self.text_config["options_menu"]["recordings_menu"]["mouse_movement_text"], variable=self.mouseMove,
                                       command=lambda: settings.change_settings("Recordings", "Mouse_Move"))
        recordings_sub.add_checkbutton(label=self.text_config["options_menu"]["recordings_menu"]["mouse_click_text"], variable=self.mouseClick,
                                       command=lambda: settings.change_settings("Recordings", "Mouse_Click"))
        recordings_sub.add_checkbutton(label=self.text_config["options_menu"]["recordings_menu"]["keyboard_text"], variable=self.keyboardInput,
                                       command=lambda: settings.change_settings("Recordings", "Keyboard"))

        # Settings Sub
        self.options_sub = Menu(self.options_menu, tearoff=0)
        self.compactJson = BooleanVar(value=userSettings["Saving"]["Compact_json"])
        self.options_sub.add_checkbutton(label=self.text_config["options_menu"]["json_compact"], command=lambda: settings.change_settings("Saving", "Compact_json"), variable=self.compactJson)
        self.options_menu.add_cascade(label=self.text_config["options_menu"]["settings_menu"]["settings_text"], menu=self.options_sub)
        self.options_sub.add_command(label=self.text_config["options_menu"]["settings_menu"]["hotkeys_text"], command=lambda: Hotkeys(self, parent))
        self.options_sub.add_command(label=self.text_config["options_menu"]["settings_menu"]["lang_text"], command=lambda: SelectLanguage(self, parent))

        minimization_sub = Menu(self.options_sub, tearoff=0)
        self.options_sub.add_cascade(label=self.text_config["options_menu"]["settings_menu"]["minimization_text"], menu=minimization_sub)
        self.minimization_playing = BooleanVar(value=userSettings["Minimization"]["When_Playing"])
        self.minimization_record = BooleanVar(value=userSettings["Minimization"]["When_Recording"])
        minimization_sub.add_checkbutton(label=self.text_config["options_menu"]["settings_menu"]["minimization_menu"]["minimization_when_playing_text"], variable=self.minimization_playing,
                                         command=lambda: settings.change_settings("Minimization", "When_Playing"))
        minimization_sub.add_checkbutton(label=self.text_config["options_menu"]["settings_menu"]["minimization_menu"]["minimization_when_recording_text"], variable=self.minimization_record,
                                         command=lambda: settings.change_settings("Minimization", "When_Recording"))

        # options_sub.add_checkbutton(label="Run on startup", variable=runStartUp, command=lambda: changeSettings("Run_On_StartUp"))
        self.options_sub.add_command(label=self.text_config["options_menu"]["settings_menu"]["after_playback_text"], command=lambda: AfterPlayBack(self, parent))

        # Others Sub
        self.others_sub = Menu(self.options_menu, tearoff=0)
        self.options_menu.add_cascade(label=self.text_config["options_menu"]["others_menu"]["others_text"], menu=self.others_sub)
        self.Check_update = BooleanVar(value=userSettings["Others"]["Check_update"])
        self.others_sub.add_checkbutton(label=self.text_config["options_menu"]["others_menu"]["check_update_text"], variable=self.Check_update, command=lambda: settings.change_settings("Others", "Check_update"))
        self.others_sub.add_command(label=self.text_config["options_menu"]["others_menu"]["reset_settings_text"], command=settings.reset_settings)
        self.others_sub.add_command(label=self.text_config["options_menu"]["others_menu"]["fixed_timestamp_text"], command=lambda: Timestamp(self, parent))

        # Help section
        self.help_section = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label=self.text_config["help_menu"]["help_text"], menu=self.help_section)
        self.help_section.add_command(label=self.text_config["help_menu"]["tutorial_text"], command=lambda: OpenUrl("https://github.com/LOUDO56/PyMacroRecord/blob/main/TUTORIAL.md"))
        self.help_section.add_command(label=self.text_config["help_menu"]["website_text"],
                                      command=lambda: OpenUrl("https://www.pymacrorecord.com"))
        self.help_section.add_command(label=self.text_config["help_menu"]["about_text"], command=lambda: About(self, parent, parent.version.version, parent.version.update))

        # Other section
        self.other_section = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label=self.text_config["others_menu"]["others_text"], menu=self.other_section)
        self.other_section.add_command(label=self.text_config["others_menu"]["donors_text"], command=lambda: Donors(self, parent))
        self.other_section.add_command(label=self.text_config["others_menu"]["translators_text"], command=lambda: Translators(self, parent))
