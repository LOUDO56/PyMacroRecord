from tkinter import *
from tkinter import messagebox
from pynput import mouse, keyboard
from pynput.keyboard import Key
from pynput.mouse import Button
from utils.get_key_pressed import getKeyPressed
from utils.record_file_management import RecordFileManagement
from utils.warning_pop_up_save import confirm_save
from utils.show_toast import show_notification_minim
from utils.keys import vk_nb
from time import time, sleep
from os import getlogin, system
from sys import platform
from threading import Thread
from datetime import datetime



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

        self.keyboard_listener = keyboard.Listener(
                on_press=self.__on_press, on_release=self.__on_release
            )
        self.keyboard_listener.start()

    def start_record(self, by_hotkey=False):
        if self.main_app.prevent_record:
            return
        if not by_hotkey:
            if not self.main_app.macro_saved and self.main_app.macro_recorded:
                wantToSave = confirm_save(self.main_app)
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
            self.keyboardBeingListened = True
        self.main_menu.file_menu.entryconfig(self.main_app.text_content["file_menu"]["load_text"], state=DISABLED)
        self.main_app.recordBtn.configure(
            image=self.main_app.stopImg, command=self.stop_record
        )
        self.main_app.playBtn.configure(state=DISABLED)
        self.main_menu.file_menu.entryconfig(self.main_app.text_content["file_menu"]["save_text"], state=DISABLED)
        self.main_menu.file_menu.entryconfig(self.main_app.text_content["file_menu"]["save_as_text"], state=DISABLED)
        self.main_menu.file_menu.entryconfig(self.main_app.text_content["file_menu"]["new_text"], state=DISABLED)
        self.main_menu.file_menu.entryconfig(self.main_app.text_content["file_menu"]["load_text"], state=DISABLED)
        if userSettings["Minimization"]["When_Recording"]:
            self.main_app.withdraw()
            Thread(target=lambda: show_notification_minim(self.main_app)).start()
        print("record started")

    def stop_record(self):
        if not self.record:
            return
        userSettings = self.user_settings.get_config()
        self.record = False
        if self.mouseBeingListened:
            self.mouse_listener.stop()
            self.mouseBeingListened = False
        if self.keyboardBeingListened:
            self.keyboardBeingListened = False 
        self.main_app.recordBtn.configure(
            image=self.main_app.recordImg, command=self.start_record
        )
        self.main_app.playBtn.configure(state=NORMAL, command=self.start_playback)
        self.main_menu.file_menu.entryconfig(
            self.main_app.text_content["file_menu"]["save_text"], state=NORMAL, command=self.macro_file_management.save_macro
        )
        self.main_menu.file_menu.entryconfig(
            self.main_app.text_content["file_menu"]["save_as_text"], state=NORMAL, command=self.macro_file_management.save_macro_as
        )
        self.main_menu.file_menu.entryconfig(
            self.main_app.text_content["file_menu"]["new_text"], state=NORMAL, command=self.macro_file_management.new_macro
        )
        self.main_menu.file_menu.entryconfig(self.main_app.text_content["file_menu"]["load_text"], state=NORMAL)

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
        self.main_menu.file_menu.entryconfig(self.main_app.text_content["file_menu"]["save_text"], state=DISABLED)
        self.main_menu.file_menu.entryconfig(self.main_app.text_content["file_menu"]["save_as_text"], state=DISABLED)
        self.main_menu.file_menu.entryconfig(self.main_app.text_content["file_menu"]["new_text"], state=DISABLED)
        self.main_menu.file_menu.entryconfig(self.main_app.text_content["file_menu"]["load_text"], state=DISABLED)
        self.main_app.recordBtn.configure(state=DISABLED)
        if userSettings["Minimization"]["When_Playing"]:
            self.main_app.withdraw()
            Thread(target=lambda: show_notification_minim(self.main_app)).start()
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
        if userSettings["Playback"]["Repeat"]["Scheduled"] > 0:
            now = datetime.now()
            seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
            secondsToWait = userSettings["Playback"]["Repeat"]["Scheduled"] - seconds_since_midnight
            if secondsToWait < 0:
                secondsToWait = 86400 + secondsToWait # 86400 + -secondsToWait. Meaning it will happen tomorrow
            sleep(secondsToWait)
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
                if timeSleep < 0:
                    timeSleep = abs(timeSleep)
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
                        except ValueError as e:
                            if keyToPress == None:
                                pass
                            else:
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
        self.main_menu.file_menu.entryconfig(self.main_app.text_content["file_menu"]["save_text"], state=NORMAL)
        self.main_menu.file_menu.entryconfig(self.main_app.text_content["file_menu"]["save_as_text"], state=NORMAL)
        self.main_menu.file_menu.entryconfig(self.main_app.text_content["file_menu"]["new_text"], state=NORMAL)
        self.main_menu.file_menu.entryconfig(self.main_app.text_content["file_menu"]["load_text"], state=NORMAL)
        if userSettings["Minimization"]["When_Playing"]:
            self.main_app.deiconify()
        if userSettings["After_Playback"]["Mode"] != "Idle" and not playback_stopped_manually:
            if userSettings["After_Playback"]["Mode"].lower() == "standby":
                if platform == "win32":
                    system("rundll32.exe powrprof.dll, SetSuspendState 0,1,0")
                elif "linux" in platform.lower():
                    system("subprocess.callctl suspend")
                elif "darwin" in platform.lower():
                    system("pmset sleepnow")
            elif userSettings["After_Playback"]["Mode"].lower() == "log off computer":
                if platform == "win32":
                    system("shutdown /l")
                else:
                    system(f"pkill -KILL -u {getlogin()}")
            elif userSettings["After_Playback"]["Mode"].lower() == "turn off computer":
                if platform == "win32":
                    system("shutdown /s /t 0")
                else:
                    system("shutdown -h now")
            elif userSettings["After_Playback"]["Mode"].lower() == "restart computer":
                if platform == "win32":
                    system("shutdown /r /t 0")
                else:
                    system("shutdown -r now")
            elif userSettings["After_Playback"]["Mode"].lower() == "hibernate (if enabled)":
                if platform == "win32":
                    system("shutdown -h")
                elif "linux" in platform.lower():
                    system("systemctl hibernate")
                elif "darwin" in platform.lower():
                    system("pmset sleepnow")
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
