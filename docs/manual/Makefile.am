docdir = ${datadir}/docs/udis86/manual

rst_sources = \
	index.rst \
	getstarted.rst \
	libudis86.rst

#
# The official distribution only contains the rst files. So users
# may generate documentation using Sphinx if they wish to.
#
EXTRA_DIST = \
	$(rst_sources) \
	udis86.info \
	conf.py \
	static

MAINTAINERCLEANFILES = \
    Makefile.in \
    udis86.info

if HAVE_SPHINX_DOC

html-local:
	$(SPHINX_BUILD) -c $(srcdir) -b html $(srcdir) $(builddir)/html

udis86.info: $(rst_sources)
	$(SPHINX_BUILD) -E -c $(srcdir) -b texinfo $(srcdir) $(builddir)/texinfo
	$(MAKEINFO) --no-split $(builddir)/texinfo/udis86.texi

check-local: html-local

else

udis86.info: $(rst_sources)
html-local udis86.info:
	@echo ""
	@echo "------------------------------------------------------------------"
	@echo ""
	@echo " Please make sure you have Sphinx (sphinx-doc.org) version 1.1.3"
	@echo " or above, to be able to build documentation."
	@echo ""
	@echo " You can also find documentation at http://udis86.sourceforge.net/"
	@echo ""
	@echo "------------------------------------------------------------------"
	@echo ""
	@exit 1

endif

install-info-local: udis86.info
	install-info --info-dir=$(infodir) $<

clean-local:
	-rm -rf $(builddir)/html
	-rm -rf $(builddir)/texinfo $(builddir)/udis86.info
