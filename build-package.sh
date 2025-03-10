#!/bin/sh

# Exit immediately if any command fails
set -e

# Remove old build directory if exists
rm -rf build 

# Create necessary directories
mkdir -p build/resources build/plugins

# Copy essential files
cp metadata.json build
cp *.py icon.png build/plugins
cp -r icon-64x64.png build/resources/icon.png

# Navigate to build directory and create the zip package
cd build && zip -r ../easyeda2kicad-plugin.zip *

echo "✅ Build complete! Package created: easyeda2kicad-plugin.zip"
