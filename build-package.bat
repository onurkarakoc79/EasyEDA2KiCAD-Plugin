@echo off
setlocal

REM Check for Python installation
where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo ❗ Python is not installed. Please install Python 3.8 or newer.
    exit /b 1
)

REM Install easyeda2kicad dependency
echo 🔄 Installing easyeda2kicad...
pip install easyeda2kicad
IF %ERRORLEVEL% NEQ 0 (
    echo ❗ Failed to install easyeda2kicad. Please check your Python environment.
    exit /b 1
)

REM Clean old build if exists
if exist build rmdir /s /q build

REM Create necessary directories
mkdir build\resources
mkdir build\plugins

REM Copy essential files
copy metadata.json build\
copy *.py build\plugins\
copy icon.png build\plugins\
copy icon-64x64.png build\resources\icon.png

REM Build the plugin package
cd build
powershell Compress-Archive -Path * -DestinationPath ../easyeda2kicad-plugin.zip

REM Success message
echo ✅ Build complete! Package created: easyeda2kicad-plugin.zip

REM End
endlocal
