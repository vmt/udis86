[bits 32]
    vaddsd xmm1, xmm2, xmm4
    vaddsd xmm2, xmm3, [eax]
    vaddps ymm1, ymm2, ymm3
    vaddps ymm1, ymm7, [eax]
