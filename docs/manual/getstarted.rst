Getting Started
===============


Building and Installing udis86
------------------------------

udis86 is developed for unix-like environments, and like most software,
the basic steps towards building and installing it are as follows.

.. code::

    $ ./configure
    $ make
    $ make install

Depending on your choice of install location, you may need to have root
privileges to do an install. The install scripts copy the necessary header
and library files to appropriate locations in your system.


Interfacing with libudis86: A Quick Example
-------------------------------------------

The following is an example of a program that interfaces with libudis86
and uses the API to generate assembly language output for 64-bit code,
input from STDIN.

.. code-block:: c

    #include <stdio.h>
    #include <udis86.h>

    int main()
    {
        ud_t ud_obj;

        ud_init(&ud_obj);
        ud_set_input_file(&ud_obj, stdin);
        ud_set_mode(&ud_obj, 64);
        ud_set_syntax(&ud_obj, UD_SYN_INTEL);

        while (ud_disassemble(&ud_obj)) {
            printf("\t%s\n", ud_insn_asm(&ud_obj));
        }

        return 0;
    }

To compile the program (using gcc):

.. code::

    $ gcc -ludis86 example.c -o example

This example should give you an idea of how this library can be used. The
following sections describe, in detail, the complete API of libudis86.
