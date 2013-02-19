[bits 64]

    ;; test sign extension

    adc   al, -100
    adc   ax, -100
    adc  eax, -100
    adc  rax, -100
    imul dx, bx, -100
    imul edx, ebx, -100
    imul rdx, r11, -100
    push byte -1
    push word -1
    push dword -1000
    push word -1000
    push -1
    push byte -1
    push dword -1
    push word -1
