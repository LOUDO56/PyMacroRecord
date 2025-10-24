from tkinter import *
from tkinter.ttk import *

from windows.popup import Popup


class About(Popup):
    def __init__(self, parent, main_app, version, updated):
        super().__init__(main_app.text_content["help_menu"]["about_settings"]["title"], 300, 150, parent)
        self.main_app = main_app
        self.main_app.about_window = self

        Label(self, text=f"{main_app.text_content['help_menu']['about_settings']['publisher_text']}: LOUDO").pack(
            side=TOP, pady=3)

        updated_display = updated if updated else "Checking..."
        self.version_label = Label(
            self,
            text=f"{main_app.text_content['help_menu']['about_settings']['version_text']}: {version} ({updated_display})"
        )
        self.version_label.pack(side=TOP, pady=3)

        Label(self,
              text=f"{main_app.text_content['help_menu']['about_settings']['license_text']}: General Public License v3.0").pack(
            side=TOP, pady=3)
        buttonArea = Frame(self)
        Button(buttonArea, text="Close", command=self.destroy).pack(side=LEFT, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        main_app.prevent_record = True
        self.wait_window()
        main_app.prevent_record = False

    def update_status(self, updated_text: str):
        if getattr(self, 'version_label', None):
            version = self.main_app.version.version
            self.version_label.configure(
                text=f"{self.main_app.text_content['help_menu']['about_settings']['version_text']}: {version} ({updated_text})"
            )

    def destroy(self):
        try:
            if hasattr(self.main_app, 'about_window'):
                self.main_app.about_window = None
        except Exception:
            pass
        return super().destroy()

