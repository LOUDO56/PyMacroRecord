import json
import os
from tkinter import (
    BOTTOM,
    LEFT,
    StringVar,
)
from tkinter.ttk import Button, Frame, LabelFrame, OptionMenu

from utils.get_file import resource_path
from windows.popup import Popup


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

        self.menuOptions = LabelFrame(self, text=main_app.text_content["options_menu"]["settings_menu"]["lang_settings"]["sub_text"])
        SelectLanguageVar = StringVar()
        OptionMenu(
            self.menuOptions, SelectLanguageVar,short_to_long_lang[main_app.lang],*self.options.keys()
        ).pack(fill="both", padx=10,pady=10)

        self.menuOptions.pack(fill="both", padx=5, pady=10)
        buttonArea = Frame(self)
        self.confirm_button = Button(
            buttonArea,
            text=main_app.text_content["global"]["confirm_button"],
            command=lambda: self.setNewLanguage(SelectLanguageVar.get(), main_app),
        )
        self.confirm_button.pack(side=LEFT, padx=10)
        self.cancel_button = Button(
            buttonArea,
            text=main_app.text_content["global"]["cancel_button"],
            command=self.destroy,
        )
        self.cancel_button.pack(side=LEFT, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        self.wait_window()
        main_app.prevent_record = False

    def setNewLanguage(self, newLang, main_app):
        self.settings.change_settings("Language", None, None, self.options[newLang])
        main_app.load_language()
        main_app.version.refresh_locale_text()
        old_menu_name = main_app["menu"]
        if old_menu_name:
            main_app.nametowidget(old_menu_name).destroy()
        from windows.main.menu_bar import MenuBar
        main_app.menu = MenuBar(main_app)
        main_app.macro.main_menu = main_app.menu
        main_app.macro.macro_file_management.menu_bar = main_app.menu
        self.title(main_app.text_content["options_menu"]["settings_menu"]["lang_settings"]["title"])
        self.menuOptions.configure(text=main_app.text_content["options_menu"]["settings_menu"]["lang_settings"]["sub_text"])
        self.confirm_button.configure(text=main_app.text_content["global"]["confirm_button"])
        self.cancel_button.configure(text=main_app.text_content["global"]["cancel_button"])
