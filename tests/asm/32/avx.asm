[bits 32]
    vaddsd xmm1, xmm2, xmm4
    vaddsd xmm2, xmm3, [eax]
    vaddps ymm1, ymm2, ymm3
    vaddps ymm1, ymm7, [eax]
    vblendpd ymm1, ymm7, ymm4, 0x42 
    vcvtpd2ps xmm1, xmm2 
    vcvtpd2ps xmm1, ymm3
    vcvtpd2ps xmm1, oword [eax]
    vcvtpd2ps xmm1, yword [eax]
    vcvtpd2dq xmm1, xmm2 
    vcvtpd2dq xmm1, ymm3
    vcvtpd2dq xmm1, oword [eax]
    vcvtpd2dq xmm1, yword [eax]
    vcvttpd2dq xmm1, xmm2 
    vcvttpd2dq xmm1, ymm3
    vcvttpd2dq xmm1, oword [eax]
    vcvttpd2dq xmm1, yword [eax]
