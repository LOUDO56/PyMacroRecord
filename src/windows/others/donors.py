from tkinter import *
from tkinter import Label as oldLabel
from tkinter.ttk import *

from requests import RequestException

from windows.popup import Popup
import requests
from sys import platform
from webbrowser import open_new

class Donors(Popup):
    def __init__(self, parent, main_app):
        width = 330
        if platform.lower() == "darwin":
            width += 110
        super().__init__(main_app.text_content["others_menu"]["donors_settings"]["title"], width, 300, parent)
        parent.prevent_record = True
        self.element_per_page = 6

        donors_link = 'https://pymacrorecord.com/donors.txt'
        try:
            response = requests.get(donors_link)
            self.donors_list = response.text.split(';')
            self.donors_list.reverse()
        except RequestException:
            pass

        Label(self, text=main_app.text_content["others_menu"]["donors_settings"]["sub_text"] + "! <3", font=('Arial', 12, 'bold')).pack(side=TOP, pady=5)
        support_work = oldLabel(self, text="Want to be a donor? Click here!", font=('Arial', 10, 'bold'), fg="blue", cursor="hand2")
        support_work.pack(side=TOP, pady=3)
        support_work.bind("<Button-1>", lambda e: open_new("https://www.ko-fi.com/loudo"))
        self.donorsArea = Frame(self)
        self.navigationArea = Frame(self)
        self.pageArea = Frame(self)
        Button(self, text=main_app.text_content["global"]["close_button"], command=self.destroy).pack(side=BOTTOM, pady=5)
        self.display_donors(0, 1, main_app)
        self.wait_window()
        parent.prevent_record = False

    def display_donors(self, current_index, page, main_app):
        donors = self.donors_list[current_index:current_index+self.element_per_page]
        for widget in self.navigationArea.winfo_children():
            widget.destroy()
        for widget in self.donorsArea.winfo_children():
            widget.destroy()
        for widget in self.pageArea.winfo_children():
            widget.destroy()
        for donor in donors:
            Label(self.donorsArea, text=donor.strip()).pack(side=TOP, pady=2)
        maxPage = (len(self.donors_list) // self.element_per_page)
        if len(self.donors_list) % self.element_per_page > 0:
            maxPage += 1
        self.donorsArea.pack(side=TOP)
        if page > 1:
            Button(self.navigationArea, text=main_app.text_content["global"]["previous_text"],
                   command=lambda: self.display_donors(current_index - self.element_per_page, page - 1, main_app)).pack(
                side=LEFT, padx=5, pady=5)
        if current_index + self.element_per_page < len(self.donors_list):
            Button(self.navigationArea, text=main_app.text_content["global"]["next_text"],
                   command=lambda: self.display_donors(current_index + self.element_per_page, page + 1, main_app)).pack(
                side=LEFT, padx=5, pady=5)
        self.navigationArea.pack(side=BOTTOM)
        Label(self.pageArea, text=f'Page {page} / {maxPage}').pack(side=TOP, pady=2)
        self.pageArea.pack(side=BOTTOM)


