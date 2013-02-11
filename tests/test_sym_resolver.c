#include <stdio.h>
#include <udis86.h>

#if defined(__amd64__) || defined(__x86_64__)
#  define FMT "l"
#else
#  define FMT "ll"
#endif

uint8_t bin[] = {
  0x01, 0xc0, 0xeb, 0x11, 0x01, 0xc0, 0xe8, 0x14, 
  0x00, 0x00, 0x00, 0x01, 0xc0, 0x01, 0xc0, 0x74,
  0x02, 0x01, 0xc0, 0x90, 0x90, 0xeb, 0xfe, 0x90,
  0x90, 0xeb, 0xf8, 0x90, 0x90, 0x74, 0xf6, 0x90,
  0x90, 0xe8, 0xf4, 0xff, 0xff, 0xff
};

static const char* 
resolve(struct ud *u, uint64_t addr, int64_t *offset)
{
  *offset = addr - 0x15;
  return "target";
}

static void
dis_loop(struct ud *ud_obj)
{
  while (ud_disassemble(ud_obj) != 0) {
    printf("%016llx %-16s %s\n", ud_insn_off(ud_obj),
                                 ud_insn_hex(ud_obj),
                                 ud_insn_asm(ud_obj));
  }
}

int
main() {
  ud_t ud_obj;
  ud_init(&ud_obj);
  ud_set_mode(&ud_obj, 32);
  ud_set_input_buffer(&ud_obj, bin, sizeof(bin));
  ud_set_syntax(&ud_obj, UD_SYN_INTEL);

  printf("==> Without Symbol Resolution\n");
  dis_loop(&ud_obj);

  printf("==> With Symbol Resolution\n");
  ud_set_pc(&ud_obj, 0);
  ud_set_input_buffer(&ud_obj, bin, sizeof(bin));
  ud_set_sym_resolver(&ud_obj, &resolve);
  dis_loop(&ud_obj);

  return 0;
}
