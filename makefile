build:
	pyinstaller airbnb-scanner.spec
	mv dist/AirbnbScanner pkg-debian/usr/share/
	dpkg -b pkg-debian AirbnbScanner_test_i386.deb

clean:
	rm -rf dist/ build/
	rm -rf pkg-debian/usr/share/AirbnbScanner
	rm *.deb

.PHONY: build clean
