[bits 32]
[org 0x80000000]

l1:
    nop
    nop
    nop
    nop
    nop

    jmp l1
    nop
    jmp word l2

    nop
    nop
    jmp dword l2
    nop
    nop
    nop
l2:
    nop
    nop
    jmp l1
