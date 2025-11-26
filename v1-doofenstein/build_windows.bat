@echo off
REM GLITCHDEX MALL ENGINE - Windows Build Script
REM This script builds a standalone executable for Windows

setlocal enabledelayedexpansion

echo.
echo ===============================================
echo GLITCHDEX MALL ENGINE - Windows Builder
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/5] Python found. Installing build dependencies...
pip install -r requirements-build.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/5] Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo.
echo [3/5] Building executable (this may take a minute)...
pyinstaller glitchdex_mall.spec
if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo [4/5] Build complete!
echo.
echo [5/5] The executable is in: dist\glitchdex-mall.exe
echo.

echo ===============================================
echo BUILD SUCCESSFUL!
echo ===============================================
echo.
echo Your game is ready to play!
echo Location: dist\glitchdex-mall.exe
echo.
echo Optional: You can now create a desktop shortcut to dist\glitchdex-mall.exe
echo for easy access.
echo.
pause
