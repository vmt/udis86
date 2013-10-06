/* udis86 - tests/libcheck.c
 * 
 * Copyright (c) 2013 Vivek Thampi
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without modification, 
 * are permitted provided that the following conditions are met:
 * 
 *     * Redistributions of source code must retain the above copyright notice, 
 *       this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright notice, 
 *       this list of conditions and the following disclaimer in the documentation 
 *       and/or other materials provided with the distribution.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR 
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
 * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
#include <stdio.h>
#include <udis86.h>
#include <string.h>

unsigned int testcase_check_count;
unsigned int testcase_check_fails; 

#define TEST_DECL(name) \
  const char * __testcase_name = name \

#define TEST_CASE() \
  do { \
    volatile int __c =  ++ testcase_check_count; \
    if (0) __c += 1; \
    do 

#define TEST_CASE_SET_FAIL() \
  do { \
    testcase_check_fails++; \
    printf("Testcase %s: failure at line %d\n", __testcase_name, __LINE__); \
  } while (0)

#define TEST_CASE_REPORT_ACTUAL(v) \
    printf("Testcase %s:    actual   = %d\n", __testcase_name, (v)) 
#define TEST_CASE_REPORT_EXPECTED(v) \
    printf("Testcase %s:    expected = %d\n", __testcase_name, (v)) 

#define TEST_CASE_END() \
    while (0); \
  } while (0)

#define TEST_CHECK(cond)               \
  TEST_CASE() {                        \
    int eval = (cond);                 \
    if (!eval) {                       \
      TEST_CASE_SET_FAIL();            \
    }                                  \
  } TEST_CASE_END()

#define TEST_CHECK_INT(expr, val)      \
  TEST_CASE() {                        \
    int eval = (expr);                 \
    int val2 = (val);                  \
    if (eval != val2) {                \
      TEST_CASE_SET_FAIL();            \
      TEST_CASE_REPORT_EXPECTED(val2); \
      TEST_CASE_REPORT_ACTUAL(eval);   \
    }                                  \
  } TEST_CASE_END()

#define TEST_CHECK_OP_REG(o, n, r) \
  TEST_CHECK(ud_insn_opr(o, n)->type == UD_OP_REG && \
             ud_insn_opr(o, n)->base == (r))


static int
input_callback(ud_t *u)
{
  int *n = (int *) ud_get_user_opaque_data(u);
  if (*n == 0) {
    return UD_EOI;
  }
  --*n;
  return 0x90; 
}

static void
check_input(ud_t *ud_obj)
{
  TEST_DECL("check_input");
  const uint8_t code[]  = { 0x89, 0xc8 }; /* mov eax, ecx */
  int i;

  /* truncate buffer */
  ud_set_mode(ud_obj, 32);
  for (i = 0; i < 5; ++i) {
    ud_set_input_buffer(ud_obj, code, (sizeof code) - 1); 
    TEST_CHECK(ud_disassemble(ud_obj) == 1);
    TEST_CHECK(ud_insn_len(ud_obj) == 1);
    TEST_CHECK(ud_obj->mnemonic == UD_Iinvalid);
  }

  /* input skip on buffer */
  {
    const uint8_t code[] = { 0x89, 0xc8, /* mov eax, ecx*/
                             0x90 };     /* nop */
    ud_set_input_buffer(ud_obj, code, (sizeof code)); 
    ud_input_skip(ud_obj, 2);
    TEST_CHECK_INT(ud_disassemble(ud_obj), 1);
    TEST_CHECK_INT(ud_obj->mnemonic, UD_Inop);

    ud_set_input_buffer(ud_obj, code, (sizeof code)); 
    ud_input_skip(ud_obj, 0);
    TEST_CHECK_INT(ud_disassemble(ud_obj), 2);
    TEST_CHECK_INT(ud_obj->mnemonic, UD_Imov);
    TEST_CHECK(ud_insn_ptr(ud_obj)[0] == 0x89);
    TEST_CHECK(ud_insn_ptr(ud_obj)[1] == 0xc8);

    /* bad skip */
    ud_set_input_buffer(ud_obj, code, (sizeof code)); 
    ud_input_skip(ud_obj, 3);
    TEST_CHECK_INT(ud_disassemble(ud_obj), 0);
    ud_input_skip(ud_obj, 1);
    TEST_CHECK_INT(ud_disassemble(ud_obj), 0);
    ud_set_input_buffer(ud_obj, code, (sizeof code)); 
    ud_input_skip(ud_obj, 0);
    TEST_CHECK_INT(ud_disassemble(ud_obj), 2);
    ud_input_skip(ud_obj, 1000);
    TEST_CHECK_INT(ud_disassemble(ud_obj), 0);
  }

  /* input hook test */
  {
    int n;
    ud_set_user_opaque_data(ud_obj, (void *) &n);
    ud_set_input_hook(ud_obj, &input_callback);

    n = 0;
    TEST_CHECK(ud_disassemble(ud_obj) == 0);

    n = 1;
    ud_set_input_hook(ud_obj, &input_callback);
    TEST_CHECK_INT(ud_disassemble(ud_obj), 1);
    TEST_CHECK(ud_insn_ptr(ud_obj)[0] == 0x90);
    TEST_CHECK_INT(ud_obj->mnemonic, UD_Inop);

    n = 2;
    ud_set_input_hook(ud_obj, &input_callback);
    ud_input_skip(ud_obj, 1);
    TEST_CHECK(ud_disassemble(ud_obj) == 1);
    TEST_CHECK(ud_obj->mnemonic == UD_Inop);
    TEST_CHECK(ud_disassemble(ud_obj) == 0);
    TEST_CHECK(ud_insn_len(ud_obj) == 0);
    TEST_CHECK(ud_obj->mnemonic == UD_Iinvalid);

    n = 1;
    ud_input_skip(ud_obj, 2);
    TEST_CHECK_INT(ud_disassemble(ud_obj), 0);
    TEST_CHECK(ud_input_end(ud_obj));
  }

  /* a known buffer overrun test case (used to be bufoverrun.c) */
  {
    const uint8_t code[] = { 0xf0, 0x66, 0x36, 0x67, 0x65, 0x66,
                             0xf3, 0x67, 0xda };
    ud_set_mode(ud_obj, 16);
    ud_set_input_buffer(ud_obj, code, sizeof code);
    TEST_CHECK(ud_disassemble(ud_obj) > 0);
  }
}
  
