from os import path, system
from sys import platform
from utils.get_file import resource_path

try:
    from win10toast import ToastNotifier
except Exception:
    print("Not on windows. win10toast not imported.")


def show_notification_minim():
    if platform == "win32":
        from win10toast import ToastNotifier

        toast = ToastNotifier()
        try:
            toast.show_toast(
                title="PyMacroRecord minimized",
                msg="PyMacroRecord has been minimized",
                duration=3,
                icon_path=resource_path(path.join("assets", "logo.ico"))
            )
        except:
            pass

    elif "linux" in platform.lower():
        system("""notify-send -u normal "PyMacroRecord" "PyMacroRecord has been minimized" """)
    elif "darwin" in platform.lower():
        system("""osascript -e 'display notification "PyMacroRecord has been minimized" with title "PyMacroRecord"'""")
