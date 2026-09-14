@echo off
title AI RAT Detection Dashboard - Test Suite
cd /d "%~dp0"

if exist ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
) else if exist "..\.venv\Scripts\activate.bat" (
    call "..\.venv\Scripts\activate.bat"
) else if exist "..\..\.venv\Scripts\activate.bat" (
    call "..\..\.venv\Scripts\activate.bat"
)

pytest tests/ -v
if errorlevel 1 (
    echo.
    echo Tests encountered failures.
    pause
)
