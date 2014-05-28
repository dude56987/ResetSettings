help:
	echo 'Run "sudo make install" to install the program'
	echo 'Run "sudo make run" to run the program'
	echo 'Run "sudo make uninstall" to uninstall the program'
install: build
	sudo gdebi --non-interactive resetsettings_UNSTABLE.deb
run:
	python resetsettings.py
uninstall:
	sudo apt-get purge resetsettings
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
	# create the md5sums file
	find ./debian/ -type f -print0 | xargs -0 md5sum > ./debian/DEBIAN/md5sums
	# cut filenames of extra junk
	sed -i.bak 's/\.\/debian\///g' ./debian/DEBIAN/md5sums
	sed -i.bak 's/\\n*DEBIAN*\\n//g' ./debian/DEBIAN/md5sums
	sed -i.bak 's/\\n*DEBIAN*//g' ./debian/DEBIAN/md5sums
	rm -v ./debian/DEBIAN/md5sums.bak
	# figure out the package size
	du -sx --exclude DEBIAN ./debian/ > Installed-Size.txt
	# copy over package data
	cp -rv debdata/. debian/DEBIAN/
	# fix permissions in package
	chmod -Rv 775 debian/DEBIAN/
	chmod -Rv ugo+r debian/
	chmod -Rv go-w debian/
	chmod -Rv u+w debian/
	# build the package
	dpkg-deb --build debian
	cp -v debian.deb resetsettings_UNSTABLE.deb
	rm -v debian.deb
	rm -rv debian
