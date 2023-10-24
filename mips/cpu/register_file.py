from amaranth import *
from mips.cpu.isa import *
from typing import *


class RegisterFile(Elaboratable):
    """
    RegisterFile abstraction

    Attributes:
        rs (Signal(5)): input register number 1
        rt (Signal(5)): input register number 2
        rs_out (Signal(32)): output data signal
        rt_out (Signal(32)): output data location
    """
    def __init__(self, init: Optional[List[int]] =None):
        self.rs = Signal(5)
        self.rt = Signal(5)
        self.rs_out = Signal(32)
        self.rt_out = Signal(32)
        self.mem = Memory(
            width=32,
            depth=31,
            init=init if init else None
        )

    def elaborate(self, platform):
        m = Module()
        m.submodules.rdport1 = rdport1 = self.mem.read_port()
        m.submodules.rdport2 = rdport2 = self.mem.read_port()

        with m.If(self.rs != 0):
            m.d.comb += [
                rdport1.addr.eq(self.rs-1),
                self.rs_out.eq(rdport1.data),
            ]
        with m.Else():
            m.d.comb += self.rs_out.eq(0)
        
        with m.If(self.rt != 0):
            m.d.comb += [
                rdport2.addr.eq(self.rt - 1),
                self.rt_out.eq(rdport2.data)
            ]
        with m.Else():
            m.d.comb += self.rt_out.eq(0)

        return m