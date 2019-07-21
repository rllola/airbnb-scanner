# Airbnb camera scanner

Python app that scan for cameras.

## Dev

```
pip install -r requirements.txt
```

## Notes

Scapy root privileges needed.

https://stackoverflow.com/questions/20763039/creating-raw-socket-in-python-without-root-privileges

https://stackoverflow.com/questions/36215201/python-scapy-sniff-without-root

```
setcap cap_net_raw=eip .venv/bin/python3.6
```

But also we need `$XDG_RUNTIME_DIR` to match the user folder so no root to see the tray icon.
