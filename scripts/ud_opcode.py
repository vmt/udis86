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
        '/sse'      : { 'name' : 'UD_TAB__OPC_SSE',     'size' : 4 },
        '/reg'      : { 'name' : 'UD_TAB__OPC_REG',     'size' : 8 },
        '/rm'       : { 'name' : 'UD_TAB__OPC_RM',      'size' : 8 },
        '/mod'      : { 'name' : 'UD_TAB__OPC_MOD',     'size' : 2 },
        '/m'        : { 'name' : 'UD_TAB__OPC_MODE',    'size' : 2 },
        '/x87'      : { 'name' : 'UD_TAB__OPC_X87',     'size' : 64 },
        '/a'        : { 'name' : 'UD_TAB__OPC_ASIZE',   'size' : 3 },
        '/o'        : { 'name' : 'UD_TAB__OPC_OSIZE',   'size' : 3 },
        '/3dnow'    : { 'name' : 'UD_TAB__OPC_3DNOW',   'size' : 256 },
        'vendor'    : { 'name' : 'UD_TAB__OPC_VENDOR',  'size' : 3 },
        '/vex.p'    : { 'name' : 'UD_TAB__OPC_VEX_P',   'size' : 4 },
        '/vex.m'    : { 'name' : 'UD_TAB__OPC_VEX_M',   'size' : 3 },
    }

    OpcodeTable0 = {
        'type'      : 'opctbl',
        'entries'   : {},
        'meta'      : 'table0'
    }

    OpcExtIndex = {

        # ssef2, ssef3, sse66
        'sse': {
            'none' : '00', 
            'f2'   : '01', 
            'f3'   : '02', 
            '66'   : '03'
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
        },

        'vex.p': {
            'none' : '00', 
            'f2'   : '01', 
            'f3'   : '02', 
            '66'   : '03'
        },

       'vex.m': {
            'none' : '00', 
            '38'   : '01', 
            '3a'   : '02', 
        },


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
            raise NameError( "error: violation in opcode mapping (overwrite) %s with %s." % 
                                ( table[ 'entries' ][ index ], type) )
        return table[ 'entries' ][ index ]

    class Insn:
        """An abstract type representing an instruction in the opcode map.
        """

        # A mapping of opcode extensions to their representational
        # values used in the opcode map.
        OpcExtMap = {
            '/rm'    : lambda v: "%02x" % int(v, 16),
            '/x87'   : lambda v: "%02x" % int(v, 16),
            '/3dnow' : lambda v: "%02x" % int(v, 16),
            '/reg'   : lambda v: "%02x" % int(v, 16),
            # modrm.mod
            # (!11, 11)    => (00, 01)
            '/mod'   : lambda v: '00' if v == '!11' else '01',
            # Mode extensions:
            # (16, 32, 64) => (00, 01, 02)
            '/o'     : lambda v: "%02x" % (int(v) / 32),
            '/a'     : lambda v: "%02x" % (int(v) / 32),
            '/m'     : lambda v: '00' if v == '!64' else '01',
            # SSE
            '/sse'   : lambda v: UdOpcodeTables.OpcExtIndex['sse'][v],
            # AVX
            '/vex.p' : lambda v: UdOpcodeTables.OpcExtIndex['vex.p'][v],
            '/vex.m' : lambda v: UdOpcodeTables.OpcExtIndex['vex.m'][v]
        }

        def __init__(self, prefixes, mnemonic, opcodes, operands, vendor):
            self.opcodes  = []
            self.prefixes = prefixes
            self.mnemonic = mnemonic
            self.operands = operands
            self.vendor   = vendor
            self.opcext   = {}

            # artificially add a /sse=none for 2 byte opcodes
            if opcodes[0] == '0f' and opcodes[1] != '0f':
                opcodes.append('/sse=none')

            # begin the list with all plain opcodes
            for opc in opcodes:
                if not opc.startswith('/'):
                    self.opcodes.append(opc)

            # re-order vex/xop prefixes to follow vex opcode
            if self.opcodes[0] == 'c4' or self.opcodes[0] == 'c5':
                for opc in opcodes:
                    if opc.startswith('/vex'):
                        self.opcodes.insert(1, opc)

            # Add extensions. The order is important, and determines how
            # well the opcode table is packed. Also note, /sse must be
            # before /o, because /sse may consume operand size prefix
            # affect the outcome of /o.
            for ext in ('/mod', '/x87', '/reg', '/rm', '/sse',
                        '/o',   '/a',   '/m', '/3dnow'):
                for opc in opcodes:
                    if opc.startswith(ext):
                        self.opcodes.append(opc)

    def parse(self, table, insn):
        # Walk down the tree, create levels as needed
        assert not insn.opcodes[0].startswith("/")
        index = insn.opcodes[0];
        for opc in insn.opcodes[1:]:
            if opc.startswith('/'):
                ext, v= opc.split('=')
                table = self.updateTable(table, index, ext, ext)
                index = insn.OpcExtMap[ext](v)
                insn.opcext[ext] = index
            else:
                table = self.updateTable(table, index, 'opctbl', index)
                index = opc

        # additional table for disambiguating vendor
        if len(insn.vendor):
            table = self.updateTable(table, index, 'vendor', insn.vendor)
            index = self.OpcExtIndex['vendor'][insn.vendor]

        # make leaf node entries
        leaf = self.updateTable(table, index, 'insn', '')

        leaf['mnemonic'] = insn.mnemonic
        leaf['prefixes'] = insn.prefixes
        leaf['operands'] = insn.operands

        # add instruction to linear table of instruction forms
        self.InsnTable.append({ 'prefixes' : insn.prefixes,  
                                'mnemonic' : insn.mnemonic, 
                                'operands' : insn.operands,
                                'vendor'   : insn.vendor,
                                'opcext'   : insn.opcext,
                                'opcodes'  : insn.opcodes })

        # add mnemonic to mnemonic table
        if not insn.mnemonic in self.MnemonicsTable:
            self.MnemonicsTable.append(insn.mnemonic)


    # Adds an instruction definition to the opcode tables
    def addInsnDef( self, prefixes, mnemonic, opcodes, operands, vendor ):
        insn = self.Insn(prefixes=prefixes,
                    mnemonic=mnemonic,
                    opcodes=opcodes,
                    operands=operands,
                    vendor=vendor)
        try: 
            self.parse(self.OpcodeTable0, insn)
        except:
            self.print_tree()
            raise

    def print_table( self, table, pfxs ):
        print("%s   |" % pfxs)
        keys = table[ 'entries' ].keys()
        if ( len( keys ) ):
            keys.sort()
        for idx in keys:
            e = table[ 'entries' ][ idx ]
            if e[ 'type' ] == 'insn':
                print("%s   |-<%s>" % ( pfxs, idx )),
                print("%s %s" % ( e[ 'mnemonic' ], ' '.join( e[ 'operands'] ) ))
            else:
                print("%s   |-<%s> %s" % ( pfxs, idx, e['type'] ))
                self.print_table( e, pfxs + '   |' )

    def print_tree( self ): 
        self.print_table( self.OpcodeTable0, '' )
