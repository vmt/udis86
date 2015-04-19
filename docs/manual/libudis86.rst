libudis86
=========

libudis86 is a disassembler library for the x86 architecture, including support
for the newer 64bit variants (IA32e, amd64, etc.) It provides you the ability
to decode a stream of bytes as x86 instructions, inspect various bits
of information about those instructions and even translate to human readable
assembly language format.

.. default-domain:: c

.. contents::
 

ud_t: udis86 object
-------------------

libudis86 is reentrant, and to maintain that property it does not use static
data. All data related to the disassembly are stored in a single object, called
the udis86 object :type:`ud_t`. 

.. c:type:: ud_t

    A structure encapsulating udis86 disassembler state.

To use libudis86 you must create an instance of this object,

.. code-block:: c

    ud_t ud_obj;

and initialize it,

.. code-block:: c

    ud_init(&ud_obj);

You can create multiple such objects and use with the library, each one
an independent disassembler.


Setup Machine State
-------------------

The decode semantics of a sequence of bytes depends on the target machine state
for which they are being disassembled. In x86, this means the current effective
processor mode (16, 32 or 64bits), the current program counter (ip/eip/rip), and
sometimes, the processor vendor. By default, libudis86 is initialized to be in
32 bit disassembly mode, program counter at 0, and vendor being :code:`UD_VENDOR_ANY`.
The following functions allow you to override these default to suit your needs.

.. c:function:: void ud_set_mode(ud_t*, uint8_t mode_bits)

    Sets the mode of disassembly. Possible values are 16, 32, and 64. By
    default, the library works in 32bit mode.

.. c:function:: void ud_set_pc(ud_t*, uint64_t pc)

    Sets the program counter (IP/EIP/RIP). This changes the offset of the
    assembly output generated, with direct effect on branch instructions.

.. c:function:: void ud_set_vendor(ud_t*, unsigned vendor)

    Sets the vendor of whose instruction to choose from. This is only useful
    for selecting the VMX or SVM instruction sets at which point INTEL and AMD
    have diverged significantly. At a later stage, support for a more granular
    selection of instruction sets maybe added.

    * :code:`UD_VENDOR_INTEL` - for INTEL instruction set.
    * :code:`UD_VENDOR_ATT` - for AMD instruction set.
    * :code:`UD_VENDOR_ANY` - for any valid instruction in either INTEL or AMD.


Setup Input
-----------

libudis86 provides three ways in which you can input binary data: as a fixed
sized memory buffer, a standard library FILE object, or as a callback function.
By default, a :type:`ud_t` object is initialized to read input from :code:`STDIN`.

.. c:function:: void ud_set_input_buffer(ud_t*, unsigned char* buffer, size_t size)

    Sets the input source for the library to a `buffer` of `size` bytes.

.. c:function:: void ud_set_input_file(ud_t*, FILE* filep)

    Sets the input source to a file pointed to by a given standard library
    :code:`FILE` pointer. Note that libudis86 does not perform any checks,
    and assumes that the file pointer is properly initialized and open for
    reading.

.. c:function:: void ud_set_input_hook(ud_t* ud_obj, int (*hook)(ud_t *ud_obj))

    Sets a pointer to a function, to callback for input. The callback is invoked
    each time libudis86 needs the next byte in the input stream. To single
    end-of-input, this callback must return the constant :code:`UD_EOI`.

    .. seealso:: :func:`ud_set_user_opaque_data`, :func:`ud_set_user_opaque_data`

.. c:function:: void ud_input_skip(ud_t*, size_t n);

    Skips ahead `n` number of bytes in the input stream.


.. c:function:: int ud_input_end(const ud_t*);

    Test for end of input. You can use this function to test if udis86
    has exhausted the input.

At the end of input, udis86 stops disassembly. If you want to restart or
reset the source of input, you must again invoke one of the above functions.

Sometimes you may want to associate custom data with a udis86 object, that you
can use with the input callback function, or even in different parts of your
own project as you pass the object around. You can use the following two
functions to achieve this.

.. c:function:: void ud_set_user_opaque_data(ud_t* ud_obj, void* opaque)

    Associates a pointer with the udis86 object to be retrieved and used in
    client functions, such as the input hook callback function.

.. c:function:: void* ud_get_user_opaque_data(const ud_t* ud_obj)

    Returns any pointer associated with the udis86 object, using the
    :func:`ud_set_user_opaque_data` function.


Setup Translation
-----------------

libudis86 can translate the decoded instruction into one of two assembly
language dialects: the INTEL syntax (such as those found in NASM and YASM) and
the other which resembles GNU Assembler (AT&T style) syntax. By default, this
is set to INTEL like syntax. You can override the default or specify your own
translator using the following function.

