from tkinter import *
from tkinter import filedialog
from os import path
from json import load, dumps
from utils.warning_pop_up_save import confirm_save


class RecordFileManagement:
    def __init__(self, main_app, menu_bar):
        self.main_app = main_app
        self.record_path = path.join(self.main_app.settings.get_path(), "temprecord.json")
        self.menu_bar = menu_bar
        self.current_file = None

    def save_macro_as(self):
        self.main_app.prevent_record = True
        macroSaved = filedialog.asksaveasfile(filetypes=[('Json Files', '*.json')], defaultextension='.json')
        if macroSaved is not None:
            self.current_file = macroSaved.name
            self.save_macro()
            self.main_app.macro_saved = True
        self.main_app.prevent_record = False

    def save_macro(self):
        if self.current_file is not None:
            self.__import_export(self.record_path, self.current_file)
        else:
            self.save_macro_as()



    def load_macro(self):
        self.main_app.prevent_record = True
        if not self.main_app.macro_saved and self.main_app.macro_recorded:
            wantToSave = confirm_save()
            if wantToSave:
                self.save_macro()
            elif wantToSave == None:
                return
        macroFile = filedialog.askopenfile(filetypes=[('Json Files', '*.json')], defaultextension='.json')
        if macroFile is not None:
            self.__import_export(macroFile.name, self.record_path)
            self.main_app.playBtn.configure(state=NORMAL, command=self.main_app.macro.start_playback)
            self.menu_bar.file_menu.entryconfig('Save', state=NORMAL, command=self.save_macro)
            self.menu_bar.file_menu.entryconfig('Save as', state=NORMAL, command=self.save_macro_as)
            self.menu_bar.file_menu.entryconfig('New', state=NORMAL, command=self.new_macro)
            macroFile.close()
            with open(self.record_path, "r") as macroContent:
                self.main_app.macro.import_record(load(macroContent))
        self.main_app.prevent_record = False

    def new_macro(self):
        if not self.main_app.macro_saved and self.main_app.macro_recorded:
            wantToSave = confirm_save()
            if wantToSave:
                self.save_macro()
            elif wantToSave == None:
                return
        self.main_app.playBtn.configure(state=NORMAL)
        self.menu_bar.file_menu.entryconfig('Save', state=DISABLED)
        self.menu_bar.file_menu.entryconfig('Save as', state=DISABLED)
        self.menu_bar.file_menu.entryconfig('New', state=DISABLED)
        self.main_app.playBtn.configure(state=DISABLED)
        self.current_file = None
        self.main_app.macro_saved = False
        self.main_app.macro_recorded = False

    def __import_export(self, toRead, toWrite):
        with open(toRead, "r") as macroContent:
            loaded_events = load(macroContent)
        with open(toWrite, "w") as fileToWrite:
            json_macroEvents = dumps(loaded_events, indent=4)
            fileToWrite.write(json_macroEvents)
