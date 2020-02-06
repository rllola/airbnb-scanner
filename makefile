build:
	python build.py --no-sysroot
	mkdir -p pkg-debian/usr/share/AirbnbScanner
	cp build-linux-64/AirbnbScanner pkg-debian/usr/share/AirbnbScanner/AirbnbScanner
	dpkg -b pkg-debian AirbnbScanner_test_i386.deb

release:
	python build.py --no-sysroot
	./scripts/generate_deb_files.sh $(TAG)
	mkdir -p pkg-debian/usr/share/AirbnbScanner
	cp build-linux-64/AirbnbScanner pkg-debian/usr/share/AirbnbScanner/AirbnbScanner
	dpkg -b pkg-debian AirbnbScanner_$(TAG)_i386.deb

clean:
	rm -rf build-*/
	rm -rf pkg-debian/usr/share/AirbnbScanner
	rm *.deb

install:
	sudo dpkg -i AirbnbScanner_$(TAG)_i386.deb

uninstall:
	sudo dpkg -r airbnbscanner

init:
	pyqtdeploy-sysroot --target linux-64 --sysroot sysroot-linux-64 --verbose sysroot.json

clean-sysroot:
	rm *.tar.gz
	rm *.tar.xz
	rm -rf sysroot-linux-64

download:
	./scripts/download_libraries.sh

.PHONY: build clean install uninstall init clean-sysroot download
