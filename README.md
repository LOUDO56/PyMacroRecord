# PyMacroRecord
<div align="center">
  <a href="https://github.com/LOUDO56/PyMacroRecord/releases"><img src="https://github.com/LOUDO56/PyMacroRecord/assets/117168736/ff16ba4d-7979-4719-bb8f-78587cb5032f" alt="pmr logo"></a>
  <p>
    Free. Easy <br>
    Coded with Python, PyMacroRecord is one of the best free macro recorder you will find. <br>
    No <b>ads</b>, no <b>premium</b>, everything <b>FREE</b>
  </p>
  <a href="https://github.com/LOUDO56/PyMacroRecord/releases"><img alt="PyMacroRecord count download" src="https://img.shields.io/github/downloads/LOUDO56/PyMacroRecord/total?label=Downloads"/></a>
</div>


# Overview
PyMacroRecord works with a GUI made using tkinter, making it easier for users to interact with it.
![image](https://github.com/LOUDO56/PyMacroRecord/assets/117168736/2a1b2d0e-d950-40ad-84e2-971464058664)

# Features
- Very easy to use
- Free. No limitations. No "premium" purchase.
- Infinite repeat
- Change speed
- Interval
- For
- Schedule
- Save, Load, Sharing
- Universal Files (work with json).
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
Then, to stop the recording, you simply click on the black square.\
To play a recording, you just need to click on the green play icon
And to stop the playback, press the `f3` key (By default).


# Showcase

## Windows






https://github.com/LOUDO56/PyMacroRecord/assets/117168736/ac77b7b6-02d0-4c12-a71a-65119c4acc59


## macOS





https://github.com/LOUDO56/PyMacroRecord/assets/117168736/2e8d8a85-c96b-4906-b8d9-b91de2c3d35b








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
  - Mac Users, you must add terminal to accessibility and input monitoring settings in system preferences to allow mouse and keyboard inputs.
  - (Optional) If you want these package to be on virtual environment follow these step [here](https://stackoverflow.com/a/41799834)
- Finally, do `cd src` and type: `python3 main.py`
- And boom! The software is now ready to use.

# Build (Windows)
To build the application, I use PyInstaller.

You need to be on home directory, not on src.

Then, use that command for onefile output (upx is optional).
```
pyinstaller --noconfirm --onefile --windowed --icon "src/assets/logo.ico" --name "PyMacroRecord-portable" --contents-directory "." --upx-dir upx --add-data "src/assets;assets/" --add-data "src/hotkeys;hotkeys/" --add-data "src/macro;macro/" --add-data "src/utils;utils/" --add-data "src/windows;windows/" --add-data "src/langs;langs"  "src/main.py"
```

For onedir output, use that command (upx is optional).

```
pyinstaller --noconfirm --onedir --windowed --icon "src/assets/logo.ico" --name "PyMacroRecord" --contents-directory "." --upx-dir upx --add-data "src/assets;assets/" --add-data "src/hotkeys;hotkeys/" --add-data "src/macro;macro/" --add-data "src/utils;utils/" --add-data "src/langs;langs" --add-data "src/windows;windows/"  "src/main.py"
```

# Support
Developing a software is not an easy task. If you really like this project, please consider making a small donation, it really helps and means a lot! <3
\
\
By making a donation, your name will appear in the "Donors" section of the PyMacroRecord software and among the last 5 donors on the [PyMacroRecord](https://www.pymacrorecord.com) website as a thank you!
\
\
<a href='https://ko-fi.com/loudo' target='_blank'><img height='35' style='border:0px;height:46px;' src='https://az743702.vo.msecnd.net/cdn/kofi3.png?v=0' border='0' alt='Buy Me a Coffee at ko-fi.com' />

# License

This program is under [GNU General Public License v3.0](https://github.com/LOUDO56/PyMacroRecord/blob/main/LICENSE.md)

# Special Thanks

- Fooinys, who playtested my program.
- <a href="https://github.com/Lenochxd">Lenoch</a>, for code enhancement.
- <a href="https://github.com/takiem">Takiem</a> for the Italian and Brazilian-Portuguese translation.
- <a href="https://github.com/DennyClarkson">DennyClarkson</a> for the Chinese-Simplified translation.
- <a href="https://github.com/SerdarSaglam">SerdarSaglam</a> for the Turkish translation.
- <a href="https://github.com/superstes">superstes</a> for the German translation.
- <a href="https://github.com/SqlWaldorf">SqlWaldorf</a> for the Dutch translation.
- <a href="https://github.com/jorge-sepulveda">jorge-sepulveda</a> for the Spanish translation.
- <a href="https://github.com/expp121">expp121</a> for the Bulgarian translation.
