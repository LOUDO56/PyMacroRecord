from tkinter import *
from tkinter import Label as oldLabel
from tkinter.ttk import *
from windows.popup import Popup
from sys import platform
from webbrowser import open_new
import os
import json

class Translators(Popup):
    def __init__(self, parent, main_app):
        width = 330
        if platform.lower() == "darwin":
            width += 110
        super().__init__(main_app.text_content["others_menu"]["translators_settings"]["title"], width, 300, parent)
        parent.prevent_record = True
        self.element_per_page = 6

        self.translators_list = []
        directory_path = os.path.join(os.path.dirname(__file__), '../../langs')
        for filename in os.listdir(directory_path):
            if filename.endswith('.json'):
                filepath = os.path.join(directory_path, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        information = data.get("information", {})
                        author = information.get("author", "Unknown Author")
                        lang_long = information.get("lang_long", "Unknown Language")
                        self.translators_list.append(f"{lang_long} - {author}")
                except Exception as e:
                    print(f"Error while opening {filename}: {e}")

        Label(self, text=main_app.text_content["others_menu"]["translators_settings"]["sub_text"] + "! <3", font=('Arial', 12, 'bold')).pack(side=TOP, pady=5)
        self.translatorsArea = Frame(self)
        self.navigationArea = Frame(self)
        self.pageArea = Frame(self)
        Button(self, text=main_app.text_content["global"]["close_button"], command=self.destroy).pack(side=BOTTOM, pady=5)
        self.display_translators(0, 1, main_app)
        self.wait_window()
        parent.prevent_record = False

    def display_translators(self, current_index, page, main_app):
        translators = self.translators_list[current_index:current_index+self.element_per_page]
        for widget in self.navigationArea.winfo_children():
            widget.destroy()
        for widget in self.translatorsArea.winfo_children():
            widget.destroy()
        for widget in self.pageArea.winfo_children():
            widget.destroy()
        for translator in translators:
            Label(self.translatorsArea, text=translator.strip()).pack(side=TOP, pady=2)
        maxPage = (len(self.translators_list) // self.element_per_page)
        if len(self.translators_list) % self.element_per_page > 0:
            maxPage += 1
        self.translatorsArea.pack(side=TOP)
        if page > 1:
            Button(self.navigationArea, text=main_app.text_content["global"]["previous_text"],
                   command=lambda: self.display_translators(current_index - self.element_per_page, page - 1, main_app)).pack(
                side=LEFT, padx=5, pady=5)
        if current_index + self.element_per_page < len(self.translators_list):
            Button(self.navigationArea, text=main_app.text_content["global"]["next_text"],
                   command=lambda: self.display_translators(current_index + self.element_per_page, page + 1, main_app)).pack(
                side=LEFT, padx=5, pady=5)
        self.navigationArea.pack(side=BOTTOM)
        Label(self.pageArea, text=f'Page {page} / {maxPage}').pack(side=TOP, pady=2)
        self.pageArea.pack(side=BOTTOM)


