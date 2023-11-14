@echo off
poetry run pyinstaller main.spec --clean --noconfirm --distpath .
move output\Onmyoji_Python.exe .
rmdir /s /q "lib"
move output\lib .
rmdir /s /q "output"
pause