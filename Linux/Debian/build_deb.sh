#!/bin/bash
set -e
cd "$(dirname "$0")"
chmod 755 package/DEBIAN/control package/usr/bin/*
dpkg-deb --build package ai-rat-detection-dashboard.deb
echo 'Debian package created: ai-rat-detection-dashboard.deb'
