@echo off
call .venv\Scripts\activate
pyinstaller --noconfirm --onefile --windowed ^
    --icon "src/assets/logo.ico" ^
    --name "PyMacroRecord-portable" ^
    --contents-directory "." ^
    --upx-dir upx ^
    --add-data "src/assets;assets/" ^
    --add-data "src/langs;langs/" ^
    --add-data "src/hotkeys;hotkeys/" ^
    --add-data "src/macro;macro/" ^
    --add-data "src/utils;utils/" ^
    --add-data "src/windows;windows/" ^
    "src/main.py"
