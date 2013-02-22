#
# Automake definitions for udis86 tests
#
check_PROGRAMS = \
    symresolve \
    bufoverrun

bufoverrun_SOURCES  = bufoverrun.c
bufoverrun_LDADD    = $(top_builddir)/libudis86/libudis86.la
bufoverrun_CFLAGS   = -I$(top_srcdir)/libudis86 -I$(top_srcdir)

symresolve_SOURCES = symresolve.c
symresolve_LDADD   = $(top_builddir)/libudis86/libudis86.la
symresolve_CFLAGS  = -I$(top_srcdir)/libudis86 -I$(top_srcdir)

YASM    = @YASM@
PYTHON  = @PYTHON@
TESTDIS = $(top_builddir)/udcli/udcli

EXTRA_DIST = \
 	$(srcdir)/asm \
	$(srcdir)/oprgen.py \
	$(srcdir)/symresolve.ref \
	$(srcdir)/installcheck.c

if HAVE_YASM
tests: diff-test test-buf-overrun test-sym-resolver 
else
tests: warn_no_yasm test-buf-overrun test-sym-resolver 
endif

SEED = 1984


.PHONY: test-buf-overrun
test-buf-overrun: bufoverrun
	@./bufoverrun && echo "$@: passed"


.PHONY: test-sym-resolver
test-sym-resolver: symresolve
	@$(top_builddir)/tests/$< > $@.out
	@diff -w $(srcdir)/symresolve.ref $@.out && echo "$@: passed."


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


diff_test_asm = \
  for mode in 16 32 64; do \
    for vendor in amd intel any; do \
      if [ "$${vendor}" == "any" ]; then \
	    vendor_opt=""; \
        asmdir=$(srcdir)/asm/$${mode}; \
	    outdir=$(abs_builddir)/_results/asm/$${mode}; \
      else \
	    vendor_opt="-v $${vendor}"; \
        asmdir=$(srcdir)/asm/$${mode}/$${vendor}; \
	    outdir=$(builddir)/_results/asm/$${mode}/$${vendor}; \
      fi; \
      if [ ! -d "$${asmdir}" ]; then \
        continue; \
      fi; \
	  mkdir -p $${outdir} && \
      for a in `find $${asmdir} -maxdepth 1 -name "*.asm"` \
	  		   `find $${outdir} -maxdepth 1 -name "*.asm"`; do \
	    srcasm=$$a && outasm=$${outdir}/$$(basename $$a) && \
        $(YASM) -f bin $${srcasm} -o $${outasm}.bin && \
        if [ "x$(1)" == "xrefup" ]; then \
          if [ -f "$${srcasm}.ref" ]; then \
            echo "REFUP  $${outasm}.out -> $${srcasm}.ref" && \
            $(TESTDIS) $${vendor_opt} -$${mode} $${outasm}.bin > $${outasm}.out && \
            cp $${outasm}.out $${srcasm}.ref; \
          fi; \
          if [ -f "$${srcasm}.Sref" ]; then \
            echo "REFUP  $${outasm}.out -> $${srcasm}.Sref" && \
            $(TESTDIS) $${vendor_opt} -att -$${mode} $${outasm}.bin > $${outasm}.out && \
            cp $${outasm}.out $${srcasm}.Sref; \
          fi; \
        else \
          if [ ! -f "$${srcasm}.ref" ]; then \
		    echo "[bits $${mode}]" > $${outasm}.out && \
            $(TESTDIS) $${vendor_opt} -$${mode} -noff -nohex $${outasm}.bin >> $${outasm}.out && \
            diff -w $${srcasm} $${outasm}.out 2>&1 > $${outasm}.diff.log; \
		  else \
            $(TESTDIS) $${vendor_opt} -$${mode} $${outasm}.bin > $${outasm}.out && \
            diff -w $${srcasm}.ref $${outasm}.out 2>&1 > $${outasm}.diff.log; \
		  fi && \
          if [ -f "$${srcasm}.Sref" ]; then \
            $(TESTDIS) $${vendor_opt} -att -$${mode} $${outasm}.bin > $${outasm}.out && \
            diff -w $${srcasm}.Sref $${outasm}.out 2>&1 > $${outasm}.diff.log; \
		  fi && \
          echo "DIFFTEST $${srcasm}: PASS" || \
		  echo "DIFFTEST $${srcasm}: ***FAIL*** ($${outasm}.diff.log)";  \
        fi; \
      done \
    done \
  done


.PHONY: diff-test
diff-test: oprtest
	@$(call diff_test_asm,"diff")


.PHONY: diff-test-refup
diff-test-refup:
	@$(call diff_test_asm,"refup")


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
