ACLOCAL_AMFLAGS = -I build/m4

SUBDIRS = scripts libudis86 udcli docs tests

MAINTAINERCLEANFILES = \
	Makefile.in \
	configure \
	config.h.in \
	config.h.in~ \
	missing \
	aclocal.m4 \
	build/config.guess \
	build/config.sub \
	build/compile \
	build/config.guess \
	build/config.sub \
	build/depcomp \
	build/install-sh \
	build/ltmain.sh \
	build/missing

include_ladir = ${includedir}
include_la_HEADERS = udis86.h

.PHONY: libudis86 udcli tests docs

libudis86:
	$(MAKE) -C $@

udcli: libudis86
	$(MAKE) -C $@

tests: check

maintainer-clean-local:
	-rm -rf build/m4
	-rm -rf build
	-rm -rf autom4te.cache
