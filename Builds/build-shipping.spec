# -*- mode: python -*-
import os

block_cipher = None

a = Analysis(['../main.py'],
             pathex=['W:\\Git\\B-Blue'],
             binaries=[],
             datas=[('../Resources/Icons/*.png', 'Resources/Icons')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='B-Blue4',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          # uac_admin=True,
          icon='W:\\Git\\B-Blue\\Resources\\light-bulb-icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='BBlue4')
