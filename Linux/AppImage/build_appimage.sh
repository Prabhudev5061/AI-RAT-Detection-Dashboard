#!/bin/bash
# Script to build standalone AppImage using appimagetool on Linux
set -e
cd "$(dirname "$0")"
chmod +x AppDir/AppRun AppDir/usr/bin/*
if ! command -v appimagetool &>/dev/null; then
    echo 'Downloading appimagetool...'
    wget -q https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage -O /tmp/appimagetool
    chmod +x /tmp/appimagetool
    /tmp/appimagetool AppDir AI-RAT-Detection-Dashboard.AppImage
else
    appimagetool AppDir AI-RAT-Detection-Dashboard.AppImage
fi
echo 'AppImage packaging complete: AI-RAT-Detection-Dashboard.AppImage'
