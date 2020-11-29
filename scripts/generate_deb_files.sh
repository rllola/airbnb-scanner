#!/bin/bash

TAG=$1

echo "====== GENERATE CONTROL FILE ======"
cat > $PWD/pkg-debian/DEBIAN/control << EOF
Package: AirbnbScanner
Version: ${TAG}
Architecture: all
Essential: no
Section: utils
Priority: optional
Maintainer: Lola Rigaut-Luczak <me@lola.ninja>
Description: Device scanner to get the camera in your Airbnb.
EOF

mkdir -p $PWD/pkg-debian/usr/share/applications/

echo "====== GENERATE .DESKTOP FILE ======"
cat > $PWD/pkg-debian/usr/share/applications/airbnb-scanner.desktop << EOF
[Desktop Entry]
Version=${TAG}
Name=Airbnb Scanner
Comment=Device scanner to get the camera in your Airbnb.
Exec=AirbnbScanner %u
Path=/usr/share/AirbnbScanner/
Icon=airbnbscanner
Terminal=talse
Type=Application
Categories=Application;Network;
EOF
