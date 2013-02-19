[bits 16]
    movzx eax, word [bx]
    iretd
    dpps xmm2, xmm1, 0x10
    blendvpd xmm1, xmm2
