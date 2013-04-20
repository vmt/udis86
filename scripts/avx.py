import ud_opcode
import ud_optable
import sys


class UdTestGenerator( ud_opcode.UdOpcodeTables ):
    
    def convt(self):
        ssepfx = { '00' : '', '01' : 'f2', '02': 'f3', '03' : '66' }
        for insn in self.InsnTable:
            if '/sse' in insn['opcext']:
                pp = ssepfx[insn['opcext']['/sse']]
                opc = insn['opcodes']
                m  = insn['opcodes'][0]
                opc.pop(0)
                if opc[0] in ('38', '3a'):
                    m += opc[0]
                    opc.pop(0)
                mnm = insn['mnemonic']
                oprs= insn['operands']
                pfx = []
                for opr in oprs:
                    if opr.startswith('M') or opr.startswith('E'):
                        pfx.append("aso")
                for opr in oprs:
                    if 'R' in opr or 'G' in opr:
                        pfx.append("vex.W")
                if not (mnm.endswith("sd") or mnm.endswith("ss")):
                    pfx.append("vex.L")
                
                if oprs == ['V', 'W']:
                    oprs = ('V', 'H', 'W')
                elif oprs == ['W', 'V']:
                    oprs = ['W', 'H', 'V']
                elif oprs == ['P', 'Q']:
                    oprs = ['V', 'W']
                elif oprs == ['Q', 'P']:
                    oprs = ['W', 'V']
                elif oprs == ['P', 'N']:
                    oprs = ['V', 'U']
                elif oprs == ['M', 'P']:
                    oprs = ['M', 'V']

                print "  <instruction>"
                print "    <mnemonic>v%s</mnemonic>" % mnm
                print "    <pfx>%s</pfx>" % ' '.join(pfx)
                print "    <opc>vex.%s%s %s</opc>" % (pp, m, ' '.join(opc))
                print "    <opr>%s</opr>" % (' '.join(oprs))
                print "    <cpuid>avx</cpuid>"
                print "  </instruction>\n"
            else:
                if 'V' in insn['operands']:
                    assert 0

def main():
    optableXmlParser = ud_optable.UdOptableXmlParser()
    generator = UdTestGenerator()
    optableXmlParser.parse( sys.argv[ 1 ], generator.addInsnDef )

    generator.convt()

if __name__ == '__main__':
    main()
