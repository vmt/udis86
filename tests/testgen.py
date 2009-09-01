# udis86 - test/testgen.py
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

import os
import sys
import random

if ( len( os.getenv( 'UD_SCRIPT_DIR' ) ) ):
    scriptsPath = os.getenv( 'UD_SCRIPT_DIR' ) + "/scripts"
else:
    scriptsPath = '../scripts'
sys.path.append( scriptsPath );

import ud_optable
import ud_opcode
import testgen_opr

class UdTestGenerator( ud_opcode.UdOpcodeTables ):

    OprTable = []

    ExcludeList = ( 'fcomp3', 'fcom2', 'fcomp5', 'fstp1', 'fstp8', 'fstp9',
                    'fxch4', 'fxch7' )

    def __init__( self ):
        pass

    def generate_yasm( self, mode, seed ):
        random.seed( seed )
        print "[bits %s]" % mode
        for insn in self.InsnTable:
            if insn[ 'mnemonic' ] in self.ExcludeList:
                continue
            if 'inv64' in insn[ 'prefixes' ] and mode == '64':
                continue
            if 'def64' in insn[ 'prefixes' ] and mode != '64':
                continue
            opr = '_'.join( insn[ 'operands' ] )
            if len( opr ):
                if not opr in testgen_opr.OperandSet.keys():
                    print "Warning: no test-case for operand type '%s' (insn=%s)" % ( opr, insn[ 'mnemonic' ] )
                testcase = testgen_opr.OperandSet[ opr ][ mode ]
                if len( testcase ):
                    print "\t%s %s" % ( insn[ 'mnemonic' ], random.choice( testcase ) )

def main():
    generator = UdTestGenerator()
    optableXmlParser = ud_optable.UdOptableXmlParser()
    optableXmlParser.parse( sys.argv[ 1 ], generator.addInsnDef )

    generator.generate_yasm( sys.argv[ 3 ], int( sys.argv[ 2 ] ) )

if __name__ == '__main__':
    main()
