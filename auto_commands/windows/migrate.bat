@echo off
call ..\..\Scripts\activate.bat
python ..\scripts\migrate.py
pause