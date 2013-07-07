[bits 64]
    vaddsd xmm12, xmm4, xmm1
    vminsd xmm13, xmm15, qword [rbx+r8-0x10]
    vaddps ymm8, ymm3, ymm14
    vaddps ymm8, ymm3, [rax]
