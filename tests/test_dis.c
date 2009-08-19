/* udis86 tests/test_dis.c - front end to udis86 testing.
 * 
 * Copyright (c) 2002-2009 Vivek Thampi
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without modification, 
 * are permitted provided that the following conditions are met:
 * 
 *     * Redistributions of source code must retain the above copyright notice, 
 *       this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright notice, 
 *       this list of conditions and the following disclaimer in the documentation 
 *       and/or other materials provided with the distribution.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR 
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
 * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <udis86.h>

int main( int argc, char **argv )
{
    ud_t ud_obj;
    FILE * input_file = NULL;

    if ( argc != 3 ) {
        fprintf( stderr, "usage: %s -16|32|64 <bin_file>", argv[ 0 ] );
        exit( 1 );
    }

    input_file = fopen( argv[ 2 ], "rb" );
    if ( input_file == NULL ) {
        fprintf( stderr, "error: failed to open file '%s'", argv[ 2 ] );
        exit( 1 );
    } 

    ud_init( &ud_obj );
    ud_set_input_file( &ud_obj, input_file );

    if (strcmp(argv[1],"-16") == 0)
        ud_set_mode( &ud_obj, 16 );
    else if (strcmp(argv[1],"-32") == 0)
        ud_set_mode( &ud_obj, 32 );
    else if (strcmp(argv[1],"-64") == 0)
        ud_set_mode( &ud_obj, 64 );

    ud_set_syntax( &ud_obj, UD_SYN_INTEL );

    while ( ud_disassemble( &ud_obj ) ) {
        printf( "\t%s\n", ud_insn_asm( &ud_obj ) );
    }

    return 0;
}
