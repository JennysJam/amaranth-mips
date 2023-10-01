from amaranth import *
import isa

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
        self.inst = Signal(32)
        self.opcode = Signal(unsigned(6))
        self.rs: Signal(unsigned(5))
        self.rt = Signal(unsigned(5))
        self.rd = Signal(unsigned(5))
        self.func = Signal(unsigned(6))
        self.shamt = Signal(unsigned(6))
        self.imm = Signal(unsigned(16))
        self.addr = Signal(26)
        pass

    def elaborate(self, platform) -> Module:
        m = Module()
        inst = Signal(isa.Inst)
        
        return m