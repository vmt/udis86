#include <stdio.h>
#include <udis86.h>

int main(void)
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
