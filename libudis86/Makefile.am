#
# -- udis86/libudis86
#

PYTHON  = @PYTHON@
OPTABLE = @top_srcdir@/docs/x86/optable.xml

lib_LTLIBRARIES	= libudis86.la

libudis86_la_SOURCES =	\
    itab.c \
    input.c \
    decode.c \
    syn.c \
    syn-intel.c \
    syn-att.c \
    udis86.c \
    input.h \
    syn.h \
    decode.h

include_ladir = ${includedir}/libudis86
include_la_HEADERS = \
    types.h \
    extern.h \
    itab.h

EXTRA_DIST = itab.py

BUILT_SOURCES = \
    itab.c \
    itab.h

#
# DLLs may not contain undefined symbol references.  
# We have the linker check this explicitly.
#
if TARGET_WINDOWS
libudis86_la_LDFLAGS = -no-undefined -version-info 0:0:0
endif

itab.c itab.h: $(top_srcdir)/libudis86/itab.py $(OPTABLE) \
               $(top_srcdir)/scripts/ud_opcode.py \
               $(top_srcdir)/scripts/ud_optable.py
	PYTHONPATH=$(top_srcdir)/scripts $(PYTHON) $(top_srcdir)/libudis86/itab.py $(OPTABLE)


clean-local:
	rm -rf $(BUILT_SOURCES)

maintainer-clean-local:
