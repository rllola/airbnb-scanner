build:
	python build.py --no-sysroot
	mkdir pkg-debian/usr/share/AirbnbScanner
	cp build-linux-64/AirbnbScanner pkg-debian/usr/share/AirbnbScanner/AirbnbScanner
	dpkg -b pkg-debian AirbnbScanner_test_i386.deb

clean:
	rm -rf build-*/
	rm -rf pkg-debian/usr/share/AirbnbScanner
	rm *.deb

install:
	sudo dpkg -i AirbnbScanner_test_i386.deb

uninstall:
	sudo dpkg -r airbnbscanner

init:
	python build.py

clean-sysroot:
	rm *.tar.gz
	rm *.tar.xz
	rm -rf sysroot-linux-64

download:
	./scripts/download_libraries.sh

.PHONY: build clean install uninstall init clean-sysroot download
