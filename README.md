# Airbnb camera scanner

Python app that scan for cameras.

## Screenshots

![Application screenshot](./screenshots/screenshot-airbnb-scanner-2.png "Boo")

Note: Show you device's company name but doesn't warn you yet about possible recording devices.

Here : Mi Home Security Camera 360° 1080P by Xiaomi.

## Dev

```
pip install -r requirements.txt
```

## Notes

### Scapy root privileges needed.

https://stackoverflow.com/questions/20763039/creating-raw-socket-in-python-without-root-privileges

https://stackoverflow.com/questions/36215201/python-scapy-sniff-without-root

```
setcap cap_net_raw=eip venv/bin/python3.6
```

But also we need `$XDG_RUNTIME_DIR` to match the user folder so no root to see the tray icon.

----

### Packaging with pyqtdeploy

Error :
```
_ctypes.c:107:10: fatal error: ffi.h: No such file or directory
```
Answer :
```
sudo apt install libffi-dev
```

----

### Release

It takes too long to build in CI. Instead builds are being done locally on my computer (maybe for the best).
```
make release TAG=v0.x.x
```

Using semver standard.
