import sys
from os import path
from pathlib import Path


def resource_path(relative_path: (str, list)) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS

    else:
        base_path = Path(__file__).parent.parent

    if not isinstance(relative_path, list):
        relative_path = [relative_path]

    for sub_path in relative_path:
        base_path = path.join(base_path, sub_path)

    return base_path
