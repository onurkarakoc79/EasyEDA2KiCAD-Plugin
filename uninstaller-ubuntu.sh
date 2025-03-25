#!/bin/bash

# Ensure script exits if any command fails
set -e

# Uninstall easyeda2kicad via pipx
if ! command -v pipx &> /dev/null; then
    echo "❗ pipx is not installed. Cannot proceed with uninstallation."
    exit 1
fi



# Remove plugin files and directories
KICAD_FOLDER_PATH="$HOME/Documents/KiCAD/EASYEDA2KICAD"
if [ -d "$KICAD_FOLDER_PATH" ]; then
    rm -rf "$KICAD_FOLDER_PATH"
    echo "✅ EASYEDA2KICAD folder removed."
fi

# Run Python script to clean KiCad paths
python3 "$(dirname "$0")/easyeda2kicad_deconfig.py" || {
    echo "❗ Failed to clean KiCad paths. Please check your Python environment."
    exit 1
}


pipx uninstall easyeda2kicad || { echo "❗ Failed to uninstall easyeda2kicad."; exit 1; }

# Remove the generated zip file
ZIP_FILE="$(dirname "$0")/easyeda2kicad-plugin.zip"
if [ -f "$ZIP_FILE" ]; then
    rm "$ZIP_FILE"
    echo "✅ easyeda2kicad-plugin.zip deleted."
fi

rm -rf build
echo "✅ Build directory removed."

# Completion message
echo "✅ EasyEDA2KiCAD uninstallation complete. All plugin files and configurations have been removed."
