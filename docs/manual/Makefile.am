docdir = ${datadir}/docs/udis86/manual

EXTRA_DIST = \
	index.rst \
	getstarted.rst \
	libudis86.rst \
	conf.py

all: html-doc

maintainer-clean-local:
	rm -rf $(GENERATED)

outdir = $(builddir)/outdir

.PHONY: build-html-doc

singlehtml-doc:
	$(SPHINX_BUILD) -c $(srcdir) -b singlehtml $(srcdir) $(outdir)/singlehtml

latex-doc:
	$(SPHINX_BUILD) -c $(srcdir) -b latex $(srcdir) $(outdir)/latex

html-doc:
	$(SPHINX_BUILD) -c $(srcdir) -b html $(srcdir) $(outdir)/html

text-doc:
	$(SPHINX_BUILD) -c $(srcdir) -b text $(srcdir) $(outdir)/text

man-doc:
	$(SPHINX_BUILD) -c $(srcdir) -b man $(srcdir) $(outdir)/man

texinfo-doc:
	$(SPHINX_BUILD) -c $(srcdir) -b texinfo $(srcdir) $(outdir)/texinfo

clean-local:
	rm -rf $(outdir)
