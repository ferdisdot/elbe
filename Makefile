all:
	dpkg-buildpackage -uc -us -b
	lintian
