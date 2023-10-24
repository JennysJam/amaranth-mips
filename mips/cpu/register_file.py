from amaranth import *
from mips.cpu.isa import *

class RegisterFile(Elaboratable):
    """
    RegisterFile abstraction

    Attributes:
        rin (Signal[5]): input, register number to interact with
        write (Signal): input, flag to set to allow for writes
        value (Signal[32]): input, value to be written (ignored if flag=0)
        out (Signal[32]): output, value in register if stored
    """
    def __init__(self):
        self.rin: Signal(5)
        self.write: Signal()
        self.value: Signal(5)
        self.out: Signal(32)

    def elaborate(self, platform):
        m = Module()
        self._memory = Memory(
            width=32,
            depth=31
        )

        with m.If(self.rin == 0):
            m.d.comb += self.out.eq(0)
        with m.Else():
            with m.If(self.write):
                m.d.sync += [
                    self.value.eq(0),
                    self.write.eq(0)
                ]
            m.d.comb += self.out.eq(self._memory)
        return m