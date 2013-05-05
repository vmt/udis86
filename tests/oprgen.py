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

if ( len( os.getenv( 'UD_SCRIPT_DIR', "" ) ) ):
    scriptsPath = os.getenv( 'UD_SCRIPT_DIR' ) + "/scripts"
else:
    scriptsPath = '../scripts'
sys.path.append( scriptsPath );

import ud_optable
import ud_opcode

def bits2name(bits):
    bits2name_map = {
         8 : "byte",
        16 : "word",
        32 : "dword",
        64 : "qword",
        80 : "tword",
    }
    return bits2name_map[bits]


class UdTestGenerator( ud_opcode.UdOpcodeTables ):

    OprTable = []

    ExcludeList = ( 'fcomp3', 'fcom2', 'fcomp5', 'fstp1', 'fstp8', 'fstp9',
                    'fxch4', 'fxch7', 'nop', 'xchg', 'movd',
                    'pmulhrw' # yasm bug
                    )

    def __init__(self, mode):
        self.mode = mode
        pass

    def OprMem(self, size=None, cast=False):
        choices = []
        if self.mode < 64:
            choices = ["[bx+si+0x1234]",
                       "[bx+0x10]", 
                       "[bp+di+0x27]",
                       "[di+0x100]"]
        choices.extend(("[eax+ebx]", "[ebx+ecx*4]", 
                        "[ebp+0x10]"))
        if self.mode == 64:
            choices.extend(("[rax+rbx]", "[rbx+r8-0x10]"))
        addr = random.choice(choices)
        if cast and size is not None:
            addr = "%s %s" % (bits2name(size), addr)
        return addr

    def OprImm(self, size, cast=False):
        imm = "0x%x" % random.randint(2, 1 << (size - 1))
        if cast and size is not None:
            imm = "%s %s" % (bits2name(size), imm)
        return imm

    def Gpr(self, size):
        if size == 8:
            choices = ['al', 'cl']
            if self.mode == 64:
                choices.extend(['sil', 'r10b'])
        elif size == 16:
            choices = ['ax', 'bp', 'dx']
            if self.mode == 64:
                choices.extend(['r8w', 'r14w'])
        elif size == 32:
            choices = ['eax', 'ebp', 'edx']
            if self.mode == 64:
                choices.extend(['r10d', 'r12d'])
        elif size == 64:
            choices = ['rax', 'rsi', 'rsp']
            if self.mode == 64:
                choices.extend(['r9', 'r13'])
        return random.choice(choices)

    def Xmm(self):
        r = 16 if self.mode == 64 else 8
        return "xmm%d" % random.choice(range(r))

    def Mmx(self):
        return "mm%d" % random.choice(range(8))

    def Modrm_RM_GPR(self, size, cast=False):
        return random.choice([self.Gpr(size),
                              self.OprMem(size=size, cast=cast)])

    def Modrm_RM_XMM(self, size, cast=False):
        return random.choice([self.Xmm(),
                              self.OprMem(size=size, cast=cast)])
   
    def OprRxb(self, n):
        regs = [ 'al', 'cl', 'dl', 'bl' ]
        if self.mode == 64 and random.choice((False, True)):
            regs += [ 'spl', 'bpl', 'sil', 'dil',
                      'r8b', 'r9b', 'r10b', 'r11b',
                      'r12b', 'r13b', 'r14b', 'r15b' ]
            n |= random.choice((0, 8))
        else: 
            regs += [ 'ah', 'ch', 'dh', 'bh' ]
        return regs[n]

    def OprRxw(self, n):
        regs = [ 'ax', 'cx', 'dx', 'bx', 'sp', 'bp', 'si', 'di' ]
        if self.mode == 64 and random.choice((False, True)):
            regs += [ 'r8w', 'r9w', 'r10w', 'r11w',
                      'r12w', 'r13w', 'r14w', 'r15w' ]
            n |= random.choice((0, 8))
        return regs[n]

    def OprRxd(self, n):
        regs = [ 'eax', 'ecx', 'edx', 'ebx', 'esp', 'ebp', 'esi', 'edi' ]
        if self.mode == 64 and random.choice((False, True)):
            regs += [ 'r8d', 'r9d', 'r10d', 'r11d',
                      'r12d', 'r13d', 'r14d', 'r15d' ]
            n |= random.choice((0, 8))
        return regs[n]

    def OprRxq(self, n):
        regs = [ 'rax', 'rcx', 'rdx', 'rbx',
                 'rsp', 'rbp', 'rsi', 'rdi',
                 'r8',  'r9',  'r10', 'r11', 
                 'r12', 'r13', 'r14', 'r15' ]
        n |= random.choice((0, 8))
        return regs[n]

    def OprRxv(self, n):
        choices = [ self.OprRxw(n), self.OprRxd(n) ]
        if self.mode == 64:
            choices.append(self.OprRxq(n))
        return random.choice(choices)

    def OprRxz(self, n):
        choices = [ self.OprRxw(n), self.OprRxd(n) ]
        return random.choice(choices)

    def OprRxy(self, n):
        choices = [ self.OprRxd(n) ]
        if self.mode == 64:
            choices.append(self.OprRxq(n))
        return random.choice(choices)

    Opr_R0b = lambda s: s.OprRxb(0);
    Opr_R1b = lambda s: s.OprRxb(1);
    Opr_R2b = lambda s: s.OprRxb(2);
    Opr_R3b = lambda s: s.OprRxb(3);
    Opr_R4b = lambda s: s.OprRxb(4);
    Opr_R5b = lambda s: s.OprRxb(5);
    Opr_R6b = lambda s: s.OprRxb(6);
    Opr_R7b = lambda s: s.OprRxb(7);

    Opr_R0y = lambda s: s.OprRxy(0);
    Opr_R1y = lambda s: s.OprRxy(1);
    Opr_R2y = lambda s: s.OprRxy(2);
    Opr_R3y = lambda s: s.OprRxy(3);
    Opr_R4y = lambda s: s.OprRxy(4);
    Opr_R5y = lambda s: s.OprRxy(5);
    Opr_R6y = lambda s: s.OprRxy(6);
    Opr_R7y = lambda s: s.OprRxy(7);

    Opr_R0v = lambda s: s.OprRxv(0);
    Opr_R1v = lambda s: s.OprRxv(1);
    Opr_R2v = lambda s: s.OprRxv(2);
    Opr_R3v = lambda s: s.OprRxv(3);
    Opr_R4v = lambda s: s.OprRxv(4);
    Opr_R5v = lambda s: s.OprRxv(5);
    Opr_R6v = lambda s: s.OprRxv(6);
    Opr_R7v = lambda s: s.OprRxv(7);

    Opr_R0z = lambda s: s.OprRxz(0);
    Opr_R1z = lambda s: s.OprRxz(1);
    Opr_R2z = lambda s: s.OprRxz(2);
    Opr_R3z = lambda s: s.OprRxz(3);
    Opr_R4z = lambda s: s.OprRxz(4);
    Opr_R5z = lambda s: s.OprRxz(5);
    Opr_R6z = lambda s: s.OprRxz(6);
    Opr_R7z = lambda s: s.OprRxz(7);

    def Insn_Av(self):
        return random.choice([("word 0x100:0x100",), ("dword 0x100:0xfaddbc",)])

    def Opr_R(self):
        if self.mode == 64:
            return self.OprRxq(random.choice(range(8)))
        return self.OprRxd(random.choice(range(8)));

    def Opr_C(self):
        return "cr3"

    def Opr_D(self):
        return "dr0"

    def Opr_S(self):
        return "fs"

    def Opr_ST0(self):
        return "st0"

    def Opr_ST1(self):
        return "st1"

    def Opr_ST2(self):
        return "st2"

    def Opr_ST3(self):
        return "st3"

    def Opr_ST4(self):
        return "st4"

    def Opr_ST5(self):
        return "st5"

    def Opr_ST6(self):
        return "st6"

    def Opr_ST7(self):
        return "st7"

    def Opr_CS(self):
        return "cs"

    def Opr_GS(self):
        return "gs"

    def Opr_ES(self):
        return "es"

    def Opr_FS(self):
        return "fs"

    def Opr_DS(self):
        return "ds"

    def Opr_SS(self):
        return "ss"

    def Opr_Ib(self, cast=False):
        return self.OprImm(8, cast=cast)

    def Opr_Iw(self, cast=False):
        return self.OprImm(16, cast=cast)

    def Opr_Id(self, cast=False):
        return self.OprImm(32, cast=cast)

    def Opr_Iq(self, cast=False):
        return self.OprImm(64, cast=cast)

    def Opr_Iz(self, cast=False):
        return random.choice((self.OprImm(16, cast=cast),
                              self.OprImm(32, cast=cast)))
    Opr_sIz = Opr_Iz

    def Opr_Iw(self, cast=False):
        return self.OprImm(16, cast=cast)

    def Opr_I1(self, cast=False):
        return "1"

    def Opr_eAX(self):
        return random.choice(['ax', 'eax'])

    def Opr_rAX(self):
        choices = ['ax', 'eax']
        if self.mode == 64:
            choices.append('rax')
        return random.choice(choices)

    def Insn_rAX_Iz(self):
        choices = [('ax', self.Opr_Iw()), ('eax', self.Opr_Id())]
        if self.mode == 64:
            choices.append(('rax', self.Opr_Id()))
        return random.choice(choices)
    Insn_rAX_sIz = Insn_rAX_Iz

    def Insn_Rxv_Iv(self, n):
        choices = [(self.OprRxw(n), self.Opr_Iw()),
                   (self.OprRxd(n), self.Opr_Id())]
        if self.mode == 64:
            choices.append((self.OprRxq(n), self.Opr_Iq()))
        return random.choice(choices)

    Insn_R0v_Iv = lambda s: s.Insn_Rxv_Iv(0)
    Insn_R1v_Iv = lambda s: s.Insn_Rxv_Iv(1)
    Insn_R2v_Iv = lambda s: s.Insn_Rxv_Iv(2)
    Insn_R3v_Iv = lambda s: s.Insn_Rxv_Iv(3)
    Insn_R4v_Iv = lambda s: s.Insn_Rxv_Iv(4)
    Insn_R5v_Iv = lambda s: s.Insn_Rxv_Iv(5)
    Insn_R6v_Iv = lambda s: s.Insn_Rxv_Iv(6)
    Insn_R7v_Iv = lambda s: s.Insn_Rxv_Iv(7)

    def Insn_Rxv_rAX(self, n):
        choices = [(self.OprRxw(n), "ax"),
                   (self.OprRxd(n), "eax")]
        if self.mode == 64:
            choices.append((self.OprRxq(n), "rax"))
        return random.choice(choices)

    Insn_R0v_rAX = lambda s: s.Insn_Rxv_rAX(0)
    Insn_R1v_rAX = lambda s: s.Insn_Rxv_rAX(1)
    Insn_R2v_rAX = lambda s: s.Insn_Rxv_rAX(2)
    Insn_R3v_rAX = lambda s: s.Insn_Rxv_rAX(3)
    Insn_R4v_rAX = lambda s: s.Insn_Rxv_rAX(4)
    Insn_R5v_rAX = lambda s: s.Insn_Rxv_rAX(5)
    Insn_R6v_rAX = lambda s: s.Insn_Rxv_rAX(6)
    Insn_R7v_rAX = lambda s: s.Insn_Rxv_rAX(7)

    def Opr_Gb(self):
        return self.Gpr(8)

    def Opr_Gw(self):
        return self.Gpr(16)

    def Opr_Gd(self):
        return self.Gpr(32)

    def Opr_Gq(self):
        return self.Gpr(64)

    def Opr_Gz(self):
        return random.choice([self.Gpr(16), self.Gpr(32)])

    def Opr_Gv(self):
        choices = [self.Gpr(16), self.Gpr(32)]
        if self.mode == 64:
            choices.append(self.Gpr(64))
        return random.choice(choices)

    def Opr_Gy(self):
        choices = [self.Gpr(32)]
        if self.mode == 64:
            choices.append(self.Gpr(64))
        return random.choice(choices)

    def Opr_M(self):
        return self.OprMem();

    def Opr_U(self):
        return self.Xmm();

    def Opr_N(self):
        return self.Mmx();

    def Opr_Mb(self, cast=False):
        return self.OprMem(size=8, cast=cast);

    def Opr_Mw(self, cast=False):
        return self.OprMem(size=16, cast=cast);

    def Opr_Md(self, cast=False):
        return self.OprMem(size=32, cast=cast);

    def Opr_Mq(self, cast=False):
        return self.OprMem(size=64, cast=cast);

    def Opr_Mt(self, cast=True):
        return self.OprMem(size=80, cast=cast);

    def Opr_MwRd(self, cast=True):
        return random.choice((self.Opr_Mw(cast=cast), self.Opr_Gd()))

    def Opr_MwRv(self, cast=False):
        return random.choice((self.Opr_Mw(cast=cast), self.Opr_Gv()))

    def Opr_MwRy(self, cast=True):
        return random.choice((self.Opr_Mw(cast=cast), self.Opr_Gy()))

    def Opr_MdRy(self, cast=False):
        return random.choice((self.Opr_Md(cast=cast), self.Opr_Gy()))

    def Opr_MbRv(self, cast=False):
        return random.choice((self.Opr_Mb(cast=cast), self.Opr_Gv()))

    def Opr_MbRd(self, cast=False):
        return random.choice((self.Opr_Mb(cast=cast), self.Opr_Gd()))

    def Opr_MwRw(self, cast=False):
        return random.choice((self.Opr_Mw(cast=cast), self.Opr_Gw()))

    def Opr_MwU(self, cast=False):
        return random.choice((self.Opr_Mw(cast=cast), self.Xmm()))

    def Opr_MdU(self, cast=False):
        return random.choice((self.Opr_Md(cast=cast), self.Xmm()))

    def Opr_MqU(self, cast=False):
        return random.choice((self.Opr_Mq(cast=cast), self.Xmm()))

    def Insn_V_MwU(self, cast=False):
        return (self.Opr_V(), self.Opr_MwU(cast=True))

    def Insn_V_MdU(self, cast=False):
        return (self.Opr_V(), self.Opr_MdU(cast=True))

    def Insn_V_MqU(self, cast=False):
        return (self.Opr_V(), self.Opr_MqU(cast=True))

    def Insn_MbRv(self):
        return [self.Opr_MbRv(cast=True)]

    def Insn_MbRv_V_Ib(self):
        return [self.Opr_MbRv(cast=True), self.Opr_V(), self.Opr_Ib()]

    def Insn_V_MbRd_Ib(self):
        return [self.Opr_V(), self.Opr_MbRd(cast=True), self.Opr_Ib()]

    def Insn_MwRv(self):
        return [self.Opr_MwRv(cast=True)]

    def Insn_MwRd_V_Ib(self):
        return [self.Opr_MwRd(cast=False), self.Opr_V(), self.Opr_Ib()]

    def Insn_S_MwRv(self):
        if self.mode == 64:
            return [self.Opr_S(), self.Opr_MwRd(cast=False)]
        if self.mode == 16:
            return [self.Opr_S(), self.Opr_MwRw(cast=False)]
        if self.mode == 32:
            return [self.Opr_S(), self.Opr_MwRd(cast=False)]

    def Insn_Mw(self):
        return [self.Opr_Mw(cast=True)]

    def Insn_Md(self):
        return [self.Opr_Md(cast=True)]

    def Insn_Mq(self):
        return [self.Opr_Mq(cast=True)]

    def Opr_Eb(self, cast=False):
        return self.Modrm_RM_GPR(8, cast=cast)

    def Opr_Ew(self, cast=False):
        return self.Modrm_RM_GPR(16, cast=cast)

    def Opr_Ed(self, cast=False):
        return self.Modrm_RM_GPR(32, cast=cast)

    def Opr_Eq(self, cast=False):
        return self.Modrm_RM_GPR(64, cast=cast)

    def Opr_Ey(self, cast=False):
        choices = [self.Modrm_RM_GPR(32, cast=cast)]
        if self.mode == 64:
            choices.append(self.Modrm_RM_GPR(64, cast=cast))
        return random.choice(choices)

    def Insn_Fv(self):
        return ("far "+ self.Opr_Mv(cast=True),)

    def Insn_V_Ew_Ib(self):
        return self.Opr_V(), self.Opr_Ew(cast=True), self.Opr_Ib()

    def Insn_V_Eq_Ib(self):
        return self.Opr_V(), self.Opr_Eq(cast=True), self.Opr_Ib()

    def Insn_V_Mo(self):
        return self.Opr_V(), self.Opr_M()

    def Insn_V_Md_Ib(self):
        return self.Opr_V(), self.Opr_Md(cast=True), self.Opr_Ib()

    def Insn_V_Ed_Ib(self):
        return self.Opr_V(), self.Opr_Ed(cast=True), self.Opr_Ib()

    def Insn_P_Ew_Ib(self):
        return self.Opr_P(), self.Opr_Ew(cast=True), self.Opr_Ib()

    def Insn_V_Ey(self):
        return self.Opr_V(), self.Opr_Ey(cast=True)

    def Insn_Ey_V(self):
        x, y = self.Insn_V_Ey()
        return y, x

    def Insn_P_Ey(self):
        return self.Opr_P(), self.Opr_Ey(cast=True)

    def Insn_Ey_P(self):
        x, y = self.Insn_P_Ey()
        return y, x

    def Opr_Mv(self, cast=False):
        choices = [self.Opr_Mw(cast), self.Opr_Md(cast)]
        if self.mode == 64:
            choices.append(self.Opr_Mq(cast))
        return random.choice(choices)

    def Opr_Ev(self, cast=False):
        choices = [self.Opr_Ew(cast), self.Opr_Ed(cast)]
        if self.mode == 64:
            choices.append(self.Opr_Eq(cast))
        return random.choice(choices)

    def Insn_Ev(self):
        choices = [self.Modrm_RM_GPR(16, cast=True),
                   self.Modrm_RM_GPR(32, cast=True)]
        if self.mode == 64:
            choices.append(self.Modrm_RM_GPR(64, cast=True))
        return [random.choice(choices)]

    def Opr_V(self):
        return self.Xmm()

    def Opr_W(self):
        return random.choice([self.Xmm(), self.OprMem(size=128)])

    def Opr_P(self):
        return self.Mmx()

    def Opr_Q(self, cast=False):
        return random.choice([self.Mmx(), self.OprMem(size=64, cast=cast)])

    def Opr_CL(self):
        return "cl"

    def Opr_AL(self):
        return "al"

    def Opr_Ob(self):
        return "[0x100]"

    def Insn_rAX_Ov(self):
        choices = [ ("ax", "[0x100]"), ("eax", "[0x1000]") ]
        if self.mode == 64:
            choices.append(("rax", "[0x1223221]"))
        return random.choice(choices)

    def Insn_Ov_rAX(self):
        x, y = self.Insn_rAX_Ov()
        return y, x

    def Opr_AX(self):
        return "ax"

    def Opr_DX(self):
        return "dx"

    def Insn_Eb_CL(self):
        return self.Opr_Eb(cast=True), self.Opr_CL()

    def Insn_Ev_CL(self):
        return self.Opr_Ev(cast=True), self.Opr_CL()

    def Insn_Eb(self):
        return [self.Modrm_RM_GPR(size=8, cast=True)]

    def Insn_Ew(self):
        return [self.Modrm_RM_GPR(size=16, cast=True)]

    def Insn_Ev_Gv(self):
        choices = [ (self.Opr_Ew(), self.Opr_Gw()),
                    (self.Opr_Ed(), self.Opr_Gd()) ]
        if self.mode == 64:
            choices.append((self.Opr_Eq(), self.Opr_Gq()))
        return random.choice(choices)

    def Insn_Ev_Gy(self):
        choices = [ (self.Opr_Ew(), self.Opr_Gd()),
                    (self.Opr_Ed(), self.Opr_Gd()) ]
        if self.mode == 64:
            choices.append((self.Opr_Eq(), self.Opr_Gq()))
        return random.choice(choices)

    def Insn_Ev_Gv_CL(self):
        x, y = self.Insn_Ev_Gv();
        return x, y, self.Opr_CL()

    def Insn_Gv_Ev_CL(self):
        x, y = self.Insn_Ev_Gv();
        return y, x, self.Opr_CL()

    def Insn_Gv_Ev_Ib(self):
        x, y = self.Insn_Ev_Gv();
        return y, x, self.Opr_Ib(cast=False)
    Insn_Gv_Ev_sIb = Insn_Gv_Ev_Ib

    def Insn_Gv_Ev_Iz(self):
        choices = [ (self.Opr_Gw(), self.Opr_Ew(), self.Opr_Iw()),
                    (self.Opr_Gd(), self.Opr_Ed(), self.Opr_Id()) ]
        if self.mode == 64:
            choices.append((self.Opr_Gq(), self.Opr_Eq(), self.Opr_Iz()))
        return random.choice(choices)

    def Insn_Ev_Ib(self):
        return self.Opr_Ev(cast=True), self.Opr_Ib()
    Insn_Ev_sIb = Insn_Ev_Ib

    def Insn_Gq_Ed(self):
        return self.Opr_Gq(), self.Opr_Ed(cast=True)

    def Insn_Gy_Eb(self):
        return self.Opr_Gy(), self.Opr_Eb(cast=True)

    def Insn_Gy_Ew(self):
        return self.Opr_Gy(), self.Opr_Ew(cast=True)

    def Insn_Ev_Iz(self):
        choices = [(self.Opr_Ew(cast=True), self.Opr_Iw()),
                   (self.Opr_Ed(cast=True), self.Opr_Id())]
        if self.mode == 64:
            choices.append((self.Opr_Eq(cast=True), self.Opr_Id()))
        return random.choice(choices)
    Insn_Ev_sIz = Insn_Ev_Iz

    def Insn_Gv_Ev(self):
        x, y = self.Insn_Ev_Gv();
        return (y, x)

    def Insn_Gy_Ev(self):
        x, y = self.Insn_Ev_Gy();
        return (y, x)

    def Insn_Gv_Eb(self):
        return (self.Opr_Gv(), self.Opr_Eb(cast=True))

    def Insn_Gv_Ew(self):
        choices = [(self.Opr_Gw(), self.Opr_Ew(cast=False)),
                   (self.Opr_Gd(), self.Opr_Ew(cast=True))]
        if self.mode == 64:
            choices.append((self.Opr_Gq(), self.Opr_Ew(cast=True)))
        return random.choice(choices)

    def Insn_V_Q(self):
        return [self.Opr_V(), self.Opr_Q(cast=True)]

    def Insn_Eb_Ib(self):
        return (self.Opr_Eb(cast=True), self.Opr_Ib(cast=False))

    def Insn_Eb_I1(self):
        return (self.Opr_Eb(cast=True), self.Opr_I1())

    def Insn_Ev_I1(self):
        return (self.Opr_Ev(cast=True), self.Opr_I1())

    def Insn_Ev_Ib(self):
        return (self.Opr_Ev(cast=True), self.Opr_Ib(cast=False))
    Insn_Ev_sIb = Insn_Ev_Ib

    def Insn_Ev_Gv_Ib(self):
        choices = [ (self.Opr_Ew(), self.Opr_Gw(), self.Opr_Ib(cast=False)),
                    (self.Opr_Ed(), self.Opr_Gd(), self.Opr_Ib(cast=False)) ]
        if self.mode == 64:
            choices.append(
                    (self.Opr_Eq(), self.Opr_Gq(), self.Opr_Ib(cast=False)) )
        return random.choice(choices)
    Insn_Ev_Gv_sIb = Insn_Ev_Gv_Ib

    def Insn_Ev_V_Ib(self):
        return (self.Opr_Ev(cast=True), self.Opr_V(), self.Opr_Ib(cast=False))

    def Insn_Ed_V_Ib(self):
        return (self.Opr_Ed(cast=False), self.Opr_V(), self.Opr_Ib(cast=False))

    def Insn_Ew_V_Ib(self):
        return (self.Opr_Ew(cast=True), self.Opr_V(), self.Opr_Ib(cast=False))

    def generate_yasm( self, mode, seed ):
        opr_combos = {}
        random.seed( seed )
        print "[bits %s]" % mode
        for insn in self.InsnTable:
            if insn[ 'mnemonic' ] in self.ExcludeList:
                continue
            if insn[ 'vendor' ] == 'intel':
                continue
            if '/m' in insn['opcext']:
                mode = insn['opcext']['/m']
                if ( (mode == '00' and self.mode == 64) or
                     (mode == '01' and self.mode != 64) ):
                    continue
            if '/o' in insn['opcext']:
                osize = insn['opcext']['/o']
                if (osize == '02' and self.mode != 64):
                    continue
            if 'def64' in insn[ 'prefixes' ] and mode != '64':
                continue

            if len(insn['operands']) == 0:
                continue
                # print "\t%s" % insn['mnemonic']

            if ( "Jb" in insn['operands'] or
                 "Jz" in insn['operands'] ):
                continue

            fusedName = '_'.join(insn['operands'])
            if fusedName not in opr_combos:
                opr_combos[fusedName] = { 'covered' : False, 'freq' : 0 }
            opr_combos[fusedName]['freq'] += 1

            fn = getattr(self, "Insn_" + fusedName , None)
            if fn is not None:
                operands = ", ".join(fn())
            else: 
                oprgens = [ getattr(self, "Opr_" + opr, None) 
                                for opr in insn['operands'] ]
                if None not in oprgens:
                    operands = ", ".join([ oprgen() for oprgen in oprgens ])
                else:
                    operands = None
            if operands is not None:
                print "\t%s %s" % (insn['mnemonic'], operands)
                opr_combos[fusedName]['covered'] = True

        # stats
        total = 0
        covered = 0
        for combo in sorted(opr_combos, key=lambda k: opr_combos[k]['freq']):
            total += 1
            is_covered = opr_combos[combo]['covered']
            covered += (1 if is_covered else 0)
            if not is_covered:
                sys.stderr.write("==> %12s : %5d\n" % 
                                    (combo, opr_combos[combo]['freq']))
        sys.stderr.write("MODE%s: Coverage = %d / %d (%d%%)\n" % 
                        (self.mode, covered, total, (100 * covered / total)))

def main():
    generator = UdTestGenerator(int(sys.argv[3]))
    optableXmlParser = ud_optable.UdOptableXmlParser()
    optableXmlParser.parse( sys.argv[ 1 ], generator.addInsnDef )

    generator.generate_yasm( sys.argv[ 3 ], int( sys.argv[ 2 ] ) )

if __name__ == '__main__':
    main()
