@echo off
title DEAD AIR - EXE Builder

cd /d "%~dp0"

echo ========================================
echo          DEAD AIR BUILD SCRIPT
echo ========================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found.
    echo Create it first with: python -m venv .venv
    pause
    exit /b 1
)

echo Installing PyInstaller...
".venv\Scripts\python.exe" -m pip install pyinstaller

if errorlevel 1 (
    echo ERROR: Could not install PyInstaller.
    pause
    exit /b 1
)

echo.
echo Building DEAD AIR...
echo.

".venv\Scripts\python.exe" -m PyInstaller ^
    --noconfirm ^
    --clean ^
    --windowed ^
    --onedir ^
    --name "DEAD AIR" ^
    --paths src ^
    --add-data "src/dead_air/assets;dead_air/assets" ^
    --add-data "src/dead_air/data;dead_air/data" ^
    src/dead_air/main.py

if errorlevel 1 (
    echo.
    echo BUILD FAILED.
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo.
echo Your executable is here:
echo dist\DEAD AIR\DEAD AIR.exe
echo.

pause