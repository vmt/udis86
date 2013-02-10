;; Test branching instructions
;;
[bits 64]

	jnz near x
	jo near x
	jno word x
	jc near x
	jnc word x
	jae dword x
	jcxz x
	jecxz x
	jrcxz x
	jmp dword near x
	call dword near x
	jmp word x
	jmp dword x
	jmp word [eax]	
x:	jmp qword [rax]
	jmp word x
	jmp dword x
