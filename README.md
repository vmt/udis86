Udis86
======================

Udis86 is a disassembler for the x86 and x86-64 class of instruction set
architectures. It consists of a C library called libudis86 which
provides a clean and simple interface to decode a stream of raw binary
data, and to inspect the disassembled instructions in a structured
manner.


####LICENSE

Udis86 is distributed under the terms of the 2-clause "Simplified BSD
License".  A copy of the license is included with the source in LICENSE.


####libudis86

* Supports all x86 and x86-64 (AMD64) General purpose and System instructions.
* Supported ISA extensions:
    - MMX, FPU (x87), AMD 3DNow
    - SSE, SSE2, SSE3, SSSE3, SSE4.1, SSE4.2, AES,
    - AMD-V, INTEL-VMX, SMX
* Instructions are defined in an XML document, with opcode tables generated for performance.
* Supports output in both INTEL (NASM) as well as AT&T (GNU as) style assembly language syntax.
* Supports a variety of input methods: Files, Memory Buffers, and
* Function Callback hooks.
* Re-entrant, no dynamic memory allocation.
* Fully documented API


##### EXAMPLE
    
    ud_t u;
    
    ud_init(&u);
    ud_set_input_file(&u, stdin);
    ud_set_mode(&u, 64);
    ud_set_syntax(&u, UD_SYN_INTEL);
    
    while (ud_disassemble(&u)) {
      printf("\t%s\n", ud_insn_asm(&ud_obj));
    }

-----
    

####udcli

udcli is a small command-line tool for your quick disassembly needs.

##### EXAMPLE

    $ echo "65 67 89 87 76 65 54 56 78 89 09 00 90" | udcli -32 -x 
    0000000080000800 656789877665     mov [gs:bx+0x6576], eax
    0000000080000806 54               push esp
    0000000080000807 56               push esi
    0000000080000808 7889             js 0x80000793
    000000008000080a 0900             or [eax], eax
    000000008000080c 90               nop

-------


####Documentation

The libudis86 api is fully documented. The package distribution contains
a Texinfo file which can be installed by invoking "make install-info".
You can also find an online html version of the documentation available
at http://udis86.sourceforge.net/.


####Autotools Build

You need autotools if building from sources cloned form version control
system, or if you need to regenerate the build system. The wrapper
script 'autogen.sh' is provided that'll generate the build system.


####AUTHOR

Udis86 is written and maintained by Vivek Thampi (vivek.mt@gmail.com).
