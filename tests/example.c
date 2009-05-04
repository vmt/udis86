/*! \file tests/example.c
 *
 * \page Example Quick usage example
 *
 * The following code is an example of a program that interfaces 
 * with libudis86 and uses the API to generate assembly language 
 * output for 64-bit code, input from STDIN.
 *
 * \include tests/example.c
 *
 * To compile the program (using gcc):
 * 
 * \code $ gcc -ludis86 example.c -o example \endcode
 */
#include <stdio.h>
#include <udis86.h>

int main()
{
    ud_t ud_obj;

    ud_init(&ud_obj);
    ud_set_input_file(&ud_obj, stdin);
    ud_set_mode(&ud_obj, 64);
    ud_set_syntax(&ud_obj, UD_SYN_INTEL);

    while (ud_disassemble(&ud_obj)) {
        printf("\t%s\n", ud_insn_asm(&ud_obj));
    }

    return 0;
}
