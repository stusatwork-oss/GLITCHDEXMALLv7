@echo off
REM GLITCHDEX MALL ENGINE - Distribution Package Creator
REM Creates a ZIP file ready to share with others

echo.
echo ===============================================
echo Glitchdex Mall - Distribution Package Creator
echo ===============================================
echo.

REM Check if executable exists
if not exist "dist\glitchdex-mall\glitchdex-mall.exe" (
    echo ERROR: Executable not found!
    echo.
    echo Please run build_windows.bat first to build the executable.
    echo.
    pause
    exit /b 1
)

echo [1/3] Preparing distribution package...

REM Create distribution directory
if exist "dist_package" rmdir /s /q dist_package
mkdir dist_package\glitchdex-mall

echo [2/3] Copying files...

REM Copy executable and dependencies
xcopy /E /I "dist\glitchdex-mall" "dist_package\glitchdex-mall" >nul

REM Copy README and docs
copy README.md "dist_package\glitchdex-mall\" >nul
copy BUILD_AND_DISTRIBUTE.md "dist_package\glitchdex-mall\" >nul

echo [3/3] Creating ZIP file...

REM Create ZIP using built-in Windows compression
cd dist_package
powershell -Command "Compress-Archive -Path glitchdex-mall -DestinationPath ..\glitchdex-mall-v1.0.zip -Force"
cd ..

echo.
echo ===============================================
echo DISTRIBUTION PACKAGE CREATED!
echo ===============================================
echo.
echo File: glitchdex-mall-v1.0.zip
echo Size: %~z"glitchdex-mall-v1.0.zip" bytes
echo.
echo You can now share this ZIP file with others!
echo They can extract and play immediately (no installation needed).
echo.
pause
