# -*- mode: python -*-

from PyInstaller.utils.hooks import collect_data_files
from sys import platform
import os

block_cipher = None

datas = Tree('data', prefix='data', excludes=[])
datas += Tree('icons', prefix='icons', excludes=[])

a = Analysis(['src/main.py'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

icon = None

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='AirbnbScanner',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          icon=icon,
          console=True )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               datas,
               strip=False,
               upx=True,
               name='AirbnbScanner')
