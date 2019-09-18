build:
	python build.py --no-sysroot
	mkdir pkg-debian/usr/share/AirbnbScanner
	cp build-linux-64/AirbnbScanner pkg-debian/usr/share/AirbnbScanner/AirbnbScanner
	dpkg -b pkg-debian AirbnbScanner_test_i386.deb

clean:
	rm -rf build-*/
	rm -rf pkg-debian/usr/share/AirbnbScanner
	rm *.deb

.PHONY: build clean
