#!/bin/bash

# Ensure script exits if any command fails
set -e

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❗ Python is not installed. Please install Python 3.8 or newer."
    exit 1
fi

# Check if pipx is installed
if ! command -v pipx &> /dev/null; then
    echo "🔄 Installing pipx..."
    sudo apt install pipx
    python3 -m pipx ensurepath
    echo "❗ Please restart your terminal session for pipx to be recognized."
    exit 1
fi

# Ensure correct path for pipx is added to PATH
pipx ensurepath

# Install easyeda2kicad via pipx
pipx install easyeda2kicad || { echo "❗ Failed to install easyeda2kicad. Please check your Python environment."; exit 1; }

# Clean old build if exists
rm -rf build

# Create necessary directories
mkdir -p build/resources
mkdir -p build/plugins

# Copy essential files
cp metadata.json build/
cp *.py build/plugins/
cp icon.png build/plugins/
cp icon-64x64.png build/resources/icon.png

# Build the plugin package
cd build
zip -r ../easyeda2kicad-plugin.zip ./*
cd ..

# Success message
echo "✅ Build complete! Package created: easyeda2kicad-plugin.zip"

# Set KiCad path to ~/Documents
KICAD_FOLDER_PATH="$HOME/Documents/KiCAD/EASYEDA2KICAD"
mkdir -p "$KICAD_FOLDER_PATH"
KICAD_PATH="$KICAD_FOLDER_PATH"

# Find correct easyeda2kicad path via pipx environment detection
EASYEDA2KICAD_PATH=$(pipx list | grep 'easyeda2kicad' | awk '{print $3 "/bin/easyeda2kicad"}')

# Fallback if primary method fails
if [ ! -f "$EASYEDA2KICAD_PATH" ]; then
    EASYEDA2KICAD_PATH=$(find ~/.local/share/pipx/venvs/easyeda2kicad/ -type f -name "easyeda2kicad" 2>/dev/null)
fi

# Check if path is found
if [ -z "$EASYEDA2KICAD_PATH" ]; then
    echo "❗ Could not find easyeda2kicad executable. Please ensure it is installed via pipx."
    exit 1
fi

# Download initial symbol (C7272)
"$EASYEDA2KICAD_PATH" --lcsc_id C7472 --full --overwrite --output "$KICAD_PATH/easyeda2kicad"

# Success message
echo "✅ EasyEDA2KiCAD setup complete! Library created in: $KICAD_PATH"

# Run the configuration script for KiCAD paths
python3 "$(dirname "$0")/easyeda2kicad_config_kicad.py" || {
    echo "❗ Failed to configure KiCAD paths. Please check your Python environment."
    exit 1
}

echo "✅ KiCAD paths configured!"
