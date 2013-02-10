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
    testobscure.asm \
    testobscure.ref \
    testcorner.asm \
    testcorner.ref \
    testgen.py \
    testgen_opr.py

yasm_tests = \
    test16 \
    test32 \
    test64 \
    testobscure \
    testcorner \
    testgen16 \
    testgen32 \
    testgen64

DIFF_TESTS_32 = \
    test_sext_32

DIFF_TESTS_64 = \
    test_sext_64

DIFF_TESTS_AMD_64 =\
	test_amd_64

DIFF_TESTS_INTEL_64 = \
	test_intel_64 \
	test_branch_64

no_yasm_tests = \
    testoverrun

if HAVE_YASM
  ud_TESTS = $(yasm_tests) \
			 $(no_yasm_tests) \
			 $(DIFF_TESTS_32) \
			 $(DIFF_TESTS_64) \
			 $(DIFF_TESTS_AMD_64) \
			 $(DIFF_TESTS_INTEL_64)
else
  ud_TESTS = $(no_yasm_tests) warn_no_yasm
endif

.PHONY: $(yasm_tests) $(no_yasm_tests) warn_no_yasm

check-local: tests

SEED = 19231

tests: $(ud_TESTS)

yasm_asm = $(YASM) -f bin -o $(1).bin $(1).asm

asm_compare = \
    @$(YASM) -f bin -o $(1).bin $(top_srcdir)/tests/$(1).asm \
	&& echo "[bits $(2)]" > $(1).out \
	&& $(top_builddir)/tests/test_dis $(1).bin -$(2) >> $(1).out \
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

testgen_compare = \
	@PYTHONPATH=$(top_srcdir)/scripts $(PYTHON) $(top_srcdir)/tests/testgen.py \
        $(top_srcdir)/docs/x86/optable.xml $(SEED) $(1) > testgen__$(1).asm \
	&& $(YASM) -f bin -o testgen__$(1).bin testgen__$(1).asm \
    && echo "[bits $(1)]" > testgen__$(1).out \
    && $(top_builddir)/tests/test_dis testgen__$(1).bin -$(1) >> testgen__$(1).out \
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

TESTDIS = $(top_builddir)/tests/test_dis

define DIFF_TEST_template
.PHONY: $(1) $(1)-ref

$(1)-ref: $(1).ref

$(1): $(1).out $(1).ref
	@diff -w $(1).ref $(1).out && echo "$(1): passed."

$(1).ref: $(1).bin
	@echo "Generating $$@"
	@$$(TESTDIS) $(1).bin $(2) $$< > $$@

$(1).bin: $(1).asm
	@echo "Generating $$@"
	@$(YASM) -f bin -o $$@ $$<

$(1).out: $$(TESTDIS) $(1).bin
	@echo "Generating $$@"
	@$$(TESTDIS) $(1).bin $(2) > $(1).out
endef

#
# Generate rules for all diff tests
#
$(foreach test,$(DIFF_TESTS_32),$(eval $(call DIFF_TEST_template,$(test),-32)))
$(foreach test,$(DIFF_TESTS_64),$(eval $(call DIFF_TEST_template,$(test),-64)))
$(foreach test,$(DIFF_TESTS_AMD_64),$(eval $(call DIFF_TEST_template,$(test),-64 -vamd)))
$(foreach test,$(DIFF_TESTS_INTEL_64),$(eval $(call DIFF_TEST_template,$(test),-64 -vintel)))

warn_no_yasm:
	@echo "*** YASM NOT FOUND: Poor Test Coverage ***"

installcheck-local:
	@$(CC) $(srcdir)/test_dis.c -o test_installcheck.bin -I$(includedir) -L$(libdir) -ludis86
	@echo "$@: passed"

clean-local:
	rm -f *.bin *.out testgen__*.asm *.pyc
