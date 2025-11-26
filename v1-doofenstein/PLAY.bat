@echo off
REM GLITCHDEX MALL - Windows Launcher
REM Just run the game. No configuration. No complexity.

echo.
echo ═══════════════════════════════════════════════════════════════════════
echo GLITCHDEX MALL ENGINE
echo ═══════════════════════════════════════════════════════════════════════
echo.

REM Check if Python exists
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo.
    echo Please install Python 3.8+ from https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM Run the launcher (cursed shareware CD menu)
echo Starting GAMEZILLA MEGA COLLECTION launcher...
echo.

python src/launcher.py

pause
