ACLOCAL_AMFLAGS = -I build/m4

SUBDIRS = libudis86 . udcli . tests . docs

GENERATED = autom4te.cache \
            aclocal.m4 \
            configure \
            build \
            *.in \
            libudis86/*.in \
            udcli/*.in \
            tests/*.in \
            docs/*.in 

include_ladir = ${includedir}
include_la_HEADERS = udis86.h

.PHONY: libudis86 udcli tests

libudis86:
	$(MAKE) -C $@

udcli: libudis86
	$(MAKE) -C $@

tests: check

maintainer-clean-local:
	rm -rf $(GENERATED)
