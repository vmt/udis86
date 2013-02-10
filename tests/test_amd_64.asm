;; Test amd specific 64bit instructions

[bits 64]

    ;; Invalid instructions in amd 64bit mode
    db 0x0f, 0x34    ; sysenter (invalid)
    db 0x0f, 0x35    ; sysexit  (invalid)
