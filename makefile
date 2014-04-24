help:
	echo 'Run "sudo make install" to install the program'
	echo 'Run "sudo make run" to run the program'
	echo 'Run "sudo make uninstall" to uninstall the program'
install:
	cp resetsettings.py /usr/bin/resetsettings
	chmod +x /usr/bin/resetsettings
run:
	python resetsettings.py
uninstall:
	rm -v /usr/bin/resetsettings
installed-size:
	du -sx --exclude DEBIAN ./debian/
build: 
	sudo make build-deb;
build-deb:
	mkdir -p debian
	mkdir -p debian/DEBIAN
	mkdir -p debian/usr
	mkdir -p debian/usr/bin
	mkdir -p debian/etc
	cp resetsettings.py ./debian/usr/bin/resetsettings
	cp resetsettings.xml ./debian/etc/resetsettings.xml
	chmod +x ./debian/usr/bin/resetsettings
	md5sum ./debian/usr/bin/resetsettings > ./debian/DEBIAN/md5sums
	sed -i.bak 's/\.\/debian\///g' ./debian/DEBIAN/md5sums
	rm -v ./debian/DEBIAN/md5sums.bak
	cp -rv debdata/. debian/DEBIAN/
	chmod -R 0755 debian/
	dpkg-deb --build debian
	cp -v debian.deb resetsettings.deb
	rm -v debian.deb
	rm -rv debian
