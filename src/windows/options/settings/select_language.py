from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from windows.popup import Popup
import os
import json
from utils.get_file import resource_path


class SelectLanguage(Popup):
    def __init__(self, parent, main_app):
        super().__init__(main_app.text_content["options_menu"]["settings_menu"]["lang_settings"]["title"], 250, 150, parent)
        main_app.prevent_record = True
        self.settings = main_app.settings
        self.options = {}
        short_to_long_lang = {}
        for lang in os.listdir(resource_path('langs')):
            file_lang = os.path.join(resource_path('langs'), lang)
            with open(file_lang, encoding='UTF-8') as f:
                content = json.load(f)
                self.options[content["information"]["lang_long"]] = content["information"]["lang_short"]
                short_to_long_lang[content["information"]["lang_short"]] = content["information"]["lang_long"]

        menuOptions = LabelFrame(self, text=main_app.text_content["options_menu"]["settings_menu"]["lang_settings"]["sub_text"])
        SelectLanguageVar = StringVar()
        (OptionMenu(menuOptions,
                   SelectLanguageVar,
                   short_to_long_lang[main_app.lang],
                   *self.options.keys())
        .pack(fill="both", padx=10,pady=10))

        menuOptions.pack(fill="both", padx=5, pady=10)
        buttonArea = Frame(self)
        Button(buttonArea, text=main_app.text_content["global"]["confirm_button"],
               command=lambda: self.setNewLanguage(SelectLanguageVar.get(), main_app)).pack(side=LEFT, padx=10)
        Button(buttonArea, text=main_app.text_content["global"]["cancel_button"], command=self.destroy).pack(side=LEFT, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        self.wait_window()
        main_app.prevent_record = False

    def setNewLanguage(self, newLang, main_app):
        messagebox.showinfo(main_app.text_content["global"]["information"], main_app.text_content["global"]["restart_software_text"])
        self.settings.change_settings("Language", None, None, self.options[newLang])
        self.destroy()
