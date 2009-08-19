docdir = ${datadir}/docs/manual
dist_doc_DATA = \
    manual.html \
    manual.xml \
    manual.xsl \
    manual.css

GENERATED = manual.html

all:

manual.html: manual.xml manual.xsl
	xsltproc manual.xsl manual.xml > $@

maintainer-clean-local:
	rm -rf $(GENERATED)
