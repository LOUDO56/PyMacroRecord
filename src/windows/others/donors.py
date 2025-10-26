from sys import platform
from threading import Thread
from tkinter import BOTTOM, LEFT, TOP
from tkinter.font import Font
from tkinter.ttk import Button, Frame, Label, Style
from webbrowser import open_new

from requests import RequestException, get

from windows.popup import Popup


class HyperlinkLabel(Label):
    def __init__(self, master=None, text="", url=None, command=None, **kw):
        passed_font = kw.pop("font", None)
        super().__init__(master, text=text, **kw)

        base = Font(self, font=passed_font or self.cget("font"))
        a = base.actual()
        link_font = Font(
            self,
            family=a.get("family"),
            size=a.get("size"),
            weight=a.get("weight"),
            slant=a.get("slant"),
            underline=True,
        )

        style_name = f"{self._w}.Hyperlink.TLabel"
        Style(self).configure(style_name, foreground="blue", font=link_font)
        self.configure(style=style_name)

        self.bind("<Enter>", lambda e: self.configure(cursor="hand2"))
        self.bind("<Leave>", lambda e: self.configure(cursor=""))
        if command or url:
            self.bind("<Button-1>", lambda e: command() if command else open_new(url))


class Donors(Popup):
    def __init__(self, parent, main_app):
        width = 330
        if platform.lower() == "darwin":
            width += 110
        super().__init__(main_app.text_content["others_menu"]["donors_settings"]["title"], width, 300, parent)
        parent.prevent_record = True
        self.element_per_page = 6
        self.donors_list = []
        self._main_app = main_app

        Label(self, text=main_app.text_content["others_menu"]["donors_settings"]["sub_text"] + "! <3", font=('Arial', 12, 'bold')).pack(side=TOP, pady=5)
        support_work = HyperlinkLabel(
            self,
            text=main_app.text_content["others_menu"]["donors_settings"]["want_be_donor"],
            url="https://www.ko-fi.com/loudo",
            font=("Arial", 10, "bold"),
        )
        support_work.pack(side=TOP, pady=3)
        self.donorsArea = Frame(self)
        self.navigationArea = Frame(self)
        self.pageArea = Frame(self)
        Button(self, text=main_app.text_content["global"]["close_button"], command=self.destroy).pack(side=BOTTOM, pady=5)
        self.donorsArea.pack(side=TOP)
        Label(self.donorsArea, text=main_app.text_content["others_menu"]["donors_settings"]["load_donors"]).pack(side=TOP, pady=2)
        Thread(target=self._fetch_donors, daemon=True).start()
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
        Label(self.pageArea, text=f'{main_app.text_content["others_menu"]["translators_settings"]["page"]} {page} / {maxPage}').pack(side=TOP, pady=2)
        self.pageArea.pack(side=BOTTOM)

    def _fetch_donors(self):
        donors_link = 'https://pymacrorecord.com/donors.txt'
        try:
            response = get(donors_link, timeout=10)
            text = response.text if response is not None else ""
            lst = [s.strip() for s in text.split(';') if s.strip()]
            lst.reverse()
            self.donors_list = lst
        except RequestException:
            self.donors_list = []
        finally:
            self.after(0, self._on_donors_ready)

    def _on_donors_ready(self):
        if self.donors_list:
            self.display_donors(0, 1, self._main_app)
        else:
            for w in self.donorsArea.winfo_children():
                w.destroy()
            Label(self.donorsArea, text=self._main_app.text_content["others_menu"]["donors_settings"]["cant_get_donors"]).pack(side=TOP, pady=2)
