@echo off
setlocal

REM Check if Python is installed
where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo ❗ Python is not installed. Please install Python 3.8 or newer.
    exit /b 1
)

REM Check if pipx is installed
where pipx >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo 🔄 Installing pipx...
    python -m pip install pipx
    python -m pipx ensurepath
    echo ❗ Please close and reopen this window for pipx to be recognized.
    exit /b 1
)

REM Install easyeda2kicad via pipx
pipx install easyeda2kicad
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


REM Set KiCad path to Documents
set KICA_FOLDER_PATH=%USERPROFILE%\Documents\KiCAD\EasyEDA2KiCAD
if not exist "%KICA_FOLDER_PATH%" mkdir "%KICA_FOLDER_PATH%"
set KICAD_PATH=%KICA_FOLDER_PATH%\easyeda2kicad
if not exist "%KICAD_FOLDER_PATH%" mkdir "%KICAD_FOLDER_PATH%"

REM Download initial symbol (C7272)
easyeda2kicad --lcsc_id C5364646 --full --overwrite --output "%KICAD_PATH%"

REM Success message
echo ✅ EasyEDA2KiCAD setup complete! Library created in: %KICAD_PATH%

REM Run the configuration script for KiCAD paths
python "%~dp0easyeda2kicad_config_kicad.py"
IF %ERRORLEVEL% NEQ 0 (
    echo ❗ Failed to configure KiCAD paths. Please check your Python environment.
    exit /b 1
)

echo ✅ KiCAD paths configured!
endlocal
