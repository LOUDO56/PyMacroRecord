from tkinter import *
from tkinter import filedialog
from os import path
from json import load, dumps

from utils import UserSettings
from utils.warning_pop_up_save import confirm_save


class RecordFileManagement:
    """Manage save and load record from main app"""

    def __init__(self, main_app, menu_bar):
        self.main_app = main_app
        self.menu_bar = menu_bar
        self.config_text = self.menu_bar.text_config

    def save_macro_as(self, event=None):
        if not self.main_app.macro_recorded or self.main_app.macro.playback:
            return
        self.main_app.prevent_record = True
        macroSaved = filedialog.asksaveasfile(
            filetypes=[("PyMacroRecord Files", "*.pmr"), ("Json Files", "*.json")],
            defaultextension=".pmr",
        )
        if macroSaved is not None:
            self.main_app.current_file = macroSaved.name
            self.save_macro()
            self.main_app.macro_saved = True
        self.main_app.prevent_record = False

    def save_macro(self, event=None):
        if not self.main_app.macro_recorded or self.main_app.macro.playback:
            return
        if self.main_app.current_file is not None:
            with open(self.main_app.current_file, "w") as current_file:
                compactJson = UserSettings(self.main_app).get_config()["Saving"]["Compact_json"]
                if compactJson:
                    json_macroEvents = dumps(self.main_app.macro.macro_events, separators=(',', ':'))
                else:
                    json_macroEvents = dumps(self.main_app.macro.macro_events, indent=4)
                current_file.write(json_macroEvents)
        else:
            self.save_macro_as()

    def load_macro(self, event=None):
        if self.main_app.macro.playback:
            return
        self.main_app.prevent_record = True
        if not self.main_app.macro_saved and self.main_app.macro_recorded:
            wantToSave = confirm_save(self.main_app)
            if wantToSave:
                self.save_macro()
            elif wantToSave is None:
                self.main_app.prevent_record = False
                return
        macroFile = filedialog.askopenfile(
            filetypes=[("PyMacroRecord Files", "*.pmr"), ("Json Files", "*.json")],
            defaultextension=".pmr",
        )
        if macroFile is not None:
            self.main_app.playBtn.configure(
                state=NORMAL, command=self.main_app.macro.start_playback
            )
            self.menu_bar.file_menu.entryconfig(
                self.config_text["file_menu"]["save_text"], state=NORMAL, command=self.save_macro
            )
            self.menu_bar.file_menu.entryconfig(
                self.config_text["file_menu"]["save_as_text"], state=NORMAL, command=self.save_macro_as
            )
            self.menu_bar.file_menu.entryconfig(
                self.config_text["file_menu"]["new_text"], state=NORMAL, command=self.new_macro
            )
            macroFile.close()
            with open(macroFile.name, "r") as macroContent:
                self.main_app.macro.import_record(load(macroContent))
            self.main_app.macro_recorded = True
            self.main_app.macro_saved = True
            self.main_app.current_file = macroFile.name
        self.main_app.prevent_record = False

    def new_macro(self, event=None):
        if not self.main_app.macro_recorded or self.main_app.macro.playback:
            return
        if not self.main_app.macro_saved and self.main_app.macro_recorded:
            wantToSave = confirm_save(self.main_app)
            if wantToSave:
                self.save_macro()
            elif wantToSave is None:
                return
        self.main_app.playBtn.configure(state=NORMAL)
        self.menu_bar.file_menu.entryconfig(self.config_text["file_menu"]["save_text"], state=DISABLED)
        self.menu_bar.file_menu.entryconfig(self.config_text["file_menu"]["save_as_text"], state=DISABLED)
        self.menu_bar.file_menu.entryconfig(self.config_text["file_menu"]["new_text"], state=DISABLED)
        self.main_app.playBtn.configure(state=DISABLED)
        self.main_app.current_file = None
        self.main_app.macro_saved = False
        self.main_app.macro_recorded = False
