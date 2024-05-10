@echo off
cls
pip install pyinstaller
cd executable
pyinstaller --onefile --icon=icon.ico --windowed ../main.py