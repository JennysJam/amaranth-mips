from amaranth import *
from mips.cpu.isa import *

class Decoder(Elaboratable):
    """
    Decoder module that parses a value in and passes all values 
    out.

    Any non-set value are going to default to 0's (this is moreso
    a quirk of Amaranth).

    Attributes:
        inst: input instruction value
        opcode: output opcode value
        rs: output rs register value
        rt: output rt register value
        rd: output rd register value
        func: output func value
        imm: immediate value
        addr: address value
    """
    def __init__(self):
        self.inst = Signal(Instr) 
        self.opcode = Signal(Opcode)
        self.rs = Signal(unsigned(5))
        self.rt = Signal(unsigned(5))
        self.rd = Signal(unsigned(5))
        self.funct = Signal(Funct)
        self.shamt = Signal(unsigned(5))
        self.imm = Signal(unsigned(16))
        self.addr = Signal(26)
        pass

    def elaborate(self, platform):
        m = Module()

        with m.Switch(self.inst.opcode):
            with m.Case(Opcode.SPECIAL):
                m.d.comb += [
                    self.opcode.eq(Opcode.SPECIAL),
                    self.rs.eq(self.inst.data.reg.rs),
                    self.rt.eq(self.inst.data.reg.rt),
                    self.rd.eq(self.inst.data.reg.rd),
                    self.funct.eq(self.inst.data.reg.funct),
                    self.shamt.eq(self.inst.data.reg.shamt)
                ]
            with m.Case(*IMM_OPCODE):
                m.d.comb += [
                    self.opcode.eq(self.inst.opcode),
                    self.rs.eq(self.inst.data.imm.rs),
                    self.rt.eq(self.inst.data.imm.rt),
                    self.imm.eq(self.inst.data.imm.imm)
                ]
            with m.Case(*JMP_OPCODE):
                m.d.comb += [
                    self.opcode.eq(self.inst.opcode),
                    self.addr.eq(self.inst.data.jmp.addr)
                ]
            with m.Default():
                pass

        return m