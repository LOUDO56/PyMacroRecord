from datetime import datetime
from os import getlogin, system
from sys import platform
from threading import Thread
from time import time, sleep
from tkinter import *
from tkinter import messagebox
from pynput.keyboard import Key # FUTURE SELF: DON'T REMOVE THIS!!
from pynput import mouse, keyboard
from pynput.mouse import Button
from utils.get_key_pressed import getKeyPressed
from utils.keys import vk_nb
from utils.record_file_management import RecordFileManagement
from utils.show_toast import show_notification_minim
from utils.warning_pop_up_save import confirm_save


class Macro:
    """Init a new Macro"""

    def __init__(self, main_app):
        self.showEventsOnStatusBar = None
        self.mouseControl = mouse.Controller()
        self.keyboardControl = keyboard.Controller()
        self.record = False
        self.playback = False
        self.macro_events = {}
        self.main_app = main_app
        self.user_settings = self.main_app.settings
        self.main_menu = self.main_app.menu
        self.macro_file_management = RecordFileManagement(self.main_app, self.main_menu)

        self.mouseBeingListened = None
        self.keyboardBeingListened = None
        self.keyboard_listener = None
        self.mouse_listener = None
        self.time = time()
        self.event_delta_time=0

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
        self.event_delta_time=0
        userSettings = self.user_settings.settings_dict
        self.showEventsOnStatusBar = userSettings["Recordings"]["Show_Events_On_Status_Bar"]
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
        userSettings = self.user_settings.settings_dict
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
        userSettings = self.user_settings.settings_dict
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
        userSettings = self.user_settings.settings_dict
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
        userSettings = self.user_settings.settings_dict
        debut = time()
        while self.playback and (time() - debut) < userSettings["Playback"]["Repeat"]["For"]:
            self.__play_events()
        if userSettings["Playback"]["Repeat"]["Interval"] == 0:
            self.stop_playback()

    def __play_events(self):
        global keyToPress
        userSettings = self.user_settings.settings_dict
        click_func = {
            "leftClickEvent": Button.left,
            "rightClickEvent": Button.right,
            "middleClickEvent": Button.middle,
        }
        keyToUnpress = []

        is_infinite = userSettings["Playback"]["Repeat"].get("Infinite", False)

        if userSettings["Playback"]["Repeat"]["For"] > 0:
            repeat_times = 1
        elif is_infinite:
            repeat_times = float('inf')
        else:
            repeat_times = userSettings["Playback"]["Repeat"]["Times"]

        if userSettings["Playback"]["Repeat"]["Scheduled"] > 0:
            now = datetime.now()
            seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
            secondsToWait = userSettings["Playback"]["Repeat"]["Scheduled"] - seconds_since_midnight
            if secondsToWait < 0:
                secondsToWait = 86400 + secondsToWait  # 86400 + -secondsToWait. Meaning it will happen tomorrow
            sleep(secondsToWait)

        repeat_count = 0
        now = time()

        while self.playback and (is_infinite or repeat_count < repeat_times):
            for events in range(len(self.macro_events["events"])):
                elapsed_time = int(time() - now)
                self.main_app.status_text.configure(
                    text=f"Repeat: {repeat_count + 1}/{repeat_times}, Time elapsed: {elapsed_time}s")
                if not self.playback:
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
                    if self.macro_events["events"][events]["pressed"]:
                        self.mouseControl.press(click_func[event_type])
                    else:
                        self.mouseControl.release(click_func[event_type])

                elif event_type == "scrollEvent":
                    self.mouseControl.scroll(
                        self.macro_events["events"][events]["dx"],
                        self.macro_events["events"][events]["dy"],
                    )

                elif event_type == "keyboardEvent":  # Keyboard Press,Release
                    if self.macro_events["events"][events]["key"] is not None:
                        try:
                            if "Key." not in self.macro_events["events"][events]["key"]:
                                keyToPress = self.macro_events["events"][events]["key"]
                            else:
                                keyToPress = eval(self.macro_events["events"][events]["key"])
                            if isinstance(keyToPress, str):
                                if ">" in keyToPress:
                                    try:
                                        keyToPress = vk_nb[keyToPress]
                                    except:
                                        keyToPress = None
                            if self.playback:
                                if keyToPress is not None:
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
                            messagebox.showerror("Error",
                                                 f"Error during playback \"{e}\". Please open an issue on Github.")
                            self.stop_playback()
                        except Exception as e:
                            messagebox.showerror("Error",
                                                 f"An unexpected error occurred\n{e}")
                            self.stop_playback()


            repeat_count += 1

            if userSettings["Playback"]["Repeat"]["Delay"] > 0:
                if is_infinite or repeat_count < repeat_times:
                    sleep(userSettings["Playback"]["Repeat"]["Delay"])

        self.unPressEverything(keyToUnpress)
        if userSettings["Playback"]["Repeat"]["Interval"] == 0 and userSettings["Playback"]["Repeat"]["For"] == 0 and repeat_count:
            self.stop_playback()
            if userSettings["Minimization"]["When_Playing"]:
                self.main_app.deiconify()

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
        userSettings = self.user_settings.settings_dict
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

    def __record_event(self,e):
        e['timestamp'] = self.event_delta_time
        self.macro_events["events"].append(e)

    def __get_event_delta_time(self):
        timenow=time()
        self.event_delta_time = timenow - self.time
        self.time=timenow

    def __on_move(self, x, y):
        self.__get_event_delta_time()
        self.__record_event(
            {"type": "cursorMove", "x": x, "y": y}
        )
        if self.showEventsOnStatusBar:
            self.main_app.status_text.configure(text=f"cursorMove {x} {y}")

    def __on_click(self, x, y, button, pressed):
        self.__get_event_delta_time()
        button_event = "unknownButtonClickEvent"
        if button == Button.left:
            button_event = "leftClickEvent"
        elif button == Button.right:
            button_event = "rightClickEvent"
        elif button == Button.middle:
            button_event = "middleClickEvent"
        self.__record_event(
            {
                "type": button_event,
                "x": x,
                "y": y,
                "pressed": pressed
            }
        )
        if self.showEventsOnStatusBar:
            self.main_app.status_text.configure(text=f"{button_event} {x} {y} {pressed}")

    def __on_scroll(self, x, y, dx, dy):
        self.__get_event_delta_time()
        self.__record_event(
            {"type": "scrollEvent", "dx": dx, "dy": dy}
        )
        if self.showEventsOnStatusBar:
            self.main_app.status_text.configure(text=f"scrollEvent {dx} {dy}")

    def __on_press(self, key):
        self.__get_event_delta_time()
        keyPressed = getKeyPressed(self.keyboard_listener, key)
        if self.keyboardBeingListened:
            self.__record_event(
                {
                    "type": "keyboardEvent",
                    "key": keyPressed,
                    "pressed": True,
                }
            )
        if self.showEventsOnStatusBar:
            self.main_app.status_text.configure(text=f"keyboardEvent {keyPressed} pressed")

    def __on_release(self, key):
        self.__get_event_delta_time()
        keyPressed = getKeyPressed(self.keyboard_listener, key)
        if self.keyboardBeingListened:
            self.__record_event(
                {
                    "type": "keyboardEvent",
                    "key": keyPressed,
                    "pressed": False,
                }
            )
        if self.showEventsOnStatusBar:
            self.main_app.status_text.configure(text=f"keyboardEvent {keyPressed} released")