.. c:function:: void ud_set_syntax(ud_t*, void (*translator)(ud_t*))

    Sets the function that translates the intermediate decode information to
    a human readable form. There are two inbuilt translators,

    - :code:`UD_SYN_INTEL` for INTEL (NASM-like) syntax. (default)
    - :code:`UD_SYN_ATT` for AT&T (GAS-like) syntax.

    If you do not want libudis86 to translate, you can pass :code:`NULL` to the
    function, with no more translations thereafter. This is useful when you
    only want to identify chunks of code and then create the assembly output if
    needed, or when you are only interested in examining the instructions and
    do not want to waste cycles generating the assembly language output.

    If you want to create your own translator, you can specify a pointer to your
    own function. This function must accept a single parameter, the udis86 object
    :type:`ud_t`, and it will be invoked everytime an instruction is decoded.


Disassemble
-----------

With target state and input source set up, you can now disassemble. At the core
of libudis86 api is the function :c:func:`ud_disassemble` which does this.
libudis86 exposes decoded instructions in an intermediate form meant to be
useful for programs that want to examine them. This intermediate form is
available using functions and fields of :type:`ud_t` as described below.


.. c:function:: unsigned int ud_disassemble(ud_t*)

    Disassembles the next instruction in the input stream.
    
    :returns: the number of bytes disassembled. A 0 indicates end of input.
    
    Note, to restart disassembly after the end of input, you must call one of
    the input setting functions with a new source of input.

    A common use-case pattern for this function is in a loop::

        while (ud_disassemble(&ud_obj)) {
            /* 
             * use or print decode info.
             */
        }

For each successful invocation of :c:func:`ud_disassemble`, you can use the
following functions to get information about the disassembled instruction.


.. c:function:: unsigned int ud_insn_len(const ud_t* u)

    Returns the number of bytes disassembled.

.. c:function:: uint64_t ud_insn_off(const ud_t*)

    Returns the offset of the disassembled instruction in terms of the
    program counter value specified initially.

    .. seealso:: :func:`ud_set_pc`

.. c:function:: const char* ud_insn_hex(ud_t*)

    Returns pointer to a character string holding the hexadecimal
    representation of the disassembled bytes.

.. c:function:: const uint8_t* ud_insn_ptr(const ud_t* u)

    Returns pointer to the buffer holding the instruction bytes. Use
    :func:`ud_insn_len` to determine the size of this buffer.

.. c:function:: const char* ud_insn_asm(const ud_t* u)

    If the syntax is specified, returns pointer to the character string holding
    assembly language representation of the disassembled instruction.

.. c:function:: const ud_operand_t* ud_insn_opr(const ud_t* u, unsigned int n)

    Returns a reference (:type:`ud_operand_t`) to the nth (starting with 0)
    operand of the instruction. If the instruction does not have such an
    operand, the function returns :code:`NULL`.

.. c:function:: enum ud_mnemonic_code ud_insn_mnemonic(const ud_t *u)

    .. versionadded:: 1.7.2

    Returns the instruction mnemonic in the form of an enumerated constant
    (:code:`enum ud_mnemonic_code`). As a convention all mnemonic constants
    are composed by prefixing standard instruction mnemonics with :code:`UD_I`. 
    For example, the enumerations for :code:`mov`, :code:`xor` and :code:`jmp`
    are :code:`UD_Imov`, :code:`UD_Ixor`, and :code:`UD_Ijmp`, respectively.::

      ud_disassemble(&ud_obj);

      switch (ud_insn_mnemonic(ud_obj)) {
        case UD_Imov:  printf("mov!"); break;
        case UD_Ixor:  printf("xor!"); break;
        case UD_Ijmp:  printf("jmp!"); break;
        /*...*/
      }

    Prior to version 1.7.2, the way to access the mnemonic was by a field of
    :code:`ud_t`, :c:member:`ud_t.mnemonc`. This field is now deprecated and
    may not be supported in the future.

    .. seealso:: :func:`ud_lookup_mnemonic`

.. c:function:: const char* ud_const lookup_mnemonic(enum ud_mnemonic_code)

    Returns a pointer to a character string corresponding to the given
    mnemonic code. Returns a :code:`NULL` if the code is invalid.

Inspect Operands
----------------

An intermediate representation of instruction operands is available in the
form of :type:`ud_operand_t`. You can retrieve the nth operand of a
disassembled instruction using the function :func:`ud_insn_opr`.

