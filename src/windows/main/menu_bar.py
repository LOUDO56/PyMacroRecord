from windows.help.about import *
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


        # Menu Setup
        my_menu = Menu(parent)
        parent.config(menu=my_menu)
        self.file_menu = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label="File", menu=self.file_menu)
        record_file_management = RecordFileManagement(parent, self)
        if len(argv) > 1:
            self.file_menu.add_command(label="New", accelerator="Ctrl+N", command=record_file_management.new_macro)
        else:
            self.file_menu.add_command(label="New", state=DISABLED, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Load", accelerator="Ctrl+L", command=record_file_management.load_macro)
        self.file_menu.add_separator()
        if len(argv) > 1:
            self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command=record_file_management.save_macro)
            self.file_menu.add_command(label="Save as", accelerator="Ctrl+Shift+S", command=record_file_management.save_macro_as)
        else:
            self.file_menu.add_command(label="Save", accelerator="Ctrl+S", state=DISABLED)
            self.file_menu.add_command(label="Save as", accelerator="Ctrl+Shift+S", state=DISABLED)

        # Options Section
        self.options_menu = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label="Options", menu=self.options_menu)

        # Playback Sub
        playback_sub = Menu(self.options_menu, tearoff=0)
        self.options_menu.add_cascade(label="Playback", menu=playback_sub)
        playback_sub.add_command(label="Speed", command=lambda: Speed(self, parent))
        playback_sub.add_command(label="Repeat", command=lambda: Repeat(self, parent))
        playback_sub.add_command(label="Interval", command=lambda: TimeGui(self, parent, "Interval"))
        playback_sub.add_command(label="For", command=lambda: TimeGui(self, parent, "For"))
        playback_sub.add_command(label="Delay", command=lambda: Delay(self, parent))

        # Recordings Sub
        self.mouseMove = BooleanVar(value=userSettings["Recordings"]["Mouse_Move"])
        self.mouseClick = BooleanVar(value=userSettings["Recordings"]["Mouse_Click"])
        self.keyboardInput = BooleanVar(value=userSettings["Recordings"]["Keyboard"])
        recordings_sub = Menu(self.options_menu, tearoff=0)
        self.options_menu.add_cascade(label="Recordings", menu=recordings_sub)
        recordings_sub.add_checkbutton(label="Mouse movement", variable=self.mouseMove,
                                       command=lambda: settings.change_settings("Recordings", "Mouse_Move"))
        recordings_sub.add_checkbutton(label="Mouse click", variable=self.mouseClick,
                                       command=lambda: settings.change_settings("Recordings", "Mouse_Click"))
        recordings_sub.add_checkbutton(label="Keyboard", variable=self.keyboardInput,
                                       command=lambda: settings.change_settings("Recordings", "Keyboard"))

        # Options Sub
        self.options_sub = Menu(self.options_menu, tearoff=0)
        self.options_menu.add_cascade(label="Settings", menu=self.options_sub)
        self.options_sub.add_command(label="Hotkeys", command=lambda: Hotkeys(self, parent))

        minimization_sub = Menu(self.options_sub, tearoff=0)
        self.options_sub.add_cascade(label="Minimization", menu=minimization_sub)
        self.minimization_playing = BooleanVar(value=userSettings["Minimization"]["When_Playing"])
        self.minimization_record = BooleanVar(value=userSettings["Minimization"]["When_Recording"])
        minimization_sub.add_checkbutton(label="Minimized when playing", variable=self.minimization_playing,
                                         command=lambda: settings.change_settings("Minimization", "When_Playing"))
        minimization_sub.add_checkbutton(label="Minimized when recording", variable=self.minimization_record,
                                         command=lambda: settings.change_settings("Minimization", "When_Recording"))

        # options_sub.add_checkbutton(label="Run on startup", variable=runStartUp, command=lambda: changeSettings("Run_On_StartUp"))
        self.options_sub.add_command(label="After playback...", command=lambda: AfterPlayBack(self, parent))

        # Others Sub
        self.others_sub = Menu(self.options_menu, tearoff=0)
        self.options_menu.add_cascade(label="Others", menu=self.others_sub)
        self.Check_update = BooleanVar(value=userSettings["Others"]["Check_update"])
        self.others_sub.add_checkbutton(label="Check update", variable=self.Check_update, command=lambda: settings.change_settings("Others", "Check_update"))
        self.others_sub.add_command(label="Fixed timestamp", command=lambda: Timestamp(self, parent))

        # Help section
        self.help_section = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label="Help", menu=self.help_section)
        self.help_section.add_command(label="Tutorial", command=lambda: OpenUrl("https://github.com/LOUDO56/PyMacroRecord/blob/main/TUTORIAL.md"))
        self.help_section.add_command(label="About", command=lambda: About(self, parent, parent.version.version, parent.version.update))
