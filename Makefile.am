ACLOCAL_AMFLAGS = -I m4

SUBDIRS = scripts . libudis86 . udcli . docs . tests

GENERATED = autom4te.cache \
            aclocal.m4 \
            configure \
            build \
            *.in \
            libudis86/*.in \
            udcli/*.in \
            tests/*.in \
            docs/manual/*.in \
            docs/x86/*.in \
            docs/*.in \
            scripts/*.in

include_ladir = ${includedir}
include_la_HEADERS = udis86.h

.PHONY: libudis86 udcli tests docs

libudis86:
	$(MAKE) -C $@

udcli: libudis86
	$(MAKE) -C $@

tests: check

maintainer-clean-local:
	rm -rf $(GENERATED)
