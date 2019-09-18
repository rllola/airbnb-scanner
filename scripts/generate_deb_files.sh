#!/bin/bash

echo "====== GENERATE CONTROL FILE ======"
cat > $PWD/pkg-debian/DEBIAN/control << EOF
Package: AirbnbScanner
Version: ${TRAVIS_TAG/v}
Architecture: all
Essential: no
Section: utils
Priority: optional
Maintainer: Lola Rigaut-Luczak
Description: Device scanner to get the camera in your Airbnb.
EOF

mkdir -p $PWD/pkg-debian/usr/share/applications/

echo "====== GENERATE .DESKTOP FILE ======"
cat > $PWD/pkg-debian/usr/share/applications/airbnb-scanner.desktop << EOF
[Desktop Entry]
Version=${TRAVIS_TAG/v}
Name=Airbnb Scanner
Comment=Device scanner to get the camera in your Airbnb.
Exec=AirbnbScanner %u
Path=/usr/share/AirbnbScanner/
Icon=airbnbscanner
Terminal=true
Type=Application
Categories=Application;Network;
EOF
