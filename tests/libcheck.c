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

unsigned int testcase_check_count;
unsigned int testcase_check_fails; 

#define TEST_DECL(name) \
  const char * __testcase_name = name \

#define TEST_CHECK(cond) \
  do { \
    int eval = (cond); \
    testcase_check_count ++; \
    if (!eval) { \
      printf("Testcase %s: failure at line %d\n", __testcase_name, __LINE__); \
      testcase_check_fails++; \
    } \
  } while (0)

#define TEST_CHECK_OP_REG(o, n, r) \
  TEST_CHECK((o)->operand[n].type == UD_OP_REG && \
             (o)->operand[n].base == (r))

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


int
main(void)
{
  ud_t ud_obj;
  ud_init(&ud_obj);
  ud_set_syntax(&ud_obj, UD_SYN_INTEL);

  check_mode(&ud_obj);

  if (testcase_check_fails > 0) {
    printf("libcheck result: %d checks, %d failures\n",
           testcase_check_count, testcase_check_fails);
    return 1;
  }
  return 0;
}

/* vim: set ts=2 sw=2 expandtab: */