.. c:type:: ud_operand_t

    The operand type, represents a single operand of an instruction. It
    contains the following fields.
    
    - :c:member:`size <ud_operand_t.size>`
    - :c:member:`type <ud_operand_t.type>`
    - :c:member:`base <ud_operand_t.base>`
    - :c:member:`index <ud_operand_t.index>`
    - :c:member:`scale <ud_operand_t.scale>`
    - :c:member:`offset <ud_operand_t.offset>`
    - :c:member:`lval <ud_operand_t.lval>`

.. c:member:: unsigned ud_operand_t.size

    Size of the operand in number of bits.

.. c:member:: enum ud_operand_type ud_operand_t.type

    Type of the operand. Possible values are,

    .. c:var:: UD_OP_MEM

        A memory operand. The intermediate form normalizes all memory address
        equations to the scale-index-base form. The address equation is
        available in,
        
        - :member:`base <ud_operand_t.base>` - base register as an enumerated
          constant of type :type:`enum ud_type`. Maybe :code:`UD_NONE`, in which
          case the memory addressing form does not include a base register.
        - :member:`index <ud_operand_t.index>` - index register as an enumerated
          constant of type :type:`enum ud_type`. Maybe :code:`UD_NONE`, in which
          case the memory addressing form does not include an index register.
        - :member:`scale <ud_operand_t.index>` - an integer value by which
          the index register must be scaled. Maybe 0, denoting the absence of
          a scale component in the address.
        - :member:`offset <ud_operand_t.offset>` - An integer value, which if
          non-zero represents the size of the displacement offset, and is one
          of 8, 16, 32, and 64. The value is available in
          :member:`lval <ud_operand_t.lval>`.

    .. c:var:: UD_OP_PTR

        A segment:offset pointer operand. The :member:`size <ud_operand_t.size>`
        field can have two values, 32 (for 16:16 seg:off) and 48 (for 16:32 seg:off).
        The pointer value is available in :member:`lval <ud_operand_t.lval>`
        (as :member:`lval.ptr.seg` and :member:`lval.ptr.off`)

    .. c:var:: UD_OP_IMM

        An Immediate operand. Value available in :member:`lval <ud_operand_t.lval>`.

    .. c:var:: UD_OP_JIMM

        An Immediate operand to a branch instruction (relative offsets). Value
        available in :member:`lval <ud_operand_t.lval>`.

    .. c:var:: UD_OP_CONST

        Implicit constant operand. Value available in :member:`lval <ud_operand_t.lval>`.

    .. c:var:: UD_OP_REG

        A register operand. The specific register is available in the
        :member:`base <ud_operand_t.base>` field as an enumerated constant of type
        :type:`enum ud_type`.


.. c:member:: enum ud_register ud_operand_t.base

    Contains an enumerated constant of type :type:`enum ud_type` representing
    a :data:`register <UD_OP_REG>` operand or the base of a :data:`memory <UD_OP_MEM>`
    operand.

.. c:member:: enum ud_register ud_operand_t.index

    Contains an enumerated constant of type :type:`enum ud_type` representing
    the index register of a :data:`memory <UD_OP_MEM>` operand.

.. c:member:: unsigned ud_operand_t.scale

    Contains the scale component of a :data:`memory <UD_OP_MEM>` address operand.

.. c:member:: unsigned ud_operand_t.offset

    Contains the size of the displacement component of a :data:`memory
    <UD_OP_MEM>` address operand. The displacement itself is given by
    :member:`lval <ud_operand_t.lval>`.

.. c:member:: ud_lval_t ud_operand_t.lval

    A union data structure that aggregates integer fields of different sizes,
    storing values depending on the :member:`type <ud_operand_t.type>` and 
    :member:`size <ud_operand_t.size>` of the operand.

    .. c:member:: lval.sbyte

        Signed Byte

    .. c:member:: lval.ubyte

        Unsigned Byte

    .. c:member:: lval.sword

        Signed Word

    .. c:member:: lval.uword

        Unsigned Word

    .. c:member:: lval.sdword

        Signed Double Word

    .. c:member:: lval.udword

        Unsigned Double Word

    .. c:member:: lval.sqword

        Signed Quad Word

    .. c:member:: lval.uqword

        Unsigned Quad Word

    .. c:member:: lval.ptr.seg

        Pointer Segment in Segment:Offset

    .. c:member:: lval.ptr.off

        Pointer Offset in Segment:Offset

