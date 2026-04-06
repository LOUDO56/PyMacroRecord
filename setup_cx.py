import sys
from cx_Freeze import Executable, setup

packages = [
    "tkinter",
    "PIL",
    "pynput",
    "pynput.keyboard",
    "pynput.mouse",
]

if sys.platform == "linux":
    packages += [
        "pynput.keyboard._xorg",
        "pynput.mouse._xorg",
        "Xlib",
        "Xlib.ext",
        "Xlib.ext.xfixes",
        "Xlib.ext.xtest",
        "Xlib.ext.xinput",
        "Xlib.keysymdef",
        "Xlib.support",
        "Xlib.support.unix_connect",
    ]
elif sys.platform == "win32":
    packages += [
        "pynput.keyboard._win32",
        "pynput.mouse._win32",
    ]

packages += ["pystray"]
excludes = []

include_files = [
    ("src/assets", "assets"),
    ("src/langs", "langs"),
    ("src/hotkeys", "hotkeys"),
    ("src/macro", "macro"),
    ("src/utils", "utils"),
    ("src/windows", "windows"),
]

build_exe_options = {
    "packages": packages,
    "excludes": excludes,
    "include_files": include_files,
}

target = Executable(
    script="src/main.py",
    base="gui" if sys.platform == "win32" else None,
    target_name="PyMacroRecord",
    icon="src/assets/logo.ico",
)

setup(
    name="PyMacroRecord",
    version="1.0",
    options={"build_exe": build_exe_options},
    executables=[target],
)
