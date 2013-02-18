docdir = ${datadir}/docs/udis86/manual

EXTRA_DIST = \
	index.rst \
	getstarted.rst \
	libudis86.rst \
	conf.py

all: build-html-docs

maintainer-clean-local:
	rm -rf $(GENERATED)

.PHONY: build-html-docs

build-html-docs:
	$(SPHINX_BUILD) -c $(srcdir) -b html $(srcdir) $(builddir)/html

clean-local:
	rm -rf $(builddir)/html
