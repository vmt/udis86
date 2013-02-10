;; Test intel specific instructions in 64bit mode

[bits 64]

    ;; yasm doesn't seem to support a mode for intel
    ;; specific instructions
    db 0x0f, 0x34    ; sysenter
    db 0x0f, 0x35    ; sysexit
