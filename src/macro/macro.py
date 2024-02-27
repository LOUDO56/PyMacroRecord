from tkinter import *
from tkinter import messagebox
from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import Key
from utils.get_key_pressed import getKeyPressed
from utils.record_file_management import RecordFileManagement
from utils.warning_pop_up_save import confirm_save
from utils.show_toast import show_notification_minim
from utils.keys import vk_nb
from time import time, sleep
from os import getlogin
from sys import platform
from threading import Thread
import subprocess
import ctypes
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)


class Macro:
    """Init a new Macro"""

    def __init__(self, main_app):
        self.mouseControl = mouse.Controller()
        self.keyboardControl = keyboard.Controller()
        self.record = False
        self.playback = False
        self.macro_events = {"events": []}
        self.main_app = main_app
        self.user_settings = self.main_app.settings
        self.main_menu = self.main_app.menu
        self.macro_file_management = RecordFileManagement(self.main_app, self.main_menu)

        self.mouseBeingListened = None
        self.keyboardBeingListened = None
        self.keyboard_listener = None
        self.mouse_listener = None
        self.time = None

    def start_record(self, by_hotkey=False):
        if self.main_app.prevent_record:
            return
        if not by_hotkey:
            if not self.main_app.macro_saved and self.main_app.macro_recorded:
                wantToSave = confirm_save()
                if wantToSave:
                    self.macro_file_management.save_macro()
                elif wantToSave is None:
                    return
        self.macro_events = {"events": []}
        self.record = True
        self.time = time()
        userSettings = self.user_settings.get_config()
        if (
            userSettings["Recordings"]["Mouse_Move"]
            and userSettings["Recordings"]["Mouse_Click"]
        ):
            self.mouse_listener = mouse.Listener(
                on_move=self.__on_move,
                on_click=self.__on_click,
                on_scroll=self.__on_scroll,
            )
            self.mouse_listener.start()
            self.mouseBeingListened = True
        elif userSettings["Recordings"]["Mouse_Move"]:
            self.mouse_listener = mouse.Listener(
                on_move=self.__on_move, on_scroll=self.__on_scroll
            )
            self.mouse_listener.start()
            self.mouseBeingListened = True
        elif userSettings["Recordings"]["Mouse_Click"]:
            self.mouse_listener = mouse.Listener(
                on_click=self.__on_click, on_scroll=self.__on_scroll
            )
            self.mouse_listener.start()
            self.mouseBeingListened = True
        if userSettings["Recordings"]["Keyboard"]:
            self.keyboard_listener = keyboard.Listener(
                on_press=self.__on_press, on_release=self.__on_release
            )
            self.keyboard_listener.start()
            self.keyboardBeingListened = True
        self.main_menu.file_menu.entryconfig("Load", state=DISABLED)
        self.main_app.recordBtn.configure(
            image=self.main_app.stopImg, command=self.stop_record
        )
        self.main_app.playBtn.configure(state=DISABLED)
        self.main_menu.file_menu.entryconfig("Save", state=DISABLED)
        self.main_menu.file_menu.entryconfig("Save as", state=DISABLED)
        self.main_menu.file_menu.entryconfig("New", state=DISABLED)
        self.main_menu.file_menu.entryconfig("Load", state=DISABLED)
        if userSettings["Minimization"]["When_Recording"]:
            self.main_app.withdraw()
            Thread(target=show_notification_minim).start()
        print("record started")

    def stop_record(self):
        if not self.record:
            return
        userSettings = self.user_settings.get_config()
        self.record = False
        if self.mouseBeingListened:
            self.mouse_listener.stop()
        if self.keyboardBeingListened:
            self.keyboard_listener.stop()
        self.main_app.recordBtn.configure(
            image=self.main_app.recordImg, command=self.start_record
        )
        self.main_app.playBtn.configure(state=NORMAL, command=self.start_playback)
        self.main_menu.file_menu.entryconfig(
            "Save", state=NORMAL, command=self.macro_file_management.save_macro
        )
        self.main_menu.file_menu.entryconfig(
            "Save as", state=NORMAL, command=self.macro_file_management.save_macro_as
        )
        self.main_menu.file_menu.entryconfig(
            "New", state=NORMAL, command=self.macro_file_management.new_macro
        )
        self.main_menu.file_menu.entryconfig("Load", state=NORMAL)

        self.main_app.macro_recorded = True
        self.main_app.macro_saved = False

        if userSettings["Minimization"]["When_Recording"]:
            self.main_app.deiconify()

        print("record stopped")

    def start_playback(self):
        userSettings = self.user_settings.get_config()
        self.playback = True
        self.main_app.playBtn.configure(
            image=self.main_app.stopImg, command=lambda: self.stop_playback(True)
        )
        self.main_menu.file_menu.entryconfig("Save", state=DISABLED)
        self.main_menu.file_menu.entryconfig("Save as", state=DISABLED)
        self.main_menu.file_menu.entryconfig("New", state=DISABLED)
        self.main_menu.file_menu.entryconfig("Load", state=DISABLED)
        self.main_app.recordBtn.configure(state=DISABLED)
        if userSettings["Minimization"]["When_Playing"]:
            self.main_app.withdraw()
            Thread(target=show_notification_minim).start()
        if userSettings["Playback"]["Repeat"]["Interval"] > 0:
            Thread(target=self.__play_interval).start()
        elif userSettings["Playback"]["Repeat"]["For"] > 0:
            Thread(target=self.__play_for).start()
        elif userSettings["Playback"]["Repeat"]["For"] > 0 and userSettings["Playback"]["Repeat"]["Interval"] > 0:
            Thread(target=self.__play_interval).start()
        else:
            Thread(target=self.__play_events).start()
        print("playback started")

    def __play_interval(self):
        userSettings = self.user_settings.get_config()
        if userSettings["Playback"]["Repeat"]["For"] > 0:
            self.__play_for()
        else:
            self.__play_events()
        timer = time()
        while self.playback:
            sleep(1)
            if time() - timer >= userSettings["Playback"]["Repeat"]["Interval"]:
                if userSettings["Playback"]["Repeat"]["For"] > 0:
                    self.__play_for()
                else:
                    self.__play_events()
                timer = time()

    def __play_for(self):
        userSettings = self.user_settings.get_config()
        debut = time()
        while self.playback and (time() - debut) < userSettings["Playback"]["Repeat"]["For"]:
            self.__play_events()
        if userSettings["Playback"]["Repeat"]["Interval"] == 0:
            self.stop_playback()

    def __play_events(self):
        userSettings = self.user_settings.get_config()
        click_func = {
            "leftClickEvent": Button.left,
            "rightClickEvent": Button.right,
            "middleClickEvent": Button.middle,
        }
        keyToUnpress = []
        if userSettings["Playback"]["Repeat"]["For"] > 0:
            repeat_times = 1
        else:
            repeat_times = userSettings["Playback"]["Repeat"]["Times"]
        for repeat in range(repeat_times):
            for events in range(len(self.macro_events["events"])):
                if self.playback == False:
                    self.unPressEverything(keyToUnpress)
                    return
                if userSettings["Others"]["Fixed_timestamp"] > 0:
                    timeSleep = userSettings["Others"]["Fixed_timestamp"]
                else:
                    timeSleep = (
                        self.macro_events["events"][events]["timestamp"]
                        * (1 / userSettings["Playback"]["Speed"])
                    )
                sleep(timeSleep)
                event_type = self.macro_events["events"][events]["type"]

                if event_type == "cursorMove":  # Cursor Move
                    self.mouseControl.position = (
                        self.macro_events["events"][events]["x"],
                        self.macro_events["events"][events]["y"],
                    )

                elif event_type in click_func:  # Mouse Click
                    self.mouseControl.position = (
                        self.macro_events["events"][events]["x"],
                        self.macro_events["events"][events]["y"],
                    )
                    if self.macro_events["events"][events]["pressed"] == True:
                        self.mouseControl.press(click_func[event_type])
                    else:
                        self.mouseControl.release(click_func[event_type])

                elif event_type == "scrollEvent":
                    self.mouseControl.scroll(
                        self.macro_events["events"][events]["dx"],
                        self.macro_events["events"][events]["dy"],
                    )

                elif event_type == "keyboardEvent":  # Keyboard Press,Release
                    if self.macro_events["events"][events]["key"] != None:
                        try:
                            keyToPress = (
                                self.macro_events["events"][events]["key"]
                                if "Key." not in self.macro_events["events"][events]["key"]
                                else eval(self.macro_events["events"][events]["key"])
                            )
                            if isinstance(keyToPress, str):
                                if ">" in keyToPress:
                                    try:
                                        keyToPress = vk_nb[keyToPress]
                                    except:
                                        keyToPress = None
                            if self.playback == True:
                                if keyToPress != None:
                                    if (
                                        self.macro_events["events"][events]["pressed"]
                                        == True
                                    ):
                                        self.keyboardControl.press(keyToPress)
                                        if keyToPress not in keyToUnpress:
                                            keyToUnpress.append(keyToPress)
                                    else:
                                        self.keyboardControl.release(keyToPress)
                        except NameError as e:
                            messagebox.showerror("Error", f"Error during playback \"{e}\". Please open an issue on Github.")
                            self.stop_playback()
            if userSettings["Playback"]["Repeat"]["Delay"] > 0:
                if repeat + 1 != repeat_times:
                    sleep(userSettings["Playback"]["Repeat"]["Delay"])
        self.unPressEverything(keyToUnpress)
        if userSettings["Playback"]["Repeat"]["Interval"] == 0 and userSettings["Playback"]["Repeat"]["For"] == 0:
            self.stop_playback()

    def unPressEverything(self, keyToUnpress):
        for key in keyToUnpress:
            self.keyboardControl.release(key)
        self.mouseControl.release(Button.left)
        self.mouseControl.release(Button.middle)

    def stop_playback(self, playback_stopped_manually=False):
        self.playback = False
        if not playback_stopped_manually:
            print("playback stopped")
        else:
            print("playback stopped manually")
        userSettings = self.user_settings.get_config()
        self.main_app.recordBtn.configure(state=NORMAL)
        self.main_app.playBtn.configure(
            image=self.main_app.playImg, command=self.start_playback
        )
        self.main_menu.file_menu.entryconfig("New", state=NORMAL)
        self.main_menu.file_menu.entryconfig("Load", state=NORMAL)
        self.main_menu.file_menu.entryconfig("Save", state=NORMAL)
        self.main_menu.file_menu.entryconfig("Save as", state=NORMAL)
        if userSettings["Minimization"]["When_Playing"]:
            self.main_app.deiconify()
        if userSettings["After_Playback"]["Mode"] != "Idle" and not playback_stopped_manually:
            if userSettings["After_Playback"]["Mode"] == "Standy":
                if platform == "win32":
                    subprocess.call("rundll32.exe powrprof.dll, SetSuspendState 0,1,0", shell=False)
                elif "linux" in platform.lower():
                    subprocess.call("subprocess.callctl suspend", shell=False)
                elif "darwin" in platform.lower():
                    subprocess.call("pmset sleepnow", shell=False)
            elif userSettings["After_Playback"]["Mode"] == "Log off Computer":
                if platform == "win32":
                    subprocess.call("shutdown /l", shell=False)
                else:
                    subprocess.call(f"pkill -KILL -u {getlogin()}", shell=False)
            elif userSettings["After_Playback"]["Mode"] == "Turn off Computer":
                if platform == "win32":
                    subprocess.call("shutdown /s /t 0", shell=False)
                else:
                    subprocess.call("shutdown -h now", shell=False)
            elif userSettings["After_Playback"]["Mode"] == "Restart Computer":
                if platform == "win32":
                    subprocess.call("shutdown /r /t 0", shell=False)
                else:
                    subprocess.call("shutdown -r now", shell=False)
            elif userSettings["After_Playback"]["Mode"] == "Hibernate (If activated)":
                if platform == "win32":
                    subprocess.call("shutdown -h", shell=False)
                elif "linux" in platform.lower():
                    subprocess.call("systemctl hibernate", shell=False)
                elif "darwin" in platform.lower():
                    subprocess.call("pmset sleepnow", shell=False)
            force_close = True
            self.main_app.quit_software(force_close)

    def import_record(self, record):
        self.macro_events = record

    def __on_move(self, x, y):
        self.macro_events["events"].append(
            {"type": "cursorMove", "x": x, "y": y, "timestamp": time() - self.time}
        )
        self.time = time()

    def __on_click(self, x, y, button, pressed):
        if button == Button.left:
            self.macro_events["events"].append(
                {
                    "type": "leftClickEvent",
                    "x": x,
                    "y": y,
                    "timestamp": time() - self.time,
                    "pressed": pressed,
                }
            )
        elif button == Button.right:
            self.macro_events["events"].append(
                {
                    "type": "rightClickEvent",
                    "x": x,
                    "y": y,
                    "timestamp": time() - self.time,
                    "pressed": pressed,
                }
            )
        elif button == Button.middle:
            self.macro_events["events"].append(
                {
                    "type": "middleClickEvent",
                    "x": x,
                    "y": y,
                    "timestamp": time() - self.time,
                    "pressed": pressed,
                }
            )
        self.time = time()

    def __on_scroll(self, x, y, dx, dy):
        self.macro_events["events"].append(
            {"type": "scrollEvent", "dx": dx, "dy": dy, "timestamp": time() - self.time}
        )
        self.time = time()

    def __on_press(self, key):
        keyPressed = getKeyPressed(self.keyboard_listener, key)
        if self.keyboardBeingListened:
            self.macro_events["events"].append(
                {
                    "type": "keyboardEvent",
                    "key": keyPressed,
                    "timestamp": time() - self.time,
                    "pressed": True,
                }
            )
            self.time = time()

    def __on_release(self, key):
        keyPressed = getKeyPressed(self.keyboard_listener, key)
        if self.keyboardBeingListened:
            self.macro_events["events"].append(
                {
                    "type": "keyboardEvent",
                    "key": keyPressed,
                    "timestamp": time() - self.time,
                    "pressed": False,
                }
            )
            self.time = time()