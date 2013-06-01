# udis86 - scripts/ud_opcode.py
# 
# Copyright (c) 2009, 2013 Vivek Thampi
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


class UdInsnDef:
    """An x86 instruction definition
    """
    def __init__(self, id, **insnDef):
        self.id        = id
        self.mnemonic  = insnDef['mnemonic']
        self.prefixes  = insnDef['prefixes']
        self._opcodes  = insnDef['opcodes']
        self.operands  = insnDef['operands']
        self._cpuid    = insnDef['cpuid']
        self._opcexts  = {}

        for opc in self._opcodes:
            if opc.startswith('/'):
                e, v = opc.split('=')
                self._opcexts[e] = v

    @property
    def vendor(self):
        return self._opcexts.get('/vendor', None)

    @property
    def mode(self):
        return self._opcexts.get('/m', None)

    @property
    def osize(self):
        return self._opcexts.get('/o', None)

    def isDef64(self):
        return 'def64' in self.prefixes

    def __str__(self):
        return self.mnemonic + " " + ', '.join(self.operands) + ' '.join(self._opcodes)


class UdOpcodeTable:
    """A single table of instruction definitions, indexed by
       a decode field. 
    """

    class CollisionError(Exception):
        pass

    class IndexError(Exception):
        """Invalid Index Error"""
        pass

    @classmethod
    def vendor2idx(cls, v):
        return (0 if v == 'amd' 
                  else (1 if v == 'intel'
                          else 2))

    @classmethod
    def vex2idx(cls, v):
        vexOpcExtMap = {
            'none'      : 0x0, 
            '0f'        : 0x1, 
            '0f38'      : 0x2, 
            '0f3a'      : 0x3,
            '66'        : 0x4, 
            '66_0f'     : 0x5, 
            '66_0f38'   : 0x6, 
            '66_0f3a'   : 0x7,
            'f3'        : 0x8, 
            'f3_0f'     : 0x9, 
            'f3_0f38'   : 0xa, 
            'f3_0f3a'   : 0xb,
            'f2'        : 0xc, 
            'f2_0f'     : 0xd, 
            'f2_0f38'   : 0xe, 
            'f2_0f3a'   : 0xf,
        }
        return vexOpcExtMap[v]


    # A mapping of opcode extensions to their representational
    # values used in the opcode map.
    OpcExtMap = {
        '/rm'    : lambda v: int(v, 16),
        '/x87'   : lambda v: int(v, 16),
        '/3dnow' : lambda v: int(v, 16),
        '/reg'   : lambda v: int(v, 16),
        # modrm.mod
        # (!11, 11)    => (00b, 01b)
        '/mod'   : lambda v: 0 if v == '!11' else 1,
        # Mode extensions:
        # (16, 32, 64) => (00, 01, 02)
        '/o'     : lambda v: (int(v) / 32),
        '/a'     : lambda v: (int(v) / 32),
        # Disassembly mode 
        # (!64, 64)    => (00b, 01b)
        '/m'     : lambda v: 1 if v == '64' else 0,
        # SSE
        # none => 0
        # f2   => 1
        # f3   => 2
        # 66   => 3
        '/sse'   : lambda v: (0 if v == 'none'
                                else (((int(v, 16) & 0xf) + 1) / 2)),
        # AVX
        '/vex'   : lambda v: UdOpcodeTable.vex2idx(v),
        # Vendor
        '/vendor': lambda v: UdOpcodeTable.vendor2idx(v)
    }


    _TableInfo = {
        'opctbl'    : { 'label' : 'UD_TAB__OPC_TABLE',   'size' : 256 },
        '/sse'      : { 'label' : 'UD_TAB__OPC_SSE',     'size' : 4 },
        '/reg'      : { 'label' : 'UD_TAB__OPC_REG',     'size' : 8 },
        '/rm'       : { 'label' : 'UD_TAB__OPC_RM',      'size' : 8 },
        '/mod'      : { 'label' : 'UD_TAB__OPC_MOD',     'size' : 2 },
        '/m'        : { 'label' : 'UD_TAB__OPC_MODE',    'size' : 2 },
        '/x87'      : { 'label' : 'UD_TAB__OPC_X87',     'size' : 64 },
        '/a'        : { 'label' : 'UD_TAB__OPC_ASIZE',   'size' : 3 },
        '/o'        : { 'label' : 'UD_TAB__OPC_OSIZE',   'size' : 3 },
        '/3dnow'    : { 'label' : 'UD_TAB__OPC_3DNOW',   'size' : 256 },
        '/vendor'   : { 'label' : 'UD_TAB__OPC_VENDOR',  'size' : 3 },
        '/vex'      : { 'label' : 'UD_TAB__OPC_VEX',     'size' : 16 },
    }


    def __init__(self, id, typ):
        assert typ in self._TableInfo
        self.id       = id 
        self._typ     = typ
        self._entries = {}


    def size(self):
        return self._TableInfo[self._typ]['size']

    def entries(self):
        return self._entries.iteritems()

    def numEntries(self):
        return len(self._entries.keys())


    def label(self):
        return self._TableInfo[self._typ]['label']


    def name(self):
        return "ud_itab__%d" % self.id


    def meta(self):
        return self._typ


    def __str__(self):
        return "table-%s" % self._typ


    def add(self, opc, obj):
        typ = UdOpcodeTable.getOpcodeTyp(opc)
        idx = UdOpcodeTable.getOpcodeIdx(opc)
        if self._typ != typ or idx in self._entries:
            raise CollisionError()
        self._entries[idx] = obj


    def lookup(self, opc):
        typ = UdOpcodeTable.getOpcodeTyp(opc)
        idx = UdOpcodeTable.getOpcodeIdx(opc)
        if self._typ != typ:
            raise UdOpcodeTable.CollisionError("%s <-> %s" % (self._typ, typ))
        return self._entries.get(idx, None)

    
    def entryAt(self, index):
        """Returns the entry at a given index of the table,
           None if there is none. Raises an exception if the
           index is out of bounds.
        """
        if index < self.size():
            return self._entries.get(index, None)
        raise self.IndexError("index out of bounds: %s" % index)


    @classmethod
    def getOpcodeTyp(cls, opc):
        if opc.startswith('/'):
            return opc.split('=')[0]
        else:
            return 'opctbl'


    @classmethod
    def getOpcodeIdx(cls, opc):
        if opc.startswith('/'):
            typ, v = opc.split('=')
            return cls.OpcExtMap[typ](v)
        else:
            # plain opctbl opcode
            return int(opc, 16)


    @classmethod
    def getLabels(cls):
        """Returns a list of all labels"""
        return [cls._TableInfo[k]['label'] for k in cls._TableInfo.keys()]


