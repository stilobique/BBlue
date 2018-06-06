# -*- mode: python -*-
import os

block_cipher = None

# path = os.path.dirname(os.path.realpath(%CD%))
# print(path)

a = Analysis(['../main.py'],
             pathex=['E:\\WORKS\\Git\\Tools\\BBlue'],
             # pathex=[path],
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
          debug=True,
          strip=False,
          upx=True,
          console=True,
          # uac_admin=True,
          icon='E:\\WORKS\\Git\\Tools\\BBlue\\Resources\\light-bulb-icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='BBlue4')
