VERSION = $$(head -n 1 src/info.py | grep -o '"[^"]\+"' | sed 's/"//g')

build:
	python build.py --no-sysroot
	./scripts/generate_deb_files.sh $(VERSION)
	mkdir -p pkg-debian/usr/share/AirbnbScanner
	cp build-linux-64/AirbnbScanner pkg-debian/usr/share/AirbnbScanner/AirbnbScanner
	dpkg -b pkg-debian AirbnbScanner_v$(VERSION)_i386.deb

clean:
	rm -rf build-*/
	rm -rf pkg-debian/usr/share/AirbnbScanner
	rm *.deb

install:
	sudo dpkg -i AirbnbScanner_v$(VERSION)_i386.deb

uninstall:
	sudo dpkg -r airbnbscanner

init:
	pyqtdeploy-sysroot --target linux-64 --sysroot sysroot-linux-64 --verbose sysroot.json

clean-sysroot:
	rm -rf sysroot-linux-64

clean-download:
	rm *.tar.gz
	rm *.tar.xz

download:
	./scripts/download_libraries.sh

patches:
	patch venv/lib/python3.7/site-packages/pyqtdeploy/sysroot/plugins/qt5.py < patches/qt5.patch
	patch venv/lib/python3.7/site-packages/pyqtdeploy/metadata/python_metadata.py < patches/python_metadata.patch

deps:
	sudo apt install -y cmake xorg-dev libxcb-xinerama0-dev libffi-dev libgl1-mesa-glx libnss3 libxcomposite-dev libxcursor-dev libxi6 libxtst6 libasound2 libegl1-mesa libxkbcommon-x11-0 libfontconfig1-dev libfreetype6-dev libx11-dev libxext-dev libxfixes-dev libxi-dev libxrender-dev libxcb1-dev libx11-xcb-dev libxcb-glx0-dev libxkbcommon-x11-dev
	pip install -r requirements.txt
	pip install pyqtdeploy

.PHONY: build clean install uninstall init clean-sysroot clean-download download deps patches
