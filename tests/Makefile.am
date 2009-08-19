#
# Automake definitions for ud/tests
#
check_PROGRAMS = \
    test_dis \
    ovrrun

test_dis_SOURCES    = test_dis.c
test_dis_LDADD      = $(top_builddir)/libudis86/libudis86.la
test_dis_CFLAGS     = -I$(top_srcdir)/libudis86 -I$(top_srcdir)

ovrrun_SOURCES      = bufovrrun.c
ovrrun_LDADD        = $(top_builddir)/libudis86/libudis86.la
ovrrun_CFLAGS       = -I$(top_srcdir)/libudis86 -I$(top_srcdir)

YASM   = @YASM@
PYTHON = @PYTHON@

export UD_SCRIPT_DIR

dist_check_DATA = \
    test16.asm \
    test32.asm \
    test64.asm \
    testjmp.asm \
    testjmp.ref \
    testobscure.asm \
    testobscure.ref \
    testcorner.asm \
    testcorner.ref \
    testgen.py \
    testgen_opr.py

ud_TESTS = \
    test16 \
    test32 \
    test64 \
    testjmp \
    testoverrun \
    testobscure \
    testcorner \
    testgen16 \
    testgen32 \
    testgen64

.PHONY: $(ud_TESTS)

check-local: tests

SEED = 1

tests: $(ud_TESTS)

yasm_asm = $(YASM) -f bin -o $(1).bin $(1).asm

asm_compare = \
    @$(YASM) -f bin -o $(1).bin $(top_srcdir)/tests/$(1).asm \
	&& echo "[bits $(2)]" > $(1).out \
	&& $(top_builddir)/tests/test_dis -$(2) $(1).bin >> $(1).out \
	&& diff -w $(top_srcdir)/tests/$(1).$(3) $(1).out \
    && echo "$@: passed."

test16: test_dis
	$(call asm_compare,test16,16,asm)

test32: test_dis
	$(call asm_compare,test32,32,asm)

test64: test_dis
	$(call asm_compare,test64,64,asm)

testobscure: test_dis
	$(call asm_compare,testobscure,32,ref)

testcorner: test_dis
	$(call asm_compare,testcorner,32,ref)

testjmp: $(top_builddir)/udcli/udcli
	@$(YASM) -f bin -o testjmp.bin $(top_srcdir)/tests/testjmp.asm
	@$(top_builddir)/udcli/udcli -64 testjmp.bin > testjmp.out
	@diff -w $(top_srcdir)/tests/testjmp.ref testjmp.out && echo "$@: passed."

testgen_compare = \
	@PYTHONPATH=$(top_srcdir)/scripts $(PYTHON) $(top_srcdir)/tests/testgen.py \
        $(top_srcdir)/docs/x86/optable.xml $(SEED) $(1) > testgen__$(1).asm \
	&& $(YASM) -f bin -o testgen__$(1).bin testgen__$(1).asm \
    && echo "[bits $(1)]" > testgen__$(1).out \
    && $(top_builddir)/tests/test_dis -$(1) testgen__$(1).bin >> testgen__$(1).out \
    && diff -w testgen__$(1).asm testgen__$(1).out \
    && echo "$@: passed."

testgen64: testgen.py testgen_opr.py
	$(call testgen_compare,64)

testgen32: testgen.py testgen_opr.py
	$(call testgen_compare,32)

testgen16: testgen.py testgen_opr.py
	$(call testgen_compare,16)

testgen: testgen16 testgen32 testgen64

testovrrun: ovrrun
	@./ovrrun && echo "$@: passed"

installcheck-local:
	@$(CC) $(srcdir)/test_dis.c -o test_installcheck.bin -I$(includedir) -L$(libdir) -ludis86
	@echo "$@: passed"

clean-local:
	rm -f *.bin *.out testgen__*.asm *.pyc
