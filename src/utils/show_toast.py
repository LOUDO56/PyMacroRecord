from os import system, path
from sys import platform
from utils.get_file import resource_path
try:
    from win10toast import ToastNotifier
except:
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

    elif platform == "Linux" or platform == "linux":
        system("""notify-send -u normal "PyMacroRecord" "PyMacroRecord has been minimized" """)
    elif platform == "Darwin" or platform == "darwin":
        system("""display notification "PyMacroRecord has been minimized" with title "PyMacroRecord""")
    else:
        pass