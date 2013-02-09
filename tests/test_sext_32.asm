[bits 32]

    ;; test sign extension

    adc  ax, -100
    and edx, -3
    or   dx, -1000
    or   dx, -1
    add edx, -1000
    imul dx, bx, -100
    imul edx, ebx, -1
    imul edx, ebx, -128
    imul edx, ebx, -129
    imul ax, bx, -129
    sub dword [eax], -1
    sub word [eax], -2000
    test eax, 1
    test eax, -1
    push byte -1
    push word -1
    push dword -1000
    push word -1000

