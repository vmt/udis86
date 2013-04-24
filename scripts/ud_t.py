# udis86 - scripts/ud_t.py
# 
# Copyright (c) 2013 Vivek Thampi
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


class UdOpcode:
    """opcode from the udis86 optable.
    """

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
            'f2'        : 0x4, 
            'f2_0f'     : 0x5, 
            'f2_0f38'   : 0x6, 
            'f2_0f3a'   : 0x7,
            'f3'        : 0x8, 
            'f3_0f'     : 0x9, 
            'f3_0f38'   : 0xa, 
            'f3_0f3a'   : 0xb,
            '66'        : 0xc, 
            '66_0f'     : 0xd, 
            '66_0f38'   : 0xe, 
            '66_0f3a'   : 0xf
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
        '/m'     : lambda v: 0 if v == '!64' else 1,
        # SSE
        # none => 0
        # f2   => 1
        # f3   => 2
        # 66   => 3
        '/sse'   : lambda v: (0 if v == 'none'
                                else (((int(v, 16) & 0xf) + 1) / 2)),
        # AVX
        '/vex'   : lambda v: UdOpcode.vex2idx(v),
        # Vendor
        '/vendor': lambda v: UdOpcode.vendor2idx(v)
    }

    def __init__(self, opc):
        if opc.startswith("/"):
            typ, val = opc.split("=")
            self._typ = typ
            self._index = self.OpcExtMap[typ](v)
            self._val = val
        else:
            self._typ = 'opctbl'
            self._index = int(opc, 16)
            self._val = opc

    def typ(self):
        return self._typ

    def index(self):
        return self._index


class UdInsn:
    """An x86 instruction definition
    """

    # a global unique id for instruction
    _InsnID = 0

    def __init__(self, **insnDef):
        self._id = self.__class__._InsnID
        self.__class_._InsnID += 1
        self._mnemonic = insnDef['mnemonic']
        self._prefixes = insnDef['prefixes']
        self._opcodes  = insnDef['opcodes']
        self._operands = insnDef['operands']
        self._vendor   = insnDef['vendor']
        self._cpuid    = insnDef['cpuid']


class UdOpcodeTable:
    """A single table of instruction definitions, indexed by
       some decode field. 
    """

    class CollisionError(Exception):
        pass

    # a global unique id for tables
    _TableID = 0

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

    def __init__(self, typ):
        assert typ in self._TableInfo
        self._id = self.__class__._TableID
        self.__class__._TableID += 1
        self._typ  = typ
        self._entries = {}

    def size(self):
        return self._TableInfo[self._typ]['size']

    def label(self):
        return self._TableInfo[self._typ]['label']

    def name(self):
        return "ud_itab__" + self._id


class UdOpcodeTrie:
    """An prefix-tree mapping opcode strings to instruction definitions
    """

    def __init__(self):
        self.root = UdOpcodeTable('opctbl')


    def newTable(self, typ):
        tbl = UdOpcodeTable(typ)
        self._tables.append(tbl)

    
    def mkTrie(self, opcStr, obj):
        if len(opcStr) == 0:
            return obj
        opc = opcStr[0]
        tbl = self.newTable(opc.typ())
        tbl.add(opc, self.mkTrie(opcStr[1:], obj))
        return tbl


    def walk(self, tbl, opcodes):
        opc = opcStr[0]
        e   = tbl.lookup(opc)
        if e is None:
            return None
        elif isinstance(e, UdOpcodeTable) and len(opcStr[1:]):
            return self.walk(e, opcStr[1:])
        return e


    def map(self, tbl, opcStr, obj):
        opc = opcStr[0]
        e   =  tbl.lookup(opc)
        if e is None:
            tbl.add(opc, self.mkTrie(opcStr[1:], obj))
        else:
            self.map(e, opcStr[1:], obj)


