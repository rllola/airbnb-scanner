# Airbnb camera scanner

Python app that scan for cameras.

## Dev

### With Virtualenv (Recommended)

#### Windows

```
$ virtualenv.exe .venv
$ .venv\Scripts\activate.bat
```

https://scapy.readthedocs.io/en/latest/installation.html#windows

#### Posix systems

```
$ virtualenv .venv
* source .venv\bin\activate
```

### Install dependencies

```
pip install -r requirements.txt
```

## Notes

### Scapy on linux

Scapy root privileges needed.

https://stackoverflow.com/questions/20763039/creating-raw-socket-in-python-without-root-privileges

https://stackoverflow.com/questions/36215201/python-scapy-sniff-without-root

```
setcap cap_net_raw=eip .venv/bin/python3.6
```

But also we need `$XDG_RUNTIME_DIR` to match the user folder so no root to see the tray icon.

### PyQt5 5.13 + pyinstaller broken

https://github.com/pyinstaller/pyinstaller/issues/4293

Temporarly fixed to version 5.12.2
