# PyMacroRecord
PyMacroRecord is a completely free Macro Recorder, coded with Python.

<a href="https://github.com/LOUDO56/PyMacroRecord/releases"><img alt="PyMacroRecord count download" src="https://img.shields.io/github/downloads/LOUDO56/PyMacroRecord/total?label=GitHub%20Downloads"/></a>

# Overview
PyMacroRecord works with a GUI made using tkinter, making it easier for users to interact with it.
![image](https://github.com/LOUDO56/PyMacroRecord/assets/117168736/2a1b2d0e-d950-40ad-84e2-971464058664)

# Features
- Very Easy to use
- Free. No limitations. No "premium" purchase.
- You can set an infinite amount of repeats.
- You can change the speed of your record.
- You can put interval in your playbacks
- You can save your record.
- You can load your record.
- You can share your record with other people.
- Universal Files (work with .json).
- After-playback options, e.g., Standby or shutdown computer.
- Can choose from recording mouse movement, click and keyboard input
- Custom Hotkey for starting a record and stop it, start playback and stop it
- Mouse Movement, click, and keyboard recording.
- Smooth recording of the mouse.

# How does this work?
To start recording, you simply have to press the red button\
From there, you can move your mouse, click, and type on your keyboard, and everything will be recorded. (You can choose what will be recorded.)
\
\
Then, to stop the recording, you simply click on the black square\
To play a recording, you just need to click on the green play icon
And to stop the playback, press the `f3` key (By default).
\
\

# Showcase

## Windows






https://github.com/LOUDO56/PyMacroRecord/assets/117168736/ac77b7b6-02d0-4c12-a71a-65119c4acc59


## macOS






https://github.com/LOUDO56/PyMacroRecord/assets/117168736/a4c57156-514c-46bf-9bb1-5e030df00726





## Linux






https://github.com/LOUDO56/PyMacroRecord/assets/117168736/25ab7c60-9f48-425f-bd5f-68c8b76e4c9c







# For bug reports or update requests
If you encounter a bug or want to request an update, simply create an issue [here](https://github.com/LOUDO56/PyMacroRecord/issues)

# For people who don't have windows or don't want to use exe file
- First, if you didn't already, install [Python](https://www.python.org/downloads/)
- Download the last source code release [here](https://github.com/LOUDO56/PyMacroRecord/releases)

- Extract it wherever you want.
- Open the terminal and type `cd <PATH TO SOFTWARE FOLDER>`
- Type the command:
  ```bash
  pip3 install -r requirements.txt
  ```
  - If you are on **Linux**, you might need to install Tkinter manually, commands to install are [here](https://www.geeksforgeeks.org/how-to-install-tkinter-on-linux/)
  - You need to remove the **win10toast** from `requirements.txt` or else you won't be able to install the depedencies
  - Mac Users, you must add python app to accessibility settings in system preferences to allow input monitoring.
  - (Optional) If you want these package to be on virtual environment follow these step [here](https://stackoverflow.com/a/41799834)
- Finally, do `cd src` and type: `python3 main.py`
- And boom! The software is now ready to use.

# Build (Windows)
To build the application, I use PyInstaller.

You need to be on home directory, not on src.

Then, use that command for onefile output (upx is optional).
```
pyinstaller --noconfirm --onefile --windowed --icon "src/assets/logo.ico" --name "PyMacroRecord-portable" --contents-directory "." --upx-dir upx --add-data "src/assets;assets/" --add-data "src/hotkeys;hotkeys/" --add-data "src/macro;macro/" --add-data "src/utils;utils/" --add-data "src/windows;windows/"  "src/main.py"
```

For onedir output, use that command (upx is optional).

```
pyinstaller --noconfirm --onedir --windowed --icon "src/assets/logo.ico" --name "PyMacroRecord" --contents-directory "." --upx-dir upx --add-data "src/assets;assets/" --add-data "src/hotkeys;hotkeys/" --add-data "src/macro;macro/" --add-data "src/utils;utils/" --add-data "src/windows;windows/"  "src/main.py"
```

# License

This program is under [GNU General Public License v3.0](https://github.com/LOUDO56/PyMacroRecord/blob/main/LICENSE.md)

# Special Thanks

- Fooinys, who playtested my program!
- Lenoch, for code enhancement!
