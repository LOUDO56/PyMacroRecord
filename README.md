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

## Linux (X11)

https://github.com/LOUDO56/PyMacroRecord/assets/117168736/25ab7c60-9f48-425f-bd5f-68c8b76e4c9c


# For bug reports or update requests
If you encounter a bug or want to request an update, simply create an issue [here](https://github.com/LOUDO56/PyMacroRecord/issues)

# Running from source

- First, install [Python](https://www.python.org/downloads/)
- Download the last source code release [here](https://github.com/LOUDO56/PyMacroRecord/releases)
- Extract it wherever you want.
- Open the terminal and type `cd <PATH TO SOFTWARE FOLDER>`
- Install dependencies:
  ```bash
  pip3 install -r requirements.txt
  ```
  - On **Linux**, you might need to install Tkinter manually: `sudo apt install python3-tk` (or equivalent for your distro)
  - On **Linux**, the app requires an **X11** session. Wayland is not supported.
- Run:
  ```bash
  cd src && python3 main.py
  ```

# Build

The project uses **cx_Freeze** to build the application.

## Linux (AppImage)

Requirements: `cx_Freeze`, `imagemagick` (`convert`), `curl`

```bash
./build.sh
```

This will produce a `PyMacroRecord-x86_64.AppImage` (or the current arch) in the project root.

> **Note:** The AppImage runs in X11 mode only. Wayland is not supported because the mouse can't leave the current window.

## Windows

Requirements: `cx_Freeze`

```bash
python setup_cx.py build
```

The output will be in the `build/` directory.

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
- <a href="https://github.com/expp121">expp121</a> for the Bulgarian translation
- <a href="https://github.com/LOUDO56/PyMacroRecord/issues?q=is%3Apr+author%3ADvaMishkiLapa">DvaMishkiLapa</a> for the Russian translation.
