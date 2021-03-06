REM Generate the Shipping release
pyinstaller --noconfirm ^
	--distpath %CD% ^
     %CD%/build-shipping.spec

rmdir /S /Q build

Set ZNAME="B-Blue4.zip"
Set ARCHIVE=%CD%"/BBlue4/"

echo %ARCHIVE%

S:\7-Zip\7z.exe a %ZNAME% %ARCHIVE%

rmdir /S /Q "BBlue4"

REM Generate the debug release

pyinstaller --noconfirm ^
	--distpath %CD% ^
     %CD%/build-debug.spec

rmdir /S /Q build

Set ZNAME="B-Blue4-debug.zip"
Set ARCHIVE=%CD%"/BBlue4-debug/"

echo %ARCHIVE%

S:\7-Zip\7z.exe a %ZNAME% %ARCHIVE%

rmdir /S /Q "BBlue4-debug"
