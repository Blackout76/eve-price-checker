# -*- mode: python -*-

block_cipher = None


a = Analysis(['app.py'],
             pathex=['C:\\Windows\\WinSxS\\amd64_avg.vc140.crt_f92d94485545da78_14.0.24210.0_none_69fa0197d9b096ae', 'E:\\Projets\\Projects_EvE_Online\\EvE price checker'],
             binaries=[],
             datas= [ ('sounds/*.wav', 'sounds' ), ('win10toast/data/python.ico', 'win10toast/data' )],
             hiddenimports=['win10toast','playsound'],
             hookspath=['.'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='app.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='app')
