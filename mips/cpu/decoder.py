from amaranth import *
import isa

class Decoder(Elaboratable):
    def __init__(self):
        self.opcode = Signal(unsigned(6))
        self.rs: Signal(unsigned(5))
        self.rt = Signal(unsigned(5))
        self.rd = Signal(unsigned(5))
        self.func = Signal(unsigned(6))
        self.shamt = Signal(unsigned(6))
        self.imm = Signal(unsigned(16))
        self.addr = Signal(26)
        pass

    def elaborate(self, platform):
        m = Module()


        return m