.. c:type:: enum ud_type

    Instruction Pointer

    .. code-block:: c

        UD_R_RIP 

    8-Bit Registers

    .. code-block:: c

        UD_NONE,

        UD_R_AL,    UD_R_CL,    UD_R_DL,    UD_R_BL,
        UD_R_AH,    UD_R_CH,    UD_R_DH,    UD_R_BH,
        UD_R_SPL,   UD_R_BPL,   UD_R_SIL,   UD_R_DIL,
        UD_R_R8B,   UD_R_R9B,   UD_R_R10B,  UD_R_R11B,
        UD_R_R12B,  UD_R_R13B,  UD_R_R14B,  UD_R_R15B,

    16-Bit General Purporse Registers

    .. code-block:: c

        UD_R_AX,    UD_R_CX,    UD_R_DX,    UD_R_BX,
        UD_R_SP,    UD_R_BP,    UD_R_SI,    UD_R_DI,
        UD_R_R8W,   UD_R_R9W,   UD_R_R10W,  UD_R_R11W,
        UD_R_R12W,  UD_R_R13W,  UD_R_R14W,  UD_R_R15W,
                
    32-Bit General Purporse Registers:

    .. code-block:: c

        UD_R_EAX,   UD_R_ECX,   UD_R_EDX,   UD_R_EBX,
        UD_R_ESP,   UD_R_EBP,   UD_R_ESI,   UD_R_EDI,
        UD_R_R8D,   UD_R_R9D,   UD_R_R10D,  UD_R_R11D,
        UD_R_R12D,  UD_R_R13D,  UD_R_R14D,  UD_R_R15D,
                
    64-Bit General Purporse Registers:

    .. code-block:: c

        UD_R_RAX,   UD_R_RCX,   UD_R_RDX,   UD_R_RBX,
        UD_R_RSP,   UD_R_RBP,   UD_R_RSI,   UD_R_RDI,
        UD_R_R8,    UD_R_R9,    UD_R_R10,   UD_R_R11,
        UD_R_R12,   UD_R_R13,   UD_R_R14,   UD_R_R15,

    Segment Registers:

    .. code-block:: c

        UD_R_ES,    UD_R_CS,    UD_R_SS,    UD_R_DS,
        UD_R_FS,    UD_R_GS,    

    Control Registers:

    .. code-block:: c

        UD_R_CR0,   UD_R_CR1,   UD_R_CR2,   UD_R_CR3,
        UD_R_CR4,   UD_R_CR5,   UD_R_CR6,   UD_R_CR7,
        UD_R_CR8,   UD_R_CR9,   UD_R_CR10,  UD_R_CR11,
        UD_R_CR12,  UD_R_CR13,  UD_R_CR14,  UD_R_CR15,
                
    Debug Registers:

    .. code-block:: c

        UD_R_DR0,   UD_R_DR1,   UD_R_DR2,   UD_R_DR3,
        UD_R_DR4,   UD_R_DR5,   UD_R_DR6,   UD_R_DR7,
        UD_R_DR8,   UD_R_DR9,   UD_R_DR10,  UD_R_DR11,
        UD_R_DR12,  UD_R_DR13,  UD_R_DR14,  UD_R_DR15,

    MMX Registers:

    .. code-block:: c

        UD_R_MM0,   UD_R_MM1,   UD_R_MM2,   UD_R_MM3,
        UD_R_MM4,   UD_R_MM5,   UD_R_MM6,   UD_R_MM7,

    FPU Registers:

    .. code-block:: c

        UD_R_ST0,   UD_R_ST1,   UD_R_ST2,   UD_R_ST3,
        UD_R_ST4,   UD_R_ST5,   UD_R_ST6,   UD_R_ST7, 

    SSE Registers:

    .. code-block:: c

        UD_R_XMM0,  UD_R_XMM1,  UD_R_XMM2,  UD_R_XMM3,
        UD_R_XMM4,  UD_R_XMM5,  UD_R_XMM6,  UD_R_XMM7,
        UD_R_XMM8,  UD_R_XMM9,  UD_R_XMM10, UD_R_XMM11,
        UD_R_XMM12, UD_R_XMM13, UD_R_XMM14, UD_R_XMM15,


Inspect Prefixes
----------------

Prefix bytes that affect the disassembly of the instruction are availabe in the
following fields, each of which corressponds to a particular type or class of
prefixes.

.. c:member:: uint8_t ud_t.pfx_rex

    64-bit mode REX prefix

.. c:member:: uint8_t ud_t.pfx_seg

    Segment register prefix

.. c:member:: uint8_t ud_t.pfx_opr

    Operand-size prefix (66h)

.. c:member:: uint8_t ud_t.pfx_adr

    Address-size prefix (67h)

.. c:member:: uint8_t ud_t.pfx_lock

    Lock prefix

.. c:member:: uint8_t ud_t.pfx_str

    String prefix

.. c:member:: uint8_t ud_t.pfx_rep

    Rep prefix

.. c:member:: uint8_t ud_t.pfx_repe

    Repe prefix

.. c:member:: uint8_t ud_t.pfx_repne

    Repne prefix

These fields default to :code:`UD_NONE` if the respective prefixes were not found.
