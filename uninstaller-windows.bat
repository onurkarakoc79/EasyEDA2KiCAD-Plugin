@echo off
setlocal

REM Uninstall easyeda2kicad from pipx
where pipx >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo ❗ pipx is not installed. Cannot proceed with uninstallation.
    pause
    exit /b 1
)

pipx uninstall easyeda2kicad
IF %ERRORLEVEL% NEQ 0 (
    echo ❗ Failed to uninstall easyeda2kicad. Please check your Python environment.
    pause
)



REM Run Python script to clean KiCad paths
python "%~dp0easyeda2kicad_deconfig.py"
IF %ERRORLEVEL% NEQ 0 (
    echo ❗ Failed to clean KiCad paths. Please check your Python environment.
    pause
    exit /b 1
)

REM Remove plugin files and directories
set KICA_FOLDER_PATH=%USERPROFILE%\Documents\KiCAD\EasyEDA2KiCAD
if exist "%KICA_FOLDER_PATH%" rmdir /s /q "%KICA_FOLDER_PATH%"

REM Remove zip file and build directory
if exist easyeda2kicad-plugin.zip del easyeda2kicad-plugin.zip
if exist build rmdir /s /q build


REM Completion message
echo ✅ EasyEDA2KiCAD uninstallation complete. All plugin files and configurations have been removed.
pause
endlocal