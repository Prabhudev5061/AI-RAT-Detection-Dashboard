@echo off
title AI RAT Detection Dashboard - Development Launcher
cd /d "%~dp0"

if exist ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
) else if exist "..\.venv\Scripts\activate.bat" (
    call "..\.venv\Scripts\activate.bat"
) else if exist "..\..\.venv\Scripts\activate.bat" (
    call "..\..\.venv\Scripts\activate.bat"
)

python desktop_app.py
if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
)
