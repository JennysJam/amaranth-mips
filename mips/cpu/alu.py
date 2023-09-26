from amaranth import *
from amaranth.sim import Simulator, Settle, Delay

from mips.cpu.isa import Funct

import random

class ALU(Elaboratable):
    """
    Arithmetic Logic Unit (only does trapping add)

    """
    def __init__(self):
        # input
        self.rs = Signal(32)
        self.rt = Signal(32)
        self.func = Signal(6)
        # output
        self.rd = Signal(32)
        self.ovf = Signal()

    def elaborate(self, platform):
        m = Module()
        ureg = Signal(33)
        ireg = Signal(33, signed=True)

        with m.Switch(self.func):
            with m.Case(Funct.ADD):
                m.d.comb += ureg.eq(self.rs + self.rt)
                m.d.comb += self.ovf.eq(ureg[-1])
                m.d.comb += self.rd.eq(ureg)
            with m.Case(Funct.ADDU):
                m.d.comb += ureg.eq(self.rs + self.rt)
                m.d.comb += self.rd.eq(ureg)
            with m.Case(Funct.ADDI):
                m.d.comb += ireg.eq(self.rs + self.rt.as_signed())
                m.d.comb += self.ovf.eq(ireg)
                m.d.comb += self.rd.eq(ireg)
            with m.Case(Funct.ADDIU):
                m.d.comb += ireg.eq(self.rs + self.rt.as_signed())
                m.d.comb += self.rd.eq(ireg)

        return m


def simulate(file: str):
    alu = ALU()
    MAX_32U = 0xff_ff_ff_ff
    sim = Simulator(alu)

    def bench():
        test_cases = [
            (1, 2, 3, 0),
            (2, 2, 4, 0),
            (4, 5, 9, 0),
            (8, 8, 16, 0),
            (MAX_32U, 1, 0, 1)
        ]
        for x, y, res, should_trap in test_cases:
                print(f"Testing {x:016x} + {y:016x} == {res:016x} {'(traps)' if should_trap else ''}")

                yield alu.rs.eq(x)
                yield alu.rt.eq(y)
                yield Settle()

                rt = yield alu.rs
                rs = yield alu.rt
                rd = yield alu.rd
                trap = yield alu.ovf
                if should_trap:
                    assert trap == 1,\
                        f"Trap {trap} should have triggered didn't on rt:{rs:016x}({x:016x}) + rd:{rt:016x}({y:016x}) => rd:{rd:016x}"
                else:
                    assert rd == res,\
                        f"rt:{rs:016x}({x:016x}) + rd:{rt:016x}({y:016x}) should be {res:016x} but was instead {rd:016x}"
                
                yield Delay(1e-6)

    #sim.add_clock(1e-6) # Is this write for ICE?
    sim.add_process(bench)
    

    with sim.write_vcd(file):
        sim.run()
