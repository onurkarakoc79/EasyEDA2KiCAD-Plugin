#!/bin/sh
set -e  # Stop on error

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "❗ Python is not installed. Please install Python 3.8 or newer."
    exit 1
fi

# Check if pipx is available
if ! command -v pipx &>/dev/null; then
    echo "🔄 Installing pipx..."
    python3 -m pip install pipx
    python3 -m pipx ensurepath
    echo "❗ Please close and reopen this terminal for pipx to be recognized."
    exit 1
fi

# Install easyeda2kicad via pipx
pipx install easyeda2kicad || {
    echo "❗ Failed to install easyeda2kicad. Please check your Python environment."
    exit 1
}

# Clean previous build if exists
rm -rf build
mkdir -p build/resources build/plugins

# Copy essential files
cp metadata.json build
cp *.py icon.png build/plugins
cp -r icon-64x64.png build/resources/icon.png

# Build the package
cd build && zip -r ../easyeda2kicad-plugin.zip *

echo "✅ Build complete! Package created: easyeda2kicad-plugin.zip"
