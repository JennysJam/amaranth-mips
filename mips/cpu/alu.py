from amaranth import *

from amaranth.sim import Simulator

class ALU(Elaboratable):
    """
    Arithmetic Logic Unit

    """
    def __init__(self):
        # input
        self.rs = Signal(32)
        self.rt = Signal(32)

        # output
        self.rd = Signal(32)
        self.trap = Signal()

    def elaborate(self, platform):
        led = platform.get("led", 1)
        m = Module()
        reg = Signal(33)
        
        m.d.comb += reg.eq(self.rs + self.rt)

        m.d.comb += self.trap.eq(reg[33])
        m.d.comb += self.rd.eq(reg[0:33])

        return m


def simulate(file: str):
    alu = ALU()

    sim = Simulator(alu)

    with sim.write_vcd(file):
        sim.run()
    