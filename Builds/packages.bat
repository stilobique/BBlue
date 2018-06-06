REM Generate the Shipping release
pyinstaller --noconfirm ^
    --noconsole ^
    --uac-admin ^
	--distpath %CD% ^
     %CD%/build-shipping.spec

rmdir /S /Q build

Set ZNAME="B-Blue4.zip"
Set ARCHIVE=%CD%"\BBlue4\"

echo %ARCHIVE%

E:\Tools\7-Zip\7z.exe a %ZNAME% %ARCHIVE%

rmdir /S /Q "BBlue4"

REM Generate the debug release

pyinstaller --noconfirm ^
    --noconsole ^
    --uac-admin ^
	--distpath %CD% ^
     %CD%/build-debug.spec

rmdir /S /Q build

Set ZNAME="B-Blue4-debug.zip"
Set ARCHIVE=%CD%"\BBlue4-debug\"

echo %ARCHIVE%

E:\Tools\7-Zip\7z.exe a %ZNAME% %ARCHIVE%

rmdir /S /Q "BBlue4-debug"