class UdOpcodeTables(object):

    """opcode from the udis86 optable.
    """

    class CollisionError(Exception):
        def __init__(self, obj1, obj2):
            self.obj1, self.obj2 = obj1, obj2

    def __init__(self):
        # Root Table --
        # The root table is always a 256 entry opctbl, indexed
        # by a plain opcode byte
        self._tableID   = 0
        self._insnID    = 0
        self._tables    = []
        self._insns     = []
        self._mnemonics = {}
        self.root       = self.newTable('opctbl')
        self._logFh     = open("opcodeTables.log", "w")

        # add an invalid instruction entry without any mapping
        # in the opcode tables.
        self.invalidInsn = UdInsnDef(self._insnID, mnemonic="invalid",
                                     opcodes=[], cpuid=[],
                                     operands=[], prefixes=[])
        self._insns.append(self.invalidInsn)
        self._insnID += 1

    def log(self, s):
        self._logFh.write(s + "\n")

    def patchAvx2byte(self):
        # create avx tables
        for pp in (None, 'f2', 'f3', '66'):
            for m in (None, '0f', '0f38', '0f3a'):
                if pp is None and m is None:
                    continue
                if pp is None:
                    vex = m
                elif m is None:
                    vex = pp
                else:
                    vex = pp + '_' + m
                table = self.walk(self.root, ('c4', '/vex=' + vex))
                self.map(self.root, ('c5', '/vex=' + vex), table)

    def newTable(self, typ):
        tbl = UdOpcodeTable(self._tableID, typ)
        self._tables.append(tbl)
        self._tableID += 1
        return tbl

    
    def mkTrie(self, opcStr, obj):
        if len(opcStr) == 0:
            return obj
        opc = opcStr[0]
        tbl = self.newTable(UdOpcodeTable.getOpcodeTyp(opc))
        tbl.add(opc, self.mkTrie(opcStr[1:], obj))
        return tbl


    def walk(self, tbl, opcodes):
        opc = opcodes[0]
        e   = tbl.lookup(opc)
        if e is None:
            return None
        elif isinstance(e, UdOpcodeTable) and len(opcodes[1:]):
            return self.walk(e, opcodes[1:])
        return e


    def map(self, tbl, opcStr, obj):
        opc = opcStr[0]
        e   =  tbl.lookup(opc)
        if e is None:
            tbl.add(opc, self.mkTrie(opcStr[1:], obj))
        else:
            if len(opcStr[1:]) == 0:
                raise self.CollisionError(e, obj)
            self.map(e, opcStr[1:], obj)


    def addInsn(self, **insnDef):

        # Canonicalize opcode list
        opcexts = insnDef['opcexts']
        opcodes = list(insnDef['opcodes'])

        # Re-order vex
        if '/vex' in opcexts:
            assert opcodes[0] == 'c4' or opcodes[0] == 'c5'
            opcodes.insert(1, '/vex=' + opcexts['/vex'])

        # Add extensions. The order is important, and determines how
        # well the opcode table is packed. Also note, /sse must be
        # before /o, because /sse may consume operand size prefix
        # affect the outcome of /o.
        for ext in ('/mod', '/x87', '/reg', '/rm', '/sse', '/o', '/a', '/m',
                    '/3dnow', '/vendor'):
            if ext in opcexts:
                opcodes.append(ext + '=' + opcexts[ext])

        insn = UdInsnDef(self._insnID,
                         mnemonic = insnDef['mnemonic'],
                         prefixes = insnDef['prefixes'],
                         operands = insnDef['operands'],
                         opcodes  = opcodes,
                         cpuid    = insnDef['cpuid'])
        self._insns.append(insn)
        self._insnID += 1

        # add to lookup by mnemonic structure
        if insn.mnemonic not in self._mnemonics:
            self._mnemonics[insn.mnemonic] = [ insn ]
        else:
            self._mnemonics[insn.mnemonic].append(insn)

        try:
            self.map(self.root, opcodes, insn)
        except self.CollisionError as e:
            self.pprint()
            print(opcodes, insn, str(e.obj1), str(e.obj2))
            # TODO
            raise
        except Exception as e:
            self.pprint()
            print e, insnDef['mnemonic'], opcodes, opcexts
            raise


    def addInsnDef(self, insnDef):
        opcodes  = []
        opcexts  = {}

        # pack plain opcodes first, and collect opcode
        # extensions
        for opc in insnDef['opcodes']:
            if not opc.startswith('/'):
                opcodes.append(opc)
            else:
                e, v = opc.split('=')
                opcexts[e] = v

        # artificially add a /sse=none for 2 byte opcodes
        if (opcodes[0] == '0f' and opcodes[1] != '0f' and
            '/sse' not in opcexts):
            opcexts['/sse'] = 'none'

        # treat vendor as an opcode extension
        if len(insnDef['vendor']):
            opcexts['/vendor'] = insnDef['vendor']

        if 'avx' in insnDef['cpuid'] and '/sse' in opcexts:
            sseoprs = []
            for opr in insnDef['operands']:
                if opr not in ( 'H', ):
                    sseoprs.append(opr)

            self.addInsn(mnemonic=insnDef['mnemonic'],
                         prefixes=insnDef['prefixes'],
                         opcodes=opcodes,
                         opcexts=opcexts,
                         operands=sseoprs,
                         cpuid=insnDef['cpuid'])

            # This is a legacy sse style instruction definition
            # for an AVX instruction
            vexopcs = ['c4']
            vexopcexts = dict([(e, opcexts[e]) for e in opcexts if e != '/sse'])
            vexopcexts['/vex'] = opcexts['/sse'] + '_' + '0f'
            if opcodes[1] == '38' or opcodes[1] == '3a':
                vexopcexts['/vex'] += opcodes[1]
                vexopcs.extend(opcodes[2:])
            else:
                vexopcs.extend(opcodes[1:])

            self.addInsn(mnemonic='v' + insnDef['mnemonic'],
                         prefixes=insnDef['prefixes'],
                         opcodes=vexopcs,
                         opcexts=vexopcexts,
                         operands=insnDef['operands'],
                         cpuid=insnDef['cpuid'])
        else:
            self.addInsn(mnemonic=insnDef['mnemonic'],
                         prefixes=insnDef['prefixes'],
                         opcodes=opcodes,
                         opcexts=opcexts,
                         operands=insnDef['operands'],
                         cpuid=insnDef['cpuid'])

    def getInsnList(self):
        """Returns an ordered (by id) list of instructions
        """
        return self._insns


    def getTableList(self):
        """Returns an ordered (by id) list of tables
        """
        return self._tables


    def getMnemonicsList(self):
        """Returns a sorted list of mnemonics
        """
        return sorted(self._mnemonics.keys())


    def pprint(self):
        def printWalk(tbl, indent=""):
            entries = tbl.entries()
            for k, e in entries:
                if isinstance(e, UdOpcodeTable):
                    print("%s    |-<%02x> %s" % (indent, k, e))
                    printWalk(e, indent + "    |")
        printWalk(self.root)


    def printStats(self):
        tables = self.getTableList()
        self.log("stats: ")
        self.log("  Num tables    = %d" % len(tables))
        self.log("  Num insnDefs  = %d" % len(self.getInsnList()))

        totalSize = 0
        totalEntries = 0
        for table in tables:
            totalSize += table.size()
            totalEntries += table.numEntries()
        self.log("  Packing Ratio = %d%%" % ((totalEntries * 100) / totalSize))
