#!/bin/bash

# Define variables for easy customization
PYTHON_SCRIPT_PATH="app.py"
APP_NAME="My Flet App"
ICON_PATH="assets/image/icon.png"
PRODUCT_NAME="My Flet App"
PRODUCT_VERSION="23.1.1"
COPYRIGHT="Yudame Inc."
BUNDLE_ID="me.yuda.myfletapp"

# Install PyInstaller if not already installed
pip install pyinstaller
# Pillow will convert provided PNG to a platform specific format
pip install pillow

# Package the app
flet pack "$PYTHON_SCRIPT_PATH" --name "$APP_NAME" --icon "$ICON_PATH"

# Optional: Add assets
flet pack "$PYTHON_SCRIPT_PATH" --add-data "assets:assets"

# Optional: Customize macOS bundle details
# add macOS-specific bundle details
flet pack "$PYTHON_SCRIPT_PATH" --product-name "$PRODUCT_NAME" --product-version "$PRODUCT_VERSION" --copyright "$COPYRIGHT" --bundle-id "$BUNDLE_ID"
