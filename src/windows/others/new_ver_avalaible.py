from tkinter import *
from tkinter.ttk import *
from windows.popup import Popup
from webbrowser import open as OpenUrl

class NewVerAvailable(Popup):
    def __init__(self, parent, version):
        super().__init__("New Version Available!", 300, 130, parent)
        parent.prevent_record = True
        Label(self, text=f"New Version {version} available!").pack(side=TOP)
        Label(self, text="Click the button to open releases page on GitHub").pack(side=TOP)
        buttonArea = Frame(self)
        Button(buttonArea, text="Click here to view",
               command=lambda: OpenUrl("https://github.com/LOUDO56/PyMacroRecord/releases")).pack(side=LEFT, pady=10)
        Button(buttonArea, text="Close", command=self.destroy).pack(side=LEFT, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        self.wait_window()
        parent.prevent_record = False