static void
check_mode(ud_t *ud_obj)
{
  TEST_DECL("check_mode");
  const uint8_t code[] = { 0x89, 0xc8 }; /* mov eax, ecx */
  ud_set_input_buffer(ud_obj, code, sizeof code); 
  ud_set_mode(ud_obj, 32);
  TEST_CHECK(ud_disassemble(ud_obj) == 2);
  TEST_CHECK_OP_REG(ud_obj, 0, UD_R_EAX);
  TEST_CHECK_OP_REG(ud_obj, 1, UD_R_ECX);
}

static void
check_disasm(ud_t *ud_obj)
{
  TEST_DECL("check_mode");
  const uint8_t code[] = { 0x89, 0xc8,  /* mov eax, ecx */
                           0x90 };      /* nop */
  ud_set_input_buffer(ud_obj, code, sizeof code); 
  ud_set_mode(ud_obj, 32);
  ud_set_pc(ud_obj, 0x100);

  TEST_CHECK(ud_disassemble(ud_obj) == 2);
  TEST_CHECK(ud_insn_off(ud_obj) == 0x100);
  TEST_CHECK(ud_insn_ptr(ud_obj)[0] == 0x89);
  TEST_CHECK(ud_insn_ptr(ud_obj)[1] == 0xc8);
  TEST_CHECK(ud_insn_mnemonic(ud_obj) == UD_Imov);
  TEST_CHECK(strcmp(ud_lookup_mnemonic(UD_Imov), "mov") == 0);

  TEST_CHECK(ud_disassemble(ud_obj) == 1);
  TEST_CHECK(ud_insn_off(ud_obj) == 0x102);
  TEST_CHECK(ud_insn_ptr(ud_obj)[0] == 0x90);
  TEST_CHECK(ud_insn_mnemonic(ud_obj) == UD_Inop);
  TEST_CHECK(strcmp(ud_lookup_mnemonic(UD_Inop), "nop") == 0);
}

int
main(void)
{
  ud_t ud_obj;
  ud_init(&ud_obj);
  ud_set_syntax(&ud_obj, UD_SYN_INTEL);

  check_input(&ud_obj);
  check_mode(&ud_obj);
  check_disasm(&ud_obj);

  if (testcase_check_fails > 0) {
    printf("libcheck result: %d checks, %d failures\n",
           testcase_check_count, testcase_check_fails);
    return 1;
  }
  return 0;
}

/* vim: set ts=2 sw=2 expandtab: */