class UdXMLOptable:
    """The udis86 xml x86 optable definition loader.
       source: $(src)/docs/x86/optable.xml
    """

    class ParseError(Exception):
        pass

    def __init__(self, xmlFile):
        self._xmlFile = xmlFile
        self._xmlDoc = minidom.parse(xmlFile)


    def add(self, **insnDef):
        self._insnDefs[insnDef['mnemonic']] = insnDef


    def canonicalize(self, **insnDef):
        opcodes  = []
        opcexts  = {}

        # pack plain opcodes first, and collect opcode extensions
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

        return { 'mnemonic' : insnDef['mnemonic'],
                 'prefixes' : insnDef['prefixes'],
                 'opcodes'  : opcodes,
                 'opcexts'  : opcexts,
                 'operands' : insnDef['operands'],
                 'cpuid'    : insnDef['cpuid'] }


    def addLegacyAVX(self, **insnDef):
        sseoprs = []
        for opr in insnDef['operands']:
            if opr not in ( 'H', ):
                sseoprs.append(opr)

        self.add(mnemonic=insnDef['mnemonic'],
                 prefixes=insnDef['prefixes'],
                 opcodes=insnDef['opcodes'],
                 opcexts=insnDef['opcexts'],
                 operands=sseoprs,
                 cpuid=insnDef['cpuid'])

        # This is a legacy sse style instruction definition
        # for an AVX instruction
        opcodes = insnDef['opcocdes']
        opcexts = insnDef['opcexts']
        vexopcs = ['c4']
        vexopcexts = dict([(e, opcexts[e]) for e in opcexts if e != '/sse'])
        vexopcexts['/vex'] = opcexts['/sse'] + '_' + '0f'
        if opcodes[1] == '38' or opcodes[1] == '3a':
            vexopcexts['/vex'] += opcodes[1]
            vexopcs.extend(opcodes[2:])
        else:
            vexopcs.extend(opcodes[1:])

        self.add(mnemonic='v' + insnDef['mnemonic'],
                 prefixes=insnDef['prefixes'],
                 opcodes=vexopcs,
                 opcexts=vexopcexts,
                 operands=insnDef['operands'],
                 cpuid=insnDef['cpuid'])


    def addInsnDef(self, **insnDef):
        cDef = self.caconicalize(**insnDef)
        if 'avx' in cDef['cpuid'] and '/sse' in cDef['opcexts']:
            self.addLegacyAVX(**cDef)
        else:
            self.add(mnemonic = cDef['mnemonic'],
                     prefixes = cDef['prefixes'],
                     opcodes  = cDef['opcodes'],
                     opcexts  = cDef['opcexts'],
                     operands = cDef['operands'],
                     cpuid    = cDef['cpuid'])

    def load(self):
        """Load the instruction definition from the file
           into a canonical form
        """
        self.TlNode = xmlDoc.firstChild
        while self.TlNode and self.TlNode.localName != "x86optable": 
            self.TlNode = self.TlNode.nextSibling

        for insnNode in self.TlNode.childNodes:
            if not insnNode.localName:
                continue
            if insnNode.localName != "instruction":
                raise self.ParseError("warning: invalid insn node - %s" % insnNode.localName)

            mnemonic = insnNode.getElementsByTagName('mnemonic')[0].firstChild.data
            vendor   = ''

            for node in insnNode.childNodes:
                if node.localName == 'vendor':
                    vendor = node.firstChild.data
                elif node.localName == 'def':
                    prefixes, opcodes, operands, lvendor, cpuid = self.parseDef(node)
                    # allow definitions to specialize vendor
                    if len(lvendor):
                        vendor = lvendor
                    self.addInsDef(mnemonic = mnemonic,
                                   prefixes = prefixes,
                                   opcodes  = opcodes,
                                   operands = operands,
                                   vendor   = vendor,
                                   cpuid    = cpuid)


    def parseDef(self, node):
        ven = '' 
        pfx = [] 
        opc = [] 
        opr = []
        cpuid = []
        for def_node in node.childNodes:
            if not def_node.localName:
                continue
            if def_node.localName == 'pfx':
                pfx = def_node.firstChild.data.split();
            elif def_node.localName == 'opc':
                opc = def_node.firstChild.data.split();
            elif def_node.localName == 'opr':
                opr = def_node.firstChild.data.split();
            elif def_node.localName == 'mode':
                pfx.extend( def_node.firstChild.data.split() );
            elif def_node.localName == 'syn':
                pfx.extend( def_node.firstChild.data.split() );
            elif def_node.localName == 'vendor':
                ven = ( def_node.firstChild.data );
            elif def_node.localName == 'class':
                cpuid = def_node.firstChild.data.split()
        return ( pfx, opc, opr, ven, cpuid )

