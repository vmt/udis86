# udis86 - scripts/ud_opcode.py
# 
# Copyright (c) 2009 Vivek Thampi
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, 
# are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright notice, 
#       this list of conditions and the following disclaimer in the documentation 
#       and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR 
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

class UdOpcodeTables:

    TableInfo = {
        'opctbl'    : { 'name' : 'UD_TAB__OPC_TABLE',   'size' : 256 },
        '3byte'     : { 'name' : 'UD_TAB__OPC_3BYTE',   'size' : 256 },
        '2byte'     : { 'name' : 'UD_TAB__OPC_2BYTE',   'size' : 4 },
        '/reg'      : { 'name' : 'UD_TAB__OPC_REG',     'size' : 8 },
        '/rm'       : { 'name' : 'UD_TAB__OPC_RM',      'size' : 8 },
        '/mod'      : { 'name' : 'UD_TAB__OPC_MOD',     'size' : 2 },
        '/m'        : { 'name' : 'UD_TAB__OPC_MODE',    'size' : 3 },
        '/x87'      : { 'name' : 'UD_TAB__OPC_X87',     'size' : 64 },
        '/a'        : { 'name' : 'UD_TAB__OPC_ASIZE',   'size' : 3 },
        '/o'        : { 'name' : 'UD_TAB__OPC_OSIZE',   'size' : 3 },
        '/3dnow'    : { 'name' : 'UD_TAB__OPC_3DNOW',   'size' : 256 },
        'vendor'    : { 'name' : 'UD_TAB__OPC_VENDOR',  'size' : 3 },
    }

    OpcodeTable0 = {
        'type'      : 'opctbl',
        'entries'   : {},
        'meta'      : 'table0'
    }

    OpcExtIndex = {

        # ssef2, ssef3, sse66
        'sse': {
            'none'  : '00', 
            'ssef2' : '01', 
            'ssef3' : '02', 
            'sse66' : '03'
        },

        # /mod=
        'mod': {
            '!11'   : '00', 
            '11'    : '01'
        },

        # /m=, /o=, /a=
        'mode': { 
            '16'    : '00', 
            '32'    : '01', 
            '64'    : '02'
        },

        'vendor' : {
            'amd'   : '00',
            'intel' : '01',
            'any'   : '02'
        }
    }

    InsnTable = []
    MnemonicsTable = []

    def sizeOfTable( self, t ): 
        return self.TableInfo[ t ][ 'size' ]

    def nameOfTable( self, t ): 
        return self.TableInfo[ t ][ 'name' ]

    #
    # Updates a table entry: If the entry doesn't exist
    # it will create the entry, otherwise, it will walk
    # while validating the path.
    #
    def updateTable( self, table, index, type, meta ):
        if not index in table[ 'entries' ]:
            table[ 'entries' ][ index ] = { 'type' : type, 'entries' : {}, 'meta' : meta } 
        if table[ 'entries' ][ index ][ 'type' ] != type:
            raise NameError( "error: violation in opcode mapping (overwrite) %s %s." % 
                                ( table[ 'entries' ][ index ][ 'type' ], type) )
        return table[ 'entries' ][ index ]


    def parse( self, table, opc ):
        if opc[ 0 ] in ( 'ssef2', 'ssef3', 'sse66' ):
            return self.parseMandatoryPfx( table, opc )
        elif opc[ 0 ] == '0f':
            return self.parse2Byte( table, opc, 'none' )
        else:
            return self.parseOpc( table, opc )

    def parseMandatoryPfx( self, table, opc ):
        if not opc[ 0 ] in ( 'ssef2', 'ssef3', 'sse66' ):
            raise NameError( 'parse Error: Expected mandatory prefix <ssef2, ssef3, sse66>' )
        return self.parse2Byte( table, opc[ 1: ], opc[ 0 ] )

    def parse2Byte( self, table, opc, pfx ):
        if opc[ 0 ] != '0f':
            raise NameError( 'parse Error: Expected 2byte escape code <0f>' )
        table = self.updateTable( table, '0f', '2byte', '0f' )
        table = self.updateTable( table, self.OpcExtIndex[ 'sse' ][ pfx ], 'opctbl', pfx )
        if opc[ 1 ] in ( '38', '3a' ):
            return self.parse3Byte( table, opc[ 1: ] )
        else:
            return self.parseOpc( table, opc[ 1: ] )

    def parse3Byte( self, table, opc ):
        if not opc[ 0 ] in ( '38', '3a' ):
            raise NameError( 'parse Error: Expected 3byte escape code <38,3a>' )
        table = self.updateTable( table, opc[ 0 ], '3byte', opc[ 0 ] )
        return self.parseOpc( table, opc[ 1: ] )

    def parseOpc( self, table, opc ):
        return self.parseOpcExt( table, opc[ 1: ], opc[ 0 ] )

    def parseOpcExt( self, table, opc, index ):
        if len( opc ) == 0:
            # recursion terminator
            return ( table, index )

        ( arg, val ) = opc[ 0 ].split( '=' )

        if arg in ( '/rm', '/x87', '/3dnow', '/reg' ):
            next_index = "%02x" % int( val, 16 )
        elif arg in ( '/o' , '/a', '/m' ):
            next_index = self.OpcExtIndex[ 'mode' ][ val ] 
        elif arg == '/mod':
            next_index = self.OpcExtIndex[ 'mod' ][ val ]

        table = self.updateTable( table, index, arg, arg )

        return self.parseOpcExt( table, opc[ 1: ], next_index )

    # Adds an instruction definition to the opcode tables
    def addInsnDef( self, prefixes, mnemonic, opcodes, operands, vendor ):
        # generate opcode tables
        ( table, index ) = self.parse( self.OpcodeTable0, opcodes )

        if len( vendor ):
            # vendor disambiguation required
            table = self.updateTable( table, index, 'vendor', vendor )
            index = self.OpcExtIndex[ 'vendor' ][ vendor ];

        # make leaf node entries
        leaf = self.updateTable( table, index, 'insn', '' )
        leaf[ 'mnemonic' ] = mnemonic
        leaf[ 'prefixes' ] = prefixes
        leaf[ 'operands' ] = operands

        # add instruction to linear table of instruction forms
        self.InsnTable.append({ 'prefixes' : prefixes,  
                                'mnemonic' : mnemonic, 
                                'operands' : operands })

        # add mnemonic to mnemonic table
        if not mnemonic in self.MnemonicsTable:
            self.MnemonicsTable.append( mnemonic )

    def print_table( self, table, pfxs ):
        print "%s   |" % pfxs
        keys = table[ 'entries' ].keys()
        if ( len( keys ) ):
            keys.sort()
        for idx in keys:
            e = table[ 'entries' ][ idx ]
            if e[ 'type' ] == 'insn':
                print "%s   |-<%s>" % ( pfxs, idx ),
                print  "%s %s" % ( e[ 'mnemonic' ], ' '.join( e[ 'operands'] ) )
            else:
                print "%s   |-<%s> %s" % ( pfxs, idx, e['type'] )
                self.print_table( e, pfxs + '   |' )

    def print_tree( self ): 
        self.print_table( self.OpcodeTable0, '' )
