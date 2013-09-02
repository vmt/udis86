#
# Automake definitions for udis86 tests
#
check_PROGRAMS = \
    symresolve \
    bufoverrun \
    libcheck

bufoverrun_SOURCES  = bufoverrun.c
bufoverrun_LDADD    = $(top_builddir)/libudis86/libudis86.la
bufoverrun_CFLAGS   = -I$(top_srcdir)/libudis86 -I$(top_srcdir)

symresolve_SOURCES = symresolve.c
symresolve_LDADD   = $(top_builddir)/libudis86/libudis86.la
symresolve_CFLAGS  = -I$(top_srcdir)/libudis86 -I$(top_srcdir)

libcheck_SOURCES  = libcheck.c
libcheck_LDADD    = $(top_builddir)/libudis86/libudis86.la
libcheck_CFLAGS   = -I$(top_srcdir)/libudis86 -I$(top_srcdir)

MAINTAINERCLEANFILES = Makefile.in

DISTCLEANFILES = difftest.sh

YASM    = @YASM@
PYTHON  = @PYTHON@
TESTDIS = $(top_builddir)/udcli/udcli

EXTRA_DIST = \
 	$(srcdir)/asm \
	$(srcdir)/oprgen.py \
	$(srcdir)/symresolve.ref \
	$(srcdir)/installcheck.c \
	$(srcdir)/libcheck.c

if HAVE_YASM
tests: difftest test-buf-overrun test-sym-resolver test-libcheck
else
tests: warn_no_yasm test-buf-overrun test-sym-resolver test-libcheck
endif

SEED = 1984


.PHONY: test-buf-overrun
test-buf-overrun: bufoverrun
	@./bufoverrun && echo "$@: passed"


.PHONY: test-sym-resolver
test-sym-resolver: symresolve
	@$(top_builddir)/tests/$< > $@.out
	@diff -w $(srcdir)/symresolve.ref $@.out && echo "$@: passed."

.PHONY: test-libcheck
test-libcheck: libcheck
	@./libcheck && echo "$@: passed"

#
# generate operand tests
#
oprtest_generate = \
	outdir=$(builddir)/_results/asm/$(1) && \
	mkdir -p $${outdir} && \
	PYTHONPATH=$(top_srcdir)/scripts $(PYTHON) $(top_srcdir)/tests/oprgen.py \
        $(top_srcdir)/docs/x86/optable.xml $(SEED) $(1) >$${outdir}/oprtest.asm

.PHONY: oprtest
oprtest: oprgen.py
	@echo "Generating operand tests."
	@$(call oprtest_generate,64)
	@$(call oprtest_generate,32)
	@$(call oprtest_generate,16)


.PHONY: difftest
difftest: oprtest $(builddir)/difftest.sh
	@sh $(builddir)/difftest.sh


.PHONY: difftest-refup
difftest-refup: $(builddir)/difftest.sh
	@sh $(builddir)/difftest.sh refup


.PHONY: warn_no_yasm
warn_no_yasm:
	@echo "*** YASM NOT FOUND: Poor Test Coverage ***"

check-local: tests

installcheck-local:
	@$(CC) $(srcdir)/installcheck.c -o installcheck.bin -I$(includedir) -L$(libdir) -ludis86
	@echo "$@: passed"

clean-local:
	rm  -f $(builddir)/*.bin $(builddir)/*.out $(builddir)/*.pyc
	rm -rf $(builddir)/_results
