#!/bin/bash

echo "====== GENERATE INFO.PLIST FILE ======"
cat > $PWD/pkg-macos/AirbnbScanner.app/Contents/Info.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleDisplayName</key>
	<string>AirbnbScanner</string>
	<key>CFBundleExecutable</key>
	<string>MacOS/AirbnbScanner</string>
	<key>CFBundleIconFile</key>
	<string>spy.icns</string>
	<key>CFBundleIdentifier</key>
	<string>AirbnbScanner</string>
	<key>CFBundleInfoDictionaryVersion</key>
	<string>6.0</string>
	<key>CFBundleName</key>
	<string>AirbnbScanner</string>
	<key>CFBundlePackageType</key>
	<string>APPL</string>
	<key>CFBundleShortVersionString</key>
	<string>${TRAVIS_TAG/v}</string>
	<key>LSBackgroundOnly</key>
	<true/>
</dict>
</plist>
EOF
